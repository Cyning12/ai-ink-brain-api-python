# Invoke · 阶段 0.1 — 推送并开 PR（当前工作分支）

## 元信息

| 字段 | 值 |
|------|-----|
| hat_id | 30（Git/PR 执行，非业务代码） |
| template | 自定义 · `RECENT_TASK_SCHEDULE` §0.1 |
| git_branch | `task/chore-diary-tmp-ignore-and-main-branch-policy` |
| worktree_root | `ai-ink-brain-api-python` |
| task_paths | `ai-ink-brain-api-python/docs/tasks/RECENT_TASK_SCHEDULE.md` §0.1 |
| related_review | 无 |
| VERIFY | `git status` 干净（除 `docs/diary/tmp/`）；可选 `pytest tests -m "not intent_eval and not intent_benchmark"`（文档变更为主） |

---

## §3 可复制 Prompt 快照（占位符已替换）

```text
你正在执行 **RECENT_TASK_SCHEDULE §0.1**：为当前分支开 PR 合入 `main`，并更新排期表状态。严格遵循：
- docs/tasks/RECENT_TASK_SCHEDULE.md §0.1、§0.2（0.2 与本 PR 合并处理）
- .cursor/rules/07-git-workflow.mdc（本地不在 main 上提交；远程须 PR）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md（本轮仅改排期/invoke 时按路径 commit）

## 输入（已固定）

- **工作分支（勿新建分支）**：`task/chore-diary-tmp-ignore-and-main-branch-policy`
- **子仓根 / cwd**：`ai-ink-brain-api-python`（相对工作区 `Projects/`）
- **排期真值**：`ai-ink-brain-api-python/docs/tasks/RECENT_TASK_SCHEDULE.md`
- **本 invoke**：`ai-ink-brain-api-python/docs/harness/invokes/by-task/harness-stage0-1-pr-chore-branch/invoke_20260522_30_harness-stage0-1-pr-chore-branch.md`
- **相对 origin/main 的提交（PR 范围，合并后按实际核对）**：
  - d48845d docs(harness): 内嵌最小 Harness，恢复 22/50 落盘约定
  - c938689 docs(diary): Harness 评价与改进草案回复裁决
  - 0460ce1 docs(harness): 归档裁决生效共识并召回历史 review 样例
  - 4934eb4 chore: ignore docs/diary/tmp 并禁止在 main 直接 commit
  - ea1b427 docs(rules): 澄清 Git 工作流为本地勿在 main 操作、远程须 PR
  - 792ff5d docs(tasks): 新增 RECENT_TASK_SCHEDULE 最近任务安排真值表
  - b0e72e9 docs(agents): 必读链至 RECENT_TASK_SCHEDULE 排期表

## 你必须完成

1. **确认分支**：`git branch --show-current` 必须为 `task/chore-diary-tmp-ignore-and-main-branch-policy`；若在 `main` 则 **停止** 并切换回本分支。
2. **检查工作区**：`git status`；`docs/diary/tmp/` 应在 `.gitignore` 中且 **未** 被 add；无意外未提交改动（若有本轮未纳入的修改，先 commit 或向用户说明）。
3. **推送**：`git push -u origin task/chore-diary-tmp-ignore-and-main-branch-policy`（需网络权限）。
4. **创建 PR**（`gh pr create`）：
   - **base**：`main`
   - **title** 建议：`docs(harness): 内嵌 Harness、排期表与 Git 工作流（阶段 0.1）`
   - **body** 须含：Summary（3～6 条）、§0.1/0.2 说明、Test plan（文档为主；可选 pytest 已绿）、链 `RECENT_TASK_SCHEDULE.md`
5. **PR 创建后**：在同一分支更新 `docs/tasks/RECENT_TASK_SCHEDULE.md` §0.1 表「状态」为 `PR #<号> 已开`；§0.2 标 `并入 0.1`；commit 仅该文件（或含 invoke 若本轮有改）。
6. **对话输出**：
   - PR URL
   - 📋 Harness 状态栏（版本 B）：已执行 0.1；下一棒 **0.2 待 PR 合并** → 然后 **P0-A（A1 扩展 TASK_TEMPLATE）**
   - 下一棒 **可复制 Prompt**（路径 B 推荐）：直接执行 P0-A1，仍用 **本分支**，勿切 main

## 禁止

- 新建 `task/harness-improve-p0-*` 分支
- 在本地 `main` 上 commit / push
- `git push --force` 到 `main`
- 将 `docs/diary/tmp/` 加入 Git

## 下一棒 Prompt（PR 合并后 · P0-A1 · 推荐）

（PR 合并且本地 `git checkout` 回任务分支并 `git pull origin main` 或 rebase 后，由人发起；Agent 可复制执行）

见对话末尾由执行 Agent 根据 `RECENT_TASK_SCHEDULE` §0.2 表 A1 生成，或用户说「继续 P0-A1」。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：§0.1 启动快照 |
