# gate_ctx_ab gold F1 — docs/diary/jsonPKmermaid/runs/gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.333/0.500/0.400 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.267/0.667/0.381 |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.333/0.500/0.400 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.444/0.667/0.533 |
| `CTX_JSON_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_JSON` | 1.000/0.833/0.909 | 0.364/0.667/0.471 |
| `CTX_MERMAID_T003_ingest_admin_rpc_S0.jsonl` | `T003_ingest_admin_rpc` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.444/0.667/0.533 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T003_ingest_admin_rpc` | `CTX_JSON` | 3 | 0.909 | 0.424 |
| `T003_ingest_admin_rpc` | `CTX_MERMAID` | 3 | 1.000 | 0.483 |
