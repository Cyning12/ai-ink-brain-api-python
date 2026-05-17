# Rubric 多轮评审 — 合并总报告

## 元信息

| 字段 | 值 |
|------|-----|
| 生成时间（UTC） | 2026-05-15T12:12:24Z |
| manifest | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/multiround.example.json` |
| run_name | `examples_builtin` |
| rubric | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/min_rubric.json` |
| 后端 | `siliconflow` |
| R1 模型 | `Pro/moonshotai/Kimi-K2.6` |
| R2 模型 | `deepseek-ai/DeepSeek-V4-Flash` |
| 仲裁模型 | `deepseek-ai/DeepSeek-V4-Flash` |
| random_seed | `42` |
| 轮数 | 3 |

## 各轮索引

| 轮次 id | 工件 | 单轮 Markdown | 单轮 JSON |
|---------|------|---------------|-----------|
| `S0` | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S0_pr_body.md` | [rubric_review_examples_builtin_S0_20260515_201126_00.md](./rubric_review_examples_builtin_S0_20260515_201126_00.md) | [rubric_review_examples_builtin_S0_20260515_201126_00.json](./rubric_review_examples_builtin_S0_20260515_201126_00.json) |
| `S1` | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S1_followup.md` | [rubric_review_examples_builtin_S1_20260515_201126_01.md](./rubric_review_examples_builtin_S1_20260515_201126_01.md) | [rubric_review_examples_builtin_S1_20260515_201126_01.json](./rubric_review_examples_builtin_S1_20260515_201126_01.json) |
| `S2` | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S2_low_overlap.md` | [rubric_review_examples_builtin_S2_20260515_201126_02.md](./rubric_review_examples_builtin_S2_20260515_201126_02.md) | [rubric_review_examples_builtin_S2_20260515_201126_02.json](./rubric_review_examples_builtin_S2_20260515_201126_02.json) |

## 各轮终分汇总

| 轮次 | `clarity` | `risk` |
| --- | --- | --- |
| `S0` | 2 | 1 |
| `S1` | 4 | 3 |
| `S2` | 4 | 2 |

## 说明

- 各轮完整双人评审与仲裁细节见上表 **单轮 Markdown / JSON**；本文件仅做索引与分数矩阵。
- 多轮共用 **同一组** R1/R2/仲裁模型分配（便于横向对比各轮工件）。
