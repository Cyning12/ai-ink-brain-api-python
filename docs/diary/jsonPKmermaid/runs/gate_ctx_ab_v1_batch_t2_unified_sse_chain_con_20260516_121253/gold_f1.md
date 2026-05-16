# gate_ctx_ab gold F1 — docs/diary/jsonPKmermaid/runs/gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.500/0.667 | 0.333/0.333/0.333 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/0.833/0.909 | 0.273/0.500/0.353 |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.500/0.667 | 0.250/0.333/0.286 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/0.833/0.909 | 0.333/0.500/0.400 |
| `CTX_JSON_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_JSON` | 1.000/0.500/0.667 | 0.286/0.333/0.308 |
| `CTX_MERMAID_T002_unified_sse_chain_contract_S0.jsonl` | `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 1.000/1.000/1.000 | 0.222/0.333/0.267 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T002_unified_sse_chain_contract` | `CTX_JSON` | 3 | 0.667 | 0.309 |
| `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 3 | 0.939 | 0.340 |
