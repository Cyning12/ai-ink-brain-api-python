# Task：Harness P0 R3 — change_status JSON + Cursor 薄命令

> **状态**：pending  
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

---

## 行为变更（Delta）

### ADDED

- **Requirement**：Agent 可查询 task Harness 状态 JSON。  
  - **Scenario**：`status-json` — GIVEN active task WHEN status --json THEN 含 pending gates 与建议下一帽。

---

## 范围

- [ ] `tools/harness_change_status.py`（O5）：读 task + human_gate → JSON。  
- [ ] `.cursor/commands/harness-validate.md`、`harness-status.md`（O6；薄封装指向 tools）。  
- [ ] `tests/test_harness_change_status.py`（最小）。  
- [ ] 复用 R1 validate 解析逻辑（DRY，同模块或 shared）。

## 非范围

- 通用 PyPI 包。  
- 改业务 api/。

---

## 验收标准

- [ ] `python tools/harness_change_status.py --task docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md --json` 输出合法 JSON。  
- [ ] Cursor 命令文件存在且指向本仓真值路径。  
- [ ] 全量 pytest 绿。

---

## 给 Cursor

Loop R3、O5、O6、R2 须 done
