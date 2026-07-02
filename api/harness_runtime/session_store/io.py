"""Session 目录 I/O。"""

from __future__ import annotations

import base64
import secrets
import shutil
from datetime import datetime, timezone
from pathlib import Path

from api.harness_runtime.errors import SessionIdMismatchError
from api.harness_runtime.gate_sync.human_gate import build_gate_summary, render_session_task_template
from api.harness_runtime.session_store.schema import (
    META_FILENAME,
    SessionMeta,
    SessionStatus,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SESSIONS_ROOT = REPO_ROOT / "docs" / "harness" / "sessions"


def default_sessions_root() -> Path:
    return DEFAULT_SESSIONS_ROOT


def generate_session_id(*, now: datetime | None = None) -> str:
    """生成 sess_{YYYYMMDD}_{base32_8}。"""
    ts = now or datetime.now(timezone.utc)
    date_part = ts.strftime("%Y%m%d")
    token = base64.b32encode(secrets.token_bytes(5)).decode("ascii").rstrip("=").lower()[:8]
    return f"sess_{date_part}_{token}"


def task_filename_for_slug(slug: str) -> str:
    safe = slug.replace("-", "_")
    return f"task_{safe}_v1.md"


def create_session(
    *,
    slug: str,
    title: str,
    sessions_root: Path | None = None,
    session_id: str | None = None,
    created_by: str = "maintainer",
    now: datetime | None = None,
) -> tuple[Path, SessionMeta]:
    """创建 session 目录 · task 草稿 · meta（原子：失败则清理目录）。"""
    root = sessions_root or default_sessions_root()
    root.mkdir(parents=True, exist_ok=True)

    ts = now or datetime.now(timezone.utc)
    sid = session_id or generate_session_id(now=ts)
    session_dir = root / sid
    if session_dir.exists():
        raise FileExistsError(f"session directory already exists: {session_dir}")

    task_name = task_filename_for_slug(slug)
    try:
        session_dir.mkdir(parents=True)
        (session_dir / "invokes").mkdir()
        (session_dir / "deliverables").mkdir()

        task_path = session_dir / task_name
        task_path.write_text(render_session_task_template(slug=slug, title=title), encoding="utf-8")

        gate_summary = build_gate_summary(task_path.read_text(encoding="utf-8"))
        meta = SessionMeta(
            schema_version="1.0",
            session_id=sid,
            slug=slug,
            title=title,
            status=SessionStatus.PLANNING,
            created_at=ts,
            updated_at=ts,
            created_by=created_by,
            primary_task_path=task_name,
            gate_summary=gate_summary,
        )
        (session_dir / META_FILENAME).write_text(meta.dump_yaml(), encoding="utf-8")
    except Exception:
        shutil.rmtree(session_dir, ignore_errors=True)
        raise

    return session_dir, meta


def load_meta(session_dir: Path) -> SessionMeta:
    """加载并校验 meta · session_id 与目录名一致。"""
    meta_path = session_dir / META_FILENAME
    if not meta_path.is_file():
        raise FileNotFoundError(f"missing {META_FILENAME} under {session_dir}")

    meta = SessionMeta.from_yaml_text(meta_path.read_text(encoding="utf-8"))
    if meta.session_id != session_dir.name:
        raise SessionIdMismatchError(
            f"directory {session_dir.name!r} != meta.session_id {meta.session_id!r}"
        )
    return meta


def save_meta(session_dir: Path, meta: SessionMeta) -> None:
    """写入 meta · 校验目录名一致。"""
    if meta.session_id != session_dir.name:
        raise SessionIdMismatchError(
            f"directory {session_dir.name!r} != meta.session_id {meta.session_id!r}"
        )
    meta_path = session_dir / META_FILENAME
    meta_path.write_text(meta.dump_yaml(), encoding="utf-8")


def transition_status(session_dir: Path, new_status: SessionStatus) -> SessionMeta:
    """状态 transition · 非法枚举由 Pydantic 拒绝。"""
    meta = load_meta(session_dir)
    meta.status = new_status
    meta.updated_at = datetime.now(timezone.utc)
    save_meta(session_dir, meta)
    return meta
