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

## V3 P1-4（2026-05-13）· 低置信澄清短路（`agent.clarify`）

当 `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` 且 Unified Agent 判定「SQL 候选 + 低置信」时，`api/agent.py` 在首轮 `text2sql_execute` 之前短路并下发 `agent.clarify`；`CHATBI_JSON_LOG=1` 时额外输出 `message=agent_clarify_short_circuit`（`run_id` 与 SSE `meta` 同源）。JSON 与 SSE 批量 replay 路径由 `api/unified_chat.py` 与 emit 增量路径对齐补帧。
