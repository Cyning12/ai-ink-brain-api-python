"""
pytest 全局夹具：在任意 `api.*` 导入（进而 `rag_env.load_dotenv(override=False)`）之前固定 Intent 评测开关。

背景：shell 里 `unset CHATBI_V2_INTENT_*` 无法撤销已在进程内由 dotenv 从 `.env` 注入的变量；
若 `.env` 中打开 `CHATBI_V2_INTENT_EVAL` / `CHATBI_V2_INTENT_LLM`，默认全量 `pytest tests` 会跑
`test_intent_agent_accuracy_smoke` 或 stub 路径仍误走真实 LLM，表现为「L0 卡死数分钟」。

保留显式评测：设置 `CHATBI_PYTEST_KEEP_INTENT_ENV=1`（或 `true`）后不再覆盖，便于
`pytest -m intent_eval` 等沿用 `.env`。
"""

from __future__ import annotations

import os

_KEEP = (os.getenv("CHATBI_PYTEST_KEEP_INTENT_ENV") or "").strip().lower() in ("1", "true", "yes", "on")

if not _KEEP:
    # 先于 dotenv 写入，使 `load_dotenv(..., override=False)` 无法把 .env 里的 true 盖进来
    os.environ["CHATBI_V2_INTENT_EVAL"] = "false"
    os.environ["CHATBI_V2_INTENT_BENCH_RUN"] = "false"
    os.environ["CHATBI_V2_INTENT_LLM"] = "false"
    # P1-4：避免 shell/.env 误开 clarify 导致未 monkeypatch 的 v2 agent 用例短路（仍可由单测 setenv 覆盖）
    os.environ["CHATBI_V3_LOW_CONFIDENCE_CLARIFY"] = ""
    # v3 低置信澄清/预览：固定 spec 默认 0.6，避免开发者 .env 降低阈值（如 0.3）使
    # confidence=0.35 的 stub 意图无法触发 clarify（见 task B-8 / test_unified_chat_backend_v2_agent）
    os.environ["INTENT_MIN_CONFIDENCE"] = "0.6"


import pytest


@pytest.fixture(autouse=True)
def _reset_chatbi_circuit_breakers_for_isolation():
    """单测间隔离全局 supabase/llm 熔断器状态，避免顺序依赖。"""
    try:
        from api.chatbi_circuit_breaker import reset_all_circuit_breakers_for_tests

        reset_all_circuit_breakers_for_tests()
    except Exception:  # noqa: BLE001
        pass
    yield
    try:
        from api.chatbi_circuit_breaker import reset_all_circuit_breakers_for_tests

        reset_all_circuit_breakers_for_tests()
    except Exception:  # noqa: BLE001
        pass
