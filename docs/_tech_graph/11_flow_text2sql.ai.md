```mermaid
flowchart TD
  %% Entry: /api/py/text2sql/chat | unified router → text2sql
  %% 拓扑协议 v2-Python 适配

  %% === Query 阶段 ===
  IN[[入口 Query]] --"->"--> AUTH[[鉴权]]
  // → api/index.py

  AUTH --"[ok]"--> INT[[Intent Check]]
  AUTH --"[err]"--> ERR_AUTH[>Auth Failed]
  // → api/intent_router.py::is_text2sql_intent
  // → api/intent_router.py::decide_intent

  INT --"[non_text2sql]"--> OUT0[[返回 non_text2sql 提示]]

  %% === Work 阶段 ===
  INT --"[text2sql]"--> RET[[text2sql_store.search()]]
  // → api/text2sql_store.py

  RET --"->"--> PROMPT[[build_sql_prompt()]]
  // → api/text2sql_core.py

  PROMPT --"->"--> GEN[[async def llm_generate_sql]]
  // → api/text2sql_core.py

  GEN --"~>"--> VAL[[validate_sql_readonly()]]
  // → api/text2sql_core.py

  %% === 执行分支 ===
  VAL --"[ok]"--> EXEC[[execute_select_sql()]]
  VAL --"[fail]"--> OUT1[[errors.generate_sql]]
  // → api/text2sql_core.py

  EXEC --"~>"--> DB[(DB: TEXT2SQL_DATABASE_URL)]

  DB --"rows==1&1 numeric"--> DET[[_try_summarize_aggregate()]]
  DB --"rows>0"--> SUM[[async def llm_summarize]]
  DB --"rows==0"--> OUT2[[未查到数据]]

  %% === Summarize 阶段 ===
  DET --"->"--> OUT[[返回 JSON]]
  SUM --"~>"--> OUT
  OUT1 --"->"--> OUT
  OUT2 --"->"--> OUT

  OUT --"::archives"--> LOG[(DB: text2sql_logs)]

  %% === 依赖锚点 ===
  RET --"依赖语料"--> SPEC[>docs/text2sql/v1/sql/supabase_init.sql]

  %% === 样式 ===
  classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef fn fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef data fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px;
  classDef milestone fill:#fff8e1,stroke:#e65100,stroke-width:2px;
  classDef err fill:#ffebee,stroke:#b71c1c,stroke-width:1px;

  class IN,Auth,INT,RET,PROMPT,GEN,VAL,EXEC,DET,SUM,OUT,OUT0,OUT1,OUT2 phase
  class DB,LOG data
  class SPEC milestone
  class ERR_AUTH,OUT1 err
```
