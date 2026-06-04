# SPEC — ChatBI Intent 站点上下文（intent_hints）总览（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **freeze_id（建议）** | `CHATBI-INTENT-HINTS@2026-06-09` |
| **分支（起草）** | `task/chatbi-graph-harness-showcase-v1` |
| **目录索引** | [`README.md`](./README.md) |
| **SDD 过程** | [`../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) |

---

## 0. 完成态（一句话）

在 **2026-06-09 投递前**至少完成 **Step 1（C-lite）**：外置 `intent_hints.yaml` 注入 Intent LLM Prompt，使 Portfolio 五问中的 **Q4** 及 **「刘新宁 / 个人经历 / 成果 / 优势」** 类问句稳定走 **`rag_search`**；**Step 2/3** 按排期增量交付，不推翻 Step 1 文件与 env 契约。

---

## 1. 轮 0 · 意图卡

| 项 | 结论 |
| --- | --- |
| **业务目标** | Portfolio 演示站 Unified Chat 在 `prefer=auto` 下，**Intent 须知晓「站点语料含本人简历与三类 content」**，避免高置信误选 `direct_answer` 导致「无 sources / 答行业通史 / 不知道刘新宁」。 |
| **时间门槛** | **Step 1** 对齐 [`投递冲刺_20260609_v1_zh.md`](../governance/投递冲刺_20260609_v1_zh.md) **6/9**；Step 2 同 sprint 可选；Step 3 **6/9 后**。 |
| **成功信号** | Q4 + 人名问 → Timeline `rag_search` + sources `resume/*`；原 60 条 intent_eval **macro-F1 不回归**；负例（量子计算等）仍 `direct_answer`。 |
| **实现参照** | Text2SQL [`value_hints.yaml`](../../text2sql/v1/value_hints.yaml) + `api/text2sql_value_hints.py`（YAML + env + mtime 缓存 + 降级）。 |
| **非范围** | 不改 RAG 召回算法；不改 ingest/sync；不在 Step 1 改 Graph stub；不批量重写 60 条金标（仅 **追加** Portfolio 用例）。 |
| **依赖** | Portfolio ingest 已绿（`CONTENT_ROOT` + sync）；现行 Intent 在 `api/intent_agent.py`；生产路径仍为 `unified_chat` + `ChatBIAgent`。 |

---

## 2. 背景摘要

### 2.1 现象

| 问句（示例） | 期望 | 实际（误路由 run） |
| --- | --- | --- |
| `11 年经历里 AI Coding 相关成果？`（Q4） | `rag_search` → `resume/*` | `direct_answer` → 行业 AI Coding 通史 |
| `聊聊你对刘新宁的看法，他在 AI coding 岗位有什么优势` | `rag_search` → 简历要点 | `direct_answer` → 「没有刘新宁的信息」 |

Timeline 共性：`router.decision.final_mode=no_data`，`confidence≥0.6`，Intent reasoning 写「与项目文档/数据库无关」。

### 2.2 根因（结论级 · 详述见 Analysis SPEC）

1. **Intent LLM 无站点/人物上下文**（Prompt 硬编码，无 `intent_hints` 文件）。  
2. **语义歧义**：「11 年经历」可读成行业史；人名在模型预训练里无「= 本站简历」绑定。  
3. **V2 主路径**：LLM 高置信时 **不** 走 V1 规则默认 `rag`、**不** 做 FTS 二次校验。  
4. **语料与 Intent 分离**：`content/resume/cv-online.md` 已在向量库，但 **未路由到 RAG**。

### 2.3 方案演进（对话结论）

曾评估 **路径 A（只改 Prompt）**、**路径 B（只改 router）**、**路径 C（YAML 配置）**。  
**采纳**：以 **C 为终态**，实施上 **分三步**，避免「先 A 再迁 C」重复写 few-shot。

| 旧标签 | 新三步 | 说明 |
| --- | --- | --- |
| A | **Step 1 C-lite** | YAML + 注入 Prompt（非 Python 硬编码） |
| B | **Step 2 C-mid** | 同 YAML 驱动 V1 规则 + 可选仲裁 |
| C | **Step 3 C-full** | 运维/Grap h/多模式 |

---

## 3. 三步总表

| 步 | 代号 | 目标 | 6/9 | 独立 PR |
| --- | --- | --- | --- | --- |
| **1** | C-lite | YAML + loader + Prompt 注入 + Portfolio eval | **必须** | 是 |
| **2** | C-mid | router 读同文件 + LLM/direct 仲裁 | 建议 | 是 |
| **3** | C-full | PROJECT_CONFIG、RUNBOOK、Graph route 共用 | 否 | 是 |

各步 **验收、文件清单、非范围** 见对应 Step SPEC；**YAML 字段** 见 Schema SPEC。

---

## 4. 与 Portfolio / Harness 关系

| 项 | 关系 |
| --- | --- |
| [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) | 本 SPEC **不替代** ingest/五问真值表；仅补 **Intent 路由** 缺口 |
| 五问 RUNBOOK | Step 3 增 **一句**：Intent 依赖 `intent_hints.yaml`（portfolio 模式） |
| 建议 task_slug | `portfolio_intent_hints_v1` 或 `chatbi_intent_hints_step1_v1`（冻结后开 active task） |

---

## 5. 与 PR #106 / #107 对齐（已合 main）

| PR | 对本 SPEC 影响 |
| --- | --- |
| **#106** 基线闸 | `INTENT_MIN_CONFIDENCE=0.6` 测试固定 · clarify 接受 `on` · **不改变** Intent 误判主因 |
| **#107** P0 Graph | `agent.py` 模块化 · Graph **stub** · **`intent_agent.py` 未改** · Portfolio 仍走 Unified |

**约束**：

- 实现基于 **含 #106+#107 的 main**（或本 showcase 分支 rebase 后）。  
- Step 1 **禁止** 依赖 `/unified/chat/graph*`。  
- Step 3 Graph 对接为 **预留**，不阻塞 Step 1 合 main。

---

## 6. 风险与降级

| 风险 | 缓解 |
| --- | --- |
| YAML 缺失/损坏 | loader 返回 `None`，行为 **等同现行**（与 value_hints 一致） |
| over-rag（通识也检索） | Schema 中 `direct_answer_exceptions` + eval 负例 |
| Intent 缓存 5min | 改 YAML 后重启或 `clear_intent_cache`（文档化） |
| eval 漂移 | 每步 PR 附 intent_eval 前后对比或 stub 增量测试 |

---

## 7. 待确认清单（冻结前）

- [ ] **Q-1**：默认 YAML 路径 `docs/chatbi/v1/intent_hints.yaml` 是否接受（vs `data/intent_hints.yaml`）  
- [ ] **Q-2**：Step 2 仲裁默认 **开/关**（建议 Step 2 PR 默认 **开**，可 env 关）  
- [ ] **Q-3**：`freeze_id` 日期是否锚定 **6/9** 或 Step 1 合 main 日  
- [ ] **Q-4**：是否与 Portfolio Epic 同 task 或独立 task（建议 **独立 task · blocks 无**）

---

## 8. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版 L0：背景、三步、PR 对齐、待确认 |
