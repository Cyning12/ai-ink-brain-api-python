# Harness invoke snapshot — 22 帽 · B3 ChatBI 注入 PoC 关账

| 字段 | 值 |
| --- | --- |
| hat_id | 22 |
| template | `docs/harness/prompts/TEMPLATE-task-audit-invoke.md` §3 |
| task_paths | `ai-ink-brain-api-python/docs/tasks/done/task_chatbi_v3_prompt_injection_guard_poc_v1.md` |
| related_review_or_none | `ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_R4_20260514.md`（工作区指针：`docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_R4_20260514.md`） |
| priority_roadmap | [`docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md`](../../../../docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md) §3 **B3** · INK-P3 |
| git_branch | **`task/chatbi-v3-prompt-injection-closeout-v1`**（**禁止**与 B1 共用） |
| worktree_root | **`ai-ink-brain-api-python-wt-chatbi-closeout`**（相对 `Projects/`；`pytest`/`git` cwd） |
| parallel_with | B1 · [`invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md`](invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md)（`task/engineering-tech-graph-gate-d-v2-tasks-v1`） |
| created | 2026-05-20 |
| revised | 2026-05-20（明确独立分支） |
| closed | 2026-05-20 · 22 帽 CLOSE → `task_chatbi_v3_prompt_injection_guard_poc_v1_audit_CLOSE_20260520.md` · INK-P3/B3 `done` |

## 分支与并行（子 Agent 必读）

1. **路线图**：关账后 **必须** 按 `PRIORITY_ROADMAP_v1_zh.md` §0 更新 **INK-P3 / §3 B3**。  
2. **仓库**：仅 `ai-ink-brain-api-python`。  
3. **禁止共用分支**：不得使用 `task/engineering-tech-graph-gate-d-v2-tasks-v1`（闸口 D · B1）；不得在前端 `task/tech-graph-v2-*` 分支上改本 task。  
4. **创建分支**（实现已在 `main` 或既有 feature 上时，从含 PoC 代码的基线拉出）：  
   `git fetch && git checkout main && git pull && git checkout -b task/chatbi-v3-prompt-injection-closeout-v1`  
   （若 PoC 仅在未合并分支，基线改维护者指定分支，**仍须** 新建上述 closeout 分支名。）  
5. **本帽产出**：审查 md +（若签收）task 关账与 `_views`；**禁止** 改 `docs/diary/jsonPKmermaid/`、闸口 fixtures。

---

## 可复制 Prompt 正文（整段粘贴到新对话 user）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md
- docs/harness/reviews/README.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md §0（签收关账后更新 INK-P3 / §3 B3）

【Git · 子 Agent 自行建分支 · 与 B1 并行】
- 仓库：ai-ink-brain-api-python
- 专用分支（本任务唯一）：task/chatbi-v3-prompt-injection-closeout-v1
- 禁止共用：task/engineering-tech-graph-gate-d-v2-tasks-v1（闸口 D / B1）
- 禁止在前端仓分支 task/tech-graph-v2-mermaid-audit-v1 或 task/tech-graph-v2-frontend-manifest-v1 上操作
- 建议：git fetch && git checkout main && git pull && git checkout -b task/chatbi-v3-prompt-injection-closeout-v1
- 若 PoC 实现仅在未合并 feature 分支，从该 feature 建上述 closeout 分支，勿与 B1 混线

待审 task（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md

关联 SPEC：
ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md

上一轮审查（工作区指针；子仓若有更新 R4 以子仓为准）：
docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_R4_20260514.md
ai-ink-brain-api-python/docs/harness/reviews/（同名 R4 若存在则优先）

本轮：R4 复审 / CLOSE（task 头部 todo · 实现与 pytest 已落地）

你必须完成：
0. Invoke：更新 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_22_chatbi-v3-prompt-injection-closeout-audit.md 修订记录（勿与 B1 invoke 混文件）。
1. 在分支 task/chatbi-v3-prompt-injection-closeout-v1 上对照 task 验收与 §failure_paths，核对 pytest/实现；产出审查 md 至子仓 docs/harness/reviews/。
2. 若无阻塞：审查「签收/关闭」写 approved；关账 checklist：task 头部 done、git mv active→done、docs/tasks/_views/done.md、PRIORITY_ROADMAP B3/INK-P3（§0）。
3. 若有阻塞：清单交 10 需求帽回填；勿未签收改 done。
4. commit（审查 md + 关账变更）；用户说不要 commit 则跳过。
5. 回复末尾给出 PRIORITY_ROADMAP §3 B3 建议：in_progress → done（日期）。

禁止：扩 scope；未签收改 done；改 jsonPKmermaid/闸口 D fixtures；与 B1 共用分支提交。

合并前：pytest tests -m "not intent_eval and not intent_benchmark" 绿（在本分支执行）。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-20 | 初版：B3 closeout · 分支 `task/chatbi-v3-prompt-injection-closeout-v1` · 与 B1 并行隔离 |
| 2026-05-20 | **CLOSE 完成**：22 帽签收 → 审查 `…_audit_CLOSE_20260520.md` · task→`done/` · pytest 199 passed · PRIORITY_ROADMAP INK-P3/B3 `done（2026-05-20）` |
