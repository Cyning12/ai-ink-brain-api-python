from __future__ import annotations

import asyncio
from collections import OrderedDict
import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Literal

from openai import OpenAI

from .intent_router import decide_intent as decide_intent_v1
from .rag_env import openai_siliconflow_client
from .text2sql_core import is_text2sql_intent
from .tools import Tool, tool_mode_map


ToolName = Literal["rag_search", "text2sql_query", "direct_answer"]
V1Mode = Literal["rag", "text2sql", "no_data"]


class LRUCache:
    """P0 预留：用于 IntentDecision 缓存（P1 实现）。当前用最小 TTL LRU 实现。"""

    def __init__(self, *, maxsize: int, ttl_s: float) -> None:
        self._maxsize = maxsize
        self._ttl_s = ttl_s
        self._items: "OrderedDict[str, tuple[float, Any]]" = OrderedDict()

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


# 预留接口：P0 可不启用，但变量必须存在
_intent_cache: LRUCache = LRUCache(maxsize=1000, ttl_s=300.0)


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


async def _llm_decide_v2(*, oai: OpenAI, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float) -> dict[str, Any]:
    # 让 LLM 按 spec 输出 tool/reasoning/confidence（并尽量使用结构化 JSON）
    tools_desc = "\n\n".join([f"- {t.name}: {t.description}" for t in tools])
    history_block = "\n".join(
        [f"{m.get('role','?')}: {str(m.get('content',''))[:120]}" for m in (history or [])[-3:]]
    ).strip() or "无历史对话"

    prompt = f"""你是一个意图识别专家。请分析用户问题，判断应该使用哪个工具来回答。

## 可用工具
{tools_desc}

## 判断标准（语义化，不要依赖关键词匹配）
1. 是否需要结构化数据聚合？是 -> text2sql_query；否 -> 继续判断
2. 是否需要内部文档证据？是 -> rag_search
3. 是否是纯写作/语言任务？是 -> direct_answer
4. 不确定时 -> rag_search（安全默认）

## 历史对话
{history_block}

## 用户问题
{query}

## 输出格式
请严格输出 JSON：
{{
  "tool": "rag_search | text2sql_query | direct_answer",
  "reasoning": "用户级 1-2 句话摘要",
  "confidence": 0.0-1.0
}}
"""

    def _sync_call() -> str:
        res = oai.chat.completions.create(
            model=os.getenv(
                "INTENT_LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct"
            ),
            messages=[{"role": "system", "content": "你是一个严谨的意图识别助手。只输出 JSON，不要输出任何其他内容。"}, {"role": "user", "content": prompt}],
            temperature=0.0,
            stream=False,
        )
        return (res.choices[0].message.content or "").strip()

    text = await asyncio.wait_for(asyncio.to_thread(_sync_call), timeout=timeout_s)
    obj = _extract_json_obj(text)
    if obj is None:
        raise ValueError("LLM intent 输出不是合法 JSON")
    return obj


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
) -> IntentDecision:
    hist = history or []
    use_tools = tools or []

    # structured_signals：gating 的关键依赖
    structured = StructuredSignals(
        llm_prefers_sql=is_text2sql_intent(query),
        has_aggregation_signals=_has_aggregation_keywords(query),
    )

    try:
        use_intent_llm_raw = (os.getenv("CHATBI_V2_INTENT_LLM", "true") or "").strip().lower()
        use_intent_llm = use_intent_llm_raw in ("1", "true", "yes", "on")

        # P0 预留接口：可缓存意图结果（默认仍可关闭/不依赖）。
        cache_key = query.strip()
        if use_intent_llm:
            cached = _intent_cache.get(cache_key)
            if isinstance(cached, IntentDecision):
                return cached

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
                _intent_cache.set(cache_key, decision)
                return decision

            raw_obj = await _llm_decide_v2(
                oai=oai, query=query, history=hist, tools=use_tools, timeout_s=timeout
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
            decision2 = IntentDecision(
                tool=tool_t,
                mode=mode,  # type: ignore[arg-type]
                reasoning=reasoning[:260],
                reasoning_full=reasoning,
                confidence=conf,
                fallback=fallback_tool,
                structured_signals=structured,
                raw_response=raw_obj,
            )
            _intent_cache.set(cache_key, decision2)
            return decision2
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
        _intent_cache.set(cache_key, decision3)
        return decision3
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
    _intent_cache.set(cache_key, decision4)
    return decision4

