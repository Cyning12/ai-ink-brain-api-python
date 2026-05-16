# gate_ctx_ab_v1 batch — `gate_ctx_ab_v1_batch_20260516_110751`

- **轮次**：3（每轮 `--parallel`）
- **剔除规则**：`wall>120.0s` 或 `>2.5×` 该 arm 当轮中位数；或 `status!=ok`

## 全量测量

| round | arm | wall_s | total_tokens | include | exclude_reason |
| ---:| --- | ---:| ---:| --- | --- |
| 1 | `CTX_JSON` | 72.449 | 12346 | False | wall>2.5x_median |
| 1 | `CTX_MERMAID` | 22.333 | 12333 | True |  |
| 2 | `CTX_JSON` | 21.245 | 11986 | True |  |
| 2 | `CTX_MERMAID` | 35.586 | 12295 | True |  |
| 3 | `CTX_JSON` | 6.993 | 11756 | True |  |
| 3 | `CTX_MERMAID` | 6.971 | 12483 | True |  |

## 剔除后对比（中位数）

| 指标 | CTX_JSON | CTX_MERMAID |
| --- | ---:| ---:|
| wall_median_s | 14.119 | 22.333 |
| total_tokens_median | 11871 | 12333 |
| 有效样本数 n | 2 | 3 |

详见 [`aggregate.json`](./aggregate.json)
