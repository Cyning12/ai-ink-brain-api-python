# 同步 Harness prompts / rules 至 by-task invoke 落盘路径

> **状态**：done（2026-06-02 · 配对前端 PR #48 已 merge）
> **task_slug**：`harness-invokes-by-task-prompts-sync`  
> **git_branch**：`task/harness-invokes-by-task-prompts-sync`  
> **配对前端 task**：`ai-ink-brain` · `task/harness-frontend-invokes-by-task-migration`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `harness-invokes-by-task-prompts-sync` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 文档 / prompts 路径同步；不触达 `api/` |
| **semi_auto** | `true` |
| **git_branch** | `task/harness-invokes-by-task-prompts-sync` |
| **freeze_id** | `HARNESS-INVOKES-BY-TASK-PROMPTS@2026-06-02` |

---

## 背景

后端 **文件** 已于 2026-05-25 全部迁入 `docs/harness/invokes/by-task/`，但以下 **消费面** 仍写扁平路径，导致前端 Agent（读工作区 prompts 单源）与新开后端 Agent 仍可能落盘到错误位置：

| 文件 | 问题 |
|------|------|
| `.cursor/rules/05-harness-semi-auto.mdc` | 写 `invokes/invoke_*.md`（与 `06-harness-in-repo` 矛盾） |
| `TEMPLATE-execute/self-check/task-audit/...` | §3 写 `Projects/docs/harness/invokes/` |
| `HANDOFF_SEMI_AUTO` §3.2 | 写 `invokes/invoke_*` |
| `HANDOFF_AUTO_COMMIT` / `HANDOFF_CLOSE_TRACE` | 示例路径扁平 |

---

## 范围（2026-06-02 已改）

- [x] `.cursor/rules/05-harness-semi-auto.mdc` → `by-task/<task_slug>/`
- [x] `docs/harness/prompts/templates/TEMPLATE-{execute,self-check,task-audit,review-spec,independent-reinspect,independent-reinspect-full}-invoke.md`
- [x] `docs/harness/prompts/handoff/HANDOFF_{SEMI_AUTO,AUTO_COMMIT,CLOSE_TRACE}.md`
- [x] 维护者 rsync 至工作区 `Projects/docs/harness/prompts/`（`cyning-ink-workspace@e682fff`）
- [x] `TEMPLATE-requirements-invoke` 已为 by-task（无需改）

## 非范围

- 不迁移 `docs/diary/harness-archive/`（已完成）
- 不改 `api/`

---

## 验收标准

- [x] `05-harness-semi-auto` 与 `06-harness-in-repo` invoke 路径一致
- [x] `rg 'invokes/invoke_' docs/harness/prompts/` 无扁平落盘指令
- [x] 配对前端 PR #48 已 merge

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | TEMPLATE §3 仍写扁平 `invokes/` 路径 | Agent 落盘到错误目录 | 是 | invoke 路径不符合 taxonomy |
| F2 | 工作区 prompts 未 rsync | 前端 Agent 读旧模板 | 是 | 前后端落盘路径不一致 |

---

## 落盘路径约定（§3 统一句式）

```text
<子仓>/docs/harness/invokes/by-task/<task_slug>/invoke_YYYYMMDD_<帽号>_<slug>.md
```

前端子仓对应：

```text
content/harness/invokes/by-task/<task_slug>/invoke_*.md
```

---

## 自检结论（执行者）

- 2026-06-02：8 个 prompts/handoff 文件 + `05-harness-semi-auto.mdc` 已更新
- `rg 'invokes/invoke_' docs/harness/prompts/` 应仅剩本 task / 历史修订记录

---

## 给 Cursor

`by-task`、`task_slug`、`TEMPLATE`、`05-harness-semi-auto`、`rsync`
