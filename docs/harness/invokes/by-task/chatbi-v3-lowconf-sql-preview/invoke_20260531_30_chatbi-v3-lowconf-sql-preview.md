# Invoke 快照 · 30 执行编码 · chatbi-v3-lowconf-sql-preview

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task_slug | chatbi-v3-lowconf-sql-preview |
| task_path | docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-sql-preview |
| freeze_id | CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31 |
| test_strategy | required |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演 Harness「执行编码帽」，严格遵循 30-execute-code.md、40-self-check.md、HARNESS_V2_PLAN §5。

输入：
- task：docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md
- worktree：ai-ink-brain-api-python（仓根）
- 审查：docs/harness/reviews/by-task/chatbi-v3-lowconf-sql-preview/task_chatbi_v3_lowconf_sql_preview_v1_audit_R1_20260531.md
- SPEC：docs/spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md
- VERIFY：pytest tests -m "not intent_eval and not intent_benchmark"

你必须完成：
1. §2 G1–G4：先红后绿 pytest（无效 token deny、SSE parity、预览失败、preview_only 断言）；非 api/ 大重构。
2. tech_graph_contract_check + 全量 pytest 绿。
3. 回填 task ### 自检结论（执行者）。
4. semi_auto → 40 invoke 落盘 + commit。

Judgment（30）：
- experience_capture: 维持 recommended；关账后可升 required（首条业务 KPI 链）
- gate/risk: 未代签 gate
- hat_self: pass
```
