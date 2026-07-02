"""session_store I/O 与 schema 单测。"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from api.harness_runtime.errors import (
    SessionIdMismatchError,
    SessionSchemaUnsupportedError,
    SessionStatusInvalidError,
)
from api.harness_runtime.session_store.io import create_session, load_meta, save_meta, transition_status
from api.harness_runtime.session_store.schema import META_FILENAME, SessionMeta, SessionStatus


def test_fp_session_schema_unsupported_missing_version() -> None:
    with pytest.raises(SessionSchemaUnsupportedError) as exc:
        SessionMeta.from_yaml_text("slug: foo\n")
    assert exc.value.code == "SESSION_SCHEMA_UNSUPPORTED"


def test_fp_session_schema_unsupported_bad_version() -> None:
    text = """
schema_version: "9.9"
session_id: sess_test
slug: test
title: t
status: planning
created_at: "2026-07-02T00:00:00Z"
updated_at: "2026-07-02T00:00:00Z"
primary_task_path: task_test_v1.md
"""
    with pytest.raises(SessionSchemaUnsupportedError):
        SessionMeta.from_yaml_text(text)


def test_s0_create_session(sessions_tmp: Path) -> None:
    session_dir, meta = create_session(
        slug="ops-session-demo",
        title="Demo Session",
        sessions_root=sessions_tmp,
        session_id="sess_20260702_test0001",
        now=datetime(2026, 7, 2, tzinfo=timezone.utc),
    )
    assert session_dir.is_dir()
    assert (session_dir / META_FILENAME).is_file()
    assert (session_dir / "task_ops_session_demo_v1.md").is_file()
    assert (session_dir / "invokes").is_dir()
    assert (session_dir / "deliverables").is_dir()
    assert meta.session_id == session_dir.name == "sess_20260702_test0001"
    assert meta.status == SessionStatus.PLANNING
    assert "HG-SESSION-PLAN" in meta.gate_summary.pending


def test_fp_session_id_mismatch(sessions_tmp: Path) -> None:
    session_dir, meta = create_session(
        slug="mismatch",
        title="Mismatch",
        sessions_root=sessions_tmp,
        session_id="sess_20260702_mm000001",
    )
    meta.session_id = "sess_other"
    with pytest.raises(SessionIdMismatchError) as exc:
        save_meta(session_dir, meta)
    assert exc.value.code == "SESSION_ID_MISMATCH"

    bad_dir = sessions_tmp / "wrong_dir"
    bad_dir.mkdir()
    (bad_dir / META_FILENAME).write_text(
        meta.model_copy(update={"session_id": "sess_20260702_mm000001"}).dump_yaml(),
        encoding="utf-8",
    )
    with pytest.raises(SessionIdMismatchError):
        load_meta(bad_dir)


def test_fp_session_status_invalid() -> None:
    text = """
schema_version: "1.0"
session_id: sess_x
slug: x
title: x
status: not_a_real_status
created_at: "2026-07-02T00:00:00Z"
updated_at: "2026-07-02T00:00:00Z"
primary_task_path: task_x_v1.md
"""
    with pytest.raises(SessionStatusInvalidError) as exc:
        SessionMeta.from_yaml_text(text)
    assert exc.value.code == "SESSION_STATUS_INVALID"


def test_transition_status(sessions_tmp: Path) -> None:
    session_dir, _ = create_session(
        slug="transition",
        title="Transition",
        sessions_root=sessions_tmp,
        session_id="sess_20260702_tr000001",
    )
    meta = transition_status(session_dir, SessionStatus.AWAITING_AUTH)
    assert meta.status == SessionStatus.AWAITING_AUTH
    reloaded = load_meta(session_dir)
    assert reloaded.status == SessionStatus.AWAITING_AUTH


def test_fp_session_io_partial_rolls_back(sessions_tmp: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """写 task 后 meta 失败须清理目录（F6）。"""
    real_write_text = Path.write_text

    def selective_write(self, data, encoding=None, errors=None):  # type: ignore[no-untyped-def]
        if self.name == META_FILENAME:
            raise OSError("simulated meta write failure")
        return real_write_text(self, data, encoding=encoding, errors=errors)

    monkeypatch.setattr(Path, "write_text", selective_write)

    sid = "sess_20260702_rb000001"
    with pytest.raises(OSError):
        create_session(
            slug="rollback",
            title="Rollback",
            sessions_root=sessions_tmp,
            session_id=sid,
        )
    assert not (sessions_tmp / sid).exists()


def test_load_meta_file_not_found(sessions_tmp: Path) -> None:
    d = sessions_tmp / "empty"
    d.mkdir()
    with pytest.raises(FileNotFoundError):
        load_meta(d)
