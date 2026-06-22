"""
RAG 聊天服务：日期查询扩展 + SiliconFlow 向量 + Supabase match_documents + 流式对话；
管理端：/api/py/admin/sync、/api/py/admin/ingest（向量入库）。

调试检索：设置环境变量 `DEBUG_RAG=1` 或 `RAG_DEBUG=1`（或 `NODE_ENV=development`）。
阈值：`RAG_MATCH_THRESHOLD=none` 关闭 SQL 侧相似度过滤（默认 0.3）。
"""

from __future__ import annotations

from typing import Any

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    Query,
    Request,
)
from fastapi.responses import JSONResponse, StreamingResponse

from . import (
    chain_chat,
    code_retrieval,
    ops,  # noqa: F401
    rag_env,  # noqa: F401 — 触发 REPO_ROOT .env 加载
    text2sql_api,
    unified_chat,
    unified_chat_graph,
)
from .chatbi_principal import (
    ChatBiPrincipal,
    require_chatbi_principal,
)
from .chatbi_rate_limit import register_rate_limit_middleware
from .ops import ops_router
from .rag_env import (
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
from .routes.admin_ingest import (
    py_admin_ingest as _legacy_admin_ingest,
)
from .routes.admin_ingest import (
    py_admin_sync_get as _legacy_admin_sync_get,
)
from .routes.admin_ingest import (
    py_admin_sync_post as _legacy_admin_sync_post,
)
from .routes.legacy_chat import (
    chat as _legacy_chat,
)
from .routes.legacy_chat import (
    chat_history as _legacy_chat_history,
)
from .routes.legacy_chat import (
    chat_suggested_questions as _legacy_chat_suggested_questions,
)

app = FastAPI(title="AI-Ink-Brain RAG API")
register_rate_limit_middleware(app)

MATCH_COUNT = 10
CONTEXT_MAX_CHARS = 6000

SOURCES_JSON_SEPARATOR = "---RAG_SOURCES_JSON---"


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
async def chat_history(
    session_id: str = Query(..., description="与 POST /api/py/chat 相同的 session_id"),
    limit: int = Query(100, ge=1, le=200, description="最多返回最近多少轮完整问答"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
    x_chatbi_access_token: str | None = Header(default=None, alias="x-chatbi-access-token"),
) -> dict[str, Any]:
    return await _legacy_chat_history(
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
async def chat(
    request: Request,
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> StreamingResponse:
    return await _legacy_chat(
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
    return await _legacy_admin_sync_post(
        background_tasks=background_tasks,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.get("/api/py/admin/sync")
async def py_admin_sync_get(
    job_id: str = Query(..., alias="jobId"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> dict[str, Any]:
    return await _legacy_admin_sync_get(
        job_id=job_id,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.post("/api/py/admin/ingest")
async def py_admin_ingest(
    type: str = Query("markdown", description="ingest 类型: markdown | code"),
    repo_path: str | None = Query(None, description="代码项目路径（仅 type=code 有效）"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> JSONResponse:
    return await _legacy_admin_ingest(
        type=type,
        repo_path=repo_path,
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
    )


@app.get("/api/py/chat/suggested-questions")
def chat_suggested_questions() -> JSONResponse:
    return _legacy_chat_suggested_questions()


app.include_router(ops_router, prefix="/api/py")
