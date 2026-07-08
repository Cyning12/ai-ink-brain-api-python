"""共享 Review 规则 V1–V4 单测。

P0-1: `api/ops/review/rules.py` 为 deep / ReAct 共用 Review 闸。
"""

from __future__ import annotations

from typing import Any

import pytest

from api.ops.orchestrator.core import review_result as core_review_result
from api.ops.review.rules import (
    REVIEW_VERDICT_FAIL,
    REVIEW_VERDICT_PARTIAL,
    REVIEW_VERDICT_PASS,
    ReviewRule,
    review_result,
)


class FakeQueries:
    """最小 Queries 假对象，覆盖 review 所需的 fetch_* 接口。"""

    def __init__(self) -> None:
        self.issues: dict[int, dict[str, Any]] = {
            545: {
                "number": 545,
                "html_url": "https://github.com/MoonshotAI/kimi-code/issues/545",
            },
        }
        self.pulls: dict[int, dict[str, Any]] = {
            123: {
                "number": 123,
                "html_url": "https://github.com/MoonshotAI/kimi-code/pull/123",
            },
        }

    def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
        return self.issues.get(number)

    def fetch_pull_by_number(self, number: int) -> dict[str, Any] | None:
        return self.pulls.get(number)


@pytest.fixture
def queries() -> FakeQueries:
    return FakeQueries()


def _make_result(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "reasoning": "分析完成",
        "suggestion": "建议参与",
        "confidence": 0.85,
        "evidence": [{"number": 545}],
        "citations": [],
    }
    base.update(overrides)
    return base


# -----------------------------------------------------------------------------
# V1: 引用 issue / PR 必须存在于同步表
# -----------------------------------------------------------------------------


def test_review_v1_pass_issue(queries: FakeQueries) -> None:
    result = _make_result(
        citations=[{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}],
    )
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PASS
    assert detail == {}


def test_review_v1_pass_pull(queries: FakeQueries) -> None:
    result = _make_result(
        citations=[{"number": 123, "url": "https://github.com/MoonshotAI/kimi-code/pull/123"}],
    )
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PASS


def test_review_v1_fail_missing(queries: FakeQueries) -> None:
    result = _make_result(
        citations=[{"number": 999, "url": "https://github.com/MoonshotAI/kimi-code/issues/999"}],
    )
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_FAIL
    assert detail["rule"] == ReviewRule.V1_EXISTS
    assert "999" in detail["message"]


# -----------------------------------------------------------------------------
# V2: 引用 URL 必须与同步表一致
# -----------------------------------------------------------------------------


def test_review_v2_fail_url_mismatch(queries: FakeQueries) -> None:
    result = _make_result(
        citations=[{"number": 545, "url": "https://example.com/wrong"}],
    )
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_FAIL
    assert detail["rule"] == ReviewRule.V2_URL
    assert "545" in detail["message"]


def test_review_v2_pass_when_no_url(queries: FakeQueries) -> None:
    """V2 仅在有 url 字段时校验；缺 url 不触发 V2。"""
    result = _make_result(citations=[{"number": 545}])
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PASS


# -----------------------------------------------------------------------------
# V3: 禁止 Git 写操作指令
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_text",
    [
        "建议提交 commit",
        "请 push 到远程",
        "你可以 open PR",
        "直接 merge 即可",
    ],
)
def test_review_v3_fail_write_op(bad_text: str, queries: FakeQueries) -> None:
    result = _make_result(reasoning=bad_text, suggestion="")
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_FAIL
    assert detail["rule"] == ReviewRule.V3_WRITE_OP


def test_review_v3_pass_read_only(queries: FakeQueries) -> None:
    result = _make_result(reasoning="查看 issue 详情后给出只读建议")
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PASS


# -----------------------------------------------------------------------------
# V4: 置信度低时必须有证据
# -----------------------------------------------------------------------------


def test_review_v4_partial_low_confidence_no_evidence(queries: FakeQueries) -> None:
    result = _make_result(confidence=0.3, evidence=[], citations=[])
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PARTIAL
    assert detail["rule"] == ReviewRule.V4_CONFIDENCE


def test_review_v4_pass_low_confidence_with_evidence(queries: FakeQueries) -> None:
    result = _make_result(confidence=0.3, evidence=[{"tool": "ops_get_issue"}], citations=[])
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PASS


# -----------------------------------------------------------------------------
# 优先级：V1/V2/V3 在 V4 之前触发
# -----------------------------------------------------------------------------


def test_review_v1_before_v4(queries: FakeQueries) -> None:
    """即使 confidence 低且无 evidence，引用不存在仍优先 fail V1。"""
    result = _make_result(
        confidence=0.2,
        evidence=[],
        citations=[{"number": 404}],
    )
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_FAIL
    assert detail["rule"] == ReviewRule.V1_EXISTS


def test_review_v3_before_v4(queries: FakeQueries) -> None:
    """即使 confidence 低且无 evidence，含写操作仍优先 fail V3。"""
    result = _make_result(
        confidence=0.2,
        evidence=[],
        reasoning="请直接 merge",
        suggestion="",
        citations=[],
    )
    verdict, detail = review_result(result, queries)
    assert verdict == REVIEW_VERDICT_FAIL
    assert detail["rule"] == ReviewRule.V3_WRITE_OP


# -----------------------------------------------------------------------------
# 共用性：deep / ReAct 从同一模块导入同一函数
# -----------------------------------------------------------------------------


def test_deep_and_react_share_review_function() -> None:
    """orchestrator.core 的 review_result 必须来自共享模块。"""
    from api.ops.orchestrator.core import review_result as imported
    from api.ops.review.rules import review_result as canonical

    assert imported is canonical


def test_react_loop_imports_shared_review(queries: FakeQueries) -> None:
    """react_loop 内可直接使用 api.ops.review.rules.review_result。"""
    from api.ops.react_loop import run_react_fallback

    # 仅确认导入路径可达；具体 ReAct 行为由 tests/ops_desk/test_react_fallback.py 覆盖。
    assert callable(run_react_fallback)


def test_orchestrator_backwards_compat_re_export(queries: FakeQueries) -> None:
    """旧入口 api.ops.orchestrator.core.review_result 仍可用。"""
    result = _make_result(citations=[{"number": 545}])
    verdict, detail = core_review_result(result, queries)
    assert verdict == REVIEW_VERDICT_PASS
    assert detail == {}
