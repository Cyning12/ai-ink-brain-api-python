# invoke_20260606_explore_gov-docs-noise-p0

> **帽**：explore  
> **round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`  
> **交付物**：`docs/harness/invokes/by-task/gov-docs-noise-p0/explore_C1-C3_diff_20260606.md`

---

## §3 Prompt（explore 帽 · 全文）

```text
【角色】Harness explore · docs-noise P0 · 只读核对 C1–C3 差分；不写业务代码、不改 README。

【canonical 读序】
1. docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md（仅边界段）
2. docs/spec/governance/docs-noise-inventory/README.md
3. docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §4、§8.1
4. docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md

【须打开核对的目标文件】
- docs/harness/invokes/README.md（C1）
- docs/harness/reviews/README.md（C1 真值对照）
- docs/README.md §1（C2）
- AGENTS.md §必读（C2 对照，本 task 不改 AGENTS）
- docs/tech_graph/ 目录列表（C3 · 2 份 gate 留痕）
- 确认 docs/tech_graph/README.md 是否存在（C3）

【forbidden】
docs/diary/** · docs/harness/invokes/by-task/** glob（除本帽交付物路径）
docs/showcase/** · docs/delivery/** · docs/flows/** 全文
api/** · tests/**

【你必须完成】
1. 逐条对照 SPEC §8.1 P0-1/2/3，列出 C1/C2/C3 **现状 vs 期望**（引用行号或原文片段）
2. C1：全文检索「已移除」「不使用 reviews」类表述；对照 reviews/README 22/20/50 分工
3. C2：docs/README §1 是否仍推 flows 为端到端主入口；期望改为 _tech_graph 优先、flows 历史快照
4. C3：tech_graph/ 仅 2 文件时，给出 README.md 建议大纲（POINTER + gate 留痕说明）
5. 落盘 explore 报告至交付物路径（Markdown：Summary / C1 / C2 / C3 / Blockers / 建议 30 帽改动清单）
6. 按 HANDOFF_AUTO_COMMIT.md commit 仅本轮路径

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
