#!/usr/bin/env python3
"""PR 全绿后更新 body：CI 状态表、Test plan 勾选、变更范围统计。见 SPEC-Governance-PR-Post-CI-v1。"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# 与 branch protection / Mergify 对齐；前端仓镜像时须改此表
REQUIRED_CHECKS = frozenset(
    {
        "pytest",
        "manifest_check",
        "contract_check",
    }
)

BLOCK_AUTOMERGE_PREFIXES = (
    "api/",
    "tests/",
    ".github/workflows/",
    "supabase/",
)

CI_SECTION = "## CI 状态（自动 · pr-post-ci）"
SCOPE_SECTION = "## 变更范围（自动统计）"
TEST_PLAN_HEADER = "## Test plan"

# Required 全绿时可自动勾选；含下列词的条目保留人工（#56 教训）
TEST_PLAN_MANUAL_LINE = re.compile(
    r"合入后|下一支|后续|可选|端到端|automerge|Mergify",
    re.IGNORECASE,
)

# CI 表仅展示 Required，避免 Mergify/Vercel 等 in_progress 误导
NOISE_CHECK_PREFIXES = ("Vercel", "Mergify")


def _run(cmd: list[str], *, check: bool = True) -> str:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout.strip()


def fetch_pr_state(pr: int) -> str:
    return _run(["gh", "pr", "view", str(pr), "--json", "state", "-q", ".state"])


def fetch_checks(pr: int) -> list[dict]:
    raw = _run(
        [
            "gh",
            "pr",
            "view",
            str(pr),
            "--json",
            "statusCheckRollup",
        ]
    )
    data = json.loads(raw)
    rollup = data.get("statusCheckRollup") or []
    out: list[dict] = []
    for item in rollup:
        name = item.get("name") or item.get("context") or ""
        if not name:
            continue
        conclusion = item.get("conclusion")
        state = item.get("state") or item.get("status")
        if conclusion:
            status = conclusion.lower()
        elif state:
            status = state.lower()
        else:
            status = "unknown"
        out.append({"name": name, "status": status})
    return out


def is_noise_check(name: str) -> bool:
    return any(name.startswith(prefix) for prefix in NOISE_CHECK_PREFIXES)


def checks_for_ci_table(checks: list[dict]) -> list[dict]:
    """CI 状态表只列 Required checks。"""
    return [c for c in checks if c["name"] in REQUIRED_CHECKS]


def all_required_green(checks: list[dict]) -> bool:
    by_name = {c["name"]: c["status"] for c in checks}
    for req in REQUIRED_CHECKS:
        if by_name.get(req) != "success":
            return False
    return True


def fetch_changed_files(pr: int) -> list[str]:
    raw = _run(["gh", "pr", "diff", str(pr), "--name-only"])
    return [line for line in raw.splitlines() if line.strip()]


def top_level_stats(files: list[str]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for f in files:
        parts = f.split("/")
        key = parts[0] if len(parts) == 1 else f"{parts[0]}/"
        counter[key] += 1
    return counter


def has_blocked_paths(files: list[str]) -> list[str]:
    hits: list[str] = []
    for f in files:
        for prefix in BLOCK_AUTOMERGE_PREFIXES:
            if f.startswith(prefix):
                hits.append(f)
                break
    return hits


def render_ci_table(checks: list[dict], *, green: bool) -> str:
    display = checks_for_ci_table(checks)
    lines = [
        CI_SECTION,
        "",
        f"> 更新：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        f"`tools/pr_post_ci_update_body.py`",
        "",
        f"**Required 全绿**：{'是' if green else '否'}",
        "",
        "| Check | Status |",
        "| --- | --- |",
    ]
    for c in sorted(display, key=lambda x: x["name"]):
        lines.append(f"| {c['name']} | {c['status']} |")
    lines.append("")
    return "\n".join(lines)


def render_scope_table(files: list[str]) -> str:
    stats = top_level_stats(files)
    blocked = has_blocked_paths(files)
    lines = [
        SCOPE_SECTION,
        "",
        f"**文件数**：{len(files)}",
        "",
        "| 顶层前缀 | 计数 |",
        "| --- | --- |",
    ]
    for prefix, count in stats.most_common():
        lines.append(f"| `{prefix}` | {count} |")
    if blocked:
        lines.extend(
            [
                "",
                "**⚠ automerge 路径闸**：含 `api/`、`tests/`、`.github/workflows/` 等 — "
                "勿打 `automerge` 或须人审 merge。",
                "",
                "<details><summary>命中路径</summary>",
                "",
            ]
        )
        for p in blocked[:40]:
            lines.append(f"- `{p}`")
        if len(blocked) > 40:
            lines.append(f"- … 另有 {len(blocked) - 40} 个")
        lines.append("")
        lines.append("</details>")
    lines.append("")
    return "\n".join(lines)


def upsert_section(body: str, section_header: str, new_content: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(section_header)}.*?(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(body):
        return pattern.sub(new_content + "\n", body, count=1)
    sep = "\n\n" if body.rstrip() else ""
    return body.rstrip() + sep + new_content + "\n"


def should_auto_tick_test_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("- [ ]"):
        return False
    return TEST_PLAN_MANUAL_LINE.search(stripped) is None


def tick_test_plan(body: str, *, green: bool) -> str:
    if not green:
        return body

    section = re.compile(
        rf"^({re.escape(TEST_PLAN_HEADER)}\s*\n)(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )

    def _replace_section(match: re.Match[str]) -> str:
        header, content = match.group(1), match.group(2)
        new_lines: list[str] = []
        for line in content.splitlines():
            if should_auto_tick_test_line(line):
                line = line.replace("- [ ]", "- [x]", 1)
            new_lines.append(line)
        body_part = "\n".join(new_lines)
        if content.endswith("\n"):
            body_part += "\n"
        return header + body_part

    if section.search(body):
        return section.sub(_replace_section, body, count=1)
    return body


def update_body(pr: int) -> tuple[str, bool]:
    body = _run(["gh", "pr", "view", str(pr), "--json", "body", "-q", ".body"])
    checks = fetch_checks(pr)
    green = all_required_green(checks)
    files = fetch_changed_files(pr)

    body = upsert_section(body, CI_SECTION, render_ci_table(checks, green=green))
    body = upsert_section(body, SCOPE_SECTION, render_scope_table(files))
    body = tick_test_plan(body, green=green)
    return body, green


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    state = fetch_pr_state(args.pr)
    if state != "OPEN":
        print(f"PR #{args.pr} state={state}; skip body update", file=sys.stderr)
        return 0

    new_body, green = update_body(args.pr)
    if args.dry_run:
        print(new_body)
        print(f"\n# required_all_green={green}", file=sys.stderr)
        return 0

    tmp = REPO_ROOT / "tmp" / f"pr_{args.pr}_body.md"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(new_body, encoding="utf-8")
    _run(["gh", "pr", "edit", str(args.pr), "--body-file", str(tmp)])
    print(f"PR #{args.pr} body updated; required_all_green={green}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
