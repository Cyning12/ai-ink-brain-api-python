# Task：ChatBI Intent Hints — Step 1（C-lite · YAML + Prompt 注入）

> **状态**：`done（2026-06-04 · 50 复检 pass-with-notes · 待人 PR/合并签收）`  
> **Epic**：ChatBI Intent Hints · **U1 · Step 1**  
> **时间门槛**：[`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) §2 — **6/9 前须合 main**  
> **关联图谱**：`api/intent_agent.py` · `api/intent_router.py`（Step 1 **不改** router）· 无 `api/graph/*`  
> **母单回链**：[`task_chatbi_v3_intent_classification_debt_v1.md`](task_chatbi_v3_intent_classification_debt_v1.md)（Intent 技术债索引 · **不** 本 PR 实施 vNext）

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_intent_hints_step1_v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **test_strategy_note** | 涉 `api/intent_hints.py` · `api/intent_agent.py` · Portfolio Q4/人名路由；须 loader 单测 + stub Intent 增量用例；关账前须 50 落盘 |
| **audit_profile** | `post_close` |
| **freeze_id** | `CHATBI-INTENT-HINTS@2026-06-09`（见 **§ SPEC 决策** Q-3） |
| **gates_before_code** | `harness_task_validate.py` OK · `## SPEC 决策` Q-1～Q-4 已落盘 · `## 失败路径` + Scenario ID · `## 验收标准` 含 pytest · `## 行为变更（Delta）` 已填 · 必读列表已读 · `HG-TASK-DRAFT` = `approved` · `HG-AUDIT-R1` = `approved`（路径 A 后） |
| **git_branch** | `task/chatbi-intent-hints-step1-v1`（从 **最新 `origin/main`** 拉出；开干前 `git fetch && git rebase origin/main`） |
| **Open Folder** | `ai-ink-brain-api-python` |
| **blocked_by** | （无 — 假定 main 已含 PR #106 基线闸 + #107 P0 Graph） |
| **blocks** | `chatbi_intent_hints_step2_v1` — Step 2（C-mid · router + 仲裁）须在 Step 1 合 main 后开干 |
| **experience_capture** | `required` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **推荐路径** | **22 R1**（SDD 清单有待确认项 + `test_strategy: required` + 涉 `api/`） |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| ------------- | ------ | ----------- | ---- |
| HG-TASK-DRAFT | approved | 22-R1, 30 | 10 帽初稿 · 2026-06-04 人签 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-REINSPECT | pending | done, 合并 PR | 50 落盘 `reinspect_results/` 后人签 · 见 **§人类签收清单** |

---

## SPEC 决策（Overview §7 · 00 编排默认 · 10 落盘）

> **SDD 状态**：轮 0+1+2 已完成；Overview §7 四项由本 task **resolved/deferred**，供 22 对照 SPEC 正文是否同步勾选。

| ID | 决策 | 状态 | 说明 |
| --- | --- | --- | --- |
| **Q-1** | 默认 YAML 路径 **`docs/chatbi/v1/intent_hints.yaml`** | **resolved** | 采纳 00 建议；与 [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) §1 一致；`INTENT_HINTS_PATH` 可覆盖 |
| **Q-2** | Step 2 仲裁默认开/关 | **deferred → U2** | 仲裁语义在 Schema `arbitration` · Step 2 SPEC；**本 task 不实现** `on_person_match_force_rag` 等代码路径；U2 task 默认 **仲裁开**、可 env 关（见 Step 2 SPEC 起草） |
| **Q-3** | `freeze_id` 锚定日 | **resolved** | `CHATBI-INTENT-HINTS@2026-06-09`（对齐投递冲刺硬门槛，非「合 main 当日」漂移） |
| **Q-4** | Epic 内 task 切分 | **resolved** | **独立 task** U1 / U2 / U3 三步各一 PR；本单 = **U1 Step 1**；`blocks: chatbi_intent_hints_step2_v1` |

**SPEC 待确认（22 可追问 · 不阻塞 10 落盘）**：

- Overview / Step1 / Schema 仍为 `draft`；合 main 前人审是否将 intent-hints 目录标 `accepted`（非本 task 交付）。
- 本地 `intent_eval` 前后对比是否 **强制** 进 PR 说明（Step1 SPEC §4.3 标可选）。

---

## 1. 背景与目标

Portfolio Unified Chat 在 `prefer=auto` 下，Intent LLM **无站点/人物上下文**，导致五问 **Q4**（`11 年经历里 AI Coding 相关成果？`）及 **刘新宁 / 优势 / 看法 / 经历** 类问句高置信误选 **`direct_answer`**（行业通史或「不知道刘新宁」），尽管 `content/resume/*` 已 ingest。

**本 task 完成态（一句话）**：交付 **Step 1 C-lite** — 外置 `intent_hints.yaml` + `api/intent_hints.py` loader + **`_llm_decide_v2` Prompt 注入**，使上述问句在 stub/集成路径稳定倾向 **`rag_search`**；**不**改 V1 router、**不**改 Graph、**不**改 `unified_chat.py` 主路径语义。

**成功信号（对齐 SPEC + RUNBOOK）**：

| 信号 | 期望 |
| --- | --- |
| Q4 逐字句 | `final_mode` → rag · 有 `rag.sources` · 主 category **`resume`** |
| 人名扩展问 | 同上 · 回答含简历要点（百果园 / Cursor / Ink 等 **至少一项**） |
| 负例 | 「解释一下量子计算，用通俗语言」仍 **`direct_answer`** |
| 降级 | YAML 缺失 / 损坏 / `INTENT_HINTS_ENABLED=0` → **等同现行** · 不 crash |

---

## 2. 范围

| # | 交付 | 要点 |
| --- | --- | --- |
| ① | **`docs/chatbi/v1/intent_hints.yaml`** | Portfolio 默认稿 · 字段见 Schema §4～§5（`version` / `site_mode` / `product_summary` / `persons` / `few_shots` 等） |
| ② | **`api/intent_hints.py`** | `_resolve_hints_path()` · `load_hints()` · `load_resolved_hints()` · `build_intent_hints_prompt_block()`；语义对齐 [`api/text2sql_value_hints.py`](../../api/text2sql_value_hints.py)（mtime 缓存 · UTF-8-sig · 失败返回 `None`） |
| ③ | **`api/intent_agent.py`** | `_llm_decide_v2`：在 `## 总原则` 与 `## 「通用知识」vs「须查资料」` 之间注入配置块；**不改变** JSON 输出 schema |
| ④ | **测试** | `tests/test_intent_hints_loader.py`（或等价）：加载 / 缺失 / 禁用 / 坏 YAML；**追加** 2～4 条 Portfolio `IntentCase` 于 `tests/test_intent_agent_accuracy.py`（stub 可断言） |
| ⑤ | **配置注释** | `.env.example` 注释 `INTENT_HINTS_*`；实现 PR **同步** [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| ⑥ | **可选同 PR** | `api/tools.py` · `rag_search.description` 增半句 Portfolio 语料说明（与 YAML 一致 · 防 registry 漂移） |

**实现约束**：

- 基于 **含 #106+#107 的 `main`**（或本分支 rebase 后）。
- **禁止** diff 含 `api/graph/*` · `unified_chat_graph.py` · Step 2/3 仲裁/router 逻辑。
- Prompt 注入块 **禁止** 含密钥或 `.env` 明文（Schema §6）。

---

## 3. 非范围

- **`api/intent_router.py`** 改动（**U2 · Step 2**）
- **`api/agent.py`** LLM/direct **仲裁**（**U2**；Q-2 defer）
- **`api/tools.py` / `direct_answer` system prompt** 大改（可选半句除外）
- **`api/graph/*`** · **`unified_chat_graph.py`** · `/unified/chat/graph*` 依赖
- **`unified_chat.py`** 行为变更（Step 1 仅 intent 子路径）
- 生产 **sync**、**ingest** 算法、前端 `content/` 改动
- 批量重写 60 条 `intent_eval` 金标（仅 **追加** Portfolio 用例）
- **Step 3**（PROJECT_CONFIG 全量、RUNBOOK 一句、Graph 共用）— **U3** 另 task
- **新 L1 SPEC**（SDD 已冻结 intent-hints 六文 · 本 task 只实现）

---

## 4. 依赖（相对路径 · 只读真值）

| 用途 | 路径 |
| --- | --- |
| Step 1 行为 SPEC | [`SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md) |
| YAML Schema / env | [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) |
| L0 总览 · PR 对齐 | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| 根因 / Timeline | [`SPEC-ChatBI-Intent-Hints-Analysis-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Analysis-v1_zh.md) |
| SPEC 索引 | [`docs/spec/intent-hints/README.md`](../spec/intent-hints/README.md) |
| Portfolio 五问 · Q4 逐字句 | [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §4 |
| Portfolio ingest 真值 | [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) |
| 投递冲刺 | [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) |
| Intent V2 现行 | [`SPEC-ChatBI-V2-Intent.md`](../spec/v2-agent/SPEC-ChatBI-V2-Intent.md) |
| value_hints 参照 | `api/text2sql_value_hints.py` · `docs/text2sql/v1/value_hints.yaml` |
| 环境 / 目录 | [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| Harness 字段 | [`HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5 |
| SDD 过程 | [`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) |
| 合并前必绿 | `AGENTS.md` §8 · `.github/workflows/pytest.yml` |

---

## 行为变更（Delta）

> 相对 **`origin/main` 基线**（Step 1 新增能力 · freeze_id `CHATBI-INTENT-HINTS@2026-06-09`）。

### ADDED

- **Requirement**：外置 `intent_hints.yaml` 经 loader 注入 Intent LLM Prompt，携带 Portfolio 站点/人物/few-shot 上下文。
  - **Scenario**：`step1-hints-prompt-injected` — GIVEN `INTENT_HINTS_ENABLED` 默认开且 YAML 存在 WHEN `_llm_decide_v2` 构建 prompt THEN prompt 含 `## 站点上下文（配置 · intent_hints.yaml）` 段且含 `product_summary` / 人物列表要点。

- **Requirement**：Portfolio Q4 与人名类问句在 stub/增量用例下倾向 `rag_search`。
  - **Scenario**：`step1-portfolio-q4-rag` — GIVEN 问句 `11 年经历里 AI Coding 相关成果？`（RUNBOOK §4 Q4）WHEN `decide_intent_v2`（stub）THEN `tool=rag_search` 且 confidence 达现有门控。
  - **Scenario**：`step1-portfolio-person-rag` — GIVEN 问句含「刘新宁」+「优势/看法/经历」类 trigger WHEN stub THEN `tool=rag_search`。

- **Requirement**：`INTENT_HINTS_ENABLED=0` 或 YAML 缺失时行为等同现行。
  - **Scenario**：`step1-hints-disabled-fallback` — GIVEN 关闭 env 或删除 YAML WHEN loader THEN `load_resolved_hints()` 为 `None` · 注入块为空 · **不抛错**。

### MODIFIED

- **Requirement**：`api/intent_agent.py` Prompt 结构在总原则后增加可选配置块（Previously: 无 `intent_hints` 文件绑定）。
  - **Scenario**：`step1-json-schema-unchanged` — GIVEN 注入开启 WHEN LLM 返回 THEN 仍解析既有 JSON schema（`tool` / `confidence` / `reasoning`）· 无新增必填字段。

### REMOVED

- （无）

---

## 5. 给执行帽（30）的必读列表

1. 本 task **§ SPEC 决策**、§2～§3、`## 验收标准`、`## 失败路径`、`gates_before_code`。
2. [`SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md) §2～§4 全文。
3. [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) §1～§6（含 Portfolio 默认稿 §5）。
4. [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §4 **Q4** 标准问句与 sources 口径。
5. `api/text2sql_value_hints.py` — loader / env / mtime 缓存模式（**照抄语义** · 非复制 SQL 逻辑）。
6. `api/intent_agent.py` — `_llm_decide_v2` 现有 Prompt 节标题与 JSON 解析路径。
7. [`docs/harness/prompts/hats/30-execute-code.md`](../harness/prompts/hats/30-execute-code.md) — 拒开工条件。

**VERIFY（合并前）**：

```bash
pytest tests/test_intent_hints_loader.py -q
pytest tests/test_intent_agent_accuracy.py -q
pytest tests -m "not intent_eval and not intent_benchmark"
```

**可选（本地 diary · 非 PR 硬门槛）**：

```bash
pytest -m intent_eval -q
```

---

## 验收标准

- [ ] `docs/chatbi/v1/intent_hints.yaml` 随仓提交 · 内容与 Schema §5 Portfolio 默认稿 **等价**（允许排版差异）
- [ ] Q4 逐字句（RUNBOOK §4）：stub/集成路径 `final_mode` 倾向 rag · 主 category **`resume`**（集成须 CONTENT_ROOT + sync 已绿 · 见 F3）
- [ ] 「刘新宁…优势/看法」类问句：同上 · 回答含简历要点（百果园 / Cursor / Ink **至少一项** · 集成验收）
- [ ] 「解释一下量子计算，用通俗语言」：仍 **`direct_answer`**
- [ ] YAML 删除或 `INTENT_HINTS_ENABLED=0`：行为回退现行 · loader 单测绿 · **不 crash**
- [ ] `tests/test_intent_hints_loader.py`（或等价）**全绿**
- [ ] `tests/test_intent_agent_accuracy.py` **追加** 2～4 条 Portfolio `IntentCase` **全绿**
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` **全绿**
- [ ] diff **不含** `api/graph/*`
- [ ] `.env.example` + `PROJECT_CONFIG` 已同步 `INTENT_HINTS_ENABLED` / `INTENT_HINTS_PATH`
- [ ] `## 行为变更（Delta）` 与实现 **一致**
- [ ] `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_hints_step1_v1.md` **OK**（若工具存在）

**PR 标题（建议）**：`feat(chatbi): intent_hints Step1 — YAML 注入 Portfolio Intent`

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md` §8）。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试（可选） |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | `fp-step1-yaml-corrupt` | YAML 语法错误 / 根非 dict | loader 返回 `None` · 不注入 · **等同现行** | 是 | 可能仍误路由 direct（与 SPEC F1 一致） | loader 单测 · 坏文件 fixture |
| F2 | `fp-step1-llm-still-direct` | Intent LLM 仍高置信 `direct_answer`（Prompt-only 未 100%） | 无仲裁 · 通史/不知人名 | 是（U2） | Q4/人名仍 FAIL 五问 | stub 增量用例 · 可选 `intent_eval` |
| F3 | `fp-step1-rag-empty-corpus` | 向量库无 resume / `RAG_RETRIEVE_EMPTY` | rag 空结果 · **非 Step1 Intent 范围** | 是 | 检索空 · 查 ingest/sync | RUNBOOK §2 sync 硬检查 · manifest_exempt |
| F4 | `fp-step1-scope-creep` | PR 含 `api/intent_router.py` 仲裁 / `api/graph/*` / Step2 逻辑 | 22/50 **拒签收** · 拆 PR | 否 | 无 | `git diff origin/main...HEAD` |
| F5 | `fp-step1-eval-regression` | 追加用例导致既有 intent stub 回归 | CI pytest **fail** | 是 | 无 | 全集 pytest |
| F6 | `FP-AGENT-LATENCY-V1-FALLBACK` | intent 耗时 > `AGENT_MAX_LATENCY_MS` 且尚未执行工具 | 降级 `intent_router.decide_intent`(V1)；缺 `decide_intent_v1` import → agent stage 失败 | 是 | RUNBOOK Q4 等探针 error | `test_agent_decide_intent_v1_import_bound` · `test_v2_agent_latency_exceeded_v1_fallback_rag` |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 10 帽：U1 Step1 task 初稿 · Overview §7 Q-1～Q-4 落盘 · HG-TASK-DRAFT pending |
| 2026-06-04 | 人签 HG-TASK-DRAFT approved · 00 派 22 R1 |
| 2026-06-04 | HG-AUDIT-R1 approved · 30 实现 Step1 C-lite |
| 2026-06-04 | 40 自检 + 50 复检 + CLOSE · task 归档 `done/` |

---

## 9. 实现备忘（30 帽回填）

| 类别 | 路径 / 说明 |
| --- | --- |
| YAML | `docs/chatbi/v1/intent_hints.yaml` |
| Loader | `api/intent_hints.py` — `load_resolved_hints` · `build_intent_hints_prompt_block` |
| 注入点 | `api/intent_agent.py` — `_llm_decide_v2`「总原则」与「通用知识」之间 |
| 可选 | `api/tools.py` — `rag_search.description` Portfolio 半句 |
| 单测 | `tests/test_intent_hints_loader.py`（9） |
| Portfolio stub | `tests/test_intent_agent_accuracy.py` — `_portfolio_intent_cases()` + 2 mock 测（不并入 60 金标） |
| 配置 | `.env.example` · `PROJECT_CONFIG` — `INTENT_HINTS_*` |
| 实现 commit | `bb59beb` |

---

### 自检结论（执行者）

> **40 帽 · 2026-06-04 · 分支 `task/chatbi-intent-hints-step1-v1` · commit `bb59beb` 基线**

#### 命令与退出码（40 独立复跑）

| 命令 | cwd | exit | 要点 |
| --- | --- | ---: | --- |
| `pytest tests/test_intent_hints_loader.py -q` | 仓根 | **0** | 9 passed |
| `pytest tests/test_intent_agent_accuracy.py -k portfolio -q` | 仓根 | **0** | 2 passed（mock LLM） |
| `pytest tests/test_intent_agent_accuracy.py::test_intent_eval_cases_inventory -q` | 仓根 | **0** | 60 条结构门禁仍绿 |
| `pytest tests/test_intent_agent_accuracy.py::test_stub_eval_end_to_end_writes_exports -q` | 仓根 | **0** | 60 stub 导出链未回归 |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 仓根 | **0** | **298 passed** · 1 skipped |
| `python tools/harness_task_validate.py docs/tasks/done/task_chatbi_intent_hints_step1_v1.md` | 仓根 | **0** | OK |
| `git diff origin/main...HEAD -- api/graph/` | 仓根 | — | **0 行**（F4 scope） |

#### 验收表（40 · 对照 `## 验收标准`）

| 验收项 | 结果 | 证据 |
| --- | :---: | --- |
| `intent_hints.yaml` 随仓 · Schema §5 等价 | **pass** | `docs/chatbi/v1/intent_hints.yaml` · `bb59beb` |
| Q4 逐字 · rag + resume（集成） | **未测** | stub/mock 已覆盖路由期望；**须** RUNBOOK §4 + CONTENT_ROOT 人验 |
| 刘新宁…优势/看法（集成） | **未测** | 同上 · F3 语料依赖 |
| 量子计算 · direct_answer | **pass** | mock LLM 负例 · `_portfolio_intent_cases` |
| YAML 缺失 / `INTENT_HINTS_ENABLED=0` 降级 | **pass** | loader 单测 + `test_portfolio_intent_hints_disabled_*` |
| loader 单测全绿 | **pass** | 9 passed |
| Portfolio IntentCase 2～4 条 stub | **pass** | 4 cases · 2 tests |
| 全集 pytest 全绿 | **pass** | 298 passed |
| diff 不含 `api/graph/*` | **pass** | git diff 空 |
| `.env.example` + PROJECT_CONFIG | **pass** | `INTENT_HINTS_*` 已同步 |
| Delta 与实现一致 | **pass** | Prompt 注入块 · loader 语义对齐 value_hints |
| `harness_task_validate` | **pass** | exit 0 |
| PR pytest workflow | **未测** | 须 CI / 维护者签核 |

#### failure_paths 抽检（F1～F5 · 40）

| Scenario ID | 40 判定 | 证据 |
| --- | :---: | --- |
| `fp-step1-yaml-corrupt` | **pass** | `test_load_hints_corrupt_yaml` · `test_load_hints_non_dict_root` |
| `fp-step1-llm-still-direct` | **pass-with-notes** | Prompt-only 不 100%；F2 诚实 · U2 defer |
| `fp-step1-rag-empty-corpus` | **未测** | 非 Step1 代码范围 |
| `fp-step1-scope-creep` | **pass** | diff 无 router/graph/Step2 |
| `fp-step1-eval-regression` | **pass** | 60 金标 inventory + stub 导出仍绿 |

#### OpenSpec × TDD 三维（40）

| 维度 | 结果 | 备注 |
| --- | :---: | --- |
| Completeness | **pass-with-notes** | F3 集成探针待人验；其余有测例/命令 |
| Correctness | **pass** | 降级返回 None · 不 crash · JSON schema 未改 |
| Coherence | **pass** | 与 Delta / Step1 SPEC / 非范围一致 |

#### 已知未测 / 阻塞

- **Portfolio 五问集成**（Q4 逐字 + sources resume）：须本地/预发 Unified Chat + sync 已绿。
- **PR 线上 `pytest` workflow**：未执行 `gh`/Actions。

**40 结论**：自检 **通过（pass-with-notes）** — 本地必绿全绿；建议 **50 复检** 后开 PR。

---

### 经验摘要（experience_capture · required）

- **Loader 模式复用**：Intent hints 照抄 `text2sql_value_hints` 的 env/mtime/utf-8-sig 语义，避免第二套降级行为。
- **评测隔离**：Portfolio 用例 **不得** 并入 60 条 `intent_eval` 金标（`test_intent_eval_cases_inventory` 硬门禁）；用 mock LLM 专测注入路径。
- **F2 诚实**：Step1 仅 Prompt 注入，真实 LLM 仍可能 direct；U2 仲裁 defer，五问集成验收须与人验并行。

---

### 人类签收清单（关账 · 须人勾选）

- [ ] **HG-REINSPECT**：阅读 [`reinspect_chatbi_intent_hints_step1_v1_20260604_v1.md`](../reinspect_results/reinspect_chatbi_intent_hints_step1_v1_20260604_v1.md) → task `HG-REINSPECT` → `approved`（**单独 commit**）
- [ ] **PR 开单**：标题 `feat(chatbi): intent_hints Step1 — YAML 注入 Portfolio Intent` · 基线 `main` · 分支 `task/chatbi-intent-hints-step1-v1`
- [ ] **CI**：PR 上 **`pytest`** Required check 全绿
- [ ] **RUNBOOK 集成**：[`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §4 — Q4 逐字 + 刘新宁问 → `rag_search` + sources `resume/*`（CONTENT_ROOT + sync 已绿）
- [ ] **负例 smoke**：「解释一下量子计算，用通俗语言」→ `direct_answer`
- [ ] **Overview §7**（可选）：`docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md` §7 checkbox 与 task §SPEC 决策对齐
- [ ] **合并 main** 后：U2 `chatbi_intent_hints_step2_v1` 可开 10 帽

---

### 审查与阶段状态

| 项 | 路径 / 结论 |
| --- | --- |
| 22 R1 | [`task_chatbi_intent_hints_step1_v1_audit_R1_20260604.md`](../harness/reviews/task_chatbi_intent_hints_step1_v1_audit_R1_20260604.md) · 零阻塞 |
| 50 复检 | [`reinspect_chatbi_intent_hints_step1_v1_20260604_v1.md`](../reinspect_results/reinspect_chatbi_intent_hints_step1_v1_20260604_v1.md) · pass-with-notes |
| 关闭回溯 | 见 50 报告 **「执行路线与 Commit 回溯」** |

---

## KPI（00）

> rubric：`KPI_RUBRIC_v1_2` · 关账 2026-06-04

| 指标 | 值 |
| --- | --- |
| **Task_KPI%** | **94** |
| **blocked** | **否**（本地验收绿；CI/集成待人签） |
| **aggregate** | pass-with-notes |

| hat | round | D1 | D2 | D3 | D4 | D5 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | R0 | pass | pass | pass | pass | pass | task + §7 吸收 |
| 22 | R1 | pass | pass | pass | pass | pass | 零阻塞 |
| 30 | — | pass | pass | pass | pass | pass | `bb59beb` · 298 pytest |
| 40 | — | pass | pass | pass | pass | warn | 集成探针未测 |
| 50 | v1 | pass | pass | pass | pass | warn | Fresh Context · 无 Actions |
| CLOSE | — | pass | pass | pass | pass | pass | 回溯已落 50 |

---
