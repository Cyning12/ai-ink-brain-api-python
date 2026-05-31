"""图谱 manifest / contract CI 失败时的三段式 stderr（IMP-B-01）。"""
from __future__ import annotations

from dataclasses import dataclass

RUNBOOK_REL = "docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md"


@dataclass(frozen=True)
class CiIssue:
    """单条 drift：位置 · 文档声明 · 当前代码。"""

    location: str
    declared: str
    actual: str


def print_ci_failure(
    *,
    title: str,
    check_name: str,
    local_command: str,
    issues: list[CiIssue],
) -> None:
    """向 stderr 打印 F20 对齐的三段式失败摘要。"""
    print(f"❌ {title}")
    print(f"检查: {check_name}")
    print()
    for i, issue in enumerate(issues, start=1):
        print(f"--- 问题 {i}/{len(issues)} ---")
        print(f"位置: {issue.location}")
        print(f"文档声明: {issue.declared}")
        print(f"当前代码: {issue.actual}")
        print()
    print("你可以:")
    print("  1. 若确属契约变更：在任务单 §行为变更 写明 → 同 PR 更新锚点/manifest/contract 与 .ai.md → 补 pytest；")
    print("  2. 若为误改：回滚 api/ 或相关 hunks；")
    print(f"  3. 本地运行与 CI 相同命令，确认变绿后再 push：")
    print(f"     {local_command}")
    print(f"Runbook: {RUNBOOK_REL}")
