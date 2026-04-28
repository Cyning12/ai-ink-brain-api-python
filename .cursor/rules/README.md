## 这是什么
这里是 `ai-ink-brain-api-python`（Python 后端）仓的 Cursor Project Rules，使用 `.mdc` 文件模块化维护。

## 如何生效
- 规则文件：本目录下 `*.mdc`
- 仓内导航入口：`ai-ink-brain-api-python/AGENTS.md`

## 文件分工（当前）
- `00-core.mdc`：核心行为约束（语言、职责边界、修改前确认、完成后报告）
- `01-agent-observability.mdc`：Agent 模式可观测性与成本控制（执行报告、Loop 防护、模式选择）
- `10-tech-graph.mdc`：后端 `_tech_graph/` 规范、协议与目录结构
- `20-tech-graph-update.mdc`：图谱增量更新规则
- `30-rag-implementation.mdc`：RAG 工程实现约束（Supabase、Hybrid、Streaming、可观测、错误处理等）
- `40-error-handling.mdc`：错误处理与降级策略（结构化响应、异常分支、备选方案）

## 维护约定
- 规则与实现必须一致：改代码后同步更新 `docs/_tech_graph/`。
