from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

try:
    import faiss  # type: ignore[import-not-found]
except Exception:  # noqa: BLE001
    faiss = None  # type: ignore[assignment]

if TYPE_CHECKING:
    import numpy as np  # type: ignore[import-not-found]


DocType = Literal["ddl", "example"]


@dataclass(frozen=True)
class StoreDoc:
    doc_type: DocType
    title: str
    content: str


def _tokenize(text: str) -> list[str]:
    t = (text or "").lower()
    # 中英文混合：保留英文/数字/下划线与中文连续片段
    parts = re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]+", t)
    return [p for p in parts if p and p not in ("select", "from", "where", "and", "or")]


def _hash_embed(text: str, *, dim: int) -> np.ndarray:
    import numpy as np  # type: ignore[import-not-found]

    vec = np.zeros((dim,), dtype=np.float32)
    toks = _tokenize(text)
    if not toks:
        return vec
    for tok in toks:
        h = hashlib.md5(tok.encode("utf-8")).digest()
        idx = int.from_bytes(h[:4], "little") % dim
        sign = 1.0 if (h[4] % 2 == 0) else -1.0
        vec[idx] += sign
    # L2 normalize
    n = float(np.linalg.norm(vec))
    if n > 0:
        vec /= n
    return vec


def _parse_supabase_init_sql(path: Path) -> list[StoreDoc]:
    sql = path.read_text(encoding="utf-8")
    lines = sql.splitlines()
    docs: list[StoreDoc] = []

    # 抽取每个 create table public.xxx (...) 块作为 ddl doc
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"create table\s+public\.([a-z0-9_]+)\s*\(", line, flags=re.IGNORECASE)
        if not m:
            i += 1
            continue
        table = m.group(1)
        buf = [lines[i]]
        i += 1
        while i < len(lines):
            buf.append(lines[i])
            if lines[i].strip().endswith(");"):
                i += 1
                break
            i += 1
        ddl = "\n".join(buf).strip()
        docs.append(StoreDoc(doc_type="ddl", title=f"DDL: {table}", content=ddl))

    # 抽取样例 Q/A（若存在）
    samples_path = Path(__file__).resolve().parent.parent / "docs" / "text2sql" / "v1" / "spec" / "SAMPLES-01-text2sql-mini.md"
    if samples_path.exists():
        md = samples_path.read_text(encoding="utf-8")
        blocks = re.split(r"^##\s+", md, flags=re.MULTILINE)
        for b in blocks:
            b = b.strip()
            if not b or b.startswith("SAMPLES-01"):
                continue
            title = b.splitlines()[0].strip()
            docs.append(StoreDoc(doc_type="example", title=f"Example: {title}", content=b))

    return docs


class Text2SqlFaissStore:
    def __init__(self, *, dim: int, docs: list[StoreDoc]):
        if faiss is None:
            raise RuntimeError("Missing dependency: faiss-cpu")
        import numpy as np  # type: ignore[import-not-found]

        self.dim = int(dim)
        self.docs = docs
        self._index = faiss.IndexFlatIP(self.dim)

        mat = np.stack([_hash_embed(d.content, dim=self.dim) for d in docs], axis=0)
        self._index.add(mat)

    def search(self, query: str, *, top_k: int = 6) -> list[dict[str, Any]]:
        q = _hash_embed(query, dim=self.dim).reshape(1, -1)
        scores, idxs = self._index.search(q, max(1, int(top_k)))
        out: list[dict[str, Any]] = []
        for score, idx in zip(scores[0].tolist(), idxs[0].tolist(), strict=False):
            if idx < 0 or idx >= len(self.docs):
                continue
            d = self.docs[idx]
            out.append(
                {
                    "doc_type": d.doc_type,
                    "title": d.title,
                    "content": d.content,
                    "score": float(score),
                }
            )
        return out


class Text2SqlFallbackStore:
    """无 faiss 时的降级检索：用哈希向量做纯 Python 排序（维持可用性 + 可解释日志）。"""

    def __init__(self, *, dim: int, docs: list[StoreDoc]):
        import numpy as np  # type: ignore[import-not-found]

        self.dim = int(dim)
        self.docs = docs
        self._mat = np.stack([_hash_embed(d.content, dim=self.dim) for d in docs], axis=0)

    def search(self, query: str, *, top_k: int = 6) -> list[dict[str, Any]]:
        import numpy as np  # type: ignore[import-not-found]

        q = _hash_embed(query, dim=self.dim)
        scores = (self._mat @ q).astype(np.float32)
        k = max(1, int(top_k))
        idxs = np.argsort(-scores)[:k].tolist()
        out: list[dict[str, Any]] = []
        for idx in idxs:
            d = self.docs[int(idx)]
            out.append(
                {
                    "doc_type": d.doc_type,
                    "title": d.title,
                    "content": d.content,
                    "score": float(scores[int(idx)]),
                }
            )
        return out


_STORE: Any | None = None


def _t2s_debug(msg: str) -> None:
    if (os.getenv("TEXT2SQL_DEBUG") or "").strip().lower() in ("1", "true", "yes", "on"):
        print(f"[text2sql] {msg}", flush=True)


def get_text2sql_store():
    """惰性加载：从 repo 内的 supabase_init.sql + samples 构建 Text2SQL 检索库。"""
    global _STORE
    if _STORE is not None:
        return _STORE

    repo_root = Path(__file__).resolve().parent.parent
    init_sql = repo_root / "docs" / "text2sql" / "v1" / "sql" / "supabase_init.sql"
    if not init_sql.exists():
        raise RuntimeError("Missing corpus file: docs/text2sql/v1/sql/supabase_init.sql")

    dim = int(os.getenv("TEXT2SQL_FAISS_DIM", "256"))
    docs = _parse_supabase_init_sql(init_sql)
    _t2s_debug(f"init store: docs={len(docs)} dim={dim} faiss_available={faiss is not None}")
    if faiss is None:
        _t2s_debug(
            "faiss-cpu 未安装，已降级为 fallback store。可执行：pip install faiss-cpu 以提升检索性能。"
        )
        _STORE = Text2SqlFallbackStore(dim=dim, docs=docs)
    else:
        _STORE = Text2SqlFaissStore(dim=dim, docs=docs)
    return _STORE

