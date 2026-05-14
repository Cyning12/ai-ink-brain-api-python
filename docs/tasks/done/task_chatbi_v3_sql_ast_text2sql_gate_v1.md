# Task：ChatBI V3 — Text2SQL 后闸 **SQL AST 硬化**（P1-1）

> **状态**：`done（2026-05-14 验收通过）`  
> **与总规批次对应**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§2.1 P1-1**  
> **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§2**（SQL 解析 / 策略 / 失败形态）  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` **§3.2.1**  
> **前置（已关单）**：`docs/tasks/done/task_chatbi_level_gate_v1.md`（**P1-3** 后闸顺序：**AST → 表白名单 → 档位策略** — 本单在 **不破坏** 该顺序前提下增强 **AST 真值**）  
> **test_strategy**：`required`  
> **test_strategy_note**：安全后闸语义须由 pytest **负例 / 正例 / 顺序**钉住；合并前须满足本仓 CI 默认命令（见 **§给执行帽的必读列表**）。合并 PR 中须可见：关键负例与 **顺序** 用例在实现前或同 PR 早期提交且可被 **`pytest` 失败复现**（与 `docs/harness/HARNESS_V2_PLAN.md` **§5.1** `required` 精神一致）。  
> **freeze_id**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§6 修订记录** 行 **`SPEC-SEC-2026-05-13-§2`** + 本单 **§4～§5**。契约变更后须同步升级本字段与 SPEC §6 新行。  
> **gates_before_code**：`["failure_paths", "freeze_id", "§给执行帽的必读列表"]`

---

## Harness（需求帽落盘）

### failure_paths

| ID | 触发条件 | 系统行为（须可测） | 可重试 | 用户可见类型 |
|----|-----------|-------------------|--------|----------------|
| FP-A | AST / 结构化规则命中（多语句、禁止 DDL/DML 形态等） | 抛出 **`ChatBiSqlGateDenied`**（或已约定子类）；HTTP **403**；body 含结构化 **`deny_code`**（与现网及 level_gate 一致）；`CHATBI_JSON_LOG=1` 时 **`sql_gate_deny`** 带 **`ast_rule_id`/`rule`**（与 §5 验收一致） | 否（同 SQL 文本不重试无意义） | 短拒绝文案（与现网一致，**不**回显完整 SQL） |
| FP-B | 解析失败或 AST 路径无法稳定分类（含恶意混淆语法） | **默认更严格**：按 **拒绝执行** 处理（与 §4 一致），语义与 FP-A 对齐或单独 `deny_code`；**禁止**静默放行到执行器。若 FP-B 使用 **单独 `deny_code`**，须在 **`_contract_manifest.json`**（若对外 body 适用）与 **pytest 负例** 中同时登记 | 否 | 与安全拒绝同类或「无法处理该查询」类短文案（执行 PR 在实现备忘 **锁死** 与 FP-A 是否共用 code） |
| FP-C | 配置/依赖异常（如 gate 内部未捕获错误） | HTTP **5xx**；**不**执行 SQL；日志可关联 `request_id`/`run_id` | 是（客户端可重试） | 通用服务器错误（无内部栈暴露） |

### 给执行帽的必读列表（开工前）

1. `docs/tasks/done/task_chatbi_level_gate_v1.md` — 后闸顺序与 **`deny_code`/`ChatBiSqlGateDenied`** 现行为。  
2. `api/chatbi_sql_gate.py` — 当前 normalize / classify / deny 日志字段。  
3. `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` **§2** + `docs/spec/v3-agent/SPEC-ChatBI-V3-Logging-Trace.md`（日志字段不与 OpenItems **§1.6** 冲突）。  
4. 合并前本地/CI：`pytest tests -m "not intent_eval and not intent_benchmark"`（与 `ai-ink-brain-api-python/.github/workflows/pytest.yml` 一致）。

### 文档对齐（子规 vs 代码）

| 观察 | 处理 |
|------|------|
| 对外失败字段命名 | **以 `SPEC-ChatBI-V3-Security.md` §2.2 + §6 行 `SPEC-SEC-2026-05-13-§2` + 代码 + level_gate 关单** 为真值；若再变更须同时改 SPEC §6、`freeze_id` 与 manifest（若适用）。 |

### 拒开工条件（执行帽）

- **`failure_paths`** 中 FP-A/FP-B 的 HTTP、`deny_code`、日志字段名未能在实现 PR 中 **同时**满足 §5 勾选与 pytest 断言说明。  
- 未读 **level_gate** 关单说明即改动 **`apply_chatbi_sql_gate`** 整体顺序或 `ChatBiPrincipal` 语义。

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

- [x] **负例集**：pytest 覆盖至少 **3** 类：**多语句**、**明确禁止的 DDL/DML 形态**、**绕过朴素前缀检测的等价恶意样例**（由实现 Agent 在 PR 中列出具体 SQL 片段标题）。  
- [x] **正例集**：至少 **2** 条「应通过」的 SELECT / 允许的 UPDATE（与 **L2 肖像表** 或 Admin 软删策略一致，fixture 可控）。  
- [x] **顺序断言**：**必须**以 **`tests/` 内 pytest**（或 CI 内等价的可失败断言）固定 **`apply_chatbi_sql_gate`** 检查顺序为 **AST → 表白名单 → access_level**；**不得**仅以注释替代。  
- [x] **`python -m pytest`**：本任务相关路径 **全绿**（在 PR 描述贴命令摘要）。  
- [x] **日志**：`CHATBI_JSON_LOG=1` 下，至少 **1** 条 AST 拒绝的 JSON 日志结构在 **`tests/`** 中断言（含 **`run_id`** 维度的关键字段）；**grep 样例**仅作 PR 说明附录。  
- [x] **子规**：`SPEC-ChatBI-V3-Security.md` **§2** 更新「现状 / 目标」一句，标明 **已合并 AST 硬化** 与 PR 链接（或修订记录表）。  
- [x] **图谱**：若流程边有变，增量 `docs/_tech_graph/` 中与 Text2SQL 后闸相关边（双轨 `.md` + `.ai.md` 按仓库协议）。

---

### 自检结论（执行者）

| 验收项 | 结论 | 证据 |
|--------|------|------|
| 负例 / 正例 / 顺序 / JSON 日志 | pass | `tests/test_chatbi_sql_ast_gate_v1.py`（本轮全仓 pytest 中 **7** 条该文件用例均绿） |
| 全仓 pytest（CI 对齐） | pass | 见下「验证命令」；摘要行 `121 passed, 2 deselected` |
| SPEC §2 / 图谱 | pass | 提交 `5e6cfdc` 含 `SPEC-ChatBI-V3-Security.md`、`docs/_tech_graph/11_flow_text2sql.md` / `.ai.md`；本帽以 **命令** 为主未二次 diff 审 SPEC 正文 |
| §5「`python -m pytest`」表述 | pass（等价） | 与 CI 真值同为 **pytest 入口**；本轮未再单独跑 `python -m` 前缀以免与下列命令重复耗时；若 PR 需字面截图可补跑一条 |
| `tools/tech_graph_contract_check.py` | **未跑（N/A）** | `git show 5e6cfdc --stat` **未**含 `_contract_manifest.json`；与 §3「仅当改 manifest」一致 |

**验证命令**（cwd 相对工作区根：`ai-ink-brain-api-python`）：

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
```

- **退出码**：`0`  
- **要点（原始日志摘录）**：`collected 123 items / 2 deselected / 121 selected`；**`=============== 121 passed, 2 deselected, 49 warnings in 37.85s ===============`**；`rootdir: .../ai-ink-brain-api-python`，`configfile: pytest.ini`。警告含 SWIG / supabase `timeout`·`verify` DeprecationWarning，**无失败**。  
- **可重试性**：全绿、非 flaky 迹象；失败时可重跑同命令（环境一致时预期稳定）。  
- **FP-B（文档对齐本 task 既有结论）**：解析不稳定统一 **`deny_code=CHATBI_SQL_DENIED`**、`rule=ast_parse_unstable`、**`ast_rule_id=AST_PARSE`**（与 FP-A 共用对外码；未新增 manifest 字段）。`conftest` 对 `CHATBI_V3_LOW_CONFIDENCE_CLARIFY` 的处理与既有 Intent 环境固定策略一致（见当次 pytest 全绿）。

**已知未测项**：未单独执行 `python -m pytest` 字面命令（与上列等价）；**FP-C** 5xx 专测未纳入本 task 验收表（与审查 R1 非阻塞建议一致）。

---

## 6. 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
|----|------|
| PR / 分支 | 已合入并通过本仓 CI；主线以远端 `agent-v3` / `main` 为准（2026-05-14 关单） |
| 选用库 / API | `sqlparse.parse` / `Statement.get_type()`；未新增第二套 parser 依赖 |
| 变更函数列表 | `apply_chatbi_sql_gate` 拆为 `_phase_ast`、`_phase_table_policy_allowlist`、`_phase_access_level_rules`；`normalize_single_sql` 多语句改由 AST；`_log_deny` / `ChatBiSqlGateDenied` 增 `ast_rule_id` |
| 新增 `rule` / `deny_code` 枚举 | `rule`：`ast_multi_statement`、`ast_forbidden_ddl`、`ast_parse_unstable`；`UNKNOWN` 非回退类用 `unsupported_stmt` + **`ast_rule_id=AST_UNSUPPORTED`**；对外 **`deny_code` 仍为 `CHATBI_SQL_DENIED`** |
| FP-B 若单独 `deny_code` | 与 FP-A **共用** `CHATBI_SQL_DENIED`；以 `rule` + `ast_rule_id` 区分 |
| 与 level_gate 差异说明 | 后闸顺序调整为 **AST → 表策略（min_*）→ 档位/L2**；`test_gate_l2_join_denied` 为两表均补 policy 行以钉死 JOIN 拒绝（原「先 JOIN 后策略」下无策略表会先 `no_policy_row`） |

---

## 7. 给 Cursor 的稳定关键词

`P1-1`、`chatbi_sql_gate`、`sqlparse`、`AST`、`CHATBI_SQL_DENIED`、`sql_gate_deny`、`apply_chatbi_sql_gate`、`Enterprise Gap` §3.2.1、`task_chatbi_v3_sql_ast_text2sql_gate_v1`、`test_strategy`、`failure_paths`、`freeze_id`、`拒开工`、`gates_before_code`、`SPEC-SEC-2026-05-13-§2`
