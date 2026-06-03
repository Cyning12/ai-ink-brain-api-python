# Invoke 快照 · 00 总调度 · portfolio-rag-demo W5 关账 Loop

| 字段 | 值 |
|------|-----|
| hat_id | 00 |
| task_slug | portfolio-rag-demo |
| task_path | docs/tasks/active/task_portfolio_rag_demo_v1.md |
| git_branch | task/portfolio-rag-w5-v1 |
| freeze_id | PORTFOLIO-RAG-DEMO@2026-06-01 |
| semi_auto | true |
| audit_profile | post_close |
| kpi_rubric | KPI_RUBRIC_v1_2 |
| kpi_aggregator | CLOSE |
| date | 20260602 |

---

## §3 调用体（快照）

```text
## 角色

你是 **Harness 00 总调度 + 关账编排 Agent（Portfolio 后端 · W5 sync + 五问留证 + task 关账）** …

（全文见 docs/harness/prompts/PROMPT_00_looptask_close_portfolio_w5_backend_v1_zh.md §3 · 用户 2026-06-02 开帽粘贴体）

Open Folder = ai-ink-brain-api-python
git_branch = task/portfolio-rag-w5-v1
task_slug = portfolio-rag-demo
freeze_id = PORTFOLIO-RAG-DEMO@2026-06-01
semi_auto = true · audit_profile = post_close · kpi_aggregator = CLOSE

帽链：00 → 10 → 22(R1′) → 30 → 40 → 22(R2) → Task·50 → CLOSE
HG-W5-SYNC / HG-W5-FIVE-Q：pending（勿代填）
禁止：api/ · 生产 sync · 无 22 进 30
```
