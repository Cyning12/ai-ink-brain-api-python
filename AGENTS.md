# AI-Ink-Brain API（Python 后端）— Agent 导航

> **角色**：RAG / Embedding / Chunking / Retrieval / ingest（FastAPI）。  
> **边界**：页面、Next BFF、博客编辑 UX **不在本仓**。

---

## 必读（按顺序 · 地图）

1. [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) — 环境变量、目录、契约、安全
2. **`.cursor/rules/*.mdc`** — 工程约束（Cursor 自动注入；非 Cursor 见文末规则索引）
3. [`docs/_tech_graph/`](docs/_tech_graph/) — 架构真值；改拓扑用 `python tools/tech_graph_graph_query.py`（**禁止**默认整包 `graph.json`）
4. [`docs/tasks/RECENT_TASK_SCHEDULE.md`](docs/tasks/RECENT_TASK_SCHEDULE.md) → 具体 `active/task_*.md`
5. [`docs/harness/README.md`](docs/harness/README.md) — Harness 帽子链、落盘、半自动（细则 **不** 堆本文）
6. [`docs/coding_wiki/index.md`](docs/coding_wiki/index.md) — 关账回顾 L2；**改代码仍 L0 图谱优先**
7. 跨仓协作：工作区 [`Projects/AGENTS.md`](../../Projects/AGENTS.md) **§2**

> **docs 分类导航**（含 UI / text2sql / diary 等扩展条）见 [`docs/README.md`](docs/README.md) **§1**。

---

## 非必读（按需）

| 路径 | 说明 |
|------|------|
| `docs/diary/` | 验收留证、实验报告；**默认不读**，仅 task / `@` 指向 |
| `docs/diary/jsonPKmermaid/` | 图谱行为实验轨；非实验任务勿遍历 |
| `docs/spec/` | SDD 规格（ChatBI 等） |

---

## 改代码入口

| 文件 | 职责 |
|------|------|
| `api/index.py` | chat、history、admin ingest |
| `api/ingest_pipeline.py` | 分块、Embedding、`documents` |
| `api/unified_chat.py` | Unified Chat（RAG + Text2SQL SSE） |
| `api/rag_recall_tools.py` | Hybrid 召回 |
| `supabase/sql/` | 库表与迁移 |

**技术栈**：FastAPI · Supabase/pgvector · SiliconFlow · Hybrid RRF。

---

## 交付与关账

- 任务驱动：先读 `docs/tasks/active/` 对应单；验收后 `git mv` → `done/` + 更新 `_views/done.md`（见 [`docs/tasks/README.md`](docs/tasks/README.md)）
- 图谱：改 `.ai.md` → 导出 `graph.json` + manifest/contract CI（见 `docs/_tech_graph/99_mermaid_protocol.md`）
- **合并前必绿（本地与 CI 同命令）**：
  - **图谱 / manifest**：`bash scripts/verify-tech-graph.sh`（对齐 `tech-graph.yml` · `manifest_check`）
  - **契约**：`python tools/tech_graph_contract_check.py`（对齐 `tech-graph-contract.yml`）
  - **一键 PR 前**：`bash scripts/verify-pr-local.sh`（上述 + pytest）
  - **pytest 单跑**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 禁止项（摘要）

- 不要提交 `.env` / service role / API key
- 不要在 **`main`** 上日常 commit（用 `task/<slug>` + PR）
- 不要用 diary / Wiki **替代** `_tech_graph` / `PROJECT_CONFIG`
- 不要默认 `glob` 整个 `docs/harness/invokes/`
- 涉 `api/`/契约且 `test_strategy: required` → **50** 落盘后再关账

---

## 安全红线

- 密钥仅平台 Secrets；RAG 日志写 `rag_conversation_logs`；结构化错误响应（见 `40-error-handling.mdc`）

---

<!-- RULES_AUTO_GENERATED -->

## 规则索引（`.cursor/rules/`）

> Cursor 自动注入；非 Cursor 按需打开下表文件。**禁止**假定 AGENTS 含全文。

| 文件 | 主题 | 说明 |
| --- | --- | --- |
| `00-core.mdc` | Core | 核心行为约束 — 语言、职责边界、修改前确认、完成后报告 |
| `01-agent-observability.mdc` | Agent Observability | Agent 模式可观测性与成本控制 — 执行报告、Loop 防护、模式选择 |
| `05-harness-semi-auto.mdc` | Harness Semi Auto | Harness 半自动 — 无人工闸阻塞时链式续跑 task，invoke 落盘优先 |
| `06-harness-in-repo.mdc` | Harness In Repo | Harness 本仓真值 — prompts/模板/规划入口，禁止默认查工作区外部路径 |
| `07-git-workflow.mdc` | Git Workflow | Git 分支与 PR — 本地不在 main 上改代码/提交；远程合并须 PR |
| `08-docs-diary.mdc` | Docs Diary | docs/diary — 非必读、易过时产物落盘；实验轨 jsonPKmermaid 按需读 |
| `09-pr-post-ci.mdc` | Pr Post Ci | PR 后 CI — body 同步、automerge 白名单、禁止未绿 merge |
| `10-tech-graph.mdc` | Tech Graph | 技术图谱 — Mermaid 维护轨 + graph.json 机器轨（双轨，低幻觉） |
| `11-coding-wiki-readorder.mdc` | Coding Wiki Readorder | Coding Wiki L2 默认读序 — 关账回顾先 index/syntheses；改代码仍 L0 图谱优先 |
| `20-tech-graph-update.mdc` | Tech Graph Update | 图谱增量更新 — 改 .ai.md 后导出 graph.json 与 manifest/contract |
| `30-rag-implementation.mdc` | Rag Implementation | — |
| `40-error-handling.mdc` | Error Handling | 错误处理与降级策略 — 结构化响应、异常分支、备选方案 |

全文附录：`python tools/gen_agents_md.py --full`
