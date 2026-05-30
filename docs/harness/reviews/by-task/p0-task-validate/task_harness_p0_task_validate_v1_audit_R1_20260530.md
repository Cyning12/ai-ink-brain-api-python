# 任务审核 · R1 · p0-task-validate

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | task | `docs/tasks/active/task_harness_p0_task_validate_v1.md` |
> | task_slug | `p0-task-validate` |
> | freeze_id | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
> | round | R1 |
> | invoke_snapshot | `docs/harness/invokes/by-task/p0-openspec-tdd/invoke_20260530_22_p0-task-validate-v1.md` |
> | 母 task | `docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md` |

---

## 审查结论摘要

**零阻塞。建议 30 执行编码。**

---

## 已核对项

| # | 项 | 结论 |
| --- | --- | --- |
| 1 | 母单 `HG-LOOP-BATCH` | **approved**（真值见母 task 表） |
| 2 | Harness 元信息 | `test_strategy: required` · `semi_auto: true` · `git_branch: task/harness-p0-openspec-tdd` |
| 3 | §行为变更 Delta | ADDED `validate-active` Scenario 与 SPEC O1 对齐 |
| 4 | failure_paths | F1/F2 含 Scenario ID · 覆盖 api/na 与缺 fp |
| 5 | 范围 / 非范围 | 仅 `tools/`+`tests/` · 不含 R2/R3 职责 |
| 6 | 验收标准 | 含 pytest 单测 + 全量 pytest + validate CLI exit 0 |
| 7 | 理论对齐 P0 §3.1–3.3 | test_strategy 与 tools 交付匹配 · **50 required** |
| 8 | SPEC §4.1 规则 | 10 条 error/warn 可在 30 实现 |

---

## 阻塞 / 非阻塞

**无阻塞项。**

---

## 是否建议执行帽开工

**是。** 30 帽交付：`tools/harness_task_validate.py` · `tests/test_harness_task_validate.py` · CLI `--json` / `--all-active` / 单文件路径。

---

## 签收 / 关闭

本 round **22 审查通过**；task 正式结束点以 **50 + git mv done/** 为准。

---

## 下一棒可复制 Prompt

见 `invoke_20260530_22_p0-task-validate-v1.md` §3 步骤 2（30 执行帽 invoke）。
