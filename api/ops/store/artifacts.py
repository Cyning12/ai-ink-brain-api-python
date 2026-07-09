"""Ops Chat run artifacts 仓储层（P1-1）。"""

from __future__ import annotations

from typing import Any


class ArtifactStoreError(RuntimeError):
    """Artifact 写入失败时的自说明异常。"""


def save_artifact(
    run_id: str,
    kind: str,
    payload: dict[str, Any],
    store: Any | None = None,
    max_retries: int = 3,
) -> dict[str, Any]:
    """幂等写入 ops_run_artifacts；按 (run_id, kind) 去重。

    - 未提供 store 时，使用全局 supabase_client() 构造 OpsRunStore。
    - 重试 max_retries + 1 次后仍失败则抛出 ArtifactStoreError。
    """
    from api.ops.store.runs import OpsRunStore
    from api.rag_env import supabase_client

    target = store if store is not None else OpsRunStore(supabase_client())
    normalized = dict(payload)
    last_exc: Exception | None = None

    for _attempt in range(max_retries + 1):
        try:
            return target.save_artifact(run_id, kind, normalized)
        except Exception as exc:
            last_exc = exc

    raise ArtifactStoreError(
        f"Failed to save artifact run_id={run_id} kind={kind} "
        f"after {max_retries + 1} attempts: {last_exc}"
    )


def save_artifact_with_failure_event(
    run_id: str,
    kind: str,
    payload: dict[str, Any],
    store: Any | None = None,
    max_retries: int = 3,
) -> dict[str, Any] | None:
    """保存 artifact；写入失败时记录 `artifact.write_failed` 事件并吞掉异常。

    返回值：成功返回写入行；失败返回 None。
    """
    from api.ops.events_schema import SCHEMA_VERSION
    from api.ops.store.runs import append_event

    try:
        return save_artifact(run_id, kind, payload, store=store, max_retries=max_retries)
    except ArtifactStoreError as exc:
        append_event(
            run_id,
            "artifact.write_failed",
            {
                "kind": kind,
                "error": str(exc),
                "schema_version": SCHEMA_VERSION,
            },
            store=store,
        )
        return None
