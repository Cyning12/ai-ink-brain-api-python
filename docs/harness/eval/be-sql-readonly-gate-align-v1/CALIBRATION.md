# BE-1 校准记录 · `be-sql-readonly-gate-align-v1`

> 小样本；**不外推** Moonshot / Kimi 产品指标。

## Base 状态（出题时 · `f86a32a`）

| 项 | 值 |
| --- | --- |
| eval 包 commit | `f86a32a` |
| 上游骨架时点 | `b6f97c6` |
| 公开测 | 3 pass / **1 fail**（`test_public_reject_multi_statement_single_semicolon`） |
| 隐藏测 | 3 pass / **4 fail**（3 变体 + chain_chat 集成） |
| 全量 | 6 pass / **5 fail** |
| 已知根因 | `validate_sql_readonly` 仅用 `s.count(";") > 1`，单分号双语句漏网 |

## 试跑记录

| 日期 | 模型档 | 公开 | 隐藏 | 全量 | 越界 | failure_cluster | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-08 | Gold（`2d3f75b`） | 4/4 | 7/7 | **11/11** | N | — | sqlparse 多语句；主仓 `run_full_eval.sh` |
| 2026-06-08 | **Kimi Code** | 4/4 | 7/7 | **11/11** | N | `AST_ALIGNED` | worktree · base `f86a32a`；sqlparse + 分号回退；仅 `api/text2sql_core.py`；回归 9/9 |
| | 中档 | | | | | | 待跑 |
| | 弱档 | | | | | | 待跑 |

## failure_cluster 枚举（E5 回流）

| cluster | 含义 | 题 vs 模型 |
| --- | --- | --- |
| `AST_ALIGNED` | sqlparse 多语句对齐 gate | 模型 OK |
| `AST_ALIGNED_WITH_FALLBACK` | 对齐 + 分号计数回退（Kimi 解法） | 模型 OK · 略宽于 gold |
| `AST_NOT_ALIGNED` | 只改分号计数，未用 sqlparse | 模型弱 |
| `OVER_COPY_GATE` | 复制整个 gate 导致 principal 路径异常 | 越界 / 模型弱 |
| `CALLER_BYPASS` | 改 chain_chat 绕过 core | 越界 |
| `REGRESSION_POSITIVE` | 合法 WITH/COMMENT SELECT 被误杀 | 题干歧义或实现 bug → 改题 |
| `TEST_TAMPER` | 删改评测测 | Constrain 失败 |

## E2 决策（2026-06-08 · Kimi 小样本 n=1）

```text
强模型（Kimi Code）公开 + 全量均 pass？
└─ 是 → 题干可执行、隐藏测有效；保留题，可送 RL（标签 AST_ALIGNED）
     └─ 待补：中/弱档试跑后再定通过率带
```

## 评测命令（worktree 无 scripts 时用）

```bash
# 公开（Agent）
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_validate_sql_readonly.py -v

# 全量（评测机）
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/ -v
```

## 修订

| 日期 | 说明 |
| --- | --- |
| 2026-06-07 | Round 2 初版 · 公开 4 + 隐藏 7 |
| 2026-06-07 | Gold solution · 全量 11/11 |
| 2026-06-08 | Kimi Code 试跑关账 · 11/11 · CALIBRATION 回填 |
