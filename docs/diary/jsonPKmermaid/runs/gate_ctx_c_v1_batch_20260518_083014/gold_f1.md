# gate_ctx_ab gold F1 — /Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_DUAL_MD_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_DUAL_MD` | 0.750/1.000/0.857 | 0.250/0.400/0.308 |
| `CTX_V2_QUERY_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_V2_QUERY` | 0.750/1.000/0.857 | 0.200/0.200/0.200 |
| `CTX_DUAL_MD_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_DUAL_MD` | 1.000/0.833/0.909 | 0.455/0.833/0.588 |
| `CTX_V2_QUERY_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_V2_QUERY` | 0.857/1.000/0.923 | 0.857/1.000/0.923 |
| `CTX_DUAL_MD_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_DUAL_MD` | 1.000/0.833/0.909 | 0.375/0.500/0.429 |
| `CTX_V2_QUERY_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_V2_QUERY` | 1.000/1.000/1.000 | 0.167/0.333/0.222 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_DUAL_MD` | 1 | 0.857 | 0.308 |
| `T001_embedding_dim_default` | `CTX_V2_QUERY` | 1 | 0.857 | 0.200 |
| `T002_unified_sse_chain_contract` | `CTX_DUAL_MD` | 1 | 0.909 | 0.588 |
| `T002_unified_sse_chain_contract` | `CTX_V2_QUERY` | 1 | 0.923 | 0.923 |
| `T003_ingest_admin_rpc` | `CTX_DUAL_MD` | 1 | 0.909 | 0.429 |
| `T003_ingest_admin_rpc` | `CTX_V2_QUERY` | 1 | 1.000 | 0.222 |
