# invoke · 22 · Round T1 · kimi-harness-recentsync

| 字段 | 值 |
|------|-----|
| **task_slug** | `kimi_harness_pilot_recentsync_v1` |
| **round** | `T1` |
| **hat** | `22` |
| **date** | `2026-06-08` |
| **git_branch** | `task/kimi-harness-pilot-recentsync-v1` |
| **freeze_id** | `GOV-KIMI-HARNESS-PILOT@2026-06-06` |

## §3 Agent Prompt（全文内联）

```text
【角色】Harness 22 任务审核帽。遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/reviews/README.md

【canonical 读序】
1. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
2. docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md
3. docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md

【forbidden】
docs/spec/v3-agent/** · api/** · docs/diary/** · 改 task 正文（除非审查要求且非阻塞）

【你必须完成】
1. HG-TASK-DRAFT 须 approved，否则拒开工
2. 对照 explore：A/B 范围是否清晰；B 是否限 10 文件
3. failure_paths F1–F4 + Scenario ID 是否满足 task_validate
4. 落盘 R1 审查 md（AUDIT_ROUND=R1 · 结论：是否建议 30 开工）
5. **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
