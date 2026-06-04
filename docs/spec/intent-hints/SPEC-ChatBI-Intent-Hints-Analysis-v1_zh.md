# SPEC — ChatBI Intent Hints · 问题分析与方案推导（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **上级** | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| **性质** | 对话分析落盘 · 供 22/50 与实现对照 |

---

## 1. 分析范围

| 项 | 内容 |
| --- | --- |
| **触发** | Portfolio 五问 **Q4** 与 ad-hoc 问句「刘新宁…优势」Intent 误路由 |
| **生产路径** | `POST /api/py/unified/chat` / `stream` · `prefer=auto` · `ChatBIAgent` → `decide_intent_v2` |
| **不在范围** | Graph stub 路由 · Legacy `/api/py/chat` 默认路径 · 前端 BFF |

---

## 2. 期望行为（Portfolio 真值）

来源：[`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) §6.2

| ID | 问句要点 | 期望工具 | 期望 sources |
| --- | --- | --- | --- |
| **Q4** | 11 年经历 · AI Coding 成果 | `rag_search` | `resume/*` · category=`resume` |
| **扩展** | 刘新宁 · 看法/优势/经历 | `rag_search` | `resume/cv-online.md` 等 |

合格回答要点（Q4）：百果园 Cursor + Ink + 连载；**不虚构**。

语料真值：`ai-ink-brain/content/resume/cv-online.md`（标题「刘新宁」）→ `CONTENT_ROOT` + `admin/sync`。

---

## 3. 实际 Timeline 证据

### 3.1 Q4 误路由（摘要）

| 阶段 | 观测 |
| --- | --- |
| Intent | reasoning：「个人经历中的 AI Coding 成果，与项目文档或数据库无关，属于通识问答」 |
| Router | `final_mode=no_data` · `rule_hits=[]` |
| Tool | `direct_answer` · confidence **0.85** |
| 回答 | 2013–2024 行业 AI Coding 发展史（Copilot/GPT 等） |
| sources | **无** |

### 3.2 刘新宁问句（摘要）

| 阶段 | 观测 |
| --- | --- |
| Intent | 「不涉及本仓库文档或数据库查询，适合直接生成回答」 |
| Tool | `direct_answer` |
| 回答 | 「目前没有关于刘新宁的具体信息」 |
| 备注 | `agent.think` 曾出现「Agent 超时，降级到 V1」——即使 fallback，主路径仍为 no_data |

### 3.3 与验收 pass 的关系

[`five-questions-results.md`](../../diary/samples/portfolio-rag-demo/five-questions-results.md) 记录 Q4 **曾 pass**（`q4-sources-run1.json`）。  
结论：**RAG 链路可用** · 问题在 **Intent 非确定性** + **无站点上下文** · 非 ingest 全坏。

---

## 4. 根因分层

### 4.1 认知层（Intent LLM）

- Prompt（`api/intent_agent.py::_llm_decide_v2`）未声明：**本产品是 Portfolio 演示站，个人经历/人名答案在 `content/` 文稿中**。  
- Few-shot 覆盖 macro-F1、量子计算等，**无** Q4/人名/履历类。  
- 模型将「11 年经历」读成 **行业 11 年**；将「刘新宁」读成 **无绑定的普通人名**。

### 4.2 机制层（V2 路由）

```
用户 query
  → decide_intent_v2 (LLM 主决策)
  → confidence ≥ INTENT_MIN_CONFIDENCE (0.6)
  → 直接 step1_tool（无 V1 rule_hits、无 FTS 校验）
  → direct_answer（无检索）
```

- `router.decision.rule_hits=[]`：V2 emit 时不填 V1 规则（非「规则未命中」的完整故事）。  
- `_heuristic_decide` 默认偏 `rag_search`，但 **LLM 开启且成功时不走**。  
- V1 `decide_intent` 无命中时 candidate 默认 `rag`，同样 **被 LLM 绕过**。

### 4.3 配置层（缺失）

| 能力 | Text2SQL | Intent（现状） |
| --- | --- | --- |
| 外置 YAML | `value_hints.yaml` ✅ | **无** ❌ |
| env 路径 | `TEXT2SQL_VALUE_HINTS_PATH` | **无** |
| 注入点 | `build_sql_prompt` | `_llm_decide_v2` 硬编码字符串 |

用户记忆中的「可配置文件辅助 Intent」：**尚无**；本 SPEC 三步补齐。

### 4.4 执行层（direct_answer）

- `direct_answer_execute` system：`你是一个中文助手。请直接回答用户问题。`  
- 无简历上下文 →  honestly 回答「不知道刘新宁」——与 Intent 误判 **一致且加剧**。

---

## 5. 曾评估方案与为何改为「三步 C」

### 5.1 路径 A — 只改 Prompt（Python 字符串）

| 优 | 劣 |
| --- | --- |
| 最快 | 与终态 C 重复劳动 |
| 当天可验证 Q4 | 人名/站点语义硬编码，运维不可配 |

### 5.2 路径 B — 只改 `intent_router.py`

| 优 | 劣 |
| --- | --- |
| 可解释 rule_hits | **单改 B 不解决 LLM 高置信主路径** |
| CI 友好 | 关键词难覆盖「聊聊你对 XX 的看法」 |

### 5.3 路径 C — intent_hints.yaml（终态）

| 优 | 劣 |
| --- | --- |
| 可配置 · 可测 · 可对接 Graph | 一次性做满工期 2～4 天 |

### 5.4 采纳：C-lite → C-mid → C-full

| 决策 | 理由 |
| --- | --- |
| **不** 先 A 再 C | few-shot 写两遍 |
| **不** 6/9 前做满 C-full | Graph/多模式非硬门槛 |
| **Step 1 即 YAML** | 6/9 最小可交付 + 终态同文件演进 |

---

## 6. PR #106 / #107 影响分析（2026-06-04）

| 变更 | 对 Portfolio Intent 影响 |
| --- | --- |
| #106 `INTENT_MIN_CONFIDENCE=0.6` in conftest | 新增 Portfolio eval case 时阈值稳定 ✅ |
| #106 clarify `on` | 仅低置信 clarify · **不解决** 0.85 direct 误判 |
| #107 `agent.py` 抽模块 | Intent 调用点仍在 `agent.py` · 改 arbitration 时注意 import ✅ |
| #107 Graph stub | **无关** · 演示不走 graph 路由 |
| 未改 `intent_agent.py` | Step 1 主改文件 **无 PR 冲突** ✅ |

**方向结论**：PR 106/107 **不改变** 本 SPEC 三步策略；实现 **rebase main 后** 在 Step 1 动手。

---

## 7. 验收探针（实现后必跑）

| # | 探针 | 通过 |
| --- | --- | --- |
| T1 | Q4 逐字句 · auto | `rag_search` · sources `resume/*` |
| T2 | 刘新宁优势/看法 | `rag_search` · 答含简历要点 |
| T3 | 「解释量子计算」 | `direct_answer` |
| T4 | 「昨天销售额是多少」 | `text2sql_query`（样例库可用时） |
| T5 | Intent cache | 改 YAML 后重启 / clear cache 再测 |

---

## 8. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版：Timeline、根因、A/B/C 推导、PR 对齐 |
