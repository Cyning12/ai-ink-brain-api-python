"""W1 · rag_env helper 行为单测（index env 收敛）。"""

from __future__ import annotations

import importlib

import pytest


@pytest.fixture()
def rag_env_module(monkeypatch: pytest.MonkeyPatch):
    """每次测试前重载 rag_env，避免模块级 env 缓存污染。"""
    monkeypatch.delenv("CONTENT_DEFAULT_YEAR", raising=False)
    monkeypatch.delenv("SILICONFLOW_CHAT_MODEL", raising=False)
    monkeypatch.delenv("MAX_X_SOURCES_HEADER_CHARS", raising=False)
    monkeypatch.delenv("DEBUG_RAG", raising=False)
    monkeypatch.delenv("RAG_DEBUG", raising=False)
    monkeypatch.delenv("NODE_ENV", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("SILICONFLOW_API_KEY", raising=False)
    import api.rag_env as rag_env

    return importlib.reload(rag_env)


def test_content_default_year_default(rag_env_module):
    assert rag_env_module.content_default_year() == 2026


def test_content_default_year_override(rag_env_module, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CONTENT_DEFAULT_YEAR", "2024")
    assert rag_env_module.content_default_year() == 2024


def test_siliconflow_chat_model_default(rag_env_module):
    assert rag_env_module.siliconflow_chat_model() == rag_env_module.DEFAULT_SILICONFLOW_CHAT_MODEL


def test_max_x_sources_header_chars_default(rag_env_module):
    assert rag_env_module.max_x_sources_header_chars() == 6000


def test_rag_debug_enabled_by_flag(rag_env_module, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEBUG_RAG", "1")
    assert rag_env_module.rag_debug_enabled() is True


def test_rag_debug_enabled_by_node_env(rag_env_module, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NODE_ENV", "development")
    assert rag_env_module.rag_debug_enabled() is True


def test_api_key_optional_empty(rag_env_module, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("API_KEY", "")
    assert rag_env_module.api_key_optional() is None


def test_api_key_optional_set(rag_env_module, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("API_KEY", " test-key ")
    assert rag_env_module.api_key_optional() == "test-key"


def test_siliconflow_api_key_optional(rag_env_module, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SILICONFLOW_API_KEY", " sf-key ")
    assert rag_env_module.siliconflow_api_key_optional() == "sf-key"


def test_index_has_no_scattered_getenv():
    """回归：index.py 不得再散落 os.getenv（P-03）。"""
    from pathlib import Path

    text = Path("api/index.py").read_text(encoding="utf-8")
    assert "os.getenv" not in text
    assert "os.environ" not in text
