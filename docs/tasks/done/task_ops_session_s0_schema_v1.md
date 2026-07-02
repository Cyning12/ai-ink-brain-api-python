# Task · Ops Session S0 Schema（sessions 落盘 · gate_sync · harness_runtime 骨架）

> **状态**：`done（2026-07-02 验收通过）`  
> **epic**：Session Orchestrator · S0 `ops-session-s0-schema`  
> **schedule_ref**：SPEC §12.1 S0 · MVP 首片（S0+S1+S2）  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) · `spec-signed` v1.3  
> **20-task-audit**：[`task_ops_session_s0_schema_v1_audit_R1_20260702.md`](../harness/reviews/by-task/ops-session-s0-schema/task_ops_session_s0_schema_v1_audit_R1_20260702.md) · conditional_pass  
> **50-reinspect**：[`reinspect_ops-session-s0-schema_20260702_v1.md`](../reinspect_results/reinspect_ops-session-s0-schema_20260702_v1.md)  
> **BLOCKERS**：[`BLOCKERS.md`](../../../docs/harness/invokes/by-task/ops-session-orchestrator/BLOCKERS.md) · B1 · B5 closed

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s0-schema` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s0-schema` |
| **blocks** | S1 `ops-session-s1-multiturn` · S2 `ops-session-s2-langgraph-00` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 2026-07-02 |
| HG-AUDIT-R1 | `approved` | 30 | 20 R1 后人签 · 2026-07-02 |

---

## 范围（已交付）

- [x] **B1 · Git 忽略**：`.gitignore` `docs/harness/sessions/**` + `!README.md`
- [x] **sessions README**：B1 Git 策略 · export 说明
- [x] `session.meta.yaml` schema v1 · Pydantic
- [x] `session_store/` · `gate_sync/`
- [x] `harness_runtime/` 骨架 B5
- [x] import 边界测试 · unit pytest

---

## 行为变更（Delta）

### ADDED

- Session 文件 Inform 真值：`api/harness_runtime` · `create_session` / `gate_sync`

### MODIFIED

- `docs/harness/sessions/README.md`：B1 Git 策略

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 |
| --- | --- | --- | --- | --- |
| F1 | `fp-session-schema-unsupported` | schema_version 无效 | `SESSION_SCHEMA_UNSUPPORTED` | 否 |
| F2 | `fp-session-id-mismatch` | 目录名 ≠ session_id | `SESSION_ID_MISMATCH` | 否 |
| F4 | `fp-gate-table-missing` | 无 human_gate 表 | `GATE_TABLE_MISSING` | 否 |

---

## 验收标准

- [x] `docs/harness/sessions/**` gitignore · README 与 SPEC §5.5 一致
- [x] `session.meta.yaml` v1 校验含 `SESSION_SCHEMA_UNSUPPORTED`
- [x] `session_id` 与目录名不一致拒绝加载（F2）
- [x] `gate_sync` patch + `gate_summary` 同步（F4/F5）
- [x] `harness_runtime` 无 RAG/ingest/probe 运行时 import
- [x] `pytest tests/harness_runtime` 26 passed
- [x] 无 LangGraph 节点 · 无 `/ops/sessions` 路由

---

## 实现备忘

| 项 | 内容 |
| --- | --- |
| 涉及文件 | `api/harness_runtime/**` · `tests/harness_runtime/**` · `.gitignore` · `docs/harness/sessions/README.md` |
| 入口 API | `create_session` · `load_meta` · `patch_gate_and_sync` |
| session 模板闸 | HG-SESSION-PLAN · HG-EXEC-AUTH · HG-AUDIT-R1 · HG-PROMOTE（SPEC §6.1） |

---

## 自检结论（执行者 · 40 帽）

| 项 | 结果 |
| --- | --- |
| `pytest tests/harness_runtime -q` | **pass** · 26 passed |
| `ruff check api/harness_runtime tests/harness_runtime` | **pass** |
| `python tools/harness_task_validate.py docs/tasks/done/task_ops_session_s0_schema_v1.md` | **pass** |

---

## 给 Cursor

S0 **CLOSE** · 下一棒 S1 `ops-session-s1-multiturn`
