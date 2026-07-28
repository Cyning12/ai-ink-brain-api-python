# Task：ChatBI Intent Hints — Step 2（C-mid · router 同步 + LLM 仲裁）

> **状态**：`done`（2026-06-06 · `CHATBI-INTENT-HINTS@2026-06-09` · PR [#111](https://github.com/Cyning12/ai-ink-brain-api-python/pull/111) @ `0fe7d2d` · Task_KPI% 88 pass）  
> **Epic**：ChatBI Intent Hints · **U2 · Step 2**  
> **时间门槛**：[`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) §2 — **6/9 sprint 建议合 main**（优先于 Step3）  
> **关联图谱**：`api/intent_hints.py` · `api/intent_router.py` · `api/intent_agent.py` · `api/agent.py` · **无** `api/graph/*`  
> **母单回链**：[`task_chatbi_intent_hints_step1_v1.md`](done/task_chatbi_intent_hints_step1_v1.md) · U1.5 已合 #110  
> **50 复检**：[`reinspect_chatbi_intent_hints_step2_v1_20260604_v1.md`](../reinspect_results/reinspect_chatbi_intent_hints_step2_v1_20260604_v1.md)  
> **22 R1**：[`task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md`](../harness/reviews/by-task/chatbi_intent_hints_step2_v1/task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md)  
> **关闭回溯**：[`invoke_20260606_CLOSE_chatbi-intent-hints-step2-v1.md`](../harness/invokes/by-task/chatbi_intent_hints_step2_v1/invoke_20260606_CLOSE_chatbi-intent-hints-step2-v1.md)

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **test_strategy_note** | 涉 `api/intent_hints.py` · `api/intent_router.py` · `api/intent_agent.py`/`api/agent.py` 仲裁；须 router Portfolio 用例 + mock LLM direct→rag 仲裁单测；关账前须 50 落盘 |
| **audit_profile** | `post_close` |
| **freeze_id** | `CHATBI-INTENT-HINTS@2026-06-09`（沿用 U1 · 见 **§ SPEC 决策**） |
| **gates_before_code** | `harness_task_validate.py` OK · `## SPEC 决策` Q-2 resolved · `## 失败路径` + Scenario ID · `## 验收标准` 含 pytest · `## 行为变更（Delta）` 已填 · 必读列表已读 · `HG-TASK-DRAFT` = `approved` · `HG-AUDIT-R1` = `approved`（路径 A 后） |
| **git_branch** | `task/chatbi-intent-hints-step2-v1`（从 **最新 `origin/main`** 拉出；开干前 `git fetch && git rebase origin/main`） |
| **Open Folder** | `ai-ink-brain-api-python` |
| **blocked_by** | （无 — main 已含 #109 Step1 + #110 U1.5） |
| **blocks** | `chatbi_intent_hints_step3_v1` — Step 3（C-full · PROJECT_CONFIG/RUNBOOK/Graph 共用）须在 Step 2 合 main 后开干 |
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
| HG-AUDIT-R1 | approved | 30 | 22 R1 零阻塞 · 2026-06-04 人签 |
| HG-REINSPECT | approved | done, 合并 PR | 50 落盘 `reinspect_results/` 后人签 |

---

## SPEC 决策（Overview §7 · U2 落盘）

> **SDD 状态**：轮 0+1+2 已完成；U1 已 resolved Q-1/Q-3/Q-4；**本 task resolved Q-2**。

| ID | 决策 | 状态 | 说明 |
| --- | --- | --- | --- |
| **Q-1** | 默认 YAML 路径 `docs/chatbi/v1/intent_hints.yaml` | **引用 U1** | 不重复争论 · 见 Step1 task |
| **Q-2** | Step 2 仲裁默认开/关 | **resolved** | **默认开**：YAML `arbitration.enabled: true`（缺省同 true）· env `INTENT_HINTS_ARBITRATION` 显式 `0/false/no/off` **关** · 关时 **零行为变更**（仅 Prompt 注入路径，同 Step1） |
| **Q-3** | `freeze_id` 锚定日 | **引用 U1** | `CHATBI-INTENT-HINTS@2026-06-09` |
| **Q-4** | Epic 内 task 切分 | **引用 U1** | 本单 = **U2 Step 2** 独立 PR |

**仲裁语义（对齐 Step2 SPEC §3 · 非「降置信 fallback」）**：

- 人名 + `rag_triggers` 命中且 LLM 选 `direct_answer` → **强制** `rag_search` · reasoning 追加配置说明  
- `rag_signals.regex` career_span 命中且 LLM 选 `direct` → **强制** `rag_search`  
- `prefer=rag|text2sql|no_data` **强制** > 仲裁 > LLM 原判  
- 负例（量子计算等）· 无配置命中 → **不** 仲裁  

**SPEC 待同步（22 可追问 · 不阻塞 10 落盘）**：

- Overview §7 正文 checkbox 是否与 U1/U2 task 决议同步勾选（非本 task 代码交付）  
- `hints_arbitration` 是否登记 cross-repo contract（实现 PR 评估 · 默认仅 `raw_response` 内观测）

---

## 1. 背景与目标

Step1（#109）通过 **Prompt 注入** 使 Portfolio Q4 / Q-INTENT 在 Intent LLM 路径倾向 `rag_search`；U1.5（#110）补 **LLM 外呼重试 + 超时阶梯**。

**仍缺口（Step2 要补）**：

| 路径 | 现象 | Step2 手段 |
| --- | --- | --- |
| Intent **超时 → V1** | V1 `_rag_rule_hits` **无** Portfolio 词表 · Q4 可能仍 `no_data` | YAML `rag_signals` + `persons` 并入 router |
| LLM **高置信 direct** | Prompt-only 未 100% · 仍答通史/不知人名 | `apply_hints_arbitration` 强制改 rag |
| **`CHATBI_V2_INTENT_LLM=false`** | 启发式/V1 无站点词 | 同上 router 合并 |

**本 task 完成态（一句话）**：**同一份** `intent_hints.yaml` 驱动 V1 规则合并 + 可选 LLM/direct 仲裁；Step1 行为 **不回归**；五问 + Q-INTENT 在 mock/关 LLM 路径稳定 rag。

**人验留证（U1 · 不重复 reinspect）**：Step1 五问 **5/5 已通过**；RUNBOOK §4.1 Q-INTENT 已写入验收参考。

---

## 2. 范围

| # | 交付 | 要点 |
| --- | --- | --- |
| **S2-1** | `api/intent_hints.py` | `rag_rule_hits_from_hints(query, hints) -> list[str]` · `match_person_rag_signal(query, hints) -> bool` · 可选 `arbitration_enabled(hints) -> bool` |
| **S2-2** | `api/intent_router.py` | `_rag_rule_hits` 合并 YAML hits（`rule:portfolio_keyword` / `rule:portfolio_regex:*` / `rule:portfolio_person`）；文件缺失 = 仅硬编码词表 |
| **S2-3** | `api/intent_agent.py` 和/或 `api/agent.py` | `apply_hints_arbitration(decision, query, hints?) -> IntentDecision` · 在 `decide_intent_v2` 成功返回前调用 |
| **S2-4** | YAML + env | `docs/chatbi/v1/intent_hints.yaml` 增 `arbitration:` 段（Schema §4.5）· `.env.example` + `PROJECT_CONFIG` 增 `INTENT_HINTS_ARBITRATION` |
| **S2-5** | `tests/test_intent_router_backend_v1.py` | Portfolio：Q4 逐字 · Q-INTENT · `CHATBI_V2_INTENT_LLM=false` → `final_mode` rag · rule_hits 含 portfolio 类 |
| **S2-6** | `tests/test_intent_hints_arbitration.py`（或 agent 单测） | mock LLM direct + Q4/Q-INTENT → 仲裁后 `rag_search` · 仲裁关 = 不变 · 量子计算负例不仲裁 |

**实现约束**：

- 基于 **含 #109+#110 的 main**（本分支 rebase 后）。  
- **禁止** diff 含 `api/graph/*` · `unified_chat_graph.py` · Step3 全量运维文档。  
- **不** 批量改 60 条 intent_eval 金标（可 **追加** Portfolio stub 用例）。

---

## 3. 非范围

- Step1 Prompt 注入逻辑 **大改**（仅仲裁 hook · 非重写 `_llm_decide_v2` prompt 结构）  
- Graph runner / `/unified/chat/graph*`  
- FTS 证据校验重写  
- Step3：`PROJECT_CONFIG` 全量 · RUNBOOK 一句 · Graph route 共用（**U3**）  
- 新 L1 SPEC 文件  

---

## 4. 依赖（相对路径 · 只读真值）

| 用途 | 路径 |
| --- | --- |
| Step 2 行为 SPEC | [`SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md) |
| Schema · arbitration | [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) §4.3 · §4.5 |
| L0 总览 | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| U1 关账 | [`task_chatbi_intent_hints_step1_v1.md`](done/task_chatbi_intent_hints_step1_v1.md) |
| 五问 + Q-INTENT | [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §4 · §4.1 |
| 默认 YAML | [`docs/chatbi/v1/intent_hints.yaml`](../../chatbi/v1/intent_hints.yaml) |
| V1 router | `api/intent_router.py` |
| V2 intent | `api/intent_agent.py` · `api/agent.py` |
| Loader | `api/intent_hints.py` |
| Harness 字段 | [`HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5 |
| 合并前必绿 | `AGENTS.md` §8 · `.github/workflows/pytest.yml` |

---

## 行为变更（Delta）

> 相对 **`origin/main` 基线**（Step 2 新增 · freeze_id 不变）。

### ADDED

- `intent_hints.py`：YAML 驱动的 rule hit / person match / arbitration 开关读取  
- `intent_router._rag_rule_hits`：合并 Portfolio YAML 信号  
- `apply_hints_arbitration`：配置命中 + LLM direct → 强制 `rag_search`  
- `intent_hints.yaml`：`arbitration` 段（默认 enabled）  
- env `INTENT_HINTS_ARBITRATION`  
- 单测：`test_intent_hints_arbitration.py` · router Portfolio 扩展  

### MODIFIED

- `api/intent_agent.py` 和/或 `api/agent.py`：decision 返回链插入仲裁  
- `.env.example` · `PROJECT_CONFIG`：`INTENT_HINTS_ARBITRATION`  

### REMOVED

- 无  

---

## 验收标准

- [x] Step1 回归：`tests/test_intent_hints_loader.py` · Portfolio stub intent 用例 **仍绿**  
- [x] **mock** LLM 返回 `direct_answer` + Q4 逐字（`11 年经历里 AI Coding 相关成果？`）→ 仲裁后 **`rag_search`** · `raw_response.hints_arbitration.applied=true`  
- [x] **mock** LLM direct + Q-INTENT（RUNBOOK §4.1 逐字）→ 同上  
- [x] `CHATBI_V2_INTENT_LLM=false` · Q4 → V1/启发式路径 **`final_mode=rag`**（或等价 rag 候选 · 见 router 单测）  
- [x] 负例「解释一下量子计算，用通俗语言」→ **不** 触发仲裁 · 仍 `direct_answer`  
- [x] `INTENT_HINTS_ARBITRATION=0` → 行为 **等同 Step1**（仲裁不生效 · 单测断言）  
- [x] Intent 超时 → V1：`decide_intent_v2` mock 超时 + Q4 → V1 rule_hits 含 **portfolio** 类 · candidate rag（单测或 router 直测）  
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` **全绿**（关账 Fresh Context：**323 passed** · 1 skipped）  
- [x] diff **不含** `api/graph/*`  
- [x] `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` **OK**  
- [x] PR **`pytest`** workflow Required check 全绿（PR #111 · 2026-06-04 merge · `gh` 核对 SUCCESS）

**PR 标题（建议）**：`feat(chatbi): intent_hints Step2 — router 同步与 LLM 仲裁`

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md` §8）。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试（可选） |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | `fp-step2-arbitration-off` | `INTENT_HINTS_ARBITRATION=0` 或 YAML `arbitration.enabled: false` | **不** 改 LLM 原判 · 等同 Step1 | — | 可能仍 direct（已知） | 单测 · env 关 |
| F2 | `fp-step2-yaml-missing` | YAML 缺失 / 损坏 | router 仅硬编码 · 仲裁无配置命中 | 是 | 同 Step1 F1 | loader 回归 |
| F3 | `fp-step2-over-rag` | 通识句误触 keyword（如单独「经历」） | 须负例单测 guard · 无 person/regex 命中则不仲裁 | 是 | 误检索 | 量子计算负例 |
| F4 | `fp-step2-prefer-override` | `prefer=rag|text2sql|no_data` 强制 | **仲裁不覆盖** prefer 强制 | 否 | 按 prefer | router/agent 单测 |
| F5 | `fp-step2-scope-creep` | PR 含 Graph / Step3 全量 | 22/50 **拒签收** | 否 | 无 | git diff |
| F6 | `fp-step2-v1-timeout-no-portfolio-hit` | 超时降级 V1 但 YAML 未合并 | Q4 仍 no_data | 是 | 五问 FAIL | router 单测 Q4 |

---

## 给执行帽的必读列表（30 开干前）

1. 本 task 全文 + **§ SPEC 决策 Q-2**  
2. [`SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md) §3～§4  
3. [`SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md`](../spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md) §4.5  
4. `api/intent_router.py` — 现有 `_rag_rule_hits`  
5. `api/intent_hints.py` — 现有 loader（扩展 S2-1）  
6. `api/intent_agent.py` — `decide_intent_v2` 返回链 · U1.5 重试  
7. [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §4 · §4.1  
8. [`docs/harness/prompts/hats/30-execute-code.md`](../harness/prompts/hats/30-execute-code.md) — 拒开工条件  

**VERIFY（合并前）**：

```bash
pytest tests/test_intent_hints_arbitration.py tests/test_intent_router_backend_v1.py -q
pytest tests/test_intent_hints_loader.py -q
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

### 自检结论（执行者）

**日期**：2026-06-04 · **分支**：`task/chatbi-intent-hints-step2-v1` · **工作目录**：仓库根

| 命令 | exit | 要点 |
| --- | ---: | --- |
| `pytest tests/test_intent_hints_arbitration.py tests/test_intent_router_backend_v1.py -q` | 0 | 17 passed |
| `pytest tests/test_intent_hints_loader.py -q` | 0 | 9 passed |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | **312 passed** · 1 skipped |
| `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` | 0 | OK |
| `git diff -- api/graph/` | — | **0 行** |

**交付摘要（S2-1～S2-6）**：

- `api/intent_hints.py`：`rag_rule_hits_from_hints` · `match_person_rag_signal` · `arbitration_enabled` · `apply_hints_arbitration` 前置信号  
- `api/intent_router.py`：`_rag_rule_hits` 合并 YAML portfolio 规则  
- `api/intent_agent.py`：`apply_hints_arbitration` · LLM 成功路径插入  
- `intent_hints.yaml`：`arbitration.enabled: true` · env `INTENT_HINTS_ARBITRATION`  
- `tests/test_intent_hints_arbitration.py`（新建）· router Portfolio 扩展 3 用例  

**已知未测**：RUNBOOK 五问/Q-INTENT **真实 LLM 人验**（Step1 已 5/5，本 task 以 mock/router 单测为准）。

#### 关账补记（2026-06-06 · main @ `0fe7d2d`）

| 项 | 结果 |
| --- | --- |
| 合入 | PR **#111** `0fe7d2d` · 2026-06-04 merged |
| PR CI | `pytest` · `contract_check` · `manifest_check` · `verify` — **SUCCESS** |
| Fresh Context 复验 | 仲裁+router **17 passed** · loader **9 passed** · 全集 **323 passed** · graph diff **0 行** |
| human_gate | HG-TASK-DRAFT / HG-AUDIT-R1 / HG-REINSPECT — **approved**（`harness_human_gate_check` OK） |
| 与 50 差异 | 50 时点 312 passed / HG-REINSPECT pending；关账 main 增其他 PR 用例 → **323 passed** |

---

### 经验摘要（experience_capture · required）

> Portfolio 仲裁 vs Prompt-only；prefer 覆盖未单测 → pass-with-notes。

1. **Step1 缺口**：Prompt-only 注入使 Portfolio Q4 倾向 rag，但 LLM 高置信 `direct_answer` 或 V1 超时路径仍可能 miss — Step2 补 **router YAML 合并** + **`apply_hints_arbitration`**。
2. **双路径设计**：router 侧 `_rag_rule_hits` 合并 YAML（V1/关 LLM）；agent 侧仲裁在 LLM 成功返回前强制改 rag — 两路共用同一份 `intent_hints.yaml`。
3. **仲裁开关**：Q-2 默认开（YAML `arbitration.enabled: true`）；`INTENT_HINTS_ARBITRATION=0` 时 **零行为变更**（等同 Step1）。
4. **prefer 优先级**：`prefer=rag|text2sql|no_data` 在 router 先行，仲裁 **不覆盖** — 50 pass-with-notes：**未增 prefer 单测**，后续 Step3 或回归批次可补。
5. **排障口诀**：Portfolio 仍 no_data → 先查 V1 rule_hits 是否含 portfolio 类 · 再查 LLM direct 是否被仲裁 · 最后查 env 关断。

---

## KPI（00）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: 88% · **状态**: pass · **帽**: 22→30→40→50→CLOSE · **aggregator**: CLOSE

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
|----------|-------|------------|----|----|----|----|-----|----------------|
| 22 | R1 | main_chat | 100 | 100 | 100 | 100 | — | Q-2 resolved · 零阻塞 |
| 30 | R1 | main_chat | 100 | 100 | 100 | 100 | — | S2-1～S2-6 交付 · 无 graph diff |
| 40 | R1 | main_chat | 100 | 100 | 100 | 100 | — | 312 pytest 绿（40 时点） |
| 50 | v1 | main_chat | 100 | 60 | 100 | 100 | 100 | pass-with-notes：prefer 覆盖未单测 · yaml-missing router 未专测；关账 PR #111 CI SUCCESS |

| 指标 | 值 |
| --- | --- |
| Task_KPI% | **88%** |
| blocked | **无** |

**D2 聚合**：min(100,100,100,60)=60 · **D5 聚合**：100 · **状态**：pass（≥80，无 blocked）

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | **Harness 关账**：`git mv` → `done/` · KPI 88% · Fresh Context 复验 main 全绿 · 合入 PR #111 @ `0fe7d2d` |
| 2026-06-04 | 50 独立复检 pass-with-notes · reinspect `reinspect_chatbi_intent_hints_step2_v1_20260604_v1.md` |
| 2026-06-04 | 10 帽：U2 Step2 task 初稿 · Q-2 resolved · HG-TASK-DRAFT pending |
| 2026-06-04 | 人签 HG-TASK-DRAFT approved（gate 独立 commit） |
| 2026-06-04 | 30/40：Step2 实现 + 自检 · 312 pytest 绿 |
