"""Graph snapshot 持久化与 sync_run 关联。"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from api.rag_env import pick_supabase_service_key, pick_supabase_url, supabase_execute_with_retry
from supabase import create_client

from .module_matrix import ModuleMatrixService
from .validator import GraphValidationError, validate_graph_json


def _client() -> Any:
    url = pick_supabase_url()
    key = pick_supabase_service_key()
    if not url or not key:
        raise RuntimeError(
            "缺少 Supabase 配置：NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"
        )
    return create_client(url, key)


def _default_graph_json_path() -> Path:
    raw = (os.getenv("OPS_GRAPH_JSON_PATH") or "").strip()
    if raw:
        return Path(raw)
    # graph 源：GitHub Cyning12/kimi-code @ cyning/meta · checkout 落盘 workspace/kimi-code-meta/
    # 映射真值：Projects/docs/harness/guides/POINTER_kimi_code_meta_git_mapping_v1_zh.md
    return Path("workspace/kimi-code-meta/docs/_tech_graph/graph.json")


def _default_manifest_json_path() -> Path | None:
    raw = (os.getenv("OPS_MANIFEST_JSON_PATH") or "").strip()
    if raw:
        return Path(raw)
    default = Path("workspace/kimi-code-meta/.cyning-harness/manifest.json")
    return default if default.exists() else None


def _default_source_branch() -> str:
    return (os.getenv("OPS_GRAPH_SOURCE_BRANCH") or "").strip() or "cyning/meta"


@dataclass(frozen=True)
class GraphIngestResult:
    snapshot_id: str | None
    status: str
    meta: dict[str, Any] | None
    error_message: str | None = None


class OpsGraphStore:
    """ops_graph_snapshots / ops_sync_run_artifacts 读写。"""

    def __init__(self, repo_id: str, client: Any | None = None) -> None:
        self.repo_id = repo_id
        self._client = client

    def _sb(self) -> Any:
        return self._client or _client()

    def write_snapshot(
        self,
        payload: dict[str, Any],
        *,
        source_branch: str,
        source_commit: str | None = None,
        manifest_version: str | None = None,
    ) -> str:
        row = {
            "repo_id": self.repo_id,
            "source_branch": source_branch,
            "source_commit": source_commit,
            "manifest_version": manifest_version,
            "payload": payload,
        }

        def _once() -> str:
            sb = self._sb()
            res = sb.table("ops_graph_snapshots").insert(row).execute()
            data = res.data if isinstance(res.data, list) else []
            if data and isinstance(data[0], dict) and data[0].get("id"):
                return str(data[0]["id"])
            raise RuntimeError("ops_graph_snapshots insert 未返回 id")

        return supabase_execute_with_retry(_once)

    def link_artifact(
        self,
        sync_run_id: str,
        graph_snapshot_id: str | None,
        scan_snapshot_id: str | None = None,
    ) -> None:
        row = {
            "sync_run_id": sync_run_id,
            "graph_snapshot_id": graph_snapshot_id,
            "scan_snapshot_id": scan_snapshot_id,
        }

        def _once() -> None:
            sb = self._sb()
            sb.table("ops_sync_run_artifacts").insert(row).execute()

        supabase_execute_with_retry(_once)

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        def _once() -> dict[str, Any] | None:
            sb = self._sb()
            res = (
                sb.table("ops_graph_snapshots")
                .select("*")
                .eq("repo_id", self.repo_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return rows[0] if rows and isinstance(rows[0], dict) else None

        return supabase_execute_with_retry(_once)

    def get_open_issues_for_module(self, module_id: str) -> list[dict[str, Any]]:
        """按 module_id 标签匹配获取 open issues（简单实现）。"""
        def _once() -> list[dict[str, Any]]:
            sb = self._sb()
            res = (
                sb.table("ops_issues")
                .select("number, title, state, labels, created_at, updated_at")
                .eq("repo_id", self.repo_id)
                .eq("state", "open")
                .contains("labels", [f"module:{module_id}"])
                .order("updated_at", desc=True)
                .limit(10)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return [r for r in rows if isinstance(r, dict)]

        return supabase_execute_with_retry(_once)

    def get_module_matrix(self, payload: dict[str, Any], *, state: str = "open") -> list[dict[str, Any]]:
        """使用共享矩阵服务构建 module×Issue 矩阵。"""
        service = ModuleMatrixService(repo_id=self.repo_id, client=self._sb())
        return service.build_matrix(payload, state=state)

    def get_module_edges(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        """提取 module 级 depends_on 边。"""
        service = ModuleMatrixService(repo_id=self.repo_id, client=self._sb())
        return service.get_module_edges(payload, relation="depends_on")


def ingest_graph_after_github_sync(
    repo_id: str,
    sync_run_id: str,
    *,
    graph_json_path: Path | None = None,
    manifest_json_path: Path | None = None,
    source_branch: str | None = None,
    source_commit: str | None = None,
    client: Any | None = None,
) -> GraphIngestResult:
    """sync_run 成功后调用：校验 graph.json 并写入 snapshot + artifact。

    graph ingest 失败 → partial（Issue/PR/scan 仍保留）。
    """
    path = graph_json_path or _default_graph_json_path()
    if not path.exists():
        return GraphIngestResult(
            snapshot_id=None,
            status="skipped",
            meta=None,
            error_message=f"graph.json not found: {path}",
        )

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return GraphIngestResult(
            snapshot_id=None,
            status="failed",
            meta=None,
            error_message=f"graph.json JSON decode error: {exc}",
        )

    if not isinstance(raw, dict):
        return GraphIngestResult(
            snapshot_id=None,
            status="failed",
            meta=None,
            error_message="graph.json root must be object",
        )

    try:
        meta = validate_graph_json(raw)
    except GraphValidationError as exc:
        return GraphIngestResult(
            snapshot_id=None,
            status="failed",
            meta=None,
            error_message=f"graph.json validation error: {exc.message}",
        )

    # manifest_version
    manifest_version: str | None = None
    mpath = manifest_json_path or _default_manifest_json_path()
    if mpath and mpath.exists():
        try:
            mdata = json.loads(mpath.read_text(encoding="utf-8"))
            if isinstance(mdata, dict):
                manifest_version = mdata.get("version")
        except (json.JSONDecodeError, OSError):
            pass

    branch = source_branch or _default_source_branch()

    store = OpsGraphStore(repo_id=repo_id, client=client)
    snapshot_id = store.write_snapshot(
        raw,
        source_branch=branch,
        source_commit=source_commit,
        manifest_version=manifest_version,
    )
    store.link_artifact(sync_run_id, snapshot_id)

    return GraphIngestResult(
        snapshot_id=snapshot_id,
        status="success",
        meta=meta,
        error_message=None,
    )
