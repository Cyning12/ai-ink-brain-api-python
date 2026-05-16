# gate_ctx_ab_v1 batch — `gate_ctx_ab_v1_batch_20260516_111037`

- **轮次**：3（每轮 `--parallel`）
- **剔除规则**：`wall>120.0s` 或 `>2.5×` 该 arm 当轮中位数；或 `status!=ok`

## 全量测量

| round | arm | wall_s | total_tokens | include | exclude_reason |
| ---:| --- | ---:| ---:| --- | --- |
| 1 | `CTX_JSON` | 60.581 | 11975 | False | wall>2.5x_median |
| 1 | `CTX_MERMAID` | 23.818 | 12355 | True |  |
| 2 | `CTX_JSON` | 22.906 | 11786 | True |  |
| 2 | `CTX_MERMAID` | 333.322 | 12509 | False | wall_abs_cap>120.0 |
| 3 | `CTX_JSON` | 11.94 | 12533 | True |  |
| 3 | `CTX_MERMAID` | 41.247 | 12864 | True |  |

## 剔除后对比（中位数）

| 指标 | CTX_JSON | CTX_MERMAID |
| --- | ---:| ---:|
| wall_median_s | 17.423 | 32.532 |
| total_tokens_median | 12159 | 12609 |
| 有效样本数 n | 2 | 2 |

详见 [`aggregate.json`](./aggregate.json)
