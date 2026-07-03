"""Session promote · probe verify · conflict action block/overwrite/merge（S4.2）· graph_delta promote（S5.2）。"""

from __future__ import annotations

import difflib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from api.harness_runtime.adapters import probe_runner
from api.harness_runtime.deliverables import deliverable_dir, write_deliverable
from api.harness_runtime.errors import HarnessRuntimeError
from api.harness_runtime.gate_sync.human_gate import build_gate_summary, patch_gate_and_sync
from api.harness_runtime.session_store.io import REPO_ROOT, load_meta, save_meta
from api.harness_runtime.session_store.schema import SessionMeta, SessionStatus

TargetRepo = Literal["ai-ink-brain-api-python", "ai-ink-brain"]
ConflictAction = Literal["block", "overwrite", "merge"]

HG_PROMOTE = "HG-PROMOTE"
HG_EXEC_AUTH = "HG-EXEC-AUTH"
HG_PROMOTE_OVERWRITE = "HG-PROMOTE-OVERWRITE"
HG_PROMOTE_GRAPH = "HG-PROMOTE-GRAPH"

_MAX_DIFF_BYTES = 5 * 1024 * 1024

_TARGET_CONFIG: dict[str, dict[str, Any]] = {
    "ai-ink-brain-api-python": {
        "tasks_subdir": Path("docs/tasks/active"),
        "graph_subdir": Path("docs/_tech_graph"),
        "default_root": REPO_ROOT,
    },
    "ai-ink-brain": {
        "tasks_subdir": Path("content/tasks/active"),
        "graph_subdir": Path("docs/_tech_graph"),
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


def get_graph_dir(target_repo: str) -> Path:
    cfg = _TARGET_CONFIG[target_repo]
    return get_repo_root(target_repo) / cfg["graph_subdir"]


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


def _is_gate_approved(session_dir: Path, gate_id: str) -> bool:
    meta = load_meta(session_dir)
    return gate_id in meta.gate_summary.approved


def _require_graph_promote_status(meta: SessionMeta) -> None:
    allowed = {
        SessionStatus.DISPATCHED,
        SessionStatus.REVIEWING,
        SessionStatus.DONE,
        SessionStatus.PARTIAL,
    }
    if meta.status not in allowed:
        raise HarnessRuntimeError(
            "SESSION_STATUS_INVALID",
            f"graph promote requires dispatched or later, got {meta.status.value}",
        )


def _append_promotion_header(
    body: str,
    meta: SessionMeta,
    target_repo: str,
    target_branch: str,
    *,
    overwrite_of: str | None = None,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = (
        f"\n\n> **promoted_from_session**: `{meta.session_id}`\n"
        f"> **promoted_at**: `{now}`\n"
        f"> **target_repo**: `{target_repo}` · **target_branch**: `{target_branch}`\n"
    )
    if overwrite_of:
        header += f"> **overwrite_of**: `{overwrite_of}`\n"
    return body.rstrip() + header


def _build_merge_draft(
    source_text: str,
    target_text: str,
    source_label: str = "session draft",
    target_label: str = "target existing",
) -> str:
    source_lines = source_text.splitlines()
    target_lines = target_text.splitlines()
    sm = difflib.SequenceMatcher(None, source_lines, target_lines)
    out: list[str] = [
        "# Merge Draft",
        "",
        f"_Auto-generated merge preview: `{source_label}` ↔ `{target_label}`._",
        "",
    ]
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.extend(source_lines[i1:i2])
        elif tag == "replace":
            out.append(f"<<<<<<< {source_label}")
            out.extend(source_lines[i1:i2])
            out.append("=======")
            out.extend(target_lines[j1:j2])
            out.append(f">>>>>>> {target_label}")
        elif tag == "delete":
            out.append(f"<<<<<<< {source_label}")
            out.extend(source_lines[i1:i2])
            out.append("=======")
            out.append(f">>>>>>> {target_label}")
        elif tag == "insert":
            out.append(f"<<<<<<< {source_label}")
            out.append("=======")
            out.extend(target_lines[j1:j2])
            out.append(f">>>>>>> {target_label}")
    return "\n".join(out) + "\n"


def _build_field_diff(source_text: str, target_text: str) -> dict[str, Any]:
    try:
        src_summary = build_gate_summary(source_text)
        tgt_summary = build_gate_summary(target_text)
    except Exception:
        return {"gate_status_changed": []}
    src_map = {g: "approved" for g in src_summary.approved}
    src_map.update({g: "pending" for g in src_summary.pending})
    tgt_map = {g: "approved" for g in tgt_summary.approved}
    tgt_map.update({g: "pending" for g in tgt_summary.pending})
    changed = []
    for gid in sorted(set(src_map) | set(tgt_map)):
        s = src_map.get(gid)
        t = tgt_map.get(gid)
        if s != t:
            changed.append({"gate_id": gid, "source": s, "target": t})
    return {"gate_status_changed": changed}


def build_diff_summary(
    source_text: str,
    target_text: str,
    target_exists: bool = True,
) -> dict[str, Any]:
    """生成源/目标 task 的行级 + 字段级 diff 摘要。"""
    if len(source_text) > _MAX_DIFF_BYTES or len(target_text) > _MAX_DIFF_BYTES:
        raise HarnessRuntimeError("PROMOTE_DIFF_FAILED", "task file too large for diff")

    source_lines = source_text.splitlines()
    target_lines = target_text.splitlines() if target_exists else []
    sm = difflib.SequenceMatcher(None, source_lines, target_lines)
    added = removed = unchanged = 0
    hunks: list[dict[str, Any]] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            unchanged += i2 - i1
        elif tag == "replace":
            removed += i2 - i1
            added += j2 - j1
            hunks.append({"type": "replace", "source_range": [i1, i2], "target_range": [j1, j2]})
        elif tag == "delete":
            removed += i2 - i1
            hunks.append({"type": "delete", "source_range": [i1, i2]})
        elif tag == "insert":
            added += j2 - j1
            hunks.append({"type": "insert", "target_range": [j1, j2]})

    unified = list(
        difflib.unified_diff(
            source_lines,
            target_lines,
            fromfile="source",
            tofile="target",
            lineterm="",
        )
    )

    return {
        "target_exists": target_exists,
        "has_conflict": target_exists and (added > 0 or removed > 0),
        "line_stats": {
            "source_lines": len(source_lines),
            "target_lines": len(target_lines),
            "added": added,
            "removed": removed,
            "unchanged": unchanged,
        },
        "field_diff": _build_field_diff(source_text, target_text),
        "hunks": hunks[:50],
        "diff_text": "\n".join(unified[:200]),
    }


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
    source_text = source.read_text(encoding="utf-8")
    target_text = target.read_text(encoding="utf-8") if conflict else ""
    try:
        diff_summary = build_diff_summary(source_text, target_text, target_exists=conflict)
    except HarnessRuntimeError:
        raise
    except Exception as exc:
        raise HarnessRuntimeError("PROMOTE_DIFF_FAILED", f"diff failed: {exc}") from exc
    gate_summary = build_gate_summary(source_text).model_dump()
    return {
        "session_id": meta.session_id,
        "source_task_path": str(source.relative_to(session_dir)),
        "source_task_abs": str(source),
        "target_repo": target_repo,
        "target_branch": target_branch,
        "target_task_path": str(target),
        "target_exists": conflict,
        "conflict": conflict,
        "diff_summary": diff_summary,
        "gate_summary": gate_summary,
        "probe_available": probe_runner.probe_available(),
        "verify_hint": "全量 verify 建议本地或 GHA 执行；Vercel 不同步跑 promote 前 verify。",
        "slug": meta.slug,
        "title": meta.title,
    }


def _run_verify(
    session_dir: Path,
    meta: SessionMeta,
    task_path: Path,
    target_repo: str,
) -> tuple[bool, dict[str, Any]]:
    repo_root = get_repo_root(target_repo)
    passed, report = probe_runner.verify_task(task_path, repo_root=repo_root, ci=True)
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
    return passed, report


def _write_merged_deliverable(
    session_dir: Path,
    meta: SessionMeta,
    source_text: str,
    target_text: str,
    target_repo: str,
) -> Path:
    run_id = meta.latest_run_id or f"promote-{meta.session_id[-8:]}"
    out_dir = deliverable_dir(session_dir, run_id)
    slug_safe = meta.slug.replace("-", "_")
    draft_name = f"task_{slug_safe}_merged_v1.md"
    draft_path = out_dir / draft_name
    draft_body = _build_merge_draft(source_text, target_text)
    draft_path.write_text(draft_body, encoding="utf-8")
    write_deliverable(
        session_dir,
        run_id,
        {
            "type": "merge_draft",
            "target_repo": target_repo,
            "draft_path": str(draft_path),
            "draft_name": draft_name,
        },
        filename="merge_draft.json",
    )
    return draft_path


def _promote_common_finish(
    session_dir: Path,
    meta: SessionMeta,
    target: Path,
    target_repo: str,
    target_branch: str,
    report: dict[str, Any],
    store: Any,
) -> dict[str, Any]:
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
                "verify_passed": True,
            },
            node_id="n_promote",
        )

    return {
        "session_id": meta.session_id,
        "status": meta.status.value,
        "target_repo": target_repo,
        "target_branch": target_branch,
        "target_task_path": str(target),
        "verify_passed": True,
        "verify_report": report,
        "gate_summary": meta.gate_summary.model_dump(),
        "message": "promote 完成 · 未 auto-commit · 请在目标仓手动 git commit。",
    }


def execute_promote(
    session_dir: Path,
    meta: SessionMeta,
    *,
    target_repo: str,
    target_branch: str,
    confirm: bool,
    conflict_action: ConflictAction = "block",
    store: Any,
) -> dict[str, Any]:
    if not confirm:
        raise HarnessRuntimeError("PROMOTE_NOT_CONFIRMED", "confirm=true required")

    _require_dispatched(meta)
    preview = build_promote_preview(
        session_dir, meta, target_repo=target_repo, target_branch=target_branch
    )
    diff_summary = preview["diff_summary"]

    source = _source_task_path(session_dir, meta)
    target = Path(preview["target_task_path"])
    source_text = source.read_text(encoding="utf-8")

    if not target.is_file():
        if conflict_action == "merge":
            raise HarnessRuntimeError(
                "PROMOTE_MERGE_BASE_MISSING",
                "merge 须源 task 与目标 task 同时存在",
            )
        # 无冲突：沿用 S4 标准 promote 路径
        if not probe_runner.probe_available():
            raise HarnessRuntimeError(
                "PROBE_UNAVAILABLE",
                "harness-probe CLI 未找到；请设置 HARNESS_PROBE_BIN 或 pip install -e harness-probe",
            )
        patch_gate_and_sync(session_dir, HG_EXEC_AUTH, "approved")
        passed, report = _run_verify(session_dir, meta, source, target_repo)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_append_promotion_header(source_text, meta, target_repo, target_branch), encoding="utf-8")
        return _promote_common_finish(session_dir, meta, target, target_repo, target_branch, report, store)

    # 以下处理目标已存在（conflict）
    if conflict_action == "block":
        err = HarnessRuntimeError(
            "PROMOTE_CONFLICT",
            f"target task already exists: {preview['target_task_path']}",
        )
        err.diff_summary = diff_summary  # type: ignore[attr-defined]
        raise err

    if conflict_action == "overwrite":
        if not _is_gate_approved(session_dir, HG_PROMOTE_OVERWRITE):
            raise HarnessRuntimeError(
                "PROMOTE_OVERWRITE_UNCONFIRMED",
                f"overwrite 须先在 task 中签发 {HG_PROMOTE_OVERWRITE}=approved",
            )
        if not probe_runner.probe_available():
            raise HarnessRuntimeError(
                "PROBE_UNAVAILABLE",
                "harness-probe CLI 未找到；请设置 HARNESS_PROBE_BIN 或 pip install -e harness-probe",
            )
        patch_gate_and_sync(session_dir, HG_EXEC_AUTH, "approved")
        passed, report = _run_verify(session_dir, meta, source, target_repo)
        target.parent.mkdir(parents=True, exist_ok=True)
        overwrite_of = str(target)
        target.write_text(
            _append_promotion_header(
                source_text, meta, target_repo, target_branch, overwrite_of=overwrite_of
            ),
            encoding="utf-8",
        )
        return _promote_common_finish(session_dir, meta, target, target_repo, target_branch, report, store)

    if conflict_action == "merge":
        if not target.is_file() or not source.is_file():
            raise HarnessRuntimeError(
                "PROMOTE_MERGE_BASE_MISSING",
                "merge 须源 task 与目标 task 同时存在",
            )
        target_text = target.read_text(encoding="utf-8")
        draft_path = _write_merged_deliverable(
            session_dir, meta, source_text, target_text, target_repo
        )
        if not _is_gate_approved(session_dir, HG_PROMOTE_OVERWRITE):
            err = HarnessRuntimeError(
                "PROMOTE_MERGE_BLOCKED",
                f"merge 须先在 task 中签发 {HG_PROMOTE_OVERWRITE}=approved",
            )
            err.merge_draft_path = str(draft_path)  # type: ignore[attr-defined]
            raise err
        if not probe_runner.probe_available():
            raise HarnessRuntimeError(
                "PROBE_UNAVAILABLE",
                "harness-probe CLI 未找到；请设置 HARNESS_PROBE_BIN 或 pip install -e harness-probe",
            )
        patch_gate_and_sync(session_dir, HG_EXEC_AUTH, "approved")
        passed, report = _run_verify(session_dir, meta, draft_path, target_repo)
        target.parent.mkdir(parents=True, exist_ok=True)
        merged_body = draft_path.read_text(encoding="utf-8")
        target.write_text(
            _append_promotion_header(merged_body, meta, target_repo, target_branch),
            encoding="utf-8",
        )
        return _promote_common_finish(session_dir, meta, target, target_repo, target_branch, report, store)

    raise HarnessRuntimeError("PROMOTE_ACTION_INVALID", f"unknown conflict_action: {conflict_action}")


def _graph_delta_dir(session_dir: Path) -> Path:
    return session_dir / "deliverables" / "graph_delta"


def _graph_target_path(source: Path, graph_delta_dir: Path, target_repo: str) -> Path:
    rel = source.relative_to(graph_delta_dir)
    return get_graph_dir(target_repo) / rel


def build_graph_promote_preview(
    session_dir: Path,
    meta: SessionMeta,
    *,
    target_repo: str,
    target_branch: str,
) -> dict[str, Any]:
    """返回 session graph_delta 复制到目标仓 _tech_graph/ 的预览。"""
    _require_graph_promote_status(meta)
    if target_repo not in _TARGET_CONFIG:
        raise HarnessRuntimeError("INVALID_TARGET_REPO", f"unknown target_repo: {target_repo}")

    graph_dir = _graph_delta_dir(session_dir)
    if not graph_dir.is_dir():
        raise HarnessRuntimeError("GRAPH_DELTA_EMPTY", "session has no graph_delta directory")

    source_files = sorted(f for f in graph_dir.rglob("*") if f.is_file())
    if not source_files:
        raise HarnessRuntimeError("GRAPH_DELTA_EMPTY", "graph_delta directory is empty")

    target_root = get_graph_dir(target_repo)
    files: list[dict[str, Any]] = []
    for src in source_files:
        rel = src.relative_to(graph_dir)
        target = target_root / rel
        target_exists = target.is_file()
        source_text = src.read_text(encoding="utf-8")
        target_text = target.read_text(encoding="utf-8") if target_exists else ""
        try:
            diff_summary = build_diff_summary(source_text, target_text, target_exists=target_exists)
        except HarnessRuntimeError:
            raise
        except Exception as exc:
            raise HarnessRuntimeError("PROMOTE_DIFF_FAILED", f"diff failed for {rel}: {exc}") from exc

        files.append(
            {
                "source_path": str(src.relative_to(session_dir)),
                "source_abs": str(src),
                "target_path": str(target),
                "target_exists": target_exists,
                "diff_summary": diff_summary,
            }
        )

    conflict_count = sum(1 for f in files if f["target_exists"])
    return {
        "session_id": meta.session_id,
        "source_graph_dir": str(graph_dir.relative_to(session_dir)),
        "target_repo": target_repo,
        "target_branch": target_branch,
        "target_graph_dir": str(_TARGET_CONFIG[target_repo]["graph_subdir"]),
        "files": files,
        "conflict_count": conflict_count,
        "empty": False,
        "gate_summary": meta.gate_summary.model_dump(),
        "slug": meta.slug,
        "title": meta.title,
    }


def execute_graph_promote(
    session_dir: Path,
    meta: SessionMeta,
    *,
    target_repo: str,
    target_branch: str,
    confirm: bool,
    conflict_action: ConflictAction = "block",
    store: Any,
) -> dict[str, Any]:
    """将 session graph_delta 复制到目标仓 _tech_graph/。"""
    if not confirm:
        raise HarnessRuntimeError("PROMOTE_NOT_CONFIRMED", "confirm=true required")

    if not _is_gate_approved(session_dir, HG_PROMOTE_GRAPH):
        raise HarnessRuntimeError(
            "GRAPH_PROMOTE_GATE_PENDING",
            f"graph promote requires {HG_PROMOTE_GRAPH}=approved",
        )

    preview = build_graph_promote_preview(
        session_dir, meta, target_repo=target_repo, target_branch=target_branch
    )
    files = preview["files"]

    if conflict_action == "block":
        conflicts = [f for f in files if f["target_exists"]]
        if conflicts:
            err = HarnessRuntimeError(
                "GRAPH_PROMOTE_CONFLICT",
                f"{len(conflicts)} graph file(s) already exist in target repo",
            )
            err.diff_summary = {"conflicts": conflicts}  # type: ignore[attr-defined]
            raise err

    repo_root = get_repo_root(target_repo)
    copied: list[dict[str, Any]] = []
    try:
        for f in files:
            target = Path(f["target_path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            source = Path(f["source_abs"])
            source_text = source.read_text(encoding="utf-8")

            if conflict_action == "merge" and f["target_exists"]:
                target_text = target.read_text(encoding="utf-8")
                merged_body = _build_merge_draft(
                    source_text,
                    target_text,
                    source_label="session graph delta",
                    target_label="target existing",
                )
                target.write_text(merged_body, encoding="utf-8")
            else:
                target.write_text(source_text, encoding="utf-8")

            copied.append(
                {
                    "source_path": f["source_path"],
                    "target_path": f["target_path"],
                    "target_repo_relative": str(target.relative_to(repo_root)),
                    "conflict": f["target_exists"],
                }
            )
    except Exception as exc:
        raise HarnessRuntimeError("GRAPH_PROMOTE_COPY_FAILED", f"copy failed: {exc}") from exc

    patch_gate_and_sync(session_dir, HG_PROMOTE_GRAPH, "approved")

    meta = load_meta(session_dir)
    meta.updated_at = datetime.now(timezone.utc)
    save_meta(session_dir, meta)

    if meta.latest_run_id:
        store.append_event(
            meta.latest_run_id,
            "orchestrator",
            "session.graph_promoted",
            payload={
                "session_id": meta.session_id,
                "target_repo": target_repo,
                "target_branch": target_branch,
                "copied_files": copied,
                "conflict_action": conflict_action,
            },
            node_id="n_graph_promote",
        )

    return {
        "session_id": meta.session_id,
        "status": meta.status.value,
        "target_repo": target_repo,
        "target_branch": target_branch,
        "conflict_action": conflict_action,
        "copied_files": copied,
        "gate_summary": meta.gate_summary.model_dump(),
        "message": "graph_delta promote 完成 · 未 auto-commit · 请在目标仓手动 git commit。",
    }
