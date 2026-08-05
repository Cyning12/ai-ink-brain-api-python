# Task：Harness 模板与规则内嵌后端仓（v1）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：done（2026-05-22 验收通过）  
> **范围**：仅 `ai-ink-brain-api-python/docs/harness/`、`.cursor/rules/`、`AGENTS.md`、`docs/README.md`  
> **目标**：后端 **最小 Harness**（10/20/30/40 + HANDOFF）；无 `reviews/`、历史 invoke 在 `docs/diary/harness-archive/`。

---

## 背景与目标

- 本仓已有 `docs/harness/invokes/`、`reviews/`、`acceptance/`，但 **缺少** `prompts/` 与规划入口，`.cursor/rules/05-harness-semi-auto.mdc` 指向工作区外部路径。
- 目标：镜像工作区 Harness **使用模板 + 规则** 到本仓，并更新 Agent 导航与 Cursor 规则。

---

## 范围

- [x] 镜像 `docs/harness/prompts/`（最小：10/20/30/40 + TEMPLATE + HANDOFF）
- [x] 保留 `HARNESS_V2_PLAN.md` §5、`SDD_HAT_FLOW.md`（最小版）
- [x] 移除 `reviews/`；归档 ~50 `invoke_*`、22/50 帽、P0/CI 留档 → `docs/diary/harness-archive/`
- [x] [`docs/harness/README.md`](../harness/README.md) v2 最小入口
- [x] 更新 `.cursor/rules/05`、`06` 与 `AGENTS.md`、`docs/tasks/README.md`

## 非范围

- 不复制工作区 `docs/harness/tasks/`（跨子仓 Harness 任务仍用工作区索引）
- 不迁移历史 `pointer_*` invoke（前端仓）

---

## 验收标准

- [x] `@docs/harness/prompts/templates/TEMPLATE-execute-invoke.md` 在本仓可打开且 §3 引用路径为 `docs/harness/...`（无 `../../../docs/harness`）
- [x] `AGENTS.md` 必读含 `docs/harness/README.md`
- [x] Agent 执行 `docs/tasks/active/*.md` 时，半自动规则指向本仓 `handoff/HANDOFF_SEMI_AUTO.md`

---

## 实现备忘

- 文件：`docs/harness/prompts/*`、`docs/harness/README.md`、`docs/harness/README.workspace-upstream.md`（上游对照）
- 维护：见 `docs/harness/README.md` §4 `rsync` 示例
