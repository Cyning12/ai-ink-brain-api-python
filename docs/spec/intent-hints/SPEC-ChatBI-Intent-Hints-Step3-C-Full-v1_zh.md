# SPEC — ChatBI Intent Hints · Step 3（C-full）（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **阶段** | **Step 3 / 3** · **6/9 后** · 依赖 Step 1+2 |
| **上级** | [`SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md`](./SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md) |
| **前置** | Step 1 · Step 2 |

---

## 1. 目标

将 intent_hints 升为 **运维级真值**：文档齐全、多 `site_mode`、与 **Graph P1 route 节点** 共用配置；Portfolio RUNBOOK 与投递冲刺文档 **显式引用**。

---

## 2. 范围

### 2.1 在范围

| # | 交付 |
| --- | --- |
| S3-1 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` · `INTENT_HINTS_*` 正式表 |
| S3-2 | `.env.example` · Portfolio 段注释与示例路径 |
| S3-3 | [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) · § 前提增 Intent 配置一句 |
| S3-4 | [`投递冲刺_20260609_v1_zh.md`](../governance/投递冲刺_20260609_v1_zh.md) · 可选 § 引用本 SPEC |
| S3-5 | `site_mode: blog` 第二份示例 YAML 或同文件多 profile（实现择一 · task 写死） |
| S3-6 | Graph **预留**：`api/graph/` route 节点读取 `load_resolved_hints()`（**仅当 Graph MVP task 开工**） |
| S3-7 | 回链 [`task_chatbi_v3_intent_classification_debt_v1.md`](../../tasks/active/task_chatbi_v3_intent_classification_debt_v1.md) §2 · 标记 Portfolio 子项已覆盖 |
| S3-8 | diary：`intent_hints` 前后 intent_eval 或五问复跑摘要（路径由 task 指定） |

### 2.2 非范围

- Graph 全链 parity（属 [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) P1 task）  
- Intent vNext 多候选 + 裁判（P3+ · 债务母单 §2.1）  
- 前端 Unified Chat UI 改动  

---

## 3. 多模式（site_mode）

| mode | 用途 | YAML |
| --- | --- | --- |
| `portfolio` | 演示站 · 6/9 | 默认稿（Step 1） |
| `blog` | Ink 全站（未来） | 扩展 `product_summary` · 人名可为空 |
| `default` | 缺省 | 仅通用「项目文档优先」短段 |

**实现选项（task 冻结其一）**：

- **A**：单文件 · 顶层 `site_mode` + env `CHATBI_SITE_MODE` 选段  
- **B**：`intent_hints.portfolio.yaml` / `intent_hints.blog.yaml` + `INTENT_HINTS_PATH`  

---

## 4. Graph 对接（预留 · D-2）

| 项 | 说明 |
| --- | --- |
| **原则** | Legacy Unified **继续**用 `decide_intent_v2` + hints；Graph 新路由 **读同一 loader** |
| **P0 现状** | Graph stub **无** Intent · 本步仅文档 + 函数导出 |
| **P1 落点** | Graph `route` 节点 Prompt 注入 `build_intent_hints_prompt_block()` |
| **超时差异** | Legacy：`LLM_API_TIMEOUT` → V1（`failure_edges_legacy`）；Graph：D-3 方案 A → 见 [`api/graph/state.py`](../../../api/graph/state.py) |

---

## 5. 验收标准

- [ ] PROJECT_CONFIG + RUNBOOK 可让运维 **仅改 YAML/env** 切换 portfolio 语义  
- [ ] Step 1+2 验收全集仍 pass  
- [ ] `tech_graph_contract_check` 若 Step 2 增 `raw_response` 字段则 manifest 同步  
- [ ] Overview §7 待确认清单 **清零** 或转入 task done  
- [ ] 本目录 SPEC 状态可由 `draft` → `active`（人审 freeze_id）  

---

## 6. 建议 task / PR

| 项 | 建议 |
| --- | --- |
| **task_slug** | `chatbi_intent_hints_step3_v1` |
| **时间** | 2026-06-10 起 |
| **PR 标题** | `docs(chatbi): intent_hints Step3 — 运维真值与 Graph 预留` |

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初版 Step 3 |
