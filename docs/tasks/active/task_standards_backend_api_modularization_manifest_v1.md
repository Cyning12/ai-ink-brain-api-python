# MANIFEST · 后端 Python 服务模块化 Tech-Debt Epic

> **状态**：active（Epic 母单 · **MANIFEST** · W1 **done** · W2～W8 执行中）  
> **schedule_ref**：编码规范 Epic · §1.5 Tech-debt  
> **epic**：`standards-engineering` · 子主题 **`api-modularization`**  
> **前置**：L2 [`CODING_BACKEND_L2_v1_zh.md`](../../standards/CODING_BACKEND_L2_v1_zh.md) **active**（P-01 路由薄层 · B-01）  
> **建议顺序**：P3+P4 **done** · PR [#145](https://github.com/Cyning12/ai-ink-brain-api-python/pull/145) · W1 **done** [#146](https://github.com/Cyning12/ai-ink-brain-api-python/pull/146) → **W2→W8** 逐 PR  
> **关联图谱**：`docs/_tech_graph/11_flow_api.md` · `10_flow_*.ai.md` · 改拓扑须 `graph_query`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `standards-backend-api-modularization-manifest` |
| **orchestration** | **Epic 链** — 子 task 各自 `task/<slug>` + 链式 PROMPT（见下） |
| **chain_prompt** | Cursor 全 Epic：[`PROMPT_cursor_task_chain_serial_v1_T1_standards-backend-api-modularization-w1-w8_zh.md`](../../harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_standards-backend-api-modularization-w1-w8_zh.md) · CC 续跑 W2～W8：[`PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md`](../../harness/prompts/PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md) |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 母单无代码；子 task 均为 `required` + pytest |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |
| **git_branch** | `—`（子批各自分支） |

---

## 背景与目标

L2 **P-01** 要求路由 **薄**（handler ~80 行软上限）、领域逻辑下沉子模块；现网 **`index.py` ~1180 行**、**`unified_chat.py` ~3200 行** 等违反 B-01 审查阈值，且阻碍 Agent 最小 diff（B-07）。

**Epic 目标**：按 **边界清晰、可独立 PR、可回归测试** 的原则拆分 Python 服务层，**禁止** 单 task「改全服务目录」或一次性 mega-refactor。

**完成态（Epic CLOSE 条件）**：

- [ ] 下表 **W1～W8** 子 task 均 **done**（或显式 **defer** 行 + 人签理由）
- [ ] 无子 task 在「非范围」外触及未列模块
- [ ] `_tech_graph` / `_manifest` 与拆分后 import 路径一致
- [ ] RECENT §1.5 更新为 **CLOSE**

---

## 硬纪律（全子 task 继承）

| # | 纪律 |
|---|------|
| D1 | **单 PR 单主题**：仅动 MANIFEST 该行「目标模块」+ 直接依赖；**禁止** 单 task 改遍 `api/*.py` |
| D2 | **先测后拆**：`test_strategy: required`；拆前补/锁行为测试（route handler mock 或纯函数） |
| D3 | **路由注册不变**：对外 path / 契约 / `_contract_manifest.json` **不破坏**（除非独立契约 task） |
| D4 | **graph_query 先行**：开工前 `python tools/tech_graph_graph_query.py neighbors <node>` 列影响面 |
| D5 | **Ruff 绿**：依赖 P3+P4 task 完成后，子 PR 须 `ruff check` + pytest 绿 |

---

## 子 task 批次（W1～W8 · 待各建 `active/task_*`）

> 行数取自 2026-06-09 `wc -l`；执行时以 HEAD 为准。  
> **分支建议** / **slug** 为初稿；10 帽可微调文件名。

| ID | 主题 | 现状行数 | 目标（摘要） | 建议 slug | 分支建议 | 风险 |
|----|------|----------|--------------|-----------|----------|------|
| **W1** | `rag_env` 收敛 | `rag_env` 234 · `index` 顶散落 env | 新代码零散落 `os.getenv`；`index` 顶层常量迁入 `rag_env` helper | `api-env-rag-env-consolidation` | `task/api-env-rag-env-w1` | Low · **done** PR [#146](https://github.com/Cyning12/ai-ink-brain-api-python/pull/146) |
| **W2** | Legacy chat 路由下沉 | `index` 内 chat/retrieve 大块 | 抽 `api/routes/legacy_chat.py`（或 `api/legacy_chat/`）；`index` 仅 register | `api-routes-legacy-chat-split` | `task/api-routes-legacy-w2` | Medium |
| **W3** | Admin ingest 路由下沉 | `index` admin/sync 段 | 抽 `api/routes/admin_ingest.py`；ingest 仍调 `ingest_pipeline` | `api-routes-admin-ingest-split` | `task/api-routes-admin-w3` | Medium |
| **W4** | Unified JSON 路径 | `unified_chat` JSON handler 段 | 抽 `api/unified/json_handler.py`（名可调整） | `api-unified-json-split` | `task/api-unified-json-w4` | High |
| **W5** | Unified SSE 路径 | `unified_chat` stream 段 | 抽 `api/unified/sse_handler.py`；契约 `_contract_manifest` 必对照 | `api-unified-sse-split` | `task/api-unified-sse-w5` | High |
| **W6** | Agent 循环 | `agent` ~1095 | 抽 tool 调度 / persist 子模块；`ChatBIAgent` 薄编排 | `api-agent-loop-split` | `task/api-agent-w6` | High |
| **W7** | Tool 注册表 | `tools` ~958 | `text2sql_*` vs RAG tools 分文件；保留 `get_tool_registry()` 入口 | `api-tools-registry-split` | `task/api-tools-w7` | Medium |
| **W8** | Intent 栈 | `intent_agent` 746 + `intent_router` 346 | 表驱动与 LLM 路径分文件；不混改 Unified | `api-intent-stack-split` | `task/api-intent-w8` | Medium |

### 显式 defer（Epic 外 · 需单独立项）

| 模块 | 行数 | 说明 |
|------|------|------|
| `rag_recall_tools.py` | 552 | 可与 W2/W4 重叠；**勿**与 W4/W5 同 PR |
| `chatbi_sql_gate.py` | 593 | Text2SQL 安全；须专项 task + 50 |
| `code_retrieval.py` | 600 | 与 GraphRAG 探索 task 可能重叠 · 见 `task_rag_graphrag_pilot_explore_v1.md` |
| `ingest_pipeline.py` | 446 | 已较独立；仅 W3 触边 |

---

## 子 task 文档模板（10 帽复制用）

每个 W* 开工时在 `docs/tasks/active/` 新建，**必填**：

```markdown
> **epic**：`standards-engineering/api-modularization`
> **manifest_ref**：W{n} · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**：`required`
> **非范围**：MANIFEST 表内未列出的 `api/*.py` 文件
```

---

## 行为变更（Delta）

无

（母单 · 无实现。）

各子 task 须独立 §行为变更 · ADDED/MODIFIED（内部 import / 模块路径），**无**对外 HTTP 形状变更除非 task 明示。

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-mega-refactor-pr | 单 PR diff >8 个 `api/*.py` 且无 MANIFEST 授权 | **拒合并** · 拆 PR |
| F2 | fp-contract-break | 拆分破坏 Unified SSE / Legacy stream 契约 | pytest contract + 50 阻塞 |
| F3 | fp-manifest-skip-order | 未 W1 即大改 `index` 300+ 行 | 22 审查要求先 env 收敛 |

---

## Epic 验收标准

- [ ] W1～W8 均有对应 `task_*` 且状态 **done** 或 **defer（人签）**
- [ ] `index.py` 降至 **<400 行**（软上限 · 或 documented 例外）
- [ ] `unified_chat.py` 降至 **<800 行** 或拆为多文件 package（`api/unified/`）
- [ ] 无 open 子 task 违反 D1
- [ ] Coding Wiki 可选 synthesis：`api-modularization-ink-backend`（关账后）

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：Epic MANIFEST 初稿 · W1～W8 批次 |
