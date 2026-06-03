# Portfolio RAG Demo · 五问预跑留证（W5）

> **task**：`docs/tasks/active/task_portfolio_rag_demo_v1.md`  
> **RUNBOOK**：[`docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../../../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §6  
> **状态**：**blocked · 待人执行** sync + 五问（Agent **禁止**代跑生产 sync）

## 留证路径（本地 vs 冻结）

| 阶段 | 目录 | 说明 |
| --- | --- | --- |
| **本地执行（默认）** | 仓库根 **`tmp/portfolio-rag-demo/`** | sync / 五问 curl / sources / 汇总表 **先落此处**（不纳入 Git） |
| **环境变量** | `PORTFOLIO_RAG_EVIDENCE_DIR` | 未设时默认 `<repo>/tmp/portfolio-rag-demo` |
| **本目录（冻结）** | `docs/diary/samples/portfolio-rag-demo/` | **HG-W5-SYNC / HG-W5-FIVE-Q 人签后**：从 tmp **脱敏复制** 下表文件再 commit |

```bash
export REPO_ROOT="$(git rev-parse --show-toplevel)"
export PORTFOLIO_RAG_EVIDENCE_DIR="${PORTFOLIO_RAG_EVIDENCE_DIR:-$REPO_ROOT/tmp/portfolio-rag-demo}"
mkdir -p "$PORTFOLIO_RAG_EVIDENCE_DIR"
```

## 预期文件（留证清单）

| 文件 | 说明 | 本地默认路径 | 冻结（本目录） |
| --- | --- | --- | --- |
| `sync-job-final.json` | admin/sync job 终态摘要（脱敏） | `$PORTFOLIO_RAG_EVIDENCE_DIR/` | 人签后复制 |
| `q1-sources-run1.json` / `q1-sources-run2.json` | Q1 两次预跑 sources | 同上 | 人签后复制 |
| `q5-sources-run1.json` / `q5-sources-run2.json` | Q5 两次预跑 sources | 同上 | 人签后复制 |
| `five-questions-results.md` | 五问 pass/fail + 重试 + category 摘要 | 同上 | 人签后复制 |
| `screenshots/` | 可选 · 录屏帧或 Unified Chat 截图 | 可选 · tmp 子目录 | 可选 |

## blocked 占位

- 待人步骤与 curl 索引：[`NOTES-w5-pending_20260602.md`](NOTES-w5-pending_20260602.md)
- 人完成留证并签闸前，**不得**宣称 W5 pass

## 人工闸

- `HG-W5-SYNC`：sync `succeeded` + §2.3 硬检查后人签（`docs/tasks/active/task_portfolio_rag_demo_v1.md`）
- `HG-W5-FIVE-Q`：五问达标 + 上表文件 **从 tmp 脱敏复制至本目录** 后人签

## 鉴权提醒

| 用途 | Token |
| --- | --- |
| admin/sync | `CHAT_API_SECRET` / BFF `SYNC_ADMIN_SECRET` |
| 五问 Unified Chat | ChatBI `chatbi_access_tokens` visitor Bearer（RUNBOOK §1.4） |
| 前端 unlock | `PORTFOLIO_VISITOR_*`（前端 W3 · 本目录不涉及） |

## 过程备忘（非 W5 留证）

| 文件 | 说明 |
| --- | --- |
| [`NOTES-ci-plan-token-test-fix_20260601.md`](NOTES-ci-plan-token-test-fix_20260601.md) | PR #101 CI：plan token 测试 base64 碰撞复盘 |
| [`NOTES-w5-pending_20260602.md`](NOTES-w5-pending_20260602.md) | W5 关账 Loop · 待人 sync/五问占位 |
