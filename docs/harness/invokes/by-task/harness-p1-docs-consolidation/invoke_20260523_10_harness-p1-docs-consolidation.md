# Invoke Snapshot · 10-requirements · harness-p1-docs-consolidation

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| hat_name | requirements |
| task_slug | harness-p1-docs-consolidation |
| task_path | `docs/tasks/active/task_harness_p1_docs_consolidation_v1.md` |
| git_branch | `task/harness-p1-docs-consolidation` |
| semi_auto | `true`（按本轮目标拟定） |
| generated_at | 2026-05-23 |
| source | 用户本轮消息全文快照 |

## Snapshot

```text
你正在扮演本仓 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/templates/TEMPLATE-requirements-invoke.md §3

【目标与上下文】
Harness P1 文档巩固（排期 RECENT_TASK_SCHEDULE §0.4）：在本仓合并交付 P1-3 + P1-2，一个 task、一个 PR。
- 分支已建：task/harness-p1-docs-consolidation（禁止在 main 上提交）
- P1-3（先做）：在 docs/tasks/README.md 增补 human_gate 场景速查表（gate_id / status / blocks_hats / 典型场景 / 谁改 approved）
- P1-2（后做）：新建 docs/tasks/skills/ + README.md，定义 6 类 SKILL（关账蒸馏 + 人审口径；类型清单以 docs/diary/2026-05-22-harness-evaluation-improvement-response.md §九 与 HARNESS_V2 §5 为准，矛盾须单列）
- 10 帽须：若 active/task_harness_p1_docs_consolidation_v1.md 不存在，按 docs/tasks/templates/TASK_TEMPLATE.md 创建并写入 Harness 元信息（建议：test_strategy=not_applicable + note；audit_profile=post_close；semi_auto=true；git_branch=task/harness-p1-docs-consolidation；human_gate 含 HG-TASK-DRAFT pending→你写完后我人扫改 approved；HG-REINSPECT 可选 pending blocks done）
- 执行顺序写在 task 内：P1-3 → P1-2
- 非范围：P1-1 工作区 Projects/docs/harness/reviews/ pointer；任何 api/ 代码与 CI workflow 变更；Ink 前端 Harness parity（P1-4）

【已有材料路径或粘贴说明】
docs/tasks/RECENT_TASK_SCHEDULE.md
docs/tasks/templates/TASK_TEMPLATE.md
docs/tasks/README.md
docs/harness/HARNESS_V2_PLAN.md
docs/harness/ACCEPTANCE_LANDING.md
docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
docs/harness/prompts/hats/10-requirements.md

【是否按任务审核文档回填】
无

你必须完成：
0. Invoke 快照：将本消息全文落盘 docs/harness/invokes/by-task/harness-p1-docs-consolidation/invoke_20260523_10_harness-p1-docs-consolidation.md（含元数据表），再开始实质输出。
1. 创建/更新 docs/tasks/active/task_harness_p1_docs_consolidation_v1.md（含验收标准、failure_paths、必读列表、给执行帽的执行顺序 P1-3→P1-2）。
2. 输出结构化分析块；矛盾单独小节（若有）。
3. 下一棒须输出两条全文 Prompt（人择一）：
   - 路径 A：22 任务审核 R1
   - 路径 B：30 执行（跳过 22）（推荐：纯 docs、排期已扫、无 API/表变更）
4. 回复末尾输出 HANDOFF_SEMI_AUTO §3.4 版本 B 状态栏；不得代填 human_gate approved。
5. 按 HANDOFF_AUTO_COMMIT 在 task/harness-p1-docs-consolidation 分支 commit 本轮路径（invoke + task）。
```
