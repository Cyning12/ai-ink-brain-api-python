# 任务审核：ChatBI V3 · Prompt 注入防护 PoC（P1-2）

## 元信息

| 字段 | 值 |
|------|-----|
| 审查轮次 | **R4**（自检帽 `40` 回填后 · 关单前终审） |
| 关联上一轮（P1-2 语境） | **R3**（与 P1-1 合审）：`ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R3_20260515.md` |
| 待审 task | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md` |
| 关联 SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` |
| **invoke_snapshot**（本轮自检锚点） | `docs/harness/invokes/invoke_20260514_0000_40_chatbi-v3-prompt-injection-guard-poc-v1.md`（相对工作区根 `Projects/`） |
| 规划对齐 | `docs/harness/HARNESS_V2_PLAN.md` **§5**（`test_strategy: required`、`failure_paths`、`freeze_id`） |
| 落盘日期 | 2026-05-14 |

---

## 审查结论摘要

1. **自检结论**：task 内「### 自检结论（执行者）」记载 `pytest tests -m "not intent_eval and not intent_benchmark"` 于子仓根 **退出码 0**、**138 passed**；本帽 **不重写** 该通过事实，仅做文档层与 task 字段对照。  
2. **§4 验收**：task 正文 `- [x]` 已全勾选；与 `test_strategy: required` 及 CI 对齐命令一致。  
3. **failure_paths / §5**：FP-1（HTTP 200、envelope、golden 路径、契约单测）、FP-2/3、FP-4（fail-closed + `internal_error` 与 warn 短路语义）均在 **§5 实现备忘** 有落笔，且与 R3 所述「契约占位 vs 功能交付」区分一致；本轮对照未发现与 **failure_paths** 表冲突的空白。  
4. **freeze_id**：task 引用 `SPEC-SEC-2026-05-13-§3`；SPEC `SPEC-ChatBI-V3-Security.md` **§6** 修订记录仍含该行，无漂移需阻塞。

---

## 独立复检帽（文档项）· 文件级证据

对照自检表中「本帽未单独跑文档命令」两项，由本 R4 轮次 **只读核对**（非 shell 断言）：

| §4 / 自检项 | 结论 | 证据（相对 `Projects/`） |
|---------------|------|---------------------------|
| 配置文档更新 | **pass** | `ai-ink-brain-api-python/docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 头部「最后校准」含 **P1-2**；**§C** 表含 `CHATBI_PROMPT_GUARD_MODE` 行（用途：`api/chatbi_prompt_guard.py`、`handle_unified_chat`；默认 `off`；与 task 链一致）。 |
| 子规 §3 PoC 已合并标注 | **pass** | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§3.1** 明确「首期 PoC（已合并代码）」、接入点与非流式边界；**§6** 修订 **2026-05-14** 行登记 P1-2 已合并及 SSE/扩展范围说明。 |

---

## 阻塞项

- **无**。

---

## 非阻塞项 / 与 R3 对齐

| ID | 说明 |
|----|------|
| NB-3（仍成立） | R3 **NB-3**：若 Agent/SSE 与 `handle_unified_chat` 非流式 body 不同形须在 §5 增补；**当前 PoC** 仍以 SPEC **§3.1** 与 task **非范围** 为真值——**仅 Unified 非流式 JSON**，**不含** SSE 同形短路；与 task「已知未测」中 **Unified SSE** 未纳入 pytest 的声明 **一致**，**无需**在本轮阻塞关单。 |

---

## 需任务帽回填清单

- [ ] 将 task 头部 **状态** 由 `todo` 改为 **`done`**（与下节签收一致后执行）。  
- [ ] 将 `task_chatbi_v3_prompt_injection_guard_poc_v1.md` 从 `docs/tasks/active/` **归档**至 `docs/tasks/done/`（路径与团队习惯一致即可）。  
- [ ] 若工作区根 `docs/harness/reviews/` 需索引：保留或更新指向本子仓 R4 全文的 **指针 md**（可选，与 `reviews/README.md` 子仓落盘规则一致）。

---

## 是否建议执行帽开工

| 结论 |
|------|
| **否**（实现与 pytest 已按自检结论完成；无待修阻塞项）。 |

---

## 签收 / 关闭

- **P1-2（本 task）**：在 **任务帽** 完成上表勾选（状态 `done` + 归档）后，视为 **Harness 书面闭环**；本 R4 审查文档可作为关单锚点。  
- **与 R3 关系**：R3 对 P1-2 的「不可开任务终审式关闭」条件已由 **实现 + §4 全勾选 + 自检回填** 满足；R4 专审本 task slug，**签收** P1-2 文档与验证链。

---

## 给下一棒（交接一句）

下一棒：**需求帽（任务分析）** 按下方可复制 Prompt 更新 task 元信息与归档；无需再开 **执行帽** 除非后续 scope 变更。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
R4 审查已签收 P1-2 Prompt guard PoC（见 `ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_R4_20260514.md`「签收 / 关闭」）。请将 `task_chatbi_v3_prompt_injection_guard_poc_v1.md` 头部状态改为 `done`，并把该文件从 `ai-ink-brain-api-python/docs/tasks/active/` 移至 `ai-ink-brain-api-python/docs/tasks/done/`；不删改「### 自检结论（执行者）」中的命令、退出码与通过事实；不扩大 scope。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md

【是否按任务审核文档回填】
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_R4_20260514.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 仅做 task 元信息、路径移动与必要交叉链接更新；不写业务实现代码。
2. 若工作区 `docs/harness/reviews/` 需指针：新增或更新链向上述 R4 全文的短指针 md（可选）。
3. 对话回复：给出变更文件相对路径列表与一句交接（下一棒可为人工 checklist 或无需再开帽）。

对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
```
