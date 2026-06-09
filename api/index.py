"""
RAG 聊天服务：日期查询扩展 + SiliconFlow 向量 + Supabase match_documents + 流式对话；
管理端：/api/py/admin/sync、/api/py/admin/ingest（向量入库）。

调试检索：设置环境变量 `DEBUG_RAG=1` 或 `RAG_DEBUG=1`（或 `NODE_ENV=development`）。
阈值：`RAG_MATCH_THRESHOLD=none` 关闭 SQL 侧相似度过滤（默认 0.3）。
"""

from __future__ import annotations

import asyncio
import hmac
from pathlib import Path
from typing import Any

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Query,
    Request,
)
from fastapi.responses import JSONResponse, StreamingResponse

from . import (
    chain_chat,
    code_retrieval,
    rag_env,  # noqa: F401 — 触发 REPO_ROOT .env 加载
    text2sql_api,
    unified_chat,
    unified_chat_graph,
)
from .chatbi_principal import (
    ChatBiPrincipal,
    require_chatbi_principal,
    resolve_chatbi_from_plain_token,
)
from .chatbi_rate_limit import register_rate_limit_middleware
from .code_ingest import process_code_files
from .ingest_pipeline import (
    create_sync_job,
    get_job,
    process_markdown_files,
    run_sync_job_sync,
)
from .rag_env import (
    admin_secret,
    api_key_optional,
    pick_supabase_service_key,
    pick_supabase_url,
    siliconflow_api_key_optional,
    siliconflow_base,
    siliconflow_chat_model,
    siliconflow_embedding_dimensions,
    siliconflow_embedding_model,
)
from .rag_shared import (
    _rag_log,
    build_sources_payload,
    parse_match_threshold,
)
from .routes.legacy_chat import chat, chat_history, chat_suggested_questions

app = FastAPI(title="AI-Ink-Brain RAG API")
register_rate_limit_middleware(app)

MATCH_COUNT = 10
CONTEXT_MAX_CHARS = 6000

SOURCES_JSON_SEPARATOR = "---RAG_SOURCES_JSON---"


def _require_auth(
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None = None,
) -> None:
    expected_admin = admin_secret()
    expected_api = api_key_optional()
    if not expected_admin and not expected_api:
        raise HTTPException(status_code=500, detail="未配置 SYNC_ADMIN_SECRET 或 API_KEY")
    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif x_blog_admin_token:
        token = x_blog_admin_token.strip()
    elif x_admin_token:
        token = x_admin_token.strip()

    def _match(expected: str | None) -> bool:
        if not expected:
            return False
        if len(token) != len(expected):
            return False
        return hmac.compare_digest(token.encode("utf-8"), expected.encode("utf-8"))

    if not (_match(expected_admin) or _match(expected_api)):
        raise HTTPException(status_code=401, detail="Unauthorized")


def _try_chatbi_bearer_plain(plain: str) -> bool:
    """尝试将明文当作 ChatBI DB token 校验。成功返回 True；`bad_hash` 返回 False（回退 Ink）；其它 401 原样抛出。"""
    t = plain.strip()
    if not t:
        return False
    try:
        resolve_chatbi_from_plain_token(t)
        return True
    except HTTPException as e:
        if e.status_code != 401:
            raise
        det = e.detail if isinstance(e.detail, dict) else {}
        if det.get("reason") == "bad_hash":
            return False
        raise


async def _require_rag_history_auth(
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
    x_chatbi_access_token: str | None,
) -> None:
    """ChatBI：`X-ChatBI-Access-Token` 或 `Authorization: Bearer <明文>`；否则 Ink admin / API_KEY。"""
    if (x_chatbi_access_token or "").strip():
        await asyncio.to_thread(resolve_chatbi_from_plain_token, (x_chatbi_access_token or "").strip())
        return
    auth = (authorization or "").strip()
    bearer_plain = ""
    if auth.lower().startswith("bearer "):
        bearer_plain = auth[7:].strip()
    if bearer_plain:
        ok = await asyncio.to_thread(_try_chatbi_bearer_plain, bearer_plain)
        if ok:
            return
    _require_auth(authorization, x_blog_admin_token, x_admin_token)


code_retrieval.bind_index_symbols(
    build_sources_payload_=build_sources_payload,
    parse_match_threshold_=parse_match_threshold,
    siliconflow_base_=siliconflow_base(),
    siliconflow_embedding_model_=siliconflow_embedding_model(),
    siliconflow_embedding_dimensions_=siliconflow_embedding_dimensions(),
    siliconflow_chat_model_=siliconflow_chat_model(),
    match_count_=MATCH_COUNT,
    rag_log_=_rag_log,
)


def _build_live_payload() -> dict[str, Any]:
    return {
        "ok": True,
        "service": "ai-ink-brain-rag",
        "probe": "live",
    }


def _component_status(name: str, ok: bool, detail: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": name,
        "status": "ok" if ok else "failed",
    }
    if detail:
        payload["detail"] = detail
    return payload


def _build_ready_components() -> list[dict[str, Any]]:
    supabase_url = (pick_supabase_url() or "").strip()
    supabase_key = (pick_supabase_service_key() or "").strip()
    siliconflow_api_key = siliconflow_api_key_optional()

    components: list[dict[str, Any]] = []
    if supabase_url and supabase_key:
        components.append(_component_status("supabase", True))
    else:
        components.append(
            _component_status(
                "supabase",
                False,
                "missing NEXT_PUBLIC_SUPABASE_URL/SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY/SUPABASE_SERVICE_KEY",
            )
        )

    if siliconflow_api_key:
        components.append(_component_status("siliconflow_api_key", True))
    else:
        components.append(_component_status("siliconflow_api_key", False, "missing SILICONFLOW_API_KEY"))
    return components


@app.get("/api/py/live")
def live() -> dict[str, Any]:
    # live 探针仅反映进程存活，不执行重依赖外呼。
    return _build_live_payload()


@app.get("/api/py/ready")
def ready() -> JSONResponse:
    components = _build_ready_components()
    is_ready = all(c.get("status") == "ok" for c in components)
    payload = {
        "ok": is_ready,
        "service": "ai-ink-brain-rag",
        "probe": "ready",
        "components": components,
    }
    return JSONResponse(status_code=200 if is_ready else 503, content=payload)


@app.get("/api/py/health")
def health() -> dict[str, Any]:
    # 兼容历史探针：沿用轻量语义，对齐 live 契约返回。
    return _build_live_payload()


@app.get("/api/py/chat/history")
async def chat_history_route(
    session_id: str = Query(..., description="与 POST /api/py/chat 相同的 session_id"),
    limit: int = Query(100, ge=1, le=200, description="最多返回最近多少轮完整问答"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
    x_chatbi_access_token: str | None = Header(default=None, alias="x-chatbi-access-token"),
) -> dict[str, Any]:
    return await chat_history(
        session_id=session_id,
        limit=limit,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
        x_chatbi_access_token=x_chatbi_access_token,
    )


@app.post("/api/py/code/query")
async def code_query(
    request: Request,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    return await code_retrieval.handle_code_query(
        request,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.post("/api/py/code/search")
async def code_search(
    request: Request,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    return await code_retrieval.handle_code_search(
        request,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.post("/api/py/text2sql/chat")
async def text2sql_chat(
    request: Request,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    return await text2sql_api.handle_text2sql_chat(
        request,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.post("/api/py/chain/chat")
async def chain_chat_route(
    request: Request,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    return await chain_chat.handle_chain_chat(
        request,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.post("/api/py/unified/chat")
async def unified_chat_route(
    request: Request,
    principal: ChatBiPrincipal = Depends(require_chatbi_principal),
) -> JSONResponse:
    return await unified_chat.handle_unified_chat(request, principal=principal)


@app.post("/api/py/unified/chat/stream")
async def unified_chat_stream_route(
    request: Request,
    principal: ChatBiPrincipal = Depends(require_chatbi_principal),
):
    return await unified_chat.handle_unified_chat_stream(request, principal=principal)


@app.post("/api/py/unified/chat/graph")
async def unified_chat_graph_route(
    request: Request,
    principal: ChatBiPrincipal = Depends(require_chatbi_principal),
) -> JSONResponse:
    return await unified_chat_graph.handle_unified_chat_graph(request, principal=principal)


@app.post("/api/py/unified/chat/graph/stream")
async def unified_chat_graph_stream_route(
    request: Request,
    principal: ChatBiPrincipal = Depends(require_chatbi_principal),
):
    return await unified_chat_graph.handle_unified_chat_graph_stream(request, principal=principal)


@app.get("/api/py/chatbi/access/verify")
async def chatbi_access_verify(
    principal: ChatBiPrincipal = Depends(require_chatbi_principal),
) -> JSONResponse:
    """轻量探活：仅校验 Bearer 与 `chatbi_access_tokens`，供 Ink BFF 解锁前置。"""
    return JSONResponse(
        {
            "ok": True,
            "access_level": principal.access_level,
            "principal_kind": principal.principal_kind,
            "token_id": str(principal.token_id),
        }
    )


@app.post("/api/py/chat")
async def chat_route(
    request: Request,
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> StreamingResponse:
    return await chat(
        request=request,
        background_tasks=background_tasks,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.post("/api/py/admin/sync")
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


@app.get("/api/py/admin/sync")
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


@app.post("/api/py/admin/ingest")
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


@app.get("/api/py/chat/suggested-questions")
def chat_suggested_questions_route() -> JSONResponse:
    return chat_suggested_questions()
