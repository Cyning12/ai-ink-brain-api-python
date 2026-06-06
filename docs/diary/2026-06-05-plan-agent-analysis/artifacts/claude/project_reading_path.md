# AI-Ink-Brain API 项目阅读完整路径

## 生成来源
> **所属**：`artifacts/claude/` · 对比分析见 [`00_README.md`](../../00_README.md)


- **工具**: Claude Code CLI
- **模型模式**: kimi-for-coding
- **生成时间**: 2026-06-05
- **任务**: 记录本项目的完整阅读路径与知识获取顺序

---

## 阅读路径总览

本项目采用**分层递进**的阅读策略，从全局配置到具体实现，从必读文档到按需参考。以下路径基于 `AGENTS.md` 的必读顺序与实际代码探索经验整理。

---

## 第一层：入口与导航（必读）

### 1. CLAUDE.md（项目级指令）
**路径**: `CLAUDE.md`

- 项目根目录的顶级指令文件
- 定义了 `@AGENTS.md` 引用，指引到 Agent 导航文档
- 包含基础约束和项目边界说明

### 2. AGENTS.md（Agent 导航地图）
**路径**: `AGENTS.md`

核心导航文档，规定了**必读顺序**和**改代码入口**：
- 必读文档列表（按优先级排序）
- 改代码入口文件表
- 技术栈说明
- 交付与关账流程
- 禁止项与安全红线
- `.cursor/rules/` 规则索引

---

## 第二层：配置与契约（必读）

### 3. PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
**路径**: `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

- 环境变量完整列表与说明
- 目录结构约定
- 接口契约定义
- 安全策略（密钥管理、日志规范）

### 4. Cursor 规则（.cursor/rules/*.mdc）
**路径**: `.cursor/rules/`

按主题分类的工程约束，共 12 个规则文件：

| 文件 | 主题 | 关键内容 |
|------|------|----------|
| `00-core.mdc` | Core | 语言、职责边界、修改前确认、完成后报告 |
| `01-agent-observability.mdc` | Agent Observability | 执行报告、Loop 防护、模式选择 |
| `05-harness-semi-auto.mdc` | Harness Semi Auto | 无人工闸阻塞时链式续跑 task |
| `06-harness-in-repo.mdc` | Harness In Repo | Harness 本仓真值，禁止查外部路径 |
| `07-git-workflow.mdc` | Git Workflow | 本地不在 main 改代码；远程合并须 PR |
| `08-docs-diary.mdc` | Docs Diary | diary 非必读、易过时产物落盘 |
| `09-pr-post-ci.mdc` | Pr Post Ci | PR 后 body 同步、automerge 白名单 |
| `10-tech-graph.mdc` | Tech Graph | Mermaid 维护轨 + graph.json 机器轨 |
| `11-coding-wiki-readorder.mdc` | Coding Wiki Readorder | L2 默认读序；改代码仍 L0 图谱优先 |
| `20-tech-graph-update.mdc` | Tech Graph Update | 图谱增量更新流程 |
| `30-rag-implementation.mdc` | Rag Implementation | RAG 实现规范 |
| `40-error-handling.mdc` | Error Handling | 结构化响应、异常分支、备选方案 |

---

## 第三层：架构与技术图谱（必读）

### 5. 技术图谱（_tech_graph/）
**路径**: `docs/_tech_graph/`

- 架构真值来源
- 使用 `python tools/tech_graph_graph_query.py` 查询（禁止默认整包读取 `graph.json`）
- 改拓扑后需导出 `graph.json` + manifest/contract CI

### 6. 任务调度（tasks/）
**路径**: `docs/tasks/RECENT_TASK_SCHEDULE.md` → `docs/tasks/active/task_*.md`

- 当前活跃任务列表
- 具体任务单的详细规格与验收标准

### 7. Harness 文档（harness/）
**路径**: `docs/harness/README.md`

- Harness 帽子链机制
- 落盘规范
- 半自动执行流程
- 细则分布在各子文档中，禁止默认 `glob` 遍历 `docs/harness/invokes/`

---

## 第四层：编码维基与回顾（按需）

### 8. Coding Wiki
**路径**: `docs/coding_wiki/index.md`

- 关账回顾 L2 内容
- **注意**: 改代码时仍以 L0 技术图谱优先，不要以 Wiki 替代架构文档

### 9. 实验与验收（按需）
**路径**: `docs/diary/`

- 验收留证、实验报告
- **默认不读**，仅当 task 或 `@` 指向时查阅
- `docs/diary/jsonPKmermaid/` 为图谱行为实验轨，非实验任务勿遍历

### 10. 规格文档（按需）
**路径**: `docs/spec/`

- SDD 规格（如 ChatBI 等子系统详细设计）

---

## 第五层：代码实现（改代码时必读）

### 核心入口文件

| 文件 | 职责 | 何时阅读 |
|------|------|----------|
| `api/index.py` | chat、history、admin ingest | 修改聊天/管理接口时 |
| `api/ingest_pipeline.py` | 分块、Embedding、documents | 修改文档处理流程时 |
| `api/unified_chat.py` | Unified Chat（RAG + Text2SQL SSE） | 修改统一聊天逻辑时 |
| `api/rag_recall_tools.py` | Hybrid 召回 | 修改召回策略时 |
| `supabase/sql/` | 库表与迁移 | 修改数据库结构时 |

### 子系统文件（按需）

- **意图识别**: `api/intent_router.py`, `api/intent_agent.py`, `api/intent_hints.py`
- **代码 RAG**: `api/code_retrieval.py`, `api/code_ingest.py`, `api/code_parser.py`
- **Text2SQL**: `api/text2sql_*.py`（5 个文件）
- **ChatBI**: `api/chatbi_*.py`（12 个文件）
- **图状态机**: `api/graph/state.py`, `api/graph/runner.py`

---

## 第六层：测试与工具（辅助）

### 测试目录
**路径**: `tests/`

- 按功能命名：`test_unified_chat_*.py`, `test_intent_*.py` 等
- `conftest.py` — pytest 共享配置

### 工具脚本
**路径**: `tools/`

- Tech Graph 校验、导出、合约检查
- Token 估算、CI 辅助、Agent 生成等

---

## 跨仓协作（如需）

**路径**: 工作区 `Projects/AGENTS.md` §2

- 前端/Next BFF/博客编辑 UX 不在本仓
- 跨仓协作时参考工作区 AGENTS.md

---

## 阅读策略建议

1. **首次接触**: 按 L1→L2→L3 顺序阅读，建立全局认知
2. **接任务时**: 先读 `docs/tasks/active/` 对应任务单，再读相关代码入口
3. **改代码前**: 确认已读对应 `.cursor/rules/*.mdc`，了解约束
4. **遇到报错**: 查 `40-error-handling.mdc` 和 `docs/_tech_graph/`
5. **提交前**: 确认符合 `07-git-workflow.mdc` 和 `09-pr-post-ci.mdc`

---

## 技术栈速查

- **框架**: FastAPI
- **数据库**: Supabase / pgvector
- **模型**: SiliconFlow（DeepSeek 系列）
- **检索**: Hybrid RRF
- **部署**: Vercel
