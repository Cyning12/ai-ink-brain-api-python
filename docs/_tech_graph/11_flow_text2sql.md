```mermaid
flowchart TD
  %% Entry: /api/py/text2sql/chat | unified router → text2sql

  IN[入口 Query] --> AUTH[鉴权<br/>API_KEY / admin_secret]
  AUTH --> INT[Intent Check<br/>is_text2sql_intent OR unified decide_intent]

  INT -->|non_text2sql| OUT0[返回 non_text2sql 提示]

  INT -->|text2sql| RET[Retrieve Corpus<br/>text2sql_store.search()]
  RET --> PROMPT[build_sql_prompt()<br/>DDL + Examples]
  PROMPT --> GEN[LLM generate SQL]
  GEN --> VAL[validate_sql_readonly()<br/>仅 SELECT/WITH]

  VAL -->|ok| EXEC[execute_select_sql()<br/>TEXT2SQL_DATABASE_URL]
  VAL -->|fail| OUT1[errors.generate_sql]

  EXEC -->|rows==1&1 numeric| DET[_try_summarize_aggregate()<br/>确定性总结]
  EXEC -->|rows>0| SUM[LLM summarize]
  EXEC -->|rows==0| OUT2[未查到数据]

  DET --> OUT[返回 JSON: answer/sql/rows/retrieved/errors]
  SUM --> OUT
  OUT1 --> OUT
  OUT2 --> OUT

  %% on-demand linking
  RET --> SPEC[依赖语料: docs/text2sql/v1/sql/supabase_init.sql]
```

