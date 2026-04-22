from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .code_parser import ParsedChunk, parse_project
from .ingest_pipeline import (
    EMBED_BATCH_SIZE,
    INSERT_BATCH_SIZE,
    IngestChunk,
    IngestMeta,
    embed_texts_batch,
    expected_embedding_dim,
    openai_siliconflow_client,
    supabase_client,
)

CODE_EMBED_BATCH_SIZE = EMBED_BATCH_SIZE
CODE_INSERT_BATCH_SIZE = INSERT_BATCH_SIZE

DEBUG_CODE_INGEST = os.getenv("DEBUG_CODE_INGEST", "").lower() in ("1", "true", "yes")


def _iso_from_mtime(mtime: float) -> str:
    return (
        datetime.fromtimestamp(mtime, tz=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


@dataclass(frozen=True)
class CodeIngestMeta:
    """代码入库扩展元信息（最终写入 metadata jsonb）。"""

    file_path: str
    start_line: int
    end_line: int
    chunk_type: str
    name: str
    signature: str
    module: str


def _to_ingest_chunk(repo_root: Path, pc: ParsedChunk, *, chunk_index: int) -> IngestChunk:
    abs_p = Path(pc.file_path)
    stat = abs_p.stat()
    last_modified = _iso_from_mtime(stat.st_mtime)
    slug = f"{pc.module}.{pc.name}".strip(".")
    meta = IngestMeta(
        category="code",
        slug=slug,
        last_modified=last_modified,
        relative_path=pc.relative_path,
        chunk_index=int(chunk_index),
    )
    # 动态挂载扩展字段（保持复用现有 IngestMeta 结构；后续写库会展开到 jsonb）
    for k, v in CodeIngestMeta(
        file_path=pc.file_path,
        start_line=pc.start_line,
        end_line=pc.end_line,
        chunk_type=pc.chunk_type,
        name=pc.name,
        signature=pc.signature,
        module=pc.module,
    ).__dict__.items():
        setattr(meta, k, v)
    return IngestChunk(content=pc.body, metadata=meta)


def get_all_code_chunks(*, repo_root: Path | None = None) -> list[IngestChunk]:
    root = (repo_root or Path(__file__).resolve().parent.parent).resolve()
    parsed: list[ParsedChunk] = parse_project(root)
    # 每个文件内 chunk_index 递增，按 relative_path 分组
    out: list[IngestChunk] = []
    counter_by_file: dict[str, int] = {}
    for pc in parsed:
        cidx = counter_by_file.get(pc.relative_path, 0)
        out.append(_to_ingest_chunk(root, pc, chunk_index=cidx))
        counter_by_file[pc.relative_path] = cidx + 1
    return out


def build_enhanced_code_text(chunk: IngestChunk) -> str:
    m = chunk.metadata
    # 兼容：这些字段由 _to_ingest_chunk 动态挂载
    file_rel = getattr(m, "relative_path", "")
    module = getattr(m, "module", "")
    start = getattr(m, "start_line", "")
    end = getattr(m, "end_line", "")
    chunk_type = getattr(m, "chunk_type", "")
    name = getattr(m, "name", "")
    signature = getattr(m, "signature", "")

    content = (chunk.content or "").replace("\r\n", "\n").rstrip()
    return "\n".join(
        [
            "[Code Context]",
            f"File: {file_rel}",
            f"Module: {module}",
            f"Lines: {start}-{end}",
            f"Type: {chunk_type}",
            f"Name: {name}",
            f"Signature: {signature}",
            "---",
            "Content:",
            content,
        ]
    )


def to_db_metadata_code(chunk: IngestChunk) -> dict[str, Any]:
    """写入 code_chunks.metadata 的 JSON（与 Markdown ingest 字段对齐并扩展代码字段）。"""
    m = chunk.metadata
    meta: dict[str, Any] = {
        "category": m.category,
        "slug": m.slug,
        "mtime": m.last_modified,
        "lastModified": m.last_modified,
        "relativePath": m.relative_path,
        "chunk_index": m.chunk_index,
        "filename": Path(m.relative_path).name,
        "original_link": None,
        "page_number": None,
        "section_header": None,
        # 代码扩展字段
        "file_path": getattr(m, "file_path", None),
        "start_line": getattr(m, "start_line", None),
        "end_line": getattr(m, "end_line", None),
        "chunk_type": getattr(m, "chunk_type", None),
        "name": getattr(m, "name", None),
        "signature": getattr(m, "signature", None),
        "module": getattr(m, "module", None),
    }
    return meta


def delete_code_chunks_by_relative_paths(sb: Any, relative_paths: list[str]) -> int:
    deleted = 0
    for rel in relative_paths:
        res = sb.table("code_chunks").select("id").eq("metadata->>relativePath", rel).execute()
        rows = res.data if isinstance(res.data, list) else []
        ids = [r["id"] for r in rows if isinstance(r, dict) and "id" in r]
        if not ids:
            continue
        sb.table("code_chunks").delete().in_("id", ids).execute()
        deleted += len(ids)
    return deleted


def delete_code_chunks_by_relative_prefixes(sb: Any, prefixes: list[str]) -> int:
    """按 relativePath 前缀批量删除（用于清理被排除目录的历史脏数据）。"""
    deleted = 0
    for prefix in prefixes:
        pfx = (prefix or "").strip()
        if not pfx:
            continue
        # 先选 id，再批量删（supabase-py delete + ilike 组合不稳定，保持保守实现）
        res = sb.table("code_chunks").select("id").ilike("metadata->>relativePath", f"{pfx}%").execute()
        rows = res.data if isinstance(res.data, list) else []
        ids = [r["id"] for r in rows if isinstance(r, dict) and "id" in r]
        if not ids:
            continue
        sb.table("code_chunks").delete().in_("id", ids).execute()
        deleted += len(ids)
    return deleted


def _assert_dim(vec: list[float], index: int) -> None:
    exp = expected_embedding_dim()
    if len(vec) != exp:
        raise RuntimeError(
            f"Embedding 维度为 {len(vec)}，与期望 {exp}（EMBEDDING_DIM / SILICONFLOW_EMBEDDING_DIM 与 supabase vector(N)）不一致。分块索引：{index}"
        )


def process_code_files(repo_root: Path | None = None) -> dict[str, Any]:
    """解析 → Embedding → 写入 Supabase code_chunks（P1：按 relativePath 先删后插，幂等）。"""
    root = (repo_root or Path(__file__).resolve().parent.parent).resolve()
    chunks = get_all_code_chunks(repo_root=root)
    unique_paths = sorted({c.metadata.relative_path for c in chunks})
    files_scanned = len(unique_paths)
    if not chunks:
        return {
            "filesScanned": files_scanned,
            "chunksTotal": 0,
            "chunksInserted": 0,
            "rowsDeleted": 0,
        }

    if DEBUG_CODE_INGEST:
        print(f"[code-ingest] files={files_scanned} chunks={len(chunks)}")

    sb = supabase_client()
    client = openai_siliconflow_client()
    # 清理历史脏数据：docs/ 目录已在 parser 排除，但旧数据可能残留在表中
    rows_deleted = 0
    rows_deleted += delete_code_chunks_by_relative_prefixes(sb, ["docs/"])
    rows_deleted += delete_code_chunks_by_relative_paths(sb, unique_paths)

    embeddings: list[list[float]] = []
    enhanced_texts = [build_enhanced_code_text(c) for c in chunks]
    for i in range(0, len(enhanced_texts), CODE_EMBED_BATCH_SIZE):
        batch = enhanced_texts[i : i + CODE_EMBED_BATCH_SIZE]
        try:
            vectors = embed_texts_batch(client, batch)
        except Exception as exc:  # noqa: BLE001
            # 兼容离线/Key 失效场景：用零向量占位，保证 ingest 可继续，后续 query 自动降级 keyword-only
            if DEBUG_CODE_INGEST:
                print(f"[code-ingest] embedding failed, fallback zero-vectors: {exc!s}")
            dim = expected_embedding_dim()
            vectors = [[0.0] * dim for _ in batch]
        for j, vec in enumerate(vectors):
            _assert_dim(vec, i + j)
            embeddings.append(vec)
        if DEBUG_CODE_INGEST:
            print(
                f"[code-ingest] Embedded {min(i + CODE_EMBED_BATCH_SIZE, len(enhanced_texts))}/{len(enhanced_texts)}"
            )

    rows = [
        {
            "content": enhanced_texts[idx],
            "metadata": to_db_metadata_code(chunks[idx]),
            "embedding": embeddings[idx],
        }
        for idx in range(len(chunks))
    ]

    inserted = 0
    for i in range(0, len(rows), CODE_INSERT_BATCH_SIZE):
        slice_ = rows[i : i + CODE_INSERT_BATCH_SIZE]
        sb.table("code_chunks").insert(slice_).execute()
        inserted += len(slice_)

    # Hybrid：兜底刷新 fts_tokens（与 documents ingest 一致）
    try:
        sb.rpc(
            "refresh_code_chunks_fts_tokens_for_paths",
            {"relative_paths": unique_paths},
        ).execute()
    except Exception as exc:  # noqa: BLE001
        if DEBUG_CODE_INGEST:
            print(f"[code-ingest] refresh fts_tokens skipped: {exc!s}")

    return {
        "filesScanned": files_scanned,
        "chunksTotal": len(chunks),
        "chunksInserted": inserted,
        "rowsDeleted": rows_deleted,
    }

