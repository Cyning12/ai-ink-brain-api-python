# Harness explore · P2 只读差分报告

> Task: `gov-docs-noise-p2-readorder-v1` · 角色: explore 帽（只读） · 日期: 2026-06-06
> 禁止: 未改任何文件、未 spawn subagent、未做 git blame

---

## 结论速览

- P2-1：`PROJECT_CONFIG` §A L17 + §B 表第 2 行仍将 `.cursorrules` 描述为「兼容/历史参考/仍常保留」，与仓库现状（已无 `.cursorrules`）冲突，须按 SPEC C4 改为「已移除；真值仅 `.cursor/rules/*.mdc`」。
- P2-2：`AGENTS.md`「必读」7 步与 `docs/README.md` §1 前 5 条 **canonical 子集基本对齐**（PROJECT_CONFIG → `.mdc`/`meta` → `_tech_graph` → tasks → coding_wiki），但 **双向互链缺失**；`docs/README.md` 未显式链回 `AGENTS.md`，`AGENTS.md` 也未显式链到 `docs/README.md` §1。
- P2-3：根 `README.md` Endpoints 缺 `POST /api/py/unified/chat`、`POST /api/py/unified/chat/stream`、`GET /api/py/chat/history`；env 缺全部 `CHATBI_*` 关键项（如 `CHATBI_USE_AGENT`、`CHATBI_PROMPT_GUARD_MODE`）。
- P2-4：`docs/tasks/legacy/` 共 6 文件；其中 `task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` 的 v2 需求（版本号/分隔符/CamelCase alias）已在 `supabase/sql/hybrid_search.sql:24–130` 的 `public.rag_fts_alias_text()` 中完整实现，建议判 `done`。其余 5 份 legacy 任务内容均与已落地的代码/SQL 一致，建议全部 `git mv` 到 `done/` 并补状态字段，更新 `_views/done.md`。
- 变更范围确认：仅涉及 `docs/` 下 `meta/PROJECT_CONFIG`、`AGENTS.md`、`docs/README.md`、根 `README.md`、`tasks/legacy/*`、`tasks/_views/done.md`，符合 P2 范围。

---

## P2-1 现状 vs 期望：PROJECT_CONFIG §A/B `.cursorrules` 表述

### 现状（行号/片段）

文件：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

- §A L17:
  ```markdown
  | 本仓负责的边界（Single Source of Truth） | **Embedding / Chunking / Retrieval / Hybrid Search / RAG 日志** 的权威实现以本仓库代码为准；**Cursor 规则载体**以 `.cursor/rules/*.mdc` 为主，根目录 `.cursorrules` 为兼容/历史参考 |
  ```
- §B 表第 2 行（L28）:
  ```markdown
  | `.cursorrules` | 历史/兼容：全仓 AI 规则摘要（若与 `.mdc` 不一致，**以 `.mdc` + 本 `PROJECT_CONFIG` 为准**） | 可选（当前仓库内仍常保留） |
  ```

### 期望（SPEC §8.3 P2-1 / C4）

- §A L17 应改为：「`.cursorrules` **已移除**；真值仅 `.cursor/rules/*.mdc`」。
- §B 表第 2 行应改为：
  - 作用：「历史/兼容（**已不存在**）；若外部引用仍以 `.cursorrules` 为准，须迁移至 `.cursor/rules/*.mdc`」
  - 是否必须存在：「**已移除**」
- 保留 `.cursor/rules` 执行层摘要（RAG 日志、pgvector Cosine、session_id、Legacy/Unified 区分、Hybrid 融合）不变。

### Gap

- 当前文本让 Agent 误以为 `.cursorrules` 仍可作为 fallback 参考，与仓库实际缺失该文件矛盾，构成 C4 真冲突。

---

## P2-2 现状 vs 期望：AGENTS.md「必读」节 + docs/README.md §1 读序对齐

### 现状（行号/片段）

文件：`AGENTS.md`

- L8–17「必读（按顺序 · 地图）」：
  1. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
  2. `.cursor/rules/*.mdc`
  3. `docs/_tech_graph/`
  4. `docs/tasks/RECENT_TASK_SCHEDULE.md` → `active/task_*.md`
  5. `docs/harness/README.md`
  6. `docs/coding_wiki/index.md`
  7. 跨仓协作：`Projects/AGENTS.md` §2
- 未在「必读」节内显式互链 `docs/README.md` §1。

文件：`docs/README.md`

- §1 L11–20 当前读序：
  1. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
  2. `docs/_tech_graph/`
  3. `docs/tasks/_views/` → active/done
  4. `docs/flows/`（Legacy · 非 L0）
  5. `docs/UI/`
  6. `docs/text2sql/`
  7. `docs/harness/README.md`
  8. `docs/coding_wiki/index.md`
  9. `docs/diary/DIARY_GUIDE.md`
  10. PR/CI spec
- 未在 §1 显式互链 `AGENTS.md`。

### 期望（SPEC §8.3 P2-2 / §7 canonical 子集）

Canonical 子集（须在前 3–5 条对齐）：

1. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`
2. `docs/_tech_graph/`（`graph_query` 按需）
3. `docs/tasks/RECENT_TASK_SCHEDULE.md` → `active/task_*.md`（`docs/README.md` 写 `_views/` 入口语义等价）
4. 涉 ChatBI → `docs/spec/v3-agent/`
5. 关账回顾 → `docs/coding_wiki/`

附加要求：

- `AGENTS.md` 在「必读」节末或「非必读」节前增加显式互链：`docs/README.md` §1。
- `docs/README.md` §1 末或文首增加显式互链：`AGENTS.md`。
- `docs/README.md` 保留 UI/text2sql/diary/PR spec 等扩展条。

### Gap

- **双向互链缺失**：两文件均未指向对方，Agent 可能在 AGENTS 与 docs/README 之间反复横跳。
- `AGENTS.md` 第 2 条是 `.cursor/rules/*.mdc`，而 `docs/README.md` 未把 `.mdc` 列为独立入口（仅在 meta 中隐含）。此差异在 SPEC 中属于「角色区分」允许范围，但建议 docs/README 在 §1 前 3 条内补一句 `.cursor/rules/*.mdc` 指针，或在 meta 条中合并提及。
- `docs/README.md` 第 4 条 `docs/flows/` 已正确降级为 Legacy（P0 已修），无回退风险。

---

## P2-3 现状 vs 期望：根 README Endpoints / env 缺失项

### 现状（行号/片段）

文件：`README.md`

- L5–11 Endpoints：
  ```markdown
  - `POST /api/py/chat`
  - `GET /api/py/health`
  - `POST /api/py/admin/sync`
  - `GET /api/py/admin/sync?jobId=...`
  - `POST /api/py/admin/ingest`
  ```
- L13–25 Required Environment Variables：
  - 含 `SILICONFLOW_*`、`SUPABASE_*`、`SYNC_ADMIN_SECRET`、废弃 secret、RAG debug 项。
  - **不含**任何 `CHATBI_*` 变量。

### 期望（SPEC §8.3 P2-3）

- Endpoints 至少补充：
  - `POST /api/py/unified/chat`（JSON `events[]`）
  - `POST /api/py/unified/chat/stream`（SSE 事件链）
  - `GET /api/py/chat/history`
- 或统一改为：「完整端点与契约见 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §F」。
- env 至少补充关键 `CHATBI_*`：
  - `CHATBI_USE_AGENT`
  - `CHATBI_PROMPT_GUARD_MODE`
- 或统一改为 pointer：「完整环境变量见 PROJECT_CONFIG §C」。

### Gap

- 根 README 作为新人/外部开发者第一眼入口，仍只呈现 Legacy chat，未体现 Unified Chat 这一当前主路径。
- `CHATBI_*` 系列 env 在 PROJECT_CONFIG §C 中已有 20+ 条，根 README 完全缺失会导致部署/调试时遗漏关键开关。

---

## P2-4 现状 vs 期望：legacy 6 文件 + b2_v2 证据 + 判定建议

### 现状：legacy 目录清单

文件：`docs/tasks/legacy/`（共 6 个）

1. `'Task 04.md'` — 引用溯源显示与 UI 透明化（sources header + 流末尾分隔符）
2. `task_03_hybrid_search_implementation.md` — Hybrid Search（Vector + FTS + RRF）
3. `task_rag_b1_metadata_structured_recall_v1.md` — metadata `date_norm`
4. `task_rag_b2_fts_alias_backfill_v1.md` — FTS alias（日期）
5. `task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` — FTS alias v2（分隔符/版本号/标识符）
6. `task_rag_keyword_websearch_date_normalize_v1.md` — keyword `websearch_to_tsquery` + 日期归一化

### b2_v2 `rg rag_fts_alias supabase/` 证据

```text
supabase/sql/hybrid_search.sql:30:create or replace function public.rag_fts_alias_text(input_text text)
supabase/sql/hybrid_search.sql:141:    coalesce(new.content, '') || ' ' || coalesce(public.rag_fts_alias_text(new.content), '')
supabase/sql/hybrid_search.sql:157:set fts_tokens = to_tsvector('simple', coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), ''))
supabase/sql/hybrid_search.sql:214:    coalesce(d.content, '') || ' ' || coalesce(public.rag_fts_alias_text(d.content), '')
supabase/check/B2-v2-fts-alias-exec-and-verify.md:31:  coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), '')
supabase/check/B2-v1-fts-alias-date-exec-and-verify.md:18:- 新增函数：`public.rag_fts_alias_text(input_text text)`
```

进一步查看 `supabase/sql/hybrid_search.sql:24–130`：

- L24–29 注释明确标注「B2 v2：生成 alias 文本」，覆盖：
  - 日期（v1 已有）
  - 版本号：`v0.1.0` / `0.1.0` / `0-1-0` / `0_1_0`（L83–96）
  - 分隔符归一：`_ - . / \` 替换为空格（L98–111）
  - CamelCase 拆分（L113–127）
- 该函数已被触发器 `trg_documents_fts_tokens_update` 与 `keyword_documents` RPC 调用。

### 判定建议

| 文件 | 判定 | 动作 |
|------|------|------|
| `Task 04.md` | `done` | `git mv` → `done/`；补头部 `状态: done`；内容描述与当前 sources 实现一致 |
| `task_03_hybrid_search_implementation.md` | `done` | `git mv` → `done/`；补头部 `状态: done`；Hybrid Search 已落地于 `supabase/sql/hybrid_search.sql` + `api/index.py` |
| `task_rag_b1_metadata_structured_recall_v1.md` | `done` | `git mv` → `done/`；补头部 `状态: done`；`date_norm` 已在 ingest/unified 路径实现 |
| `task_rag_b2_fts_alias_backfill_v1.md` | `done` | `git mv` → `done/`；补头部 `状态: done`；v1 日期 alias 已合入 `rag_fts_alias_text` |
| `task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` | `done` | `git mv` → `done/`；补头部 `状态: done`；v2 全部需求已在 SQL 中实现（见上证据） |
| `task_rag_keyword_websearch_date_normalize_v1.md` | `done` | `git mv` → `done/`；补头部 `状态: done`；`keyword_documents` 使用 `websearch_to_tsquery` 且日期归一化已落地 |

- 6 份全部建议 `done`（无 archived），因为功能均已在代码/SQL 中实现。
- 须同步更新 `docs/tasks/_views/done.md`，在头部新增 6 条条目（或合并为一句「P2 消化 legacy 6 文件」索引）。
- 若 `legacy/` 清空，可在 `docs/tasks/README.md` 标注「legacy 已消化，新增任务直接落 `active/`」。

---

## 变更范围确认

根据以上差分，P2 执行时变更范围严格限于：

- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（P2-1）
- `AGENTS.md`（P2-2）
- `docs/README.md`（P2-2）
- `README.md`（P2-3）
- `docs/tasks/legacy/*`（6 文件 · P2-4 · `git mv` 或补状态）
- `docs/tasks/_views/done.md`（P2-4 · 索引更新）
- 可选：`docs/tasks/README.md`（legacy 清空标注）

未涉及 `api/`、`tests/`、`.github/workflows/`，符合 `test_strategy: not_applicable` 与 P2 非范围。

---

## 回报 Lead（≤10 行）

- **Status**: explore 完成；P2 四项交付均有明确现状/期望/证据。
- **Deliverables**: 已生成本差分报告；legacy 6 文件全部可判 done；b2_v2 SQL 实现证据充分。
- **Blockers**: 无；人工闸 HG-GOV-P2-EXEC 已 approved，可进 22/30 执行。
- **Judgment**: P2 属于纯 docs 指针修正，范围清晰、风险低；建议 30 帽按本报告逐项改后 40 自检，`git diff --stat` 确认仅 docs 目录即可 CLOSE。
