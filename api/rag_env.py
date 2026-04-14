"""
共享环境：项目根目录、.env 加载、Supabase / SiliconFlow 与向量维度（与 Next 侧约定对齐）。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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


def siliconflow_embedding_model() -> str:
    # 注意：CI/环境变量若显式设置为空字符串，os.getenv 会返回 ""，此时也应回退默认模型
    raw = os.getenv("SILICONFLOW_EMBEDDING_MODEL", "").strip()
    return raw or "Qwen/Qwen3-Embedding-0.6B"


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


def admin_secret() -> str | None:
    return (
        os.getenv("NEXT_PUBLIC_ADMIN_SECRET") or os.getenv("CHAT_API_SECRET") or ""
    ).strip() or None

