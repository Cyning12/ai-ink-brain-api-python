# invoke · explore · Round T1 · kimi-harness-recentsync

| 字段 | 值 |
|------|-----|
| **task_slug** | `kimi_harness_pilot_recentsync_v1` |
| **round** | `T1` |
| **hat** | `explore` |
| **date** | `2026-06-08` |
| **git_branch** | `task/kimi-harness-pilot-recentsync-v1` |
| **freeze_id** | `GOV-KIMI-HARNESS-PILOT@2026-06-06` |

## §3 Agent Prompt（全文内联）

```text
【角色】Harness explore · Kimi 试点 A+B · 只读差分；不改 RECENT/done 正文。

【canonical 读序 · 必须按序打开】
1. AGENTS.md §必读
2. docs/_tech_graph/00_main.md
3. docs/tasks/RECENT_TASK_SCHEDULE.md §1.2 全文
4. docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md §子批状态
5. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md §范围 A/B

【须核对】
- RECENT §1.2 vs MANIFEST：MANIFEST 路径是否仍写 active/；P1/P2/P3 状态是否过期
- 5 个 gov-docs-noise done task 文首 **状态** 行格式是否一致、是否含 PR 号
- 用 rg 扫描 docs/tasks/done/ 中 **状态** 行缺 PR 或缺日期的候选（列出路径，上限 15 条供 22/30 选用）

【forbidden】
docs/spec/v3-agent/** · api/** · tests/** · .github/**
docs/diary/** · docs/harness/invokes/by-task/**（除本交付物）
git log · git blame · 改任何业务文件

【你必须完成】
1. **A 段**：RECENT §1.2 现状 vs 期望（引用行号）
2. **B 段**：5 文件状态行对照表 + rg 候选清单（标注建议修/跳过）
3. 落盘 explore 报告（Summary / A / B / Blockers / 30 帽改动清单）
4. **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```
