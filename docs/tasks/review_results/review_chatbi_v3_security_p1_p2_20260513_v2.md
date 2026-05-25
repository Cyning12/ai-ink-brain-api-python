# 审查归档 R2：ChatBI V3 Security — P1-1 / P1-2（回填后再审）

> **审查帽**：工作区 `docs/harness/prompts/hats/20-review-spec-task.md`  
> **字段约定**：`docs/harness/HARNESS_V2_PLAN.md` **§5**  
> **R1 归档**：`review_chatbi_v3_security_p1_p2_20260513_v1.md`（**一至五为当时快照**；回填记录见该文件 **§八**）  
> **R2 落盘路径（本文件）**：`ai-ink-brain-api-python/docs/tasks/review_results/review_chatbi_v3_security_p1_p2_20260513_v2.md`  
> **审查日期**：2026-05-13（与 R1 同日二次扫描；以被审文件 HEAD 为准）

---

## 被审对象（相对工作区根 `Projects/`）

| 类型 | 路径 |
|------|------|
| Task P1-1 | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` |
| Task P1-2 | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md` |
| SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` |

---

## 一、阻塞项（R2）

**无。**  
对照 R1：§2.2 `error_code` / `deny_code` 冲突、§6 可指认 `freeze_id`、P1-1 顺序「仅 pytest」、P1-2 FP-1 golden / FP-2 键名 / FP-4 默认策略、`gates_before_code` 与 `test_strategy_note` 对齐 HARNESS §5.1 — 在被审 Markdown **当前正文**中均已闭合或可执行。

---

## 二、非阻塞建议（R2）

| 对象 | 位置 | 问题 | 建议补一句（可选） |
|------|------|------|-------------------|
| P1-1 | §6 实现备忘 | 未显式要求与 P1-2 **同请求**先后（若未来同一 PR 触 Unified） | 若改动入口链，在备忘增一行 **「与 prompt guard 先后只读交叉核对 P1-2 §5」**。 |
| SPEC | 文首 `draft` | 与已冻结 §6 行并存，新人可能误以为整本 SPEC 未冻结 | 文首可加一句 **「章节冻结以 §6 带 `SPEC-SEC-*` 行为准」** — 非关单硬门槛。 |
| P1-2 | §5 实现备忘 | `FP-1` golden 路径仍为待填占位 | 属执行前动作；**拒开工条件**已覆盖「未写死不改路由」。 |

---

## 三、`test_strategy: required` 对照（R2）

| Task | 结论 |
|------|------|
| **P1-1** | 负例 / 正例 / **顺序仅 pytest** / 日志 **tests 断言** / `test_strategy_note` 引 HARNESS §5.1 — **与 required 对齐**。 |
| **P1-2** | 规则、block、warn、`FP-4` 默认、e2e 拦在 LLM 前、日志 tests 断言、golden 与 HTTP 由拒开工 + 备忘约束 — **与 required 对齐**（golden 路径实现前由拒开工兜底）。 |

---

## 四、契约与 `freeze_id`（R2）

- **P1-1**：`freeze_id` 指向 **`SPEC-SEC-2026-05-13-§2`**，与 §2.2 `deny_code` 叙述一致；后续字段变更须 **§6 新行 + task 同步**。  
- **P1-2**：`freeze_id` 指向 **`SPEC-SEC-2026-05-13-§3`**；若 FP-1 引入新 HTTP/对外字段，task 元信息已要求 **manifest（若适用）+ §6** — **可审计**。

---

## 五、审查结论与执行门闸（R2）

**审查通过，可按 task 执行**（**仅文档 / 任务单真值**；不含尚未编写的实现代码）。

**门闸提醒（执行帽）**

- **P1-1**：先 **红测** 负例与 **顺序** 用例，再改 `api/chatbi_sql_gate.py`；合并前 `pytest tests -m "not intent_eval and not intent_benchmark"`。  
- **P1-2**：先在 **§实现备忘** 写死 **FP-1** HTTP/body 与 **golden JSON** 路径、**FP-4** 显式策略，再改路由；保证「拦在 LLM 前」路径有 **可失败** 测试。

---

## 六、给需求帽 / 复检

- **需求帽**：`docs/harness/prompts/hats/10-requirements.md`  
- **独立复检帽**：`docs/harness/prompts/hats/50-independent-reinspect.md`（若以 diff + 验收表为主）

---

## 七、R3 复核（2026-05-14 · 回填后再审 / 对话触发）

- **阻塞项**：仍为 **无**（对照当前 task / SPEC HEAD）。  
- **相对 R2 的增量观测**：P1-2 **§4** 已显式增加 **`warn` 路径** pytest 验收行，与 `failure_paths` **FP-2** 一致，**可测性**较 R2 撰稿时更完整。  
- **非阻塞（可选润色）**：`gates_before_code` 可追加 **`"test_strategy"`** 与 HARNESS **§5.4** 示例对齐；SPEC 文首 **`draft`** 可加一句「章节冻结以 §6 `SPEC-SEC-*` 行为准」；**FP-3 `off`** 可加 1 条轻量「不调 scan」测试；**SPEC §3.1** 与 `_tech_graph` 交点是否在 P1-2 关单强制，若否可在 SPEC §6 或 P1-2 验收补一句免责。

**结论（R3）**：维持 **§五** — **审查通过，可按 task 执行**；门闸同 **§五**。

---

## 给 Cursor 的稳定关键词

`Harness`、`审查帽`、`R2`、`review_results`、`ChatBI`、`P1-1`、`P1-2`、`审查通过`、`failure_paths`、`freeze_id`、`SPEC-SEC-2026-05-13`
