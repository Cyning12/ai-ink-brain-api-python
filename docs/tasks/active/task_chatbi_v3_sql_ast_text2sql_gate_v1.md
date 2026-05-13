# Task：ChatBI V3 — Text2SQL 后闸 **SQL AST 硬化**（P1-1）

> **状态**：`todo`（**P1-1** implementation；可与 **P1-2**、**P1-4** 分 PR，但 **关单** 须满足本单 **§验收标准**）  
> **与总规批次对应**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§2.1 P1-1**  
> **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§2**（SQL 解析 / 策略 / 失败形态）  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` **§3.2.1**  
> **前置（已关单）**：`docs/tasks/done/task_chatbi_level_gate_v1.md`（**P1-3** 后闸顺序：**AST → 表白名单 → 档位策略** — 本单在 **不破坏** 该顺序前提下增强 **AST 真值**）

---

## 1. 背景与目标

当前 `api/chatbi_sql_gate.py` 已使用 **`sqlparse`** 做结构化辅助，但简历与总规仍要求将「仅靠关键字/前缀」的防护升级为 **可证明的 AST 级约束**（多语句、危险子句、方言边界等），并与 **`CHATBI_SQL_DENIED` / `sql_gate_deny` 日志** 对齐。

**完成态（初版）**：

1. **解析**：对 **normalize 后、执行前** 的 SQL 走 **AST 或 sqlparse 等价可证明路径**，能稳定识别至少：**多语句**、**禁止类 DDL**（与现 `_forbidden_ddl_dml` 语义对齐或收紧）、**与产品策略冲突的 DML 形态**（实现 PR 列清单）。  
2. **顺序**：与 **`task_chatbi_level_gate_v1`** 已拍板的后闸顺序一致；**新增**检查须插在 **表白名单 / access_level 策略** 之前或与现有一致（见 **§4** 实现备忘回填）。  
3. **失败**：仍抛 **`ChatBiSqlGateDenied`**（或统一子类），HTTP **403** + 结构化 `deny_code`；用户可见短文案与现网一致。  
4. **可观测**：`CHATBI_JSON_LOG=1` 时 **`sql_gate_deny`** 可区分 **「AST 规则 id」**（新增字段或 `rule` 命名约定，与 Logging 子规不冲突即可）。

---

## 2. 范围 / 非范围

- **范围**：`api/chatbi_sql_gate.py` 及其单测；必要时 **`api/tools.py` / `api/text2sql_core.py`** 仅在「传入 gate 的 SQL 形态」上配合；**`_contract_manifest.json`** 仅当对外错误 body 形状变化时同 PR。  
- **非范围**：替换 Postgres；**RLS 全集**；Intent 侧语义（归 **P1-4**）；Prompt 注入（归 **`task_chatbi_v3_prompt_injection_guard_poc_v1.md`**）。  
- **非范围**：重写 **前闸** schema 裁剪（`task_chatbi_level_gate` 已覆盖）；本单仅 **后闸 AST 层**。

---

## 3. 依赖与引用

| 项 | 路径 |
|----|------|
| 现网后闸真值 | `api/chatbi_sql_gate.py`（`normalize_single_sql`、`_classify_stmt`、`apply_chatbi_sql_gate` 等） |
| 主体与策略 | `api/chatbi_principal.py`、`api/chatbi_policies.py` |
| 日志 | `api/chatbi_json_log.py`、OpenItems **§1.6** |
| 契约门禁 | `python tools/tech_graph_contract_check.py`（仅当改 manifest） |

---

## 4. 与 P1-3 的衔接（硬约束）

- **不得**改变 **`ChatBiPrincipal` + `chatbi_sql_table_policy`** 的语义真值；仅增强 **SQL 文本 → 结构化判定** 路径。  
- **若** AST 检出与现有关键字路径结论不一致，以 **更严格** 为默认（安全优先），并在 **§实现备忘** 记录差异与迁移说明。

---

## 5. 验收标准

- [ ] **负例集**：pytest 覆盖至少 **3** 类：**多语句**、**明确禁止的 DDL/DML 形态**、**绕过朴素前缀检测的等价恶意样例**（由实现 Agent 在 PR 中列出具体 SQL 片段标题）。  
- [ ] **正例集**：至少 **2** 条「应通过」的 SELECT / 允许的 UPDATE（与 **L2 肖像表** 或 Admin 软删策略一致，fixture 可控）。  
- [ ] **顺序断言**：单测或注释说明 **`apply_chatbi_sql_gate`** 内检查顺序符合 **AST → 表白名单 → access_level**。  
- [ ] **`python -m pytest`**：本任务相关路径 **全绿**（在 PR 描述贴命令摘要）。  
- [ ] **日志**：`CHATBI_JSON_LOG=1` 下，至少 **1** 条 AST 拒绝可在 **`run_id`** 维度与 Unified 请求对齐（grep 样例或引用 RUNBOOK 写法）。  
- [ ] **子规**：`SPEC-ChatBI-V3-Security.md` **§2** 更新「现状 / 目标」一句，标明 **已合并 AST 硬化** 与 PR 链接（或修订记录表）。  
- [ ] **图谱**：若流程边有变，增量 `docs/_tech_graph/` 中与 Text2SQL 后闸相关边（双轨 `.md` + `.ai.md` 按仓库协议）。

---

## 6. 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
|----|------|
| PR / 分支 | |
| 选用库 / API | `sqlparse` 深化或补充；**禁止**在无评审下引入第二套完整 SQL parser 依赖，除非子规修订 |
| 变更函数列表 | |
| 新增 `rule` / `deny_code` 枚举 | |
| 与 level_gate 差异说明 | |

---

## 7. 给 Cursor 的稳定关键词

`P1-1`、`chatbi_sql_gate`、`sqlparse`、`AST`、`CHATBI_SQL_DENIED`、`sql_gate_deny`、`apply_chatbi_sql_gate`、`Enterprise Gap` §3.2.1、`task_chatbi_v3_sql_ast_text2sql_gate_v1`
