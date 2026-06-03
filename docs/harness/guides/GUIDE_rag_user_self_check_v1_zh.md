# 用户指南 · RAG 问答自查（v1）

| 项 | 内容 |
| --- | --- |
| **用途** | 演示站 / Portfolio 五问：**答非所问、sources 为空、把 Harness 讲成 Harness.io** 时，运维或验收人 **5～10 分钟** 自行定位根因 |
| **适用** | `POST /api/py/unified/chat`（ChatBI V2 Agent · `metadata.v = chatbi_v2_agent`） |
| **不在范围** | 改代码、自动 sync、密钥明文；sync 操作见 [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](./RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §2 |
| **env 真值** | [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) §C.1 |
| **本地排查落盘** | 可选：`$PORTFOLIO_RAG_EVIDENCE_DIR/sql/`（见 RUNBOOK 留证路径约定 · 默认 `tmp/portfolio-rag-demo/`） |

---

## 0. 本地落盘（可选）

SQL 结果、日志片段等 **本机排查产物** 默认写入（不纳入 Git）：

```bash
export REPO_ROOT="$(git rev-parse --show-toplevel)"
export PORTFOLIO_RAG_EVIDENCE_DIR="${PORTFOLIO_RAG_EVIDENCE_DIR:-$REPO_ROOT/tmp/portfolio-rag-demo}"
mkdir -p "$PORTFOLIO_RAG_EVIDENCE_DIR/sql"
```

| 文件（建议） | 内容 |
| --- | --- |
| `sql/category-distribution.json` | §3.1 ① 查询结果 |
| `sql/agent-log-latest.json` | §4 最近一条 `rag_conversation_logs` |

冻结验收留证仍按 RUNBOOK §6 复制至 `docs/diary/samples/portfolio-rag-demo/`。

---

## 1. 何时打开本文

| 现象 | 先怀疑 |
| --- | --- |
| 问「卷三 / Harness / 签收」，回答像 **DevOps 平台 Harness.io** | **语料未入库** 或 **检索零命中** 后模型瞎编 |
| UI 有回答但 **无 sources** / sources  category 不对 | 同上，或 Q3 误命中 `methodology`（见 RUNBOOK §4） |
| 刚改过 `content/` 文稿，问答仍像旧版 | **未 re-sync** |
| sync job 已成功，仍不对 | **连错 Supabase**、**FTS 未迁移**、或 **Embedding 不一致** |
| history 能拉会话，但 sync **401**（直连 Python） | `$ADMIN_TOKEN` 是 visitor token，或 **Python `.env` 无 `SYNC_ADMIN_SECRET`**（BFF 页面仍 202） | 走 RUNBOOK §2.1 路径 B，或对齐两端 `SYNC_ADMIN_SECRET` |

> **常见误判**：以为是「意图置信度太低」——V2 Agent 里 **`metadata.mode = no_data` 多半是 RAG 空命中后的 fallback**，与 intent confidence 无关。

---

## 2. 五分钟决策树

```text
问卷三类问题
    │
    ├─ Supabase：category=methodology 的 chunk 数 = 0？
    │       └─ 是 → 【根因 A】未 sync 或 CONTENT_ROOT 错 → RUNBOOK §2
    │
    ├─ methodology > 0，但 keyword_documents('Harness') = 0？
    │       └─ 是 → 【根因 B】fts_tokens 未回填 → 执行 hybrid_search.sql 后 re-sync
    │
    ├─ 库里有 vol3，仍 RAG_RETRIEVE_EMPTY？
    │       └─ 是 → 【根因 C】向量阈值 / Embedding 模型不一致 → §4.3
    │
    └─ rag_search 成功但答偏？
            └─ 【根因 D】问句与语料不对齐 → 查 sources category，见 RUNBOOK §4
```

---

## 3. Supabase SQL 自查套餐

在 **与线上一致的 Supabase 项目** → SQL Editor 执行（可逐条跑）。

### 3.1 语料是否在库（最先跑）

```sql
-- ① 全库 category 分布（portfolio 期望见 methodology / resume / evidence）
SELECT
  metadata->>'category' AS category,
  COUNT(*) AS chunks,
  COUNT(DISTINCT metadata->>'relativePath') AS files
FROM public.documents
GROUP BY 1
ORDER BY chunks DESC;
```

**读结果**：

| 结果 | 含义 |
| --- | --- |
| **无 `methodology` 行** | 根因 A：portfolio 语料 **从未灌入**（本地有 `content/` 文件 ≠ 库里有 chunk） |
| 三目录都有 chunk | 语料面 OK，继续 3.2 |

```sql
-- ② vol3 是否在库（Q1 硬依赖）
SELECT
  metadata->>'relativePath' AS path,
  COUNT(*) AS chunks,
  MAX(created_at) AS last_ingested
FROM public.documents
WHERE metadata->>'relativePath' ILIKE '%vol3%'
GROUP BY 1;
```

### 3.2 关键词路是否可用

```sql
-- ③ FTS 列是否为空（需先跑过 supabase/sql/hybrid_search.sql）
SELECT
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE fts_tokens IS NULL) AS missing_fts
FROM public.documents
WHERE metadata->>'category' = 'methodology';

-- ④ keyword RPC（应先能命中 Harness）
SELECT id, metadata->>'relativePath' AS path, score
FROM public.keyword_documents('Harness', 5);
```

| 结果 | 含义 |
| --- | --- |
| `total = 0` | 仍属根因 A |
| `missing_fts = total` 且 total > 0 | 根因 B：执行 `supabase/sql/hybrid_search.sql`，再 **admin/sync** |
| `Harness` 有分、`卷三` 无分 | 中文 FTS 弱属正常；向量路应兜底——若仍空命中见根因 C |

### 3.3 向量路（可选 · 需已有 embedding 时排查）

默认 **`RAG_MATCH_THRESHOLD=0.3`**（相似度须 **>** 0.3 才进向量 Top-K）。临时验证可在 **预发** 设 `RAG_MATCH_THRESHOLD=none` 后重问同一句；若立刻有 sources → 阈值过严或问句 embedding 与入库不一致。

---

## 4. 从对话日志确认（不用猜）

```sql
SELECT
  created_at,
  metadata->>'mode' AS final_mode,
  agent_steps,
  tool_results
FROM public.rag_conversation_logs
WHERE query ILIKE '%卷三%'
ORDER BY created_at DESC
LIMIT 3;
```

### 4.1 `metadata.mode` 含义

| `final_mode` | 通常含义 |
| --- | --- |
| `rag` | 最终由 **文档检索 + 生成** 作答 |
| `no_data` | 常为 **RAG 空命中 → direct_answer 兜底**（易幻觉） |

### 4.2 `tool_results` 典型失败链（2026-06-02 实测样例）

```json
{
  "results": [
    {
      "tool": "rag_search",
      "success": false,
      "error_code": "RAG_RETRIEVE_EMPTY",
      "error_stage": "rag.retrieve"
    },
    {
      "tool": "direct_answer",
      "success": true,
      "answer": "… Harness.io …"
    }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `RAG_RETRIEVE_EMPTY` | 向量 + keyword + 日期结构化 **融合后 hits = 0** |
| 随后 `direct_answer` 成功 | Agent **故意** 改用模型常识作答 → **不可当作 RAG 验收通过** |

### 4.3 根因 C 检查清单

- [ ] sync 与在线 **`SILICONFLOW_EMBEDDING_MODEL`** 一致  
- [ ] **`EMBEDDING_DIM`** 与 `documents.embedding vector(N)` 一致（默认 1024）  
- [ ] 预发 Python 与 sync job 使用 **同一 Supabase 项目**  
- [ ] 长问句 + 书名引号导致相似度 < 0.3 时，考虑调低阈值或优化问句（chip 文案）

---

## 5. 处置对照（怎么修）

| 根因 | 处置 | 验证 |
| --- | --- | --- |
| **A · 未灌库** | 设 `CONTENT_ROOT` → 前端 `ai-ink-brain/content/`；跑 RUNBOOK §2 **admin/sync** | ① 出现 `methodology` / `resume` / `evidence`；② vol3 `COUNT > 0` |
| **B · FTS 空** | Supabase 执行 `supabase/sql/hybrid_search.sql`；re-sync | ④ `keyword_documents('Harness')` 有行 |
| **C · 阈值 / 模型** | 对齐 Embedding env；必要时预发 `RAG_MATCH_THRESHOLD=none` 试跑 | 同问句 `rag_search.success = true` |
| **D · 答偏但有 sources** | 对照 RUNBOOK §4 期望 category；Q3 不得仅 `methodology` | 五问表 pass |

**本地 content 应对照路径**（sync 前 `find` 应各 ≥1 `.md`）：

```text
ai-ink-brain/content/methodology/vol3_*.md
ai-ink-brain/content/resume/*.md
ai-ink-brain/content/evidence/*.md
```

---

## 6. 与 RUNBOOK 分工

| 文档 | 负责 |
| --- | --- |
| **本文** | 问答异常 → **SQL + 日志** 快速定因 |
| [`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](./RUNBOOK_portfolio_rag_five_questions_v1_zh.md) | sync 命令、五问表、留证目录、人工闸 |
| [`PROJECT_CONFIG`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) §C.1 | env 变量真值 |

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-02 | 初版：portfolio Q1 空命中排障沉淀（methodology 未入库 + RAG_RETRIEVE_EMPTY 链） |
| v1.1 | 2026-06-03 | §0：本地排查落盘默认 `tmp/portfolio-rag-demo/` |
