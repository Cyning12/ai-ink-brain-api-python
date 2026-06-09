"""Admin ingest / sync 路由 handlers（从 api/index.py 下沉）。"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, Header, HTTPException, Query
from fastapi.responses import JSONResponse

from ..auth_utils import _require_auth
from ..code_ingest import process_code_files
from ..ingest_pipeline import create_sync_job, get_job, process_markdown_files, run_sync_job_sync


async def py_admin_sync_post(
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    _require_auth(authorization, x_blog_admin_token, x_admin_token)
    job_inner = create_sync_job()
    jid = job_inner["id"]

    async def runner() -> None:
        await asyncio.to_thread(run_sync_job_sync, jid)

    background_tasks.add_task(runner)
    job_view = get_job(jid)
    return JSONResponse(
        status_code=202,
        content={
            "ok": True,
            "job": job_view,
            "statusUrl": f"/api/py/admin/sync?jobId={jid}",
        },
    )


async def py_admin_sync_get(
    job_id: str = Query(..., alias="jobId"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> dict[str, Any]:
    _require_auth(authorization, x_blog_admin_token, x_admin_token)
    jid = job_id.strip()
    if not jid:
        raise HTTPException(status_code=400, detail="Missing required query param: jobId")
    job = get_job(jid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"ok": True, "job": job}


async def py_admin_ingest(
    type: str = Query("markdown", description="ingest 类型: markdown | code"),
    repo_path: str | None = Query(None, description="代码项目路径（仅 type=code 有效）"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    _require_auth(authorization, x_blog_admin_token, x_admin_token)
    try:
        t = (type or "markdown").strip().lower()
        if t == "markdown":
            result = await asyncio.to_thread(process_markdown_files)
        elif t == "code":
            root: Path | None = None
            if repo_path and repo_path.strip():
                root = Path(repo_path.strip()).expanduser().resolve()
            result = await asyncio.to_thread(process_code_files, root)
        else:
            raise HTTPException(status_code=400, detail="Invalid ingest type")
        return JSONResponse(content={"ok": True, **result})
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        status = 500
        if "维度" in msg or "Unsupported" in msg:
            status = 400
        return JSONResponse({"ok": False, "error": msg}, status_code=status)
