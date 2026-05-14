```mermaid
flowchart TD
  %% Entry: /api/py/text2sql/chat | unified router → text2sql
  %% 拓扑协议 v2-Python 适配

  %% === Query 阶段 ===
  IN[[入口 Query]] --"->"--> AUTH[[鉴权]]
  // → api/index.py::_require_auth
  // → api/index.py::unified_chat_route Depends(require_chatbi_principal)

  AUTH --"[ok]"--> INT[[Intent Check]]
  AUTH --"[err]"--> ERR_AUTH[>Auth Failed]
  // → api/intent_router.py::is_text2sql_intent
  // → api/intent_router.py::decide_intent

  INT --"[non_text2sql]"--> OUT0[[返回 non_text2sql 提示]]

  %% === Work 阶段 ===
  INT --"[text2sql]"--> RET[[text2sql_store.search()]]
  // → api/text2sql_store.py

  RET --"->"--> PF[[run_text2sql_schema_prefetch_sync]]
  // → api/text2sql_schema_prefetch.py

  PF --"?>[ok|skip]"--> PROMPT[[build_sql_prompt()]]
  PF --"?>[err]"--> ERR_PF[>TEXT2SQL_SCHEMA_PREFETCH_FAILED]
  // → api/tools.py::text2sql_execute / api/unified_chat.py

  ERR_PF --"->"--> OUT1[[errors.generate_sql]]

  PROMPT --"->"--> GEN[[async def llm_generate_sql]]
  // → api/text2sql_core.py

  GEN --"~>"--> VAL[[validate_sql_readonly()]]
  // → api/text2sql_core.py::validate_sql_readonly

  %% === 执行分支 ===
  VAL --"[ok]"--> EXEC[[execute_select_sql()]]
  VAL --"[err]"--> ERR_VALIDATE[>validate_sql_readonly err]
  // → api/text2sql_core.py::validate_sql_readonly
  ERR_VALIDATE --"->"--> OUT1[[errors.generate_sql]]

  EXEC --"~>"--> DB[(DB: TEXT2SQL_DATABASE_URL)]
  // → api/text2sql_core.py::execute_select_sql

  EXEC --"[err]"--> ERR_EXEC[>execute_select_sql err]
  // → api/text2sql_core.py::execute_select_sql
  ERR_EXEC --"->"--> OUT1

  DB --"TEXT2SQL_DATABASE_URL missing"--> ERR_DSN[>Missing env]
  // → api/text2sql_core.py#L88
  ERR_DSN --"->"--> OUT1

  DB --"rows==1&1 numeric"--> DET[[try_summarize_aggregate()]]
  DB --"rows>0"--> SUM[[async def llm_summarize]]
  DB --"rows==0"--> OUT2[[未查到数据]]

  %% === Summarize 阶段 ===
  DET --"->"--> OUT[[返回 JSON]]
  SUM --"~>"--> OUT
  OUT1 --"->"--> OUT
  OUT2 --"->"--> OUT

  OUT --"::archives"--> LOG[(DB: rag_conversation_logs)]
  // → api/database_manager.py::save_debug_log

  %% === 依赖锚点 ===
  RET --"依赖语料"--> SPEC[>docs/text2sql/v1/sql/supabase_init.sql]

  %% === 样式 ===
  classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef fn fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef data fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px;
  classDef milestone fill:#fff8e1,stroke:#e65100,stroke-width:2px;
  classDef err fill:#ffebee,stroke:#b71c1c,stroke-width:1px;

  class IN,AUTH,INT,RET,PF,PROMPT,GEN,VAL,EXEC,DET,SUM,OUT,OUT0,OUT1,OUT2 phase
  class DB,LOG data
  class SPEC milestone
  class ERR_AUTH,OUT1,ERR_PF,ERR_VALIDATE,ERR_EXEC,ERR_DSN err
```

**V2 多轮锚点（2026-05-09）**：`tool_results.text2sql_grounding` → `agent_memory.load` → `history_to_rewrite_block` / Intent assistant 前缀；实现见 `api/text2sql_grounding.py`、`api/unified_chat.py::_text2sql_grounding_from_agent_result`。

**V3 P0 Agent（2026-05-11）**：`api/tools.text2sql_execute` 产出 `text2sql_phases_ms`、可选增量 `text2sql.phase.start|end`（`api/agent.py` 注入 `chain_emit`）、LLM 分阶段 `wait_for` 超时；**P0-2**：`CHATBI_JSON_LOG` → `api/chatbi_json_log.py` 单行 JSON（与 SSE **`run_id`** 同源）；人类版说明见同目录 `11_flow_text2sql.md` §V3 P0。

**V3 P0-3 结构预取（2026-05-12）**：写入/更新意图且检索 DDL 列锚点不足时，`run_text2sql_schema_prefetch_sync` 只读查询 `information_schema.columns`（`TEXT2SQL_SCHEMA_PREFETCH` 可关），结果注入 `build_sql_prompt`；失败码 `TEXT2SQL_SCHEMA_PREFETCH_FAILED`；SSE `text2sql.phase.schema_prefetch` / `tool`=`text2sql.schema_prefetch`；见 `api/text2sql_schema_prefetch.py`。

**V3 P1-1（2026-05-14）· SQL 后闸 AST**：`api/chatbi_sql_gate.apply_chatbi_sql_gate`：**AST（sqlparse）→ 表策略 → 档位/L2**；`sql_gate_deny` 可带 `ast_rule_id`；单测 `tests/test_chatbi_sql_ast_gate_v1.py`；人类版 `11_flow_text2sql.md` §V3 P1-1。

**V3 P1-4 澄清短路（2026-05-13）**：`CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` 时 `api/agent.py` 在首轮 `text2sql_execute` 前可短路并下发 `agent.clarify`；`CHATBI_JSON_LOG` 行 `agent_clarify_short_circuit`；JSON/SSE 批量路径补帧见 `api/unified_chat.py::_clarify_short_circuit_events`；人类版 `11_flow_text2sql.md` §V3 P1-4。
