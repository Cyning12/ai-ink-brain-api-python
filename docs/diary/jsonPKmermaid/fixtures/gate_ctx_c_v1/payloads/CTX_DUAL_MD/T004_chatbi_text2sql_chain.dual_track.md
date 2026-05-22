---
schema: gate_ctx_c_dual_md_main_v1
arm: CTX_DUAL_MD
task_id: T004_chatbi_text2sql_chain
freeze_id: TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0
---

<!-- gate_ctx_c dual_track role=ai path=docs/_tech_graph/11_flow_text2sql.ai.md -->
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

---
<!-- gate_ctx_c dual_track role=human path=docs/_tech_graph/11_flow_text2sql.md -->
```mermaid
flowchart TD
    %% Entry: /api/py/text2sql/chat | unified router → text2sql

    %% Query 阶段
    IN[入口 Query] --> AUTH[鉴权<br/>API_KEY / admin_secret]
    AUTH --> INT[Intent 判定<br/>is_text2sql_intent]

    INT -->|non_text2sql| OUT0[返回 non_text2sql 提示]

    %% Work 阶段
    INT -->|text2sql| RET[语料检索<br/>text2sql_store.search()]
    RET --> PROMPT[SQL Prompt 构建<br/>DDL + Examples]
    PROMPT --> GEN[LLM 生成 SQL]
    GEN --> VAL[SQL 校验<br/>仅 SELECT / WITH]
    VAL -->|err| OUT1[errors.generate_sql]

    %% 执行分支
    VAL -->|ok| EXEC[执行 SQL<br/>TEXT2SQL_DATABASE_URL]
    EXEC -->|env missing / db err| OUT1

    EXEC -->|单值数值| DET[确定性总结<br/>try_summarize_aggregate()]
    EXEC -->|多行| SUM[LLM 总结]
    EXEC -->|零行| OUT2[未查到数据]

    %% 输出
    DET --> OUT[返回 JSON<br/>answer / sql / rows / retrieved / errors]
    SUM --> OUT
    OUT1 --> OUT
    OUT2 --> OUT

    %% 依赖
    RET --> SPEC[> docs/text2sql/v1/sql/supabase_init.sql]

    %% 样式
    classDef query fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef work fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef out fill:#fff8e1,stroke:#ff6f00,stroke-width:2px
    classDef err fill:#ffebee,stroke:#b71c1c,stroke-width:1px

    class IN,Auth,INT query
    class RET,PROMPT,GEN,VAL,EXEC,DET,SUM work
    class OUT,OUT0 out
    class OUT1,OUT2 err
    class SPEC err
```

## 补充：ChatBI V2 多轮锚点（2026-05-09）

Unified Agent 路径下，成功执行 Text2SQL 后由 `api/unified_chat.py::_sync_persist_chatbi_v2_agent_log`（经 `_await_persist_chatbi_v2_agent_log`）在 `rag_conversation_logs.tool_results.text2sql_grounding` 写入 `primary_table` / `resolved_tables` / `sql_excerpt`（由 `api/text2sql_grounding.py` 从 SQL 解析）。次轮 `api/agent_memory.py::load` 合并进 `history[]`，经 `api/query_rewrite.py::history_to_rewrite_block` 与 `api/agent.py`（Intent 历史前缀）注入 Text2SQL 检索与生成。

## V3 P0（2026-05-11）· Agent `api/tools.text2sql_execute`

- **结构化**：`ToolResult.data.text2sql_phases_ms`（`retrieve` / `llm_sql` / `validate` / `db` / `llm_summary`，已执行阶段为整数 ms；聚合快路径跳过 `llm_summary` 时不写入该键）。
- **增量 SSE**（`chain_emit` 有值时）：`text2sql.phase.start` / `text2sql.phase.end`，`step_id` 与 `payload.subphase_id` 形如 `text2sql.phase.<phase_id>`；契约见 `docs/_tech_graph/_contract_manifest.json`。
- **超时**：`CHATBI_TEXT2SQL_LLM_SQL_TIMEOUT_S` / `CHATBI_TEXT2SQL_LLM_SUMMARY_TIMEOUT_S` → 回退 `CHATBI_TEXT2SQL_LLM_TIMEOUT_S` → 默认 `120` 秒；`asyncio.wait_for` 包裹 LLM 线程调用。
- **总结模型**：`CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL` 未设时与 `INTENT_LLM_MODEL` 默认一致。
- **对话块预算**：`TEXT2SQL_DIALOGUE_CONTEXT_MAX_LEN`（默认 8000）截断 `history_to_rewrite_block` 再注入 `build_sql_prompt`。
- **P0-3 结构预取（2026-05-12）**：当用户问题含 **INSERT/UPDATE 类语义** 且向量检索 DDL **列锚点不足** 时，在调用 LLM 生成 SQL 之前执行 **只读** `information_schema.columns` 预取（与 `chatbi_sql_table_policy` 可见写权限对齐），将列清单注入 `build_sql_prompt`；失败返回 `TEXT2SQL_SCHEMA_PREFETCH_FAILED`，不盲写。环境变量：`TEXT2SQL_SCHEMA_PREFETCH`（默认随 `TEXT2SQL_DATABASE_URL` 启用）、`TEXT2SQL_SCHEMA_PREFETCH_TIMEOUT_MS`、`TEXT2SQL_SCHEMA_PREFETCH_MAX_ROWS`。协议版图见 `11_flow_text2sql.ai.md`（`PF` 节点）。

## V3 P1-1（2026-05-14）· Text2SQL 后闸 SQL AST 硬化

- **实现**：`api/chatbi_sql_gate.py` 中 `apply_chatbi_sql_gate`：**AST（sqlparse）→ 表策略 `chatbi_sql_table_policy`（min_* / 无行拒绝）→ 档位与 L2 收窄**；`CHATBI_JSON_LOG=1` 时 `sql_gate_deny` 可含 **`ast_rule_id`**。  
- **单测**：`tests/test_chatbi_sql_ast_gate_v1.py`（负例 / 正例 / 阶段顺序 / JSON 字段）。  
- **子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§2.1**；任务：`docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（已归档）。

## V3 P1-4（2026-05-13）· 低置信澄清短路（`agent.clarify`）

当 `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` 且 Unified Agent 判定「SQL 候选 + 低置信」时，`api/agent.py` 在首轮 `text2sql_execute` 之前短路并下发 `agent.clarify`；`CHATBI_JSON_LOG=1` 时额外输出 `message=agent_clarify_short_circuit`（`run_id` 与 SSE `meta` 同源）。JSON 与 SSE 批量 replay 路径由 `api/unified_chat.py` 与 emit 增量路径对齐补帧。

