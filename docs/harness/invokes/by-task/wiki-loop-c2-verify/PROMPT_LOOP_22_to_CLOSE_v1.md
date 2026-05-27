# 启动 Prompt · Loop 执行 · 22 → 关账（v1 · 无 10）

> **单 round 模板** · 先读 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) 替换 §3 占位符。  
> **全链首次启动**（R1→META 同会话）：用 [`PROMPT_START_loop_c2_verify_full_chain_v1.md`](./PROMPT_START_loop_c2_verify_full_chain_v1.md)（【授权】**仅**在该文件，**不在**本模板 §3）。  
> **禁止** 再跑 10；task 初稿已由 [`PROMPT_BATCH_10_c2_verify_v1.md`](./PROMPT_BATCH_10_c2_verify_v1.md) 生成。  
> **invoke C2**：见 [`SKILL-harness-loop-batch`](../../../tasks/skills/SKILL-harness-loop-batch.md) §invoke 质量门禁；§3 步骤 1–5 **换帽前**须自检（R2+ 与 R1 同标准）。

---

## 1. 执行前替换表（粘贴 §3 前必改）

| 占位符 | 示例（R1 轮） |
|--------|----------------|
| `{{LOOP_ROUND}}` | `R1` |
| `{{TASK_PATH}}` | `docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| `{{TASK_SLUG}}` | `wiki-c2-r1-schedule-draft` |
| `{{FREEZE_ID}}` | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| `{{GIT_BRANCH}}` | `task/wiki-loop-c2-verify-v1` |
| `{{NEXT_TASK_PATH}}` | R1 关账填 R2 path；R2/META 填 `无` |
| `{{PLACEHOLDER_ID}}` | 本 Loop 无 HTML 占位；填 `无` |
| `{{PREV_DONE_TASK}}` | R2 开工填 R1 done path；R1 填 `无` |

---

## 2. 回合特例

| round | 22 开工前额外步骤 |
|-------|-------------------|
| **R1** | 确认母 task `HG-LOOP-BATCH` = approved |
| **R2** | R1 须在 `done/` 且 RECENT §6.6 含 Loop C2 Verify draft 行；**本 round 负责** RECENT done + `_views/done.md` + invoke README 验收行 |
| **META** | 两轮子 task 均在 `done/`；只关账母 task + 第三 Loop C2 注记；**禁止** Agent 代 SKILL 标 `accepted` |

---

## 3. 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **{{LOOP_ROUND}}** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/tasks/skills/SKILL-harness-loop-batch.md
- .cursor/rules/05-harness-semi-auto.mdc、06-harness-in-repo.mdc、07-git-workflow.mdc
- semi_auto: true（无 pending 闸时可同会话连跑至本 round 关账）
- **commit（硬）**：每帽结束须 `git add` 本轮路径 + `commit` 后再戴下一帽（见 HANDOFF_AUTO_COMMIT）；禁止只落盘不提交
- **invoke C2（硬）**：每帽 invoke §3 全文 ≥15 行（或文件 ≥800B）；元信息表含 round/hat/task/task_slug/freeze_id/git_branch；cross-round 续跑 R2+ **与 R1 同标准**（见 SKILL-harness-loop-batch §invoke 质量门禁）

【元信息】
- round: {{LOOP_ROUND}}
- task: {{TASK_PATH}}
- task_slug: {{TASK_SLUG}}
- freeze_id: {{FREEZE_ID}}
- git_branch: {{GIT_BRANCH}}
- 母 task: docs/tasks/active/task_harness_wiki_loop_c2_verify_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-c2-verify/

---

### 步骤 0 · 占位回填（仅当 {{PLACEHOLDER_ID}} ≠ 无）

若 {{TASK_PATH}} 中含 `<!-- PLACEHOLDER:{{PLACEHOLDER_ID}} -->` 且仍为「待回填」：

1. 读 {{PREV_DONE_TASK}} 的 §实现备忘、§自检结论、关账 commit message。
2. 用 3～8 行 Markdown **替换** 占位块（保留起止 HTML 注释行）。
3. `git add` 仅 {{TASK_PATH}} · commit `chore(task): 回填 {{PLACEHOLDER_ID}} · {{FREEZE_ID}}`
4. 再进入 22。

若占位已填或 {{PLACEHOLDER_ID}} = 无：跳过步骤 0。

---

### 步骤 1 · 22

【invoke C2 自检 · 落盘前】§3 正文 ≥15 行？元信息表含 task_slug？§3 为可复制 Prompt 而非摘要？

【开帽】落盘 invoke：
docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_YYYYMMDD_22_{{TASK_SLUG}}-v1.md

- §3 须含：`22-task-audit` 引用、审 {{TASK_PATH}} §范围/§非范围/§failure_paths、review 落盘路径、准许 30 条件
- 子 task：确认「继承 HG-LOOP-BATCH」；**禁止** 代填 pending
- 落盘 review：docs/harness/reviews/by-task/wiki-loop-c2-verify/task_<basename>_audit_R1_YYYYMMDD.md
- 无阻塞 → 准许 30
- commit review + invoke（**invoke 未过 C2 不得 commit**）

---

### 步骤 2 · 30 执行

【invoke C2 自检 · 落盘前】§3 正文 ≥15 行？元信息表含 task_slug？§3 非「交付摘要」？

【开帽】落盘 invoke：
docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_YYYYMMDD_30_{{TASK_SLUG}}-v1.md

- §3 须含：`30-execute-code` 引用、按 task §范围交付项清单、回填 §实现备忘、commit 含 {{FREEZE_ID}}、下一棒 40
- 按 task §范围交付（纯 docs）；不改 api/、tests/、docs/harness/prompts/。
- 回填 task §实现备忘；commit 含 {{FREEZE_ID}}（**invoke 未过 C2 不得 commit**）

---

### 步骤 3 · 40 自检

【invoke C2 自检 · 落盘前】§3 正文 ≥15 行？元信息表含 task_slug？§3 非「交付摘要」？

【开帽】落盘 invoke：
docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_YYYYMMDD_40_{{TASK_SLUG}}-v1.md

- §3 须含：`40-self-check` 引用、task/PROMPT 中 VERIFY 项列表、填 ### 自检结论（执行者）表、commit 路径
- 跑 task / PROMPT 中 VERIFY 项，填 ### 自检结论（执行者）表
- commit task + invoke（**invoke 未过 C2 不得 commit**）

---

### 步骤 4 · 50 复检

【invoke C2 自检 · 落盘前】§3 正文 ≥15 行？元信息表含 task_slug？§3 非「交付摘要」？

【开帽】落盘 invoke：
docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_YYYYMMDD_50_{{TASK_SLUG}}-v1.md

- §3 须含：`50-independent-reinspect` 引用、独立重跑 40 VERIFY、`reinspect_{{TASK_SLUG}}_*` 落盘路径、关账/回 30 结论
- 独立重跑 40 VERIFY
- 落盘 docs/tasks/reinspect_results/reinspect_{{TASK_SLUG}}_YYYYMMDD_v1.md
- 结论：建议关账 / 须回 30
- commit reinspect + invoke（**invoke 未过 C2 不得 commit**）

---

### 步骤 5 · 关账（本 round）

【invoke C2 自检 · 落盘前】§3 正文 ≥15 行？元信息表含 task_slug？

【开帽】落盘 invoke：
docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_YYYYMMDD_CLOSE_{{TASK_SLUG}}-v1.md

1. `git mv` {{TASK_PATH}} → docs/tasks/done/（文件名保持 task_*_v1.md）
2. 状态行 `done（YYYY-MM-DD 验收通过 · {{FREEZE_ID}}）`；勾选 §验收
3. 更新 docs/tasks/_views/done.md 一行
4. **仅当 round = R2 或 META**：改 RECENT_TASK_SCHEDULE §6.6 本 Loop 行 → done
5. 文末 HANDOFF_CLOSE_TRACE（22/30/40/50 · commit 列表）

**关账后 · 下一子 task 准备（若 {{NEXT_TASK_PATH}} ≠ 无）**：

6. 打开 {{NEXT_TASK_PATH}}，确认 R1 交付已就绪（本 Loop 无 PLACEHOLDER 块则跳过回填 commit）
7. **若** cross-round 授权（PROMPT_START §2 或首份 22 invoke `cross_round_semi_auto: true`）：同会话续 MANIFEST 下一 round
8. commit 关账 · message `docs(task): Wiki loop C2 Verify {{LOOP_ROUND}} 关账 · {{FREEZE_ID}}`

---

### 步骤 6 · 对话末尾

- 📋 Harness 状态栏（版本 B）
- round = META：整链 CLOSE_TRACE · **无下一棒**
- round = META：对话可摘要完成汇报 §1～§5；**§6 待你侧后续仅对话、禁止落盘**

---

### 步骤 7 · 长 Loop 完成汇报（**仅 `{{LOOP_ROUND}}` = META**）

> 真值：docs/tasks/skills/SKILL-harness-loop-batch.md §长 Loop 完成汇报

1. META 关账 commit（步骤 5 · 母单）**已完成** 后执行
2. 落盘：docs/harness/invokes/by-task/wiki-loop-c2-verify/REPORT_completion_YYYYMMDD_v1.md
   - **须含 §1～§5**（任务定位、核心成果、Harness 工件、Commit 回溯、验收核对）
   - 文首链 invoke_*_CLOSE_*-META-v1.md；**禁止**整段复制 CLOSE_TRACE
   - **禁止**写入 §6（开 PR、meta-reinspect、SKILL accepted 等 → **仅步骤 6 对话**）
3. `git add` 仅 REPORT · commit · message 含母 freeze_id（WIKI-LOOP-C2-VERIFY@…）
4. 更新本实例 README「完成汇报」链一行（若尚无）

硬约束：Open ai-ink-brain-api-python/ · 分支 {{GIT_BRANCH}} · 单 PR 纪律 · **C2 invoke 质量全绿**为本 Loop 主验收
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：自 wiki-loop-bq3-recheck 复制改编 · 2 round + META · C2 Verify 主题 |
| 2026-05-26 | v1.1：第三批 · invoke C2 自检句（步骤 1–5）+ R2 RECENT/_views 特例 |
| 2026-05-26 | v1.2：步骤 7 · META 后 `REPORT_completion_*`（§6 仅对话） |
