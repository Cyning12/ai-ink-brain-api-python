# AI-Ink-Brain API（Python 后端）— Agent 导航

> **角色**：Ink-Brain 博客的 **RAG / Embedding / Chunking / Retrieval / ingest** 服务端（FastAPI）。  
> **边界**：页面渲染、Next.js BFF、博客内容编辑 UX **不在本仓**；本仓提供 HTTP API 与数据库写入能力。

---

## 必读（按顺序）

1. **`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`**：环境变量真值表、目录地图、对外契约、安全注意项
2. **规则文件**（`.cursor/rules/*.mdc`）：RAG / 图谱 / Harness 等工程约束（Cursor 真值源）；其它 Agent 平台读本文 **自动同步规则** 小节（运行 `python tools/gen_agents_md.py` 从 `.mdc` 生成）
3. **`docs/_tech_graph/`**：技术图谱（架构唯一可信来源）
   - `00_main.md` — 顶层流程总图（[AI 协议版](docs/_tech_graph/00_main.ai.md)）
   - `01_struct.md` — 数据库 Struct 模型
   - `02_version.md` — 版本迭代时间线
   - `10_flow_rag.md` — RAG 检索流程（[AI 协议版](docs/_tech_graph/10_flow_rag.ai.md)）
   - `11_flow_text2sql.md` — Text2SQL 流程（[AI 协议版](docs/_tech_graph/11_flow_text2sql.ai.md)）
   - `12_flow_fts.md` — 全文检索流程（[AI 协议版](docs/_tech_graph/12_flow_fts.ai.md)）
   - `13_flow_supabase_rpc.md` — Supabase RPC 流程（[AI 协议版](docs/_tech_graph/13_flow_supabase_rpc.ai.md)）
   - `99_spec.md` — 实现规约
   - `99_mermaid_protocol.md` — Mermaid 拓扑协议（Python/FastAPI 适配版）
4. **`docs/tasks/`**：任务规格（实现与验收口径）；**近期排期** 先读 [`docs/tasks/RECENT_TASK_SCHEDULE.md`](docs/tasks/RECENT_TASK_SCHEDULE.md)  
   - **蒸馏 SKILL（跨 Agent 便携真值）**：[`docs/tasks/skills/README.md`](docs/tasks/skills/README.md)；Harness 流程元复检见 [`SKILL-harness-meta-reinspect.md`](docs/tasks/skills/SKILL-harness-meta-reinspect.md)（Cursor 快捷入口：`.cursor/skills/harness-meta-reinspect/`）
5. **`docs/harness/`**：Harness（10→**人择** 22 或 30→40→50；落盘可查收）
   - 入口：[`docs/harness/README.md`](docs/harness/README.md) → [`docs/harness/ACCEPTANCE_LANDING.md`](docs/harness/ACCEPTANCE_LANDING.md)
   - **22 审核**（仅本仓）：`docs/harness/reviews/` · **50 复检**：`docs/tasks/reinspect_results/`
   - 10 下一棒：**两条** Prompt（A=22，B=30），见 `TEMPLATE-requirements-invoke` §3
6. **多子仓协作**（总设职责、任务单规范与落盘路径）见工作区根 `Projects/AGENTS.md` **§2**，跨仓任务按该约定先写任务初稿再分派子 Agent 丰富。

---

## 非必读（按需）

| 路径 | 说明 |
|------|------|
| **`docs/diary/`** | **非长期、易过时**产物落盘区（验收留证、排障快照、实验报告等）；**默认不读**，仅 task / 用户 `@` 显式指向时打开 |
| **`docs/diary/jsonPKmermaid/`** | 图谱 **行为实验轨**（闸口 A–C″、fixtures、runs）；**非必读**，非实验复现任务勿主动遍历 |
| **写作规范** | 向 diary 新增内容时见 `docs/diary/DIARY_GUIDE.md`；工作区根 `DIARY_GUIDE.md` 为跨仓日记格式 |

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
- **任务驱动**：优先阅读对应 `docs/tasks/*.md`，实现完成后回填验收项与涉及文件列表；**验收通过后**须按 `docs/tasks/README.md` 将任务单从 `active/` **归档**至 `docs/tasks/done/` 并更新 `_views/done.md`：**头部 `done（日期）` 与 `git mv` 同一提交完成**，禁止「状态 done 但文件仍在 `active/`」
- **图谱同步**：代码变更后自动增量更新 `docs/_tech_graph/` 对应文件
  - 流程图（`10_*.md` ~ `13_*.md`）维护双轨：`.md`（人类版）+ `.ai.md`（AI 协议版）
  - 修改代码后，优先更新 `.ai.md`，再同步 `.md`
  - 拓扑协议规范见 `docs/_tech_graph/99_mermaid_protocol.md`

---

## 安全红线

- **不要**把 `.env` / `.env.local` / service role key / API key 提交进 Git。
- CI/生产注入请使用平台 Secrets（不要写进仓库明文）。

<!-- RULES_AUTO_GENERATED -->

## Core

> 核心行为约束 — 语言、职责边界、修改前确认、完成后报告

# Core Principles
- **Language**: 所有解释、注释用简体中文；代码与专有名词保持英文。
- **Single Responsibility**: 仅修改请求涉及的模块，不碰无关文件或函数。
- **Logic Preservation**: 修改前分析现有逻辑，增量修复，不随意删除正确代码。
- **Consistency**: 遵循项目现有代码风格（缩进、命名、结构），禁止纯格式化变更。

# Before Any Modification
1. 列出计划修改的文件清单（相对路径）。
2. 若涉及 3+ 个文件，等待用户确认或收到明确授权「无需确认直接执行」。
3. 自评变更风险等级（Low / Medium / High），High 需额外说明回滚方案。

# After Completion
- 提供 git diff 风格摘要（按文件：+N/-N）。
- 新功能附最小验证示例、预期返回值或日志片段。
- 禁止仅在大段文本中描述变更，必须实际写入文件系统。

---

## Agent Observability

> Agent 模式可观测性与成本控制 — 执行报告、Loop 防护、模式选择

# Agent Observability & Cost Control

## Execution Report（每次任务末尾必须报告）
以结构化格式输出以下信息：

```
📊 Execution Report
├── Duration:     {从接收指令到输出完成的耗时}
├── Thinking Steps:
│   1. {关键决策 1：为什么这样改}
│   2. {关键决策 2}
│   3. {关键决策 3}
├── Files Modified:
│   - {文件 1 相对路径}
│   - {文件 2 相对路径}
├── Risk Level:   {Low / Medium / High}
└── Notes:        {阻塞点、待确认项、或「无」}
```

- **Duration**: 估算或记录实际耗时（分钟/秒）。
- **Thinking Steps**: 3–5 步，说明核心决策路径，不是流水账。
- **Files Modified**: 本次实际修改的文件清单（新增、修改、删除分别标注）。
- **Risk Level**: High 时必须附带回滚方案或风险提示。

## Cost Awareness
- **Fast Request Budget**: Cursor Pro Agent 模式 Fast Requests 约 500 次/月；Agent 应优先在一次对话轮次内完成任务。
- **Mode Preference**:
  - 纯代码生成、格式化、简单重构 → 优先建议 Auto 模式。
  - 跨文件重构、复杂调试、架构设计 → 使用 Agent 模式。
- **Batch Operations**: 涉及多文件时，先输出完整计划再一次性执行，避免「改一点测一点」的循环消耗。

## Loop Guard
- 同一文件修改 **3 次**仍未通过验证（测试失败、编译错误、逻辑不符），必须停止自动重试。
- 向用户报告当前阻塞点（错误日志、失败原因），请求人工介入或明确下一步指令。

## Ambiguity Stop
- 需求模糊、上下文缺失、或可能破坏现有功能时，**优先停止并询问用户**。
- 禁止基于假设继续执行，尤其是涉及数据库迁移、环境变量变更、删除表/字段等操作。

---

## Harness Semi Auto

> Harness 半自动 — 无人工闸阻塞时链式续跑 task，invoke 落盘优先

# Harness 半自动续跑（本仓）

执行 `docs/tasks/active/*.md` 或用户 `@task` 时：

1. **先读** task 文首 `semi_auto`、`human_gate`、`audit_profile`；通则见本仓 `docs/harness/prompts/HANDOFF_SEMI_AUTO.md`（及 `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE`）；入口 [`docs/harness/README.md`](docs/harness/README.md)。
2. **无阻塞则连续跑**：凡 `human_gate` 对下一棒 **非** `pending`（或 `blocks_hats` 不含该帽），**同会话**自动戴下一帽；**禁止**每棒要求用户重贴 `TEMPLATE-*` §3。
3. **下一棒前必落盘**：将下一棒 §3 全文写入本仓 `docs/harness/invokes/invoke_*.md`（本仓 `docs/tasks/` 任务 **禁止** 只写工作区 invokes），再 **commit** 本轮路径，然后执行。
4. **人工闸**：仅 **人** 可将 `pending`→`approved`；遇 `pending` **停**，只输出须改的 `gate_id` 与文件路径，**不得**代填、不得标 `done`。
5. **新会话续跑**：读 task + **最新** `docs/harness/invokes/` 下与本 task 相关的 invoke，按其中 §3 继续；用户可说「按 semi_auto 继续」。
6. **关账**：无下一棒时输出 **执行路线与 Commit 回溯**（`HANDOFF_CLOSE_TRACE`），非空 Prompt。

---

## Harness In Repo

> Harness 本仓真值 — prompts/模板/规划入口，禁止默认查工作区外部路径

# Harness（本后端仓内嵌）

执行 Harness 流程、复制帽子 Prompt、`semi_auto` 续跑时：

1. **唯一入口**：[`docs/harness/README.md`](docs/harness/README.md) → [`docs/harness/prompts/README.md`](docs/harness/prompts/README.md)
2. **模板**：`docs/harness/prompts/TEMPLATE-*-invoke.md` §3；帽子 `10`～`50` 与同目录 `HANDOFF_*.md`
3. **落盘**：invoke → `docs/harness/invokes/`；**22** → `docs/harness/reviews/`（仅本仓 task）；20 → `docs/tasks/review_results/`；**50** → `docs/tasks/reinspect_results/`。10 结束须给 **下一棒 A（22）+ B（30）** 两条 Prompt，**人**择一（见 `ACCEPTANCE_LANDING.md`）
4. **禁止**：在未获 task 显式指向时，默认去读 `Projects/docs/harness/prompts/`（工作区）；跨子仓 Harness **任务单** 例外见 `docs/tasks/README.md`「工作区 Harness 任务」

半自动续跑细则见 [`05-harness-semi-auto.mdc`](05-harness-semi-auto.mdc)。

---

## Git Workflow

> 本地不在 main 上改/提交；远程合入 main 须 PR

# Git 工作流（本仓）

- **远程**：合并 **`main`** **必须 PR**。
- **本地**：**一切任务**（代码、文档、Harness 等）**不要在 `main` 上**直接修改或 `commit`；若在 `main`，先 **切换已有 `task/*` 分支** 或 **`git checkout -b task/<slug>`** 再动手。
- 用户仅说「commit」时：先确认/切换任务分支，再提交。
- **不**默认 `git push`。
- Harness 半自动多帽落盘同样只在任务分支（`HANDOFF_SEMI_AUTO` §5）。

细则见 [`.cursor/rules/07-git-workflow.mdc`](.cursor/rules/07-git-workflow.mdc)。

---

## Docs Diary

> docs/diary — 非必读、易过时产物落盘；实验轨 jsonPKmermaid 按需读

# `docs/diary/` 目录约定（非必读）

## Agent 读取策略（强制）

- **非必读**：`docs/diary/` **全树**不纳入日常必读链路；**非需要不主动读取**（不预加载、不 glob 遍历、不在无关任务中引用）。
- **何时可读**：用户 `@` 明确路径；当前 **task / invoke** 依赖列出 diary 路径；排障、复盘、实验复现且范围已锁定到**具体文件**。
- **`docs/diary/tmp/`**：**不纳入 Git**（`.gitignore`）；Agent **禁止**默认 glob/grep/遍历；仅用户或 task **单独指明**具体文件时可读。
- **真值优先级**：实现与架构以 `docs/_tech_graph/`、`docs/meta/`、`docs/tasks/`、`docs/spec/` 为准；diary **不得**覆盖或替代上述真值。

## 落盘纪律（写什么进 diary）

- **用途**：存放 **非长期维护**、**易过时** 的产物，例如：一次性验收记录、实验批次报告、对比跑分、留证 curl、阶段性结论草稿、排障快照。
- **长期真值不得滞留**：结论已冻结并写入 `_tech_graph/`、`docs/tasks/done/`、`docs/tech_graph/SPEC/` 等稳定位置后，diary 内文稿仅作 **历史回溯**；Agent 默认 **不再**以其叙述作为实现依据。
- **新增沉淀**：优先落在 `docs/diary/`（按 `DIARY_GUIDE.md` 命名）；若内容将长期引用，须同步提炼进真值表 / 图谱 / task，而非仅堆在 diary。

## 实验轨：`docs/diary/jsonPKmermaid/`（非必读）

| 项 | 约定 |
| --- | --- |
| **性质** | 图谱 **行为实验 / 闸口对照** 的脚本、`fixtures/`、`reports/`、`runs/` 等 |
| **读取** | **非必读**；仅在做 jsonPKmermaid 复现、闸口实验、或 task 显式引用其中路径时，打开 **最小必要文件集** |
| **与生产轨** | accepted 结论的 **执行真值** 在 `docs/_tech_graph/`、`tools/tech_graph*.py` 与 CI；**禁止**为日常改代码默认遍历 `jsonPKmermaid/` |

## 日期总结（`YYYY-MM-DD.md`）

- 按 `docs/diary/DIARY_GUIDE.md` 写的后端知识总结同属 diary，同样 **按需** 读取，作为归总素材而非实现依据。

---

## Tech Graph

> 技术图谱 — Mermaid 维护轨 + graph.json 机器轨（双轨，低幻觉）

## `_tech_graph/` 技术图谱（唯一事实来源）

- 架构、流程、依赖的**维护真值**在 `docs/_tech_graph/`；禁止用大段纯文本文档替代图谱做业务逻辑依据。
- 前后端**各自**维护本仓 `_tech_graph/`，禁止混用他仓图谱文件。
- 与 **jsonPKmermaid 实验轨**（`docs/diary/jsonPKmermaid/`）的关系：**非必读**（见 `08-docs-diary.mdc`）；本规则描述 **生产轨**（`_tech_graph/` + `graph_query`）。仅在做闸口复现或 task 显式引用时按需读实验目录，**禁止**默认遍历。

## 双轨制（维护轨 vs 机器轨）

| 轨道 | 载体 | 谁维护 | Agent 何时优先读 |
|------|------|--------|------------------|
| **维护轨** | `*.md` / `*.ai.md`（内嵌 Mermaid） | 人 + Agent 改图后导出 | 改流程拓扑、补锚点、写规约叙述、对照 `01_struct` |
| **机器轨** | `graph.json`（**graph_v2**）、`_manifest.json`、`_contract_manifest.json` | 脚本导出 + 契约门禁；`graph.json` 由 `.ai.md` 导出 | **影响分析、依赖遍历**：**`graph_query` 子图优先**（`tools/tech_graph_graph_query.py`），再 `_manifest` / `_contract`；**禁止**默认整包 `graph.json` 或 **graph_v1** 整图灌 prompt |

- **禁止**把 `graph.json` 当作可手改源文件；改图 → 改对应 `.ai.md` → `python tools/tech_graph_graph_export.py`（或 CI `--check`）再生 `graph.json`。
- **禁止**在对话里用整份 `graph.json` 替代已导出的 Mermaid 维护义务；JSON 与 Mermaid 语义须等价。
- **禁止**将 **graph_v1 整包** 或 **graph_v2 整文件** 作为 Agent 默认主载荷（闸口 A / G-END-5）；须 **`graph_query`**（`downstream` / `upstream` / `neighbors`）取子图 + anchors。无 `graph_v2` 时 query **FAIL（FP-5）**，不得静默降级为 v1 整包。
- `01_struct.md` 的 **classDiagram** 仍为库表 Struct 真值（未并入 `graph.json` 时不得仅用 JSON 推断表结构）。

## Mermaid 格式与协议（维护轨）

- 流程图（flowchart）：遵循 `docs/_tech_graph/99_mermaid_protocol.md`。
  - 边标记：`->`（同步）、`~>`（异步）、`?>`（条件）、`[ok]` / `[err]`（状态）、`::xxx`（元关系）
  - 禁止裸边（无边标记的 `-->`）
  - 锚点用 `// → path#Ln` 独立注释行，不写在节点标签内
- 数据结构：Struct 用 `classDiagram`；**禁止**在图谱正文中粘贴完整 DDL / 长 JSON / TS interface（见 `99_spec.md`）。

## 本仓 `docs/_tech_graph/` 目录（摘要）

```text
docs/_tech_graph/
├─ 00_main.md / 00_main.ai.md     # 顶层流程（人/AI 双轨）
├─ 01_struct.md                   # DB Struct（classDiagram）
├─ 02_version.md                  # 版本时间线
├─ 10_flow_*.md / *.ai.md          # 子流程（双轨）
├─ 99_spec.md                     # 实现规约与 Env 约束
├─ 99_mermaid_protocol.md
├─ graph.json                     # 【机器轨】由 *.ai.md 导出，勿手改
├─ _manifest.json                 # 端点 / RPC / 表 / env 清单
└─ _contract_manifest.json        # 跨端契约（如 Unified SSE）
```

## Mermaid 人读 / AI 协议双轨（`.md` vs `.ai.md`）

- `.md`：人类友好（可裸边、锚点可写在节点内）。
- `.ai.md`：AI 协议版（零裸边、锚点分离、异步/错误显式）；**导出 `graph.json` 的输入源**。
- 流程图须保持两者语义等价。

## Agent 读取顺序（本仓后端）

1. **影响分析 / 改接口 / 改 RAG 链路**（**query 优先**）：
   - `python tools/tech_graph_graph_query.py downstream <id> <depth>`（或 `upstream` / `neighbors`）→ 子图 JSON + `anchors`
   - → `_manifest.json` 切片 →（若涉 **Unified Chat / SSE / T002 类题**）`_contract_manifest.json` 切片（与闸口 C′ 物化一致；**不**在本规则展开新实验）
   - → 按需 `01_struct.md` / `99_spec.md`
   - → query 不足时再读对应 `10_flow_*.ai.md` 片段
   - **Admin Ingest / T003 类题**（且 **task 已指向** `docs/diary/jsonPKmermaid/fixtures/...`）：在子图 + manifest/contract 之后，可参照实验轨 **`manifest_slice` + `impact_surface`**（path/kind 来自 gold `impacts[]`）；产出 `impacts[]` **须含 `path` + `kind`**。**无 task 指向时勿读** jsonPKmermaid fixtures。
   - **勿**默认 `cat graph.json` 整包；**勿**用 graph_v1 冒充 v2 query。
2. **改表结构 / 向量维度 / Env**：`01_struct.md`、`99_spec.md` + 代码；不单靠 `graph.json`。
3. **改代码后**：同步更新受影响 `.ai.md` / `_manifest` / `_contract`，并确保 `graph.json`（**graph_v2**）导出与 CI（`tech_graph_manifest_check`、`tech_graph_contract_check`、`tech_graph_graph_export --check`、`tech_graph_graph_equivalence_check`）通过。

## jsonPKmermaid 物化轨 vs 默认 machine 轨（闸口 C / C′ / C″ · 实验轨 · 非必读）

> 本节为 **历史实验结论摘要**；日常实现以 **`graph_query` + `_tech_graph/`** 为准。详文与 fixtures 在 `docs/diary/jsonPKmermaid/`，**仅 task/用户显式需要时**打开。

| 项 | 约定 |
| --- | --- |
| **machine 默认** | **`CTX_V2_QUERY`** / **`graph_query` 子图**（闸口 C **accepted**，C″ **不推翻**） |
| **物化切片** | 分题 `manifest_slice` / `impact_surface` 为 **实验/物化辅助**，**不等于**整包 `graph.json` 或默认 **`15_e2e` 双轨** |
| **人读/对照轨** | **`CTX_DUAL_MD`** 仅对照或人读按需；**禁止**升为 machine 默认 |

## 禁止项（Agent 消费 · 重申）

- **禁止**将物化 `impact_surface` 或分题 `manifest_slice` **当作**默认整包 `graph.json`、graph_v1/v2 全文件或 `15_e2e` Mermaid 双轨主载荷。
- **禁止**因物化切片有效而默认切换为 `CTX_DUAL_MD`；维持 **`graph_query` + `CTX_V2_QUERY`**。

## 稳定引用（生产轨）

- 方案 1 规约：`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`
- 方案 2 查询：`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` · `tools/tech_graph_graph_query.py`

## 按需引用（实验轨 · 非必读）

- 闸口 C / C′ / C″ 结论文与 gold 题集：`docs/diary/jsonPKmermaid/reports/`、`docs/diary/jsonPKmermaid/fixtures/`（freeze_id 见各 `conclusion_*`；**勿**在无 task 时主动读取）
- 前端图谱：见 `ai-ink-brain/` 仓内规则（目录同为 `docs/_tech_graph/`）
- 工作区总规范：`Projects/AGENTS.md` §7

---

## Tech Graph Update

> 图谱增量更新 — 改 .ai.md 后导出 graph.json 与 manifest/contract

## 图谱自动增量更新规则

### 触发条件

- 代码、表结构、接口、Env、SSE/契约变更时：更新 `docs/_tech_graph/` 中**受影响**的 `.ai.md` / `_manifest.json` / `_contract_manifest.json`（及人类版 `.md` 若需同步）。
- 禁止无差别全量重生成所有图谱文件。

### 更新原则

- 只改受影响节点/边/清单项；保持文件命名与双轨结构稳定。
- `02_version.md` 在里程碑变更时追加记录。
- 维护轨改完后**必须**再生机器轨：
  - `python tools/tech_graph_graph_export.py`（或 CI 等价 `--check`）→ 更新 `graph.json`
  - 端点/RPC/表/env 变更 → 跑 `python tools/tech_graph_manifest_check.py`
  - 契约变更 → 跑 `python tools/tech_graph_contract_check.py`

### AI 必须遵守

- 改代码前：影响分析优先读 `graph.json` + `_manifest.json`（+ 契约 JSON 若相关）。
- 改代码后：同步维护轨与机器轨；**不允许**代码与 `graph.json` / manifest / contract 长期不一致。
- **不允许**只改 `graph.json` 而不改源 `.ai.md`。

---

## Rag Implementation

## RAG & Architecture Standards（本仓实现约束）
- **Single Source of Truth**：本 Python 服务是 Embedding / Chunking / Retrieval 逻辑的唯一权威来源。
- **Supabase Integration**：
  - 使用 `supabase-py` 做 DB/Auth 交互。
  - 所有 RAG logs 必须写入 `rag_conversation_logs` 表。
  - 相似度检索使用 `pgvector` 的 Cosine Distance。
- **Session & Memory**：
  - 每次请求必须处理 `session_id`。
  - Retrieval 前需要查询 `rag_conversation_logs` 以重建最近 3-5 轮上下文。
- **Efficiency**：
  - 使用 `BackgroundTasks` 处理非阻塞操作（例如写 Supabase 日志、更新 analytics）。
  - 对 Postgres 做连接池，以支撑并发 API 请求。

## Logic Implementation Rules
- **Intent Routing**：使用 `QueryRewrite` 模块做用户意图分类（Search vs. Chat vs. Command）。
- **Hybrid Retrieval**：Vector + Postgres FTS（TSVECTOR）结合，提高关键词精度。
- **Streaming**：LLM 输出优先使用 `StreamingResponse`，保持 “Ink-writing” 效果。

## Development & Quality Control
- **Environment**：严格依赖 `.env` 注入密钥与环境变量。
- **Terminologies**：使用 “Embedding / Rerank / Context Window / Vector Dimension” 等术语。
- **Observability**：每次 RAG turn 必须记录 `retrieved_context` 与 `latency`。

## Error Handling
- 使用结构化错误响应。
- Supabase 失败：返回 graceful 500（`DATABASE_DISCONNECT`）。
- SiliconFlow 限流/失败：实现 retry 或 fallback。


---

## Error Handling

> 错误处理与降级策略 — 结构化响应、异常分支、备选方案

# Error Handling & Uncertainty

## Structured Error Response
- 所有异常必须返回结构化信息，禁止裸字符串抛出。
- FastAPI 场景：使用 `HTTPException` 或自定义 `ErrorResponse` 模型，包含 `code`, `message`, `detail`。

## Graceful Degradation
- **Supabase 失败**: 返回 `500 DATABASE_DISCONNECT`，附带重试建议或缓存降级逻辑。
- **SiliconFlow 限流/失败**: 实现指数退避重试（max 3 次）或 fallback 模型切换。
- **依赖缺失**: 若推荐方案依赖未安装包或未配置环境，必须提供备选方案（如纯原生实现或 mock 路径）。

## Fallback Strategy
- 主方案受阻时，主动提供 Plan B（性能略低但可立即运行）。
- 涉及外部服务（API、DB、向量库）时，默认考虑「服务不可用」场景。

## Uncertainty Stop
- 遇到以下情况必须暂停并询问，不猜测：
  - 需求存在多种矛盾解释
  - 缺少关键环境变量或密钥
  - 修改可能影响未在请求中提及的模块
  - 数据库 schema 变更无迁移脚本
