# 标准样本 · ChatBI V3 低置信 Text2SQL 预览 + plan_execution_token（§5-2）

> **用途**：联调 / PR / FE-1 烟测留证；**非**实现真值（真值见 docs/tasks/done/task_chatbi_v3_lowconf_sql_preview_v1.md、SPEC、pytest）。
> **采集**：2026-05-31 · Ink Unified Chat · 后端分支 task/chatbi-v3-lowconf-sql-preview
> **freeze_id**：CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31

## 环境要点

| 项 | 值 |
|----|-----|
| 问句 | 统计 heros  表里有多少条数据 |
| session_id | 211d54b7-f806-4265-b46e-fc1a897f51e2 |
| 开关 | CHATBI_USE_AGENT + CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1 + CHATBI_V3_PLAN_PREVIEW_CONFIRM=1 |

## 两轮预期

| 轮次 | 文件 | 关键观测 |
|------|------|----------|
| 1 预览+澄清 | round1_preview_clarify_timeline.json | agent.plan.preview → agent.clarify；total_steps=0 |
| 2 令牌放行 | round2_token_bypass_execute_timeline.json | 已校验 token；sql.result heros count=10 |

## 截图

- screenshots/timeline-plan-preview-clarify.png — step-11/12 方案预览与澄清
- screenshots/ui-confirm-execute-card.png — 「按预览执行」卡片

## 关联

- docs/tasks/done/task_chatbi_v3_lowconf_sql_preview_v1.md
- docs/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-sql-preview_20260531_v1.md
