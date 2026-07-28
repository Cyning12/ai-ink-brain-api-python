# Task：Harness P0 R3 — change_status JSON + Cursor 薄命令

> **状态**：done（2026-05-30 验收通过 · HARNESS-P0-STATUS-CURSOR@2026-05-30）  
> **schedule_ref**：RECENT §0.6 · Loop R3  
> **母单**：[`task_harness_p0_openspec_tdd_loop_v1.md`](task_harness_p0_openspec_tdd_loop_v1.md)  
> **前置**：R2 在 `done/`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `recommended` |
| **freeze_id** | `HARNESS-P0-STATUS-CURSOR@2026-05-30` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **task_slug** | `p0-status-cursor` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 行为变更（Delta）

### ADDED

- **Requirement**：Agent 可查询 task Harness 状态 JSON。  
  - **Scenario**：`status-json` — GIVEN active task WHEN status --json THEN 含 pending gates 与建议下一帽。

---

## 范围

- [x] `tools/harness_change_status.py`（O5）：读 task + human_gate → JSON。  
- [x] `.cursor/commands/harness-validate.md`、`harness-status.md`（O6；薄封装指向 tools）。  
- [x] `tests/test_harness_change_status.py`（最小）。  
- [x] 复用 R1 validate 解析逻辑（DRY，同模块或 shared）。

## 非范围

- 通用 PyPI 包。  
- 改业务 api/。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| F1 | `fp-status-json` | task 路径不存在 | CLI exit 1 | 修正路径 | stderr 提示 |
| F2 | `fp-status-gate-pending` | pending gate 阻塞帽 | JSON `pending_gates` 非空 | 人批 gate | suggested_next_hat 调整 |

---

## 验收标准

- [x] `python tools/harness_change_status.py --task docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md --json` 输出合法 JSON。  
- [x] Cursor 命令文件存在且指向本仓真值路径。  
- [x] 全量 pytest 绿。

---

### 自检结论（执行者）

| # | 验收项 | 结果 | 证据 |
| --- | --- | --- | --- |
| V1 | change_status 单测 | **pass** | 2 passed |
| V2 | 母单 JSON | **pass** | `pending_gates: []` · `task_slug: p0-openspec-tdd` |
| V3 | Cursor commands | **pass** | `.cursor/commands/harness-{validate,status}.md` |
| V4 | 全量 Required pytest | **pass** | 269 passed |

---

## 实现备忘

| 项 | 内容 |
|----|------|
| 涉及文件 | `tools/harness_change_status.py`、`tests/test_harness_change_status.py`、`.cursor/commands/harness-*.md` |
| DRY | import `harness_task_validate` + `harness_human_gate_check` |

---

## 给 Cursor

Loop R3、O5、O6、R2 须 done
