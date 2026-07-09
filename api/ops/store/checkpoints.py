"""Ops Desk Checkpoint 存储适配层（P1-2）。

复用 `ops_run_checkpoints` 表：
- `checkpoint_id` 字段存放 thread/session 标识。
- `state_json` 存放 ReAct 运行时状态。
"""

from __future__ import annotations

import logging
from typing import Any

from api.ops.store.runs import OpsRunStore
from api.rag_env import supabase_client

logger = logging.getLogger(__name__)


class CheckpointStoreError(RuntimeError):
    """Checkpoint 读写或校验失败。"""


REQUIRED_STATE_KEYS = ("route", "query", "step", "messages", "tool_evidence")


def _validate_react_state(state_json: Any) -> dict[str, Any]:
    """校验 checkpoint 状态是否足够恢复 ReAct 循环。

    校验通过返回原字典；失败抛出 CheckpointStoreError。
    """
    if not isinstance(state_json, dict):
        raise CheckpointStoreError("checkpoint state_json is not a dict")
    missing = [k for k in REQUIRED_STATE_KEYS if k not in state_json]
    if missing:
        raise CheckpointStoreError(f"checkpoint state missing keys: {missing}")
    if state_json.get("route") != "react":
        raise CheckpointStoreError("checkpoint route is not 'react'")
    if not isinstance(state_json.get("messages"), list):
        raise CheckpointStoreError("checkpoint state messages is not a list")
    if not isinstance(state_json.get("step"), int):
        raise CheckpointStoreError("checkpoint state step is not an int")
    return state_json


def save_checkpoint(
    run_id: str,
    thread_id: str,
    state_json: dict[str, Any],
    store: OpsRunStore | None = None,
) -> dict[str, Any]:
    """保存 ReAct 运行时 checkpoint。

    参数:
        run_id: 当前 run id。
        thread_id: session/thread 标识；与 `checkpoint_id` 同义。
        state_json: 运行状态字典。
        store: 可选 OpsRunStore；默认使用全局 supabase_client() 构造。
    """
    target = store if store is not None else OpsRunStore(supabase_client())
    if not hasattr(target, "save_checkpoint"):
        raise CheckpointStoreError("store does not support save_checkpoint")
    return target.save_checkpoint(run_id, thread_id, state_json)


def find_latest_checkpoint_for_session(
    session_id: str,
    store: OpsRunStore | None = None,
) -> dict[str, Any] | None:
    """按 session_id 查找最新的有效 checkpoint（跨 run）。

    返回整行（含 run_id / checkpoint_id / state_json / created_at）；
    不存在时返回 None。
    """
    target = store if store is not None else OpsRunStore(supabase_client())
    # 防御：部分测试 double 未实现 checkpoint 方法时直接返回 None
    if not hasattr(target, "find_latest_checkpoint_for_session"):
        return None
    return target.find_latest_checkpoint_for_session(session_id)


def load_checkpoint(
    run_id: str,
    thread_id: str,
    store: OpsRunStore | None = None,
) -> dict[str, Any] | None:
    """读取指定 run + thread 的 checkpoint。

    返回状态字典；不存在时返回 None。
    注意：返回前不做结构校验，由调用方 `resume_react_state` 处理。
    """
    target = store if store is not None else OpsRunStore(supabase_client())
    if not hasattr(target, "load_checkpoint"):
        return None
    row = target.load_checkpoint(run_id, thread_id)
    if not row:
        return None
    return row.get("state_json")