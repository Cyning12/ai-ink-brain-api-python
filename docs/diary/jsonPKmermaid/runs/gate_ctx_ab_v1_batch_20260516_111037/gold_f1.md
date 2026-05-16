# gate_ctx_ab gold F1 — docs/diary/jsonPKmermaid/runs/gate_ctx_ab_v1_batch_20260516_111037

> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。
> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。

## 逐条记录

| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |
| --- | --- | --- | --- | --- |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/1.000/1.000 | 0.333/0.400/0.364 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.750/1.000/0.857 | 0.333/0.400/0.364 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 1.000/0.667/0.800 | 0.333/0.400/0.364 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.500/1.000/0.667 | 0.333/0.600/0.429 |
| `CTX_JSON_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_JSON` | 0.500/1.000/0.667 | 0.375/0.600/0.462 |
| `CTX_MERMAID_T001_embedding_dim_default_S0.jsonl` | `T001_embedding_dim_default` | `CTX_MERMAID` | 0.750/1.000/0.857 | 0.167/0.200/0.182 |

## 按 task × arm 均值（F1）

| task | arm | n | entrypoints F1 | impacts F1 |
| --- | --- | ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_JSON` | 3 | 0.822 | 0.396 |
| `T001_embedding_dim_default` | `CTX_MERMAID` | 3 | 0.794 | 0.325 |
