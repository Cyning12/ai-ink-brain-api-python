# gate_ctx_ab gold F1 — docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260521_091709

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_DUAL_MD_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_DUAL_MD` | 0.750/1.000/0.857 | 0.333/0.400/0.364 |
| `CTX_V2_QUERY_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_V2_QUERY` | 0.750/1.000/0.857 | 0.200/0.200/0.200 |
| `CTX_DUAL_MD_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_DUAL_MD` | 1.000/0.833/0.909 | 0.400/0.667/0.500 |
| `CTX_V2_QUERY_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_V2_QUERY` | 0.857/1.000/0.923 | 0.857/1.000/0.923 |
| `CTX_DUAL_MD_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_DUAL_MD` | 1.000/0.833/0.909 | 0.375/0.500/0.429 |
| `CTX_V2_QUERY_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_V2_QUERY` | 0.857/1.000/0.923 | 1.000/1.000/1.000 |
| `CTX_DUAL_MD_T004_chatbi_text2sql_chain_S0.jsonl` | `T004_chatbi_text2sql_chain` | `CTX_DUAL_MD` | 1.000/1.000/1.000 | 0.333/0.500/0.400 |
| `CTX_V2_QUERY_T004_chatbi_text2sql_chain_S0.jsonl` | `T004_chatbi_text2sql_chain` | `CTX_V2_QUERY` | 1.000/1.000/1.000 | 0.600/1.000/0.750 |
| `CTX_DUAL_MD_T005_intent_routing_S0.jsonl` | `T005_intent_routing` | `CTX_DUAL_MD` | 1.000/0.750/0.857 | 0.167/0.167/0.167 |
| `CTX_V2_QUERY_T005_intent_routing_S0.jsonl` | `T005_intent_routing` | `CTX_V2_QUERY` | 0.667/1.000/0.800 | 0.750/1.000/0.857 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_DUAL_MD` | 1 | 0.857 | 0.364 |
| `T001_embedding_dim_default` | `CTX_V2_QUERY` | 1 | 0.857 | 0.200 |
| `T002_unified_sse_chain_contract` | `CTX_DUAL_MD` | 1 | 0.909 | 0.500 |
| `T002_unified_sse_chain_contract` | `CTX_V2_QUERY` | 1 | 0.923 | 0.923 |
| `T003_ingest_admin_rpc` | `CTX_DUAL_MD` | 1 | 0.909 | 0.429 |
| `T003_ingest_admin_rpc` | `CTX_V2_QUERY` | 1 | 0.923 | 1.000 |
| `T004_chatbi_text2sql_chain` | `CTX_DUAL_MD` | 1 | 1.000 | 0.400 |
| `T004_chatbi_text2sql_chain` | `CTX_V2_QUERY` | 1 | 1.000 | 0.750 |
| `T005_intent_routing` | `CTX_DUAL_MD` | 1 | 0.857 | 0.167 |
| `T005_intent_routing` | `CTX_V2_QUERY` | 1 | 0.800 | 0.857 |
