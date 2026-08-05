# Task · Ops Session S5.2 Graph Delta Promote API（graph_delta → _tech_graph/）

> **状态**：`draft` · 00 统筹起草 · 2026-07-03  
> **epic**：Session Orchestrator · S5.2 `ops-session-s5-graph-promote`  
> **schedule_ref**：SPEC §10.3 · BLOCKERS B6 · PLAN §5 · §9 D1  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §10.3 图谱同步 · §5.3 Promote 流程  
> **前置**：S5.1 `ops-session-s5-extract-adr` · HG-AUDIT-R1 approved  
> **配对前端**：[`task_ops_session_s5_graph_promote_ui_v1.md`](./task_ops_session_s5_graph_promote_ui_v1.md) · D1：UI 要做  
> **依赖**：S5.1 ADR 结论  
> **人拍板**：D1 = **UI 要做** · D4 = **完整 checklist 后再确认 Epic 收官**（PLAN §9）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s5-graph-promote-api` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s5-graph-promote-api` |
| **blocks** | Epic §12.3 勾选项 · MVP+ 验收 |
| **blocked_by** | S5.1 `ops-session-s5-extract-adr` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 行为变更 Delta

| 变更 | 类型 | 触达 api/ | 说明 |
| --- | --- | --- | --- |
| graph_delta promote API | ADDED | `api/ops/sessions.py` · 新路由 | 将 session `deliverables/graph_delta/` 复制到目标仓 `_tech_graph/` |
| HG-PROMOTE-GRAPH 闸 | ADDED | task human_gate | 图谱 promote 须人签（B6） |
| 授权入口 gate_id | ADDED | `POST .../auth` body | `gate_id` 参数支持签发 `HG-PROMOTE-GRAPH` |
| graph_delta 预览 | ADDED | `GET .../promote/graph/preview` | 返回待写入 `_tech_graph/` 的文件清单与 diff |
| 事件扩展 | ADDED | `ops_run_events` | `session.graph_promoted` |

---

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 人签 · 2026-07-03 · 派工执行 |
| HG-AUDIT-R1 | `approved` | 30 | 人签 · 2026-07-03 · 20-task-audit 关注点由 30/50 复核 |
| HG-PROMOTE-GRAPH | `pending` | — | 图谱 promote 须 maintainer 显式确认（B6） |

---

## 背景与目标

BLOCKERS B6 已拍板：session 内 `deliverables/graph_delta/` 仅暂存，**人签 `HG-PROMOTE-GRAPH`** 后由 maintainer promote 到目标子仓 `docs/_tech_graph/`。S5.2 将这一流程 API 化，并与 task promote 解耦（可独立 promote graph_delta）。

**完成态一句话**：提供独立 API 让 maintainer 预览并确认后，将 session `graph_delta/` 复制到目标业务仓 `docs/_tech_graph/`，不 auto-commit。

### 拍板

| # | 决策 |
| --- | --- |
| D1 | graph_delta promote **与 task promote 解耦** · 独立路由 |
| D2 | 默认仍为 **暂存** · 须经 `HG-PROMOTE-GRAPH` approved 才复制 |
| D3 | 复制前 preview 目标路径与 diff · 冲突策略同 S4.2（block/overwrite/merge） |
| D4 | 不 auto-commit · 写 `session.graph_promoted` 事件 |

---

## 范围

- [ ] `GET .../promote/graph/preview?target_repo=...`：返回 graph_delta 文件清单、目标路径、diff 摘要
- [ ] `POST .../promote/graph` body `{ target_repo, target_branch, confirm, conflict_action }`：复制到 `_tech_graph/`
- [ ] 支持 `HG-PROMOTE-GRAPH` 人签状态校验
- [ ] 扩展 `POST .../auth` 支持 `gate_id=HG-PROMOTE-GRAPH` 人签（不切换 session status）
- [ ] 冲突处理复用 S4.2 逻辑（block/overwrite/merge）
- [ ] 写 `session.graph_promoted` 事件
- [ ] pytest：`tests/harness_runtime/test_session_graph_promote_s5_2.py`
- [ ] ruff + pytest 全量绿

---

## 非范围

- 不改 `graph_delta` 生成逻辑（S3 subagent 已负责）
- 不自动运行 `_tech_graph` CI（仅触发事件，CI 由业务仓 workflow 监听）
- 不替代 task promote
- 不处理 `_tech_graph` 以外的图谱目录

---

## 失败路径

| # | Scenario ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- | --- |
| F1 | fp-graph-gate-pending | `HG-PROMOTE-GRAPH` 未签 | `409 GRAPH_PROMOTE_GATE_PENDING` | 是（人签后） |
| F2 | fp-graph-empty | session 无 `graph_delta/` | `409 GRAPH_DELTA_EMPTY` | 否 |
| F3 | fp-graph-conflict | 目标 `_tech_graph/` 文件已存在且 conflict_action=block | `409 GRAPH_PROMOTE_CONFLICT` + diff | 是 |
| F4 | fp-graph-target-repo-invalid | target_repo 不在允许列表 | `400 INVALID_TARGET_REPO` | 否 |
| F5 | fp-graph-copy-failed | 文件复制失败 | `500 GRAPH_PROMOTE_COPY_FAILED` | 是 |
| F6 | fp-auth-gate-not-found | `gate_id=HG-PROMOTE-GRAPH` 不在 task human_gate 表 | `400 GATE_NOT_FOUND` | 否 |

---

## 验收标准

- [ ] graph_delta preview 返回文件清单与 diff
- [ ] 人签 `HG-PROMOTE-GRAPH` 后才可执行复制
- [ ] 复制后目标仓出现对应文件，无 auto-commit
- [ ] `session.graph_promoted` 事件写入
- [ ] pytest 覆盖 gate/conflict/empty/copy-failed
- [ ] ruff + S1–S4 回归绿

**合并前必绿**：`pytest tests/harness_runtime -q` · `ruff check api/harness_runtime`

---

### 自检结论（执行者，30 回填）

| 项 | 结果 |
| --- | --- |
| **日期** | 2026-07-03 |
| **分支** | `task/ops-session-s5-graph-promote-api` |

```text
ruff → 0 · graph_promote_s5_2 → 12 passed · harness 全量 → 59 passed
```

---

## 给 Cursor

`ops-session-s5-graph-promote-api` · **HG-AUDIT-R1 pending** · 30 不可开工直至人签。
