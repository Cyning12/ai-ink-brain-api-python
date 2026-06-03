# Portfolio RAG Demo · 五问预跑留证（W5）

> **task**：`docs/tasks/done/task_portfolio_rag_demo_v1.md`  
> **RUNBOOK**：[`docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../../../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) §6  
> **状态**：**sync 已签** · **五问 Tranche 1 部分落盘** · `HG-W5-FIVE-Q` pending · 补录见 [`w5-retest-backlog.md`](./w5-retest-backlog.md)

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
| `sync-job-final.json` | admin/sync job 终态摘要（脱敏） | `$PORTFOLIO_RAG_EVIDENCE_DIR/` | ✅ **已冻结** · [`sync-job-final.json`](./sync-job-final.json) |
| `sync-job-summary.md` | sync 人签摘要 | 同上 | ✅ **已冻结** · [`sync-job-summary.md`](./sync-job-summary.md) |
| `q1-sources-run1.json` / `q1-sources-run2.json` | Q1 两次预跑 sources | 同上 | 人签后复制 |
| `q5-sources-run1.json` / `q5-sources-run2.json` | Q5 两次预跑 sources | 同上 | 人签后复制 |
| `five-questions-results.md` | 五问 pass/fail 主表（Tranche 1 部分） | tmp 或本目录 | ✅ **Tranche 1** |
| `w5-acceptance-tranche1_20260603.md` | 已通过项索引 | — | ✅ |
| `w5-retest-backlog.md` | **补录清单 P0/P1** | — | ✅ |
| `q1-sources-run1.json` | Q1 sources run1（UI 导出） | — | ✅ |
| `q4-sources-run1.json` | Q4 sources run1 | — | ✅ |
| `q5-sources-run1.json` | Q5 sources run1（清 diary 后） | UI Timeline | ⚠️ **partial · 主 evidence · 答缺 1/9** |
| `screenshots/q5-evidence-card-run1-execution-trace-20260603.png` | Q5 run1 执行链路（PASS · evidence-card） | UI 导出 | ✅ |
| `screenshots/q5-on-demand-image-run1-execution-trace-20260603.png` | Q5 run1 执行链路（旧 · partial · 99cecd45） | UI 导出 | 归档 |
| `screenshots/q2-hybrid-rag-success-execution-trace-20260603.png` | Q2 成功 · 执行链路截图（**另开对话** · run `50f48bd8…`） | UI 导出 | ✅ **Tranche 2 R1** |
| `q2-sources-run1.json` | Q2 sources run1 | UI Timeline | ✅ **Tranche 2 R1** |
| `q3-sources-run1.json` | Q3 sources run1 | UI Timeline | ✅ **Tranche 2 R2** |
| `screenshots/q3-cold-warm-hot-execution-trace-20260603.png` | Q3 成功 · 执行链路 | UI 导出 | ✅ **Tranche 2 R2** |
| `screenshots/` | 其他录屏帧或 Unified Chat 截图 | 可选 · tmp 子目录 | 按需 |

## blocked 占位

- 待人步骤与 curl 索引：[`NOTES-w5-pending_20260602.md`](NOTES-w5-pending_20260602.md)
- 人完成 **五问** 留证并签 `HG-W5-FIVE-Q` 前，**不得**宣称 W5 全 pass

## 人工闸

| gate | 条件 | 状态 |
| --- | --- | --- |
| **HG-W5-SYNC** | sync `succeeded` + §2.4 硬检查 | ✅ **approved** · 2026-06-03 · job `c44158a5-…` |
| **HG-W5-FIVE-Q** | 五问达标 + 五问文件从 tmp 脱敏复制 | **pending** |

## 鉴权提醒

| 用途 | Token |
| --- | --- |
| admin/sync | **`SYNC_ADMIN_SECRET`** / BFF Cookie（RUNBOOK §2 路径 B） |
| 五问 Unified Chat | ChatBI `chatbi_access_tokens` visitor Bearer（RUNBOOK §1.4） |
| 前端 unlock | `PORTFOLIO_VISITOR_*`（前端 W3 · 本目录不涉及） |

## 过程备忘（非 W5 留证）

| 文件 | 说明 |
| --- | --- |
| [`NOTES-ci-plan-token-test-fix_20260601.md`](NOTES-ci-plan-token-test-fix_20260601.md) | PR #101 CI：plan token 测试 base64 碰撞复盘 |
| [`NOTES-w5-pending_20260602.md`](NOTES-w5-pending_20260602.md) | W5 关账 Loop · 待人 sync/五问占位 |
