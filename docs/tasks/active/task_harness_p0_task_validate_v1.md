# Task：Harness P0 R1 — task_validate（OpenSpec Delta + TDD test_strategy）

> **状态**：pending  
> **schedule_ref**：RECENT §0.6 · Loop R1  
> **母单**：[`task_harness_p0_openspec_tdd_loop_v1.md`](task_harness_p0_openspec_tdd_loop_v1.md)  
> **freeze_id**：`HARNESS-P0-TASK-VALIDATE@2026-05-30`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **task_slug** | `p0-task-validate` |

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | pending | 22-R1,30 | 继承母单 |

---

## 行为变更（Delta）

### ADDED

- **Requirement**：CLI 校验 task 文件 Harness 字段与 OpenSpec 写法节。  
  - **Scenario**：`validate-active` — GIVEN active task WHEN run validate THEN 报告 error/warn 清单。

### MODIFIED

- 无（Previously: 无机械 validate，仅 22 人工核对）

---

## 范围

- [ ] 新增 `tools/harness_task_validate.py`（规则见 execution-plan §4.1）。  
- [ ] 新增 `tests/test_harness_task_validate.py`。  
- [ ] 支持 `--json`、`--all-active`、单文件路径。  
- [ ] CI：经 pytest 覆盖（不新增 Required workflow 本 round）。

## 非范围

- `harness_change_status.py`（R3）。  
- 22/40 帽正文（R2）。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-validate-api-na` | 触达 api/ 且 test_strategy=not_applicable | validate **error** | 改 task | 规则 ID + 路径 |
| F2 | `fp-validate-missing-fp` | 无 failure_paths 表行 | validate **error** | 补 task | 同上 |

---

## 验收标准

- [ ] `pytest tests/test_harness_task_validate.py` 绿。  
- [ ] `python tools/harness_task_validate.py docs/tasks/active/task_harness_p0_task_validate_v1.md` exit 0。  
- [ ] 全量 `pytest -m "not intent_eval and not intent_benchmark"` 绿。  
- [ ] 50 复检落盘（本 task `required`）。

---

## 实现备忘

| 项 | 内容 |
|----|------|
| 涉及文件 | `tools/harness_task_validate.py`、`tests/test_harness_task_validate.py` |

---

## 给 Cursor

`test_strategy: required`、`harness_task_validate`、Loop R1、skip 10
