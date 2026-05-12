"""加载 `chatbi_sql_table_policy`（表级 min_* 等级）。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from .rag_env import supabase_client


@dataclass(frozen=True)
class ChatBiTablePolicyRow:
    schema_name: str
    table_name: str
    min_select_level: int | None
    min_insert_level: int | None
    min_update_level: int | None
    min_delete_level: int | None
    owner_column: str


def _row_from_dict(r: dict[str, Any]) -> ChatBiTablePolicyRow | None:
    try:
        sn = str(r.get("schema_name") or "public").strip() or "public"
        tn = str(r.get("table_name") or "").strip()
        if not tn:
            return None

        def _i(v: Any) -> int | None:
            if v is None:
                return None
            try:
                x = int(v)
            except Exception:  # noqa: BLE001
                return None
            if x < 0 or x > 2:
                return None
            return x

        oc = str(r.get("owner_column") or "user_id").strip() or "user_id"
        return ChatBiTablePolicyRow(
            schema_name=sn,
            table_name=tn,
            min_select_level=_i(r.get("min_select_level")),
            min_insert_level=_i(r.get("min_insert_level")),
            min_update_level=_i(r.get("min_update_level")),
            min_delete_level=_i(r.get("min_delete_level")),
            owner_column=oc,
        )
    except Exception:  # noqa: BLE001
        return None


def load_chatbi_table_policies_sync() -> dict[tuple[str, str], ChatBiTablePolicyRow]:
    """返回 (schema, table) → 策略行；拉取失败或表不存在时返回空 dict（闸门侧可降级日志）。"""
    try:
        sb = supabase_client()
        res = sb.table("chatbi_sql_table_policy").select("*").limit(500).execute()
        rows = getattr(res, "data", None) or []
    except Exception:  # noqa: BLE001
        return {}
    out: dict[tuple[str, str], ChatBiTablePolicyRow] = {}
    for raw in rows:
        if not isinstance(raw, dict):
            continue
        pr = _row_from_dict(raw)
        if pr is None:
            continue
        out[(pr.schema_name, pr.table_name)] = pr
    if not out and (os.getenv("CHATBI_POLICY_DEBUG", "") or "").strip().lower() in ("1", "true", "yes", "on"):
        # 仅占位：避免生产刷屏
        pass
    return out


def allowed_op(*, access_level: int, min_level: int | None) -> bool:
    """NULL → 全员禁止；否则当且仅当 access_level <= min_level。"""
    if min_level is None:
        return False
    return access_level <= min_level
