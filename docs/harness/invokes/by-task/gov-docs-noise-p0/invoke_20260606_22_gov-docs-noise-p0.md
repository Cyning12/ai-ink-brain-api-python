# invoke_20260606_22_gov-docs-noise-p0

> **帽**：22 任务审核  
> **round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`  
> **交付物**：`docs/harness/reviews/by-task/gov-docs-noise-p0/task_gov_docs_noise_p0_readme_v1_audit_R1_20260606.md`

---

## §3 Prompt（22 帽 · 全文）

```text
【角色】Harness 22 任务审核帽。遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/reviews/README.md
- docs/harness/HARNESS_V2_PLAN.md §5

【canonical 读序】
docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md
docs/spec/governance/docs-noise-inventory/README.md
docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.1
docs/harness/invokes/by-task/gov-docs-noise-p0/explore_C1-C3_diff_20260606.md（若已存在）

【forbidden】
docs/diary/** · api/** · tests/** · 改 task 正文（除非审查清单要求回填且非阻塞）

【输入】
- task：docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md
- SPEC：docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md
- 上一轮审查：无（R1）
- explore 差分报告：（路径见上，若无则自读目标三文件）

【你必须完成】
1. 扫描 human_gate：HG-TASK-DRAFT 须 approved，否则拒开工
2. 对照 HARNESS_V2 §5：test_strategy=not_applicable 理由是否充分；failure_paths 是否可操作
3. 对照 explore 差分（或自读）：P0 范围是否清晰、非范围是否禁止删审计链
4. 落盘 R1 审查 md 至交付物路径（元信息表含 task_path、invoke_snapshot、AUDIT_ROUND=R1）
5. 结论：是否建议 30 帽开工；阻塞项清单
6. commit 仅本轮路径

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
