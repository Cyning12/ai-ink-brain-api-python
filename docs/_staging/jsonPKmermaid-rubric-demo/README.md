# Rubric 多轮演示（暂存）

> **自** `docs/diary/jsonPKmermaid/` **迁出**（2026-05-15），与 **JSON vs Mermaid 行为实验**（见 [`../../diary/jsonPKmermaid/01_experiment_json_vs_mermaid_kpi_v1.md`](../../diary/jsonPKmermaid/01_experiment_json_vs_mermaid_kpi_v1.md)）**无关**。  
> **用途**：`examples_builtin` 批跑产物、元评审示例、`prompt_analyze_first_round_rubric.md`；日后若做 P1/P2 双人 Rubric 可从此目录或 `tools/rubric_review` 恢复。

## 内容

| 路径 | 说明 |
|------|------|
| [`rubric_runs/`](./rubric_runs/) | `batch_stamp=20260515_201818` 等机器输出 |
| [`results/`](./results/) | `copy_ready_*`、`meta_review_*` 人读示例 |
| [`prompt_analyze_first_round_rubric.md`](./prompt_analyze_first_round_rubric.md) | 元评审 Prompt 模板 |
| [`rubric_pr_and_design_v1.json`](./rubric_pr_and_design_v1.json) | PR/设计向 Rubric（与模板 JSON 同内容） |

## CLI 默认落盘

`tools/rubric_review` 默认输出目录已指向本目录下 [`rubric_runs/`](./rubric_runs/)（见 `tools/rubric_review/paths.py`）。
