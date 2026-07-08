# Task Audit · Ops Chat ← Session 能力下沉 · P0 + P1 · R2

| 字段 | 值 |
| --- | --- |
| **task_path** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **audit_round** | R2 |
| **date** | 2026-07-08 |
| **auditor** | 20-task-audit Agent |
| **invoke_snapshot** | `Projects/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_20260708_0000_22_ops_chat_session_sink_p0_p1_v1_R2.md` |
| **prior_review** | `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260708.md` |
| **related_plan** | `docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md` |
| **paired_frontend_task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_frontend_v1.md` |

---

## 审查结论摘要

对照 R1 回填清单逐项核验：

| R1 阻塞项 | 当前 task 状态 | 结论 |
| --- | --- | --- |
| B1 · `failure_paths` 缺可观测/可重试/验证命令列 | `## 失败路径` 已改为 5 列表（触发 / 系统行为 / 可观测 / 可重试 / 验证命令），4 条路径全部 actionable | ✅ 已回填 |
| B2 · 缺 `test_strategy_note` | 头部元信息表与独立 `## test_strategy_note` 均说明 `required` 理由，并给出最终验证命令 `pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark"` + `ruff check api/ops` | ✅ 已回填 |
| B3 · 缺执行帽必读列表 | 新增 `## 给执行帽的必读列表`，覆盖 PLAN、SNAPSHOT、gap matrix、子仓 AGENTS/PROJECT_CONFIG、cursor rules、现有入口、链式常模共 7 项 | ✅ 已回填 |
| B4 · 缺 Harness 元信息 | 头部已填 `audit_profile: full`、`experience_capture: required`、`kpi_rubric: KPI_RUBRIC_v1_2`、`kpi_aggregator: CLOSE` | ✅ 已回填 |

| 维度 | 结论 |
| --- | --- |
| 范围清晰度 | ✅ P0/P1 八子项明确；P2 明确排除 |
| 非范围 | ✅ Session promote、生产图修改、Agently lab 已排除 |
| 依赖与引用 | ✅ 已链 PLAN、SNAPSHOT、gap matrix、核心代码入口 |
| 验收标准 | ✅ M0/M1 可观测；最终验证命令与 PLAN §6 一致 |
| `failure_paths` | ✅ 结构完整，含可观测 / 可重试 / 验证命令 |
| `test_strategy` | ✅ `required` + note，符合 HARNESS_V2_PLAN §5.1 |
| 执行帽必读 | ✅ 列表齐全，`gates_before_code` 语义明确 |
| 元信息完整度 | ✅ `audit_profile`、`experience_capture`、`kpi_rubric`、`kpi_aggregator` 已填 |
| `human_gate` | ✅ HG-TASK-DRAFT / HG-AUDIT-R1 均 pending；本帽不代签 approved |

**综合判定**：**R2 通过（零阻塞）**。R1 列出的 B1–B4 已全部回填，task 满足进入 30 执行编码帽的文档门槛。

---

## 阻塞项

无。

---

## 非阻塞建议

| # | 建议 | 说明 |
| --- | --- | --- |
| N1 | 30 开工首日先按必读列表确认现有入口文件未变 | `api/ops/chat_service.py`、`orchestrator/core.py`、`react_loop.py`、`store/runs.py` 是 P0-1/P0-3/P0-4 改动基础 |
| N2 | `failure_paths` 中「Supabase artifact 写失败」的可重试为「是」 | 30 实现时务必保证幂等键/去重，避免重试产生重复 event |
| N3 | P1-1 migration 回滚验证 | 虽在验收标准 M1 中提及，建议 30 在自检时显式跑 `alembic downgrade -1` 并回填结果 |
| N4 | 线 C 前端 task 须在 D3 前完成其 own 20-task-audit R1 | 本审查仅覆盖线 B BE task；B↔C 联调依赖以 Master Dispatch §2 日历为准 |

---

## 是否建议执行帽开工

**文档层面：R2 已可放行 30**；但 **实际开工须同时满足**：
1. 维护者将 `HG-TASK-DRAFT` 改为 `approved`；
2. 维护者将 `HG-AUDIT-R1` 改为 `approved`。

本帽 **不代签** 任何人人工闸。

---

## 签收 / 关闭

- [x] R1 回填清单 B1–B4 已闭合
- [x] 20-task-audit R2 审查通过
- [ ] HG-TASK-DRAFT approved（仅人签）
- [ ] HG-AUDIT-R1 approved（仅人签）
- [ ] 派 30 执行帽
- [ ] 后续 40 自检 / 50 复检 / CLOSE 关账按 `audit_profile: full` 与 `kpi_aggregator: CLOSE` 执行

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8

输入（占位符已全部替换；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/ruff 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" && ruff check api/ops
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R2_20260708.md
- 关联 SPEC / 总规（无则「无」）：
docs/harness/guides/PLAN_ops_chat_session_sink_p0_p1_v1_zh.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将本用户消息全文按 docs/harness/invokes/README.md 落盘到 ai-ink-brain-api-python/docs/harness/invokes/by-task/ops-chat-session-sink-p0-p1/invoke_YYYYMMDD_HHMM_30_ops_chat_session_sink_p0_p1_v1.md（含元数据表 + 快照 fenced code）。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate。若任一对本帽（30）为 pending → 仅输出须人改的 gate_id 与路径，拒开工；禁止代填 approved。
1. 通读 task 全文：头部 gates_before_code、audit_profile、orchestration、chain_prompt、test_strategy / test_strategy_note、failure_paths、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足 → 仅输出 Markdown 阻塞清单，不写业务实现代码。
3. test_strategy: required 时：先增加或调整可失败的自动化测试（或与实现同 PR 且满足 red-green 语义），再改实现；禁止只写实现、后补测。
4. 在 ai-ink-brain-api-python/ 内按 task P0→P1 范围改代码/配置；禁止静默扩大 scope；禁止改 Session 生产图或 Agently lab worktree。
5. 执行上述 VERIFY_COMMAND，保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 40-self-check.md 将结论与命令摘要回填至 task 正文「### 自检结论（执行者）」。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行。
8. 自动 commit：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python/ commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。
9. 链式下一棒：若 task 由 00 / Lead 按 PROMPT_claude_chain_serial_v2.md 编排 → 不在本帽同会话自动换帽；仅输出下一棒 §3 或交还父 Agent。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出。

Judgment（本帽 · 对话末尾必填）：
- experience_capture: 维持 required（运行时契约/失败路径/联调经验具备跨 Epic 复用价值）
- gate/risk: 无（HG-TASK-DRAFT / HG-AUDIT-R1 已 approved 后）
- hat_self: pass | pass-with-notes | blocked
```

---

## Judgment

- **experience_capture**: `required` — Chat Session Sink 涉及 Review/Events/Transcript/Checkpoint/Router 五个运行时契约变更，失败路径与 B↔C 联调经验具备跨 Epic 复用价值。维持 task 当前档位。
- **gate/risk**: `HG-TASK-DRAFT` pending、`HG-AUDIT-R1` pending 均阻塞 30；本帽建议两者均可在 R2 结论落盘后由维护者签为 approved。
- **hat_self**: `pass` — R2 零阻塞，审查结论、下一棒 Prompt 与 commit 均按规范落盘。
