# 审查归档：ChatBI V3 Security — P1-1 / P1-2 task + SPEC

> **审查帽**：工作区 `docs/harness/prompts/20-review-spec-task.md`  
> **字段约定**：`docs/harness/HARNESS_V2_PLAN.md` **§5**（`test_strategy` / `failure_paths` / `freeze_id`）  
> **归档日期**：2026-05-13  
> **落盘路径（本文件）**：`ai-ink-brain-api-python/docs/tasks/review_results/review_chatbi_v3_security_p1_p2_20260513_v1.md`  
> **回填状态**：第六节清单已落地；**二次审查（R2）** 见同目录 **`review_chatbi_v3_security_p1_p2_20260513_v2.md`**（本节一至五为 **R1 当时结论**，保留不作改写）。

---

## 被审对象（真值路径，相对工作区根 `Projects/`）

| 类型 | 路径 |
|------|------|
| Task P1-1 | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` |
| Task P1-2 | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md` |
| SPEC | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` |

---

## 一、阻塞项（审查当时结论）

以下条目为 **当次审查** 中认定的「缺了易导致拒开工或规格与实现真值冲突」项；**不代表**当前 HEAD 仍全部未闭合（见文末 **「与当前仓库对照」**）。

### 1. SPEC `SPEC-ChatBI-V3-Security.md`

| 位置 | 问题 | 建议补一句（审查建议） |
|------|------|------------------------|
| **§2.2** | 「失败」行曾使用 **`error_code`**，与 level_gate / 现网 **`deny_code`** 冲突 | 对外失败字段以 **`ChatBiSqlGateDenied` + `deny_code`** 为准；**不**用 `error_code` 指代对外 JSON。 |
| **文首状态 / §6** | SPEC 为 `draft` 且修订表未按章节粒度可指认时，`freeze_id` 难以审计 | 在 **§6** 为 §2 / §3 各增可引用 **freeze 行**（或 task `freeze_id` 改为提交哈希）；与 P1 task 互指。 |

### 2. Task P1-1 `task_chatbi_v3_sql_ast_text2sql_gate_v1.md`

| 位置 | 问题 | 建议补一句 |
|------|------|------------|
| **§5 顺序验收** | 曾写「单测 **或** 注释」，与 `test_strategy: required` 可失败自动化不一致 | **顺序必须以 pytest 固定**，不得仅以注释替代。 |

### 3. Task P1-2 `task_chatbi_v3_prompt_injection_guard_poc_v1.md`

| 位置 | 问题 | 建议补一句 |
|------|------|------------|
| **FP-1** | HTTP/body 仅写「与现网一致」时，执行前缺 golden | 在 **§实现备忘** 写死状态码 + 字段名，并在 **`tests/`** 提供 **golden JSON**。 |
| **FP-4** | fail-open / fail-closed 未事先拍板易静默默认 | 未在备忘写明前，**默认 fail-closed**；合入前备忘须显式记录最终选择。 |

---

## 二、非阻塞建议（审查当时）

### P1-1

- **FP-B**：若单独 `deny_code`，在 **`_contract_manifest.json`**（若适用）与 pytest 负例中同时登记。  
- **§5 日志**：优先在 `tests/` 中断言 JSON 结构；grep 仅作 PR 附录。  
- **`test_strategy_note`**：显式对齐 `HARNESS_V2_PLAN` **§5.1**（关键用例可被 pytest 失败复现）。

### P1-2

- **FP-2 `warn`**：固定结构化键名（审查建议示例：`prompt_guard_warn`），pytest 断言出现一次且不阻断下游。  
- **与 P1-1 先后**：同请求内 SQL gate 与 prompt guard 顺序在 **§实现备忘** 一句话钉死。

### SPEC

- **§3 / §3.2**：明确 PoC 首期与「输出侧」未交付边界，避免对外误标已交付。  
- **§4**：可执行验收以关联 task §5/§4 勾选为准。

---

## 三、`test_strategy: required` 对照（§5.1）

| Task | 结论（审查当时） |
|------|------------------|
| P1-1 | 负例/正例/日志 pytest 导向成立；**顺序**若允许纯注释则与 **required** 不完全对齐 → 须改为仅 pytest。 |
| P1-2 | 规则、block、正例、e2e 栈、FP-4 分支均有 pytest 要求；FP-1 依赖 golden 落地。 |

---

## 四、契约变更与 `freeze_id`

- **§2.2 字段命名** 与现网对齐 → 视为文档契约变更 → **SPEC §6 修订行 + task `freeze_id` 升级** 应同步。  
- **P1-2** 若引入新 HTTP 码或对外字段 → **`_contract_manifest.json`**（若适用）+ **freeze** 各记一行。

---

## 五、审查通过条件与执行门闸（审查当时）

- **P1-1**：SPEC §2.2 与 `deny_code` 矛盾消除 + §5 **顺序仅 pytest** 后，可按 task 执行；**先**红测负例/顺序，**再**改 `chatbi_sql_gate`；合并前 `pytest tests -m "not intent_eval and not intent_benchmark"`。  
- **P1-2**：FP-1 golden、FP-4 策略在备忘写死后可视为文档侧就绪；**先**备忘与 golden，**再**改路由；保证拦在 LLM 前的可测路径。

---

## 六、给需求帽的回填清单（可直接勾选驱动改文档）

1. **SPEC**：§2.2 与 **`deny_code` / `ChatBiSqlGateDenied`** 对齐；§6 增加可指认 **freeze 行**（§2 / §3）。  
2. **P1-1 task**：§5 **顺序断言** 改为 **仅 pytest**，删「或注释」。  
3. **P1-2 task**：FP-1 **golden JSON 路径**、FP-4 **默认 fail-closed**（或显式二选一）写入 failure_paths / 待确认 / 实现备忘指引。  
4. （可选）两份 task：增加 **`gates_before_code`** 列表，引用 `failure_paths`、`freeze_id`、必读列表 — 见 `HARNESS_V2_PLAN.md` **§5.4**。

**需求帽入口形状**：`docs/harness/prompts/10-requirements.md`

---

## 七、与当前仓库对照（落盘后核查摘要）

以下为本归档写入时，对 **同路径被审文件** 的简要核对：**若已一致，则第六节对应条可视作已回填，无需重复劳动**。

| 审查项 | 当前仓库观测（摘要） |
|--------|----------------------|
| SPEC §2.2 `deny_code` | **已**：失败行已与 `ChatBiSqlGateDenied` / `deny_code` 对齐，并废止 `error_code` 指代。 |
| SPEC §3 PoC 边界 / §4 可执行验收 | **已**：§3 引用块、§4 以 task 勾选为准。 |
| SPEC §6 freeze 行 | **已**：含 `SPEC-SEC-2026-05-13-§2`、`SPEC-SEC-2026-05-13-§3` 等。 |
| P1-1 §5 顺序 | **已**：要求 **必须 pytest**，不得仅以注释替代。 |
| P1-1 `test_strategy_note` / `freeze_id` / `gates_before_code` | **已**：对齐 HARNESS §5.1、§6 行引用、gates 列表。 |
| P1-2 FP-1 golden / FP-2 键名 / FP-4 默认 | **已**：failure_paths 与待确认/拒开工已加强。 |
| P1-2 `test_strategy_note` / `freeze_id` / `gates_before_code` | **已**。 |

若后续再次审查，请新开 `review_*_v2.md` 或更新日期版次，勿静默覆盖本文件语义。

---

## 八、回填执行记录（R1 → 文档真值）

| 项 | 说明 |
|----|------|
| **回填对象** | `SPEC-ChatBI-V3-Security.md`（§2.2 / §3 边界 / §4 / §6 `SPEC-SEC-*`）；`task_chatbi_v3_sql_ast_text2sql_gate_v1.md`；`task_chatbi_v3_prompt_injection_guard_poc_v1.md` |
| **对应清单** | 本文 **§六** 第 1–4 条（及可选第 4 条 `gates_before_code`，已见于两份 task 元信息） |
| **Git（供审计）** | 以 `ai-ink-brain-api-python` 仓库 `git log` 中 **`docs(spec+tasks): 审查帽回填 Security deny_code 冻结与 P1-1/P1-2 验收收紧`** 一类提交为准（哈希随分支变化） |
| **R2** | 审查帽对回填后 HEAD 的再审结论：**`review_chatbi_v3_security_p1_p2_20260513_v2.md`** |

---

## 给 Cursor 的稳定关键词

`Harness`、`审查帽`、`review_results`、`ChatBI`、`P1-1`、`P1-2`、`failure_paths`、`test_strategy`、`freeze_id`、`SPEC-ChatBI-V3-Security`
