# gate_ctx_ab gold F1 — /Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_b_v1_batch_20260517_095228

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_QUERY_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_QUERY` | 0.750/1.000/0.857 | 0.200/0.200/0.200 |
| `CTX_QUERY_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_QUERY` | 1.000/0.500/0.667 | 0.250/0.333/0.286 |
| `CTX_QUERY_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_QUERY` | 1.000/1.000/1.000 | 0.222/0.333/0.267 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_QUERY` | 1 | 0.857 | 0.200 |
| `T002_unified_sse_chain_contract` | `CTX_QUERY` | 1 | 0.667 | 0.286 |
| `T003_ingest_admin_rpc` | `CTX_QUERY` | 1 | 1.000 | 0.267 |
