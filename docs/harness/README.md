# docs/harness（本后端仓 · 22 + 50 + 执行链）

> **目标**：日常只读本目录 + `docs/tasks/`；含 **三方 Agent（50 帽）** 可查收落盘。  
> **历史**：22/reviews、旧 invoke 见 [`../diary/harness-archive/`](../diary/harness-archive/README.md)。

---

## 1. 日常读什么

| 场景 | 路径 |
|------|------|
| 写 task / **下一棒双 Prompt** | `TEMPLATE-requirements`（**A:22** + **B:30**，人择一） |
| 任务审核 22 | [`reviews/README.md`](reviews/README.md) → `TEMPLATE-task-audit` |
| 执行 + 自检 | `TEMPLATE-execute` → `TEMPLATE-self-check` |
| **三方复检** | `TEMPLATE-independent-reinspect` → [`../tasks/reinspect_results/`](../tasks/reinspect_results/README.md) |
| 半自动 / 人工闸 | `HANDOFF_SEMI_AUTO` |
| commit / 关账 | `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE` |
| task 字段 | `HARNESS_V2_PLAN.md` §5 |
| 流程 | `SDD_HAT_FLOW.md` |
| 新 invoke | `invokes/` |
| **Harness 裁决共识（已接受）** | [`../diary/2026-05-22-harness-evaluation-improvement-response.md`](../diary/2026-05-22-harness-evaluation-improvement-response.md) **§九** |

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc`、`.cursor/rules/06-harness-in-repo.mdc`。

**Agent 禁止（日常）**：

- **禁止** 默认读取工作区 `Projects/docs/harness/`（跨子仓 Harness 任务除外，见 `docs/tasks/README.md`）。
- **禁止** 将子仓 `prompts/` 软链到工作区；真值以 **本仓** `docs/harness/prompts/` 为准。
- **禁止** 在任务执行中运行下文 **§4 `rsync`**（仅维护者偶发同步）。

---

## 2. 目录结构

```text
docs/harness/
  README.md
  ACCEPTANCE_LANDING.md     # 人类可读落盘 + 50 硬规则
  HARNESS_V2_PLAN.md
  SDD_HAT_FLOW.md
  prompts/                  # 10/20/22/30/40/50 + TEMPLATE + HANDOFF_*
  reviews/README.md         # 22 帽 · 仅本仓 task
  invokes/README.md
```

---

## 3. 关账最低要求（摘要）

1. （若人择 **路径 A**）`docs/harness/reviews/task_*_audit_*.md`（22）无阻塞  
2. task **`### 自检结论（执行者）`**（40）  
3. **`docs/tasks/reinspect_results/reinspect_*.md`**（50）  
4. **`human_gate`** → `approved`（人改）  
5. CI 绿

---

## 4. 上游同步（**仅维护者** · 非 Agent 路径）

> **裁决**：Harness 评价 **§2** — 子仓 **内嵌 prompts** 为 Agent 唯一日常真值；`rsync` 为 **维护者偶发** 从工作区拉取差量，**不是** 执行 task / 半自动链的必读步骤。

| 角色 | 行为 |
|------|------|
| **Agent / 子 Agent** | 只读 **本仓** `docs/harness/prompts/`、`reviews/`、`invokes/`；**不** 执行本节命令 |
| **维护者** | 工作区 `Projects/docs/harness/` 有模板更新时，按需 `rsync` 差量进子仓；合并时 **保留** 本仓 `ACCEPTANCE_LANDING.md`、50 落盘约定、`reviews/` 规则，**勿** 整目录覆盖删改 |

**前提**：在 **工作区根** `Projects/` 下执行（路径相对该根）；目标为 **`ai-ink-brain-api-python/docs/harness/prompts/`**。

```bash
# 示例：仅同步指定文件（按实际上游变更增删行，禁止 blind 全量覆盖 prompts/）
rsync -a docs/harness/prompts/50-independent-reinspect.md \
  ai-ink-brain-api-python/docs/harness/prompts/
rsync -a docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md \
  ai-ink-brain-api-python/docs/harness/prompts/
# 合并后人工 diff：保留本仓 ACCEPTANCE_LANDING、reinspect 落盘路径、reviews 仅本仓 等约定
```

**维护者合并检查清单**：

- [ ] 未删除本仓 `50` 与 `reinspect_results/` 关账链
- [ ] 未恢复工作区 `reviews/` 正文到子仓（历史样例以本仓 `reviews/README` 为准）
- [ ] `06-harness-in-repo.mdc` 仍指向 **本仓** `docs/harness/`，非工作区默认路径

---

## 5. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v2 最小集 |
| 2026-05-22 | v3：**恢复 50** + `ACCEPTANCE_LANDING` + `reinspect_results` 关账 |
| 2026-05-22 | v4：链 diary **§九 生效共识**；`reviews/` 历史样例召回见 `reviews/README.md` |
| 2026-05-22 | v5：§4 标明 rsync **仅维护者**；§1 Agent 禁止默认读工作区 harness |
