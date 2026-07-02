# Harness Sessions · 编排落盘目录

> **用途**：Ops **Session Orchestrator** 的多轮 00 对话、任务单、派工 invoke 与 subagent 交付物的 **Inform 真值**落点。  
> **与工程文档分离**：本目录 **不** 替代 `docs/tasks/`、`docs/_tech_graph/`；避免业务 coding 阶段误读编排草稿。

## 读取纪律

| 角色 | 是否默认读取 |
| --- | --- |
| Session Orchestrator（00 Runtime） | ✅ |
| Ops Chat UI / 维护者 | ✅ 按 `session_id` |
| 业务 30 改码 Agent | ❌ 除非 task 已 promote 到 `docs/tasks/active/` |
| CI / pytest 默认 | ❌ |

## 目录结构（约定）

```text
docs/harness/sessions/
  <session_id>/
    session.meta.yaml       # slug · title · status · created_at · worktree_hint
    task_<slug>_v1.md       # Harness 任务单 · 含 human_gate 表（闸真值）
    invokes/                # 派工 prompt 快照
    deliverables/           # subagent 产出
    events.index.yaml       # 可选 · 关联 ops_run_events
```

## Git 跟踪策略（BLOCKERS B1 · 已定：A）

**决策**：`docs/harness/sessions/**` 已加入 api-python `.gitignore`；运行时 session 目录 **不入库**。

| 项 | 说明 |
| --- | --- |
| **忽略** | `<session_id>/` 下全部内容（meta · task · deliverables · invokes） |
| **可跟踪** | 本 `README.md`（目录约定说明） |
| **持久化** | 本地磁盘 / 部署卷；生产环境按 Host 挂载策略 |
| **导出（可选）** | 维护者可将脱敏 session 快照 export 到 `docs/harness/reviews/` 或本地归档 |
| **敏感数据** | 含 token / 用户原文的 session **永不** commit |

## 授权与 human_gate

- 用户在对话中「授权并开始」→ **必须同步**更新本目录内 task 的 **人工闸表**（如 `HG-EXEC-AUTH`）。
- 再次打开 session：按 `session_id` 加载本目录，恢复 planning / awaiting_auth / dispatched 等状态。

## 规划真值

工作区：[`docs/harness/guides/PLAN_ops_session_orchestrator_v1_zh.md`](../../../../docs/harness/guides/PLAN_ops_session_orchestrator_v1_zh.md)

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-07-01 | 初建目录约定 · 随 Session Orchestrator Epic 实施 |
| 2026-07-02 | S0：补充 B1 Git 策略 · export 说明 · `harness_runtime` session_store |
