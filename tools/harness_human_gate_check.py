#!/usr/bin/env python3
"""Harness human_gate 机器门禁：文件内 status 非 approved 则 exit 1。

与 Prompt / semi_auto / 【授权】无关；合入前对「执行产物」diff 强制校验。
真值：docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md §2.3
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ACTIVE_TASKS = REPO_ROOT / "docs" / "tasks" / "active"

# PR 出现下列变更 ⇒ 视为已「执行」Harness / Wiki ingest，须闸口已 approved
EXECUTION_PATH_PREFIXES = (
    "docs/harness/reviews/by-task/",
    "docs/harness/invokes/by-task/",
    "docs/tasks/reinspect_results/",
    "docs/coding_wiki/syntheses/",
)

PLANNING_BASENAMES = frozenset(
    {
        "LOOP_MANIFEST.md",
        "README.md",
    }
)

PLANNING_PREFIXES = (
    "PROMPT_START",
    "PROMPT_LOOP",
    "PROMPT_BATCH",
    "PROMPT_TASK_",
)

TABLE_ROW = re.compile(
    r"^\|\s*(HG-[A-Z0-9-]+)\s*\|\s*(pending|approved)\s*\|",
    re.IGNORECASE,
)
HTML_GATE = re.compile(
    r"human_gate:(?P<id>HG-[A-Z0-9-]+)\s+status=(?P<status>pending|approved)",
    re.IGNORECASE,
)
MOTHER_LINK = re.compile(
    r"task_harness_wiki_loop_[a-z0-9_]+\.md",
    re.IGNORECASE,
)
TASK_SLUG_FIELD = re.compile(r"^\|\s*\*\*task_slug\*\*\s*\|\s*`?([a-z0-9-]+)`?\s*\|", re.M)
BY_TASK_SLUG = re.compile(r"docs/harness/[^/]+/by-task/([a-z0-9-]+)/")


@dataclass(frozen=True)
class GateFinding:
    task_path: Path
    gate_id: str
    status: str
    source: str  # table | html


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_gates(text: str, source_label: str) -> list[GateFinding]:
    findings: list[GateFinding] = []
    for line in text.splitlines():
        m = TABLE_ROW.match(line.strip())
        if m:
            gid, status = m.group(1), m.group(2).lower()
            if status == "pending":
                findings.append(
                    GateFinding(
                        task_path=Path(source_label),
                        gate_id=gid,
                        status=status,
                        source="table",
                    )
                )
        m2 = HTML_GATE.search(line)
        if m2 and m2.group("status").lower() == "pending":
            findings.append(
                GateFinding(
                    task_path=Path(source_label),
                    gate_id=m2.group("id"),
                    status="pending",
                    source="html",
                )
            )
    return findings


def gates_in_file(path: Path) -> list[GateFinding]:
    if not path.is_file():
        return []
    rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
    raw = parse_gates(_read(path), str(rel))
    return [GateFinding(path, f.gate_id, f.status, f.source) for f in raw]


def mother_task_paths(child_path: Path, text: str) -> list[Path]:
    paths: list[Path] = []
    for m in MOTHER_LINK.finditer(text):
        name = m.group(0)
        for candidate in (ACTIVE_TASKS / name, REPO_ROOT / "docs" / "tasks" / "active" / name):
            if candidate.is_file():
                paths.append(candidate)
                break
    if "继承母" in text or "inherit" in text.lower():
        for line in text.splitlines():
            if "task_harness_wiki_loop" in line and ".md" in line:
                for part in re.findall(r"[\w./-]+\.md", line):
                    p = (REPO_ROOT / part).resolve() if not part.startswith("docs/") else REPO_ROOT / part
                    if p.is_file():
                        paths.append(p)
    return list(dict.fromkeys(paths))


def collect_tasks(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for p in paths:
        if not p.is_file():
            continue
        queue = [p.resolve()]
        while queue:
            cur = queue.pop(0)
            if cur in seen:
                continue
            seen.add(cur)
            out.append(cur)
            text = _read(cur)
            for mp in mother_task_paths(cur, text):
                if mp.resolve() not in seen:
                    queue.append(mp.resolve())
    return out


def active_tasks_with_gates() -> list[Path]:
    if not ACTIVE_TASKS.is_dir():
        return []
    return sorted(p for p in ACTIVE_TASKS.glob("*.md") if "### 人工闸" in _read(p) or "human_gate_id" in _read(p))


def slug_to_active_tasks(slug: str) -> list[Path]:
    hits: list[Path] = []
    for p in active_tasks_with_gates():
        text = _read(p)
        if f"**task_slug**` | `{slug}`" in text or f'task_slug** | `{slug}`' in text:
            hits.append(p)
        elif f"**task_slug** | {slug}" in text:
            hits.append(p)
        elif f"| `{slug}` |" in text and "task_slug" in text:
            hits.append(p)
    return hits


def is_execution_artifact(path: str) -> bool:
    if not any(path.startswith(prefix) for prefix in EXECUTION_PATH_PREFIXES):
        return False
    base = path.rsplit("/", 1)[-1]
    if base in PLANNING_BASENAMES:
        return False
    if any(base.startswith(p) for p in PLANNING_PREFIXES):
        return False
    if "/invokes/by-task/" in path and base.startswith("invoke_"):
        return True
    if path.startswith("docs/harness/reviews/by-task/") and base.endswith(".md"):
        return True
    if path.startswith("docs/tasks/reinspect_results/") and base.startswith("reinspect_"):
        return True
    if path.startswith("docs/coding_wiki/syntheses/") and base.endswith(".md"):
        return True
    return False


def git_changed_files(base_ref: str) -> list[str]:
    for ref in (base_ref, "origin/main", "main"):
        try:
            out = subprocess.check_output(
                ["git", "diff", "--name-only", f"{ref}...HEAD"],
                cwd=REPO_ROOT,
                text=True,
            )
            return [ln.strip() for ln in out.splitlines() if ln.strip()]
        except subprocess.CalledProcessError:
            continue
    out = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=REPO_ROOT,
        text=True,
    )
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def tasks_from_pr_diff(base_ref: str) -> list[Path]:
    changed = git_changed_files(base_ref)
    exec_paths = [p for p in changed if is_execution_artifact(p)]
    if not exec_paths:
        return []

    task_paths: list[Path] = []
    for p in exec_paths:
        m = BY_TASK_SLUG.search(p)
        if m:
            task_paths.extend(slug_to_active_tasks(m.group(1)))
    # 有执行产物时，扫描全部带闸 active task（防漏关联）
    task_paths.extend(active_tasks_with_gates())
    return collect_tasks(task_paths)


def check_tasks(task_files: list[Path]) -> list[GateFinding]:
    pending: list[GateFinding] = []
    for tp in collect_tasks(task_files):
        pending.extend(gates_in_file(tp))
    return pending


def format_report(findings: list[GateFinding]) -> str:
    lines = [
        "HARNESS_HUMAN_GATE_FAIL: human_gate 仍为 pending，禁止 Harness 执行产物合入。",
        "（与 Prompt / semi_auto / 【授权】无关；须人在 task 中将 status 改为 approved。）",
        "",
    ]
    for f in findings:
        rel = f.task_path if isinstance(f.task_path, Path) else Path(f.task_path)
        if isinstance(rel, Path) and rel.is_absolute():
            try:
                rel = rel.relative_to(REPO_ROOT)
            except ValueError:
                pass
        lines.append(f"  - {f.gate_id} ({f.source}) @ {rel}")
    lines.extend(
        [
            "",
            "修复：人改 task human_gate 表 pending→approved（建议单独 commit）。",
            "自检：python tools/harness_human_gate_check.py --task docs/tasks/active/<task>.md",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Harness human_gate 机器门禁")
    parser.add_argument(
        "--task",
        action="append",
        dest="tasks",
        metavar="PATH",
        help="检查指定 task（可重复）；Loop 子 task 会连带母单",
    )
    parser.add_argument(
        "--all-active",
        action="store_true",
        help="检查 docs/tasks/active 下所有含 human_gate 的 task",
    )
    parser.add_argument(
        "--pr-diff",
        action="store_true",
        help="若相对 base 的 diff 含 Harness 执行产物，则校验关联 task 闸口",
    )
    parser.add_argument(
        "--base",
        default="origin/main",
        help="--pr-diff 用的 git base（默认 origin/main）",
    )
    args = parser.parse_args(argv)

    task_files: list[Path] = []
    if args.tasks:
        task_files = [(REPO_ROOT / t).resolve() if not Path(t).is_absolute() else Path(t) for t in args.tasks]
    elif args.all_active:
        task_files = active_tasks_with_gates()
    elif args.pr_diff:
        task_files = tasks_from_pr_diff(args.base)
        if not task_files:
            print("harness_human_gate_check: no execution artifacts in diff — skip")
            return 0
    else:
        parser.error("specify --task, --all-active, or --pr-diff")

    pending = check_tasks(task_files)
    if pending:
        print(format_report(pending), file=sys.stderr)
        return 1
    print("harness_human_gate_check: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
