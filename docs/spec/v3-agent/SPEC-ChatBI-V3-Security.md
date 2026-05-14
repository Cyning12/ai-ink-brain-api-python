# ChatBI V3 — 安全：SQL 与 Prompt

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2.1** P1-1 / P1-2  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §3.2、§4.2 P0

---

## 1. 目标

在 **不破坏** V2 Text2SQL 主路径的前提下，将安全能力从「关键字过滤」升级到 **可证明的约束**（SQL）与 **输入/输出侧防护**（Prompt）。

---

## 2. SQL 注入与越权读写

### 2.1 现状（V2 真值）

- **已合并 P1-1（本仓）**：`api/chatbi_sql_gate.py` 在 `normalize_single_sql` 之后以 **sqlparse 结构化路径** 判定 **多语句**、**顶语句禁止类 DDL/DML 形态**（与 `ast_forbidden_ddl` / `ast_multi_statement` 等 `rule` + 可选 `ast_rule_id` 对齐），再进入 **`chatbi_sql_table_policy`（min_*）** 与 **档位/L2 收窄**；详见 `docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` **§5** 与 pytest `tests/test_chatbi_sql_ast_gate_v1.py`。  
- 历史说明：早期简历若写「纯关键字过滤」须以本节 **现状** 为准更新。

### 2.2 V3 目标形态（初版 — 待实现 PR 选型）

| 层级 | 说明 |
|------|------|
| **解析** | 对 **最终执行前** 的 SQL 做 AST 或等价结构化解析（方言与 Supabase 对齐）。 |
| **策略** | **只读**：禁止多语句、禁止 DML/DDL（除非产品明确开放 — **默认禁止**）、参数化或白名单表/列。 |
| **失败** | HTTP 与响应 body 以 **`ChatBiSqlGateDenied`**、结构化 **`deny_code`**、用户可读短文案为准（与 `docs/tasks/done/task_chatbi_level_gate_v1.md` 及 **P1-1** `docs/tasks/active/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` 现网真值一致）；日志带 `request_id` / `run_id`（见 Logging 子规）。**本节不再使用 `error_code` 指代对外 JSON 字段**，避免与实现漂移。 |

### 2.3 非范围（初版）

- 替换数据库引擎；行级安全（RLS）全集 —— 与 **Identity** 子规协同时分层讨论。

---

## 3. Prompt 注入

> **首期 PoC 边界**：V3 首期 Prompt 防护的**可执行交付范围**以 `docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md` **§4 验收**为准；**§3.2 输出侧**未在该 task 验收勾选并合并代码前，**不得**在对外叙述或简历中将本子规「输出侧」标为已交付。

### 3.1 输入侧

- **首期 PoC（已合并代码）**：`api/chatbi_prompt_guard.py` + `CHATBI_PROMPT_GUARD_MODE`（`off`/`warn`/`block`），接入 **`api/unified_chat.py::handle_unified_chat`**（非流式 JSON）与 **`handle_unified_chat_stream`**（**SSE**；`meta` 之后、`decide_intent` / `ChatBIAgent.run` 之前短路）。规则与验收以 `docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md` 为准。  
- 用户消息、历史、**工具回灌** 中的异常模式（指令覆盖、数据渗出请求）—— **PoC 级**检测规则 + 可配置阈值；与 Intent / rewrite 链路交点须在 `_tech_graph` 或本子规修订中标注。

### 3.2 输出侧

- 对 **即将执行** 的 SQL 与 **即将展示** 的模型输出做长度与模式校验（与 SQL 子系统共享部分规则）。

---

## 4. 验收方向

- **可执行验收**：以关联 **implementation task** 正文 **「验收标准」** 小节（如 P1-1 / P1-2 task 的 §5 / §4）中的 **`- [ ]` 勾选** 与 pytest 门禁为准；本节不替代 task 的可观测断言。  
- **负例用例集**：至少覆盖「多语句」「禁止关键字」「越权表名」之一类，CI 或本地脚本可跑。  
- **简历对齐**：未合并代码前，对外表述仍为「V3 规划中」。

---

## 5. 关联

- `docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（**P1-1** implementation · 已归档）  
- `docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（**P1-2** implementation）  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Tool-Design.md`  
- [`SPEC-ChatBI-V3-Logging-Trace.md`](SPEC-ChatBI-V3-Logging-Trace.md)

---

## 6. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
| 2026-05-13 | **§2.2**：「失败」行用语与现网 **`deny_code` / `ChatBiSqlGateDenied`** 对齐；废止以 `error_code` 指代对外字段的叙述。**freeze_id**：`SPEC-SEC-2026-05-13-§2`（P1-1 task `freeze_id` 引用本行）。 |
| 2026-05-13 | **§3 / §4**：明确 PoC 与 §3.2 输出侧边界；可执行验收以关联 task 勾选为准。**freeze_id**：`SPEC-SEC-2026-05-13-§3`（P1-2 task `freeze_id` 引用本行）。 |
| 2026-05-14 | **§2.1**：登记 **P1-1 AST 硬化已合并**（`chatbi_sql_gate` + `tests/test_chatbi_sql_ast_gate_v1.py`）；`sql_gate_deny` 可带 **`ast_rule_id`**（与 `rule` 并存）。**freeze_id**：沿用 `SPEC-SEC-2026-05-13-§2`（对外 `deny_code` / `ChatBiSqlGateDenied` 未变）。 |
| 2026-05-14 | **§5**：登记 **P1-1 / P1-2** implementation 任务单路径（`task_chatbi_v3_sql_ast_text2sql_gate_v1` → **`docs/tasks/done/`** 已归档、`task_chatbi_v3_prompt_injection_guard_poc_v1`）。 |
| 2026-05-14 | **§3.1**：**P1-2 Prompt guard**：`chatbi_prompt_guard` + Unified **JSON**（`handle_unified_chat`）与 **SSE**（`handle_unified_chat_stream`，`meta` 后短路）；**历史块 / rewrite 出口** 仍按 task 非范围。 |
