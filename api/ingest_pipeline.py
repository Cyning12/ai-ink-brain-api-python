"""
content/ → 分块 → SiliconFlow 向量 → Supabase documents。

注意：该 repo 不包含 content/，用于远端部署时通常只跑 chat；
若要在此项目里跑 ingest/sync，请自行提供 content/ 目录或实现远端数据源。
"""

from __future__ import annotations

import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .rag_env import (
    REPO_ROOT,
    embedding_kwargs_for_inputs,
    expected_embedding_dim,
    openai_siliconflow_client,
    supabase_client,
)

EMBED_BATCH_SIZE = 32
INSERT_BATCH_SIZE = 80
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

DEBUG_INGEST = os.getenv("DEBUG_INGEST", "").lower() in ("1", "true", "yes")


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def chunk_text_by_chars(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[tuple[str, int]]:
    cleaned = text.replace("\r\n", "\n").strip()
    if not cleaned:
        return []
    step = max(1, chunk_size - overlap)
    chunks: list[tuple[str, int]] = []
    idx = 0
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        slice_ = cleaned[start:end].strip()
        if slice_:
            chunks.append((slice_, idx))
            idx += 1
        if end >= len(cleaned):
            break
        start += step
    return chunks


def _is_md(name: str) -> bool:
    lower = name.lower()
    return lower.endswith(".md") or lower.endswith(".mdx")


@dataclass
class IngestMeta:
    category: str
    slug: str
    last_modified: str
    relative_path: str
    chunk_index: int


@dataclass
class IngestChunk:
    content: str
    metadata: IngestMeta


def _walk_markdown(content_root: Path) -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    if not content_root.is_dir():
        return out

    for dirpath, dirnames, filenames in os.walk(content_root):
        dirnames[:] = [
            d
            for d in dirnames
            if not d.startswith(".") and d not in ("node_modules", ".next")
        ]
        for fn in filenames:
            if not _is_md(fn):
                continue
            abs_p = Path(dirpath) / fn
            rel = abs_p.relative_to(content_root).as_posix()
            out.append((abs_p, rel))
    return sorted(out, key=lambda x: x[1])


def get_all_markdown_chunks() -> list[IngestChunk]:
    content_root = REPO_ROOT / "content"
    content_root.mkdir(parents=True, exist_ok=True)
    results: list[IngestChunk] = []
    for abs_p, rel in _walk_markdown(content_root):
        stat = abs_p.stat()
        last_modified = (
            datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
        parts = rel.split("/")
        category = parts[0] if parts else "uncategorized"
        base = abs_p.name
        slug = re.sub(r"\.(md|mdx)$", "", base, flags=re.IGNORECASE)
        raw = abs_p.read_text(encoding="utf-8")
        for text, cidx in chunk_text_by_chars(raw):
            results.append(
                IngestChunk(
                    content=text,
                    metadata=IngestMeta(
                        category=category or "uncategorized",
                        slug=slug,
                        last_modified=last_modified,
                        relative_path=rel,
                        chunk_index=cidx,
                    ),
                )
            )
    return results


def _filename_from_rel(rel: str) -> str:
    return Path(rel).name


def to_db_metadata(chunk: IngestChunk) -> dict[str, Any]:
    m = chunk.metadata
    return {
        "category": m.category,
        "slug": m.slug,
        "mtime": m.last_modified,
        "lastModified": m.last_modified,
        "relativePath": m.relative_path,
        "chunk_index": m.chunk_index,
        "filename": _filename_from_rel(m.relative_path),
        "original_link": None,
        "page_number": None,
        "section_header": None,
    }


def build_enhanced_chunk_text(chunk: IngestChunk) -> str:
    m = chunk.metadata
    fn = _filename_from_rel(m.relative_path)
    return "\n".join(
        [
            "[Document Context]",
            f"Title: {fn}",
            f"Date: {m.last_modified}",
            f"Category: {m.category}",
            "---",
            f"Content: {chunk.content}",
        ]
    )


def _assert_dim(vec: list[float], index: int) -> None:
    exp = expected_embedding_dim()
    if len(vec) != exp:
        raise RuntimeError(
            f"Embedding 维度为 {len(vec)}，与期望 {exp}（EMBEDDING_DIM / SILICONFLOW_EMBEDDING_DIM 与 supabase vector(N)）不一致。分块索引：{index}"
        )


def delete_documents_by_relative_paths(sb: Any, relative_paths: list[str]) -> int:
    deleted = 0
    for rel in relative_paths:
        res = sb.table("documents").select("id").eq("metadata->>relativePath", rel).execute()
        rows = res.data if isinstance(res.data, list) else []
        ids = [r["id"] for r in rows if isinstance(r, dict) and "id" in r]
        if not ids:
            continue
        sb.table("documents").delete().in_("id", ids).execute()
        deleted += len(ids)
    return deleted


def delete_documents_by_slugs(sb: Any, slugs: list[str]) -> int:
    deleted = 0
    for slug in slugs:
        sel = sb.table("documents").select("id").eq("metadata->>slug", slug).execute()
        rows = sel.data if isinstance(sel.data, list) else []
        n = len(rows)
        if n == 0:
            continue
        sb.table("documents").delete().eq("metadata->>slug", slug).execute()
        deleted += n
    return deleted


def embed_texts_batch(client: Any, texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    kw = embedding_kwargs_for_inputs(texts)
    emb_res = client.embeddings.create(**kw)
    items = sorted(emb_res.data, key=lambda d: d.index)
    return [list(items[i].embedding) for i in range(len(items))]


def embed_one(client: Any, text: str) -> list[float]:
    vecs = embed_texts_batch(client, [text])
    return vecs[0]


def process_markdown_files() -> dict[str, Any]:
    chunks = get_all_markdown_chunks()
    unique_paths = sorted({c.metadata.relative_path for c in chunks})
    files_scanned = len(unique_paths)
    if not chunks:
        return {
            "filesScanned": files_scanned,
            "chunksTotal": 0,
            "chunksInserted": 0,
            "rowsDeleted": 0,
        }

    if DEBUG_INGEST:
        print(f"[ingest] Files to process: {len(unique_paths)}")
        for p in unique_paths:
            print(f"[ingest] file: {p}")

    sb = supabase_client()
    client = openai_siliconflow_client()
    rows_deleted = delete_documents_by_relative_paths(sb, unique_paths)

    embeddings: list[list[float]] = []
    for i in range(0, len(chunks), EMBED_BATCH_SIZE):
        batch = chunks[i : i + EMBED_BATCH_SIZE]
        texts = [build_enhanced_chunk_text(c) for c in batch]
        vectors = embed_texts_batch(client, texts)
        for j, vec in enumerate(vectors):
            _assert_dim(vec, i + j)
            embeddings.append(vec)
        if DEBUG_INGEST:
            print(f"[ingest] Embedded {min(i + EMBED_BATCH_SIZE, len(chunks))}/{len(chunks)} chunks")

    rows = [
        {
            "content": build_enhanced_chunk_text(chunks[idx]),
            "metadata": to_db_metadata(chunks[idx]),
            "embedding": embeddings[idx],
        }
        for idx in range(len(chunks))
    ]

    inserted = 0
    for i in range(0, len(rows), INSERT_BATCH_SIZE):
        slice_ = rows[i : i + INSERT_BATCH_SIZE]
        sb.table("documents").insert(slice_).execute()
        inserted += len(slice_)

    return {
        "filesScanned": files_scanned,
        "chunksTotal": len(chunks),
        "chunksInserted": inserted,
        "rowsDeleted": rows_deleted,
    }


def sync_content_to_vector() -> dict[str, Any]:
    chunks = get_all_markdown_chunks()
    unique_paths = sorted({c.metadata.relative_path for c in chunks})
    files_scanned = len(unique_paths)
    if not chunks:
        return {
            "filesScanned": files_scanned,
            "chunksTotal": 0,
            "chunksUpserted": 0,
            "rowsDeleted": 0,
        }

    if DEBUG_INGEST:
        print(f"[ingest] Files to process: {len(unique_paths)}")
        for p in unique_paths:
            print(f"[ingest] file: {p}")

    unique_slugs = list({c.metadata.slug for c in chunks})
    sb = supabase_client()
    client = openai_siliconflow_client()
    rows_deleted = delete_documents_by_slugs(sb, unique_slugs)

    embeddings: list[list[float]] = []
    last_rel = ""
    for i, chunk in enumerate(chunks):
        if DEBUG_INGEST and chunk.metadata.relative_path != last_rel:
            last_rel = chunk.metadata.relative_path
            print(f"[ingest] Processing file: {last_rel}")
        vec = embed_one(client, build_enhanced_chunk_text(chunk))
        _assert_dim(vec, i)
        embeddings.append(vec)
        if DEBUG_INGEST and (i + 1) % 25 == 0:
            print(f"[ingest] Embedded {i + 1}/{len(chunks)} chunks")

    rows = [
        {
            "content": build_enhanced_chunk_text(chunks[idx]),
            "metadata": to_db_metadata(chunks[idx]),
            "embedding": embeddings[idx],
        }
        for idx in range(len(chunks))
    ]

    inserted = 0
    for i in range(0, len(rows), INSERT_BATCH_SIZE):
        slice_ = rows[i : i + INSERT_BATCH_SIZE]
        sb.table("documents").insert(slice_).execute()
        inserted += len(slice_)

    return {
        "filesScanned": files_scanned,
        "chunksTotal": len(chunks),
        "chunksUpserted": inserted,
        "rowsDeleted": rows_deleted,
    }


# --- 内存任务队列（单实例；serverless 场景不保证持久） ---

JOBS: dict[str, dict[str, Any]] = {}


def _job_public(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": job["id"],
        "status": job["status"],
        "createdAt": job["createdAt"],
        "startedAt": job["startedAt"],
        "finishedAt": job["finishedAt"],
        "result": job["result"],
        "error": job["error"],
    }


def create_sync_job() -> dict[str, Any]:
    job_id = str(uuid.uuid4())
    now = _iso_now()
    job: dict[str, Any] = {
        "id": job_id,
        "status": "queued",
        "createdAt": now,
        "startedAt": None,
        "finishedAt": None,
        "result": None,
        "error": None,
    }
    JOBS[job_id] = job
    return job


def run_sync_job_sync(job_id: str) -> None:
    job = JOBS.get(job_id)
    if not job:
        return
    job["status"] = "running"
    job["startedAt"] = _iso_now()
    try:
        result = sync_content_to_vector()
        job["status"] = "succeeded"
        job["result"] = result
    except Exception as e:  # noqa: BLE001
        job["status"] = "failed"
        job["error"] = str(e)
    finally:
        job["finishedAt"] = _iso_now()


def get_job(job_id: str) -> dict[str, Any] | None:
    job = JOBS.get(job_id)
    return _job_public(job) if job else None

