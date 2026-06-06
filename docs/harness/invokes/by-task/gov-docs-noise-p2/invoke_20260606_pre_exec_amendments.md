# Invoke · pre-exec amendments · P2

> **Round**：T0 改稿（pre-T2c）
> **Hat**：Lead（按 Cursor R1 审核改稿 Prompt 执行 §1–§4）
> **Branch**：`task/gov-docs-noise-p2-v1`
> **Date**：2026-06-06

---

## 输入

- R1 审核真值：`docs/harness/reviews/by-task/gov-docs-noise-p2/task_gov_docs_noise_p2_readorder_v1_audit_R1_20260606.md`
- 改稿 Prompt：`docs/harness/prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md`
- task：`docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md`

## 执行内容

### §1 task 改稿
- B1：P2-2 从「完全一致」改为「canonical 子集对齐 + 双向互链 + 扩展导航保留」
- B2：C4/C5/C6 映射修正（C4→P2-1, C5→P2-3, C6 非范围）
- B3：task 内 Round 表链至 T0/T2c PROMPT

### §2 验证
- `python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md` → OK
- `python tools/harness_task_validate.py docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md` → OK

### §3 新建 PROMPT
- `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`
- `PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`

### §4 更新 MANIFEST / 导图 / prompts/README
- MANIFEST P2 行：task 路径 / draft 状态 / Round 表链
- docs-noise-inventory README §6：当前下一棒 P2 · T2c
- harness/prompts/README.md 增索引

## 交付 commit

1. `222d3be` docs(task): P2 R1 改稿
2. `a0dcc43` docs(harness): P2 T0/T2c PROMPT + MANIFEST 脚手架

## Gate 状态

| gate_id | status | blocks |
|---------|--------|--------|
| HG-TASK-DRAFT | **pending** | 22-R1, 30 |
| HG-GOV-P2-EXEC | **pending** | explore, 22, 30, 40, CLOSE |

## 下一棒

待人签 `HG-TASK-DRAFT` + `HG-GOV-P2-EXEC` 后，执行：
`docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`

---
*改稿完成 · 未执行 P2-1~P2-4 实现 · 未改 api/tests/workflows*
