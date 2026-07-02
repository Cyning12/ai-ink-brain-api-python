"""gate_sync human_gate 单测。"""

from __future__ import annotations

from pathlib import Path

import pytest

from api.harness_runtime.errors import (
    GateNotFoundError,
    GateStatusInvalidError,
    GateTableMissingError,
)
from api.harness_runtime.gate_sync.human_gate import (
    build_gate_summary,
    parse_gate_table,
    patch_gate,
    patch_gate_and_sync,
    render_session_task_template,
)
from api.harness_runtime.session_store.io import create_session


def test_parse_gate_table_from_template() -> None:
    content = render_session_task_template(slug="demo", title="Demo")
    rows = parse_gate_table(content)
    assert any(r.human_gate_id == "HG-SESSION-PLAN" and r.status == "pending" for r in rows)


def test_fp_gate_table_missing() -> None:
    with pytest.raises(GateTableMissingError) as exc:
        parse_gate_table("# no gate table\n")
    assert exc.value.code == "GATE_TABLE_MISSING"


def test_s0_patch_gate(sessions_tmp: Path) -> None:
    session_dir, meta = create_session(
        slug="gate-patch",
        title="Gate Patch",
        sessions_root=sessions_tmp,
        session_id="sess_20260702_gp000001",
    )
    task_path = session_dir / meta.primary_task_path
    assert "HG-SESSION-PLAN" in meta.gate_summary.pending

    updated = patch_gate_and_sync(session_dir, "HG-SESSION-PLAN", "approved")
    assert "HG-SESSION-PLAN" in updated.gate_summary.approved
    assert "HG-SESSION-PLAN" not in updated.gate_summary.pending

    body = task_path.read_text(encoding="utf-8")
    rows = parse_gate_table(body)
    plan = next(r for r in rows if r.human_gate_id == "HG-SESSION-PLAN")
    assert plan.status == "approved"


def test_fp_gate_status_invalid(sessions_tmp: Path) -> None:
    session_dir, meta = create_session(
        slug="bad-status",
        title="Bad Status",
        sessions_root=sessions_tmp,
        session_id="sess_20260702_bs000001",
    )
    task_path = session_dir / meta.primary_task_path
    with pytest.raises(GateStatusInvalidError) as exc:
        patch_gate(task_path, "HG-SESSION-PLAN", "rejected")
    assert exc.value.code == "GATE_STATUS_INVALID"


def test_fp_gate_not_found(sessions_tmp: Path) -> None:
    session_dir, meta = create_session(
        slug="missing-gate",
        title="Missing Gate",
        sessions_root=sessions_tmp,
        session_id="sess_20260702_mg000001",
    )
    task_path = session_dir / meta.primary_task_path
    with pytest.raises(GateNotFoundError):
        patch_gate(task_path, "HG-NOT-REAL", "approved")


def test_build_gate_summary() -> None:
    content = render_session_task_template(slug="x", title="X")
    summary = build_gate_summary(content)
    assert summary.pending
    assert not summary.approved
