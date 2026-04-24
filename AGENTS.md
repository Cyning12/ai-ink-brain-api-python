# AI-Ink-Brain API（Python 后端）— Agent 导航

> **角色**：Ink-Brain 博客的 **RAG / Embedding / Chunking / Retrieval / ingest** 服务端（FastAPI）。  
> **边界**：页面渲染、Next.js BFF、博客内容编辑 UX **不在本仓**；本仓提供 HTTP API 与数据库写入能力。

---

## 必读（按顺序）

1. **`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`**：环境变量真值表、目录地图、对外契约、安全注意项
2. **`.cursorrules`**：RAG 工程约束（日志、Hybrid、Streaming 等）
3. **`docs/_tech_graph/`**：技术图谱（架构唯一可信来源）
   - `00_main.md` — 顶层流程总图
   - `01_struct.md` — 数据库 Struct 模型
   - `02_version.md` — 版本迭代时间线
   - `10_flow_rag.md` — RAG 检索流程
   - `11_flow_text2sql.md` — Text2SQL 流程
   - `12_flow_fts.md` — 全文检索流程
   - `13_flow_supabase_rpc.md` — Supabase RPC 流程
   - `99_spec.md` — 实现规约
4. **`docs/tasks/`**：任务规格（实现与验收口径）
5. **多子仓协作**（总设职责、任务单规范与落盘路径）见工作区根 `Projects/AGENTS.md` **§2**，跨仓任务按该约定先写任务初稿再分派子 Agent 丰富。
6. **日记/日志规则**（含截图占位、引用 ≤ 300 字、禁止本地路径）见工作区根 `DIARY_GUIDE.md`；后端"知识总结"素材写在 `docs/diary/`（按日期命名）。

---

## 关键入口文件（改代码从这里开始）

| 文件 | 职责 |
|------|------|
| `api/index.py` | `/api/py/chat`、`/api/py/chat/history`、admin ingest/sync |
| `api/ingest_pipeline.py` | Markdown 分块、Embedding、写入 `documents` |
| `api/rag_env.py` | `.env` 加载、Supabase/SiliconFlow 选择器 |
| `api/database_manager.py` | `rag_conversation_logs` 读写 |
| `api/unified_chat.py` | Unified Chat（RAG + Text2SQL events） |
| `api/rag_recall_tools.py` | RAG 召回工具（keyword + vector + metadata） |
| `supabase/sql/` | 数据库初始化与迁移脚本 |

---

## 技术栈

- **Framework**: FastAPI, Uvicorn
- **AI Stack**: SiliconFlow (DeepSeek/Claude), LangChain, PyDeepSearch
- **Database**: Supabase (PostgreSQL + pgvector)
- **Vector Search**: Cosine Distance (`match_documents`)
- **Hybrid**: Vector + FTS (Full-Text Search) + RRF 融合

---

## 交付物约定（给总 Agent / 子 Agent）

- **配置真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（随代码演进持续更新）
- **任务驱动**：优先阅读对应 `docs/tasks/*.md`，实现完成后回填验收项与涉及文件列表
- **图谱同步**：代码变更后自动增量更新 `docs/_tech_graph/` 对应文件

---

## 安全红线

- **不要**把 `.env` / `.env.local` / service role key / API key 提交进 Git。
- CI/生产注入请使用平台 Secrets（不要写进仓库明文）。
