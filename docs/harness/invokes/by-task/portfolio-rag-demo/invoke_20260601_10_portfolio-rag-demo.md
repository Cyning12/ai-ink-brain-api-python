# Invoke 快照 · 10 需求 · portfolio-rag-demo

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| task_slug | portfolio-rag-demo |
| task_path | docs/tasks/active/task_portfolio_rag_demo_v1.md |
| git_branch | task/portfolio-rag-demo-v1 |
| freeze_id | PORTFOLIO-RAG-DEMO@2026-06-01 |
| date | 20260601 |
| sdd_status | 轮0+1+2 已完成，清单已人确认 |
| new_or_major_spec | 否 |

---

## §3 调用体（快照）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/harness/prompts/templates/TEMPLATE-requirements-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md §5

Open Folder = ai-ink-brain-api-python
git_branch = task/portfolio-rag-demo-v1

【目标与上下文】
冻结 SPEC `PORTFOLIO-RAG-DEMO@2026-06-01` 已 active。请从 `docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md` §7 工作包（W2 RUNBOOK · W3 env 文档 · W5 预跑留证）拆出本仓 **`docs/tasks/active/task_portfolio_rag_demo_v1.md`** 可执行 task 草案。硬 deadline：**2026-06-09** 投递前 ingest 对齐 + 五问 RUNBOOK + 预发/生产等价环境 sync 与五问预跑留证。**禁止**改 `api/`/`tests/` 业务实现（本帽仅 task）；**禁止**执行生产 `admin/sync`。

【已有材料路径】
docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md
docs/spec/governance/投递冲刺_20260609_v1_zh.md
ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md（配对前端 · 只读）
docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md

【审查回填】无
【SDD 状态】轮0+1+2 已完成，清单已人确认
【新建 SPEC】否

你必须完成：
0. Invoke 落盘 → docs/harness/invokes/by-task/portfolio-rag-demo/
1. 写 task 草案 → docs/tasks/active/task_portfolio_rag_demo_v1.md（含 freeze_id、failure_paths、test_strategy: recommended、semi_auto、audit_profile: post_close）
2. 输出下一棒 A（22 任务审核 R1 · 推荐）与 B（30 执行）**全文**，由人择一
3. 回复末尾 Harness 状态栏（版本 B）
4. 用户未说「不要 commit」时，落盘 task + invoke 后 commit

【人择路径】下一棒已选 A（22 任务审核 R1）；与前端 portfolio task 审查节奏对齐。
```
