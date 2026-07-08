# Task Audit · Ops Chat ← Session 能力下沉 · P0 + P1 · R1

| 字段 | 值 |
| --- | --- |
| **task_path** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **audit_round** | R1 |
| **date** | 2026-07-08 |
| **auditor** | 00 统筹 fallback（子 Agent 调用 transient 失败） |
| **invoke_snapshot** | `docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260708_0000_22_ops_chat_session_sink_p0_p1_v1.md` |
| **related_plan** | `docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md` |
| **paired_frontend_task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_frontend_v1.md` |

---

## 审查结论摘要

| 维度 | 结论 |
| --- | --- |
| 范围清晰度 | ✅ P0/P1 八子项明确；P2 明确排除 |
| 非范围 | ✅ Session promote、生产图修改、Agently lab 已排除 |
| 依赖与引用 | ✅ 已链 PLAN、SNAPSHOT、gap matrix、核心代码入口 |
| 验收标准 | ⚠️ 可观测，但缺单测/集成测命令粒度；缺 M0/M1  checklist 细化 |
| failure_paths | ⚠️ 有 4 条，但缺「可观测」与「可重试」列，部分缺降级后验证方式 |
| test_strategy | ✅ 已标 `required`；❌ 缺 `test_strategy_note` |
| 执行帽必读 | ❌ 未列出 |
| 元信息完整度 | ❌ 缺 `audit_profile`、`experience_capture`、`kpi_rubric`、`kpi_aggregator` |
| human_gate | ✅ HG-TASK-DRAFT 存在且 pending；不代签 approved |

**综合判定**：**blocked-for-revision**。task 骨架已完整，但 HARNESS_V2_PLAN §5 推荐字段（failure_paths 可观测/可重试、test_strategy_note、执行帽必读、元信息）缺失，20-task-audit 不宜直接放行 30。

---

## 阻塞项（必须先回填）

| # | 阻塞项 | 原因 | 建议回填位置 |
| --- | --- | --- | --- |
| B1 | `failure_paths` 表结构不足 | 仅「触发/行为」两列，缺「可观测/可重试/验证命令」 | task `## 失败路径` 改为 5 列表 |
| B2 | 缺 `test_strategy_note` | `required` 必须有理由，且需说明「先写失败测试再实现」的证据 | task 新增 `## test_strategy_note` |
| B3 | 缺执行帽必读列表 | 30 执行前须明确必读文件，避免误改 Session 图或跨 worktree | task 新增 `## 执行帽必读列表` |
| B4 | 缺 Harness 元信息 | `audit_profile`、`experience_capture`、`kpi_rubric`、`kpi_aggregator` 未填 | task 头部元信息表 |

---

## 非阻塞建议

| # | 建议 | 说明 |
| --- | --- | --- |
| N1 | P0-1 Review 单测 V1–V4 明确命令 | 验收标准中可写 `pytest tests/ops/test_review_*.py` |
| N2 | P0-3 transcript 集成测用例 | 写清「第二轮『它』继承 issue 号」的测试脚本或 curl 步骤 |
| N3 | P1-1 migration 回滚验证 | 验收标准写 `alembic downgrade -1` 或对应 downgrade 命令 |
| N4 | 行为变更节补充「REMOVED」 | 若 Review 逻辑从原处删除，需说明旧入口废弃 |

---

## 是否建议执行帽开工

**否**。须先走 **10-task 修订** 回填 B1–B4，再经 **20-task-audit R2** 审查；R2 无阻塞后，维护者签 **HG-TASK-DRAFT approved** 方可派 30。

---

## 签收 / 关闭

- [ ] 10-task 修订完成 B1–B4
- [ ] 20-task-audit R2 审查通过
- [ ] HG-TASK-DRAFT approved
- [ ] 派 30 执行帽

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/00-orchestrator.md

【目标与上下文】
线 B Chat sink BE task 经 20-task-audit R1 判定 blocked-for-revision，需回填以下项：
1. failure_paths 表增加「可观测 / 可重试 / 验证命令」列；
2. 新增 test_strategy_note；
3. 新增执行帽必读列表；
4. task 头部补 audit_profile / experience_capture / kpi_rubric / kpi_aggregator。

【已有材料路径或粘贴说明】
docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md
docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260708.md

【是否按任务审核文档回填】
docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260708.md

工作目录：Projects/

你必须完成：
0. Invoke 快照落盘到 Projects/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260708_0000_10_ops_chat_session_sink_p0_p1_v1.md。
1. 按 R1 审查回填清单修改 task，不扩大 scope，不改业务代码。
2. 保持 human_gate HG-TASK-DRAFT pending。
3. 生成下一棒 20-task-audit R2 Prompt。
4. 自动 commit：仅本轮路径，禁止 git add -A。

Judgment: experience_capture / gate/risk / hat_self
```

---

## Judgment

- **experience_capture**: `required` — Chat Session Sink 涉及 Review/Events/Transcript/Checkpoint/Router 五个运行时契约变更，失败路径与联调经验具备跨 Epic 复用价值。
- **gate/risk**: `HG-TASK-DRAFT` pending 阻塞 30；R1 因字段缺失 blocked，需 10-task 修订 + R2。
- **hat_self**: `pass-with-notes` — 审查结论与回填清单已落盘；notes：子 Agent 调用 transient 失败，由 00 fallback 完成。
