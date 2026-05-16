# gate_ctx_ab gold F1 — docs/diary/jsonPKmermaid/runs

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 0.600/1.000/0.750 | 0.375/0.600/0.462 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.500/1.000/0.667 | 0.286/0.400/0.333 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/0.667/0.800 | 0.333/0.400/0.364 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.500/1.000/0.667 | 0.286/0.400/0.333 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/0.667/0.800 | 0.333/0.400/0.364 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.750/1.000/0.857 | 0.167/0.200/0.182 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/1.000/1.000 | 0.333/0.400/0.364 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.750/1.000/0.857 | 0.333/0.400/0.364 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/0.667/0.800 | 0.333/0.400/0.364 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.500/1.000/0.667 | 0.333/0.600/0.429 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 0.500/1.000/0.667 | 0.375/0.600/0.462 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.750/1.000/0.857 | 0.167/0.200/0.182 |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.333/0.500/0.400 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.267/0.667/0.381 |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.333/0.500/0.400 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.444/0.667/0.533 |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.364/0.667/0.471 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.444/0.667/0.533 |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.500/0.667 | 0.333/0.333/0.333 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/0.833/0.909 | 0.273/0.500/0.353 |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.500/0.667 | 0.250/0.333/0.286 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/0.833/0.909 | 0.333/0.500/0.400 |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.500/0.667 | 0.286/0.333/0.308 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.222/0.333/0.267 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_JSON` | 6 | 0.803 | 0.396 |
| `T001_embedding_dim_default` | `CTX_MERMAID` | 6 | 0.762 | 0.304 |
| `T002_unified_sse_chain_contract` | `CTX_JSON` | 3 | 0.667 | 0.309 |
| `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 3 | 0.939 | 0.340 |
| `T003_ingest_admin_rpc` | `CTX_JSON` | 3 | 0.909 | 0.424 |
| `T003_ingest_admin_rpc` | `CTX_MERMAID` | 3 | 1.000 | 0.483 |
