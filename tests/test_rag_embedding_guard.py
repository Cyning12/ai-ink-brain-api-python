from __future__ import annotations

import pytest

from api.rag_embedding_guard import (
    EMBEDDING_MISMATCH_ERROR_CODE,
    check_embedding_alignment,
    clear_embedding_alignment_cache,
    embedding_mismatch_mode,
    ensure_embedding_alignment,
)


class _FakeQuery:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def select(self, *_args: object, **_kwargs: object) -> _FakeQuery:
        return self

    def limit(self, *_args: object, **_kwargs: object) -> _FakeQuery:
        return self

    def execute(self) -> object:
        class _Res:
            data = None

        res = _Res()
        res.data = self._rows
        return res


class _FakeSb:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def table(self, _name: str) -> _FakeQuery:
        return _FakeQuery(self._rows)


def test_check_alignment_ok_when_models_match(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SILICONFLOW_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
    monkeypatch.setenv("EMBEDDING_DIM", "1024")
    rows = [{"metadata": {"embedding_model": "Qwen/Qwen3-Embedding-0.6B", "embedding_dim": 1024}}]
    alignment = check_embedding_alignment(_FakeSb(rows))
    assert alignment.ok is True
    assert alignment.error_code is None


def test_check_alignment_fail_on_model_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-m3")
    monkeypatch.setenv("EMBEDDING_DIM", "1024")
    rows = [{"metadata": {"embedding_model": "Qwen/Qwen3-Embedding-0.6B", "embedding_dim": 1024}}]
    alignment = check_embedding_alignment(_FakeSb(rows))
    assert alignment.ok is False
    assert alignment.error_code == EMBEDDING_MISMATCH_ERROR_CODE
    assert "BAAI/bge-m3" in (alignment.message or "")


def test_check_alignment_fail_on_multiple_stored_models(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SILICONFLOW_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
    rows = [
        {"metadata": {"embedding_model": "Qwen/Qwen3-Embedding-0.6B"}},
        {"metadata": {"embedding_model": "BAAI/bge-m3"}},
    ]
    alignment = check_embedding_alignment(_FakeSb(rows))
    assert alignment.ok is False
    assert "多种 embedding_model" in (alignment.message or "")


def test_ensure_alignment_block_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_embedding_alignment_cache()
    monkeypatch.setenv("RAG_EMBEDDING_MISMATCH_MODE", "block")
    monkeypatch.setenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-m3")
    rows = [{"metadata": {"embedding_model": "Qwen/Qwen3-Embedding-0.6B", "embedding_dim": 1024}}]
    alignment = ensure_embedding_alignment(_FakeSb(rows))
    assert alignment.ok is False


def test_ensure_alignment_warn_mode_allows(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_embedding_alignment_cache()
    monkeypatch.setenv("RAG_EMBEDDING_MISMATCH_MODE", "warn")
    monkeypatch.setenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-m3")
    rows = [{"metadata": {"embedding_model": "Qwen/Qwen3-Embedding-0.6B", "embedding_dim": 1024}}]
    alignment = ensure_embedding_alignment(_FakeSb(rows))
    assert alignment.ok is True
    assert alignment.message


def test_embedding_mismatch_mode_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RAG_EMBEDDING_MISMATCH_MODE", "off")
    assert embedding_mismatch_mode() == "off"
    monkeypatch.setenv("RAG_EMBEDDING_MISMATCH_MODE", "warn")
    assert embedding_mismatch_mode() == "warn"
