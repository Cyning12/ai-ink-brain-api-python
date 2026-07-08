# Harness invoke snapshot · 30 execute-code

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_path | docs/harness/tasks/active/task_agently_lab_doc_review_v1.md |
| related_review | ai-ink-brain-api-python-wt-agently-lab/docs/harness/reviews/task_agently_lab_doc_review_v1_audit_R1_20260708.md |
| spec_path | docs/harness/guides/RUNTIME_agently_parallel_learning_track_v0_zh.md |
| git_branch | task/agently-lab-doc-review |
| worktree_root | ai-ink-brain-api-python-wt-agently-lab |
| created_local | 2026-07-08 12:00 CST |
| notes | D1 骨架 + import 边界测试 stub + health/doc-review stub；验证 pytest + ruff |

## 可复制 Prompt 快照（本帽开局用户消息全文）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8

输入：
- 主 task 路径（相对工作区根 Projects/）：
docs/harness/tasks/active/task_agently_lab_doc_review_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致）：
ai-ink-brain-api-python-wt-agently-lab
- 合并前须跑通的验证命令：
pytest tests/agently_lab/ -q && ruff check api/agently_lab
- 关联任务审核书面结论路径：
ai-ink-brain-api-python-wt-agently-lab/docs/harness/reviews/task_agently_lab_doc_review_v1_audit_R1_20260708.md
- 关联 SPEC / 总规：
docs/harness/guides/RUNTIME_agently_parallel_learning_track_v0_zh.md

人工闸状态：维护者已全部签收，HG-TASK-DRAFT approved。

你必须完成：
0. Invoke 快照：将本用户消息全文落盘到 ai-ink-brain-api-python-wt-agently-lab/docs/harness/invokes/by-task/agently-lab-doc-review/。
1. 通读 task 全文：gates_before_code、test_strategy、freeze_id、failure_paths、验收标准、必读列表、非范围。
2. 缺 failure_paths / 验收命令 / 必读未覆盖 → 仅输出阻塞清单，不写业务代码。
3. test_strategy: required 时先写可失败测试再改实现。
4. 在 ai-ink-brain-api-python-wt-agently-lab/ 内按 task 范围改代码；禁止 import harness_runtime 生产图；禁止跨 worktree。
5. 执行验证命令并保留输出要点；修复直至通过或记录环境阻塞。
6. 按 40-self-check.md 回填 task「### 自检结论（执行者）」。
7. 生成下一棒 40 自检 Prompt。
8. 自动 commit：仅本轮路径，禁止 git add -A。
9. 链式下一棒：不自动换帽；交还 00 或输出下一棒。

禁止：未读完 failure_paths 改路由/契约；删除无关重构；口头宣称「已测过」而无命令输出。

本帽目标：D1 骨架 · import 边界测试 stub · api/agently_lab/ 路由 health + doc-review stub · pytest 绿。
```
