# BE-1 校准记录 · `be-sql-readonly-gate-align-v1`

> 小样本；**不外推** Moonshot / Kimi 产品指标。

## Base 状态（出题时）

| 项 | 值 |
| --- | --- |
| base commit | `b6f97c6`（Round 1 骨架时点；以实际 checkout 为准） |
| 公开测 | 3 pass / **1 fail**（`test_public_reject_multi_statement_single_semicolon`） |
| 隐藏测 | 0 pass / **5 fail**（含 chain_chat 集成） |
| 已知根因 | `validate_sql_readonly` 仅用 `s.count(";") > 1`，单分号双语句漏网 |

## 试跑记录（待填）

| 日期 | 模型档 | 公开 pass | 隐藏 pass | 越界 | failure_cluster | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| | 强基线 | | | | | |
| | 中档 | | | | | |
| | 弱档 | | | | | |

## failure_cluster 枚举（E5 回流）

| cluster | 含义 | 题 vs 模型 |
| --- | --- | --- |
| `AST_NOT_ALIGNED` | 只改分号计数，未用 sqlparse | 模型弱 |
| `OVER_COPY_GATE` | 复制整个 gate 导致 principal 路径异常 | 越界 / 模型弱 |
| `CALLER_BYPASS` | 改 chain_chat 绕过 core | 越界 |
| `REGRESSION_POSITIVE` | 合法 WITH/COMMENT SELECT 被误杀 | 题干歧义或实现 bug → 改题 |
| `TEST_TAMPER` | 删改评测测 | Constrain 失败 |

## E2 决策（通过率待跑后填）

```text
强模型公开测仍 fail？
├─ 是 → 检查 TASK 歧义 / 公开测过严
└─ 否 → 看 hidden 聚类 → AST_NOT_ALIGNED 为主则保留题送 RL
```

## 修订

| 日期 | 说明 |
| --- | --- |
| 2026-06-07 | Round 2 初版 · 公开 4 + 隐藏 5 |
| 2026-06-07 | Gold solution：`text2sql_core` sqlparse 多语句 · 全量 11/11 绿 |
