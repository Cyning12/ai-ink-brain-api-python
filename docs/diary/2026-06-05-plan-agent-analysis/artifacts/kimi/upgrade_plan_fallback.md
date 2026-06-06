# AI-Ink-Brain API（Python 后端）升级计划

> **制定日期**：2026-06-05  
> **所属**：`artifacts/kimi/` · Claude 成功版见 [`../claude/upgrade_plan.md`](../claude/upgrade_plan.md)

> **基线版本**：当前 `main` 分支（P2 Loop 已关账，P0 OpenSpec×TDD 已收口）  
> **范围**：`ai-ink-brain-api-python` 全仓代码、测试、文档、CI/CD

---

## 1. 现状评估

### 1.1 架构成熟度

| 维度 | 状态 | 说明 |
|------|------|------|
| **核心服务** | 成熟 | FastAPI + Supabase/pgvector + SiliconFlow 已稳定运行 |
| **RAG 检索** | 成熟 | Hybrid（Vector + FTS + Date Anchor + RRF）已生产化 |
| **Text2SQL** | 成熟 | SQL 生成、AST Gate、Schema Prefetch、Value Hints 完整 |
| **ChatBI V2 Agent** | 成熟 | ReAct 循环、工具调用、SSE 流式、失败恢复已落地 |
| **ChatBI V3 韧性** | 基本成熟 | P2-1a/b/c（health/ready、限流、熔断）已关账 |
| **Graph 路径** | 骨架 | `unified_chat_graph.py` + `graph/runner.py` 为 P0 占位 |
| **Intent 系统** | 双轨并行 | V1 规则路由 + V2 LLM Agent；V2 为默认但 V1 兜底仍存 |
| **代码 RAG** | 可用 | FAISS-based code retrieval，但非主路径 |

### 1.2 技术债务

| 债务项 | 严重度 | 位置 |
|--------|--------|------|
| **Legacy `/api/py/chat` 与 Unified 并存** | 中 | `api/index.py` 含 1163 行 Legacy 流式逻辑 |
| **V1 Intent Router 未下线** | 中 | `api/intent_router.py` 与 `intent_agent.py` 双维护 |
| **Graph 路径仅 stub** | 中 | `graph/runner.py` 为 `run_graph_stub` |
| **多轮对话工程债** | 中高 | `task_chatbi_v3_debt_from_v2_multiturn_v1.md` 为 backlog |
| **低置信预览确认 §5.1** | 中 | 后端 done，但 RAG 全栈预览（§5-3）为 draft |
| **Chain Events 统一** | 中 | `task_ui_chain_events_backend.md` 为 pending |
| **依赖管理粗放** | 低 | `requirements.txt` 无版本锁定，无 `pyproject.toml` |
| **无类型检查** | 低 | 未配置 `mypy` 或 `pyright` |
| **无格式化/静态检查 CI** | 低 | `.ruff_cache` 存在但无 CI 集成 |

### 1.3 测试与质量

| 维度 | 状态 |
|------|------|
| pytest 覆盖率 | 62 个测试文件 + 2 个 benchmark，覆盖核心路径 |
| CI 门禁 | `pytest.yml` + `tech-graph.yml` + `tech-graph-contract.yml` 为 Required |
| 意图评测 | 60 条 intent_eval 可跑（需 `CHATBI_V2_INTENT_EVAL=true`） |
| 延迟基准 | intent_benchmark + agent_e2e_latency 脚本存在 |
| 缺失 | 无覆盖率报告、无 mutation test、无 load test |

---

## 2. 升级目标

### 2.1 总体目标

在保持现有服务稳定的前提下，完成 **V3 全功能闭环**、**架构现代化**、**工程体验提升** 三大主线。

### 2.2 关键成功指标

1. **Legacy 路由优雅下线** 或明确迁移时间表
2. **Graph 路径从 P0 骨架演进为可用实现**
3. **Intent 系统统一为 V2（LLM-based），V1 作为可配置降级**
4. **多轮对话工程债清零**
5. **依赖管理现代化**（锁定版本 + 可选 `pyproject.toml`）
6. **CI 增加静态检查**（ruff/mypy）
7. **所有 active task 进入 `done/`**

---

## 3. 升级阶段

### Phase 1：债务清偿与基础加固（2–3 周）

**目标**：清理技术债务，夯实工程基础。

| # | 任务 | 优先级 | 验收标准 |
|---|------|--------|----------|
| 1.1 | **多轮对话工程债** (`task_chatbi_v3_debt_from_v2_multiturn_v1`) | P2 | 母单拆解完成，子任务进入 active 并逐关账 |
| 1.2 | **低置信 RAG 全栈预览** (`task_chatbi_v3_lowconf_rag_preview_v1`) | P2 | draft → active → done，SSE/JSON 双路径支持 |
| 1.3 | **Intent 分类债务** (`task_chatbi_v3_intent_classification_debt_v1`) | P4 | V1 路由标记为 deprecated，V2 为唯一默认 |
| 1.4 | **依赖版本锁定** | 中 | `requirements.txt` 增加 `==` 版本号；评估 `pyproject.toml` |
| 1.5 | **CI 增加 ruff 检查** | 低 | `.github/workflows/lint.yml` 新增，不阻塞合并（先观察） |

### Phase 2：架构演进（3–4 周）

**目标**：Graph 路径落地，Legacy 路由迁移。

| # | 任务 | 优先级 | 验收标准 |
|---|------|--------|----------|
| 2.1 | **Graph 路径实现** | P3 | `graph/runner.py` 从 stub 替换为真实实现；`graph/state.py` 状态机完整 |
| 2.2 | **Chain Events 统一后端** (`task_ui_chain_events_backend`) | P3 | SSE 事件格式统一，与前端契约对齐 |
| 2.3 | **Legacy 路由迁移计划** | 中 | 制定 `/api/py/chat` → `/api/py/unified/chat/stream` 迁移 RUNBOOK |
| 2.4 | **V3 统筹索引** (`task_chatbi_v3_planning_after_resume_v1`) | P4 | 完成 V3 总规索引，明确 P3/P4 边界 |

### Phase 3：工程体验与可观测性（2–3 周）

**目标**：提升开发效率与运维可观测性。

| # | 任务 | 优先级 | 验收标准 |
|---|------|--------|----------|
| 3.1 | **类型检查引入** | 低 | 配置 `mypy`（或 `pyright`），先对 `api/` 核心模块检查 |
| 3.2 | **覆盖率报告** | 低 | CI 输出 pytest-cov 报告，设定基线（如 60%） |
| 3.3 | **结构化日志增强** | 中 | `CHATBI_JSON_LOG` 覆盖更多路径（agent 决策、RAG 召回细节） |
| 3.4 | **本地开发体验** | 低 | `docker-compose.yml`（可选）一键启动 Postgres + pgvector |

### Phase 4：前瞻探索（按需）

| # | 任务 | 说明 |
|---|------|------|
| 4.1 | **GraphRAG 探索** (`task_rag_graphrag_pilot_explore_v1`) | 按需启动，不阻塞主路径 |
| 4.2 | **Intent vNext** | 多标签意图、置信度校准、A/B 框架 |
| 4.3 | **模型供应商解耦** | 抽象 LLM client，支持多供应商切换 |

---

## 4. 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| Legacy 下线导致前端兼容问题 | 中 | 高 | 保留 Legacy 为只读至少 1 个迭代；与前端仓同步契约 |
| Graph 路径重构引入回归 | 中 | 高 | 新增 `test_chatbi_graph_*` 单元测试；渐进式替换 |
| 依赖版本锁定后 CI 失败 | 低 | 中 | 先在 `task/` 分支验证，再合入 `main` |
| V2 Intent 独占后准确率下降 | 低 | 高 | 保留 V1 为 `CHATBI_V2_INTENT_LLM=false` 降级开关 |
| 多轮对话重构波及 SSE 契约 | 中 | 高 | 严格按 SPEC 变更；契约 CI (`tech-graph-contract.yml`) 必绿 |

---

## 5. 近期执行建议（下一棒）

根据 `RECENT_TASK_SCHEDULE.md` §4.2 **纯后端线**，建议按以下顺序执行：

```
① 低置信 §5.1 / P2-2 评估 → 拆单并进入 Phase 1.1/1.2
② P2 Loop 后续（如 P2-2 烟测集）
③ task_ui_chain_events_backend 现网对照后再动
④ 按需 legacy/ 治理
```

**当前最高优先**：将 `task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`（backlog）与 `task_chatbi_v3_lowconf_rag_preview_v1.md`（draft）推进为 active 并进入 Harness 关账链。

---

## 6. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-05 | 初稿：基于 explore Agent 代码库分析 + 项目文档读取制定 |
