# invoke_20260606_30_gov-docs-noise-p0

> **帽**：30 执行  
> **round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`  
> **交付物**：C1–C3 三文件 + SPEC 导图 C* 状态

---

## §3 Prompt（30 帽 · 全文）

```text
【角色】Harness 30 执行帽（纯 docs）。遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md（自检回填格式）

【canonical 读序】
docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md
docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.1
docs/harness/reviews/by-task/gov-docs-noise-p0/task_gov_docs_noise_p0_readme_v1_audit_R1_20260606.md

【forbidden】
删除 docs/harness/invokes/** 或 reviews/** 历史全文
改 api/ tests/ .github/workflows/
docs/diary/** glob · docs/showcase/**

【输入】
- task：docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md
- 审查 R1：见上路径（须无阻塞）
- git_branch：task/gov-docs-noise-p0-v1
- VERIFY：无 pytest（test_strategy=not_applicable）；docs 自检见 task 验收

【你必须完成】
1. 扫描 human_gate：HG-GOV-P0-EXEC、HG-TASK-DRAFT 须 approved
2. **C1** 修 docs/harness/invokes/README.md：
   - 无「reviews 已移除」类表述
   - 明确 22→docs/harness/reviews/；20→review_results/；50→reinspect_results/
   - 与 docs/harness/reviews/README.md 一致
3. **C2** 修 docs/README.md §1：
   - 端到端优先 docs/_tech_graph/
   - docs/flows/ 降为历史快照（Legacy · 非 L0）
4. **C3** 新建 docs/tech_graph/README.md：
   - POINTER → docs/_tech_graph/
   - 说明 gate_a 两份 md 为闸口留痕，非 L0
5. 更新 docs/spec/governance/docs-noise-inventory/README.md §3：C1/C2/C3 状态 → done
6. 回填 task「### 自检结论（执行者）」
7. commit 仅本轮路径

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
