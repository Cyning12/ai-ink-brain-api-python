"""Task markdown human_gate 表解析与 patch。"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from api.harness_runtime.errors import (
    GateNotFoundError,
    GateStatusInvalidError,
    GateTableMissingError,
)
from api.harness_runtime.session_store.schema import GateSummary, SessionMeta

ALLOWED_GATE_STATUSES = frozenset({"pending", "approved"})
HG_PROMOTE_OVERWRITE = "HG-PROMOTE-OVERWRITE"
_GATE_HEADER = re.compile(r"^\|\s*human_gate_id\s*\|", re.IGNORECASE)
_SEPARATOR = re.compile(r"^\|\s*[-:]+\s*\|")


@dataclass(frozen=True)
class GateRow:
    human_gate_id: str
    status: str
    blocks_hats: str
    description: str


def render_session_task_template(*, slug: str, title: str) -> str:
    """Session 内 task 草稿 · 种子闸对齐 SPEC §6.1 最小集。"""
    return f"""# Task · {title}

> **状态**：`draft`
> **session_slug**：`{slug}`

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `{slug}` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-SESSION-PLAN | pending | dispatch | 00 计划呈现 · 用户授权开始派工 |
| HG-EXEC-AUTH | pending | 30 | 授权进入实现 / promote |
| HG-AUDIT-R1 | pending | — | promote 后业务 task 开工闸（复制到业务仓后签收） |
| HG-PROMOTE | pending | — | 显式 promote 到业务仓（可选） |
| HG-PROMOTE-OVERWRITE | pending | — | overwrite/merge 冲突时 maintainer 二次确认 |
| HG-PROMOTE-GRAPH | pending | — | graph_delta promote 到 _tech_graph 须显式确认 |

## 背景与目标

（Session Orchestrator 草稿 · 由 00 维护）

## 验收标准

- [ ] （待 00 回填）
"""


def parse_gate_table(content: str) -> list[GateRow]:
    """解析 markdown human_gate 表。"""
    lines = content.splitlines()
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        if _GATE_HEADER.match(line.strip()):
            header_idx = idx
            break
    if header_idx is None:
        raise GateTableMissingError()

    rows: list[GateRow] = []
    for line in lines[header_idx + 1 :]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        if _SEPARATOR.match(stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        gate_id, status = cells[0], cells[1]
        if gate_id.lower() in {"human_gate_id", "---"}:
            continue
        rows.append(
            GateRow(
                human_gate_id=gate_id,
                status=status.strip("`"),
                blocks_hats=cells[2],
                description=cells[3],
            )
        )

    if not rows:
        raise GateTableMissingError("human_gate table has no data rows")
    return rows


def build_gate_summary(content: str) -> GateSummary:
    rows = parse_gate_table(content)
    pending = [r.human_gate_id for r in rows if r.status == "pending"]
    approved = [r.human_gate_id for r in rows if r.status == "approved"]
    return GateSummary(pending=pending, approved=approved)


def _replace_gate_status(content: str, gate_id: str, new_status: str) -> str:
    if new_status not in ALLOWED_GATE_STATUSES:
        raise GateStatusInvalidError()

    rows = parse_gate_table(content)
    if not any(r.human_gate_id == gate_id for r in rows):
        raise GateNotFoundError(gate_id)

    pattern = re.compile(
        rf"^(\|\s*{re.escape(gate_id)}\s*\|\s*)([^|]+)(\|.*)$",
        re.MULTILINE,
    )
    updated, count = pattern.subn(rf"\1{new_status}\3", content, count=1)
    if count != 1:
        raise GateNotFoundError(gate_id)
    return updated


def patch_gate(task_path: Path, gate_id: str, status: str) -> str:
    """Patch task 闸表 status · 返回新正文。"""
    content = task_path.read_text(encoding="utf-8")
    new_content = _replace_gate_status(content, gate_id, status)
    task_path.write_text(new_content, encoding="utf-8")
    return new_content


def sync_gate_summary(session_dir: Path) -> SessionMeta:
    """从 task 重算 gate_summary 并写回 meta。"""
    from api.harness_runtime.session_store.io import load_meta, save_meta

    meta = load_meta(session_dir)
    task_path = session_dir / meta.primary_task_path
    if not task_path.is_file():
        raise FileNotFoundError(f"missing task file: {task_path}")

    summary = build_gate_summary(task_path.read_text(encoding="utf-8"))
    meta.gate_summary = summary
    meta.updated_at = datetime.now(timezone.utc)
    save_meta(session_dir, meta)
    return meta


def patch_gate_and_sync(session_dir: Path, gate_id: str, status: str) -> SessionMeta:
    """Patch task 闸表并同步 meta gate_summary。"""
    from api.harness_runtime.session_store.io import load_meta

    meta = load_meta(session_dir)
    task_path = session_dir / meta.primary_task_path
    patch_gate(task_path, gate_id, status)
    return sync_gate_summary(session_dir)
