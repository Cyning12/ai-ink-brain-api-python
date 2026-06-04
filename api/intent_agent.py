from __future__ import annotations

import asyncio
from collections import OrderedDict
import hashlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass, replace
from typing import Any, Literal

from openai import APIConnectionError, APITimeoutError, InternalServerError, OpenAI, RateLimitError
from openai import APIStatusError

from .intent_hints import build_intent_hints_prompt_block, load_resolved_hints
from .intent_router import decide_intent as decide_intent_v1
from .rag_env import openai_siliconflow_client
from .text2sql_core import is_text2sql_intent
from .tools import Tool, tool_mode_map


ToolName = Literal["rag_search", "text2sql_query", "direct_answer"]
V1Mode = Literal["rag", "text2sql", "no_data"]


_logger = logging.getLogger(__name__)

_VOLATILE_RAW_KEYS = frozenset({"cache", "cache_key_hash", "latency_ms", "llm_prompts"})


class LRUCache:
    """IntentDecision 缓存：TTL 到期失效 + 超容量 LRU 淘汰。"""

    def __init__(self, *, maxsize: int, ttl_s: float) -> None:
        self._maxsize = maxsize
        self._ttl_s = ttl_s
        self._items: "OrderedDict[str, tuple[float, Any]]" = OrderedDict()

    def clear(self) -> None:
        self._items.clear()

    def get(self, key: str) -> Any | None:
        now = time.time()
        it = self._items.get(key)
        if not it:
            return None
        expires_at, val = it
        if expires_at <= now:
            try:
                del self._items[key]
            except KeyError:
                pass
            return None
        # refresh LRU
        self._items.move_to_end(key)
        return val

    def set(self, key: str, val: Any) -> None:
        expires_at = time.time() + self._ttl_s
        self._items[key] = (expires_at, val)
        self._items.move_to_end(key)
        while len(self._items) > self._maxsize:
            self._items.popitem(last=False)


# 全局 Intent 缓存：maxsize/TTL 与任务单 P1-C 对齐
_intent_cache: LRUCache = LRUCache(maxsize=1000, ttl_s=300.0)


def clear_intent_cache() -> None:
    """供基准脚本 / 测试做「冷启动」轮次清空缓存。"""
    _intent_cache.clear()


def _debug_intent_cache_enabled() -> bool:
    raw = (os.getenv("DEBUG_INTENT_CACHE", "") or "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def _intent_history_tail_for_hash(history: list[dict[str, Any]]) -> list[dict[str, str]]:
    """最近 3 轮对话：最多 6 条 user/assistant 消息，仅 role + content。"""
    tail = (history or [])[-6:]
    out: list[dict[str, str]] = []
    for m in tail:
        role = str(m.get("role", "") or "")
        content = str(m.get("content", "") or "")
        out.append({"role": role, "content": content})
    return out


def compute_history_hash(history: list[dict[str, Any]] | None) -> str:
    """稳定 history 指纹：JSON sort_keys + sha256 前 16 hex。"""
    normalized = _intent_history_tail_for_hash(history or [])
    payload = json.dumps(normalized, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _intent_composite_cache_key(*, query: str, history: list[dict[str, Any]] | None) -> str:
    """缓存主键：history_hash + query，不同 history 不会共用条目。"""
    hh = compute_history_hash(history)
    return f"{hh}\x1f{(query or '').strip()}"


def _cache_key_obs_hash(composite_key: str) -> str:
    """可观测短哈希：不暴露 query 明文。"""
    return hashlib.sha256(composite_key.encode("utf-8")).hexdigest()[:16]


def _raw_response_for_cache_store(raw: dict[str, Any]) -> dict[str, Any]:
    """写入缓存前去掉本轮可观测字段与大段 prompt，避免污染命中副本。"""
    return {k: v for k, v in raw.items() if k not in _VOLATILE_RAW_KEYS}


def _log_intent_cache_line(*, event: str, key_hash: str, latency_ms: int) -> None:
    if not _debug_intent_cache_enabled():
        return
    _logger.info("[intent-cache] %s key_hash=%s latency_ms=%s", event, key_hash, latency_ms)


@dataclass(frozen=True)
class StructuredSignals:
    """用于 gating 的结构化信号（关键约束：RAG_RETRIEVE_EMPTY 的 SQL fallback 必须依赖这些信号）。"""

    llm_prefers_sql: bool
    has_aggregation_signals: bool


@dataclass(frozen=True)
class IntentDecision:
    tool: ToolName
    mode: V1Mode
    reasoning: str  # 用户级 1-2 句话摘要
    reasoning_full: str  # 内部级，用于日志/调试
    confidence: float
    fallback: ToolName | None
    structured_signals: StructuredSignals
    raw_response: dict[str, Any]


def _intent_decision_for_cache_store(d: IntentDecision) -> IntentDecision:
    return replace(d, raw_response=_raw_response_for_cache_store(dict(d.raw_response)))


def _attach_cache_observability(
    d: IntentDecision,
    *,
    cache: Literal["hit", "miss"],
    cache_key_hash: str,
    latency_ms: int,
) -> IntentDecision:
    merged = {**dict(d.raw_response), "cache": cache, "cache_key_hash": cache_key_hash, "latency_ms": latency_ms}
    return replace(d, raw_response=merged)


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _has_aggregation_keywords(query: str) -> bool:
    q = (query or "").lower()
    needles = (
        "多少",
        "金额",
        "收入",
        "支出",
        "人数",
        "数量",
        "总数",
        "平均",
        "最大",
        "最小",
        "top",
        "排行",
        "排名",
        "趋势",
        "对比",
        "分组",
        "group by",
        "count",
        "sum",
        "avg",
    )
    return any(n in q for n in needles)


def _fallback_tool_by_low_confidence(tool: ToolName) -> ToolName:
    # 按总纲的“Intent 低置信度 fallback”映射
    if tool == "text2sql_query":
        return "rag_search"
    if tool == "rag_search":
        return "direct_answer"
    return "rag_search"


def _map_v1_mode_to_tool(mode: str) -> ToolName:
    m = (mode or "").strip().lower()
    if m == "text2sql":
        return "text2sql_query"
    if m == "rag":
        return "rag_search"
    return "direct_answer"


def _extract_json_obj(text: str) -> dict[str, Any] | None:
    # 仅做稳健提取：找到第一个 {...} 区块解析
    s = text or ""
    m = re.search(r"\{[\s\S]*\}", s)
    if not m:
        return None
    raw = m.group(0)
    try:
        obj = json.loads(raw)
    except Exception:  # noqa: BLE001
        return None
    if isinstance(obj, dict):
        return obj
    return None


async def _llm_decide_v2(
    *,
    oai: OpenAI,
    query: str,
    history: list[dict[str, Any]],
    tools: list[Tool],
    timeout_s: float,
    capture_prompts: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]] | None]:
    # 让 LLM 按 spec 输出 tool/reasoning/confidence（并尽量使用结构化 JSON）
    tools_desc = "\n\n".join([f"- {t.name}: {t.description}" for t in tools])
    # 与 compute_history_hash 的「最近 6 条」对齐，避免多轮指代时上下文过短
    history_block = "\n".join(
        [f"{m.get('role', '?')}: {str(m.get('content', ''))[:200]}" for m in (history or [])[-6:]]
    ).strip() or "无历史对话"

    hints_block = build_intent_hints_prompt_block(load_resolved_hints()).strip()
    hints_section = f"\n\n{hints_block}\n" if hints_block else ""

    prompt = f"""你是 ChatBI V2 的意图识别器：在下列工具中选**恰好一个**，用于本仓库/本产品的对话路由（评测集亦按此口径）。

## 可用工具（描述以注册表为准）
{tools_desc}

## 总原则

- **text2sql_query**：用户要**本库业务数据**的具体数值/排名/趋势/分组统计，且应由数据库查询给出答案。
- **rag_search**：需要**项目内文档、规范、任务单、架构说明、评测口径、错误码约定、实现细节**等；或问题明显落在「本仓库怎么说/怎么做」而非百科通识一句带过。
- **direct_answer**：**不依赖**内部文档即可完成——翻译、润色、创作、头脑风暴、纯算法题/语法教学、与当前产品/仓库无关的通识科普等。
{hints_section}
## 「通用知识」vs「须查资料」（易错点）

下列主题若**未**明确说「只要高中数学定义、不要项目文档」，在本产品中默认走 **rag_search**（便于对齐内部文档与评测口径）：

- 指标与评测：**macro-F1**、**confusion matrix**、准确率/Precision/Recall、分桶统计等；
- 工程约束：**CI**、**stub**、零外呼门禁、**P50/P95** 基准写法；
- 仓库与规范：**_tech_graph**、**intent_router**、**Supabase** 在本项目中的错误处理约定等。

若用户只要**与项目无关**的通识（例：「用通俗语言解释量子计算」），选 **direct_answer**。

## 多轮对话

- 必须结合 **历史对话** 做指代消解：「它/那/这个」继承上文主题。
- 若上文在讨论 **Text2SQL / 销售额 / 查库**，本轮问「**要不要查数据库**」「**是否要走 SQL**」「路由边界」等——属于**产品能力/路由说明**，选 **rag_search**（查文档说明），**不要**因字面像常识而选 direct_answer。
- 若上文是写作/翻译/生成示例代码，本轮续写、改写语气、再要例子——多为 **direct_answer**。

## 与 text2sql 的边界

| 用户问题 | 选择 |
|---------|------|
| 「昨天销售额是多少」 | **text2sql_query**（要真实数据） |
| 「怎么统计 heros 表」且明显教写法、不要执行 | **direct_answer** |
| 「heros 表有哪些字段」 | **rag_search** |

## Few-shot（短）

Q: 昨天销售额是多少？
{{"tool": "text2sql_query", "reasoning": "需要查库得到金额", "confidence": 0.95}}

Q: 如何计算 confusion matrix
{{"tool": "rag_search", "reasoning": "评测/文档口径，宜检索项目内说明", "confidence": 0.9}}

Q: 解释一下量子计算，用通俗语言
{{"tool": "direct_answer", "reasoning": "与仓库无关的通识解释", "confidence": 0.88}}

[历史]
user: 昨天销售额是多少
assistant: 我可以通过 Text2SQL 去查询……
user: 那需要查数据库吗
{{"tool": "rag_search", "reasoning": "结合上文仍在谈查数路由，应查文档说明是否走库", "confidence": 0.86}}

## 历史对话
{history_block}

## 当前用户问题
{query}

## 输出
仅输出一个 JSON 对象，勿其它文字：
{{
  "tool": "rag_search | text2sql_query | direct_answer",
  "reasoning": "用户可见的 1-2 句摘要",
  "confidence": 0.0-1.0
}}
"""

    intent_model = os.getenv("INTENT_LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    intent_messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "你是严谨的意图分类器。仅从工具名集合中选择；"
                "只输出一个 JSON 对象，不要 Markdown、不要前后缀说明。"
            ),
        },
        {"role": "user", "content": prompt},
    ]

    def _sync_call() -> str:
        res = oai.chat.completions.create(
            model=intent_model,
            messages=intent_messages,
            temperature=0.0,
            stream=False,
        )
        return (res.choices[0].message.content or "").strip()

    text = await asyncio.wait_for(asyncio.to_thread(_sync_call), timeout=timeout_s)
    obj = _extract_json_obj(text)
    if obj is None:
        raise ValueError("LLM intent 输出不是合法 JSON")
    prompts: list[dict[str, Any]] | None = None
    if capture_prompts:
        prompts = [{"phase": "intent", "model": intent_model, "messages": intent_messages}]
    return obj, prompts


def _effective_intent_llm_timeout_s(override: float) -> float:
    """Intent LLM 单次 `wait_for` 上限：优先读 `CHATBI_V2_INTENT_TIMEOUT_S`，否则用调用方传入值。"""
    raw = (os.getenv("CHATBI_V2_INTENT_TIMEOUT_S") or "").strip()
    if raw:
        try:
            return max(0.5, min(120.0, float(raw)))
        except ValueError:
            pass
    return max(0.5, min(120.0, float(override)))


def _intent_llm_max_retries() -> int:
    """Intent LLM 外呼最大尝试次数（含首次）；默认 3。"""
    raw = (os.getenv("CHATBI_V2_INTENT_LLM_RETRIES") or "").strip()
    if raw:
        try:
            return max(1, min(5, int(raw)))
        except ValueError:
            pass
    return 3


def _intent_llm_retry_backoff_s(attempt: int) -> float:
    """第 attempt 次失败后的退避秒数（attempt 从 1 起）。"""
    base = 0.15
    raw = (os.getenv("CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S") or "").strip()
    if raw:
        try:
            base = max(0.0, min(5.0, float(raw)))
        except ValueError:
            pass
    return base * (2 ** max(0, attempt - 1))


def _intent_llm_retry_timeout_factors() -> tuple[float, ...]:
    """各轮单次 wait_for 相对首轮的系数；末项用于超出长度的后续轮次。"""
    raw = (os.getenv("CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS") or "").strip()
    if raw:
        try:
            parsed = tuple(max(0.1, min(1.0, float(x.strip()))) for x in raw.split(",") if x.strip())
            if parsed:
                return parsed
        except ValueError:
            pass
    return (1.0, 0.65, 0.4)


def _intent_llm_timeout_s_for_attempt(base_timeout_s: float, attempt: int) -> float:
    """重试轮次逐步缩短单次 wait_for：首轮全量，后续轮按系数递减。"""
    factors = _intent_llm_retry_timeout_factors()
    idx = min(max(attempt, 1) - 1, len(factors) - 1)
    scaled = base_timeout_s * factors[idx]
    return max(0.5, min(120.0, scaled))


def _intent_llm_retryable(exc: BaseException) -> bool:
    """仅瞬态/超时类错误可重试；JSON 解析与 tool 校验失败不重试。"""
    if isinstance(exc, (asyncio.TimeoutError, APITimeoutError)):
        return True
    if isinstance(exc, (APIConnectionError, InternalServerError, RateLimitError)):
        return True
    if isinstance(exc, APIStatusError):
        code = getattr(exc, "status_code", None)
        return code in (429, 502, 503, 504)
    return False


async def _llm_decide_v2_with_retries(
    *,
    oai: OpenAI,
    query: str,
    history: list[dict[str, Any]],
    tools: list[Tool],
    timeout_s: float,
    capture_prompts: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]] | None, dict[str, Any]]:
    """包装 `_llm_decide_v2`：可重试错误最多 `CHATBI_V2_INTENT_LLM_RETRIES` 次，耗尽后抛 TimeoutError 走 V1。"""
    max_retries = _intent_llm_max_retries()
    last_retryable: BaseException | None = None
    for attempt in range(1, max_retries + 1):
        attempt_timeout_s = _intent_llm_timeout_s_for_attempt(timeout_s, attempt)
        try:
            raw_obj, intent_prompts = await _llm_decide_v2(
                oai=oai,
                query=query,
                history=history,
                tools=tools,
                timeout_s=attempt_timeout_s,
                capture_prompts=capture_prompts,
            )
            meta: dict[str, Any] = {"attempt": attempt, "timeout_s": attempt_timeout_s}
            if attempt > 1:
                meta["used"] = "llm_retry"
            return raw_obj, intent_prompts, meta
        except Exception as exc:  # noqa: BLE001
            if not _intent_llm_retryable(exc) or attempt >= max_retries:
                if _intent_llm_retryable(exc) and attempt >= max_retries:
                    raise asyncio.TimeoutError from exc
                raise
            last_retryable = exc
            await asyncio.sleep(_intent_llm_retry_backoff_s(attempt))
    raise asyncio.TimeoutError from last_retryable


def _heuristic_decide(query: str) -> tuple[ToolName, V1Mode, float, str]:
    # 轻量启发式：用于 LLM 不可用时保证功能可用
    if is_text2sql_intent(query):
        tool: ToolName = "text2sql_query"
        mode: V1Mode = "text2sql"
        conf = 0.72
        reasoning = "问题更像需要结构化统计/聚合数据，因此优先查询数据库。"
        return tool, mode, conf, reasoning

    q = (query or "").lower()
    if any(k in q for k in ["翻译", "润色", "改写", "写作", "总结", "概括", "提纲", "生成", "邮件", "周报", "brainstorm", "translate", "polish"]):
        tool = "direct_answer"
        mode = "no_data"
        conf = 0.75
        reasoning = "问题更偏语言处理或创作，不需要检索/查库，直接生成回答。"
        return tool, mode, conf, reasoning

    tool = "rag_search"
    mode = "rag"
    conf = 0.68
    reasoning = "问题更像需要参考内部资料的解释或信息检索，因此选择文档检索。"
    return tool, mode, conf, reasoning


async def decide_intent_v2(
    *,
    query: str,
    history: list[dict[str, Any]] | None = None,
    tools: list[Tool] | None = None,
    min_confidence: float = 0.6,
    timeout: float = 3.0,
    capture_llm_prompts: bool = False,
) -> IntentDecision:
    t_start = time.perf_counter()
    hist = history or []
    use_tools = tools or []

    # structured_signals：gating 的关键依赖
    structured = StructuredSignals(
        llm_prefers_sql=is_text2sql_intent(query),
        has_aggregation_signals=_has_aggregation_keywords(query),
    )

    # 与 tests、benchmark、PROJECT_CONFIG 对齐：关闭时仅启发式/V1 降级，不创建 SiliconFlow client（CI 零外呼）。
    use_intent_llm_raw = (os.getenv("CHATBI_V2_INTENT_LLM", "true") or "").strip().lower()
    use_intent_llm = use_intent_llm_raw in ("1", "true", "yes", "on")

    composite_key = _intent_composite_cache_key(query=query, history=hist)
    key_obs = _cache_key_obs_hash(composite_key)

    def _latency_ms() -> int:
        return int((time.perf_counter() - t_start) * 1000)

    def _return_cache_hit(base: IntentDecision) -> IntentDecision:
        lat = _latency_ms()
        out = _attach_cache_observability(base, cache="hit", cache_key_hash=key_obs, latency_ms=lat)
        _log_intent_cache_line(event="hit", key_hash=key_obs, latency_ms=lat)
        return out

    def _return_cache_miss(decision: IntentDecision) -> IntentDecision:
        lat = _latency_ms()
        _intent_cache.set(composite_key, _intent_decision_for_cache_store(decision))
        out = _attach_cache_observability(decision, cache="miss", cache_key_hash=key_obs, latency_ms=lat)
        _log_intent_cache_line(event="miss", key_hash=key_obs, latency_ms=lat)
        return out

    cached = _intent_cache.get(composite_key)
    if isinstance(cached, IntentDecision):
        return _return_cache_hit(cached)

    try:
        if use_intent_llm:
            # 显式开启：用 LLM 做主决策
            oai = openai_siliconflow_client()
            if not use_tools:
                # tool registry 为空时退化到启发式（避免空描述影响输出）
                tool, mode, conf, reasoning = _heuristic_decide(query)
                raw = {"used": "heuristic", "confidence": conf}
                fallback = _fallback_tool_by_low_confidence(tool) if conf < min_confidence else None
                decision = IntentDecision(
                    tool=tool,
                    mode=mode,
                    reasoning=reasoning,
                    reasoning_full=reasoning,
                    confidence=conf,
                    fallback=fallback,
                    structured_signals=structured,
                    raw_response=raw,
                )
                return _return_cache_miss(decision)

            t_llm = _effective_intent_llm_timeout_s(timeout)
            raw_obj, intent_prompts, retry_meta = await _llm_decide_v2_with_retries(
                oai=oai,
                query=query,
                history=hist,
                tools=use_tools,
                timeout_s=t_llm,
                capture_prompts=capture_llm_prompts,
            )

            tool_raw = raw_obj.get("tool")
            reasoning_raw = raw_obj.get("reasoning")
            confidence_raw = raw_obj.get("confidence")
            tool = str(tool_raw or "").strip()
            if tool not in ("rag_search", "text2sql_query", "direct_answer"):
                raise ValueError("LLM intent tool 不在允许集合")
            tool_t = tool  # type: ignore[assignment]
            mode = tool_mode_map()[tool_t]
            conf = _clamp01(float(confidence_raw if confidence_raw is not None else 0.0))
            reasoning = str(reasoning_raw or "").strip() or "意图识别完成。"
            fallback_tool = _fallback_tool_by_low_confidence(tool_t) if conf < min_confidence else None
            raw_merged: dict[str, Any] = dict(raw_obj)
            if retry_meta.get("used") == "llm_retry":
                raw_merged["used"] = "llm_retry"
                raw_merged["attempt"] = retry_meta.get("attempt")
            if retry_meta.get("timeout_s") is not None:
                raw_merged["timeout_s"] = retry_meta.get("timeout_s")
            if intent_prompts:
                raw_merged["llm_prompts"] = intent_prompts
            decision2 = IntentDecision(
                tool=tool_t,
                mode=mode,  # type: ignore[arg-type]
                reasoning=reasoning[:260],
                reasoning_full=reasoning,
                confidence=conf,
                fallback=fallback_tool,
                structured_signals=structured,
                raw_response=raw_merged,
            )
            return _return_cache_miss(decision2)
    except asyncio.TimeoutError:
        # timeout -> 降级到 V1 规则路由
        v1 = decide_intent_v1(query=query, prefer="auto")
        tool_t = _map_v1_mode_to_tool(v1.final_mode)
        mode_t = tool_mode_map()[tool_t]
        reasoning = "意图识别超时，降级到 V1 规则路由。"
        conf = float(min_confidence)
        fallback = None
        decision3 = IntentDecision(
            tool=tool_t,
            mode=mode_t,  # type: ignore[arg-type]
            reasoning=reasoning[:260],
            reasoning_full=reasoning,
            confidence=_clamp01(conf),
            fallback=fallback,
            structured_signals=structured,
            raw_response={"used": "v1_fallback", "confidence": conf},
        )
        return _return_cache_miss(decision3)
    except Exception:
        # LLM 失败/输出不符合预期 -> 启发式降级
        pass

    # 默认：启发式（保证可用性 + 运行成本可控）
    tool_h, mode_h, conf_h, reasoning_h = _heuristic_decide(query)
    fallback_tool_h = _fallback_tool_by_low_confidence(tool_h) if conf_h < min_confidence else None
    # 还可追加一次：低置信度时向 V1 规则路由对齐（作为“超时回退”一致性）
    if conf_h < min_confidence and use_tools:
        try:
            v1 = decide_intent_v1(query=query, prefer="auto")
            tool_h = _map_v1_mode_to_tool(v1.final_mode)
            mode_h = tool_mode_map()[tool_h]
            fallback_tool_h = _fallback_tool_by_low_confidence(tool_h) if conf_h < min_confidence else None
        except Exception:  # noqa: BLE001
            pass

    decision4 = IntentDecision(
        tool=tool_h,
        mode=mode_h,
        reasoning=reasoning_h,
        reasoning_full=reasoning_h,
        confidence=conf_h,
        fallback=fallback_tool_h,
        structured_signals=structured,
        raw_response={"used": "heuristic", "confidence": conf_h},
    )
    return _return_cache_miss(decision4)

