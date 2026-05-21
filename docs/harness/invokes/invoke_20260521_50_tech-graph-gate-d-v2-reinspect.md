# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| template | docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md §3 |
| task_paths | docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md |
| related_review_or_none | docs/harness/reviews/task_engineering_tech_graph_gate_d_v2_tasks_v1_audit_R1_20260520.md |
| git_branch | task/engineering-tech-graph-gate-d-v2-tasks-v1 |
| worktree_root | ai-ink-brain-api-python-wt-gate-d-v2 |
| prerequisite_gate | HG-GATE-D-SIGNOFF（须人改 approved 后再开 50 帽） |
| prior_commit | 6b45c1c（PR-3）· c5b8c62（PR-1） |

## 快照（§3 可复制 Prompt）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md（§一 独立复检；§二 全局验收）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: required 时关注测试与实现关系）
- 根目录 AGENTS.md §8、docs/harness/HARNESS_V2_P0_ACCEPTANCE.md（若本次变更触及合并前必绿子仓）

**开帽前硬停**：读取 task「Harness 元信息」人工闸表。若 **HG-GATE-D-SIGNOFF** 仍为 `pending` → 仅输出须人改 `gate_id` 与路径（`docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md`），**拒开工**；不得代填 `approved`。

输入：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md
- 子仓根（cwd · worktree）：
ai-ink-brain-api-python-wt-gate-d-v2
- 模式：
两者
- diff 或变更范围说明：
git diff c5b8c62^..HEAD
（PR-1 c5b8c62 + PR-3 6b45c1c；分支 task/engineering-tech-graph-gate-d-v2-tasks-v1）
- 任务审核书面结论路径：
docs/harness/reviews/task_engineering_tech_graph_gate_d_v2_tasks_v1_audit_R1_20260520.md

你必须完成：
0. **Invoke 快照**：将本消息全文落盘 `docs/harness/invokes/`（若已有 invoke_20260521_50_* 则增量核对）。

【§一 独立复检】
1. 读取 task「### 自检结论（执行者）」；对照 PR-3 证据：
   - 主 run：`docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260521_091709/`
   - 结论文：`docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`
   - NR：未改 `052803`/`083014`/`102810`；未升 CTX_DUAL_MD 默认
2. 对 §3.1 PR-1、§3.2 PR-3、§3.3 关账（除 HG 仍 pending 项）逐条验收表：pass/fail + 证据。
3. 复跑（或核对日志）：`pytest tests -m "not intent_eval and not intent_benchmark"`；`score_gold_f1` 与表 1/2/3 数字一致。
4. 汇总阻塞合并项；建议是否可合并 PR。

【§二 全局验收 · post_close】
5. 核对 `freeze_id` / `gate_d_v2_tasks_freeze_id` 与 batch_index、结论文一致。
6. checklist：维持 CTX_V2_QUERY、C 系 accepted 未改、结论文 draft→accepted 是否待人签（HG-GATE-D-SIGNOFF）。
7. 若建议关账且无返工：输出「执行路线与 Commit 回溯」（HANDOFF_CLOSE_TRACE）；**勿**在 HG-GATE-D-SIGNOFF 仍为 pending 时宣称 task done 或 git mv。

8. **自动 commit**：落盘复检报告（若有）+ 本 invoke 后按 HANDOFF_AUTO_COMMIT 分仓 commit。
```

---

## 执行结果（50 帽 · 20260521_194037）

| 项 | 值 |
| --- | --- |
| **开帽前硬停** | **是** — `HG-GATE-D-SIGNOFF` 仍为 `pending` |
| **§一 / §二** | **未执行**（拒开工） |
| **复检报告** | 未落盘 |
| **下一动作（人）** | 将 `HG-GATE-D-SIGNOFF` 改为 `approved`（结论文 `accepted` 后）再重开 50 帽 |

