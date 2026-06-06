# 代码库升级计划

## 生成来源
> **所属**：`artifacts/claude/` · 对比分析见 [`00_README.md`](../../00_README.md)


- **工具**: Claude Code CLI
- **模型模式**: kimi-for-coding
- **生成时间**: 2026-06-05
- **任务**: plan Agent — 制定 AI-Ink-Brain API 升级计划
- **Token 输入输出量**: 30.3k tokens（37 tool uses）

---

## 升级计划（分五阶段）

### 阶段一：基础加固（P0，立即执行）
**目标**：消除单点风险，提升稳定性与可观测性基线。

- **依赖锁定**：将 `requirements.txt` 升级为 `pyproject.toml`，锁定 FastAPI、openai、supabase 等关键库版本；Python 3.11 保持不变（Vercel 运行时兼容）。
- **可观测性**：统一结构化日志（`chatbi_json_log.py` 已存在，推广至全模块）；接入 OpenTelemetry 追踪，覆盖 LLM/SiliconFlow 外呼、Supabase RPC、意图决策链路。
- **熔断与限流**：`chatbi_circuit_breaker.py` 和 `chatbi_rate_limit.py` 已具备基础，补充 Redis 后端实现分布式限流（当前为进程内内存版，多实例部署失效）。
- **预期收益**：故障定位时间缩短 60%，多实例限流一致。

### 阶段二：架构解耦（P1，2-3 周）
**目标**：拆分巨型模块，建立清晰分层。

- **路由拆分**：`api/index.py`（1163 行）承载 18 个端点，按领域拆分为 `routers/chat.py`、`routers/admin.py`、`routers/unified.py`。
- **服务层抽象**：`unified_chat.py`（3217 行）拆分为 `services/intent.py`、`services/rag.py`、`services/text2sql.py`、`services/agent.py`，解耦业务逻辑与 HTTP 传输。
- **数据模型**：引入 Pydantic v2 定义请求/响应模型（当前几乎无模型校验），替代裸 `dict[str, Any]`。
- **预期收益**：单文件复杂度下降 50%，新功能开发周期缩短。

### 阶段三：性能优化（P2，3-4 周）
**目标**：降低延迟，提升并发吞吐。

- **缓存层**：Embedding 结果、schema 预取、意图决策引入 `cachetools.TTLCache` 或 Redis；避免重复调用 SiliconFlow Embedding API。
- **数据库优化**：Supabase RPC `match_documents` 和 `keyword_documents` 增加查询计划审查；`rag_conversation_logs` 按 `session_id` + `created_at` 复合索引。
- **异步化**：`database_manager.py` 中 `asyncio.to_thread` 调用 Supabase 同步客户端，评估迁移至 `supabase-py` 异步分支或 `httpx.AsyncClient` 直连 PostgREST。
- **连接池**：SiliconFlow OpenAI 客户端启用 `http_client=httpx.Client(limits=...)` 连接池复用。
- **预期收益**：P95 延迟降低 30%，Embedding 成本降低。

### 阶段四：测试与质量（P3，持续）
**目标**：建立高置信发布流水线。

- **覆盖率**：当前 57 个测试文件覆盖较好，补充 `unified_chat.py` 和 `agent.py` 的单元测试（业务最复杂、测试最少）。
- **集成测试**：增加 SiliconFlow API 契约测试（mock 服务器验证请求/响应形状）。
- **CI 强化**：技术图谱 `graph.json` + Mermaid 双轨校验纳入 CI（已有工具链 `tech_graph_*`）；增加 `ruff`/`mypy` 严格模式。
- **预期收益**：回归缺陷减少，发布信心提升。

### 阶段五：开发者体验（P4，持续）
**目标**：降低认知负担，加速迭代。

- **API 文档**：启用 FastAPI 原生 OpenAPI，补充端点描述与示例。
- **本地开发**：`docker-compose.yml` 一键启动 Supabase 本地栈 + 服务；统一 `.env` 模板。
- **技术图谱自动化**：Mermaid 渲染与 `graph.json` 一致性检查由 CI 自动修复（当前为半手动）。
- **预期收益**：新成员 onboarding 时间从数天降至数小时。

---

## 关键文件（如需实施）

- `api/index.py`
- `api/unified_chat.py`
- `api/agent.py`
- `api/database_manager.py`
- `requirements.txt`
