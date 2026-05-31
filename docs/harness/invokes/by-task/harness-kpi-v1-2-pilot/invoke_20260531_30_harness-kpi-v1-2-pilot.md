# Invoke 快照 · 30 执行编码 · harness-kpi-v1-2-pilot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task_slug | harness-kpi-v1-2-pilot |
| task_path | docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md |
| git_branch | KPI_RUBRIC_v1_2 |
| worktree_root | ai-ink-brain-api-python |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

上一帽已结束；本帽只按下文执行。

输入：
- 主 task：docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md
- 子仓：ai-ink-brain-api-python
- Worktree：ai-ink-brain-api-python
- VERIFY：pytest tests -m "not intent_eval and not intent_benchmark"
- 审查：docs/harness/reviews/by-task/harness-kpi-v1-2-pilot/task_harness_kpi_v1_2_pilot_audit_R1_20260531.md
- SPEC：无

你必须完成：
1. 按 task §2 范围改 docs（README §1、HARNESS_V2_PLAN §5.7/§5.8、TASK_TEMPLATE 字段）。
2. 修正 task §失败路径 标题以通过 harness_task_validate（若 22 未做）。
3. 跑 VERIFY；摘要写入 task ### 自检结论（执行者）或由 40 回填。
4. 落盘 40 invoke + commit。
5. 禁止触达 api/、tests/、workflows。

Judgment（30 · 末尾）：
- experience_capture: 维持 required
- gate/risk: 无新增 pending 闸
- hat_self: pass
```
