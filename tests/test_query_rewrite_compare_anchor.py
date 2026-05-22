"""query_compare / compare_anchor_tokens 单测（task_05 可观测性）。"""

from __future__ import annotations

from api.keyword_fallback import compare_anchor_tokens, extract_anchor_tokens


def test_extract_anchor_tokens_task_and_file_and_date() -> None:
    raw = "task_04 和 2026-05-14.md 有什么关系"
    tokens = extract_anchor_tokens(raw)
    assert any("task" in t.lower() for t in tokens)
    assert any("2026" in t for t in tokens)
    assert any(t.endswith(".md") for t in tokens)


def test_compare_anchor_tokens_detects_missing_task_id() -> None:
    raw = "请总结 task_04 的要点"
    rewritten = "请总结第四项任务的要点"
    cmp = compare_anchor_tokens(raw, rewritten)
    assert cmp["is_key_entity_lost"] is True
    assert "task_04" in cmp["missing"] or any("task" in m.lower() for m in cmp["missing"])


def test_compare_anchor_tokens_no_loss_when_preserved() -> None:
    raw = "打开 notes/2026-05-14.md"
    rewritten = "打开 notes/2026-05-14.md 文件"
    cmp = compare_anchor_tokens(raw, rewritten)
    assert cmp["is_key_entity_lost"] is False
    assert cmp["missing"] == []


def test_compare_anchor_tokens_empty_rewrite() -> None:
    raw = "task_05 日志字段"
    cmp = compare_anchor_tokens(raw, "")
    assert cmp["is_key_entity_lost"] is True
    assert len(cmp["missing"]) >= 1
