from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest


class _FakeQuery:
    def __init__(self, table: str, parent: "_FakeSB"):
        self.table = table
        self.parent = parent
        self._filters: list[tuple[str, str, str]] = []
        self._in_ids: list[str] | None = None

    def select(self, _cols: str) -> "_FakeQuery":
        return self

    def eq(self, col: str, val: str) -> "_FakeQuery":
        self._filters.append(("eq", col, val))
        return self

    def in_(self, col: str, ids: list[str]) -> "_FakeQuery":
        self._in_ids = ids
        return self

    def insert(self, rows: list[dict[str, Any]]) -> "_FakeQuery":
        self.parent.insert_calls.append((self.table, rows))
        return self

    def delete(self) -> "_FakeQuery":
        return self

    def execute(self) -> Any:
        # select ids for delete path
        if self.table == "code_chunks" and self._filters:
            # metadata->>relativePath eq ...
            rel = None
            for op, col, val in self._filters:
                if op == "eq" and col == "metadata->>relativePath":
                    rel = val
            assert rel is not None
            ids = [r["id"] for r in self.parent.rows if r.get("metadata", {}).get("relativePath") == rel]
            return type("R", (), {"data": [{"id": i} for i in ids]})()

        return type("R", (), {"data": []})()


class _FakeSB:
    def __init__(self):
        self.rows: list[dict[str, Any]] = []
        self.insert_calls: list[tuple[str, list[dict[str, Any]]]] = []
        self.rpc_calls: list[tuple[str, dict[str, Any]]] = []

    def table(self, name: str) -> _FakeQuery:
        return _FakeQuery(name, self)

    def rpc(self, name: str, params: dict[str, Any]) -> Any:
        self.rpc_calls.append((name, params))

        class _R:
            def execute(self_inner) -> Any:
                return type("R", (), {"data": []})()

        return _R()


def test_process_code_files_deletes_then_inserts(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    import api.code_ingest as ci

    repo = tmp_path
    (repo / "api").mkdir(parents=True, exist_ok=True)
    (repo / "api" / "demo.py").write_text("def foo():\n    return 1\n", encoding="utf-8")

    fake_sb = _FakeSB()
    # 预置旧数据：同 relativePath 应被删除
    fake_sb.rows.append(
        {
            "id": "old-1",
            "metadata": {"relativePath": "api/demo.py"},
        }
    )

    monkeypatch.setattr(ci, "supabase_client", lambda: fake_sb)
    monkeypatch.setattr(ci, "openai_siliconflow_client", lambda: object())

    vectors = [[0.0] * 1024]

    def fake_embed(_client: object, texts: list[str]) -> list[list[float]]:
        assert texts, "empty embed batch"
        return [vectors[0] for _ in texts]

    monkeypatch.setattr(ci, "embed_texts_batch", fake_embed)

    # patch delete on table chain end-to-end: reuse FakeQuery delete path
    # Our FakeQuery delete().in_().execute isn't fully modeled; instead monkeypatch delete function
    monkeypatch.setattr(ci, "delete_code_chunks_by_relative_prefixes", lambda sb, prefixes: 0)
    monkeypatch.setattr(ci, "delete_code_chunks_by_relative_paths", lambda sb, paths: 3)

    res = ci.process_code_files(repo_root=repo)
    assert res["filesScanned"] == 1
    assert res["chunksTotal"] >= 1
    assert res["chunksInserted"] >= 1
    assert res["rowsDeleted"] == 3

    assert fake_sb.insert_calls, "expected insert"
    table, rows = fake_sb.insert_calls[0]
    assert table == "code_chunks"
    assert isinstance(rows, list) and rows
    row0 = rows[0]
    assert "embedding" in row0 and "metadata" in row0 and "content" in row0
    assert row0["metadata"]["relativePath"] == "api/demo.py"
    assert row0["metadata"]["category"] == "code"

    assert any(name == "refresh_code_chunks_fts_tokens_for_paths" for name, _ in fake_sb.rpc_calls)
