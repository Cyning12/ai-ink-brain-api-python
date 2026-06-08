# invoke · 30 · Round T1 · kimi-harness-recentsync

| 字段 | 值 |
|------|-----|
| **task_slug** | `kimi_harness_pilot_recentsync_v1` |
| **round** | `T1` |
| **hat** | `30` |
| **date** | `2026-06-08` |
| **git_branch** | `task/kimi-harness-pilot-recentsync-v1` |
| **freeze_id** | `GOV-KIMI-HARNESS-PILOT@2026-06-06` |

## §3 Agent Prompt（全文内联）

```text
【角色】Harness 30 执行帽（纯 docs · Kimi 试点）。遵循 task §范围 A/B。

【canonical 读序】
1. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
2. docs/harness/reviews/by-task/kimi-harness-recentsync/（R1 · 须无阻塞）
3. docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md

【forbidden】
git log · git blame · docs/spec/v3-agent/** · api/** · tests/** · .github/**
删除 docs/harness/invokes/** 或 reviews/** 历史
修改超过 10 个 done/ 文件（含 B-2 五文件）

【你必须完成】
**A（必做）** 更新 docs/tasks/RECENT_TASK_SCHEDULE.md §1.2：
- MANIFEST → done/ 路径
- P0–P3 done + PR 号
- 执行器：P0 Cursor · P1–P3 CC · 治理线 CLOSE
- 删过期「脚手架/pending/active MANIFEST」表述

**B（必做 B-2 + 可选 B-3）**：
- 统一 5 个 gov-docs-noise done task 状态行格式
- 若 explore 有合格候选且总数≤10：补 PR/日期；否则跳过并在 task 自检注明

**其它**：
- 回填 task「### 自检结论（执行者）」草稿
- **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
