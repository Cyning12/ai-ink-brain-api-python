# 任务审核：ChatBI V3 · SQL AST 后闸（P1-1）与 Prompt 注入 PoC（P1-2）

## 元信息

| 字段 | 值 |
|------|-----|
| 审查轮次 | **R2**（复审） |
| 关联上一轮 | 工作区指针：`Projects/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md` → 目标路径 **`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md`**（**当前仓库内该文件不存在**，见下文「非阻塞」） |
| 待审 task | `ai-ink-brain-api-python/docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（P1-1）<br>`ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（P1-2） |
| 关联 SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md`<br>`ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Logging-Trace.md`<br>`ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` |
| invoke_snapshot（建议） | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260515_0000_22_chatbi-v3-sql-ast-prompt-injection.md` |
| 规划对齐 | `docs/harness/HARNESS_V2_PLAN.md` **§5**（`test_strategy`、`failure_paths`、`gates_before_code`） |
| 落盘日期 | 2026-05-15 |

---

## 审查结论摘要

1. **P1-1（`task_chatbi_v3_sql_ast_text2sql_gate_v1.md`）**：头部 **`done`** 与 Harness 字段一致；`test_strategy: required` 与 **`### 自检结论（执行者）`** 中 pytest 命令、用例文件、退出码摘要 **可观测**；`failure_paths`（FP-A/B/C）与 `freeze_id`、`gates_before_code` 已落盘。**本轮仅作文档与任务单可执行性结论**，不质疑已实现关单。  
2. **P1-2（`task_chatbi_v3_prompt_injection_guard_poc_v1.md`）**：仍为 **`todo`**；`test_strategy: required` 及 `test_strategy_note` 与 §5 验收条目 **可失败自动化** 方向一致；`failure_paths`（FP-1～4）与 `freeze_id`、`gates_before_code` 齐备。**R1 要求在任务单内的回填**（OpenItems §1.6 脚注、`### 审查回填（任务审核 R1）`、FP-1 golden JSON 与 OpenItems 对齐说明）**已在正文可见**。**§5 实现备忘中 FP-1 golden JSON 仍为 `TBD` 属「待实现 PR 写死」的预期态，不得解读为 implementation 已终态。**  
3. **P1-1 必读第 3 条与 OpenItems**：`SPEC-ChatBI-V3-Identity-Access-OpenItems.md` 存在 **`### 1.6 结构化日志（写入）`**，与 task 引用一致；与 `failure_paths` 脚注中「`message` 承载语义标签、与 `sql_gate_*`/`auth_*` 草案并列」的表述 **无路径级矛盾**。

---

## 阻塞项

- **无**（就「任务帽是否可继续维护文档 / 执行帽是否在阅读 task 前提下进入编码准备」而言）：P1-2 的 `TBD` 与 task 自带 **拒开工条件** 已明确由 **实现 PR / 备忘写死** 承接，不构成本审查帽对「task 文档形态」的硬阻塞。

---

## 非阻塞项

| ID | 说明 |
|----|------|
| NB-1 | **R1 真值断链**：工作区 `docs/harness/reviews/...R1...md` 仅为指向子仓的指针，但 **`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md` 在子仓不存在**，与 `reviews/README.md`「子仓落盘为真值」约定不一致；**不影响**本轮从 **两 task 现行正文** 核对 R1 回填要点，但 **影响**「指令 → 结论」双锚可追溯。 |
| NB-2 | **P1-1 自检**：已诚实记录 **FP-C** 专测未纳入、`python -m pytest` 字面未单独跑；与 R1 非阻塞口径一致，**不**要求回溯改 done 状态（除非产品后续单开硬门禁）。 |
| NB-3 | **P1-2 Invoke 快照路径**：task 内写的是 `docs/harness/invokes/...`（相对工作区根），与子仓 invoke 实际落盘 **`ai-ink-brain-api-python/docs/harness/invokes/...`** 易混淆；建议任务帽 **一行澄清**（非功能）。 |

---

## 需任务帽回填清单（可选但建议）

- [ ] **（建议 · 可追溯）** 将 **R1 审查全文** 恢复为子仓真值文件 `ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md`，**或** 统一 task 内「按审查 R1 回填」链接为 **可打开的唯一 URL/相对工作区根路径**，并在指针 md 中说明「正文仅在工作区 / 仅在后端仓」避免双真值。  
- [ ] **（建议 · 歧义）** 在 P1-2 **`### Invoke 快照（可选）`** 中，将 invoke 路径写为 **相对工作区根** 的完整路径 `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260515_0000_22_chatbi-v3-sql-ast-prompt-injection.md`，与 `invoke_snapshot` 元信息一致。

---

## 是否建议执行帽开工

| 对象 | 建议 |
|------|------|
| **P1-1** | **否**（已 **done**；仅文档/运维复盘时只读）。 |
| **P1-2** | **有条件**：允许在 **遵守 task「拒开工条件」** 的前提下进入实现——即 **不得在 §实现备忘 仍缺 FP-1 的 HTTP 状态码与 body 字段名、且 golden JSON 路径仍为裸 `TBD` 时，直接改动 Unified/Agent 路由或外显契约**；应先在同一 PR 早期或开工首步 **写死 §实现备忘**（可与首条测试同提交，以满足 `test_strategy: required` 与 `HARNESS_V2_PLAN.md` §5.1 精神）。 |

---

## 签收 / 关闭

- **P1-1**：自本审查视角 **维持关单**；不要求因 R2 再改 task 正文（除非为修复 NB-1 链路的 **链接** 类编辑）。  
- **P1-2**：**不可开「任务终审」式关闭**——状态仍为 **`todo`**，`§5 实现备忘` 中 golden JSON 仍为 **`TBD`** 属 **未实现** 而非文档失误；须在 **实现 + 自检回填 + 后续任务审核 R3（若需要）** 后再行签收。  
- **本轮 R2 审查文档本身**：已落盘，可作为复审锚点。

---

## 给下一棒（交接一句）

下一棒请按对话中的 **可复制 Prompt** 选择角色：**任务帽**（修链/备忘歧义）、**执行帽**（P1-2 且先备忘/测试）、或 **任务审核帽 R3**（执行与回填完成后）；**勿**将 P1-2 的 `TBD` 当作已交付。
