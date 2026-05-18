# Task：博客 RAG — GraphRAG 试点探索（小范围 / 可选独立页）

> **状态**：`backlog`（**不阻塞**现有 Hybrid RAG 主线；仅供了解实际使用与成本，待排期后小范围试点）  
> **登记日期**：2026-05-18  
> **分支**：`docs/rag-graphrag-pilot-backlog-v1`（自 `main` 拉出，需求池落盘）  
> **背景对照**：[`docs/diary/jsonPKmermaid/Ink博客RAG_vs_GraphRAG_对照.md`](../diary/jsonPKmermaid/Ink博客RAG_vs_GraphRAG_对照.md)  
> **关联图谱**：`docs/_tech_graph/10_flow_rag.md`、`01_struct.md`  
> **前端依赖**：可选（见 §4.2「独立页」）；首阶段可仅后端 dev 路由

---

## 1. 背景与目标

Ink 博客 RAG 当前为 **chunk + 向量 + FTS + RRF**（经典 Hybrid RAG），**非** GraphRAG。团队在概念上已对齐差异（见背景对照文档），但缺少 **真实语料上的使用体感**：建图成本、Global/Local 收益、幻觉与延迟。

**完成态（试点级，非生产默认）**：

- 在 **受控范围**（如 `diary/` 子集或固定 N 篇）跑通 **最小 GraphRAG 离线索引**；
- 提供 **小范围入口**（dev API 或内部页面）对比「现有 RRF」vs「GraphRAG 路径」；
- 产出 **可复现报告**：token、延迟、人工抽检问答质量（含 Global 类问题）。

---

## 2. 范围

- [ ] **T0 范围钉死**：试点语料目录、篇数上限、是否含 `diary` only；`freeze_id` / 实验 run 目录约定。
- [ ] **T1 离线索引（最小）**：在保留现有 `documents` ingest 前提下，**增量**脚本：实体/关系抽取 → 图存储（新表或 JSON 工件，**不替换** `ingest_pipeline` 主路径）。
- [ ] **T2 社区摘要（可选减配）**：若成本过高，可先 **仅 Local**（子图 + 原 chunk），Global 社区摘要作为 T2b 开关。
- [ ] **T3 在线对比路由**：`admin` 或 `debug` 级 API（须鉴权），请求体指定 `recall_mode: hybrid | graphrag_local | graphrag_global`；**默认生产仍为 hybrid**。
- [ ] **T4 评测集**：≥10 条黄金问句（局部事实 + 跨篇主题各半），记录 sources 与人工 pass/fail。
- [ ] **T5 结论文档**：写入 `docs/diary/jsonPKmermaid/reports/`（命名 `conclusion_graphrag_pilot_*`），含 **继续 / 搁置 / 全量** 建议。

## 非范围

- **不**替换 `/api/py/chat`、`unified/chat` 的默认召回策略。  
- **不**与 `docs/_tech_graph/` 治理层、`graph_query` 合并（见对照文档 §6）。  
- **不**在本 backlog 内实现完整 Microsoft GraphRAG 产品化 pipeline（仅 POC）。  
- **不**改 `code_chunks` / Code Query 线。

---

## 3. 依赖与引用

| 依赖项 | 路径/说明 |
| --- | --- |
| 现状 RAG 流程 | `docs/_tech_graph/10_flow_rag.md` |
| 入库 | `api/ingest_pipeline.py`（512/50、1024d、`documents`） |
| 对照说明 | `docs/diary/jsonPKmermaid/Ink博客RAG_vs_GraphRAG_对照.md` |
| 表结构 | `docs/_tech_graph/01_struct.md` · `documents` |

---

## 4. 交付形态（小范围使用）

### 4.1 后端 dev / admin（优先）

- 新路由示例：`POST /api/py/admin/rag/graphrag-pilot/query`（名称实施时定，须 `admin_secret`）。  
- 响应含：`recall_mode`、`latency_ms`、`context_preview`、`sources`（与现有 `build_sources_payload` 对齐）。

### 4.2 可选：前端独立页（Ink）

- 路径建议：`/dev/graphrag-pilot` 或挂在现有 Chat Debug 区；**仅开发/内网**可见。  
- 能力：选 `recall_mode`、并排展示 Hybrid vs GraphRAG 回答与 sources。  
- **单独开** `ai-ink-brain/content/tasks/active/task_frontend_rag_graphrag_pilot_v1.md`（本单不阻塞）。

---

## 5. 验收标准（母单 · 试点签收）

- [ ] 试点语料 ingest + GraphRAG 索引可 **一键复现**（脚本 + README 片段）。  
- [ ] dev/admin 路由在鉴权下可跑通三种 `recall_mode`（至少 hybrid + 一种 graphrag）。  
- [ ] 报告含：离线 LLM 调用次数估算、P95 延迟、≥10 条黄金问句结果表。  
- [ ] 明确书面结论：**是否值得进入 active 实施**；若否，写明搁置理由。

---

## 6. Harness

| 字段 | 值 |
| --- | --- |
| `test_strategy` | `recommended`（试点须有可失败 pytest 或脚本断言，至少覆盖路由鉴权与空图降级） |
| `failure_paths` | 建图失败 → 降级 hybrid；GraphRAG 0 hit → 结构化错误码，不 silent 空答 |

---

## 7. 风险与假设

| 风险 | 缓解 |
| --- | --- |
| 抽实体噪声大 | 小语料 + 人工抽检；不扩大至全库 |
| ingest 成本暴涨 | 语料篇数上限；社区摘要可关 |
| 与 ChatBI 路由混淆 | 仅博客 `documents` 域；独立 API 前缀 |

**假设**：SiliconFlow（或现有 embed 供应商）可用于抽取阶段；试点预算可接受 **数倍于纯 embed** 的离线 LLM 调用。

---

## 给 Cursor

关键词：`GraphRAG`、`backlog`、`documents`、`hybrid`、`RRF`、`pilot`、`diary`、`非生产默认`
