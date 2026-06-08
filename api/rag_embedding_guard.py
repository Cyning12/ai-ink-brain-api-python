"""RAG Embedding 模型一致性守卫：防止「换模型但未全量 re-sync / env 未对齐」导致 silent 检索空命中。"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal

from .rag_env import expected_embedding_dim, siliconflow_embedding_model

DEFAULT_SILICONFLOW_EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
EMBEDDING_MISMATCH_ERROR_CODE = "RAG_EMBEDDING_MODEL_MISMATCH"

_cache_lock = threading.Lock()
_cached_alignment: EmbeddingAlignment | None = None


@dataclass(frozen=True)
class EmbeddingAlignment:
    ok: bool
    runtime_model: str
    runtime_dim: int
    stored_models: tuple[str, ...]
    stored_dims: tuple[int, ...]
    message: str | None = None
    error_code: str | None = None
    legacy_unstamped: bool = False


def embedding_mismatch_mode() -> Literal["block", "warn", "off"]:
    raw = (os.getenv("RAG_EMBEDDING_MISMATCH_MODE") or "block").strip().lower()
    if raw in ("off", "none", "0", "false", "no"):
        return "off"
    if raw in ("warn", "warning"):
        return "warn"
    return "block"


def build_embedding_metadata_stamp() -> dict[str, Any]:
    """入库 metadata 附加字段：记录写入时 embedding 模型与维度。"""
    return {
        "embedding_model": siliconflow_embedding_model(),
        "embedding_dim": expected_embedding_dim(),
        "ingested_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def _parse_stored_dim(raw: Any) -> int | None:
    if raw is None:
        return None
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def _collect_stored_embedding_fingerprints(sb: Any, *, sample_limit: int = 40) -> tuple[set[str], set[int], bool]:
    """返回 (models, dims, saw_any_stamped_row)。"""
    models: set[str] = set()
    dims: set[int] = set()
    saw_stamped = False

    def _ingest_rows(rows: Any) -> None:
        nonlocal saw_stamped
        if not isinstance(rows, list):
            return
        for row in rows:
            if not isinstance(row, dict):
                continue
            md = row.get("metadata")
            if not isinstance(md, dict):
                continue
            sm = md.get("embedding_model")
            if isinstance(sm, str) and sm.strip():
                saw_stamped = True
                models.add(sm.strip())
            sd = _parse_stored_dim(md.get("embedding_dim"))
            if sd is not None:
                dims.add(sd)

    # 优先读已写入 fingerprint 的行（避免 legacy 样本稀释）
    try:
        res = (
            sb.table("documents")
            .select("metadata")
            .neq("metadata->>embedding_model", "")
            .limit(sample_limit)
            .execute()
        )
        _ingest_rows(res.data)
    except Exception:  # noqa: BLE001
        pass

    if saw_stamped:
        return models, dims, True

    try:
        res = sb.table("documents").select("metadata").limit(sample_limit).execute()
        _ingest_rows(res.data)
    except Exception:  # noqa: BLE001
        return models, dims, False

    return models, dims, saw_stamped


def check_embedding_alignment(sb: Any) -> EmbeddingAlignment:
    """比对运行时 embedding 配置与 Supabase documents.metadata 中的入库指纹。"""
    runtime_model = siliconflow_embedding_model()
    runtime_dim = expected_embedding_dim()
    stored_models, stored_dims, saw_stamped = _collect_stored_embedding_fingerprints(sb)

    if not saw_stamped and not stored_models and not stored_dims:
        return EmbeddingAlignment(
            ok=True,
            runtime_model=runtime_model,
            runtime_dim=runtime_dim,
            stored_models=(),
            stored_dims=(),
            legacy_unstamped=True,
        )

    if len(stored_models) > 1:
        return EmbeddingAlignment(
            ok=False,
            runtime_model=runtime_model,
            runtime_dim=runtime_dim,
            stored_models=tuple(sorted(stored_models)),
            stored_dims=tuple(sorted(stored_dims)),
            message=(
                "向量库中存在多种 embedding_model（"
                f"{', '.join(sorted(stored_models))}"
                f"），当前运行时={runtime_model!r}。"
                "请全量 re-sync 后再切换查询侧模型。"
            ),
            error_code=EMBEDDING_MISMATCH_ERROR_CODE,
        )

    if stored_models and runtime_model not in stored_models:
        stored = next(iter(stored_models))
        return EmbeddingAlignment(
            ok=False,
            runtime_model=runtime_model,
            runtime_dim=runtime_dim,
            stored_models=tuple(sorted(stored_models)),
            stored_dims=tuple(sorted(stored_dims)),
            message=(
                f"Embedding 模型不一致：运行时={runtime_model!r}，"
                f"向量库={stored!r}。"
                "请对齐 SILICONFLOW_EMBEDDING_MODEL（本地 / Vercel / CI ingest）并全量 re-sync。"
            ),
            error_code=EMBEDDING_MISMATCH_ERROR_CODE,
        )

    if stored_dims and runtime_dim not in stored_dims:
        stored = next(iter(stored_dims))
        return EmbeddingAlignment(
            ok=False,
            runtime_model=runtime_model,
            runtime_dim=runtime_dim,
            stored_models=tuple(sorted(stored_models)),
            stored_dims=tuple(sorted(stored_dims)),
            message=(
                f"Embedding 维度不一致：运行时={runtime_dim}，向量库={stored}。"
                "请对齐 EMBEDDING_DIM 并全量 re-sync。"
            ),
            error_code=EMBEDDING_MISMATCH_ERROR_CODE,
        )

    return EmbeddingAlignment(
        ok=True,
        runtime_model=runtime_model,
        runtime_dim=runtime_dim,
        stored_models=tuple(sorted(stored_models)),
        stored_dims=tuple(sorted(stored_dims)),
    )


def clear_embedding_alignment_cache() -> None:
    global _cached_alignment
    with _cache_lock:
        _cached_alignment = None


def ensure_embedding_alignment(sb: Any, *, force: bool = False) -> EmbeddingAlignment:
    """进程内缓存的一致性检查；block/warn/off 由 RAG_EMBEDDING_MISMATCH_MODE 控制。"""
    global _cached_alignment
    mode = embedding_mismatch_mode()
    if mode == "off":
        return EmbeddingAlignment(
            ok=True,
            runtime_model=siliconflow_embedding_model(),
            runtime_dim=expected_embedding_dim(),
            stored_models=(),
            stored_dims=(),
        )

    with _cache_lock:
        if _cached_alignment is not None and not force:
            alignment = _cached_alignment
        else:
            alignment = check_embedding_alignment(sb)
            _cached_alignment = alignment

    if alignment.ok:
        if alignment.legacy_unstamped and mode == "block":
            # 无 stamp 的旧库：放行但提示运维 re-sync（避免一次性误杀）
            return alignment
        return alignment

    if mode == "warn":
        print(
            f"[rag.embedding_guard] WARN {alignment.message}",
            file=os.sys.stderr,
        )
        return EmbeddingAlignment(
            ok=True,
            runtime_model=alignment.runtime_model,
            runtime_dim=alignment.runtime_dim,
            stored_models=alignment.stored_models,
            stored_dims=alignment.stored_dims,
            message=alignment.message,
        )

    return alignment
