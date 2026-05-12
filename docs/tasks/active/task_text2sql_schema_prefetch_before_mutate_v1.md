# Task：Text2SQL — 变更类 SQL 前强制表结构预取（防臆造列名）

> **状态**：`done`  
> **关联实录**：`docs/spec/v3-agent/text2sql/1.md`（`tool.call.end` 报错：`column "id" of relation "agent_info" does not exist`，INSERT 列名与真实表结构不一致）  
> **关联实现入口**：`api/tools.py::text2sql_execute`、`api/text2sql_core.py::build_sql_prompt`、`api/text2sql_store.py`（检索 DDL）、`api/unified_chat.py`（非 Agent 路径若仍调 Text2SQL 需对齐）  
> **关联图谱**：`docs/_tech_graph/11_flow_text2sql.md` / `.ai.md`（流程增加「结构预取」分支后须双轨更新）  
> **真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（若新增 env / 工具名须回填）

---

## 1. 背景与问题

当前 Text2SQL 管线在 **`retrieve` → `build_sql_prompt`** 中，将向量检索到的 **`doc_type == ddl`** 片段拼成「可用表结构(DDL)」。当检索结果 **未覆盖目标表**、或 **DDL 片段过短/缺列** 时，模型仍可能输出 **`INSERT`/`UPDATE`** 并 **臆造列名**（如本实录中 `agent_info` 使用不存在的 `id` 等），执行阶段在 Postgres 报错。

**产品要求**：在 **意图为写入或更新**（或模型计划输出非只读语句）且 **当前 prompt 中对该表的 DDL 证据不足** 时，应 **先主动读取真实表结构**（如 `information_schema` / 已封装的只读 `pg_catalog` 查询 / 与现有 ingest 同源的字典），再进入 SQL 生成；**禁止**在无表结构锚点的情况下「猜列名」生成变更类 SQL。

---

## 2. 目标（完成态）

1. **可判定**：在 `llm_generate_sql` 之前，能判定「目标表集合」及「是否已有足够 DDL 列信息」（规则见 §4）。  
2. **可补全**：若不足，执行 **一次或有限次** 只读元数据拉取（带超时与行数上限），将结果 **注入** `build_sql_prompt` 的 DDL 区块（或等价独立区块「系统拉取的表结构」）。  
3. **可观测**：SSE / JSON 日志中可区分「检索命中 DDL」与「预取补全 DDL」（便于验收与排障）。  
4. **安全**：预取查询本身须走 **只读连接** / 白名单语句形态，与 `CHATBI_SQL_DENIED`、等级闸门一致；**不**扩大 mutating 执行面。

---

## 3. 范围 / 非范围

**范围**

- Unified Agent 路径下 **`text2sql_query` / `text2sql_execute`** 等与 INSERT/UPDATE 相关的生成前补全。  
- 与 `filter_text2sql_retrieved`、ChatBI 表策略的 **可见表集合** 对齐（仅对 **策略允许且意图涉及的表** 预取）。

**非范围**

- 不替代向量检索主路径；预取为 **兜底/补全**。  
- 不在本任务内重做整库 schema 同步管线（若需离线全量字典另开任务）。  
- 不在本任务内放宽 ChatBI 写闸门规则。

---

## 4. 依赖与设计要点（供实现 Agent 细化）

| 项 | 说明 |
|----|------|
| 触发条件 | 例：`sql_kind` 预判为 `insert`/`update` **或** Router 标记写入意图；且 **目标表在 prompt 的 DDL 块中缺列清单** / 检索 ddl 为空 |
| 元数据来源 | 优先复用仓库内已有只读 introspection（若有）；否则新增受限查询模板（仅 `information_schema.columns` + `table_schema='public'` + 表名 IN …） |
| Prompt 契约 | `build_sql_prompt` 增加明确段落：「以下列名来自系统预取，须逐列使用」；保留原有「不要编造字段」约束 |
| 失败策略 | 预取失败 → 返回结构化错误 / `agent.clarify`，**不**继续让模型盲写 INSERT |

---

## 5. 验收标准

- [x] 复现类场景：在 **故意弱化 DDL 检索** 的集成/单测中，触发预取后生成的 INSERT **列名与真实表一致** 或通过闸门拒绝。  
- [x] 仅 SELECT 的短路径 **不** 无故增加高成本预取（或可被 env 关闭）。  
- [x] 预取 SQL **只读**，经现有安全审计习惯自检（或补单测断言 SQL 形态）。  
- [x] `python -m pytest` 相关子集通过；`_tech_graph` 流程图与任务状态同步更新。

---

## 6. 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/text2sql_schema_prefetch.py`（新）、`api/text2sql_core.py`（`build_sql_prompt`）、`api/tools.py`（`text2sql_execute`）、`api/unified_chat.py`（JSON + SSE）、`tests/test_text2sql_schema_prefetch.py`、`docs/_tech_graph/11_flow_text2sql.md` / `.ai.md` |
| 新增 env（若有） | `TEXT2SQL_SCHEMA_PREFETCH`（`0`/`1`，未设则随 `TEXT2SQL_DATABASE_URL`）、`TEXT2SQL_SCHEMA_PREFETCH_TIMEOUT_MS`、`TEXT2SQL_SCHEMA_PREFETCH_MAX_ROWS` |
| 图谱变更路径 | `docs/_tech_graph/11_flow_text2sql.md` §V3 P0-3、`11_flow_text2sql.ai.md` 增加 `PF` 节点 |

---

## 7. 给 Cursor 的稳定关键词

`Text2SQL`、`schema`、`information_schema`、`DDL`、`INSERT`、`预取`、`text2sql_execute`、`build_sql_prompt`、`臆造列名`
