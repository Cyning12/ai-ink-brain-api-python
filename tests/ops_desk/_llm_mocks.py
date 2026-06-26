"""Ops Desk 集成测试 · 统一 LLM mock（CI 无外网 / dummy key 时不打真实 API）。"""

from __future__ import annotations

from typing import Any, Callable


def patch_ops_llm_imports(
    monkeypatch: Any,
    *,
    chat_completion: Callable[..., Any],
    synthesize_answer: Callable[..., Any] | None = None,
    synthesize: Callable[..., tuple[str, Any]] | None = None,
) -> None:
    """Patch 各模块顶层的 chat_completion / synthesize 绑定（非仅 api.ops.llm）。"""
    monkeypatch.setattr("api.ops.llm.chat_completion", chat_completion)

    if synthesize_answer is not None:
        monkeypatch.setattr("api.ops.llm.synthesize_answer", synthesize_answer)
        monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", synthesize_answer)

    synth = synthesize
    if synth is not None:
        monkeypatch.setattr("api.ops.orchestrator.core.synthesize", synth)
        monkeypatch.setattr("api.ops.react_loop.synthesize", synth)

    for module in (
        "api.ops.react_loop",
        "api.ops.agents.issue_analyst",
        "api.ops.agents.graph_analyst",
        "api.ops.agents.scan_analyst",
    ):
        monkeypatch.setattr(f"{module}.chat_completion", chat_completion)
