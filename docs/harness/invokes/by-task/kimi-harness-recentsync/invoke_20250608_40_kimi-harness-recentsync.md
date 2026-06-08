# invoke · 40 · Round T1 · kimi-harness-recentsync

| 字段 | 值 |
|------|-----|
| **task_slug** | `kimi_harness_pilot_recentsync_v1` |
| **round** | `T1` |
| **hat** | `40` |
| **date** | `2026-06-08` |
| **git_branch** | `task/kimi-harness-pilot-recentsync-v1` |
| **freeze_id** | `GOV-KIMI-HARNESS-PILOT@2026-06-06` |

## §3 Agent Prompt（全文内联）

```text
【角色】Harness 40 自检帽。

【canonical 读序】
docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
docs/tasks/RECENT_TASK_SCHEDULE.md §1.2

【验证命令】
rg -n 'active/task_governance_docs_noise_line_manifest' docs/tasks/RECENT_TASK_SCHEDULE.md  # 期望无命中
rg -n '脚手架|P2/P3.*pending' docs/tasks/RECENT_TASK_SCHEDULE.md  # 期望无命中（§1.2 段）
# 不跑 pytest（not_applicable）

【你必须完成】
1. 逐条勾选 task 验收标准
2. 更新 task「### 自检结论（执行者）」含命令输出要点
3. 无阻塞 → 建议 CLOSE + PR
4. **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
