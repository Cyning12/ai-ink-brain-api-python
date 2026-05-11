# Task：ChatBI V2 — Text2SQL 多轮语义承接（已实现基线 + 值域锚点后续）

> **状态**：`archived_done`（**V2 本子任务完结**；B-PR1 2026-05-09；B-PR2 2026-05-11；§验收已闭合。）  
> **归档位置**：`docs/tasks/done/task_chatbi_v2_text2sql_multiturn_grounding_v1.md`（若你仍打开 `active/` 下旧路径，请改指向 **done**）。  
> **未纳入 V2 的后续**：**欠债已单独记录** → `docs/tasks/active/task_chatbi_v3_debt_from_v2_multiturn_v1.md`（**V3 统筹**，含 §4.3 澄清、同义词语义等）。  
> **范围**：仅后端 `ai-ink-brain-api-python`（Text2SQL 工具链、会话记忆形状；不涉及前端 transcript UI）  
> **关联规格**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md`（L1–L4 分层、§3 指代与 rewrite、§4 结构化上下文）  
> **父任务索引**：`docs/tasks/done/task_chatbi_v2_agent_p1_behavior.md`（P1 总览，**已归档**；本子任务可视为其下「多轮 + Text2SQL 真值」专项）  
> **真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（环境变量与路由以该文件为准，本文不复制）  
> **关联（V2 可观测 / RAG 改写 / LLM Prompt）**：`docs/tasks/done/task_chatbi_v2_rewrite_timeline_llm_prompt_capture_v1.md`

---

## 背景与目标

多轮场景下，用户首轮明确表名（如 `agent_info`），次轮用「刚刚那张表 / 其中有多少男性」等**省略主语**的问法时，系统需在语义上接得住：**Intent 仍走结构化查库、Text2SQL 检索与生成能继承上轮表/语境**，避免出现「未查到数据」或**选错表**（如 `agent_info` 与 `customer_info` 混用）、**条件字面量与库内枚举不一致**等问题。

本子任务落盘 **A / B / C** 三块（可分期验收）：

1. **A（已实现）**：在 Text2SQL 路径注入会话历史，用于 DDL 检索与 SQL 生成提示（基线修复）。  
2. **B（分阶段）**：**PR1 已完成**可版本化字典 + `build_sql_prompt` 注入；**PR2 已实现** DISTINCT 采样与 YAML 并集防漂移（默认 `TEXT2SQL_DISTINCT_PROBE` 关闭）。与规格 §4 对齐。  
3. **C（已实现基线）**：上轮结构化锚点（表/SQL 摘要）；澄清策略 P1+ 另单。

---

## 范围

### A. 多轮历史注入 Text2SQL（已实现）

- [x] `text2sql_execute`：不再丢弃 `history`；用 `history_to_rewrite_block` 生成对话块。  
- [x] DDL 检索：检索串合并历史 + 当前问题（`_text2sql_retrieve_query`，长度上限 `TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`，默认 1200）。  
- [x] `build_sql_prompt`：可选 `dialogue_context`，注入「近期对话（指代消解）」说明块。  
- [x] `AgentMemoryStore.save`：内存缓存条目与 `load` 一致为 `{query, response}`，避免同进程次轮解析出空历史。

### B. 枚举 / 同义词 / 列值域提示（PR1 + PR2 已落地）

- [x] **PR1**：可版本化 **YAML**（`docs/text2sql/v1/value_hints.yaml`：当前 `agent_info.gender` + `commission_structure`，`values` 与 `docs/text2sql/v1/sql/supabase_init.sql` 对齐），经 `api/text2sql_value_hints.py` 注入 `build_sql_prompt(..., value_hints_block=)`。  
- [x] **PR2**：allowlist DISTINCT + 与 YAML `values` 并集（不 YAML 短路）；探针失败列降级仅 YAML；说明文案见 `build_value_hints_block_for_text2sql`。  
- [x] 与 DDL 边界：prompt 内固定为「业务术语与库内取值」+ 不替代表结构说明（见代码拼装）。  
- [x] **PR1 env**：`TEXT2SQL_VALUE_HINTS_PATH`、`TEXT2SQL_VALUE_HINTS_ENABLED` 已写入 `PROJECT_CONFIG`。  
- [x] **PR2 env**：`TEXT2SQL_DISTINCT_PROBE` / `TEXT2SQL_DISTINCT_MAX` / `TEXT2SQL_DISTINCT_COLUMNS` / `TEXT2SQL_DISTINCT_MAX_PROBES` / `TEXT2SQL_DISTINCT_STMT_TIMEOUT_MS` 已写入 `PROJECT_CONFIG` 与 `.env.example`。

### C. 上轮结构化锚点（已实现基线；澄清策略仍为 P1+）

- [x] 成功执行 Text2SQL 后，在 `rag_conversation_logs.tool_results` 写入 **`text2sql_grounding`**（`v`、`primary_table`、`resolved_tables`、`sql_excerpt`，由 SQL 解析，无新 DB 列）。  
- [x] 次轮 `AgentMemoryStore.load` 将 `text2sql_grounding` 合并进 `history[]`；`history_to_rewrite_block` 与 Intent 侧 assistant 正文**前缀**注入锚点行，工具侧 `call_history` 沿用原列表引用。  
- [x] 低置信指代时的澄清策略（规格 §4.3）：**不纳入 V2**；欠债与 V3 排期见 **`task_chatbi_v3_debt_from_v2_multiturn_v1.md` §1**。

---

## B 实施方案细化（试行 / 分阶段）

> 目标：在 **不替代 DDL** 的前提下，把「口语 / 英文碎片 → 与库内 `WHERE` 字面量一致」的真值塞进 Text2SQL prompt，对齐规格 **§4 结构化上下文** 中与「列值域」相关的缺口类型说明。

### B.0 原则与优先级

1. **分阶段交付**：**PR1** 仅落地可版本化 YAML（或 JSON）+ prompt 注入，便于先闭环同义词与回归用例；**PR2** 起在 allowlist 上启用 DISTINCT 探针，与 YAML **合并**防漂移（见下条 **已选型**）。  
2. **与 DDL 边界**：字典块标题固定为「业务术语与库内取值」；**不声明 DDL 未出现的列**；仅约束 `WHERE` / `CASE` / `GROUP BY` 标签与枚举字面量一致。  
3. **注入顺序**：在 `build_sql_prompt` 中独立小节 **置于「近期对话（指代）」之前**较稳妥——先给列真值，再结合 `dialogue_context` 与 `text2sql_grounding` 消歧。  
4. **表级裁剪**：仅当「本轮检索到的 DDL 表名」与（可选）`text2sql_grounding.primary_table` 的交集中，字典里存在对应 `tables.<name>` 时，才注入该表的列块，控制 prompt 体积。  
5. **防漂移策略（已选型）**：当 `TEXT2SQL_DISTINCT_PROBE` 开启且某列在 allowlist 内时，**即使 YAML 已完整覆盖该列，仍执行** `SELECT DISTINCT ... LIMIT N`，将 **DISTINCT 结果与 YAML 的 `values` 做并集去重** 后再写入 prompt；**禁止默认行为**为「YAML 命中即短路、跳过 DISTINCT」。探针超时/失败/权限错误时 **降级为仅 YAML**（可用性优先）。若将来需省 I/O，可另增可选 env（如「短路节能模式」），**默认关闭**，与防漂移主策略区分。

### B.1 数据形态（建议）

- **路径**：例如 `docs/text2sql/v1/value_hints.yaml`（与现有 `docs/text2sql/v1/sql/` 并列，便于评审）；真名以 PR 为准，**实现后**在 `PROJECT_CONFIG` 增补一行说明。  
- **结构要点**：

  - 顶层 `version`（整数，便于破坏性格式升级）。  
  - `tables.<table>.<logical_key>`：`column`（必须与 DDL 中列名一致）、`values`（库内枚举真值列表）、`synonyms`（口语 → 真值映射；键可为「男性」「男的」「male」等）。  
  - 可选 `notes`：给人看的业务说明，**默认不注入 prompt**（避免干扰模型），仅文档用。

- **示例（示意，非最终数据）**：

```yaml
version: 1
tables:
  agent_info:
    gender:
      column: gender
      values: ["男", "女"]
      synonyms:
        男性: 男
        男的: 男
        female: 女
    commission_structure:
      column: commission_structure
      values: ["底薪加提成", "固定佣金"]
      synonyms:
        提成结构: 底薪加提成
```

### B.2 代码落点（与现栈对齐）

| 职责 | 建议 |
|------|------|
| 加载与缓存 | 新建 `api/text2sql_value_hints.py`：`load_hints(path) -> dict`；进程内 `functools.lru_cache` 或模块级「mtime 变更则重载」，避免每次请求读盘。 |
| Prompt 拼装 | `api/text2sql_core.py`：为 `build_sql_prompt` 增加可选参数 `value_hints_block`，在 `ctx_block` 前插入「【值域与口语映射】」固定说明 + 块正文。 |
| 调用方 | `api/tools.py`：`text2sql_execute` 在组 `dialogue_context` 之后、`build_sql_prompt` 之前：根据 env、检索结果中的 DDL 表名集合、以及已有 `text2sql_grounding`（若有）决定要注入的表/列，调用 `format_hints_for_prompt(...)`。 |
| 其它入口 | **已统一**：`unified_chat.py` / `chain_chat.py` / `text2sql_api.py` 均调用 `build_value_hints_block_for_text2sql`（无会话历史处传 `history=None`）；Agent 路径以 `tools.text2sql_execute` 为准并传入 `history`。 |

### B.3 环境变量（草案 → 落地后写入 PROJECT_CONFIG）

- `TEXT2SQL_VALUE_HINTS_PATH`：可选；未设置或文件不存在则 **跳过** 值域块（零行为变更）。  
- `TEXT2SQL_VALUE_HINTS_ENABLED`：`1` / `0`；默认建议：`path` 非空且文件存在则等效启用，否则关闭（减少双配置心智负担）。  

**Phase 2（PR2）** 引入 DISTINCT 相关（与 **B.0-5 / B.4** 防漂移合并策略一致）：

- `TEXT2SQL_DISTINCT_PROBE`（是否启用）、`TEXT2SQL_DISTINCT_MAX`（每列上限）、`TEXT2SQL_DISTINCT_COLUMNS`（allowlist，如 `public.agent_info.gender` 语法）——**不在 PR1 必达**；启用后默认 **YAML 不短路 DISTINCT**。

### B.4 DISTINCT 探针（Phase 2；与 YAML 关系：**防漂移合并**）

- 仅对 allowlist 列执行只读 `SELECT DISTINCT "col" FROM "schema"."table" LIMIT N`。  
- **与 YAML 的合并规则（防漂移）**：同一列的最终取值集合 = **`values` ∪ DISTINCT 结果**，去重、排序稳定（如字典序）；`synonyms` 仍只来自 YAML，指向并集中的**某一真值**。prompt 内保留说明：**「以下为库内采样与业务字典的合并；口语映射以同义词表为准」**，避免模型把 `LIMIT N` 的采样误当作闭集。  
- **不采用**：「YAML 已查到该列就不再调用 DISTINCT」作为默认路径（与 **B.0-5** 一致）。  
- **漂移文档**：任务验收项「字典或 DISTINCT 与真实库漂移时有文档说明」——在 `docs/text2sql/` 或本任务「实现备忘」说明：**库侧新枚举由 DISTINCT 进入并集；同义词仍靠 YAML/人工**；可选 CI 对 fixture 做告警（非强制）。

### B.5 测试与验收挂钩

- **单测**：新建 `tests/test_text2sql_value_hints.py`——对 `format_hints_for_prompt` / `build_sql_prompt` 做快照或子串断言：给定 YAML fixture，用户问「多少男性」时，**期望生成 SQL 中出现字典真值 `男`**（可与 `llm_generate_sql` mock 分层：先单测 prompt 含映射说明，再少量集成测）。  
- **数据真值**：以 `docs/text2sql/v1/sql/supabase_init.sql`（或约定测试库）中的枚举为准维护 YAML，避免「字典写了、库里没有」。  
- **回归**：现有 `pytest` Agent / grounding 用例不因 prompt 变长而 flaky；`temperature=0` 已有利于稳定。

### B.6 PR 拆分建议

| PR | 内容 | 风险 |
|----|------|------|
| **PR1** | YAML 样板 + loader + `build_sql_prompt` 注入 + `tools.text2sql_execute` 接线 + `test_text2sql_value_hints` | Low：默认关闭或 path 空则无 diff 行为。 |
| **PR2** | DISTINCT allowlist 探针 + env；**默认防漂移**：与 YAML 并集、不 YAML 短路；超时/失败降级仅 YAML + 漂移说明文档 | Medium：allowlist 内每列多一次只读 round-trip，需超时、并发上限与失败降级。 |

## 非范围

- 前端 Unified Chat `session_id` 传参与 Timeline UI（见前端任务单与 `_tech_graph`）。  
- Intent 模型选型与 60 条集准确率（见 **`docs/tasks/done/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`**）。  
- 修改 `SPEC-ChatBI-V2-Multiturn-Semantics.md` 正文（以规格为引用真值；任务单只跟踪实现）。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 多轮语义规格 | `docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md` |
| Agent 总规 §2.6 记忆 | `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` |
| Text2SQL 实现 | `api/tools.py`、`api/text2sql_core.py` |
| 会话记忆 | `api/agent_memory.py`、`api/agent.py`（`turn_history` / `call_history`） |
| 历史格式化复用 | `api/query_rewrite.py`（`history_to_rewrite_block`） |
| 样例 DDL/数据 | `docs/text2sql/v1/sql/supabase_init.sql` |

---

## 验收标准

### A（已实现，回归防回归）

- [x] 同一 `session_id` 下，首轮问「统计 agent_info 表有多少条」、次轮问「刚刚的表里多少男性」时，`text2sql` 路径的检索串或生成 prompt 中**能出现**首轮语境中的表名锚点（日志或 debug 可核对）。  
- [x] `pytest`：`tests/test_unified_chat_backend_v2_agent.py`、`tests/test_intent_cache.py` 等与 Agent 路径相关用例不因本次改动失败。

### B（PR1 + PR2 + 文档已闭合）

- [x] **PR1 自动化**：`tests/test_text2sql_value_hints.py` 断言 prompt 含性别/佣金 **库内取值与同义词映射**（不依赖外呼 LLM）。  
- [x] **集成 / 人工**：真库抽检示例：`gender = '保密'` 计数与库一致（Timeline `sql.result` / `WHERE` 字面量）；「男性 / commission 口语」等仍可按需加抽。  
- [x] **漂移说明**：`docs/text2sql/v1/VALUE_HINTS_DISTINCT.md`。

### C（已实现基线）

- [x] 自动化用例：`tests/test_text2sql_grounding.py`（表抽取、`tool_results` 块形状、`history_to_rewrite_block` 含 `[Text2SQL 锚点]`）。  
- [x] 无新 Supabase 列：沿用 `tool_results` JSONB；与 `supabase/sql/create_rag_conversation_logs.sql` 现结构一致。

---

## 实现备忘（子 Agent 回填）

| 项 | 内容 |
|----|------|
| **A 已涉及文件** | `api/tools.py`（`_text2sql_retrieve_query`、`text2sql_execute`）、`api/text2sql_core.py`（`build_sql_prompt(..., dialogue_context=)`）、`api/agent_memory.py`（`save` 缓存形状） |
| **A 新增 env** | `TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`（默认 `1200`，可选） |
| **C 已涉及文件** | `api/text2sql_grounding.py`（新建）、`api/unified_chat.py`（`_text2sql_grounding_from_agent_result` / 落库）、`api/agent_memory.py`（load 合并）、`api/query_rewrite.py`、`api/agent.py`、`tests/test_text2sql_grounding.py` |
| **B-PR1 已涉及文件** | `docs/text2sql/v1/value_hints.yaml`、`api/text2sql_value_hints.py`、`api/text2sql_core.py`（`value_hints_block`）、`api/tools.py`、`api/unified_chat.py`、`api/chain_chat.py`、`api/text2sql_api.py`、`tests/test_text2sql_value_hints.py`、`requirements.txt`（`pyyaml`） |  
| **B-PR1 新增 env** | `TEXT2SQL_VALUE_HINTS_PATH`、`TEXT2SQL_VALUE_HINTS_ENABLED`（真值表 §C） |  
| **B-PR2 已涉及文件** | `api/text2sql_value_hints.py`（`merge_hints_with_distinct_probes`、`parse_distinct_allowlist`、`run_distinct_probe_values`）、`api/text2sql_core.py`（`execute_select_sql(..., statement_timeout_ms=)`）、`api/tools.py`（`asyncio.to_thread` 构建 value hints）、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`、`.env.example`、`docs/text2sql/v1/VALUE_HINTS_DISTINCT.md`、`tests/test_text2sql_value_hints.py` |  
| **B-PR2 新增 env** | `TEXT2SQL_DISTINCT_PROBE`、`TEXT2SQL_DISTINCT_MAX`、`TEXT2SQL_DISTINCT_COLUMNS`、`TEXT2SQL_DISTINCT_MAX_PROBES`、`TEXT2SQL_DISTINCT_STMT_TIMEOUT_MS` |  
| **B 待拆 PR** | 无（PR2 已合入本仓）；可选后续：「YAML 命中短路 DISTINCT」节能模式（默认关，见任务 B.0-5） |
| **图谱** | 若流程变更跨请求锚点，同步 `_tech_graph/` 中 Text2SQL / Agent 子流程（遵守双轨与 Mermaid 协议）；**B-PR1 未改跨请求契约，图谱非强制，审核可选查** |

---

## 审核清单（供审核 Agent）

> 审核目标（2026-05-09 口径）：确认 **B-PR1** 与任务单 / `PROJECT_CONFIG` 一致。**B-PR2** 已于 2026-05-11 合入；复审时补充核对 DISTINCT env 与 `VALUE_HINTS_DISTINCT.md` 即可。

- [x] **代码与路径**：存在 `docs/text2sql/v1/value_hints.yaml`；存在 `api/text2sql_value_hints.py`；`build_sql_prompt` 含 `value_hints_block`，且块在「近期对话」**之前**（`text2sql_core.py`：`vh` 先于 `ctx_block` 追加）。  
- [x] **入口一致**：`tools.text2sql_execute` 与 `unified_chat` / `chain_chat` / `text2sql_api` 均通过 `build_value_hints_block_for_text2sql` 注入（Agent 路径带 `history` 以利 grounding 表裁剪）。  
- [x] **环境变量真值**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 已收录 `TEXT2SQL_VALUE_HINTS_PATH`、`TEXT2SQL_VALUE_HINTS_ENABLED`，且与代码读取逻辑一致（含「显式 `false` 关闭」语义）。  
- [x] **数据对齐**：YAML 中 `gender` / `commission_structure` 的 `values` 与 `supabase_init.sql` 样例数据中出现的取值一致（`commission_structure` 含库内字面量「提成结构」，与同义词表并存属已知产品语义点，见下条）。  
- [x] **测试**：`pytest tests/test_text2sql_value_hints.py tests/test_text2sql_grounding.py tests/test_unified_chat_backend_v2_agent.py tests/test_intent_cache.py` → **26 passed, 2 skipped**（skipped 为 L5 mock 暂缓，见 `docs/diary/L5-ChatBI-V2-FailureTypeHandler-pytest指南.md`）；PR2 后请复跑并含 `tests/test_supabase_http_retry.py`（以当前 CI 为准）。  
- [x] **已知缺口登记**：同义词「提成结构→底薪加提成」与库内字面量「提成结构」同名，产品若需区分须在后续迭代拆 `logical_key` 或改措辞；**B-PR2 DISTINCT** 已实现（默认关 env），漂移说明见 `docs/text2sql/v1/VALUE_HINTS_DISTINCT.md`。  
- [x] **结论（2026-05-09）**：**通过（B-PR1 + A/C 回归）**。**结论（2026-05-11 增补）**：B-PR2、集成抽检与漂移说明已闭合；任务单 **2026-05-11 归档** 至 `docs/tasks/done/`。

---

## 给 Cursor 的稳定关键词

多轮、Text2SQL、`dialogue_context`、`history_to_rewrite_block`、`_text2sql_retrieve_query`、`TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`、`AgentMemoryStore`、指代消解、枚举字典、DISTINCT、防漂移、并集、resolved_table、SQL 摘要、L3、SPEC-ChatBI-V2-Multiturn-Semantics、grounding
