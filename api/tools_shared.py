from __future__ import annotations

import os
import time
from typing import Any


def _elapsed_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _pick_chat_model() -> str:
    return os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")


def _pick_embed_model_kwargs() -> dict[str, Any]:
    # 统一由 embedding_kwargs_for_inputs 处理维度参数等
    return {}


def _sql_error_code_from_message(msg: str) -> str:
    m = (msg or "").lower()
    # 粗粒度映射：足够满足 gating/fallback 行为（CI 不应强依赖文案精确命中）
    if "syntax" in m or "parse" in m or "token" in m:
        return "SQL_GEN_SYNTAX"
    if "does not exist" in m or "relation" in m or "undefined table" in m or "表" in msg:
        return "SQL_EXEC_TABLE_NOT_FOUND"
    if "row-level security" in m or "violates row-level security" in m:
        return "SQL_EXEC_PERMISSION_DENIED"
    if "permission" in m or "denied" in m or "权限" in msg:
        return "SQL_EXEC_PERMISSION_DENIED"
    if "no data" in m or "empty" in m:
        return "SQL_EXEC_NO_DATA"
    return "UNKNOWN"


def _sql_exec_user_facing_error(raw: str, *, code: str) -> str:
    """DB 执行层错误：对用户可见的短中文（与 agent FailureTypeHandler 终态一致）。"""
    if code == "SQL_EXEC_PERMISSION_DENIED":
        return "数据库拒绝执行该语句：当前连接账号无足够权限，或触发了行级安全策略（RLS）。请联系管理员配置 GRANT / RLS policy。"
    return (raw or "").strip()


def _rag_should_treat_as_uncertain(answer: str) -> bool:
    a = (answer or "").strip()
    if not a:
        return True
    # 与 V1 行为一致：当模型明确表达“不确定/无法回答”，可按不确定失败处理
    lowered = a.lower()
    return "不确定" in lowered or "无法" in lowered or "暂时无法" in lowered


def _safe_snippet(text: str, *, max_len: int) -> str:
    t = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    return t[:max_len] if len(t) > max_len else t
