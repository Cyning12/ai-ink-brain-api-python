# Task：Harness P0 R1 — task_validate（OpenSpec Delta + TDD test_strategy）

> **状态**：done（2026-05-30 验收通过 · HARNESS-P0-TASK-VALIDATE@2026-05-30）  
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
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | approved | 22-R1,30 | 继承母单 |

---

## 行为变更（Delta）

### ADDED

- **Requirement**：CLI 校验 task 文件 Harness 字段与 OpenSpec 写法节。  
  - **Scenario**：`validate-active` — GIVEN active task WHEN run validate THEN 报告 error/warn 清单。

### MODIFIED

- 无（Previously: 无机械 validate，仅 22 人工核对）

---

## 范围

- [x] 新增 `tools/harness_task_validate.py`（规则见 [`SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md`](../../spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md) §4.1）。  
- [x] 新增 `tests/test_harness_task_validate.py`。  
- [x] 支持 `--json`、`--all-active`、单文件路径。  
- [x] CI：经 pytest 覆盖（不新增 Required workflow 本 round）。

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

- [x] `pytest tests/test_harness_task_validate.py` 绿。  
- [x] `python tools/harness_task_validate.py docs/tasks/active/task_harness_p0_task_validate_v1.md` exit 0。  
- [x] 全量 `pytest -m "not intent_eval and not intent_benchmark"` 绿。  
- [x] 50 复检落盘（本 task `required`）。

---

### 自检结论（执行者）

| # | 验收项 | 结果 | 证据 |
| --- | --- | --- | --- |
| V1 | `pytest tests/test_harness_task_validate.py` | **pass** | 6 passed |
| V2 | validate CLI 本 task exit 0 | **pass** | 输出 `OK` |
| V3 | 全量 Required pytest | **pass** | 267 passed, 1 skipped |
| V4 | invoke C2（22/30/40/50） | **pass** | `p0-openspec-tdd/invoke_20260530_*` 已落盘 |

**命令记录**（cwd=仓根）：

```bash
pytest tests/test_harness_task_validate.py -v          # exit 0
python tools/harness_task_validate.py docs/tasks/active/task_harness_p0_task_validate_v1.md  # exit 0
pytest tests -m "not intent_eval and not intent_benchmark" -q  # exit 0
```

---

## 实现备忘

| 项 | 内容 |
|----|------|
| 涉及文件 | `tools/harness_task_validate.py`、`tests/test_harness_task_validate.py` |
| 规则 | SPEC §4.1 十条（error/warn）· CLI `--json` / `--all-active` / 单路径 |

---

## 给 Cursor

`test_strategy: required`、`harness_task_validate`、Loop R1、skip 10
