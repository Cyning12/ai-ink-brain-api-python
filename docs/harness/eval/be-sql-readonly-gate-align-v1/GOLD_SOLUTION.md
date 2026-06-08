# BE-1 Gold Solution（强基线对照）

| 项 | 内容 |
| --- | --- |
| **commit** | 见 `fix(text2sql): gold solution for BE-1` |
| **改动文件** | `api/text2sql_core.py` |
| **思路** | 引入 `sqlparse`，用 `_non_empty_sqlparse_statements` 对齐 `chatbi_sql_gate` 多语句判定；替换原 `s.count(";") > 1` 弱检查 |

## 核心 diff 摘要

- 新增 `_non_empty_sqlparse_statements(sql)`（与 gate 同名逻辑，仅只读路径使用）
- `validate_sql_readonly`：`len(stmts) > 1` → `ValueError`；**可选回退** `s.count(";") > 1`（Kimi Code 试跑解法，已合入 `task/moonshot-be1-r2`）

## 验证命令

```bash
./docs/harness/eval/be-sql-readonly-gate-align-v1/scripts/run_full_eval.sh
pytest tests/test_chatbi_sql_ast_gate_v1.py tests/test_chain_chat_events.py -q
```

## 非范围（故意未做）

- 块注释前缀 SELECT 与 AST gate 完全等价（`/* */ SELECT` 仍走前缀检查）
- 未改 `chatbi_sql_gate.py` 三阶段语义
