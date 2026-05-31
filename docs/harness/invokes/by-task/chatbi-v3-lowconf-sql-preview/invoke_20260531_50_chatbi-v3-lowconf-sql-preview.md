# Invoke 快照 · 50 独立复检 · chatbi-v3-lowconf-sql-preview

| 字段 | 值 |
|------|-----|
| hat_id | 50 |
| task_slug | chatbi-v3-lowconf-sql-preview |
| task_path | docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-sql-preview |
| freeze_id | CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31 |
| reinspect_mode | 独立复检 |
| fresh_context | **必须新会话** |
| date | 20260531 |

---

## §3 调用体（快照 · 新会话粘贴）

```text
你正在扮演 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/templates/TEMPLATE-independent-reinspect-invoke.md §3
- docs/harness/guides/KPI_RUBRIC_v1_2.md

【Fresh Context · 硬】新对话开帽；禁止读 30 invoke 全文；必读 task + §10 自检 + 本分支 diff。

输入：
- task：docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md
- 子仓：ai-ink-brain-api-python
- 模式：独立复检
- diff：git diff origin/main...HEAD（或 task 分支相对 main）
- 审查：docs/harness/reviews/by-task/chatbi-v3-lowconf-sql-preview/task_chatbi_v3_lowconf_sql_preview_v1_audit_R1_20260531.md

你必须完成：
1. 对照 §2 G1–G6、failure_paths F1–F5、Delta ADDED/MODIFIED 场景。
2. 复跑 §6 验证命令；落盘 docs/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-sql-preview_20260531_v1.md
3. Judgment + 合并建议（required · 涉 api/ 契约）。
4. commit 本轮路径；回报 00 续 CLOSE（KPI 终算 + G5 母单 5-2 + CLOSE_TRACE）。

禁止：代签 human_gate；无 reinspect 落盘宣称通过。

Judgment（50 · 末尾）：
- experience_capture: 是否升 required
- gate/risk: HG-REINSPECT 人签后再 merge
- hat_self: pass | pass-with-notes | blocked
```
