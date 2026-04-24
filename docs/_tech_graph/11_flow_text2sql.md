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

    %% 执行分支
    VAL -->|ok| EXEC[执行 SQL<br/>TEXT2SQL_DATABASE_URL]
    VAL -->|fail| OUT1[errors.generate_sql]

    EXEC -->|单值数值| DET[确定性总结<br/>_try_summarize_aggregate()]
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
