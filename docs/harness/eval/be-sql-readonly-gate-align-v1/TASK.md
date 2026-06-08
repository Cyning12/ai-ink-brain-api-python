# TASK · be-sql-readonly-gate-align-v1

| 项 | 内容 |
| --- | --- |
| **task_id** | `be-sql-readonly-gate-align-v1` |
| **轨道** | A · Coding |
| **技能** | `READ_LEGACY` `TEST_DISCIPLINE` `BOUNDARY` |
| **难度** | L2 |
| **base** | 当前分支 checkout 点（见 `README.md`） |

---

## 背景

本仓 Text2SQL 存在 **双轨 SQL 校验**：

| 路径 | 校验函数 | 能力 |
| --- | --- | --- |
| ChatBI 主路径（有 `principal`） | `apply_chatbi_sql_gate` | sqlparse AST：多语句、DDL 顶语句等 |
| Legacy / 无 principal | `validate_sql_readonly` | 前缀 + 关键词 + **分号计数** |

`tests/test_chatbi_sql_ast_gate_v1.py` 已证明 `SELECT 1; SELECT 2`（**仅一个分号**）会被 AST 闸以 `ast_multi_statement` 拒绝；但 `validate_sql_readonly` 仍可能放行并继续执行。

调用 `validate_sql_readonly` 的入口包括：

- `api/chain_chat.py::handle_chain_chat`
- `api/tools.py::text2sql_execute`（`get_chatbi_principal()` 为 `None` 时）
- `api/text2sql_api.py`
- `api/text2sql_value_hints.py`

---

## 目标

加固 `api/text2sql_core.py::validate_sql_readonly`，使其与 `apply_chatbi_sql_gate` 的 **AST 多语句规则** 对齐：单分号双语句（如 `SELECT 1; SELECT 2`）必须拒绝。

验收时 **公开测全绿**；评测机另跑隐藏测（你本地不可见）。

---

## 允许修改

| 路径 | 说明 |
| --- | --- |
| `api/text2sql_core.py` | **主改点**：`validate_sql_readonly` |
| `tests/test_*sql*.py` | 可增补（非必须） |
| `docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_*.py` | 仅当需修正明显题面错误 |

## 禁止修改

- `api/chatbi_sql_gate.py` 内 **三阶段 gate 语义**（表策略、access_level、L2 portrait UPDATE 等）
- `api/index.py` 路由注册
- `supabase/`、`.github/workflows/`
- `docs/_tech_graph/` 拓扑真值
- 新增 `requirements.txt` / `pyproject.toml` 依赖（`sqlparse` 已在仓内使用）

## 实现提示（非唯一解）

1. 先读 `api/chatbi_sql_gate.py::_phase_ast` 与 `_non_empty_sqlparse_statements`，理解 AST 多语句判定。
2. 在 `validate_sql_readonly` 中增加 **sqlparse 非空语句计数**；`len(stmts) > 1` 时抛 `ValueError("Multiple statements are not allowed")`（与现有文案保持一致）。
3. **优先** 提取可复用的轻量 helper（放在 `text2sql_core.py` 或从 gate **只读复用** 解析函数），**禁止** 复制粘贴整个 `apply_chatbi_sql_gate`。
4. 保持现有 **已通过** 的公开正例行为：合法 `WITH … SELECT`、单条 `SELECT …`、尾部分号单语句仍应通过（块注释前缀 SELECT 与 AST gate 完全等价属 **非本题** 范围）。
5. 不必改 `chain_chat` / `tools` 调用点——加固 core 函数即可覆盖全路径。

---

## 本地自测（公开测）

在仓库根目录执行：

```bash
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_validate_sql_readonly.py -v
```

通过后再跑回归（推荐）：

```bash
pytest tests/test_chatbi_sql_ast_gate_v1.py tests/test_chain_chat_events.py -v
```

---

## 验收标准

- [ ] 公开 pytest 全绿
- [ ] `git diff --name-only` 未触及禁止路径
- [ ] 未引入新 pip 依赖
- [ ] 隐藏测由评测机判定（见 `HIDDEN_TESTS.md`，执行 Agent 不可见）

---

## 禁止项（越界即 0 分）

- 删除或弱化 `test_chatbi_sql_ast_gate_v1.py` 既有用例
- 在 `validate_sql_readonly` 中直接 `return sql_raw` 绕过校验
- 修改 `apply_chatbi_sql_gate` 业务规则以「凑过」公开测
