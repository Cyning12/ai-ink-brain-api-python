# SPEC — ChatBI Intent Hints · Step 2（C-mid）（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **阶段** | **Step 2 / 3** · 6/9 **建议** · 依赖 Step 1 合 main |
| **上级** | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| **前置** | [`SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md) |

---

## 1. 目标

**同一份** `intent_hints.yaml` 驱动：

1. V1 **`_rag_rule_hits`**（keywords + regex + 人名）  
2. **可选仲裁**：配置命中 + LLM 选 `direct_answer` → 覆盖为 `rag_search`（或降低置信并走 fallback）

补齐 Step 1 **未覆盖** 路径：Intent **超时 → V1**、**LLM 高置信仍误判**、**关 LLM** 时的 Portfolio 稳定度。

---

## 2. 范围

### 2.1 在范围

| # | 交付 |
| --- | --- |
| S2-1 | `api/intent_hints.py`：`rag_rule_hits_from_hints(query, hints)` · `match_person_rag_signal(query, hints)` |
| S2-2 | `api/intent_router.py`：`_rag_rule_hits` 合并 YAML 信号（文件缺失则仅硬编码词表） |
| S2-3 | `api/intent_agent.py` 或 `api/agent.py`：`apply_hints_arbitration(decision, query, hints)` |
| S2-4 | Schema `arbitration` 段生效 · env `INTENT_HINTS_ARBITRATION` |
| S2-5 | `tests/test_intent_router_backend_v1.py` · Portfolio 规则用例 |
| S2-6 | `tests/test_intent_hints_arbitration.py`（或并入 agent 单测） |

### 2.2 非范围

- Graph runner / 边表实现  
- FTS 证据校验重写（仍非本步）  
- 修改 60 条既有金标（除新增 Portfolio 条）  

---

## 3. 仲裁规则（建议默认）

| 条件 | LLM 输出 | Step 2 行为 |
| --- | --- | --- |
| `persons[].name` + `rag_triggers` 任一在 query 中 | `direct_answer` | **强制** `rag_search` · reasoning 追加「配置：站点人物须查 resume」 |
| `rag_signals.regex` career_span 命中 | `direct_answer` | **强制** `rag_search` |
| 无配置命中 | 任意 | **不** 仲裁 |
| 明确负例句（Schema exceptions 仅 Prompt；实现可选 keyword 豁免） | `direct_answer` | 保持 direct |

**优先级**：`prefer=rag|text2sql|no_data` **强制** > 仲裁 > LLM 原判。

**可观测**：`IntentDecision.raw_response` 增 `hints_arbitration: { applied, reason }`（若契约允许 · 实现 PR 评估是否需 contract 登记）。

---

## 4. V1 规则合并

```text
rule_hits = hardcoded_rag_hits(query)
         ∪ hints_rag_keywords(query)
         ∪ hints_regex_hits(query)
         ∪ hints_person_hits(query)
```

当 `decide_intent_v2` **超时** 降级 V1 时：Portfolio 问句应出现 `rule:portfolio_*` 类 hit，candidate → `rag`。

---

## 5. 验收标准

- [ ] Step 1 全部验收仍 pass  
- [ ] **模拟** LLM 返回 direct + Q4 问句 · 仲裁后 `rag_search`（单测 mock）  
- [ ] `CHATBI_V2_INTENT_LLM=false` · Q4 → 启发式/V1 路径 **rag**  
- [ ] 负例「量子计算」· **不** 被人名/经历词表误伤（eval 或单测）  
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿  

---

## 6. 建议 task / PR

| 项 | 建议 |
| --- | --- |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **blocked_by** | Step 1 合 main |
| **PR 标题** | `feat(chatbi): intent_hints Step2 — router 同步与 LLM 仲裁` |

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版 Step 2 |
