# Task · Ops Session S3 Subagent API（dispatch · deep/ReAct · deliverables）

> **状态**：`draft`  
> **epic**：Session Orchestrator · S3 `ops-session-s3-subagent`  
> **schedule_ref**：SPEC §12.1 S3 · §7.1 图拓扑 dispatch 段  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §7 · §9 · §12 S3 · §13  
> **前置**：[`task_ops_session_s2_langgraph_00_api_v1.md`](../done/task_ops_session_s2_langgraph_00_api_v1.md) · 本地验收通过  
> **配对前端**：[`task_ops_session_s3_subagent_ui_v1.md`](../../../ai-ink-brain/content/tasks/active/task_ops_session_s3_subagent_ui_v1.md)  
> **依赖**：P3-1 ReAct fallback · `api/ops/orchestrator` · `api/ops/react_loop.py`

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

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 00 起草 · 2026-07-02 |
| HG-AUDIT-R1 | `pending` | 30 | 20 R1 后人签 |

---

## 背景与目标

S2 已交付 00 层 plan → auth → synthesize；`dispatched` 后 messages 为 **S2 占位**。本 task 扩展 **`session_orchestrator_v1`**：auth 后 `node_dispatch` → subagent router（deep / react / fast）→ `node_review` → `node_00_synthesize`；交付物写入 `deliverables/` · invokes 快照。

**完成态一句话**：`dispatched` 阶段 Session messages **走真实编排**（复用 P1/P3 orchestrator）· 产出落盘 `deliverables/` · 00 合并进 synthesize 回复。

---

## 范围

- [ ] **图扩展**：`node_dispatch` · `node_subagent_router` · `node_subagent_deep|react|fast` · `node_review` · 接通 `node_00_synthesize`
- [ ] **messages 路由**：`dispatched` → dispatch 子图（替换 S2 `handle_dispatched_message` 占位）
- [ ] **deliverables**：session 目录 `deliverables/{run_id}/` · 索引写入 SessionState
- [ ] **invokes 快照**：关键节点事件后可选写 `invokes/` 摘要（只读镜像）
- [ ] **auth approve 路径**：resume 后进入 `node_dispatch`（替换 S2 直 synthesize）
- [ ] **pytest**：`tests/harness_runtime/test_session_orchestrator_s3.py` · subagent 路由 · deliverables 落盘 · 超时 partial
- [ ] **回归**：S2 auth/plan · legacy `/ops/chat/messages`

---

## 非范围

- probe `verify --ci`（**S4**）
- promote 向导（**S4**）
- Ink UI 时间线增强（配对 **前端 task**）
- revise/cancel 行为差分（可 follow-up · 见 backlog thinking task）

---

## 验收标准

- [ ] `dispatched` + messages 触发 deep/fast/react · 非占位文案
- [ ] `deliverables/` 有可追溯产出 · events 含 dispatch/review
- [ ] auth approve 后图路径 dispatch → subagent → synthesize
- [ ] `pytest` + `ruff` 绿

**合并前必绿**：`pytest tests/harness_runtime -q` · S2/S1 回归

---

## 给 Cursor

`ops-session-s3-subagent-api` · Open `ai-ink-brain-api-python/` · **HG-AUDIT-R1 pending 拒开工** · PR 批次暂定 S4 后
