# Task · Ops Session S4.2 Promote Conflict（block · overwrite · merge / diff 预览）

> **状态**：`draft` · 00 统筹起草 · 2026-07-03  
> **epic**：Session Orchestrator · S4.2 `ops-session-s4-promote-conflict`  
> **schedule_ref**：SPEC §5.3 · §13 · BLOCKERS B4 · PLAN §5 · §9 D2  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §5.3 Promote 流程 · §13 failure_paths  
> **前置**：`[task_ops_session_s4_verify_api_v1.md](../done/task_ops_session_s4_verify_api_v1.md)` · HG-S4-LOCAL-ACCEPTANCE  
> **配对前端**：[`task_ops_session_s4_promote_conflict_ui_v1.md`](../../../ai-ink-brain/content/tasks/active/task_ops_session_s4_promote_conflict_ui_v1.md)  
> **人拍板**：D2 = **都做** · block + overwrite + merge/diff 预览（PLAN §9）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s4-promote-conflict-api` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s4-promote-conflict-api` |
| **blocks** | S5 promote 运营闭环 |
| **blocked_by** | S4 `ops-session-s4-verify-api` |

### 行为变更 Delta

| 变更 | 类型 | 触达 api/ | 说明 |
| --- | --- | --- | --- |
| promote preview 增加 diff | ADDED | `api/ops/sessions.py` · promote 路由 | 返回源/目标文件 diff 摘要 |
| promote 支持 conflict_action | ADDED | `POST .../promote` body | `block` · `overwrite` · `merge` |
| 新增 merge 草稿生成 | ADDED | `session_store` / deliverables | 生成合并版 task · 人签后落盘 |
| HG-PROMOTE-OVERWRITE 闸 | ADDED | task human_gate | overwrite/merge 必须人签 |
| 授权入口 gate_id | ADDED | `POST .../auth` body | `gate_id` 参数支持签发 `HG-PROMOTE-OVERWRITE` |

---

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 人签 · 2026-07-03 · 派工执行 |
| HG-AUDIT-R1 | `approved` | 30 | 人签 · 2026-07-03 · 20-task-audit 关注点由 30/50 复核 |
| HG-PROMOTE-OVERWRITE | `pending` | — | overwrite/merge 时 maintainer 显式确认 |

---

## 背景与目标

S4 已实现 `PROMOTE_CONFLICT` 仅 block。人拍板 D2 要求 **block + overwrite + merge 都做**，且都须显式二次确认（B4）。本 task 扩展 promote 冲突处理：默认仍 block，可选 overwrite（覆盖目标文件）或 merge（生成合并版 → 人签 → 落盘）。

**完成态一句话**：`POST .../promote` 支持 `conflict_action` 枚举，preview 返回 diff 摘要，overwrite/merge 须经 `HG-PROMOTE-OVERWRITE` 人签。

### 拍板

| # | 决策 |
| --- | --- |
| D1 | 默认策略仍为 **block** · 返回 `PROMOTE_CONFLICT` + diff 摘要 |
| D2 | **overwrite** 须 `confirm=true` + `conflict_action=overwrite` + 二次确认 |
| D3 | **merge** 生成合并版 task 草稿 → UI 预览 → maintainer 签 `HG-PROMOTE-OVERWRITE` → 落盘 |
| D4 | 所有 conflict 处理 **不** auto-commit |

---

## 范围

- [ ] `GET .../promote/preview` 增加 `diff_summary`（行级/字段级 diff）
- [ ] `POST .../promote` body 增加 `conflict_action: block | overwrite | merge`
- [ ] overwrite 分支：覆盖目标 task · 追加 `promoted_from_session` / `promoted_at` / `overwrite_of`
- [ ] merge 分支：生成 `task_<slug>_merged_v1.md` 草稿到 session deliverables → UI 预览 → 人签 `HG-PROMOTE-OVERWRITE` → 落盘到业务仓
- [ ] 新增 `HG-PROMOTE-OVERWRITE` 人签闸
- [ ] 扩展 `POST .../auth` 支持 `gate_id=HG-PROMOTE-OVERWRITE` 人签（不切换 session status）
- [ ] pytest：`tests/harness_runtime/test_session_promote_conflict_s4_2.py` 覆盖 block/overwrite/merge/diff
- [ ] ruff + pytest 全量绿

---

## 非范围

- 不改 S4 已交付的默认 block 行为
- 不处理 graph_delta merge（S5.2）
- 不 auto-commit / auto-merge
- 不新增除 `conflict_action` 外的 promote 参数

---

## 失败路径

| # | Scenario ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- | --- |
| F1 | fp-conflict-block | `conflict_action=block`（默认）且目标已存在 | `409 PROMOTE_CONFLICT` + diff 摘要 | 是（改目标或源后） |
| F2 | fp-overwrite-unconfirmed | `conflict_action=overwrite` 但二次确认缺失 | `409 PROMOTE_OVERWRITE_UNCONFIRMED` | 是 |
| F3 | fp-merge-gate-pending | `conflict_action=merge` 但 `HG-PROMOTE-OVERWRITE` 未签 | `409 PROMOTE_MERGE_BLOCKED` | 是（人签后） |
| F4 | fp-merge-base-missing | merge 时目标或源 task 文件缺失 | `409 PROMOTE_MERGE_BASE_MISSING` | 否 |
| F5 | fp-diff-tool-failed | diff 生成失败（如二进制或超大文件） | `409 PROMOTE_DIFF_FAILED` | 否 |
| F6 | fp-auth-gate-not-found | `gate_id=HG-PROMOTE-OVERWRITE` 不在 task human_gate 表 | `400 GATE_NOT_FOUND` | 否 |

---

## 验收标准

- [ ] preview 返回 diff 摘要
- [ ] overwrite 成功覆盖目标文件并写事件
- [ ] merge 生成草稿 → 人签 → 落盘
- [ ] block 仍为默认且行为不退化
- [ ] pytest 覆盖三种 conflict_action
- [ ] ruff + S1–S4 回归绿

**合并前必绿**：`pytest tests/harness_runtime -q` · `ruff check api/harness_runtime`

---

### 自检结论（执行者，30 回填）

| 项 | 结果 |
| --- | --- |
| **日期** | 2026-07-03 |
| **分支** | `task/ops-session-s4-promote-conflict-api` |

```text
ruff → 0 · promote_conflict_s4_2 → 8 passed · harness 全量 → 56 passed
```

---

## 给 Cursor

`ops-session-s4-promote-conflict-api` · **HG-AUDIT-R1 pending** · 30 不可开工直至人签。
