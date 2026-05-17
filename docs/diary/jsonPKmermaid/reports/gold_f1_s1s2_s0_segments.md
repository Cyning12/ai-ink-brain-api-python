# gate_ctx_ab gold F1 — jsonl

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/0.667/0.800 | 0.286/0.400/0.333 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.750/1.000/0.857 | 0.333/0.400/0.364 |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.333/0.500 | 0.143/0.167/0.154 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.250/0.500/0.333 |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.222/0.333/0.267 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/0.833/0.909 | 0.625/0.833/0.714 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_JSON` | 1 | 0.800 | 0.333 |
| `T001_embedding_dim_default` | `CTX_MERMAID` | 1 | 0.857 | 0.364 |
| `T002_unified_sse_chain_contract` | `CTX_JSON` | 1 | 0.500 | 0.154 |
| `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1 | 1.000 | 0.333 |
| `T003_ingest_admin_rpc` | `CTX_JSON` | 1 | 0.909 | 0.267 |
| `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1 | 0.909 | 0.714 |
