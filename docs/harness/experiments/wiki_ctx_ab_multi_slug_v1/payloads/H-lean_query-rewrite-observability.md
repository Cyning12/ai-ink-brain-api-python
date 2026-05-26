# Payload · H-lean（Multi 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `query-rewrite-observability` |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **generated** | 2026-05-26 · semi_auto 30 帽 |

## Agent 约束

只能依据下文作答。禁止 invoke/review 全文。禁止 `docs/coding_wiki/*`。

---

## 载荷正文

--- FILE: docs/harness/README.md ---
## 1. 日常读什么

| 场景 | 路径 |
|------|------|
| 写 task / **下一棒双 Prompt** | `TEMPLATE-requirements`（**A:22** + **B:30**，人择一） |
| 任务审核 22 | [`reviews/README.md`](reviews/README.md) → `TEMPLATE-task-audit` |
| 执行 + 自检 | `TEMPLATE-execute` → `TEMPLATE-self-check` |
| **三方复检** | `TEMPLATE-independent-reinspect` → [`../tasks/reinspect_results/`](../tasks/reinspect_results/README.md) |
| 半自动 / 人工闸 | `HANDOFF_SEMI_AUTO` |
| commit / 关账 | `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE` |
| task 字段 | `HARNESS_V2_PLAN.md` §5 |
| 流程 | `SDD_HAT_FLOW.md` |
| 新 invoke | `invokes/` |
| **Harness 裁决共识（已接受）** | [`../diary/2026-05-22-harness-evaluation-improvement-response.md`](../diary/2026-05-22-harness-evaluation-improvement-response.md) **§九** |

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc`、`.cursor/rules/06-harness-in-repo.mdc`。

**Agent 禁止（日常）**：

- **禁止** 默认读取工作区 `Projects/docs/harness/`（跨子仓 Harness 任务除外，见 `docs/tasks/README.md`）。
- **禁止** 将子仓 `prompts/` 软链到工作区；真值以 **本仓** `docs/harness/prompts/` 为准。
- **禁止** 在任务执行中运行下文 **§4 `rsync`**（仅维护者偶发同步）。

---

## 2. 目录结构

```text
docs/harness/
  README.md
  ACCEPTANCE_LANDING.md
  HARNESS_V2_PLAN.md
  SDD_HAT_FLOW.md
  prompts/
    hats/                   # 10～50 帽正文
    templates/              # TEMPLATE-*-invoke
    handoff/                # HANDOFF_*
    README.md
  invokes/by-task/<slug>/   # §2.1
  reviews/by-task/<slug>/   # §2.1
```

### 2.1 落盘 taxonomy（**已迁移** · 2026-05-25）

**原则**：**按 task 绑定**落盘（`invokes` / `reviews` / `reinspect_results` 已按 task 语义）；**不按业务域分顶层目录**。域知识进 **LLM Wiki**（`task_coding_wiki_pilot_v1`），不进 `prompts/domains/`。

| 树 | 目标路径 | 内容 |
|----|----------|------|
| **prompts** | `prompts/hats/` | `10-requirements` … `50-independent-reinspect` |
| | `prompts/templates/` | `TEMPLATE-*-invoke.md` |
| | `prompts/handoff/` | `HANDOFF_*.md` |
| **invokes** | `invokes/by-task/<task_slug>/` | `invoke_YYYYMMDD_<帽号>_<slug>.md`（见 [`invokes/README.md`](invokes/README.md)） |
| **reviews** | `reviews/by-task/<task_slug>/` | `task_<slug>_audit_R<轮次>_YYYYMMDD.md`（见 [`reviews/README.md`](reviews/README.md)） |
| **50（不变）** | `docs/tasks/reinspect_results/` | 关账复检；文件名可含 task slug |

**为何不建 `prompts/domains/chatbi` 或 `domains/tech-graph`？**

- Harness 文件描述的是**帽序与 HANDOFF 协议**，与「ChatBI / 图谱」等业务域 **正交**；同一 task 常跨多域。
- 按域拆目录会导致：同一 `invoke` 难归类、Agent 误把域片段当关账真值。
- **若将来**需要跨 task 复用的 Prompt **片段**，再用 `prompts/snippets/<domain>/`（可选），与 Wiki 词条分工，**仍不**替代 `by-task/` 落盘。

**新落盘**：invoke / review **必须**进 `by-task/<task_slug>/`；prompts 从 `hats/`、`templates/`、`handoff/` 读取（勿在 `prompts/` 根新增帽文件）。

**落地 task**：[`docs/tasks/active/task_coding_wiki_pilot_v1.md`](../tasks/active/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../tasks/active/task_wiki_ctx_ab_v1.md)（Wiki-CTX-AB）。

**实验（P1 题集 / payload 模板）**：[`experiments/wiki_ctx_ab_v1/`](experiments/wiki_ctx_ab_v1/README.md) · SPEC [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)。

--- FILE: docs/harness/invokes/README.md ---
# docs/harness/invokes（新快照落盘）

> **用途**：本仓 `docs/tasks/` 任务在 **每顶帽子新开局** 时，将已替换占位符的 `TEMPLATE-*` **§3 全文** 存一份于此。  
> **历史快照**（2026-05 图谱/闸口等 ~50 份）已迁至 [`../../diary/harness-archive/invokes/`](../../diary/harness-archive/invokes/)，**非必读**。

---

## 命名

`invoke_YYYYMMDD_<帽号>_<slug>.md`（例：`invoke_20260525_30_chatbi-v3-p2-1a-health.md`）

## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。

## 规则（摘要）

1. **同一帽**多轮追问 **不** 重复落盘；换帽才新建文件。  
2. 与 task 同 **`git_branch`** 提交；并行任务用独立 worktree（见 [`../README.md`](../README.md) §3）。  
3. 审查结论：用 **`docs/tasks/review_results/`**（20 帽）或 task 正文，**不**使用已移除的 `harness/reviews/`。

## 模板来源

[`../prompts/README.md`](../prompts/README.md)


--- FILE: docs/tasks/done/task_05_query_rewrite_observability.md ---
# Task：Rewrite 可观测性（raw vs rewrite 召回对比 + 关键实体丢失）

> **状态**：done（2026-05-22 验收通过 · [PR #46](https://github.com/Cyning12/ai-ink-brain-api-python/pull/46)）  
> **关联图谱**：`docs/_tech_graph/10_flow_rag.md`  
> **关联 Issue/PR**：[#46](https://github.com/Cyning12/ai-ink-brain-api-python/pull/46)  
> **前端依赖**：无（仅 metadata / DEBUG_RAG；前端展示另任务）

> 归档：`docs/tasks/done/` · Harness 试点见 [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §0.3

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `recommended` |
| **test_strategy_note** | — |
| **freeze_id** | `task_05_query_rewrite_obs@2026-05-22` |
| **gates_before_code** | `failure_paths`, 验收命令, 必读路径 |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/query-rewrite-obs` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 试点 task 已按模板补齐 |
| HG-AUDIT-R1 | approved | 30 | R1 落盘后 **人** 改 approved（见 `reviews/by-task/05_query_rewrite_observability/task_05_*_audit_R1_*.md`） |
| HG-REINSPECT | approved | done | 50 落盘后人签 |

---

## 背景与目标

排查「rewrite 导致检索变差 / 丢失关键 token（如 task_04、文件名、日期）」时，不宜频繁查 Supabase 或翻 `rag_conversation_logs` 全文。

**完成态**：

- 每次 `POST /api/py/chat` 在 `rag_conversation_logs.metadata.match.query_compare` 写入 raw vs rewrite 对比指标；
- `DEBUG_RAG=1` 时终端一行 `query_compare` 摘要。

> 不改变对外 API 契约；双查询并行融合另起任务。

---

## 范围

- [x] `POST /api/py/chat`：`metadata.match.query_compare` 字段（实现见 `api/index.py`）
- [x] Keyword 路 raw/rewrite 各跑一次计数（仅观测，不改变融合策略）
- [x] `compare_anchor_tokens` 关键实体丢失判定（`api/keyword_fallback.py`）
- [x] `DEBUG_RAG=1` 日志摘要
- [x] 单测：`tests/test_query_rewrite_compare_anchor.py`

## 非范围

- 不修改 Supabase SQL
- 不改变 RRF 融合主策略
- 不新增前端 UI

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| API | `POST /api/py/chat` · `api/index.py` |
| 表 | `public.rag_conversation_logs` · `docs/_tech_graph/01_struct.md` |
| 图谱 | `docs/_tech_graph/10_flow_rag.md` |
| 锚点规则 | `api/keyword_fallback.py` · `ANCHOR_TOKEN_PATTERNS` |

---

## 设计（`metadata.match.query_compare`）

| 字段 | 含义 |
|------|------|
| `query_raw` / `query_rewrite` | 原始与改写问句 |
| `recall_raw_count` / `recall_rw_count` | Keyword/FTS 路命中数 |
| `recall_raw_top1_score` / `recall_rw_top1_score` | Keyword Top1 `score`（`score_type: fts_score`） |
| `is_key_entity_lost` | raw 锚点 token 是否在 rewrite 中缺失 |
| `key_entities` | `tokens_raw` / `tokens_rewrite` / `missing` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | Supabase 不可用 | 检索失败；日志可能无 `query_compare` | 是 | 流式仍可能降级；500 类 |
| F2 | Embedding 失败 | keyword-only；`query_compare` 仍写入 | 是 | 无向量路 |
| F3 | rewrite 失败 | `rewritten_query=query`；对比仍有效 | — | 无单独错误码 |

---

## 验收标准

- [x] `metadata.match.query_compare` 含约定字段（`build_rag_match_meta` / `index.py`）
- [x] 含 `task_04` / 文件名 / 日期 时，rewrite 丢 token → `is_key_entity_lost=true` 且 `missing` 含对应 token（单测覆盖）
- [x] `DEBUG_RAG=1` 输出 `query_compare` 一行摘要
- [x] 不影响流式输出与 sources

**测试命令**：`pytest tests/test_query_rewrite_compare_anchor.py -q`

---

## 实现备忘

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/index.py`, `api/keyword_fallback.py`, `api/rag_logging.py`, `tests/test_query_rewrite_compare_anchor.py` |
| 关键 env | `DEBUG_RAG=1` |
| 图谱变更点 | 无（行为已在 `10_flow_rag` 隐含，可选增量） |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| 结论 | **pass** |
| 要点 | 208 passed，1 skipped（2026-05-22 本地 `.venv`）；含 `test_query_rewrite_compare_anchor.py` 4 条 |

---

## 给 Cursor

`task_05`、`query_compare`、`rewrite`、`DEBUG_RAG`、`compare_anchor_tokens`、`Harness P0-B/C`

--- FILE: docs/tasks/RECENT_TASK_SCHEDULE.md ---
| 0.3     | ~~建分支 `task/harness-improve-p0-20260522~~`                  | **取消**   | 沿用 `task/query-rewrite-obs` 承接 P0-B/C                                                         |
### 0.3 阶段 P0-B/C — 验收闭环（历史 · 曾用于首开验证）
| ~~B1~~    | ~~选定首开验证 task~~       | `task_05_query_rewrite_observability`                              | **done** |
| ~~B2~~    | ~~任务分支~~              | `task/query-rewrite-obs`                                           | **done** |
| ~~C1~~    | ~~**22 R1** 新落盘~~     | `reviews/by-task/05_query_rewrite_observability/task_05_query_rewrite_observability_audit_R1_20260522.md` | **done** |
> **关账**：`docs/tasks/done/task_05_query_rewrite_observability.md`（2026-05-22）
| `task_rag_b1_metadata_structured_recall_v1.md`             | 同上              |
| 2026-05-22 | **P0-A1～A4 done**；**P0-B/C** 以 `task_05` 试点                                                       |

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 8796 |
| `file_count` | 4 |
| `notes` | H-lean：README §1+§2.1 + invokes README 摘录 + done task 全文 + 排期关键词行 |
