# gate_ctx_ab_v1 batch — `gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300`

- **轮次**：3（每轮 `--parallel`）
- **剔除规则**：`wall>120.0s` 或 `>2.5×` 该 arm 当轮中位数；或 `status!=ok`

## 全量测量

| round | arm | wall_s | total_tokens | include | exclude_reason |
| ---:| --- | ---:| ---:| --- | --- |
| 1 | `CTX_JSON` | 45.311 | 12301 | True |  |
| 1 | `CTX_MERMAID` | 118.926 | 13113 | True |  |
| 2 | `CTX_JSON` | 11.072 | 12258 | True |  |
| 2 | `CTX_MERMAID` | 29.461 | 12696 | True |  |
| 3 | `CTX_JSON` | 85.358 | 11997 | True |  |
| 3 | `CTX_MERMAID` | 57.842 | 12810 | True |  |

## 剔除后对比（中位数）

| 指标 | CTX_JSON | CTX_MERMAID |
| --- | ---:| ---:|
| wall_median_s | 45.311 | 57.842 |
| total_tokens_median | 12258 | 12810 |
| 有效样本数 n | 3 | 3 |

详见 [`aggregate.json`](./aggregate.json)
