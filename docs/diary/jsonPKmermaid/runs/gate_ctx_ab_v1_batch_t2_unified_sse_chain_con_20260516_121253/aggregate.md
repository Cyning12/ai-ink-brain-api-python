# gate_ctx_ab_v1 batch — `gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253`

- **轮次**：3（每轮 `--parallel`）
- **剔除规则**：`wall>120.0s` 或 `>2.5×` 该 arm 当轮中位数；或 `status!=ok`

## 全量测量

| round | arm | wall_s | total_tokens | include | exclude_reason |
| ---:| --- | ---:| ---:| --- | --- |
| 1 | `CTX_JSON` | 61.955 | 12014 | True |  |
| 1 | `CTX_MERMAID` | 66.581 | 12571 | True |  |
| 2 | `CTX_JSON` | 38.965 | 12250 | True |  |
| 2 | `CTX_MERMAID` | 7.13 | 12374 | True |  |
| 3 | `CTX_JSON` | 23.646 | 12044 | True |  |
| 3 | `CTX_MERMAID` | 47.626 | 12708 | True |  |

## 剔除后对比（中位数）

| 指标 | CTX_JSON | CTX_MERMAID |
| --- | ---:| ---:|
| wall_median_s | 38.965 | 47.626 |
| total_tokens_median | 12044 | 12571 |
| 有效样本数 n | 3 | 3 |

详见 [`aggregate.json`](./aggregate.json)
