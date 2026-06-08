# BE-1 隐藏测清单（评测机 / 人审）

> **勿**放入解题 Agent 的 system prompt 或 `@` 引用。

| ID | 文件 | 用例 | 断言要点 |
| --- | --- | --- | --- |
| H1 | `test_hidden_validate_sql_readonly.py` | `test_hidden_multi_statement_variants` | 空白/换行变体的单分号双 SELECT 均 `ValueError` + `Multiple statements` |
| H2 | 同上 | `test_hidden_reject_drop_table` | 单条 DDL `DROP TABLE` → `Forbidden keyword` |
| H3 | 同上 | `test_hidden_reject_select_then_delete` | `SELECT; DELETE` → 拒绝（关键词或多语句） |
| H4 | 同上 | `test_hidden_reject_empty_sql` | 空串 → `Empty SQL` |
| H5 | 同上 | `test_hidden_chain_chat_rejects_multi_statement_sql` | `POST /api/py/chain/chat`：LLM 返回双语句时 `ok=false`，`tool.call.end` 带 `error`，**未** mock `validate_sql_readonly` |

## 硬门禁

- 隐藏测 5/5 通过
- 公开测 4/4 通过
- `git diff --name-only` 无禁止路径

## 防刷题（Round 2）

- 轮换表名：`agent_info` / `chatbi_user_portrait` / seed 后缀
- 定期替换 H1 参数化 SQL 变体（30%）

## 与公开测分工

| 类型 | 目的 |
| --- | --- |
| 公开 | 3 正例 + 1 主缺口负例（`SELECT 1; SELECT 2`） |
| 隐藏 | 变体、DDL、chain_chat 集成、空 SQL |
