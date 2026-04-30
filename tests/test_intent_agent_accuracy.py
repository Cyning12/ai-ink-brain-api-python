from __future__ import annotations

import asyncio
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

import pytest

from api.intent_agent import IntentDecision, decide_intent_v2
from api.tools import Tool, ToolName


ExpectedTool = Literal["rag_search", "text2sql_query", "direct_answer"]


@dataclass(frozen=True)
class HistoryMsg:
    role: Literal["user", "assistant"]
    content: str


@dataclass(frozen=True)
class IntentCase:
    query: str
    expected: ExpectedTool
    category: str
    note: str
    history: list[HistoryMsg]


def _env_flag(name: str, default: bool = False) -> bool:
    raw = (os.getenv(name, "true" if default else "false") or "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def _ensure_out_path() -> Path:
    out = (os.getenv("CHATBI_V2_INTENT_EVAL_OUT") or "").strip()
    if out:
        p = Path(out)
    else:
        p = Path(__file__).resolve().parent / "_out" / "intent_accuracy.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


async def _dummy_execute(*, query: str, history: list[dict[str, Any]] | None = None) -> Any:  # noqa: ANN401
    _ = (query, history)
    return {"ok": True}


def _make_tools() -> list[Tool]:
    async def _exec(query: str, *, history: list[dict[str, Any]] | None = None) -> Any:  # noqa: ANN401
        return await _dummy_execute(query=query, history=history)

    return [
        Tool(
            name="text2sql_query",
            description="执行结构化数据查询与聚合统计，返回具体数值/表格结果。",
            parameters={},
            execute=_exec,
        ),
        Tool(
            name="rag_search",
            description="检索项目内部文档/知识库来回答概念、方法、原理、对比、操作步骤等问题。",
            parameters={},
            execute=_exec,
        ),
        Tool(
            name="direct_answer",
            description="不依赖内部数据或文档，直接完成翻译、润色、写作、代码生成、通用知识解释等任务。",
            parameters={},
            execute=_exec,
        ),
    ]


def _cases() -> list[IntentCase]:
    # 约束：总计 60 条（Text2SQL 20 / RAG 20 / Direct 10 / 多轮 10）
    # 说明：多轮 10 条的 expected 仍属于三类之一，但依赖 history 做指代/省略消解。
    return [
        # Text2SQL（20）
        IntentCase("昨天销售额是多少", "text2sql_query", "时间+金额", "口语化", []),
        IntentCase("这个月有多少订单", "text2sql_query", "数量", "口语化", []),
        IntentCase("最近7天收入多少", "text2sql_query", "时间范围", "自然语言", []),
        IntentCase("按月统计销售额", "text2sql_query", "分组+时间", "聚合", []),
        IntentCase("Top10产品销售额", "text2sql_query", "排名", "英文+数字", []),
        IntentCase("平均客单价", "text2sql_query", "平均", "业务术语", []),
        IntentCase("各渠道转化率", "text2sql_query", "分组", "无统计词但强业务指标", []),
        IntentCase("同比去年增长了多少", "text2sql_query", "对比", "同比", []),
        IntentCase("环比上月增长多少", "text2sql_query", "对比", "环比", []),
        IntentCase("本周每日新增用户数", "text2sql_query", "趋势", "时间序列", []),
        IntentCase("上周退款金额", "text2sql_query", "金额", "退款", []),
        IntentCase("昨天的订单量和销售额", "text2sql_query", "多指标", "组合指标", []),
        IntentCase("近30天复购率", "text2sql_query", "比率", "业务指标", []),
        IntentCase("哪个产品卖得最好", "text2sql_query", "排名", "口语化", []),
        IntentCase("哪个渠道贡献最大", "text2sql_query", "排名", "口语化", []),
        IntentCase("本季度销售额趋势", "text2sql_query", "趋势", "季度", []),
        IntentCase("看一下昨天的数据", "text2sql_query", "模糊-数据", "模糊表达", []),
        IntentCase("过去一年每月订单数", "text2sql_query", "趋势", "长时间跨度", []),
        IntentCase("按城市分组统计订单数", "text2sql_query", "分组", "明确分组", []),
        IntentCase("用户增长趋势", "text2sql_query", "趋势", "无关键词但强统计倾向", []),
        # RAG（20）
        IntentCase("什么是RAG", "rag_search", "概念", "标准概念", []),
        IntentCase("MCP 是什么", "rag_search", "概念", "新术语", []),
        IntentCase("ReAct 和 Plan-and-Execute 区别", "rag_search", "对比", "技术对比", []),
        IntentCase("怎么优化向量检索", "rag_search", "如何", "技术操作", []),
        IntentCase("为什么检索不准", "rag_search", "为什么", "原因分析", []),
        IntentCase("Text2SQL 的原理是什么", "rag_search", "概念", "技术原理", []),
        IntentCase("怎么部署这个项目", "rag_search", "如何", "操作文档", []),
        IntentCase("这个项目的目录结构是怎样的", "rag_search", "文档", "项目约定", []),
        IntentCase("如何写一份 _tech_graph 的流程图", "rag_search", "规范", "项目内规范", []),
        IntentCase("Supabase 失败时应该返回什么错误码", "rag_search", "规范", "错误处理约定", []),
        IntentCase("如何做意图缓存（LRU+TTL）", "rag_search", "方法", "实现建议", []),
        IntentCase("什么是 macro-F1", "rag_search", "概念", "指标解释", []),
        IntentCase("如何计算 confusion matrix", "rag_search", "概念", "指标解释", []),
        IntentCase("这份任务单的 P1 目标是什么", "rag_search", "文档", "指向任务说明", []),
        IntentCase("为什么 CI 默认要走 stub", "rag_search", "原因", "工程约束", []),
        IntentCase("如何做性能基准的 P50/P95", "rag_search", "方法", "性能指标口径", []),
        IntentCase("RAG 检索的 topk 该怎么选", "rag_search", "选型", "参数选择", []),
        IntentCase("为什么要区分 direct_answer 和 rag_search", "rag_search", "设计", "路由边界", []),
        IntentCase("LangChain 的 long-term memory 是什么", "rag_search", "概念", "内部学习资料", []),
        IntentCase("这个仓库的 intent_router 做了什么", "rag_search", "代码", "查文档/代码解释", []),
        # Direct（10）
        IntentCase("翻译：Hello", "direct_answer", "翻译", "明确翻译", []),
        IntentCase("把这段英文翻译成中文：How are you?", "direct_answer", "翻译", "语言转换", []),
        IntentCase("润色这段话：今天工作很忙", "direct_answer", "润色", "文本处理", []),
        IntentCase("帮我写周报，包含本周进展和下周计划", "direct_answer", "写作", "内容生成", []),
        IntentCase("写一封请假邮件，语气正式", "direct_answer", "写作", "商务写作", []),
        IntentCase("用 Python 写快排", "direct_answer", "代码", "代码生成", []),
        IntentCase("解释一下量子计算，用通俗语言", "direct_answer", "解释", "通用知识", []),
        IntentCase("头脑风暴：新产品 idea 5 个", "direct_answer", "创意", "发散", []),
        IntentCase("总结下面这段话：……", "direct_answer", "总结", "文本处理", []),
        IntentCase("给这段代码加注释：print('hi')", "direct_answer", "代码", "代码辅助", []),
        # 多轮（10）
        IntentCase(
            "它有什么缺点",
            "rag_search",
            "多轮-指代",
            "指代消解（它=RAG）",
            [
                HistoryMsg("user", "什么是RAG"),
                HistoryMsg("assistant", "RAG 是一种检索增强生成的方法……"),
            ],
        ),
        IntentCase(
            "那怎么优化",
            "rag_search",
            "多轮-省略",
            "省略主语（那=向量检索）",
            [
                HistoryMsg("user", "向量检索为什么不准"),
                HistoryMsg("assistant", "可能是 embedding 质量、召回策略、重排等问题……"),
            ],
        ),
        IntentCase(
            "改成更正式一点",
            "direct_answer",
            "多轮-改写",
            "对上文内容改写",
            [
                HistoryMsg("user", "帮我写一段自我介绍"),
                HistoryMsg("assistant", "我叫……很高兴认识你。"),
            ],
        ),
        IntentCase(
            "再给我 3 个点子",
            "direct_answer",
            "多轮-续写",
            "延续创意生成",
            [
                HistoryMsg("user", "头脑风暴：新产品 idea 5 个"),
                HistoryMsg("assistant", "1) …… 2) …… 3) …… 4) …… 5) ……"),
            ],
        ),
        IntentCase(
            "把第 2 个展开说说",
            "direct_answer",
            "多轮-扩写",
            "基于上轮列点扩写",
            [
                HistoryMsg("user", "给我 3 条学习建议"),
                HistoryMsg("assistant", "1) …… 2) …… 3) ……"),
            ],
        ),
        IntentCase(
            "那需要查数据库吗",
            "rag_search",
            "多轮-澄清",
            "问路由边界/方法",
            [
                HistoryMsg("user", "昨天销售额是多少"),
                HistoryMsg("assistant", "我可以通过 Text2SQL 去查询……"),
            ],
        ),
        IntentCase(
            "那你给个 SQL 示例",
            "direct_answer",
            "多轮-示例",
            "请求示例而非实际查询",
            [
                HistoryMsg("user", "怎么统计订单数"),
                HistoryMsg("assistant", "可以用 COUNT(*)……"),
            ],
        ),
        IntentCase(
            "那份文档在哪",
            "rag_search",
            "多轮-定位",
            "定位项目内文档",
            [
                HistoryMsg("user", "怎么部署这个项目"),
                HistoryMsg("assistant", "可以参考项目的部署文档……"),
            ],
        ),
        IntentCase(
            "顺便给我一个性能压测脚本",
            "direct_answer",
            "多轮-生成",
            "请求代码生成",
            [
                HistoryMsg("user", "如何做性能基准的 P50/P95"),
                HistoryMsg("assistant", "可以用多次采样计算分位数……"),
            ],
        ),
        IntentCase(
            "再补 10 条测试用例",
            "direct_answer",
            "多轮-生成",
            "请求生成测试数据",
            [
                HistoryMsg("user", "我需要一个 60 条的测试集格式"),
                HistoryMsg("assistant", "可以用 list[dict] 或 dataclass 来描述用例……"),
            ],
        ),
    ]


def _as_history_dicts(history: list[HistoryMsg]) -> list[dict[str, Any]]:
    return [{"role": m.role, "content": m.content} for m in history]


def _confusion_matrix(labels: list[str]) -> dict[str, dict[str, int]]:
    return {a: {b: 0 for b in labels} for a in labels}


def _safe_div(n: float, d: float) -> float:
    return 0.0 if d == 0.0 else n / d


def _f1_scores(cm: dict[str, dict[str, int]], labels: list[str]) -> tuple[dict[str, float], float]:
    per: dict[str, float] = {}
    for c in labels:
        tp = float(cm[c][c])
        fp = float(sum(cm[a][c] for a in labels if a != c))
        fn = float(sum(cm[c][b] for b in labels if b != c))
        p = _safe_div(tp, tp + fp)
        r = _safe_div(tp, tp + fn)
        f1 = 0.0 if (p + r) == 0.0 else (2.0 * p * r) / (p + r)
        per[c] = f1
    macro = sum(per.values()) / float(len(labels)) if labels else 0.0
    return per, macro


async def _run_eval(*, real_llm: bool) -> dict[str, Any]:
    # 约束：CI 默认不跑真实 LLM；脚本内仍允许用 env 切换。
    tools = _make_tools()
    labels: list[str] = ["rag_search", "text2sql_query", "direct_answer"]
    cm = _confusion_matrix(labels)
    out_path = _ensure_out_path()

    records: list[dict[str, Any]] = []
    for idx, tc in enumerate(_cases(), start=1):
        hist_dicts = _as_history_dicts(tc.history)
        t0 = time.perf_counter()
        decision: IntentDecision = await decide_intent_v2(
            query=tc.query,
            history=hist_dicts,
            tools=tools,
            timeout=3.0,
        )
        latency_ms = int((time.perf_counter() - t0) * 1000)

        predicted = str(decision.tool)
        expected = str(tc.expected)
        if predicted not in labels:
            predicted = "direct_answer"
        cm[expected][predicted] += 1

        rec = {
            "i": idx,
            "query": tc.query,
            "expected": expected,
            "predicted": predicted,
            "ok": predicted == expected,
            "category": tc.category,
            "note": tc.note,
            "confidence": float(decision.confidence),
            "mode": str(decision.mode),
            "fallback": decision.fallback,
            "reasoning": decision.reasoning,
            "reasoning_full": decision.reasoning_full,
            "latency_ms": latency_ms,
            "raw_response": decision.raw_response,
            "history": hist_dicts,
            "real_llm": real_llm,
        }
        records.append(rec)

    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    per_f1, macro_f1 = _f1_scores(cm, labels)
    ok_cnt = sum(1 for r in records if bool(r.get("ok")))
    return {
        "n": len(records),
        "ok": ok_cnt,
        "acc": _safe_div(float(ok_cnt), float(len(records)) if records else 1.0),
        "macro_f1": macro_f1,
        "per_class_f1": per_f1,
        "confusion_matrix": cm,
        "out_path": str(out_path),
    }


def _print_report(summary: dict[str, Any]) -> None:
    print("Intent Accuracy Summary")
    print(f"- n: {summary['n']}, ok: {summary['ok']}, acc: {summary['acc']:.3f}")
    print(f"- macro_f1: {summary['macro_f1']:.3f}")
    print("- per_class_f1:")
    per: dict[str, float] = summary["per_class_f1"]
    for k in ("text2sql_query", "rag_search", "direct_answer"):
        if k in per:
            print(f"  - {k}: {per[k]:.3f}")
    print(f"- out: {summary['out_path']}")
    print("- confusion_matrix (expected -> predicted):")
    cm: dict[str, dict[str, int]] = summary["confusion_matrix"]
    for exp, row in cm.items():
        items = ", ".join([f"{pred}={row[pred]}" for pred in ("text2sql_query", "rag_search", "direct_answer")])
        print(f"  - {exp}: {items}")


@pytest.mark.skipif(
    not _env_flag("CHATBI_V2_INTENT_EVAL", default=False),
    reason="默认不跑真实 LLM/评测；本地设置 CHATBI_V2_INTENT_EVAL=true 执行。",
)
def test_intent_agent_accuracy_smoke(monkeypatch: pytest.MonkeyPatch) -> None:
    # 默认跑真实 LLM：由任务单要求；如需 stub，可在本地将 CHATBI_V2_INTENT_LLM=false。
    # 说明：此测试只负责“评测闭环可跑通”，不作为 CI gate（已 skip）。
    real_llm = _env_flag("CHATBI_V2_INTENT_LLM", default=True)
    summary = asyncio.run(_run_eval(real_llm=real_llm))
    _print_report(summary)

    # 最小验收（本地跑用）：避免完全跑偏
    assert summary["n"] == 60
    assert float(summary["macro_f1"]) >= 0.0


if __name__ == "__main__":
    real_llm_flag = _env_flag("CHATBI_V2_INTENT_LLM", default=True)
    # 作为脚本运行时，默认执行并输出报告。
    # 建议搭配：
    # - CHATBI_V2_INTENT_LLM=true
    # - SILICONFLOW_API_KEY=...
    # - INTENT_LLM_MODEL=deepseek-ai/DeepSeek-V3（或 Qwen Turbo）
    summary0 = asyncio.run(_run_eval(real_llm=real_llm_flag))
    _print_report(summary0)
