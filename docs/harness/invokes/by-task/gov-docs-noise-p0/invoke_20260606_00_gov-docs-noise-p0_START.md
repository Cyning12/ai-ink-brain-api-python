# invoke_20260606_00_gov-docs-noise-p0_START

> **帽**：00 总调度（Cursor 父 Agent · 串行 Task 链试点）  
> **round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`  
> **merge_policy**：`stop_before_merge`（CI 绿后停，等人确认 merge）  
> **续跑**：无（首轮）  
> **Prompt 真值（各帽 §3 全文）**：[`docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md`](../../../prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md)  
> **通用模板**：[`docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md`](../../../prompts/PROMPT_cursor_task_chain_serial_v1.md)

---

## §3 Prompt（父 Agent 正文）

**复制来源**：[`PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md`](../../../prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md) **§1**（00 正文）。

各帽 Task §3：**同文件 §2–§6**（explore / 22 / 30 / 40 / CLOSE）。

**Round T1 帽链（串行）**

| 序 | 帽 | subagent_type | Prompt 节 | 交付 |
| --- | --- | --- | --- | --- |
| 1 | explore | `explore` | §2 | `explore_C1-C3_diff_20260606.md` |
| 2 | 22 | `generalPurpose` | §3 | `reviews/by-task/.../audit_R1_20260606.md` |
| 3 | 30 | `generalPurpose` | §4 | C1–C3 三文件 + SPEC §3 状态 |
| 4 | 40 | `generalPurpose` | §5 | 自检回填 |
| 5 | CLOSE | 父会话 | §6 | PR + CI（stop_before_merge） |

**纪律摘要**：GATE_SCAN → 每帽 invoke→commit→Task→短报告；禁止代签 gate；禁止子 Task 再派 Task。

**完成后**：`HANDOFF_CLOSE_TRACE` + Harness 状态栏 B。
