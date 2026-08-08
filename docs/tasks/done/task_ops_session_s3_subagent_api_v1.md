# Task · Ops Session S3 Subagent API（dispatch · deep/ReAct · deliverables）

> **状态**：`done（2026-07-02 本地验收通过）`  
> **epic**：Session Orchestrator · S3 `ops-session-s3-subagent`  
> **schedule_ref**：SPEC §12.1 S3 · §7.1 图拓扑 dispatch 段  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §7 · §9 · §12 S3 · §13  
> **前置**：[`task_ops_session_s2_langgraph_00_api_v1.md`](task_ops_session_s2_langgraph_00_api_v1.md) · 本地验收通过  
> **配对前端**：[`task_ops_session_s3_subagent_ui_v1.md`](../../../ai-ink-brain/content/tasks/done/task_ops_session_s3_subagent_ui_v1.md)  
> **本地验收**：[`CHECKLIST_ops_session_s3_local_acceptance_v1_zh.md`](../../../docs/harness/reviews/CHECKLIST_ops_session_s3_local_acceptance_v1_zh.md) · HG-S3-LOCAL-ACCEPTANCE  
> **50 复检**：[`task_ops_session_s3_subagent_reinspect_R1_20260702.md`](../../../docs/harness/reviews/task_ops_session_s3_subagent_reinspect_R1_20260702.md)  
> **PR**：暂缓 · 与 S4 **合并批次**开 PR（`task/ops-session-s3-subagent-api` · `1fbb5a7d`）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s3-subagent-api` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s3-subagent-api` |
| **blocks** | S4 `ops-session-s4-verify` |
| **blocked_by** | S2 `ops-session-s2-langgraph-00-api` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 00 起草 · 2026-07-02 |
| HG-AUDIT-R1 | `approved` | 30 | 20 R1 后人签 · 2026-07-02 |

---

## 背景与目标

S2 已交付 00 层 plan → auth → synthesize；`dispatched` 后 messages 为 **S2 占位**。本 task 扩展 **`session_orchestrator_v1`**：auth 后 `node_dispatch` → subagent router（deep / react / fast）→ `node_review` → `node_00_synthesize`；交付物写入 `deliverables/` · invokes 快照。

**完成态一句话**：`dispatched` 阶段 Session messages **走真实编排**（复用 P1/P3 orchestrator）· 产出落盘 `deliverables/` · 00 合并进 synthesize 回复。

---

## 范围

- [x] **图扩展**：`node_dispatch` · `node_subagent` · `node_review` · 接通 `node_00_synthesize`
- [x] **messages 路由**：`dispatched` → 真实编排（替换 S2 占位）
- [x] **deliverables**：`deliverables/{run_id}/` · GET 列表端点
- [x] **invokes 快照**：dispatch 节点写 `invokes/`
- [x] **auth approve 路径**：resume → `node_dispatch`
- [x] **pytest**：`tests/harness_runtime/test_session_orchestrator_s3.py`
- [x] **回归**：S2 auth/plan · legacy `/ops/chat/messages`

---

## 非范围

- probe `verify --ci`（**S4**）
- promote 向导（**S4**）

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-not-dispatched | 非 `dispatched` 发 messages | `409 SESSION_STATUS_INVALID` |
| F2 | fp-subagent-timeout | 深析超时 | 结构化错误 · events 记录 |
| F3 | fp-deliverable-missing | deliverables 目录不可写 | `500` · 不静默 |

---

## 验收标准

- [x] `dispatched` + messages 触发 deep/fast/react · 非占位文案
- [x] `deliverables/` 有可追溯产出 · events 含 dispatch/review
- [x] auth approve 后图路径 dispatch → subagent → synthesize
- [x] `pytest` + `ruff` 绿

---

### 自检结论（执行者）

| 项 | 结果 |
| --- | --- |
| **日期** | 2026-07-02 |
| **分支** | `task/ops-session-s3-subagent-api` |
| **commit** | `1fbb5a7d` · `98068fdb` |

**命令与退出码**

```text
pytest tests/harness_runtime/ ... → 51 passed
ruff check api/harness_runtime api/ops/sessions.py → 0
```

**浏览器验收**：maintainer 签收 · session `sess_20260702_7c33qci6` · 2026-07-02

---

## 给 Cursor

`ops-session-s3-subagent-api` · **done** · 下一棒 S4 `ops-session-s4-verify-api`
