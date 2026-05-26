# 启动 Prompt · Loop 执行 · 22 → 关账（v1 · 无 10）

> **单 round 模板** · 先读 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) 替换 §3 占位符。  
> **全链首次启动**（A1→META 同会话）：用 [`PROMPT_START_loop_a1_full_chain_v1.md`](./PROMPT_START_loop_a1_full_chain_v1.md)（【授权】**仅**在该文件，**不在**本模板 §3）。  
> **禁止** 再跑 10；task 初稿已由 [`PROMPT_BATCH_10_four_tasks_v1.md`](./PROMPT_BATCH_10_four_tasks_v1.md) 生成。

---

## 1. 执行前替换表（粘贴 §3 前必改）

| 占位符 | 示例（A1 轮） |
|--------|----------------|
| `{{LOOP_ROUND}}` | `A1` |
| `{{TASK_PATH}}` | `docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md` |
| `{{TASK_SLUG}}` | `wiki-a1-ingest-test-strategy` |
| `{{FREEZE_ID}}` | `CODING-WIKI-A1-TEST-STRATEGY@2026-05-26` |
| `{{GIT_BRANCH}}` | `task/wiki-loop-a1-a4-v1` |
| `{{NEXT_TASK_PATH}}` | A1 关账填：`docs/tasks/active/task_coding_wiki_schema_test_strategy_rule_v1.md`；A4/META 填 `无` |
| `{{PLACEHOLDER_ID}}` | A1 关账填：`A1_OUTCOME`；其他轮多为 `无` |
| `{{PREV_DONE_TASK}}` | A2 开工填：`docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md`；A1 填 `无` |

---

## 2. 回合特例

| round | 22 开工前额外步骤 |
|-------|-------------------|
| **A1** | 确认母 task `HG-LOOP-BATCH` = approved |
| **A2** | 读 `{{PREV_DONE_TASK}}`；若 A2 active 内 `PLACEHOLDER:A1_OUTCOME` 仍为「待回填」→ **先回填**（见 §3 步骤 0）再 22 |
| **A3** | 无占位；可读 A1/A2 done 备忘，非硬依赖 |
| **A4** | 建议 A1–A3 已在 `done/` |
| **META** | 四轮子 task 均在 `done/`；本 round 只关账母 task |

---

## 3. 可复制 Prompt 正文

```text
你正在执行 Wiki Loop **{{LOOP_ROUND}}** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/05-harness-semi-auto.mdc、06-harness-in-repo.mdc、07-git-workflow.mdc
- semi_auto: true（无 pending 闸时可同会话连跑至本 round 关账）
- **commit（硬）**：每帽结束须 `git add` 本轮路径 + `commit` 后再戴下一帽（见 HANDOFF_AUTO_COMMIT）；禁止只落盘不提交

【元信息】
- round: {{LOOP_ROUND}}
- task: {{TASK_PATH}}
- task_slug: {{TASK_SLUG}}
- freeze_id: {{FREEZE_ID}}
- git_branch: {{GIT_BRANCH}}
- 母 task: docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-a1-a4/

---

### 步骤 0 · 占位回填（仅当 {{PLACEHOLDER_ID}} ≠ 无）

若 {{TASK_PATH}} 中含 `<!-- PLACEHOLDER:{{PLACEHOLDER_ID}} -->` 且仍为「待回填」：

1. 读 {{PREV_DONE_TASK}} 的 §实现备忘、§自检结论、关账 commit message。
2. 用 3～8 行 Markdown **替换** 占位块（保留起止 HTML 注释行），含：test_strategy 取值、改动路径、commit 短哈希。
3. `git add` 仅 {{TASK_PATH}} · commit `chore(task): 回填 {{PLACEHOLDER_ID}} · {{FREEZE_ID}}`
4. 再进入 22。

若占位已填或 {{PLACEHOLDER_ID}} = 无：跳过步骤 0。

---

### 步骤 1 · 22 R1

【开帽】落盘 invoke：
docs/harness/invokes/by-task/wiki-loop-a1-a4/invoke_YYYYMMDD_22_{{TASK_SLUG}}-v1.md

- 审 {{TASK_PATH}} §范围/§非范围/§failure_paths
- 子 task：确认「继承 HG-LOOP-BATCH」；**禁止** 代填 pending
- 落盘 R1：docs/harness/reviews/by-task/wiki-loop-a1-a4/task_<basename>_audit_R1_YYYYMMDD.md
- 无阻塞 → 准许 30
- commit review + invoke

---

### 步骤 2 · 30 执行

【开帽】invoke_YYYYMMDD_30_{{TASK_SLUG}}-v1.md

按 task §范围交付（纯 docs）；不改 api/、tests/、docs/harness/prompts/。
回填 task §实现备忘；commit 含 {{FREEZE_ID}}。

---

### 步骤 3 · 40 自检

【开帽】invoke_YYYYMMDD_40_{{TASK_SLUG}}-v1.md

- 跑 task / PROMPT 中 VERIFY 项，填 ### 自检结论（执行者）表
- commit task + invoke

---

### 步骤 4 · 50 复检

【开帽】invoke_YYYYMMDD_50_{{TASK_SLUG}}-v1.md

- 独立重跑 40 VERIFY
- 落盘 docs/tasks/reinspect_results/reinspect_{{TASK_SLUG}}_YYYYMMDD_v1.md
- 结论：建议关账 / 须回 30

---

### 步骤 5 · 关账（本 round）

【开帽】invoke_YYYYMMDD_CLOSE_{{TASK_SLUG}}-v1.md

1. `git mv` {{TASK_PATH}} → docs/tasks/done/（文件名保持 task_*_v1.md）
2. 状态行 `done（YYYY-MM-DD 验收通过 · {{FREEZE_ID}}）`；勾选 §验收
3. 若 round ≠ META：更新 docs/tasks/_views/done.md 一行；**仅当 A4 或 META** 时改 RECENT_TASK_SCHEDULE §6.6（避免每轮改排期冲突）
4. 文末 HANDOFF_CLOSE_TRACE（22/30/40/50 · commit 列表）

**关账后 · 下一子 task 准备（若 {{NEXT_TASK_PATH}} ≠ 无）**：

5. 打开 {{NEXT_TASK_PATH}}，若含 `<!-- PLACEHOLDER:... -->`：
   - 用本 round 交付摘要回填（与步骤 0 相同纪律）
   - commit `chore(task): 预回填 <PLACEHOLDER_ID> from {{LOOP_ROUND}} close`
6. **禁止** 为下一子 task 新建 10 或重写 task 结构。
   - **若** 当会话已授权 cross-round（见 [`PROMPT_START_loop_a1_full_chain_v1.md`](./PROMPT_START_loop_a1_full_chain_v1.md) §2，或首份 22 invoke 元信息 `cross_round_semi_auto: true`）：关账 commit 后 **同会话** 读 MANIFEST 下一 round → 生成下一 round 22 invoke §3 全文 → commit → 续跑 22；**禁止** 要求用户开新对话或再贴【授权】。
   - **否则**：**禁止** 在本会话代跑下一子 task 的 22；步骤 6 输出「下一对话 · 本文件 · MANIFEST round=…」。

7. commit 关账改动 · message `docs(task): Wiki loop {{LOOP_ROUND}} 关账 · {{FREEZE_ID}}`

---

### 步骤 6 · 对话末尾

- 📋 Harness 状态栏（版本 B）
- 若 {{NEXT_TASK_PATH}} ≠ 无 **且未** cross-round 授权：输出「下一对话 · PROMPT_LOOP_22_to_CLOSE · MANIFEST round=…」
- 若已 cross-round 授权且 {{NEXT_TASK_PATH}} ≠ 无：状态栏写「续跑 round=… · 同会话」；**不**停
- 若 round = META：输出整链 CLOSE_TRACE · **无下一棒**

硬约束：Open ai-ink-brain-api-python/ · 分支 {{GIT_BRANCH}} · 单 PR 纪律

关键词：Loop、{{LOOP_ROUND}}、22、30、40、50、关账、无10、PLACEHOLDER、HANDOFF_AUTO_COMMIT
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：Batch 10 与 Loop 22→关账 分离 |
| 2026-05-26 | v1.1：跨 round【授权】迁至 PROMPT_START_loop_a1_full_chain；§3 增 commit 硬纪律与 cross-round 续跑规则 |
