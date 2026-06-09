from __future__ import annotations

import asyncio
import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.graph.runner import run_graph_stub
from api.graph.state import (
    ChatBIState,
    failure_edges_graph,
    failure_edges_legacy,
    resolve_failure_edge,
)


@pytest.mark.parametrize("code", ["LLM_API_TIMEOUT", "RAG_RETRIEVE_EMPTY", "UNKNOWN"])
def test_failure_edges_cover_main_codes(code: str) -> None:
    assert code in failure_edges_legacy()
    assert code in failure_edges_graph()


def test_graph_intent_timeout_scheme_a() -> None:
    assert failure_edges_graph()["LLM_API_TIMEOUT"] == "direct_answer"


def test_legacy_intent_timeout_v1_fallback() -> None:
    assert failure_edges_legacy()["LLM_API_TIMEOUT"] == "intent_v1_fallback"


def test_resolve_failure_edge_graph_vs_legacy() -> None:
    assert resolve_failure_edge(error_code="LLM_API_TIMEOUT", graph=True) == "direct_answer"
    assert resolve_failure_edge(error_code="LLM_API_TIMEOUT", graph=False) == "intent_v1_fallback"


def test_run_graph_stub_sets_node() -> None:
    state = ChatBIState(run_id="r1", query="hello")
    out = asyncio.run(run_graph_stub(state))
    assert out.current_node == "stub"
    assert out.partial.get("graph_stub") is True


def test_chatbi_shared_modules_importable() -> None:
    from api import chatbi_agent_models, chatbi_events, chatbi_failure  # noqa: F401

    assert chatbi_events.agent_chain("agent.think", 0.0, "s1", {"text": "x"})["type"] == "agent.think"
    assert chatbi_failure.FailureTypeHandler.TEXT2SQL_DENY_FINAL_ANSWER_CODES


def _reload_index(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")

    import api.index as index

    importlib.reload(index)
    from tests._chatbi_auth_overrides import install_unified_chat_auth_override

    install_unified_chat_auth_override(index.app)
    return index


def test_graph_json_route_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _reload_index(monkeypatch)
    client = TestClient(index.app)
    resp = client.post(
        "/api/py/unified/chat/graph",
        json={"query": "P0 graph stub"},
        headers={"Authorization": "Bearer dummy"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("ok") is True
    assert data.get("graph_stub") is True
    assert "run_id" in data


def test_graph_stream_route_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _reload_index(monkeypatch)
    client = TestClient(index.app)
    with client.stream(
        "POST",
        "/api/py/unified/chat/graph/stream",
        json={"query": "P0 graph stream"},
        headers={"Authorization": "Bearer dummy"},
    ) as resp:
        assert resp.status_code == 200
        body = "".join(resp.iter_text())
    assert "event: chain" in body or "event:chain" in body.replace(" ", "")
    assert "event: done" in body or 'event: done' in body
    assert "graph_stub" in body
