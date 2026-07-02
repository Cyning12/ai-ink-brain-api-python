"""Session promote · probe verify · 业务仓 task 复制（S4 · B4）。"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from api.harness_runtime.adapters import probe_runner
from api.harness_runtime.deliverables import write_deliverable
from api.harness_runtime.errors import HarnessRuntimeError
from api.harness_runtime.gate_sync.human_gate import build_gate_summary, patch_gate_and_sync
from api.harness_runtime.session_store.io import REPO_ROOT, load_meta, save_meta
from api.harness_runtime.session_store.schema import SessionMeta, SessionStatus

TargetRepo = Literal["ai-ink-brain-api-python", "ai-ink-brain"]

HG_PROMOTE = "HG-PROMOTE"
HG_EXEC_AUTH = "HG-EXEC-AUTH"

_TARGET_CONFIG: dict[str, dict[str, Any]] = {
    "ai-ink-brain-api-python": {
        "tasks_subdir": Path("docs/tasks/active"),
        "default_root": REPO_ROOT,
    },
    "ai-ink-brain": {
        "tasks_subdir": Path("content/tasks/active"),
        "default_root": REPO_ROOT.parent / "ai-ink-brain",
    },
}

_repo_root_overrides: dict[str, Path] = {}


def set_repo_root_override(target_repo: str, root: Path) -> None:
    """测试注入目标仓根路径。"""
    _repo_root_overrides[target_repo] = root


def clear_repo_root_overrides() -> None:
    _repo_root_overrides.clear()


def get_repo_root(target_repo: str) -> Path:
    if target_repo in _repo_root_overrides:
        return _repo_root_overrides[target_repo]
    cfg = _TARGET_CONFIG.get(target_repo)
    if not cfg:
        raise HarnessRuntimeError("PROMOTE_REPO_INVALID", f"unknown target_repo: {target_repo}")
    return Path(cfg["default_root"])


def get_tasks_dir(target_repo: str) -> Path:
    cfg = _TARGET_CONFIG[target_repo]
    return get_repo_root(target_repo) / cfg["tasks_subdir"]


def _require_dispatched(meta: SessionMeta) -> None:
    if meta.status != SessionStatus.DISPATCHED:
        raise HarnessRuntimeError(
            "SESSION_STATUS_INVALID",
            f"promote requires dispatched, got {meta.status.value}",
        )


def _source_task_path(session_dir: Path, meta: SessionMeta) -> Path:
    path = session_dir / meta.primary_task_path
    if not path.is_file():
        raise HarnessRuntimeError("TASK_NOT_FOUND", f"missing session task: {path.name}")
    return path


def _target_task_path(session_dir: Path, meta: SessionMeta, target_repo: str) -> Path:
    source = _source_task_path(session_dir, meta)
    return get_tasks_dir(target_repo) / source.name


def build_promote_preview(
    session_dir: Path,
    meta: SessionMeta,
    *,
    target_repo: str,
    target_branch: str,
) -> dict[str, Any]:
    _require_dispatched(meta)
    source = _source_task_path(session_dir, meta)
    target = _target_task_path(session_dir, meta, target_repo)
    conflict = target.is_file()
    task_body = source.read_text(encoding="utf-8")
    gate_summary = build_gate_summary(task_body).model_dump()
    return {
        "session_id": meta.session_id,
        "source_task_path": str(source.relative_to(session_dir)),
        "source_task_abs": str(source),
        "target_repo": target_repo,
        "target_branch": target_branch,
        "target_task_path": str(target),
        "target_exists": conflict,
        "conflict": conflict,
        "gate_summary": gate_summary,
        "probe_available": probe_runner.probe_available(),
        "verify_hint": "全量 verify 建议本地或 GHA 执行；Vercel 不同步跑 promote 前 verify。",
        "slug": meta.slug,
        "title": meta.title,
    }


def execute_promote(
    session_dir: Path,
    meta: SessionMeta,
    *,
    target_repo: str,
    target_branch: str,
    confirm: bool,
    store: Any,
) -> dict[str, Any]:
    if not confirm:
        raise HarnessRuntimeError("PROMOTE_NOT_CONFIRMED", "confirm=true required")

    _require_dispatched(meta)
    preview = build_promote_preview(
        session_dir, meta, target_repo=target_repo, target_branch=target_branch
    )
    if preview["conflict"]:
        raise HarnessRuntimeError(
            "PROMOTE_CONFLICT",
            f"target task already exists: {preview['target_task_path']}",
        )

    if not probe_runner.probe_available():
        raise HarnessRuntimeError(
            "PROBE_UNAVAILABLE",
            "harness-probe CLI 未找到；请设置 HARNESS_PROBE_BIN 或 pip install -e harness-probe",
        )

    # 二次确认即 HG-EXEC-AUTH 授权；须在 verify 前写回 task
    patch_gate_and_sync(session_dir, HG_EXEC_AUTH, "approved")

    source = _source_task_path(session_dir, meta)
    repo_root = get_repo_root(target_repo)
    passed, report = probe_runner.verify_task(source, repo_root=repo_root, ci=True)
    run_id = meta.latest_run_id or f"promote-{meta.session_id[-8:]}"
    write_deliverable(
        session_dir,
        run_id,
        {"type": "verify_report", "passed": passed, "report": report, "target_repo": target_repo},
        filename="verify_report.json",
    )

    if not passed:
        err = HarnessRuntimeError(
            "VERIFY_FAILED",
            "harness-probe verify failed"
            + (f": {'; '.join(str(x) for x in report.get('blocking_errors', []))}" if report.get("blocking_errors") else ""),
        )
        err.verify_report = report  # type: ignore[attr-defined]
        raise err

    target = Path(preview["target_task_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = source.read_text(encoding="utf-8")
    promoted_header = (
        f"\n\n> **promoted_from_session**: `{meta.session_id}`\n"
        f"> **promoted_at**: `{now}`\n"
        f"> **target_repo**: `{target_repo}` · **target_branch**: `{target_branch}`\n"
    )
    target.write_text(body.rstrip() + promoted_header, encoding="utf-8")

    patch_gate_and_sync(session_dir, HG_PROMOTE, "approved")

    meta = load_meta(session_dir)
    meta.updated_at = datetime.now(timezone.utc)
    save_meta(session_dir, meta)

    if meta.latest_run_id:
        store.append_event(
            meta.latest_run_id,
            "orchestrator",
            "session.promoted",
            payload={
                "session_id": meta.session_id,
                "target_repo": target_repo,
                "target_branch": target_branch,
                "target_task_path": str(target),
                "verify_passed": passed,
            },
            node_id="n_promote",
        )

    return {
        "session_id": meta.session_id,
        "status": meta.status.value,
        "target_repo": target_repo,
        "target_branch": target_branch,
        "target_task_path": str(target),
        "verify_passed": passed,
        "verify_report": report,
        "gate_summary": meta.gate_summary.model_dump(),
        "message": "promote 完成 · 未 auto-commit · 请在目标仓手动 git commit。",
    }
