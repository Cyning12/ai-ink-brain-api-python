# Task：ChatBI V3 — **Prompt 注入** 防护 PoC（P1-2）

> **状态**：`todo`（**P1-2** implementation，**PoC 级**；可与 **P1-1**、**P1-4** 分 PR）  
> **与总规批次对应**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§2.1 P1-2**  
> **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§3**（输入侧 / 输出侧）  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` **§3.2.2**  
> **交叉（可选）**：`api/intent_agent.py`（用户消息进 LLM 前）、`api/tools.py` / `api/text2sql_core.py`（rewrite / 历史块拼接处）— 具体落点由实现 PR 在 **§实现备忘** 写死

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
- **非范围**：SQL AST（归 **`task_chatbi_v3_sql_ast_text2sql_gate_v1.md`**）。

---

## 3. 依赖与引用

| 项 | 路径 |
|----|------|
| 安全子规 | `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` §3 |
| 日志 | `api/chatbi_json_log.py` |
| 契约 | 若新增 SSE `chain.type`，须 **`_contract_manifest.json` + `tech_graph_contract_check` + Ink 消费** 同 PR；**PoC 默认**仅 HTTP/日志侧可不扩展 SSE |

---

## 4. 验收标准

- [ ] **规则**：至少 **5** 条可命名规则（中英文混合样例均可），覆盖：**忽略前文指令覆盖**、**假 system 标记**、**要求透出密钥/ env`**、**要求删除审计日志类话术**（实现 PR 列标题）。  
- [ ] **pytest**：`block` 模式下恶意样例 **被拦**；正常业务问句 **不误拦**（至少 **5** 条正例，含短中文问数 / 表名）。  
- [ ] **集成路径**：至少 **1** 条 e2e 风格测试（mock LLM 或仅测 guard 调用栈）证明 **拦在 LLM 调用之前**。  
- [ ] **日志**：`CHATBI_JSON_LOG=1` 下 **1** 次拒绝可 grep **`run_id`**（贴 PR 或路径）。  
- [ ] **配置文档**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 或子规 **§修订记录** 二选一更新，避免 env 漂移。  
- [ ] **子规**：`SPEC-ChatBI-V3-Security.md` §3 标注 **PoC 已合并** 与范围边界。

---

## 5. 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
|----|------|
| 接入函数 / 文件 | |
| 新 env 键名 | |
| 与 Intent / rewrite 的先后关系 | |

---

## 6. 给 Cursor 的稳定关键词

`P1-2`、`prompt injection`、`prompt_guard`、`CHATBI_PROMPT_GUARD`、`Enterprise Gap` §3.2.2、`task_chatbi_v3_prompt_injection_guard_poc_v1`
