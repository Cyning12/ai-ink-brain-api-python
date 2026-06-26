"""Ops Desk Graph Module Matrix v1 测试。

覆盖：
- _extract_module_ids（distinct module_id · 上限 20）
- _match_issue_to_module（labels 优先 · flow_map 回落）
- _count_tiers（C3-P0/P1/P2）
- ModuleMatrixService.build_matrix（端到端）
- ModuleMatrixService.get_module_edges（depends_on 过滤）
- API router / store 委托矩阵
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops.graph.module_matrix import (
    ModuleMatrixService,
    _count_tiers,
    _extract_module_ids,
    _match_issue_to_module,
)
from api.ops.graph.router import get_graph_store

# ── Fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def sample_payload() -> dict[str, Any]:
    """含 module_id 与 struct 节点的 graph payload。"""
    return {
        "schema_version": "graph_v2",
        "freeze_id": "KIMI-META-GRAPH-V2-BATCH@0fa2d54f",
        "graphs": [{"id": "00_main", "title": "顶层流程总图"}],
        "nodes": [
            {"graph_id": "00_main", "id": "AC", "label": "agent-core", "module_id": "agent_core", "kind": "struct"},
            {"graph_id": "00_main", "id": "CLI", "label": "kimi CLI", "module_id": "cli", "kind": "struct"},
            {"graph_id": "00_main", "id": "SDK", "label": "node-sdk", "module_id": "node_sdk", "kind": "struct"},
            {"graph_id": "00_main", "id": "FLOW_TURN", "label": "turn flow", "kind": "flow"},
        ],
        "edges": [
            {"from": "AC", "to": "CLI", "type": "depends_on", "graph_id": "00_main", "label": ""},
            {"from": "CLI", "to": "SDK", "type": "depends_on", "graph_id": "00_main", "label": "加载"},
            {"from": "FLOW_TURN", "to": "AC", "type": "triggers", "graph_id": "00_main", "label": ""},
        ],
    }


@pytest.fixture
def sample_flow_map() -> dict[str, dict[str, Any]]:
    return {
        "agent_core": {"path_substrings": ["agent-core", "agent_core"], "path_globs": ["packages/agent-core/**"]},
        "cli": {"path_substrings": ["cli", "kimi-code"], "path_globs": ["apps/kimi-code/**"]},
        "node_sdk": {"path_substrings": ["node-sdk", "sdk"], "path_globs": ["packages/node-sdk/**"]},
    }


@pytest.fixture
def sample_issues() -> list[dict[str, Any]]:
    return [
        {
            "number": 545,
            "title": "agent-core memory leak",
            "state": "open",
            "labels": ["module:agent_core"],
            "scan_tags": ["C3-P0"],
            "body": "",
        },
        {
            "number": 583,
            "title": "CLI startup slow on macOS",
            "state": "open",
            "labels": [],
            "scan_tags": ["C3-P2"],
            "body": "apps/kimi-code startup takes 3s",
        },
        {
            "number": 708,
            "title": "node-sdk type mismatch",
            "state": "open",
            "labels": [],
            "scan_tags": ["C3-P1"],
            "body": "packages/node-sdk types broken",
        },
        {
            "number": 999,
            "title": "Unrelated docs typo",
            "state": "open",
            "labels": [],
            "scan_tags": [],
            "body": "",
        },
    ]


class FakeSupabaseTable:
    def __init__(self, rows: list[dict[str, Any]] | None = None) -> None:
        self._rows = rows or []
        self._filters: list[tuple[str, Any]] = []

    def select(self, *_cols: str) -> FakeSupabaseTable:
        return self

    def eq(self, col: str, value: Any) -> FakeSupabaseTable:
        self._filters.append(("eq", col, value))
        return self

    def order(self, _col: str, *, desc: bool = False) -> FakeSupabaseTable:
        return self

    def limit(self, _n: int) -> FakeSupabaseTable:
        return self

    def execute(self) -> MagicMock:
        resp = MagicMock()
        resp.data = self._rows
        return resp


class FakeSupabase:
    def __init__(self, rows: list[dict[str, Any]] | None = None) -> None:
        self._rows = rows or []

    def table(self, _name: str) -> FakeSupabaseTable:
        return FakeSupabaseTable(self._rows)


# ── Unit Tests ────────────────────────────────────────────────────────────

class TestExtractModuleIds:
    def test_extracts_module_id_first(self, sample_payload: dict[str, Any]) -> None:
        ids = _extract_module_ids(sample_payload)
        assert ids == ["agent_core", "cli", "node_sdk"]

    def test_fallback_struct_kind(self) -> None:
        payload = {
            "nodes": [
                {"id": "LEGACY", "label": "legacy", "kind": "struct"},
                {"id": "FLOW", "label": "flow", "kind": "flow"},
            ]
        }
        ids = _extract_module_ids(payload)
        assert ids == ["LEGACY"]

    def test_max_20(self) -> None:
        payload = {
            "nodes": [
                {"id": f"M{i}", "label": f"mod{i}", "module_id": f"mod_{i}", "kind": "struct"}
                for i in range(25)
            ]
        }
        ids = _extract_module_ids(payload)
        assert len(ids) == 20

    def test_deduplicates(self) -> None:
        payload = {
            "nodes": [
                {"id": "A", "label": "a", "module_id": "dup", "kind": "struct"},
                {"id": "B", "label": "b", "module_id": "dup", "kind": "struct"},
            ]
        }
        ids = _extract_module_ids(payload)
        assert ids == ["dup"]

    def test_empty_payload(self) -> None:
        assert _extract_module_ids({}) == []
        assert _extract_module_ids({"nodes": "bad"}) == []


class TestMatchIssueToModule:
    def test_label_hit(self, sample_flow_map: dict[str, dict[str, Any]]) -> None:
        issue = {"labels": ["module:cli"], "scan_tags": [], "title": "x", "body": ""}
        assert _match_issue_to_module(issue, "cli", sample_flow_map) is True

    def test_label_miss_scan_hit(self, sample_flow_map: dict[str, dict[str, Any]]) -> None:
        issue = {"labels": [], "scan_tags": ["C3-P2"], "title": "CLI startup slow", "body": ""}
        assert _match_issue_to_module(issue, "cli", sample_flow_map) is True

    def test_body_substring_hit(self, sample_flow_map: dict[str, dict[str, Any]]) -> None:
        issue = {"labels": [], "scan_tags": ["C3-P1"], "title": "x", "body": "apps/kimi-code broken"}
        assert _match_issue_to_module(issue, "cli", sample_flow_map) is True

    def test_no_scan_tags(self, sample_flow_map: dict[str, dict[str, Any]]) -> None:
        issue = {"labels": [], "scan_tags": [], "title": "x", "body": ""}
        assert _match_issue_to_module(issue, "cli", sample_flow_map) is False

    def test_no_flow_map_rule(self) -> None:
        issue = {"labels": [], "scan_tags": ["C3-P0"], "title": "x", "body": ""}
        assert _match_issue_to_module(issue, "unknown", {}) is False


class TestCountTiers:
    def test_counts(self) -> None:
        issues = [
            {"scan_tags": ["C3-P0"]},
            {"scan_tags": ["C3-P0", "C3-P1"]},
            {"scan_tags": ["C3-P2"]},
            {"scan_tags": []},
        ]
        counts = _count_tiers(issues)
        assert counts == {"p0": 2, "p1": 1, "p2": 1}

    def test_empty(self) -> None:
        assert _count_tiers([]) == {"p0": 0, "p1": 0, "p2": 0}


class TestModuleMatrixServiceBuildMatrix:
    def test_build_matrix(self, sample_payload: dict[str, Any], sample_issues: list[dict[str, Any]], sample_flow_map: dict[str, dict[str, Any]]) -> None:
        fake = FakeSupabase(sample_issues)
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map=sample_flow_map)
        matrix = service.build_matrix(sample_payload, state="open")

        assert len(matrix) == 3
        by_id = {m["module_id"]: m for m in matrix}

        # agent_core: label hit → 1 issue, P0
        ac = by_id["agent_core"]
        assert ac["open_issue_count"] == 1
        assert ac["p0_count"] == 1
        assert ac["p1_count"] == 0
        assert ac["p2_count"] == 0
        assert ac["issue_numbers"] == [545]
        assert ac["sample_issues"][0]["number"] == 545

        # cli: scan_tags + body keyword hit → 1 issue, P2
        cli = by_id["cli"]
        assert cli["open_issue_count"] == 1
        assert cli["p0_count"] == 0
        assert cli["p1_count"] == 0
        assert cli["p2_count"] == 1
        assert cli["issue_numbers"] == [583]

        # node_sdk: scan_tags + body keyword hit → 1 issue, P1
        ns = by_id["node_sdk"]
        assert ns["open_issue_count"] == 1
        assert ns["p0_count"] == 0
        assert ns["p1_count"] == 1
        assert ns["p2_count"] == 0
        assert ns["issue_numbers"] == [708]

    def test_empty_issues(self, sample_payload: dict[str, Any]) -> None:
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        matrix = service.build_matrix(sample_payload, state="open")
        assert len(matrix) == 3
        for m in matrix:
            assert m["open_issue_count"] == 0
            assert m["p0_count"] == 0
            assert m["p1_count"] == 0
            assert m["p2_count"] == 0
            assert m["issue_numbers"] == []
            assert m["sample_issues"] == []

    def test_state_closed_returns_empty(self, sample_payload: dict[str, Any]) -> None:
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        matrix = service.build_matrix(sample_payload, state="closed")
        assert len(matrix) == 3
        for m in matrix:
            assert m["open_issue_count"] == 0

    def test_no_module_nodes(self) -> None:
        payload = {"nodes": [{"id": "FLOW", "kind": "flow"}]}
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        matrix = service.build_matrix(payload, state="open")
        assert matrix == []


class TestModuleMatrixServiceGetModuleEdges:
    def test_extracts_depends_on(self, sample_payload: dict[str, Any]) -> None:
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        edges = service.get_module_edges(sample_payload, relation="depends_on")
        assert len(edges) == 2
        assert edges[0] == {"from": "agent_core", "to": "cli", "relation": "depends_on", "label": ""}
        assert edges[1] == {"from": "cli", "to": "node_sdk", "relation": "depends_on", "label": "加载"}

    def test_ignores_non_module_nodes(self) -> None:
        payload = {
            "nodes": [
                {"id": "AC", "module_id": "agent_core", "kind": "struct"},
                {"id": "FLOW", "kind": "flow"},  # 非 module
            ],
            "edges": [
                {"from": "AC", "to": "FLOW", "type": "depends_on", "graph_id": "g", "label": ""},
            ],
        }
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        edges = service.get_module_edges(payload, relation="depends_on")
        assert edges == []

    def test_ignores_other_relation_types(self, sample_payload: dict[str, Any]) -> None:
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        edges = service.get_module_edges(sample_payload, relation="triggers")
        assert len(edges) == 0  # FLOW_TURN->AC 但 FLOW_TURN 非 module

    def test_empty_payload(self) -> None:
        fake = FakeSupabase([])
        service = ModuleMatrixService(repo_id="repo-1", client=fake, flow_map={})
        assert service.get_module_edges({}, relation="depends_on") == []


# ── API Router Tests ──────────────────────────────────────────────────────

class FakeGraphStoreMatrix:
    """新版 FakeGraphStore：委托 get_module_matrix / get_module_edges。"""

    def __init__(self, snapshot: dict[str, Any] | None) -> None:
        self._snapshot = snapshot

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        return self._snapshot

    def get_module_matrix(self, payload: dict[str, Any], *, state: str = "open") -> list[dict[str, Any]]:
        if not self._snapshot:
            return []
        # 简化：直接返回预构造矩阵（与 ModuleMatrixService 解耦测试）
        return [
            {
                "module_id": "agent_core",
                "label": "agent-core",
                "open_issue_count": 3,
                "p0_count": 1,
                "p1_count": 0,
                "p2_count": 2,
                "issue_numbers": [545, 583, 708],
                "sample_issues": [
                    {"number": 545, "title": "agent-core memory leak", "state": "open", "labels": ["module:agent_core"]},
                    {"number": 583, "title": "CLI startup slow", "state": "open", "labels": []},
                    {"number": 708, "title": "node-sdk type mismatch", "state": "open", "labels": []},
                ],
            },
            {
                "module_id": "cli",
                "label": "kimi CLI",
                "open_issue_count": 1,
                "p0_count": 0,
                "p1_count": 0,
                "p2_count": 1,
                "issue_numbers": [583],
                "sample_issues": [
                    {"number": 583, "title": "CLI startup slow", "state": "open", "labels": []},
                ],
            },
        ]

    def get_module_edges(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"from": "agent_core", "to": "cli", "relation": "depends_on", "label": ""},
        ]


@pytest.fixture
def matrix_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("OPS_DESK_SECRET", "test")
    snapshot = {
        "id": "graph-snapshot-1",
        "source_branch": "cyning/meta",
        "source_commit": "abc123",
        "manifest_version": "2.0.3",
        "payload": {
            "schema_version": "graph_v2",
            "freeze_id": "KIMI-META-GRAPH-V2-BATCH@0fa2d54f",
            "graphs": [{"id": "00_main", "title": "顶层流程总图"}],
            "nodes": [
                {"graph_id": "00_main", "id": "AC", "label": "agent-core", "module_id": "agent_core", "kind": "struct"},
                {"graph_id": "00_main", "id": "CLI", "label": "kimi CLI", "module_id": "cli", "kind": "struct"},
            ],
            "edges": [
                {"from": "AC", "to": "CLI", "type": "depends_on", "graph_id": "00_main"},
            ],
        },
        "created_at": "2026-06-21T00:00:00Z",
    }
    app.dependency_overrides[get_graph_store] = lambda: FakeGraphStoreMatrix(snapshot)
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestModuleIssuesAPIV1:
    def test_module_issues_v1_schema(self, matrix_client: TestClient) -> None:
        resp = matrix_client.get("/api/py/ops/graph/module-issues?state=open", headers={"x-ops-secret": "test"})
        assert resp.status_code == 200
        data = resp.json()
        assert "modules" in data
        modules = data["modules"]
        assert len(modules) <= 20

        # 验证契约字段
        ac = next(m for m in modules if m["module_id"] == "agent_core")
        assert ac["label"] == "agent-core"
        assert ac["open_issue_count"] == 3
        assert ac["p0_count"] == 1
        assert ac["p1_count"] == 0
        assert ac["p2_count"] == 2
        assert ac["issue_numbers"] == [545, 583, 708]
        assert len(ac["sample_issues"]) == 3
        assert ac["sample_issues"][0]["number"] == 545
        assert ac["sample_issues"][0]["title"] == "agent-core memory leak"
        assert ac["sample_issues"][0]["state"] == "open"
        assert "labels" in ac["sample_issues"][0]

        cli = next(m for m in modules if m["module_id"] == "cli")
        assert cli["open_issue_count"] == 1
        assert cli["p2_count"] == 1

    def test_module_issues_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("OPS_DESK_SECRET", "")
        app.dependency_overrides[get_graph_store] = lambda: FakeGraphStoreMatrix(None)
        client = TestClient(app)
        try:
            resp = client.get("/api/py/ops/graph/module-issues", headers={"x-ops-secret": "test"})
            assert resp.status_code == 404
            assert resp.json()["detail"]["code"] == "GRAPH_SNAPSHOT_NOT_FOUND"
        finally:
            app.dependency_overrides.clear()


# ── graph_analyst evidence 测试 ───────────────────────────────────────────

class TestGraphAnalystEvidence:
    def test_evidence_has_module_edges(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """graph_analyst 返回的 evidence 必须含 module_edges。"""
        from api.ops.agents import graph_analyst

        captured_prompt: str = ""

        def fake_chat_completion(messages: list[dict[str, Any]], **kwargs: Any) -> Any:
            nonlocal captured_prompt
            captured_prompt = messages[0]["content"]
            class FakeResult:
                content = '{"reasoning": "r", "suggestion": "s", "confidence": 0.8, "citations": []}'
                class usage:
                    @staticmethod
                    def to_dict() -> dict[str, Any]:
                        return {"provider": "x", "model": "m", "prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2, "latency_ms": 1}
            return FakeResult()

        monkeypatch.setattr(graph_analyst, "chat_completion", fake_chat_completion)

        from api.ops.queries import OpsQueries
        fake_client = FakeSupabase([])
        queries = OpsQueries(fake_client)

        # mock _repo_id 返回固定值
        monkeypatch.setattr(queries, "_repo_id", lambda: "repo-1")

        # mock snapshot 查询
        snapshot_rows = [
            {
                "id": "snap-1",
                "payload": {
                    "nodes": [
                        {"id": "AC", "module_id": "agent_core", "label": "agent-core", "kind": "struct"},
                        {"id": "CLI", "module_id": "cli", "label": "cli", "kind": "struct"},
                    ],
                    "edges": [
                        {"from": "AC", "to": "CLI", "type": "depends_on", "graph_id": "g", "label": ""},
                    ],
                },
            }
        ]

        class FakeSbTable:
            def __init__(self, rows: list[dict[str, Any]]) -> None:
                self._rows = rows
            def select(self, *_cols: str) -> FakeSbTable:
                return self
            def eq(self, _col: str, _value: Any) -> FakeSbTable:
                return self
            def order(self, _col: str, *, desc: bool = False) -> FakeSbTable:
                return self
            def limit(self, _n: int) -> FakeSbTable:
                return self
            def execute(self) -> MagicMock:
                resp = MagicMock()
                resp.data = self._rows
                return resp

        class FakeSb:
            def table(self, _name: str) -> FakeSbTable:
                return FakeSbTable(snapshot_rows)

        monkeypatch.setattr(queries, "client", FakeSb())

        result = graph_analyst.analyze_graph("kimi-code 的模块依赖图长什么样？", queries)

        assert result["found"] is True
        evidence = result["evidence"]
        assert len(evidence) == 1
        assert evidence[0]["kind"] == "graph_snapshot"
        assert "module_edges" in evidence[0]
        module_edges = evidence[0]["module_edges"]
        assert len(module_edges) >= 1
        assert module_edges[0]["from"] == "agent_core"
        assert module_edges[0]["to"] == "cli"
        assert module_edges[0]["relation"] == "depends_on"

        # prompt 中必须包含 edges 摘要
        assert "模块依赖边摘要" in captured_prompt


# ── Store 委托测试 ────────────────────────────────────────────────────────

class TestOpsGraphStoreDelegates:
    def test_get_module_matrix_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from api.ops.graph.store import OpsGraphStore

        fake = FakeSupabase([])
        store = OpsGraphStore(repo_id="repo-1", client=fake)
        payload = {
            "nodes": [
                {"id": "AC", "module_id": "agent_core", "label": "agent-core", "kind": "struct"},
            ],
            "edges": [],
        }
        matrix = store.get_module_matrix(payload, state="open")
        assert isinstance(matrix, list)
        assert len(matrix) == 1
        assert matrix[0]["module_id"] == "agent_core"

    def test_get_module_edges_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from api.ops.graph.store import OpsGraphStore

        fake = FakeSupabase([])
        store = OpsGraphStore(repo_id="repo-1", client=fake)
        payload = {
            "nodes": [
                {"id": "AC", "module_id": "agent_core", "label": "agent-core", "kind": "struct"},
                {"id": "CLI", "module_id": "cli", "label": "cli", "kind": "struct"},
            ],
            "edges": [
                {"from": "AC", "to": "CLI", "type": "depends_on", "graph_id": "g", "label": ""},
            ],
        }
        edges = store.get_module_edges(payload)
        assert len(edges) == 1
        assert edges[0]["from"] == "agent_core"
        assert edges[0]["to"] == "cli"
