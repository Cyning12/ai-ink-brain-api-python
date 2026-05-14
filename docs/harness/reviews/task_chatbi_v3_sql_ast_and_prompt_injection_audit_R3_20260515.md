# 任务审核：ChatBI V3 · SQL AST 后闸（P1-1）与 Prompt 注入 PoC（P1-2）

## 元信息

| 字段 | 值 |
|------|-----|
| 审查轮次 | **R3**（任务帽 + 执行帽契约回填后复审） |
| 关联上一轮 | **R2**：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R2_20260515.md` |
| 更早轮次 | **R1**：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md`（子仓真值；R2 元信息中「子仓不存在」已过时，见下文 **NB-1 解除**） |
| 待审 task | `ai-ink-brain-api-python/docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（P1-1）<br>`ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（P1-2） |
| 关联 SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md`<br>`ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Logging-Trace.md`<br>`ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` |
| invoke_snapshot（建议） | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260515_0000_22_chatbi-v3-sql-ast-prompt-injection.md` |
| 规划对齐 | `docs/harness/HARNESS_V2_PLAN.md` **§5**（`test_strategy`、`failure_paths`、`gates_before_code`） |
| 落盘日期 | 2026-05-15 |

---

## 审查结论摘要

1. **P1-1**：仍为 **`done`**；本轮仅 **链接类** 编辑（R1 审查路径改为相对工作区根的子仓路径），不改变关单结论。  
2. **P1-2**：仍为 **`todo`**；**R2「需任务帽回填清单」** 已落实：**Invoke 快照** 路径与 **failure_paths / 审查回填** 中的 **R1** 链接已统一为 **`Projects/` 根下** 的 `ai-ink-brain-api-python/docs/harness/reviews/...` 与 `ai-ink-brain-api-python/docs/harness/invokes/...`，消除与 `docs/harness/invokes/...`（工作区 invokes）混用歧义。  
3. **§5 实现备忘 · FP-1（执行帽契约回填）**：已 **写死** 现网锚定的 **HTTP 200**、`POST /api/py/unified/chat`、body 顶层键与 `events` 内 **`type: "error"`** 帧形态；**golden** 路径为 `tests/fixtures/chatbi/prompt_guard_fp1_unified_chat_error_envelope.json`，配套契约单测 `tests/test_chatbi_prompt_guard_fp1_envelope_contract.py`。**这不等于** Prompt guard **业务实现已交付**；备忘与单测明确为 **envelope 契约占位**，guard 行为与集成断言仍待实现 PR。  
4. **拒开工条件**：P1-2 正文已更新为「§5 已钉契约真值」后始得改路由；**FP-1 与 golden 路径** 对「盲写路由」的硬缺口已闭合到 **可执行** 程度；**与 P1-1 SQL gate 先后顺序** 等条仍须在改动 `text2sql_core` 主链前于 §5 写死。

---

## 阻塞项

- **无**（就「任务帽文档链」「执行帽在已读 task 前提下进入路由级编码」而言）：P1-2 **仍为 todo**，但不构成本轮 **task 文档层** 硬阻塞。

---

## 非阻塞项

| ID | 说明 |
|----|------|
| NB-1（解除） | **R1 子仓真值**：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md` **已存在**；R2 元信息中「子仓不存在」**不再成立**，追溯请以 **R3 本表** 为准。 |
| NB-2 | **P1-2 实现备忘** 其余行（接入点、env、与 Intent/rewrite 先后等）仍为空白，由 **实现 PR** 回填；**非**本轮契约回填范围。 |
| NB-3 | **Agent/SSE** 路径若与 `handle_unified_chat` 非流式 body 不完全同形，实现 PR 须在 §5 **增补** 分支 envelope 或显式声明「仅 Unified JSON」为 PoC 范围。 |

---

## 需任务帽回填清单（对照 R2）

- [x] **R1 链路与双真值**：子仓 R1 全文已存在；task 内 R1 引用已改为 **相对工作区根** 的单一可打开路径。  
- [x] **P1-2 Invoke 歧义**：`### Invoke 快照（可选）` 已写为 **`ai-ink-brain-api-python/docs/harness/invokes/invoke_20260515_0000_22_chatbi-v3-sql-ast-prompt-injection.md`**。  
- [x] **（由执行帽配合）FP-1 契约**：§5 写死 HTTP/body + golden + pytest（占位契约，**非** guard 终态）。

---

## 是否建议执行帽开工

| 对象 | 建议 |
|------|------|
| **P1-1** | **否**（已 **done**）。 |
| **P1-2** | **是（有条件）**：**允许**在遵守 **其余拒开工条件**（尤其 **SQL gate 与 guard 先后**、§5 其余备忘）前提下，进入 **Unified/Agent 路由与 guard 实现**；**不得**将当前 **契约单测 + golden 样例** 误读为 **PoC 功能已合并完成**。 |

---

## 签收 / 关闭

- **P1-1**：**维持关单**。  
- **P1-2**：**不可开「任务终审」式关闭**——状态仍为 **`todo`**；须在 **guard 实现 + 验收勾选 + 自检回填 + 如需 R4 审查** 后再签收。  
- **本轮 R3 审查文档**：已落盘，可作为复审锚点。

---

## 给下一棒（交接一句）

下一棒：**执行帽** 可开工 P1-2 实现，但须持续区分 **契约占位（本轮已钉）** 与 **功能交付**；完成后触发 **自检帽** 与 **任务审核 R4**（若需要）。
