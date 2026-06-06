# 代码库结构分析

## 生成来源
> **所属**：`artifacts/claude/` · 对比分析见 [`00_README.md`](../../00_README.md)


- **工具**: Claude Code CLI
- **模型模式**: kimi-for-coding
- **生成时间**: 2026-06-05
- **任务**: explore Agent — 代码库结构分析
- **Token 输入输出量**: 15.2k tokens（12 tool uses）

---

## AI-Ink-Brain API 代码库地图

### 顶层结构
| 文件/目录 | 说明 |
|-----------|------|
| `main.py` | 本地开发入口，转发自 `api/index.app` |
| `vercel.json` | Vercel 部署配置，生产入口指向 `api/index.py` |
| `requirements.txt` | 依赖：FastAPI、uvicorn、openai、anthropic、supabase、faiss-cpu 等 |
| `pytest.ini` | 测试配置 |
| `.env` / `.env.example` | 环境变量模板 |

### `api/` — 核心模块（~30 个文件）
| 文件 | 职责 |
|------|------|
| `index.py` | FastAPI 主应用：RAG 检索、管理端 `/admin/sync` `/admin/ingest`、流式对话 |
| `unified_chat.py` | 统一聊天后端（36k，核心） |
| `agent.py` | Agent 逻辑（50k） |
| `intent_router.py` / `intent_agent.py` / `intent_hints.py` | 意图识别与路由 |
| `chain_chat.py` | 链式对话编排 |
| `code_retrieval.py` / `code_ingest.py` / `code_parser.py` | 代码 RAG：解析、入库、检索 |
| `ingest_pipeline.py` | 文档同步流水线（Markdown 处理） |
| `text2sql_*.py`（5 个） | Text2SQL：API、核心、grounding、schema 预取、结果存储 |
| `chatbi_*.py`（12 个） | ChatBI 子系统：权限、熔断、限流、SQL 网关、Prompt Guard、审计日志 |
| `graph/` | 图状态机：`state.py`、`runner.py`（用于 unified_chat_graph） |
| `hybrid_fusion.py` | RRF 混合排序 |
| `keyword_fallback.py` | 关键词降级检索 |
| `rag_recall_tools.py` / `query_rewrite.py` | 查询改写与召回工具 |

### `tests/` — 测试结构（~35 个文件）
- 按功能命名：`test_unified_chat_*.py`、`test_intent_*.py`、`test_chatbi_*.py`、`test_code_*.py`、`test_tech_graph_*.py`
- `conftest.py` — pytest 共享配置

### `docs/` — 文档组织
- `chatbi/`、`text2sql/`、`tech_graph/`、`coding_wiki/`、`harness/`、`showcase/`、`spec/`、`tasks/`、`diary/`、`meta/` — 按子系统/主题分目录

### `supabase/` — 数据库
- `sql/` — 初始化与函数脚本：`init.sql`、`match_documents.sql`、`hybrid_search.sql`、`code_chunks.sql`

### `.github/workflows/` — CI/CD
- `pytest.yml` — 单元测试
- `tech-graph.yml` / `tech-graph-contract.yml` — Tech Graph 校验
- `pr-post-ci.yml` — PR 后处理
- `verify-fast.yml` — 快速验证

### `tools/` — 工程工具（~20 个脚本）
- Tech Graph 校验、导出、合约检查、token 估算、CI 辅助、Agent 生成等
