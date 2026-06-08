# PROMPT · Kimi Code · Plan Agent 导航修复复验（零业务 PR）

> **日期**：2026-06-06  
> **性质**：产品/导航实验 · **独立于** Harness T1 试点  
> **背景**：[`docs/diary/2026-06-05-plan-agent-analysis/00_README.md`](../../diary/2026-06-05-plan-agent-analysis/00_README.md) · Issue [#489](https://github.com/MoonshotAI/kimi-code/issues/489)  
> **默认**：**不**改 `docs/tasks/`、`RECENT`、代码 · 产出落 `tmp/diary/` 或可选 commit diary

---

## 1. 目标

用 **修过的 prompt** 重跑 Plan Agent（「制定升级计划」），验证：

1. 子 Agent **不** 深读 `docs/spec/v3-agent/**` / `api/**`
2. **按序**读 `AGENTS` → `_tech_graph/00_main` → `RECENT` → active task
3. **300s 内**完成或主动汇报超时风险

**成功标准**：Plan 产出可读 · 读路径与 forbidden 合规 · 无业务 repo diff（除非人主动 commit 对比简报）

---

## 2. Kimi 主会话正文（可复制）

```text
【实验】Plan Agent 导航修复复验 · 零业务 PR

请 spawn Plan Agent（或等价子 Agent），任务：为本仓制定「升级/排期计划」摘要。

【子 Agent prompt 必须内联以下内容 · 不可省略】

--- 子 Agent 读序（强制按序）---
1. AGENTS.md §必读
2. docs/_tech_graph/00_main.md
3. docs/tasks/RECENT_TASK_SCHEDULE.md §1.1 active 表
4. docs/tasks/active/ 下各 task **仅读文首 30 行**（禁止逐个全文深读）

【forbidden · 违反则立即停并回报】
- docs/spec/v3-agent/** 任何文件
- api/**、tests/**、.github/** 源码
- docs/diary/**、docs/harness/invokes/** glob
- docs/_tech_graph/graph.json 整包
- git log / git blame

【深度控制】
- 总 wall-clock 目标 ≤240s；120s 须输出阶段性摘要
- 禁止读超过 12 个文件
- 禁止 spawn 子 subagent

【交付物】
- 计划 Markdown：5 段以内（现状 / 下一棒 / 风险 / 非范围 / 引用路径列表）
- 落盘：tmp/diary/2026-06-XX-kimi-plan-agent-revalidation/plan.md（本机 · 默认不 commit）

【回报格式】
Status / FilesRead（路径列表）/ ForbiddenViolations / Blockers / Judgment（各≤10行）

【主会话纪律】
- 不要改 docs/tasks/、RECENT、api/
- 不要 git commit 业务文件
- 可选：将对比简报写入 docs/diary/…（仅当人授权 commit）
```

---

## 3. 对照基准（只读）

| 臂 | 路径 |
| --- | --- |
| Claude 成功 | `docs/diary/2026-06-05-plan-agent-analysis/artifacts/claude/upgrade_plan.md` |
| Kimi 失败补救 | `docs/diary/2026-06-05-plan-agent-analysis/artifacts/kimi/upgrade_plan_fallback.md` |
| 根因 | `docs/diary/2026-06-05-plan-agent-analysis/analysis/02_agent_design_comparison.md` |

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1 · Plan Agent 导航复验 · 零业务 PR 默认 |
