# 编码规范 L2 — Ink 后端（Python / FastAPI · v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` — R1 三方验收签收（2026-06-09 · 人签 HG-L2-ACTIVE） |
| **版本** | v1.1 |
| **日期** | 2026-06-09 |
| **栈** | Python **3.11** · FastAPI · Uvicorn · pytest · Supabase/pgvector |
| **L1** | 工作区 [`docs/standards/CODING_BASELINE_L1_v1_zh.md`](../../../docs/standards/CODING_BASELINE_L1_v1_zh.md) |
| **配置真值** | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| **图谱** | [`docs/_tech_graph/`](../_tech_graph/) |

---

## 1. 适用范围

| 路径 | 职责 |
| --- | --- |
| `api/` | FastAPI 路由注册、RAG、ingest、Unified Chat、Text2SQL、Agent |
| `api/index.py` | 应用入口、路由挂载、Legacy chat、admin sync/ingest |
| `api/rag_env.py` | 环境变量、Supabase/SiliconFlow 客户端、重试与熔断封装 |
| `api/unified_chat.py` | Unified JSON / SSE、Intent 编排、事件契约 |
| `api/ingest_pipeline.py` | Markdown 分块、Embedding、`documents` 写入 |
| `tests/` | pytest 单元与集成（含 Harness structured error shape） |
| `tools/` | 图谱导出、契约检查、运维脚本（非业务路由） |

**不适用范围**：`node_modules/`、`.venv/`、`docs/diary/` 归档（见 `AGENTS.md` Docs Diary）、纯文档 task 且无 `api/` 变更。

---

## 2. 条文（P-01～P-15）

### P-01 模块边界（遵循 B-01）

| 规则 | 说明 |
| --- | --- |
| 路由层 | **薄**：`api/index.py` 负责注册、鉴权依赖、调领域模块、返回 `JSONResponse` / `StreamingResponse`；**禁止**在单路由函数内堆 >80 行业务 |
| 领域模块 | RAG / ingest / Unified / Text2SQL 各自在 `api/*.py`；跨域编排优先 `unified_chat.py` + `agent.py`，禁止 `index.py` 承担 ChatBI 全链路 |
| ingest | 分块与向量写入在 `ingest_pipeline.py`；admin 路由只触发 job |

软上限：**函数** ~60 行、**文件** ~400 行触发审查（与 L1 B-01 一致）。**路由 handler** 因须串联鉴权、解析、调用子模块与响应组装，**单函数软上限放宽至 ~80 行**；超过仍须拆子模块或私有 helper（同文件内 ≤60 行/函数）。

### P-02 早返回与异常（遵循 B-02）

- 路由入口：鉴权失败、缺 env、非法 body **先** `raise HTTPException` / 返回结构化 JSON，再写主路径。
- 业务模块：校验前置；**禁止** 三层以上嵌套 `try` 套 `try`；窄捕获具体异常（如 `CircuitBreakerOpenError`），禁止裸 `except Exception: pass`。
- Unified / Agent：短路分支（如 prompt guard `block`、低置信澄清）用早 return / emit error event，避免 elongate if-else 包裹主链。

### P-03 环境变量（遵循 B-03）

| 类型 | 规则 |
| --- | --- |
| 单一真值 | **所有** env 读取经 `api/rag_env.py` 或该模块 re-export 的 helper；**禁止** 业务模块散落 `os.getenv("SILICONFLOW_*")`（历史 `index.py` 顶层常量逐步收敛，新代码不得新增散落读取） |
| Supabase | `pick_supabase_url()` / `pick_supabase_service_key()`；禁止硬编码 Project URL |
| SiliconFlow | `must_siliconflow_api_key()`、`siliconflow_base()`、`siliconflow_embedding_model()` |
| Admin 鉴权 | `admin_secret()` → `SYNC_ADMIN_SECRET`；**禁止** 新代码依赖 `CHAT_API_SECRET` / `NEXT_PUBLIC_ADMIN_SECRET` |
| ChatBI 开关 | Intent、SSE、限流、熔断、Text2SQL 等见 `PROJECT_CONFIG` §C；禁止 magic 默认写死在业务逻辑 |

`.env.local` / `.env` 由 `rag_env` import 时加载（`override=False`）；文档化变量名以 `PROJECT_CONFIG` 为准。

CI / pytest 中的 `NEXT_PUBLIC_ADMIN_SECRET` 等 dummy 值仅用于兼容 `admin_secret()` 旧回退路径（见 `pytest.yml`）；**新代码不得新增**对上述废弃变量的读取。

### P-04 命名与导入（遵循 B-04）

- 模块：`snake_case` 文件名；公开函数/变量 `snake_case`；类型别名与 dataclass `PascalCase`。
- 常量：模块级 `UPPER_SNAKE`；错误码字符串与 registry / `_manifest` 一致（如 `RAG_EMBEDDING_MODEL_MISMATCH`）。
- 导入：标准库 → 第三方 → 本包相对导入（`.rag_env`）；禁止循环 import 绕过（抽 `rag_shared.py` 等）。
- 术语：与 `_tech_graph`、`docs/spec/` ChatBI 事件名、Tool 名对齐（`rag_search`、`text2sql_query` 等）。

### P-05 结构化错误（遵循 B-05）

| 场景 | 形状 |
| --- | --- |
| HTTP 路由 | `HTTPException(status_code=..., detail={...})` 或 `JSONResponse`；detail 含可枚举 `error_code`（或顶层 `error_code` 字段） |
| Unified JSON | `events[]` 内 `error` 事件；字段对齐 `docs/spec/v2-agent/` 与 `_contract_manifest.json` |
| Unified SSE | `chain` 内 error + `done.ok=false`；与 BFF 转发契约一致 |
| Tool / Agent | `ToolResult`：`success`、`error_code`、`error_stage`（见 `SPEC-ChatBI-V2-Tool-Design.md`）；**禁止** Agent 仅解析 `error` 字符串 |
| Harness 注册表 | 限流 / 熔断等路径须满足 [`docs/harness/linters/structured_error_registry_v1.json`](../harness/linters/structured_error_registry_v1.json) 必填键 `ok`、`error_code`、`message` |

**禁止** 向客户端返回 Python traceback；**禁止** 仅 `print` 而不返回结构化失败。

### P-06 策略表与注册表（遵循 B-06）

- Intent / Tool 路由：扩展 `tool_mode_map`、`get_tool_registry()`、`_fallback_tool_by_low_confidence` 等 **表驱动** 结构，禁止在 `agent.py` 复制第 N 份 if-elif。
- ChatBI 策略：`chatbi_policies.py`、`intent_hints.yaml`；新站点/表策略加配置或常量表。
- 限流 / 熔断 / embedding guard：行为由 env 枚举（`block`/`warn`/`off`）+ 单一判定函数，禁止散落字符串比较。

### P-07 最小 diff（遵循 B-07）

- 禁止全仓 `black`/`ruff format` 式无 task 授权重格式化；禁止升级无关 `requirements.txt` 依赖。
- 改 `api/index.py` 路由时对照邻域 handler 与既有 `Depends` / 鉴权模式。
- 图谱 / manifest 变更须与代码同 PR 或 follow-up task 明示。

### P-08 类型注解与边界（遵循 B-08）

| 规则 | 落地 |
| --- | --- |
| 新公开函数 | 参数与返回值须有类型注解；复杂结构用 `@dataclass(frozen=True)` 或 `TypedDict` |
| Literal / Enum | 有限枚举用 `Literal["block", "warn", "off"]` 等（见 `rag_embedding_guard.py`） |
| 禁止裸 dict 对外 | 路由响应、Tool 结果、日志 payload 须具名结构或 documented dict keys |
| `Any` | 新代码 **禁止** 无说明的 `Any`；Supabase 等边界保留须 `# noqa` 并附一行理由（对齐 L1 B-08） |
| Pydantic | 新 Route body/query 模型优先 Pydantic `BaseModel`（与 FastAPI 原生集成） |

**Ruff / 类型检查（P4 · 待升严）**：计划 `ruff.toml` 启用 `E`、`F`、`I`、`UP`、`B` 及 `ANN` 子集；当前 CI 以 pytest 为主，新 PR 仍须人工满足本条文。

### P-09 FastAPI 路由与依赖（遵循 B-01、REF-MS-REST）

| 规则 | 说明 |
| --- | --- |
| 注册集中 | 路由在 `index.py` 或子模块 `router` 挂载；路径前缀与 `PROJECT_CONFIG` §F、`_manifest.json` 一致 |
| 依赖注入 | 鉴权用 `Depends`（`_require_auth`、`require_chatbi_principal`）；禁止 handler 内复制 Bearer 解析 |
| 同步 vs 异步 | 阻塞 I/O（部分 Supabase sync、CPU 轻量）可用 `def`；长 I/O / 流式用 `async def` + `await`；**禁止** 在 async 路由内调阻塞 LLM 而不线程池/await 封装（沿用现有 `llm_execute_with_circuit_breaker` 模式） |
| 流式 | Legacy chat：`StreamingResponse`（`text/plain`）；Unified：`/unified/chat/stream` SSE；契约见 `_contract_manifest.json` |

### P-10 异步与并发纪律（遵循 B-02）

- `asyncio.gather` / `create_task`：须明确取消与超时（`asyncio.wait_for`）；Intent / Text2SQL 超时见 env（如 `CHATBI_V2_INTENT_TIMEOUT_S`）。
- **禁止** 无界后台 task 泄漏；`BackgroundTasks` 仅用于 ingest job 等已文档化路径。
- SSE 背压：`CHATBI_SSE_EMIT_QUEUE_MAX` 有界队列；队列满时须 emit truncated / error，禁止 silent drop。

### P-11 重复与共享（遵循 B-09）

- 相同 Supabase RPC / 重试 / embedding 调用 ≥2 处 → `rag_recall_tools.py`、`rag_env.supabase_execute_with_retry`。
- 相同错误 body 构造 ≥2 处 → 抽 factory（对齐 structured error registry 的 `factory` 字段）。
- Hybrid 融合、query rewrite 等已有模块复用，禁止在 `index.py` 与 `unified_chat.py` 各写一份 RRF。

### P-12 测试（遵循 B-10）

| 层级 | 工具 | 范围 |
| --- | --- | --- |
| 单元 | pytest | `rag_env` 解析、intent 规则、mapper、纯函数 |
| 集成 | pytest + mock | 路由 handler、Tool 执行、registry shape |
| 标记 | `@pytest.mark.intent_eval` / `intent_benchmark` | **默认不跑**；CI 与本地合并前命令排除 |

`test_strategy: required` → 先红测试再实现。默认命令：

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
```

Structured error：`tests/test_harness_structured_error_shape_check.py` 须绿。

### P-13 安全（遵循 B-11）

- Admin / sync：`SYNC_ADMIN_SECRET` + `_require_auth()`；禁止绕过或降级为空 secret 上线。
- Text2SQL：`chatbi_sql_gate`、`TEXT2SQL_DATABASE_URL` 只读/变更路径分离；用户 SQL 须经 gate 与 allowlist。
- **禁止** 日志 / pytest 输出完整 Bearer、service role、`CHATBI_PLAN_EXEC_TOKEN_SECRET`。
- Prompt 注入：`CHATBI_PROMPT_GUARD_MODE`；生产默认 `off` 或 `warn`，`block` 须 task 明示。
- OWASP：参数化查询、禁止拼接用户输入进 SQL；路径与 env 注入见 REF-OWASP-API。

### P-14 日志与可观测（遵循 B-12）

| 路径 | 字段 / 约定 |
| --- | --- |
| RAG 对话 | **必须** 写 `rag_conversation_logs`（Legacy + Unified 路径；见 [`.cursor/rules/30-rag-implementation.mdc`](../../.cursor/rules/30-rag-implementation.mdc) · [`AGENTS.md`](../../AGENTS.md) 规则索引） |
| ChatBI JSON | `CHATBI_JSON_LOG=1` → `api/chatbi_json_log.py` 单行 JSON；含 `request_id` / `run_id`（与 SSE `meta.run_id` 对齐） |
| stderr 调试 | `DEBUG_RAG` / `DEBUG_INGEST` 仅开发；**禁止** 生产默认开启大量 PII |
| 关联 id | 新路径须 propagates `session_id`、request/run id，便于 BFF 与日志关联 |

### P-15 CI 与合并前（遵循 L1 §4、B-10）

合并前 **在本仓根** 依次（与 `AGENTS.md` §8、`.github/workflows/pytest.yml` 一致）：

```bash
bash scripts/verify-tech-graph.sh
python tools/tech_graph_contract_check.py
pytest tests -m "not intent_eval and not intent_benchmark"
```

或一键：

```bash
bash scripts/verify-pr-local.sh
```

图谱 / 契约变更时必跑前两项；`test_strategy: required` 的 task 须全绿后再 PR。

---

## 3. 后端反模式（节选）

| ID | 反模式 | 改法 | 条文 |
| --- | --- | --- | --- |
| AP-01 | 业务模块直接 `os.getenv("SILICONFLOW_API_KEY")` | `rag_env.must_siliconflow_api_key()` | P-03 |
| AP-02 | `index.py` 单函数含 ingest + embedding + DB 写 | 下沉 `ingest_pipeline` / 子模块 | P-01 |
| AP-03 | `except Exception: pass` 或仅 `_rag_log` | 窄捕获 + `error_code` + 日志 | P-02, P-05 |
| AP-04 | Agent 解析 `ToolResult.error` 字符串判型 | 只认 `error_code` / `error_stage` | P-05, P-06 |
| AP-05 | 硬编码 `https://api.siliconflow.cn` 或 Supabase URL | `rag_env` helper | P-03 |
| AP-06 | 新路由返回裸字符串 500 | `HTTPException` / Unified error event | P-05 |

全表规划：工作区 `ANTI_PATTERNS_v1_zh.md`（P2 工作区 · 含 notebook 场景）。L1 通用 AP-01～AP-05 仍适用。

---

## 4. PR 自检（后端增量 · 叠加 L1 §4）

在 [`CODING_BASELINE_L1_v1_zh.md`](../../../docs/standards/CODING_BASELINE_L1_v1_zh.md) §4 基础上追加：

- [ ] 新/改路由经既有鉴权与 env helper（P-03, P-09, P-13）
- [ ] 对外错误含可枚举 `error_code`；未破坏 registry / contract（P-05）
- [ ] 无散落 magic URL / 模型名 / 密钥 env 读取（P-03, P-13）
- [ ] 无无理由深层嵌套或裸 `except Exception: pass`（P-02）
- [ ] RAG / Unified 路径考虑 `rag_conversation_logs` 或 ChatBI JSON 日志（P-14）
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿（P-12, P-15）

`code_quality_bar: strict` 时 22 审查须逐项引用上表 + L1 §4。字段定义见工作区 [`docs/harness/HARNESS_V2_PLAN.md`](../../../docs/harness/HARNESS_V2_PLAN.md) **§5.9**（`baseline` 默认 · `strict` = L1 §4 + 本 L2 + 无新增 lint 豁免）。

---

## 5. 工具与 REF 映射

| REF | 本仓落地 |
| --- | --- |
| REF-PEP8 | 格式与 import 顺序；**P4 计划** `ruff check` / `ruff format`（`ruff.toml` 待 P4 task） |
| REF-GOOG-PY | P-08 类型注解；dataclass / Literal；异常窄捕获 |
| REF-MS-REST | P-05、P-09；HTTP status + 结构化 body；幂等与流式契约 |
| REF-OWASP-API | P-13；Text2SQL gate、鉴权、限流 |
| REF-GOOG-CL | PR Test plan + `pytest`（P-12, P-15） |
| REF-OTEL-LOG | P-14；`CHATBI_JSON_LOG` 字段（可选对齐） |

| 工具 | 命令 / 路径 | 状态 |
| --- | --- | --- |
| pytest | `pytest tests -m "not intent_eval and not intent_benchmark"` | CI **Required**（`pytest.yml`） |
| tech-graph | `bash scripts/verify-tech-graph.sh` | CI Required |
| contract | `python tools/tech_graph_contract_check.py` | CI / `verify-pr-local.sh` |
| structured error | `tests/test_harness_structured_error_shape_check.py` | 经 pytest |
| ruff | （待 P4）`ruff check api tests` | **未** 入 CI |

---

## 6. 与 L3 的关系（P3 · 待办）

- Cursor 规则：计划 `.cursor/rules/07-coding-standards-l2.mdc`（`globs: api/**/*.py,tests/**/*.py` · 短链至本文件）。
- `AGENTS.md` → `docs/standards/README.md`。
- **禁止** 在 rules 内复制 P-01～P-15 全文。

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-09 | P2 初稿：P-01～P-15 + AP 节选 + PR 自检 + REF 映射 |
| v1.1 | 2026-06-09 | R1 签收 **active**；S-02 P-08 Any 措辞；S-03 P-14 规则可发现性；S-04 P-03 CI dummy 说明 |
