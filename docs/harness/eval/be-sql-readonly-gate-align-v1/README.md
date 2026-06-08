# BE-1 评测包 · `be-sql-readonly-gate-align-v1`

Round 2 可跑最小题包（Moonshot Mentor / coding engineer 造题）。

## 目录

```text
docs/harness/eval/be-sql-readonly-gate-align-v1/
├── TASK.md                 # 给解题 Agent 的题干
├── AGENT_PROMPT.md         # 复制到新 Agent 会话的指令块
├── HIDDEN_TESTS.md         # 评测机 / 人审：隐藏测清单（不给解题 Agent）
├── CALIBRATION.md          # 校准记录表
├── README.md               # 本文件
├── scripts/
│   ├── run_public.sh       # 解题 Agent 自测
│   └── run_full_eval.sh    # 评测机全量（含隐藏测）
└── tests/
    ├── test_public_validate_sql_readonly.py
    └── test_hidden_validate_sql_readonly.py
```

## 快速开始

### 解题 Agent

1. Open Folder = `ai-ink-brain-api-python`
2. 阅读 `TASK.md`
3. 运行公开测（**当前 base 应失败**，修复后应全绿）：

```bash
./docs/harness/eval/be-sql-readonly-gate-align-v1/scripts/run_public.sh
```

### 评测机 / 人审

```bash
./docs/harness/eval/be-sql-readonly-gate-align-v1/scripts/run_full_eval.sh
```

越界检查（示例）：

```bash
git diff --name-only origin/main...HEAD
# 期望仅白名单路径
```

## 已知 base 缺口（出题时确认）

`validate_sql_readonly("SELECT 1; SELECT 2")` 在加固前 **不会** 抛错；`apply_chatbi_sql_gate` 同语句会 `ast_multi_statement` 拒绝。

## 关联

- Round 1 骨架：`docs/harness/drafts/DRAFT_moonshot_造题骨架_后端_v1_zh.md` · BE-1
- 方法论：`docs/planning/月之暗面_全流程模拟/05b_造题方法论与例题集_v1_zh.md` §3
