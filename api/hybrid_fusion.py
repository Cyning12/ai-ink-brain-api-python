from __future__ import annotations

from typing import Any

# RRF 融合的常用常数（论文/业界常见取值 60）
RRF_K = 60


def _rrf_score(rank: int, *, k: int = RRF_K) -> float:
    """Reciprocal Rank Fusion: 1 / (k + rank)，rank 从 1 开始。"""
    r = max(1, int(rank))
    return 1.0 / float(k + r)


def fuse_hits_rrf(
    vector_hits: list[dict[str, Any]],
    keyword_hits: list[dict[str, Any]],
    *,
    max_total: int = 22,
) -> list[dict[str, Any]]:
    """将两路召回按排名做 RRF 融合，输出按 fused_score 降序的去重结果。"""
    by_id: dict[Any, dict[str, Any]] = {}

    for idx, h in enumerate(vector_hits):
        hid = h.get("id")
        if hid is None:
            continue
        row = by_id.get(hid) or dict(h)
        row["rrf"] = row.get("rrf") or {}
        if isinstance(row["rrf"], dict):
            row["rrf"]["vector_rank"] = idx + 1
            row["rrf"]["vector_score"] = _rrf_score(idx + 1)
        by_id[hid] = row

    for idx, h in enumerate(keyword_hits):
        hid = h.get("id")
        if hid is None:
            continue
        row = by_id.get(hid) or dict(h)
        row["rrf"] = row.get("rrf") or {}
        if isinstance(row["rrf"], dict):
            row["rrf"]["keyword_rank"] = idx + 1
            row["rrf"]["keyword_score"] = _rrf_score(idx + 1)
        by_id[hid] = row

    fused: list[dict[str, Any]] = []
    for _hid, row in by_id.items():
        rrf = row.get("rrf") if isinstance(row.get("rrf"), dict) else {}
        vs = float(rrf.get("vector_score") or 0.0)
        ks = float(rrf.get("keyword_score") or 0.0)
        row["fused_score"] = vs + ks
        fused.append(row)

    fused.sort(key=lambda r: float(r.get("fused_score") or 0.0), reverse=True)
    return fused[: max(1, int(max_total))]
