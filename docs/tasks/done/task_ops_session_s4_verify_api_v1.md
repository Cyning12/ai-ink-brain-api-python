# Task · Ops Session S4 Verify API（probe subprocess · promote · verify 阻塞）

> **状态**：`done（2026-07-02 · HG-S4-LOCAL-ACCEPTANCE）`  
> **epic**：Session Orchestrator · S4 `ops-session-s4-verify`  
> **schedule_ref**：SPEC §5.3 · §10.4–§10.5 · §12.1 S4 · BLOCKERS B4/B7  
> **关联 SPEC**：`[SPEC_ops_session_orchestrator_v1_zh.md](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md)` §5.3 · §9.2 · §10 · §12 S4  
> **前置**：`[task_ops_session_s3_subagent_api_v1.md](../done/task_ops_session_s3_subagent_api_v1.md)` · HG-S3-LOCAL-ACCEPTANCE  
> **配对前端**：[`task_ops_session_s4_verify_ui_v1.md`](../../../ai-ink-brain/content/tasks/done/task_ops_session_s4_verify_ui_v1.md)  
> **依赖**：harness-probe **v0.10.0+**（subprocess CLI · **禁止** Runtime import probe）

---



## Harness 元信息


| 字段                | 值                                |
| ----------------- | -------------------------------- |
| **task_slug**     | `ops-session-s4-verify-api`      |
| **module_id**     | `OPS-SESSION-ORCH`               |
| **freeze_id**     | `OPS-SESSION-ORCH-SPEC-V1`       |
| **test_strategy** | `required`                       |
| **worktree_root** | `ai-ink-brain-api-python/`       |
| **git_branch**    | `task/ops-session-s4-verify-api` |
| **blocks**        | S5 `ops-session-s5-extract`      |
| **blocked_by**    | S3 `ops-session-s3-subagent-api` |




### 人工闸 `human_gate`


| human_gate_id | status     | blocks_hats       | 说明                 |
| ------------- | ---------- | ----------------- | ------------------ |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 00 起草 · 2026-07-02 |
| HG-AUDIT-R1   | `approved` | 30                | 20 R1 后人签          |


---



## 背景与目标

S3 已交付 subagent 派工与 deliverables。本 task 接入 **harness-probe subprocess**（B7）与 **00 半自动 promote**（B4）：maintainer 确认后将 session 内 task 草稿复制到业务仓 · promote **前** `verify --ci` 阻塞 · 产出 `verify_report.json` · 写 `session.promoted` 事件。

**完成态一句话**：`POST .../promote` 在 verify 通过后复制 task 到目标子仓 `docs/tasks/active/`（或前端 `content/tasks/active/`）· **不** auto-commit · probe 仅 subprocess。

### 拍板（00 统筹 · SPEC/BLOCKERS）


| #   | 决策                                                                                        |
| --- | ----------------------------------------------------------------------------------------- |
| D1  | **唯一路径**：`api/harness_runtime/adapters/probe_runner.py` → `subprocess` CLI                |
| D2  | promote **前** `verify --ci` **阻塞**；auth 后 `task validate` **可选 warn-only**                |
| D3  | `target_repo` 枚举：`ai-ink-brain-api-python` | `ai-ink-brain` · `target_branch` 默认各仓 `main` |
| D4  | 冲突：目标已存在同名 task → `409 PROMOTE_CONFLICT` + diff 摘要                                        |
| D5  | Vercel **不**同步全量 verify · API 可返回「仅本地/GHA」提示                                              |


---



## 范围

- [x] `adapters/probe_runner.py`：`task_validate` · `verify_task`（`HARNESS_PROBE_BIN` · `HARNESS_PROBE_REPO_ROOT` · timeout）
- [x] `POST /ops/sessions/{id}/promote`：body `{ target_repo, target_branch, confirm: true }` · maintainer 显式确认
- [x] **promote 预览**：`GET .../promote/preview`（或 promote dry-run）· 源路径 · 目标路径 · gate 表 · diff 摘要
- [x] **复制逻辑**：session `task_*.md` → 业务仓 active task · 追加 `promoted_from_session` / `promoted_at` · 同步 `HG-PROMOTE` / `HG-EXEC-AUTH`（按 SPEC §6.1）
- [x] **verify 落盘**：`deliverables/{run_id}/verify_report.json` · `ops_run_events`
- [ ] **auth 后可选**：`task validate` on session 草稿（warn · 不阻塞 dispatch）
- [x] **pytest**：`tests/harness_runtime/test_session_promote_s4.py` · mock subprocess · conflict · verify fail 阻塞
- [x] **回归**：S1–S3 harness_runtime · sessions REST

---



## 非范围

- `import harness_probe` / MCP（**禁止** · §11.2）
- auto-commit / auto-merge / auto-PR（B4 · maintainer 在 IDE/gh 侧操作）
- graph_delta promote 到 `_tech_graph/`（**B6 · S5+**）
- Ink promote 向导 UI（配对 **前端 task**）
- probe v0.10.1 `--repo-root` 未就绪时：可 **validate + 人工 verify** 过渡（须在 task 记录）

---



## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-probe-unavailable | probe CLI 不存在 | `503 PROBE_UNAVAILABLE` |
| F2 | fp-verify-failed | verify exit≠0 | `409 VERIFY_FAILED` · 不复制文件 |
| F3 | fp-promote-conflict | 目标 task 已存在 | `409 PROMOTE_CONFLICT` |
| F4 | fp-session-status-invalid | 非 `dispatched` / gate 未满足 | `409 SESSION_STATUS_INVALID` |


---



## 验收标准

- [x] promote 预览可返回源/目标/gate 摘要
- [x] verify 失败时 promote **不**写业务仓
- [x] verify 通过后复制 task · `session.promoted` 事件
- [x] subprocess 测试 mock 覆盖 validate/verify
- [x] `pytest` + `ruff` 绿 · S1–S3 回归

**合并前必绿**：`pytest tests/harness_runtime -q`

---

### 自检结论（执行者）

| 项 | 结果 |
| --- | --- |
| **日期** | 2026-07-02 |
| **分支** | `task/ops-session-s4-verify-api` |

```text
ruff → 0 · promote_s4 5 passed · harness 57 passed
```

---

## 给 Cursor

`ops-session-s4-verify-api` · **HG-AUDIT-R1 approved** · 30 done · 待人签 checklist