# Text2SQL 场景留档（`docs/spec/v3-agent/text2sql/`）

> **用途**：Unified Chat + Agent 路径下 Text2SQL 的 **抓包 / Timeline 实录**、改进需求锚点，以及与 **权限 / 策略** 相关的 **执行结果** 对照说明。  
> **契约真值**：对外 SSE 键名仍以 `docs/_tech_graph/_contract_manifest.json` 为准。

---

## 目录索引

| 路径 | 说明 |
|------|------|
| [`1.md`](./1.md) | 长链路实录（含列名臆测问题 → 已驱动 **schema 预取** 任务） |
| [`2.md`](./2.md) | 另一轮 INSERT/UPDATE 实录（含子阶段耗时） |
| [`archive/`](./archive/) | **无权限**场景：修复前 / 预期迭代 / **验收终版**（见 [`archive/README.md`](./archive/README.md)） |

---

## 执行结果输出：有权限 vs 无权限（产品可读口径）

以下描述 **Agent + `text2sql_query`** 路径下，终态对用户与 Timeline **可见**的差异（不含密钥与完整 SQL 落库细节）。

### 有权限（策略允许 + SQL 通过闸门）

| 维度 | 典型表现 |
|------|----------|
| **`done.ok`** | 成功时为 `true`（或按现网错误模型为 `false` 但带明确业务失败原因） |
| **`tool.call.end`** | `success: true` 时常见 **`output`** 含结果摘要 / `sql.result` 链路等；失败时 `error` 为 DB/超时等业务错误（非「表级策略拒绝」话术） |
| **`text2sql.phase.*`** | `retrieve` → … → `db` / `llm_summary` 等阶段按实际执行出现；`tool.call.end.output.text2sql_phases_ms` 与 SSE 子阶段对齐 |
| **后续工具** | 若走 Agent 成功路径，可能出现 **`rag_search`** 等（与失败拒绝路径不同） |

### 无权限（表级策略 / 预取拒绝 / DB 权限）

| 维度 | 典型表现（与任务单 [`docs/tasks/done/task_chatbi_text2sql_denial_final_answer_no_respin_v1.md`](../../tasks/done/task_chatbi_text2sql_denial_final_answer_no_respin_v1.md) 一致） |
|------|----------|
| **`tools_used` / 工具链** | 仅 **`text2sql_query`**；**不**再调用 **`rag_search`** 作为拒绝后的绕路 |
| **`tool.call.end`** | `success: false`；`error` 为 **用户可读中文**（无权限 / 策略限制说明）；`error_code` 常为 **`CHATBI_SQL_WRITE_DENIED`**、**`SQL_EXEC_PERMISSION_DENIED`**、**`CHATBI_SQL_DENIED`** 之一 |
| **`assistant.message`（终态）** | 与工具 `error` 同源的可读说明；**不应**被泛化为仅「问题太复杂」而无权限语义 |
| **`text2sql.phase.*`** | 常见在 **`schema_prefetch`** 结束即失败返回（`latency_ms` 等仍按契约输出）；详见 [`archive/4-无权限用户-预期-终版.md`](./archive/4-无权限用户-预期-终版.md) |
| **`agent.llm`（总结流）** | 拒绝终态仍应出现与 **`assistant.message`** 对齐的 **模拟 `text2sql_summary`** 流（避免仅 `tool.call.end` 而无 LLM 帧的断裂感） |

**归档真值**：无权限完整 Timeline 与 JSON 片段以 **`archive/4-无权限用户-预期-终版.md`** 为准；修复前对照 **`archive/3-无权限用户-非预期.md`**。

---

## 给 Cursor

`text2sql`、`CHATBI_SQL_WRITE_DENIED`、`schema_prefetch`、`text2sql.phase.end`、`_contract_manifest`、`task_chatbi_text2sql_denial_final_answer_no_respin_v1`
