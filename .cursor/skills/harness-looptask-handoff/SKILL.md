---
name: harness-looptask-handoff
description: >-
  LoopTask stop_after_hat:50 后交付 50 全文 Prompt、R1/R2/50 签收路径、以及人改 human_gate
  的「文件+表格字段+改前值→改后值」表。用于 CLOSE、HG-REINSPECT、Portfolio 跨仓关账。
  Use when looptask ends at 50, user asks for reinspect handoff, or manual gate edit checklist.
disable-model-invocation: true
---

# Harness LoopTask 交接（后端 · 止于 50）

> **便携真值（跨 Agent）**：[`docs/tasks/skills/SKILL-harness-looptask-handoff.md`](../../docs/tasks/skills/SKILL-harness-looptask-handoff.md)  
> **配对前端 skill**：`ai-ink-brain/.cursor/skills/harness-looptask-handoff/SKILL.md`

## 硬规则（摘要）

1. **50 Prompt**：占位符全替换 · 对话贴 **Handoff + §5 正文** · 禁止只给链接  
2. **签收清单**：R1 · R2 · 40 自检节 · 50 reinspect · invoke 链 · **写实际相对路径**  
3. **人改 gate**：**禁止**笼统；**必须**表格式「文件 | 位置 | 改什么」  
4. **禁止 Agent**：代签 `HG-REINSPECT` · 代填 `### KPI（00）` · 擅自 `git mv` done

## 本子仓路径速查

| 类型 | 路径 |
|------|------|
| task | `docs/tasks/active/task_*.md` |
| reviews | `docs/harness/reviews/by-task/<slug>/` |
| invokes | `docs/harness/invokes/by-task/<slug>/` |
| reinspect | `docs/tasks/reinspect_results/` |
| CLOSE | `docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md` |

完整条文、Portfolio 跨仓示例、关账步骤 → **读便携真值 MD**（上链）。
