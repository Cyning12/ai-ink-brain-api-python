"""
共享环境：项目根目录、.env 加载、Supabase / SiliconFlow 与向量维度（与 Next 侧约定对齐）。
"""

from __future__ import annotations

import errno
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")

from dotenv import load_dotenv
from openai import OpenAI

try:
    import httpcore
    import httpx as _httpx
except ImportError:  # pragma: no cover - 测试环境可能无 httpx
    httpcore = None  # type: ignore[assignment,misc]
    _httpx = None  # type: ignore[assignment,misc]

REPO_ROOT = Path(__file__).resolve().parent.parent
for _name in (".env.local", ".env"):
    load_dotenv(REPO_ROOT / _name, override=False)


def pick_supabase_url() -> str:
    return (
        os.getenv("NEXT_PUBLIC_SUPABASE_URL", "").strip()
        or os.getenv("SUPABASE_URL", "").strip()
    )


def pick_supabase_service_key() -> str:
    raw = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        or os.getenv("SUPABASE_SERVICE_KEY", "").strip()
    )
    if raw.lower().startswith("bearer "):
        raw = raw[7:].strip()
    return raw


def expected_embedding_dim() -> int:
    raw = (os.getenv("EMBEDDING_DIM") or os.getenv("SILICONFLOW_EMBEDDING_DIM") or "").strip()
    if not raw:
        return 1024
    try:
        n = int(raw, 10)
        return n if n > 0 else 1024
    except ValueError:
        return 1024


def siliconflow_base() -> str:
    return os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1").rstrip("/")


DEFAULT_SILICONFLOW_EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"


def siliconflow_embedding_model() -> str:
    # 注意：CI/环境变量若显式设置为空字符串，os.getenv 会返回 ""，此时也应回退默认模型
    raw = os.getenv("SILICONFLOW_EMBEDDING_MODEL", "").strip()
    return raw or DEFAULT_SILICONFLOW_EMBEDDING_MODEL


def siliconflow_embedding_dimensions() -> int:
    return int(os.getenv("SILICONFLOW_EMBEDDING_DIMENSIONS", "1024"))


def must_siliconflow_api_key() -> str:
    k = os.getenv("SILICONFLOW_API_KEY", "").strip()
    if not k:
        raise RuntimeError("Missing required env: SILICONFLOW_API_KEY")
    return k


def openai_siliconflow_client() -> OpenAI:
    return OpenAI(api_key=must_siliconflow_api_key(), base_url=siliconflow_base())


def embedding_kwargs_for_inputs(texts: list[str]) -> dict:
    """OpenAI SDK embeddings.create 参数；Qwen3 须带 dimensions。"""
    model = siliconflow_embedding_model()
    kw: dict = {"model": model, "input": texts}
    if "Qwen3-Embedding" in model:
        kw["dimensions"] = siliconflow_embedding_dimensions()
    return kw


def supabase_client():
    from supabase import create_client

    url = pick_supabase_url()
    key = pick_supabase_service_key()
    if not url or not key:
        raise RuntimeError(
            "缺少 NEXT_PUBLIC_SUPABASE_URL 或 SUPABASE_URL，以及 "
            "SUPABASE_SERVICE_ROLE_KEY 或 SUPABASE_SERVICE_KEY"
        )
    return create_client(url, key)


def transient_supabase_network_error(exc: BaseException) -> bool:
    """判断是否为可重试的网络 / 连接层错误（PostgREST 经 httpx 常见 TCP 复位、超时等）。"""
    depth = 0
    e: BaseException | None = exc
    while e is not None and depth < 8:
        if _httpx is not None and isinstance(
            e,
            (_httpx.ConnectError, _httpx.TimeoutException, _httpx.NetworkError),
        ):
            return True
        if httpcore is not None and isinstance(
            e,
            (httpcore.ConnectError, httpcore.TimeoutException),
        ):
            return True
        if isinstance(e, OSError):
            en = e.errno
            if en is not None and en in (
                errno.ECONNRESET,
                errno.ECONNABORTED,
                errno.ETIMEDOUT,
                errno.EPIPE,
                errno.ECONNREFUSED,
            ):
                return True
            # 部分平台对「Connection reset by peer」使用非标准 errno（如 macOS 54）
            if en == 54:
                return True
        msg = (str(e) or "").lower()
        needles = (
            "connection reset",
            "connection aborted",
            "broken pipe",
            "remote protocol",
            "timed out",
            "timeout",
            "temporarily unavailable",
            "connection refused",
            "ssl",
            "tls",
            "readerror",
            "writeerror",
        )
        if any(n in msg for n in needles):
            return True
        nxt = getattr(e, "__cause__", None) or getattr(e, "__context__", None)
        if nxt is e:
            break
        e = nxt
        depth += 1
    return False


def _supabase_http_retry_params() -> tuple[int, float]:
    raw_r = (os.getenv("SUPABASE_HTTP_RETRIES") or os.getenv("SUPABASE_INSERT_RETRIES", "") or "").strip()
    try:
        retries = int(raw_r) if raw_r else 4
    except ValueError:
        retries = 4
    retries = max(1, min(retries, 12))
    raw_d = (
        os.getenv("SUPABASE_HTTP_RETRY_BASE_DELAY_S") or os.getenv("SUPABASE_INSERT_RETRY_BASE_DELAY_S", "") or ""
    ).strip()
    try:
        delay_base = float(raw_d) if raw_d else 0.25
    except ValueError:
        delay_base = 0.25
    delay_base = max(0.05, min(delay_base, 5.0))
    return retries, delay_base


def supabase_execute_with_retry(fn: Callable[[], T]) -> T:
    """对任意同步 Supabase（PostgREST）调用做有限次重试；每次调用 fn() 内宜新建 client。"""
    from .chatbi_circuit_breaker import execute_with_circuit_breaker

    return execute_with_circuit_breaker("supabase", lambda: _supabase_execute_with_retry_inner(fn))


def _supabase_execute_with_retry_inner(fn: Callable[[], T]) -> T:
    retries, delay_base = _supabase_http_retry_params()
    last: BaseException | None = None
    for attempt in range(retries):
        try:
            return fn()
        except BaseException as exc:
            last = exc
            if attempt >= retries - 1 or not transient_supabase_network_error(exc):
                raise
            time.sleep(min(3.0, delay_base * (2**attempt)))
    raise RuntimeError("supabase_execute_with_retry: exhausted") from last


def llm_execute_with_circuit_breaker(fn: Callable[[], T]) -> T:
    """LLM / Embedding 外呼熔断包装。"""
    from .chatbi_circuit_breaker import execute_with_circuit_breaker

    return execute_with_circuit_breaker("llm", fn)


def supabase_table_insert_with_retry(table: str, row: dict[str, Any]) -> None:
    """对单条 insert 做有限次重试；每次新建 client，减轻半开连接复用导致的复位问题。"""

    def _once() -> None:
        supabase_client().table(table).insert(row).execute()

    supabase_execute_with_retry(_once)


def content_default_year() -> int:
    raw = (os.getenv("CONTENT_DEFAULT_YEAR") or "2026").strip()
    try:
        n = int(raw, 10)
        return n if n > 0 else 2026
    except ValueError:
        return 2026


DEFAULT_SILICONFLOW_CHAT_MODEL = "deepseek-ai/DeepSeek-V4-Pro"


def siliconflow_chat_model() -> str:
    raw = os.getenv("SILICONFLOW_CHAT_MODEL", DEFAULT_SILICONFLOW_CHAT_MODEL).strip()
    return raw or DEFAULT_SILICONFLOW_CHAT_MODEL


def max_x_sources_header_chars() -> int:
    raw = (os.getenv("MAX_X_SOURCES_HEADER_CHARS") or "6000").strip()
    try:
        n = int(raw, 10)
        return n if n > 0 else 6000
    except ValueError:
        return 6000


def rag_debug_enabled() -> bool:
    v = (os.getenv("DEBUG_RAG") or os.getenv("RAG_DEBUG") or "").strip().lower()
    if v in ("1", "true", "yes", "on"):
        return True
    return os.getenv("NODE_ENV", "").strip().lower() == "development"


def api_key_optional() -> str | None:
    return (os.getenv("API_KEY") or "").strip() or None


def siliconflow_api_key_optional() -> str:
    return os.getenv("SILICONFLOW_API_KEY", "").strip()


def admin_secret() -> str | None:
    """admin/sync 等 Bearer 校验用 secret。

    真值：`SYNC_ADMIN_SECRET`（与前端 BFF `forwardToPyAdmin` 同值）。
    `CHAT_API_SECRET` / `NEXT_PUBLIC_ADMIN_SECRET` 已废弃，后续版本将移除读取逻辑。
    """
    sync = (os.getenv("SYNC_ADMIN_SECRET") or "").strip()
    if sync:
        return sync
    # deprecated · 待删
    chat = (os.getenv("CHAT_API_SECRET") or "").strip()
    if chat:
        return chat
    # deprecated · 待删
    legacy = (os.getenv("NEXT_PUBLIC_ADMIN_SECRET") or "").strip()
    if legacy:
        return legacy
    return None

