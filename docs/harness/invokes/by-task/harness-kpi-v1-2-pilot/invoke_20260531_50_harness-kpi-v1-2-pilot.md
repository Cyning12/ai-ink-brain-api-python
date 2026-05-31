# Invoke 快照 · 50 独立复检 · harness-kpi-v1-2-pilot

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| task_slug | harness-kpi-v1-2-pilot |
| task_path | docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md |
| git_branch | KPI_RUBRIC_v1_2 |
| reinspect_mode | 独立复检 |
| fresh_context | **必须新会话** |
| date | 20260531 |

---

## §3 调用体（快照 · 新会话粘贴）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/guides/KPI_RUBRIC_v1_2.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

【Fresh Context · 禁止读 30 invoke 全文】

输入：
- task：docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md
- 子仓：ai-ink-brain-api-python
- 模式：独立复检
- diff：git diff main...KPI_RUBRIC_v1_2 -- docs/harness docs/tasks
- 审查：docs/harness/reviews/by-task/harness-kpi-v1-2-pilot/task_harness_kpi_v1_2_pilot_audit_R1_20260531.md

你必须完成：
0. 本 invoke 落盘 + commit。
1. 读 task ### 自检结论（执行者）；独立重跑 VERIFY。
2. 对 task §7 验收逐项 pass/fail + 证据。
3. 落盘 docs/tasks/reinspect_results/reinspect_harness-kpi-v1-2-pilot_20260531_v1.md。
4. 建议合并或阻塞清单；Judgment 必填。
5. 完成后提示用户：00/CLOSE 新会话汇总 ### KPI（00）+ CLOSE_TRACE；HG-REINSPECT 须人签 approved 再 merge。

Judgment（50 · 末尾）：
- experience_capture: …
- gate/risk: HG-REINSPECT pending
- hat_self: pass | pass-with-notes | blocked
```
