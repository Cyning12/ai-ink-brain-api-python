# Invoke 快照 · 40 自检 · harness-kpi-v1-2-pilot

| 字段 | 值 |
|------|-----|
| hat_id | 40 |
| task_slug | harness-kpi-v1-2-pilot |
| task_path | docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md |
| git_branch | KPI_RUBRIC_v1_2 |
| worktree_root | ai-ink-brain-api-python |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

上一帽已结束；本帽只按下文执行。

输入：
- task：docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md
- 子仓：ai-ink-brain-api-python
- Worktree：ai-ink-brain-api-python
- VERIFY：pytest tests -m "not intent_eval and not intent_benchmark"
- diff：git diff KPI_RUBRIC_v1_2 — docs/harness、docs/tasks

你必须完成：
1. 逐条对照 task §7 验收；跑 VERIFY + harness_task_validate + harness_human_gate_check（记录预期 FAIL 项）。
2. 回填 task ### 自检结论（执行者）含 OpenSpec×TDD 三维摘要。
3. 落盘 50 invoke（新会话 Fresh Context）+ commit。
4. 禁止粘贴 30 长文给 50。

Judgment（40 · 末尾）：
- experience_capture: 维持 required
- gate/risk: HG-REINSPECT pending → 50 后可关账预备，merge 仍须人签
- hat_self: pass
```
