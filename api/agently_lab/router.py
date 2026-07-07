"""Agently lab HTTP 路由（maintainer 门 · flag 控制）。"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from api.agently_lab.doc_review import run_doc_review_stub
from api.agently_lab.flags import is_agently_lab_enabled, is_agently_lab_online
from api.agently_lab.schemas import DocReviewRequest, DocReviewResult
from api.ops.deps import OpsPrincipal, require_ops_maintainer

router = APIRouter(prefix="/agently-lab", tags=["agently-lab"])


def _require_lab_enabled() -> None:
    if not is_agently_lab_enabled():
        raise HTTPException(
            status_code=404,
            detail={"code": "AGENTLY_LAB_DISABLED", "message": "设置 AGENTLY_LAB_ENABLED=1 启用"},
        )


def _repo_root() -> Path:
    """仓根；读 `docs/harness/**` 时设 AGENTLY_LAB_REPO_ROOT=工作区 Projects 根。"""
    raw = (os.getenv("AGENTLY_LAB_REPO_ROOT") or os.getenv("REPO_ROOT") or "").strip()
    if raw:
        return Path(raw).resolve()
    # api-python 仓根：api/agently_lab/router.py -> parents[2]
    return Path(__file__).resolve().parents[2]


@router.get("/health")
def agently_lab_health(
    _: None = Depends(_require_lab_enabled),
) -> dict[str, object]:
    return {
        "ok": True,
        "service": "agently-lab",
        "online_mode": is_agently_lab_online(),
    }


@router.post("/doc-review", response_model=DocReviewResult)
def doc_review(
    body: DocReviewRequest,
    _principal: OpsPrincipal = Depends(require_ops_maintainer),
    _: None = Depends(_require_lab_enabled),
) -> DocReviewResult:
    """Harness 文档/task 审查（stub → Agently Flow）。"""
    try:
        return run_doc_review_stub(request=body, repo_root=_repo_root())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"code": "DOC_NOT_FOUND", "message": str(exc)}) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={"code": "DOC_REVIEW_INVALID", "message": str(exc)}) from exc
