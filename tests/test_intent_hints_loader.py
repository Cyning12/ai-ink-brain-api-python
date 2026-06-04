from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from api.intent_hints import (
    build_intent_hints_prompt_block,
    clear_intent_hints_cache,
    load_hints,
    load_resolved_hints,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_yaml_path() -> Path:
    return _repo_root() / "docs/chatbi/v1/intent_hints.yaml"


def test_load_default_intent_hints_yaml() -> None:
    clear_intent_hints_cache()
    data = load_hints(_default_yaml_path())
    assert isinstance(data, dict)
    assert data.get("version") == 1
    assert data.get("site_mode") == "portfolio"


def test_build_prompt_block_contains_site_context() -> None:
    data = load_hints(_default_yaml_path())
    assert data is not None
    block = build_intent_hints_prompt_block(data)
    assert "## 站点上下文（配置 · intent_hints.yaml）" in block
    assert "刘新宁" in block
    assert "11 年经历里 AI Coding 相关成果？" in block


def test_load_resolved_hints_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_intent_hints_cache()
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "false")
    assert load_resolved_hints() is None


def test_load_resolved_hints_missing_path(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_intent_hints_cache()
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "true")
    monkeypatch.setenv("INTENT_HINTS_PATH", "/nonexistent/intent_hints.yaml")
    assert load_resolved_hints() is None


def test_load_hints_corrupt_yaml(tmp_path: Path) -> None:
    clear_intent_hints_cache()
    bad = tmp_path / "bad.yaml"
    bad.write_text(":\n  - [unclosed", encoding="utf-8")
    assert load_hints(bad) is None


def test_load_hints_non_dict_root(tmp_path: Path) -> None:
    clear_intent_hints_cache()
    p = tmp_path / "list.yaml"
    p.write_text("- only\n- list\n", encoding="utf-8")
    assert load_hints(p) is None


def test_build_prompt_block_empty_when_no_content() -> None:
    assert build_intent_hints_prompt_block(None) == ""
    assert build_intent_hints_prompt_block({}) == ""


def test_load_hints_utf8_bom(tmp_path: Path) -> None:
    clear_intent_hints_cache()
    p = tmp_path / "bom.yaml"
    p.write_bytes(b"\xef\xbb\xbf" + b"version: 1\nsite_mode: portfolio\n")
    data = load_hints(p)
    assert data is not None
    assert data.get("version") == 1


def test_custom_path_via_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    clear_intent_hints_cache()
    custom = tmp_path / "custom.yaml"
    custom.write_text(
        textwrap.dedent(
            """
            version: 1
            product_summary: custom portfolio hint
            few_shots:
              - query: "test q"
                tool: rag_search
                reasoning: custom
            """
        ).strip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "true")
    monkeypatch.setenv("INTENT_HINTS_PATH", str(custom))
    data = load_resolved_hints()
    assert data is not None
    block = build_intent_hints_prompt_block(data)
    assert "custom portfolio hint" in block
