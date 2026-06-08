# 后端造题骨架 · 月之暗面（Round 1）

> **Draft 副本**：canonical 路径为 docs 仓 `[planning/月之暗面_全流程模拟/06b_后端造题骨架_v1_zh.md](../../../../docs/planning/月之暗面_全流程模拟/06b_后端造题骨架_v1_zh.md)`（相对本文件为工作区外路径，以用户本机 docs 仓为准）。


| 项       | 内容                                                                                            |
| ------- | --------------------------------------------------------------------------------------------- |
| **版本**  | v1.0                                                                                          |
| **日期**  | 2026-06-07                                                                                    |
| **来源仓** | `ai-ink-brain-api-python` @ `b6f97c6`                                                         |
| **轨道**  | A · Coding ×2 + B · Harness ×1                                                                |
| **题量**  | 3（仅骨架）                                                                                        |
| **状态**  | draft · Round 1                                                                               |
| **方法论** | `[05b_造题方法论与例题集_v1_zh.md](../../../../docs/planning/月之暗面_全流程模拟/05b_造题方法论与例题集_v1_zh.md)` §2～§4 |


---

## 造题六步法（本回合覆盖范围）

① 定技能 → ② 选场景 → ③ 最小环境（目录树骨架）→ ④ 题干与约束 → ⑤ 判分思路 → ⑥ **校准：待跑**

---

### 题目卡片 · BE-1


| 字段                | 内容                                                                                                                                                                                                                                                                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **标题 slug**       | `be-sql-readonly-gate-align-v1`                                                                                                                                                                                                                                                                                                    |
| **轨道**            | A · Coding                                                                                                                                                                                                                                                                                                                         |
| **技能标签**          | `READ_LEGACY` `TEST_DISCIPLINE` `BOUNDARY`                                                                                                                                                                                                                                                                                         |
| **难度**            | L2                                                                                                                                                                                                                                                                                                                                 |
| **本仓锚点**          | `api/text2sql_core.py::validate_sql_readonly` · `api/chatbi_sql_gate.py::apply_chatbi_sql_gate` · `api/chatbi_sql_gate.py::_phase_ast` · `api/chain_chat.py::handle_chain_chat`（L653 附近调用 `validate_sql_readonly`）· `api/tools.py::text2sql_execute`（`principal2 is None` 时仅走 readonly 路径）· `tests/test_chatbi_sql_ast_gate_v1.py` |
| **场景（1 句）**       | 自研 Text2SQL 存在 **双轨校验**：ChatBI 主路径走 AST 后闸，而 `chain_chat` / 无 principal 的 tool 路径仍依赖较弱的 `validate_sql_readonly`，隐藏测可构造「单分号多语句」漏网。                                                                                                                                                                                                  |
| **任务（1 句）**       | 对齐只读校验与 `apply_chatbi_sql_gate` 的 AST 多语句规则，并补测试，使 `chain_chat` 与 `text2sql_execute` 的无 principal 分支无法执行 `SELECT 1; SELECT 2` 类语句。                                                                                                                                                                                                 |
| **允许 / 禁止**       | **允许**：`api/text2sql_core.py`、`api/chain_chat.py`、`api/tools.py`（仅校验调用点）、`tests/test_*sql`*、`tests/test_chain_chat_events.py`。**禁止**：改 `api/chatbi_sql_gate.py` 业务规则语义（可复用其函数）、改 `api/index.py` 路由、改 `supabase/`、引入新依赖、动 `_tech_graph/`。                                                                                           |
| **最小环境（骨架）**      | `task-be-sql-gate/` → `api/text2sql_core.py` · `api/chain_chat.py` · `api/tools.py` · `tests/test_chatbi_sql_ast_gate_v1.py` · `tests/test_chain_chat_events.py` · `TASK.md`（Round 2）；私有：`tests/_hidden/test_sql_gate_leaks.py`                                                                                                    |
| **（B 专）工具与步数**    | —                                                                                                                                                                                                                                                                                                                                  |
| **（B 专）H0 vs H1** | —                                                                                                                                                                                                                                                                                                                                  |
| **公开测 / 隐藏测（思路）** | **公开**：`validate_sql_readonly` 对合法 `WITH … SELECT`、块注释前缀 SELECT 通过；`chain_chat` mock 下游后返回 `events[]` 含 `tool.call` 且无 error。**隐藏**：`SELECT 1; SELECT 2`（单分号双语句）须拒绝且 error_stage 为 validate；`SELECT 1; DELETE FROM public.agent_info` 须拒绝；仅改 `text2sql_core` 未改 `chain_chat` 调用语义时行为仍一致。                                           |
| **判分**            | **终态**：相关 pytest 全绿。**轨迹**：diff 仅白名单路径。**越界**：触及 `chatbi_sql_gate` 规则表或 DB 迁移 → fail。**A-B**：不适用。                                                                                                                                                                                                                                  |
| **预期失败聚类**        | 只加固关键词正则、未用 sqlparse 多语句 → 隐藏测 `SELECT 1; SELECT 2` 仍过（模型弱）。 复制整段 `apply_chatbi_sql_gate` 进 core 导致 principal 路径双重拒绝或异常（越界/过度修改）。                                                                                                                                                                                                  |
| **防刷题**           | 隐藏测表名 / schema 从 `agent_info`、`chatbi_user_portrait` 等池随机；语句间空白与大小写变体轮换 seed。                                                                                                                                                                                                                                                      |
| **校准** | Round 2 可跑 → [`docs/harness/eval/be-sql-readonly-gate-align-v1/README.md`](../../eval/be-sql-readonly-gate-align-v1/README.md) |


最小环境目录树（BE-1）

```text
task-be-sql-gate/
├── api/text2sql_core.py
├── api/chain_chat.py
├── api/tools.py
├── tests/test_chatbi_sql_ast_gate_v1.py
├── tests/test_chain_chat_events.py
└── TASK.md                    # Round 2 扩写
# 评测机私有：tests/_hidden/test_sql_gate_leaks.py
```



---

### 题目卡片 · BE-2


| 字段                | 内容                                                                                                                                                                                                                                                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **标题 slug**       | `be-tool-registry-schema-prefetch-v1`                                                                                                                                                                                                                                                                                                                   |
| **轨道**            | A · Coding                                                                                                                                                                                                                                                                                                                                              |
| **技能标签**          | `CROSS_FILE` `BOUNDARY` `ASYNC_ERR`                                                                                                                                                                                                                                                                                                                     |
| **难度**            | L1                                                                                                                                                                                                                                                                                                                                                      |
| **本仓锚点**          | `api/tools.py::ToolRegistry` · `api/tools.py::get_tool_registry` · `api/tools.py::Tool` / `ToolResult` · `api/agent.py::ChatBIAgent._select_tool` · `api/agent.py::ChatBIAgent.run` · `api/text2sql_schema_prefetch.py::run_text2sql_schema_prefetch_sync` · `docs/spec/research/SPEC-Research-SelfChain-vs-LangChain-v1_zh.md`（Tool 层对照，非 LangChain 库） |
| **场景（1 句）**       | V2 Agent 仅暴露 `rag_search` / `text2sql_query` / `direct_answer`，而 Text2SQL 链路内已有 schema prefetch 能力未作为独立 Tool 供 Intent 显式选用。                                                                                                                                                                                                                             |
| **任务（1 句）**       | 在 `ToolRegistry` 注册只读 Tool `schema_prefetch`（包装现有 prefetch 同步函数），并在 `ChatBIAgent` 工具选择与 `tool_mode_map` 中接入，使 `prefer` 强制或 Intent 选中时可调用且返回结构化 `ToolResult`。                                                                                                                                                                                            |
| **允许 / 禁止**       | **允许**：`api/tools.py`、`api/agent.py`、`api/chatbi_agent_models.py`（若需扩展 `ToolName`）、`tests/test_agent*.py` 或新建 `tests/test_tool_schema_prefetch.py`。**禁止**：改 `api/unified_chat.py` 主路由、改 Intent LLM prompt、新增 HTTP 端点、声称使用 LangChain/LangGraph 库、修改 `text2sql_schema_prefetch` 核心检索逻辑（仅可包装调用）。                                                           |
| **最小环境（骨架）**      | `task-be-tool-prefetch/` → `api/tools.py` · `api/agent.py` · `api/text2sql_schema_prefetch.py` · `tests/test_tool_schema_prefetch.py` · `TASK.md`；可选 `tests/fixtures/schema_prefetch_hits.json`                                                                                                                                                         |
| **（B 专）工具与步数**    | —                                                                                                                                                                                                                                                                                                                                                       |
| **（B 专）H0 vs H1** | —                                                                                                                                                                                                                                                                                                                                                       |
| **公开测 / 隐藏测（思路）** | **公开**：`get_tool_registry().get("schema_prefetch")` 非空；mock prefetch 返回固定 DDL 片段时 `execute` 成功且 `error_code` 为空。**隐藏**：未知 tool 名仍抛 `RuntimeError`；prefetch 抛异常时 `ToolResult.success=False` 且 `error_stage` 含 `schema_prefetch`；`AGENT_MAX_STEPS` 内多步 run 未无限循环调用 prefetch。                                                                              |
| **判分**            | **终态**：新 tool 单测 + 现有 agent 相关测不回归。**轨迹**：`git diff` 文件数 ≤4。**越界**：改 unified 路由或引入第三方 Agent 框架 → fail。                                                                                                                                                                                                                                                  |
| **预期失败聚类**        | 只在 `tools.py` 注册未改 `agent.py` 的 `ToolName` 联合类型 → Intent 选中后 runtime 崩溃（模型弱）。 在 tool 内直接执行 SQL 或 mutate DB（越界 / 题干理解错误）。                                                                                                                                                                                                                                |
| **防刷题**           | Tool 描述文案与 fixture DDL 标题随 task_id hash 轮换；隐藏测校验 `parameters` JSON Schema 必填字段名。                                                                                                                                                                                                                                                                        |
| **校准**            | **待跑**                                                                                                                                                                                                                                                                                                                                                  |


最小环境目录树（BE-2）

```text
task-be-tool-prefetch/
├── api/tools.py
├── api/agent.py
├── api/text2sql_schema_prefetch.py
├── tests/test_tool_schema_prefetch.py
└── TASK.md
# 可选：tests/fixtures/schema_prefetch_hits.json
```



---

### 题目卡片 · BE-3


| 字段                | 内容                                                                                                                                                                                                                                                                                                                                                                          |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **标题 slug**       | `be-harness-unified-events-prefer-v1`                                                                                                                                                                                                                                                                                                                                       |
| **轨道**            | B · Harness                                                                                                                                                                                                                                                                                                                                                                 |
| **技能标签**          | `TOOL_CHAIN` `CONTEXT_MGMT` `EVAL_HARNESS` `LONG_HORIZON`                                                                                                                                                                                                                                                                                                                   |
| **难度**            | L2                                                                                                                                                                                                                                                                                                                                                                          |
| **本仓锚点**          | `api/unified_chat.py::handle_unified_chat` · `api/unified_chat.py::_parse_prefer` · `api/unified_chat.py::_event` · `api/index.py`（`POST /api/py/unified/chat`）· `tests/test_unified_chat_backend_v1.py` · `docs/_tech_graph/_contract_manifest.json`（Unified SSE / events 契约切片）· `docs/spec/research/SPEC-Research-SelfChain-vs-LangChain-v1_zh.md` §1.1（自研 `events[]` 叙事） |
| **场景（1 句）**       | Portfolio 演示需证明 Unified Chat 在 `prefer=text2sql` 与 `CHATBI_USE_AGENT=false` 时 `events[]` 顺序与契约一致；Agent 须从文档片段提取路由规则并更新评测 stub，而非臆造事件类型。                                                                                                                                                                                                                                     |
| **任务（1 句）**       | 依据给定 `docs/fixtures/unified_prefer_brief.md` 与契约摘录，将 `harness/fixtures/expected_unified_events.yaml` 的 `event_types` / `final_mode` 与 mock 请求参数对齐，并通过轨迹断言脚本验证（不修改生产 `api/`）。                                                                                                                                                                                                |
| **允许 / 禁止**       | **允许**：`harness/`、`tests/fixtures/`、`docs/fixtures/`（题面注入）、只读打开 `api/unified_chat.py`。**禁止**：改 `api/` 业务代码、改 `_tech_graph` 拓扑、跑真实 Supabase/SiliconFlow、写完整 pytest 实现（Round 1 仅思路）。                                                                                                                                                                                          |
| **最小环境（骨架）**      | `task-be-harness-unified/` → `docs/fixtures/unified_prefer_brief.md` · `docs/_tech_graph/_contract_manifest.json` · `harness/fixtures/expected_unified_events.yaml` · `harness/scripts/assert_event_trace.py` · `tests/test_unified_chat_backend_v1.py` · `SCENARIO.md`                                                                                                     |
| **（B 专）工具与步数**    | **工具白名单**：`read_file`、`grep`、`write_file`（仅 `harness/fixtures/`）、`run_terminal_cmd`（仅 `pytest tests/test_unified_chat_backend_v1.py -k <pattern>` 或 `python harness/scripts/assert_event_trace.py`）。**max steps**：12                                                                                                                                                        |
| **（B 专）H0 vs H1** | **H0** 将 `api/unified_chat.py` 全文 + `docs/spec/research/` 灌入上下文；**H1** 仅注入 `_contract_manifest.json` 中 Unified Chat 条目 + `unified_prefer_brief.md` 子图索引，按需 `read_file` 打开 `tests/test_unified_chat_backend_v1.py` 样例。**小样本**对照成功率/步数，不外推 Kimi 产品指标。                                                                                                                         |
| **公开测 / 隐藏测（思路）** | **公开**：yaml 中 `final_mode=text2sql` 且 `event_types` 含 `router.decision` 与 `latency`。**隐藏**：未读 brief 不得写入 `tool.call.text2sql` 顺序；`prefer=tool:rag_search` 在 v1 须产出 `error` 事件（见 `handle_unified_chat` L883–901）；修改 `api/` 任何文件 → 越界 fail。                                                                                                                                   |
| **判分**            | **终态**：`expected_unified_events.yaml` 字段与 gold 一致。**轨迹**：至少一次 `grep`/`read_file` 命中 `prefer` 或 `router.decision`；步数 ≤12。**越界**：diff 超出 `harness/fixtures/`。**A-B**：同题 H0 vs H1 比较通过率、平均步数、是否误改无关事件类型。                                                                                                                                                                       |
| **预期失败聚类**        | H0 上下文过长抄错事件名或漏 `latency`（Harness 弱 / compaction）。 未读契约臆造 `agent.intent` 顺序（模型弱；题干已给 brief 指针）。                                                                                                                                                                                                                                                                             |
| **防刷题**           | 每次运行轮换 `prefer` 枚举与 `query` 文案；gold yaml hash 入库，brief 章节号随机。                                                                                                                                                                                                                                                                                                               |
| **校准**            | **待跑** · H0/H1 各 ≥5 次小样本                                                                                                                                                                                                                                                                                                                                                    |


最小环境目录树（BE-3）

```text
task-be-harness-unified/
├── docs/fixtures/unified_prefer_brief.md
├── docs/_tech_graph/_contract_manifest.json
├── harness/fixtures/expected_unified_events.yaml
├── harness/scripts/assert_event_trace.py
├── tests/test_unified_chat_backend_v1.py
└── SCENARIO.md
```



---

## § 自检清单

- [x] 题量 = 3，轨道 **A×2 + B×1**
- [x] 难度覆盖 **L1**（BE-2）与 **L2**（BE-1、BE-3）
- [x] 含 **1 道 Harness 题**（BE-3），含工具白名单、步数上限、终态断言、H0 vs H1
- [x] 每题主技能标签不重复（BE-1：`READ_LEGACY`；BE-2：`CROSS_FILE`；BE-3：`TOOL_CHAIN`）
- [x] 锚点路径来自只读扫描（`api/index.py` 路由、`chatbi_sql_gate`、`ToolRegistry`、`handle_unified_chat`）
- [x] 无完整 `TASK.md` / `SCENARIO.md` 正文、无隐藏测代码
- [x] **无 LangChain / LangGraph 库依赖表述**（仅自研链 / `events[]` / `ToolRegistry`）
- [x] 校准均标 **待跑**
- [x] 适合 Mentor 口述「为何选 SQL 双轨、Tool 扩展、Unified 轨迹 A/B」

---

## 修订记录


| 日期         | 说明                    |
| ---------- | --------------------- |
| 2026-06-07 | v1.0 · Round 1 后端三题骨架 |


