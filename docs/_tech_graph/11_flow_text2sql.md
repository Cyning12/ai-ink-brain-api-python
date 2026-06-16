---
graph_id: 11_flow_text2sql
version: 2026-06-16
generated_at: 2026-06-16T12:08:13Z
source: docs/_tech_graph/11_flow_text2sql.graph.yaml
---

# Text2SQL 子流程

Text2SQL 意图判定、schema 预取、SQL 生成/校验/执行/总结流程

## Mermaid

```mermaid
flowchart TD
    INT[Intent Check]
    OUT0[返回 non_text2sql 提示]
    RET[text2sql_store.search()]
    PF[run_text2sql_schema_prefetch_sync]
    ERR_PF[>TEXT2SQL_SCHEMA_PREFETCH_FAILED]
    PROMPT[build_sql_prompt()]
    GEN[async def llm_generate_sql]
    VAL[validate_sql_readonly()]
    EXEC[execute_select_sql()]
    ERR_VALIDATE[>validate_sql_readonly err]
    ERR_EXEC[>execute_select_sql err]
    ERR_DSN[>Missing env]
    DET[try_summarize_aggregate()]
    SUM[async def llm_summarize]
    OUT2[未查到数据]
    OUT1[errors.generate_sql]
    SPEC[>docs/text2sql/v1/sql/supabase_init.sql]

    IN --> AUTH
    // → api/index.py::_require_auth
    AUTH --"[ok]"--> INT
    AUTH --"[err]"--> ERR_AUTH
    // → api/intent_router.py::is_text2sql_intent
    // → api/intent_router.py::decide_intent
    INT --"[non_text2sql]"--> OUT0
    INT --"[text2sql]"--> RET
    // → api/text2sql_store.py
    RET --> PF
    // → api/text2sql_schema_prefetch.py
    RET --"依赖语料"--> SPEC
    PF --"[ok|skip]"--> PROMPT
    PF --"[err]"--> ERR_PF
    ERR_PF --> OUT1
    PROMPT --> GEN
    // → api/text2sql_core.py
    GEN --"~>"--> VAL
    // → api/text2sql_core.py::validate_sql_readonly
    VAL --"[ok]"--> EXEC
    VAL --"[err]"--> ERR_VALIDATE
    // → api/text2sql_core.py::validate_sql_readonly
    ERR_VALIDATE --> OUT1
    EXEC --"~>"--> DB
    // → api/text2sql_core.py::execute_select_sql
    EXEC --"[err]"--> ERR_EXEC
    // → api/text2sql_core.py::execute_select_sql
    ERR_EXEC --> OUT1
    DB --"TEXT2SQL_DATABASE_URL missing"--> ERR_DSN
    // → api/text2sql_core.py#L88
    ERR_DSN --> OUT1
    DB --"rows==1&1 numeric"--> DET
    DB --"rows>0"--> SUM
    DB --"rows==0"--> OUT2
    DET --> OUT
    SUM --"~>"--> OUT
    OUT1 --> OUT
    OUT2 --> OUT
    OUT --"::archives"--> LOG
    // → api/database_manager.py::save_debug_log

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| INT | Intent Check |  |
| OUT0 | 返回 non_text2sql 提示 |  |
| RET | text2sql_store.search() |  |
| PF | run_text2sql_schema_prefetch_sync |  |
| ERR_PF | >TEXT2SQL_SCHEMA_PREFETCH_FAILED |  |
| PROMPT | build_sql_prompt() |  |
| GEN | async def llm_generate_sql |  |
| VAL | validate_sql_readonly() |  |
| EXEC | execute_select_sql() |  |
| ERR_VALIDATE | >validate_sql_readonly err |  |
| ERR_EXEC | >execute_select_sql err |  |
| ERR_DSN | >Missing env |  |
| DET | try_summarize_aggregate() |  |
| SUM | async def llm_summarize |  |
| OUT2 | 未查到数据 |  |
| OUT1 | errors.generate_sql |  |
| SPEC | >docs/text2sql/v1/sql/supabase_init.sql |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| IN | AUTH | -> | depends_on |  | 1 anchor(s) |
| AUTH | INT | [ok] | depends_on |  |  |
| AUTH | ERR_AUTH | [err] | depends_on |  | 2 anchor(s) |
| INT | OUT0 | [non_text2sql] | depends_on |  |  |
| INT | RET | [text2sql] | depends_on |  | 1 anchor(s) |
| RET | PF | -> | depends_on |  | 1 anchor(s) |
| RET | SPEC | -> | depends_on | 依赖语料 |  |
| PF | PROMPT | -> | condition | [ok\|skip] |  |
| PF | ERR_PF | -> | condition | [err] |  |
| ERR_PF | OUT1 | -> | depends_on |  |  |
| PROMPT | GEN | -> | depends_on |  | 1 anchor(s) |
| GEN | VAL | ~> | async_calls |  | 1 anchor(s) |
| VAL | EXEC | [ok] | depends_on |  |  |
| VAL | ERR_VALIDATE | [err] | depends_on |  | 1 anchor(s) |
| ERR_VALIDATE | OUT1 | -> | depends_on |  |  |
| EXEC | DB | ~> | async_calls |  | 1 anchor(s) |
| EXEC | ERR_EXEC | [err] | depends_on |  | 1 anchor(s) |
| ERR_EXEC | OUT1 | -> | depends_on |  |  |
| DB | ERR_DSN | -> | depends_on | TEXT2SQL_DATABASE_URL missing | 1 anchor(s) |
| ERR_DSN | OUT1 | -> | depends_on |  |  |
| DB | DET | -> | depends_on | rows==1&1 numeric |  |
| DB | SUM | -> | depends_on | rows>0 |  |
| DB | OUT2 | -> | depends_on | rows==0 |  |
| DET | OUT | -> | depends_on |  |  |
| SUM | OUT | ~> | async_calls |  |  |
| OUT1 | OUT | -> | depends_on |  |  |
| OUT2 | OUT | -> | depends_on |  |  |
| OUT | LOG | ::archives | archives |  | 1 anchor(s) |

## Notes

### ChatBI V2 多轮锚点

Unified Agent 路径下，成功执行 Text2SQL 后由 `api/unified_chat.py::_sync_persist_chatbi_v2_agent_log` 在 `rag_conversation_logs.tool_results.text2sql_grounding` 写入 `primary_table` / `resolved_tables` / `sql_excerpt`；次轮 `api/agent_memory.py::load` 合并进 `history[]`。

### V3 P0 · Schema 预取

当用户问题含 INSERT/UPDATE 类语义且向量检索 DDL 列锚点不足时，在 LLM 生成 SQL 之前执行只读 `information_schema.columns` 预取（与 `chatbi_sql_table_policy` 可见写权限对齐），将列清单注入 `build_sql_prompt`；失败返回 `TEXT2SQL_SCHEMA_PREFETCH_FAILED`。

相关环境变量：
- `TEXT2SQL_DIALOGUE_CONTEXT_MAX_LEN`（默认 8000）截断历史注入 prompt
- `TEXT2SQL_SCHEMA_PREFETCH_TIMEOUT_MS`
- `TEXT2SQL_SCHEMA_PREFETCH_MAX_ROWS`

### V3 P1-1 · SQL AST 硬化

`api/chatbi_sql_gate.py::apply_chatbi_sql_gate` 使用 AST（sqlparse）→ 表策略 `chatbi_sql_table_policy`（min_* / 无行拒绝）→ 档位与 L2 收窄。

