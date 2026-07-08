# Invoke Snapshot · 30 执行帽 · retry

| 项 | 内容 |
| --- | --- |
| **role** | `30-execute-code` |
| **task** | `docs/harness/tasks/active/task_agently_lab_doc_review_v1.md` |
| **worktree** | `ai-ink-brain-api-python-wt-agently-lab/` |
| **git_branch** | `task/agently-lab-doc-review` |
| **base_commit** | `781b6c6f` |
| **timestamp** | `2026-07-08T13:30:00+08:00` |
| **human_gate** | `HG-TASK-DRAFT: approved` |
| **verification_target** | `pytest tests/agently_lab/ -q && ruff check api/agently_lab` |
| **d1_goal** | `api/agently_lab/` 路由 health + doc-review stub；import 边界测试 stub；pytest 绿 |

---

## 用户消息全文

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8

输入：
- 主 task 路径（相对工作区根 Projects/）：
docs/harness/tasks/active/task_agently_lab_doc_review_v1.md
- 逻辑子仓（相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录：
ai-ink-brain-api-python-wt-agently-lab
- 合并前须跑通的验证命令：
pytest tests/agently_lab/ -q && ruff check api/agently_lab
- 关联任务审核书面结论路径：
ai-ink-brain-api-python-wt-agently-lab/docs/harness/reviews/task_agently_lab_doc_review_v1_audit_R1_20260708.md
- 关联 SPEC / 总规：
docs/harness/guides/RUNTIME_agently_parallel_learning_track_v0_zh.md

人工闸状态：HG-TASK-DRAFT approved（维护者已全部签收）。

重要上下文：
- 上一轮 30 执行被中断，仅留下 invoke 快照 @ `781b6c6f`。
- task 正文中已有部分「### 自检结论（执行者）」，由中断的 Agent 写入；本轮完成后请覆盖/更新为完整结论。
- 本轮必须完成 D1 目标：`api/agently_lab/` 路由 health + doc-review stub、import 边界测试 stub、pytest 绿。

你必须完成：
0. Invoke 快照：将本用户消息全文落盘到 `ai-ink-brain-api-python-wt-agently-lab/docs/harness/invokes/by-task/agently-lab-doc-review/invoke_20260708_1330_30_agently_lab_doc_review_v1_retry.md`。
1. 通读 task 全文，重点看 failure_paths、验收标准、非范围、必读列表。
2. 检查当前 worktree 状态；继承已有代码（如果有），补完 D1 骨架。
3. test_strategy: required 时先写可失败测试再改实现。
4. 在 ai-ink-brain-api-python-wt-agently-lab/ 内改代码；禁止 import `harness_runtime` 生产图；禁止跨 worktree。
5. 执行验证命令并保留输出要点；修复直至通过。
6. 覆盖/更新 task「### 自检结论（执行者）」。
7. 生成下一棒 40 自检 Prompt。
8. 自动 commit：仅本轮路径，禁止 git add -A。
9. 链式下一棒：不自动换帽；交还 00 或输出下一棒。

禁止：未读完 failure_paths 改路由/契约；删除无关重构；口头宣称「已测过」而无命令输出。

本帽目标：D1 骨架 · import 边界测试 stub · `api/agently_lab/` 路由 health + doc-review stub · pytest 绿。
```
