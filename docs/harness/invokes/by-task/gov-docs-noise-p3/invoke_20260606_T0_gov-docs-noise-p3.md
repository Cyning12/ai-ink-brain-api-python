# Invoke · T0 · gov-docs-noise-p3

> **Round**：T0
> **Hat**：Lead / harness-10
> **Branch**：`task/gov-docs-noise-p3-v1`
> **Date**：2026-06-06

---

## 输入

- MANIFEST：`docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`
- SPEC §8.4：P3 SPEC 收敛索引 + showcase 入口
- P2 precedent：`docs/tasks/done/task_gov_docs_noise_p2_readorder_v1.md`

## 交付

- `docs/tasks/active/task_gov_docs_noise_p3_index_v1.md`（新建）
- `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p3_zh.md`（新建）
- `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2d_gov-docs-noise-p3_zh.md`（新建）
- MANIFEST P3 行更新：`draft` + T0/T2d PROMPT 链入
- SPEC 导图 §6 更新：当前下一棒 → P3 · T0 · 待人签

## 验证

- `python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p3_index_v1.md` → OK
- `python tools/harness_task_validate.py docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md` → OK

## 回填

- task `HG-TASK-DRAFT`：`pending` → 待人签
- task `HG-GOV-P3-EXEC`：`pending`

## 下一棒

人签 `HG-TASK-DRAFT` + `HG-GOV-P3-EXEC` → T2d 执行
