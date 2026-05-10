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
