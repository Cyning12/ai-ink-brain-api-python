from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

mod = importlib.import_module("tools.pr_post_ci_update_body")


def test_all_required_green():
    checks = [
        {"name": "pytest", "status": "success"},
        {"name": "manifest_check", "status": "success"},
        {"name": "contract_check", "status": "success"},
        {"name": "Mergify Merge Queue", "status": "in_progress"},
    ]
    assert mod.all_required_green(checks) is True


def test_all_required_green_missing():
    checks = [{"name": "pytest", "status": "success"}]
    assert mod.all_required_green(checks) is False


def test_checks_for_ci_table_only_required():
    checks = [
        {"name": "pytest", "status": "success"},
        {"name": "verify", "status": "success"},
        {"name": "Mergify Merge Queue", "status": "neutral"},
    ]
    table = mod.checks_for_ci_table(checks)
    assert [c["name"] for c in table] == ["pytest"]


def test_tick_test_plan_smoke_like_56():
    body = """## Test plan

- [ ] pytest / manifest_check / contract_check 全绿
- [ ] PR body 出现 `## CI 状态（自动 · pr-post-ci）` 且 Required 全绿后勾选本段
- [ ] 打 `automerge` 后 Mergify 自动 squash merge

## automerge
"""
    out = mod.tick_test_plan(body, green=True)
    assert "- [x] pytest / manifest_check / contract_check 全绿" in out
    assert "- [x] PR body 出现" in out
    assert "打 `automerge` 后 Mergify" in out
    assert "- [ ] 打 `automerge`" in out


def test_tick_test_plan_skips_when_not_green():
    body = "## Test plan\n\n- [ ] pytest 绿\n"
    assert mod.tick_test_plan(body, green=False) == body


def test_tick_test_plan_excludes_post_merge_items():
    body = """## Test plan

- [ ] CI 绿
- [ ] 合入后开一支仅 docs PR 验证

## Summary
"""
    out = mod.tick_test_plan(body, green=True)
    assert "- [x] CI 绿" in out
    assert "- [ ] 合入后开一支" in out


def test_render_ci_table_no_mergify_row():
    checks = [
        {"name": "pytest", "status": "success"},
        {"name": "Mergify Merge Queue", "status": "in_progress"},
    ]
    table = mod.render_ci_table(checks, green=True)
    assert "Mergify" not in table
    assert "| pytest | success |" in table


@pytest.mark.parametrize(
    "line,expected",
    [
        ("- [ ] pytest / manifest_check 全绿", True),
        ("- [ ] 打 automerge 后 Mergify merge", False),
        ("- [ ] 合入后验证", False),
        ("- [x] already done", False),
    ],
)
def test_should_auto_tick_test_line(line: str, expected: bool):
    assert mod.should_auto_tick_test_line(line) is expected


def test_fetch_changed_files_prefers_pr_view_files(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], *, check: bool = True) -> str:
        calls.append(cmd)
        if cmd[:4] == ["gh", "pr", "view", str(78)] and "files" in cmd:
            return "docs/a.md\napi/b.py\n"
        raise AssertionError(f"unexpected cmd: {cmd}")

    monkeypatch.setattr(mod, "_run", fake_run)
    assert mod.fetch_changed_files(78) == ["docs/a.md", "api/b.py"]
    assert len(calls) == 1
