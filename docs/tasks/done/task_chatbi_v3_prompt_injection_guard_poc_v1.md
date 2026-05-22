# Task：ChatBI V3 — **Prompt 注入** 防护 PoC（P1-2）

> **状态**：`done（2026-05-20 · 22 帽 CLOSE 签收）`  
> **关闭回溯**：`docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_CLOSE_20260520.md`  
> **与总规批次对应**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§2.1 P1-2**  
> **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§3**（输入侧 / 输出侧）  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` **§3.2.2**  
> **交叉（可选）**：`api/intent_agent.py`（用户消息进 LLM 前）、`api/tools.py` / `api/text2sql_core.py`（rewrite / 历史块拼接处）— 具体落点由实现 PR 在 **§实现备忘** 写死  
> **test_strategy**：`required`  
> **test_strategy_note**：PoC 须 pytest 钉住 **规则命中 / 正例不误拦 / warn|block|off**；合并前须满足本仓 CI 默认 pytest 门禁。合并 PR 须符合 `docs/harness/HARNESS_V2_PLAN.md` **§5.1** `required`：关键用例可被 **`pytest` 失败复现**（或与 CI 等价本地命令）。  
> **freeze_id**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§6** 行 **`SPEC-SEC-2026-05-13-§3`** + 本单 **§4～§5**。若 FP-1 引入新 HTTP 码或对外字段名，须同步 **`_contract_manifest.json`**（若适用）与本字段及 SPEC §6。  
> **gates_before_code**：`["failure_paths", "freeze_id", "§给执行帽的必读列表"]`

---

## Harness（需求帽落盘）

### failure_paths

| ID | 触发条件 | 系统行为（须可测） | 可重试 | 用户可见类型 |
|----|-----------|-------------------|--------|----------------|
| FP-1 | **`CHATBI_PROMPT_GUARD_MODE=block`** 且 `scan()` 命中规则 | **不调用**下游 LLM（或短路统一错误路径）；HTTP 状态码与 body **须与现网 Unified/Agent 错误 envelope 一致**；实现 PR 在 **§实现备忘** 写死 **状态码 + 字段名**，并在 **`tests/`** 内提供 **golden JSON**（fixture 或快照路径写死在备忘）。`CHATBI_JSON_LOG=1` 打 **`prompt_guard_deny`**，含 **`request_id`/`run_id`**、`matched_rule_id` | 否（同文本策略不变则仍拦） | 短拒绝文案（**不**暴露规则细节与内部路径） |
| FP-2 | **`mode=warn`** 且命中 | **仅日志**：使用固定日志/结构化键名 **`prompt_guard_warn`**（与 `prompt_guard_deny` 并列），请求 **继续** 下游；pytest 断言该键在命中时出现 **一次** 且不阻断下游 | 适用下游可重试语义 | 用户 **无额外**阻断提示（PoC 默认） |
| FP-3 | **`mode=off`** | 跳过扫描 | 适用下游 | 无 |
| FP-4 | Guard 模块自身异常（导入失败、规则表损坏等） | **fail-open 或 fail-closed 须在 §实现备忘二选一并文档化**；推荐 **fail-closed**；须 pytest 覆盖该分支。**若备忘未落笔，实现阶段默认 fail-closed**（合入前须回填备忘为显式选择） | 视 HTTP 而定 | 通用错误或拒绝类（与所选策略一致） |

> **FP-1 日志字段与 OpenItems §1.6**：`prompt_guard_deny` / `prompt_guard_warn` 为 JSON 行根级 **`message`** 承载的语义标签（见 `api/chatbi_json_log.py` 的 `log_chatbi_record`），与 `docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` **§1.6** 中 `sql_gate_*`、`auth_*` 草案**并列、不复用同名**；OpenItems 表内「`event=`」为草案表述，实现以代码为准。**按审查 R1 回填**（相对工作区根 `Projects/`）：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md`。

### 给执行帽的必读列表（开工前）

1. `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§3**（输入侧范围与 PoC 边界）。  
2. `api/chatbi_json_log.py` 与 `docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access-OpenItems.md` **`### 1.6 结构化日志（写入）`**（与 `sql_gate_*` / `auth_*` 键域分离）。  
3. 选定接入点上下游：`api/intent_agent.py`、`api/unified_chat.py` 或 rewrite 出口 — **在 §实现备忘画「先后」** 避免双扫或漏扫。  
4. 合并前：`pytest tests -m "not intent_eval and not intent_benchmark"`（与 `ai-ink-brain-api-python/.github/workflows/pytest.yml` 一致）。

### 文档对齐（子规 vs 本单）

| 观察 | 处理 |
|------|------|
| 子规 **§3.2 输出侧** 与 PoC 范围 | **以 SPEC §3 引用块 + 本子规 §4 勾选** 为准；SPEC §6 行 **`SPEC-SEC-2026-05-13-§3`** 已钉边界。 |

### 待确认问题（缺答则执行帽输出阻塞清单）

- **FP-1**：golden JSON 的 **`tests/`** 路径须在 §实现备忘写死；与现网 body 字段命名是否独立于 `deny_code` 须在 PR 描述附 **一例 JSON**。

### 拒开工条件（执行帽）

- `failure_paths` 与 **§5 实现备忘** 中 **FP-1** 的 HTTP/body 与 golden 路径未写死即开始改路由（本单 §5 已钉 **契约真值**；若实现选用不同 HTTP 语义，须先更新 §5 与相关 manifest 再改代码）。  
- 未说明与 **P1-1 SQL gate** 的先后顺序（同请求内谁先谁后）即改动 `text2sql_core` 主链（须在 **§实现备忘** 用一句话钉死，避免重复拦截或绕过）。

### 审查回填（任务审核 R1）

- **§5 · FP-1**：golden 路径与 HTTP/body 已在 **§5 实现备忘** 写死（任务帽 + 执行帽契约回填，**非** guard 实现终态）；**failure_paths** 上栏已含 `message` 与 OpenItems §1.6 对齐说明。来源（相对工作区根）：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md`。

### Invoke 快照（可选）

- **相对工作区根 `Projects/`**：`ai-ink-brain-api-python/docs/harness/invokes/invoke_20260515_0000_22_chatbi-v3-sql-ast-prompt-injection.md`（任务审核帽 `22`、R2 复审启动体；总规见工作区 `docs/harness/invokes/README.md`）

---

## 1. 背景与目标

总规要求：在 V3 首阶段交付 **Prompt 注入检测的 PoC** —— 覆盖「用户消息 / 多轮历史 / 工具回灌」中的 **指令覆盖、系统角色劫持、数据渗出话术** 等模式的 **可配置规则 + 阈值**，默认 **偏保守**（误杀可配置降级），并与现有 **Intent / Text2SQL** 路径兼容。

**完成态（PoC）**：

1. **检测模块**：独立模块或 `api/` 下清晰命名包（例：`api/chatbi_prompt_guard.py`），提供 **`scan(text: str) -> GuardResult`**（或等价），含 **`blocked: bool`、`reason_code`、`matched_rule_id`**。  
2. **接入点（至少 1 个）**：在 **进入 SiliconFlow / OpenAI 补全之前** 对用户侧拼接文本做一次扫描；**或** 在 **rewrite 输出** 进入下一跳前扫描 —— 实现 PR **二选一或组合**，须在 **§实现备忘** 说明并配 pytest。  
3. **可观测**：`CHATBI_JSON_LOG=1` 时打 **`prompt_guard_deny`**（或沿用现有 `sql_gate_*` 之外的新 `message`，与 OpenItems **§1.6** 不冲突即可），含 **`request_id` / `run_id`**。  
4. **配置**：`PROJECT_CONFIG` 或 env（例：`CHATBI_PROMPT_GUARD_MODE=off|warn|block`）文档化默认值。

---

## 2. 范围 / 非范围

- **范围**：规则表初版（可 YAML 或 Python 常量）、单元测、日志打点、与 **一条** Unified 或 Agent 路径集成。  
- **非范围**：完整 **对抗样本** 平台、在线学习、多语言 NLP 模型；**前端**展示（可归 Ink 另任务，本单 pytest + 日志即可）。  
- **非范围**：SQL AST（归 **`docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`**（P1-1））。

---

## 3. 依赖与引用

| 项 | 路径 |
|----|------|
| 安全子规 | `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` §3 |
| 日志 | `api/chatbi_json_log.py` |
| 契约 | 若新增 SSE `chain.type`，须 **`_contract_manifest.json` + `tech_graph_contract_check` + Ink 消费** 同 PR；本 PoC 复用既有 **`error`/`latency`/`done`**，**不**新增 `chain.type`。 |

---

## 4. 验收标准

- [x] **规则**：至少 **5** 条可命名规则（中英文混合样例均可），覆盖：**忽略前文指令覆盖**、**假 system 标记**、**要求透出密钥/ env`**、**要求删除审计日志类话术**（实现 PR 列标题）。  
- [x] **pytest**：`block` 模式下恶意样例 **被拦**；正常业务问句 **不误拦**（至少 **5** 条正例，含短中文问数 / 表名）。  
- [x] **warn 路径**：`CHATBI_PROMPT_GUARD_MODE=warn` 且命中规则时，pytest 断言 **`prompt_guard_warn`** 出现 **一次** 且不阻断下游（mock / spy 可证）。  
- [x] **集成路径**：至少 **1** 条 e2e 风格测试（mock LLM 或仅测 guard 调用栈）证明 **拦在 LLM 调用之前**。  
- [x] **SSE**：`CHATBI_USE_AGENT=false` 时 **`POST /api/py/unified/chat/stream`** 在 `block` 下 **不调用** `decide_intent`，响应流含 **`stage=prompt_guard`**（`tests/test_chatbi_prompt_guard_poc.py::test_sse_v1_prompt_guard_short_circuits_before_decide_intent`）。  
- [x] **日志**：`CHATBI_JSON_LOG=1` 下 **1** 次拒绝：在 **`tests/`** 中断言 JSON 日志结构（含 **`run_id`**）；grep 仅作 PR 附录。  
- [x] **配置文档**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 或子规 **§修订记录** 二选一更新，避免 env 漂移。  
- [x] **子规**：`SPEC-ChatBI-V3-Security.md` §3 标注 **PoC 已合并** 与范围边界。

---

### 自检结论（执行者）

| 项目 | 结果 |
|------|------|
| VERIFY 命令（task「给执行帽的必读列表」§4 与 CI `pytest.yml` 对齐） | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| cwd（相对 `Projects/`） | `ai-ink-brain-api-python` |
| 退出码 | **0** |
| 摘要（本轮本地） | **139 passed**, 2 deselected；约 24s；存在第三方 DeprecationWarning（Supabase / SWIG），**非失败** |

**task 列出的其他验证命令**：无（本单合并前仅显式列出上述 pytest）。

**§4 验收对照摘要**（与 `test_strategy: required` 一致：以 pytest 证据为主）：

| §4 项 | 结果 | 证据 |
|-------|------|------|
| 规则 ≥5 条等 | pass | 同上 pytest 绿；实现侧见 `tests/test_chatbi_prompt_guard_poc.py` |
| block / 正例 pytest | pass | 同上 |
| warn 路径 `prompt_guard_warn` 一次且不阻断 | pass | 同上 |
| 集成：拦在 LLM 之前 | pass | 同上（JSON + **SSE v1** `test_sse_v1_prompt_guard_short_circuits_before_decide_intent`） |
| `CHATBI_JSON_LOG=1` JSON 日志结构含 `run_id` | pass | 同上 |
| 配置文档或子规修订记录更新 | **本帽未单独跑文档命令** | 须复检对照 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` / `SPEC-ChatBI-V3-Security.md` §3 落笔 |
| 子规 §3 PoC 已合并标注 | **本帽未单独跑文档命令** | 同上 |

**已知未测 / 非范围**：**历史块 / rewrite 出口** 仍仅扫 **原始用户 `query`**（与 SPEC §3.1 非范围一致）。**SSE Agent** 路径已接入同一短路 helper，与 JSON 共用规则；若需单独 Agent 流式 pytest 可后续补。**文档项**未由本 run 的 shell 命令直接断言。

**Invoke 快照（本自检帽 `40`）**：相对工作区根 `Projects/` → `docs/harness/invokes/invoke_20260514_0000_40_chatbi-v3-prompt-injection-guard-poc-v1.md`

---

## 5. 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
|----|------|
| 接入函数 / 文件 | `api/chatbi_prompt_guard.py`（`scan`、`chatbi_prompt_guard_mode`）；`api/unified_chat.py`：**`handle_unified_chat`**（`finish` 之后、**`CHATBI_USE_AGENT` 分支之前**）；**`handle_unified_chat_stream`**（`meta` 之后：`CHATBI_USE_AGENT` 的 Agent 主路径用 `if not _pg_ab` 包裹 **incremental / batch**；**v1 非 Agent** 在 **`decide_intent` 之前** 整段短路；**`prefer=tool:*`** 在 meta 后短路）。共用 **`_unified_prompt_guard_short_circuit_events`**；SSE 日志 `route` 字段为 **`unified_chat_sse`**（JSON 为 **`unified_chat`**）。 |
| **SSE · FP-1** | **HTTP 200** + `text/event-stream`；**`chain`**：`error`（`payload.stage=prompt_guard`）+ **`latency`**；**`done`**：`ok: false`。不新增 `chain.type`。 |
| 新 env 键名 | `CHATBI_PROMPT_GUARD_MODE`：`off`（默认）\| `warn` \| `block` |
| 与 Intent / rewrite 的先后关系 | **同请求**：对原始用户 `query` 扫描 **早于** `decide_intent` / `ChatBIAgent.run` / `no_data.generate` LLM / `text2sql` 路径上的 `llm_generate_sql`。**P1-1 SQL AST gate** 仍在 `apply_chatbi_sql_gate`（SQL 文本生成之后），故顺序为 **Prompt guard（用户 query）→ … → SQL gate**；**未**修改 `api/text2sql_core.py` 主链。 |
| **FP-4**（fail-open / fail-closed） | **fail-closed**：`scan()` 捕获全部异常 → `blocked=True` + `internal_error=True`；Unified 路径下 **`warn` 模式若 `internal_error`** 与 **`block`** 同等短路并写 **`prompt_guard_deny`**（不继续下游）。pytest：`test_scan_fail_closed_internal`。 |
| **FP-1**（HTTP + body + golden） | **路由**：`POST /api/py/unified/chat`（`api/unified_chat.py` → `handle_unified_chat`）。**HTTP**：**200**（`JSONResponse` 未传 `status_code`，与现网非流式 Unified 一致）。**Body 顶层键**：`ok`（bool）、`run_id`（str）、`session_id`（str 或 null）、`mode`（str）、`events`（list）。**拒绝语义载体**（与现行 text2sql 生成阶段失败短路同形）：`ok: false` 且 `events` 中含 **`type`: `"error"`** 的项，`payload` 含 **`stage`**（str）、**`message`**（str，短拒绝文案，**不**暴露规则细节）。若后续产品改为 **403** 或引入 **`deny_code`** 顶层字段，须与本行、`_contract_manifest.json`（若适用）同 PR 更新后再动路由。<br>**golden JSON（相对本仓根）**：`tests/fixtures/chatbi/prompt_guard_fp1_unified_chat_error_envelope.json`；契约单测：`tests/test_chatbi_prompt_guard_fp1_envelope_contract.py`（仅锁 envelope 形态；**guard 行为**仍以 PoC 实现 PR 为准）。 |

---

## 6. 给 Cursor 的稳定关键词

`P1-2`、`prompt injection`、`prompt_guard`、`CHATBI_PROMPT_GUARD`、`Enterprise Gap` §3.2.2、`task_chatbi_v3_prompt_injection_guard_poc_v1`、`test_strategy`、`failure_paths`、`freeze_id`、`拒开工`、`gates_before_code`、`prompt_guard_warn`
