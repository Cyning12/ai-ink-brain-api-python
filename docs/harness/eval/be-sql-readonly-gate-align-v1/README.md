# BE-1 评测包 · `be-sql-readonly-gate-align-v1`

Round 2 可跑最小题包（Moonshot Mentor / coding engineer 造题）。

## 目录

```text
docs/harness/eval/be-sql-readonly-gate-align-v1/
├── TASK.md
├── AGENT_PROMPT.md         # 复制到新 Agent（---COPY START/END---）
├── HIDDEN_TESTS.md         # 评测机专用
├── CALIBRATION.md          # 试跑记录（含 Kimi Code 2026-06-08）
├── GOLD_SOLUTION.md        # 强基线对照（勿给解题 Agent）
├── scripts/                # 可选；需 commit ≥ f86a32a
└── tests/
    ├── test_public_validate_sql_readonly.py
    └── test_hidden_validate_sql_readonly.py
```

## 快速开始

### 出题 base

```bash
git checkout f86a32a
# 或：git worktree add ../ai-ink-brain-api-python-be1-eval f86a32a
```

### 解题 Agent

1. Open Folder = 本仓（worktree 亦可）
2. 复制 `AGENT_PROMPT.md` 中 COPY 块到新会话
3. 公开自测（**base 应 1 fail**，修复后 4/4）：

```bash
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_validate_sql_readonly.py -v
```

### 评测机 / 人审（关账）

```bash
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/ -v
```

期望 **11 passed**（公开 4 + 隐藏 7）。可选快捷脚本（主仓 `f86a32a+` 才有）：

```bash
./docs/harness/eval/be-sql-readonly-gate-align-v1/scripts/run_full_eval.sh
```

越界检查：

```bash
git diff --name-only
# 期望仅 api/text2sql_core.py（及 Agent 自增 tests 若 TASK 允许）
```

## 校准摘要（2026-06-08）

| 模型 | 全量 | 备注 |
| --- | --- | --- |
| Gold `2d3f75b` | 11/11 | sqlparse 多语句 |
| Kimi Code | 11/11 | worktree · sqlparse + 分号回退 |

详见 [`CALIBRATION.md`](./CALIBRATION.md)。

## 关联

- Round 1 骨架：`docs/harness/drafts/DRAFT_moonshot_造题骨架_后端_v1_zh.md` · BE-1
- 方法论：`docs/planning/月之暗面_全流程模拟/05b_造题方法论与例题集_v1_zh.md` §3
