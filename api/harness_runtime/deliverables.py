"""Session deliverables 落盘（S3 · Inform 真值补充）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def deliverable_dir(session_dir: Path, run_id: str) -> Path:
    path = session_dir / "deliverables" / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_deliverable(
    session_dir: Path,
    run_id: str,
    payload: dict[str, Any],
    *,
    filename: str = "result.json",
) -> Path:
    """写入 deliverables/{run_id}/result.json · 返回路径。"""
    out_dir = deliverable_dir(session_dir, run_id)
    out_path = out_dir / filename
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def write_invoke_snapshot(
    session_dir: Path,
    run_id: str,
    payload: dict[str, Any],
) -> Path:
    """可选 invokes 镜像摘要。"""
    invokes_dir = session_dir / "invokes"
    invokes_dir.mkdir(parents=True, exist_ok=True)
    out_path = invokes_dir / f"{run_id}_dispatch.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def list_deliverables(session_dir: Path) -> list[dict[str, Any]]:
    """扫描 deliverables/{run_id}/ · 供 Session GET 与 UI 只读列表。"""
    base = session_dir / "deliverables"
    if not base.is_dir():
        return []

    items: list[dict[str, Any]] = []
    for run_dir in sorted(base.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not run_dir.is_dir():
            continue
        run_id = run_dir.name
        rel_dir = f"deliverables/{run_id}"
        entry: dict[str, Any] = {
            "run_id": run_id,
            "path": rel_dir,
            "files": [],
        }
        for file_path in sorted(run_dir.glob("*.json")):
            file_entry: dict[str, Any] = {
                "name": file_path.name,
                "path": f"{rel_dir}/{file_path.name}",
            }
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    file_entry["type"] = data.get("type")
                    file_entry["route"] = data.get("route")
            except json.JSONDecodeError:
                pass
            entry["files"].append(file_entry)
        if entry["files"]:
            primary = entry["files"][0]
            entry["type"] = primary.get("type")
            entry["route"] = primary.get("route")
        items.append(entry)
    return items
