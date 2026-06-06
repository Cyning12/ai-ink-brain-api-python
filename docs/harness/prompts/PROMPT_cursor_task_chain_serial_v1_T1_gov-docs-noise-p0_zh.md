# PROMPT · Cursor Task 链 T1 实例 · gov-docs-noise P0（C1–C3）

> **Round**：T1  
> **task_slug**：`gov_docs_noise_p0_readme_v1`  
> **task_path**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **git_branch**：`task/gov-docs-noise-p0-v1`  
> **slug**：`gov-docs-noise-p0`  
> **merge_policy**：`stop_before_merge`  
> **通用模板**：[`PROMPT_cursor_task_chain_serial_v1.md`](PROMPT_cursor_task_chain_serial_v1.md)  
> **00 START invoke**：[`../invokes/by-task/gov-docs-noise-p0/invoke_20260606_00_gov-docs-noise-p0_START.md`](../invokes/by-task/gov-docs-noise-p0/invoke_20260606_00_gov-docs-noise-p0_START.md)

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞帽 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22-R1, 30 |
| `HG-GOV-P0-EXEC` | `approved` | explore, 22, 30, 40, CLOSE |

任一为 `pending` → 00 **只报 gate_id + task 路径**，不派 Task。

---

## 1. §3 父 Agent 正文（00 · 可复制）

```text
你 = Harness 00 总调度（Cursor · 串行 Task 链 · Round T1）。遵循：
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md
- docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md（本文件 · 各帽 §3）
- docs/spec/governance/docs-noise-inventory/README.md

输入（已填）：
- task：docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md
- Round：T1
- slug：gov-docs-noise-p0
- git_branch：task/gov-docs-noise-p0-v1
- merge_policy：stop_before_merge
- 续跑 invoke：无（或填最新 invoke 路径）

Round T1 帽链（串行，禁止并行 Task）：
  explore → 22 → 30 → 40 → CLOSE → PR → CI（停于 merge 前）

纪律：
1. GATE_SCAN 通过后，按 §2–§6 顺序：每帽 invoke 落盘 → commit → Task → 收 ≤10 行报告
2. 各帽 Task prompt 使用本文件 §2–§5 正文（勿省略 canonical/forbidden）
3. 禁止子 Task 再派 Task；禁止贴子 Task 全文
4. test_strategy=not_applicable：40 帽不跑 pytest；对照 task 验收清单即可
5. CLOSE 后 gh pr create；CI Required 全绿后 stop_before_merge → 停，不 merge
6. 禁止代签 human_gate

完成后：HANDOFF_CLOSE_TRACE + Harness 状态栏 B
```

---

## 2. §3 explore 帽（Task · subagent_type=explore）

**invoke 建议名**：`invoke_20260606_explore_gov-docs-noise-p0.md`  
**交付物**：`docs/harness/invokes/by-task/gov-docs-noise-p0/explore_C1-C3_diff_20260606.md`

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

---

## 3. §3 22 帽（Task · subagent_type=generalPurpose）

**invoke 建议名**：`invoke_20260606_22_gov-docs-noise-p0.md`  
**交付物**：`docs/harness/reviews/by-task/gov-docs-noise-p0/task_gov_docs_noise_p0_readme_v1_audit_R1_20260606.md`

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

---

## 4. §3 30 帽（Task · subagent_type=generalPurpose）

**invoke 建议名**：`invoke_20260606_30_gov-docs-noise-p0.md`  
**交付物**：C1–C3 三文件 + SPEC 导图 C* 状态

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

---

## 5. §3 40 帽（Task · subagent_type=generalPurpose）

**invoke 建议名**：`invoke_20260606_40_gov-docs-noise-p0.md`

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

---

## 6. §3 CLOSE 帽（父 Agent 会话 · 非 Task）

```text
【角色】Harness CLOSE · Round T1

【你必须完成】
1. 落盘 invoke_YYYYMMDD_CLOSE_gov-docs-noise-p0.md
2. 更新 docs/tasks/_views/（若 task 仍 active 则暂不 git mv；PR 合并后再 done）
3. git push -u origin task/gov-docs-noise-p0-v1
4. gh pr create --title "docs(governance): docs-noise P0 fix C1-C3 README pointers" \
     --body 含 Summary / Test plan（docs-only · CI Required）
5. gh pr checks --watch；全绿后 stop_before_merge → 向人报告 PR URL，不 merge
6. HANDOFF_CLOSE_TRACE + Harness 状态栏 B
```

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T1 P0 实例 · 占位符全填 · 五帽 §3 落盘 |
