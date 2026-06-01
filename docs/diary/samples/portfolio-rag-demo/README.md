# Portfolio RAG Demo · 五问预跑留证（W5）

> **task**：`docs/tasks/active/task_portfolio_rag_demo_v1.md`  
> **RUNBOOK**：[`docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../../../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §6  
> **状态**：**待人执行** sync + 五问后落盘（Agent **禁止**代跑生产 sync）

## 预期文件（留证清单）

| 文件 | 说明 |
| --- | --- |
| `sync-job-final.json` | admin/sync job 终态摘要（脱敏） |
| `q1-sources-run1.json` / `q1-sources-run2.json` | Q1 两次预跑 sources |
| `q5-sources-run1.json` / `q5-sources-run2.json` | Q5 两次预跑 sources |
| `five-questions-results.md` | 五问 pass/fail + 重试次数 + category 摘要 |
| `screenshots/` | 可选 · 录屏帧或 Unified Chat 截图 |

## 人工闸

- `HG-W5-SYNC`：sync `succeeded` 后人签  
- `HG-W5-FIVE-Q`：五问达标 + 本目录留证后人签

## 过程备忘（非 W5 留证）

| 文件 | 说明 |
| --- | --- |
| [`NOTES-ci-plan-token-test-fix_20260601.md`](NOTES-ci-plan-token-test-fix_20260601.md) | PR #101 CI：plan token 测试 base64 碰撞复盘 · commit `1823ba7` |
