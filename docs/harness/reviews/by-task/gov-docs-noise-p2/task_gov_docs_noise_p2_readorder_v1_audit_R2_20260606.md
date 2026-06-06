# R2 审核 · task_gov_docs_noise_p2_readorder_v1

> **日期**：2026-06-06
> **审核帽**：22（Harness Task Audit · R2 零阻塞签出）
> **task**：[docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md](../../../../tasks/active/task_gov_docs_noise_p2_readorder_v1.md)
> **前置**：R1 预审 + 改稿 Prompt 已执行 + T0/T2c PROMPT 与 MANIFEST 已就绪

---

## 1. task 范围审查（P2-1 ~ P2-4）

| ID | 清晰度 | 可验收性 | 说明 |
|----|--------|----------|------|
| P2-1 | 清晰 | 可验收 | PROJECT_CONFIG §A L17 + §B 表第 2 行须改为「已移除」；保留 `.cursor/rules/*.mdc` 摘要；可用 `rg` 验证 |
| P2-2 | 清晰 | 可验收 | 子集对齐（前 3–5 条 canonical）+ 双向互链；不要求全节逐步一致；扩展导航条保留 |
| P2-3 | 清晰 | 可验收 | 根 README Endpoints/env 补 Unified Chat 或 pointer；可用 `rg` 验证 |
| P2-4 | 清晰 | 可验收 | legacy 6 文件逐一判定；explore 已提供 `rag_fts_alias_text()` SQL 证据，建议全部 `done`；须更新 `_views/done.md` |

**结论**：四项交付目标、验收 checklist、失败路径 F1–F7 均完整；范围边界明确。

---

## 2. explore 差分确认

根据 [explore_P2_diff_20260606.md](../../../invokes/by-task/gov-docs-noise-p2/explore_P2_diff_20260606.md) 及 task 正文：

- **变更范围严格限于 docs 目录及相关根层文件**：
  - `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（P2-1）
  - `AGENTS.md`（P2-2）
  - `docs/README.md`（P2-2）
  - `README.md`（P2-3）
  - `docs/tasks/legacy/*`（6 文件 · P2-4 · `git mv` 或补状态）
  - `docs/tasks/_views/done.md`（P2-4 · 索引更新）
  - 可选：`docs/tasks/README.md`（legacy 清空标注）

- **未涉及**：`api/`、`tests/`、`.github/workflows/`，符合 `test_strategy: not_applicable` 与 P2 非范围。

---

## 3. R1 预审结论继承（B1–B3 改稿落实）

| R1 项 | 改稿状态 | 验证依据 |
|-------|----------|----------|
| **B1** P2-2「读序完全一致」过严 | 已落实 | task 正文 §P2-2 明确「角色区分」+「canonical 子集」+「扩展导航条保留」 |
| **B2** 冲突寄存器编号 C4/C5/C6 错误 | 已落实 | task 背景 bullets、非范围、验收标准均正确映射 C4→P2-1、C5→P2-3、C6→非本批范围；关账验收加「更新 C4、C5 为 done」 |
| **B3** 执行脚手架缺失 | 已落实 | `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md` 与 `PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md` 已存在；MANIFEST 已建；commit `a0dcc43` 确认 |

---

## 4. 阻塞项

**零阻塞，建议 30 开工。**

- `HG-TASK-DRAFT`：`approved`
- `HG-GOV-P2-EXEC`：`approved`
- T0/T2c PROMPT 与 MANIFEST 脚手架已就位
- `python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md` → **OK**

---

## 5. 可选 validate 结果

```text
$ python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md
=== docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md ===
OK
```

---

## 6. 总判

**条件通过 → 通过。**

- P2-1~P2-4 范围清晰、可验收；
- explore 差分确认变更仅 docs/ 目录及根 README；
- R1 B1–B3 改稿已全部落实；
- 人工闸与脚手架均就绪；
- **建议 30 帽按 T2c PROMPT 执行，40 自检后 CLOSE。**

---

## 7. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-06 | R1 预审 · 条件通过 · 列出 B1–B3 |
| 2026-06-06 | R2 审核 · 改稿与脚手架已落实 · 零阻塞签出 |
