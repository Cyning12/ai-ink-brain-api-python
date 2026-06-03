# W5 复测 / P1 backlog · 维护者决策

| 项 | 值 |
| --- | --- |
| **task** | `docs/tasks/done/task_portfolio_rag_demo_v1.md` |
| **RUNBOOK** | `docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md` |
| **更新** | 2026-06-03 · 维护者 P1 签收 |

## R 系列（五问 / 交叉验证）

| ID | 项 | 状态 | 说明 |
| --- | --- | --- | --- |
| R1 | Q1 双跑 | ✅ | `q1-sources-run{1,2}.json` |
| R2 | Q2 RAG 成功（非纯降级） | ✅ | `q2-sources-run1.json` |
| R3 | Q3 evidence-only | ✅ | `q3-sources-run1.json` |
| R4 | Q4 resume | ✅ | `q4-sources-run1.json` |
| R5 | Q5 evidence-card + 双跑 | ✅ | `q5-sources-run{1,2}.json` |
| R6 | `five-questions-results.md` 汇总对齐 | ✅ | 2026-06-03 修正 Q5 行 |
| R7 | 后端 stream curl 与 UI 交叉 | ✅ **已结束** | **P1-1**：维护者确认结束；curl 非 FIVE-Q 硬门槛 |

## P1 可选项（维护者 2026-06-03）

| ID | 项 | 决策 | 后续 |
| --- | --- | --- | --- |
| **P1-1** | R7 stream curl | **已结束** | 不阻塞 `HG-W5-FIVE-Q` |
| **P1-2** | `resume/cv-online.md` 真简历 | **defer** | 维护者：**此前亦无真简历** · 真稿就绪后再 sync（不阻塞 W5 签收） |
| **P1-3** | Supabase 内 `diary/` chunk 噪音 | **保留** | 维护者接受 rank 噪音 · **不**清库 |
| **P1-4** | 跨仓 commit（`evidence-card.md` · sync 脚本 vol3） | **前端 Agent** | 见 `ai-ink-brain` · `PROMPT_looptask_close_portfolio_w6_v1_zh.md` · 分支 `task/portfolio-e2e-demo-qa-v1` |

## 关账门禁（不变）

- **HG-W5-FIVE-Q**：UI 五问 5/5 + 本目录留证 → **人签** `task` · `human_gate`
- **HG-REINSPECT**：50 后 · 合并 PR 前
- P1 全部为 **recommended / defer**，**不**抬升为 FIVE-Q 阻塞
