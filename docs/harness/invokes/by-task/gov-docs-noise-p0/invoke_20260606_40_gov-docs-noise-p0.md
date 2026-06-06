# invoke_20260606_40_gov-docs-noise-p0

> **帽**：40 自检  
> **round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`

---

## §3 Prompt（40 帽 · 全文）

```text
【角色】Harness 40 自检帽。遵循 docs/harness/prompts/hats/40-self-check.md

【canonical 读序】
docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md
docs/spec/governance/docs-noise-inventory/README.md §3

【须核对文件】
- docs/harness/invokes/README.md
- docs/README.md §1
- docs/tech_graph/README.md
- docs/spec/governance/docs-noise-inventory/README.md §3（C1–C3=done）

【验证命令】
rg -n '已移除|reviews.*移除' docs/harness/invokes/README.md  # 期望无命中
test -f docs/tech_graph/README.md
# 不跑 pytest（not_applicable）

【你必须完成】
1. 逐条勾选 task 验收标准
2. 更新/确认 task「### 自检结论（执行者）」含命令输出要点
3. 无阻塞则建议 CLOSE + PR
4. commit 仅本轮路径

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
