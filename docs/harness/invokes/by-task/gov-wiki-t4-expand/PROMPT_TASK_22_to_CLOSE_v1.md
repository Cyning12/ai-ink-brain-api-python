# 启动 Prompt · 单 task · 22 → 关账（v1 · 无 10）

> **模板** · 全链入口：[`PROMPT_START_full_chain_v1.md`](./PROMPT_START_full_chain_v1.md)  
> **SKILL**：[`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md)

---

## 1. 元信息（固定 · 勿改）

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/active/task_governance_wiki_t4_expand_v2.md` |
| **task_slug** | `gov-wiki-t4-expand` |
| **freeze_id** | `GOV-T4-EXPAND@2026-05-27` |
| **git_branch** | `task/gov-wiki-t4-expand-v1` |
| **invoke 目录** | `docs/harness/invokes/by-task/gov-wiki-t4-expand/` |
| **review 目录** | `docs/harness/reviews/by-task/gov-wiki-t4-expand/` |

---

## 2. 22 开工前

- [ ] `git branch --show-current` = `task/gov-wiki-t4-expand-v1`
- [ ] `HG-TASK-DRAFT` = **approved**
- [ ] 读 Pilot：`docs/coding_wiki/syntheses/query-rewrite-observability.md`
- [ ] 读 Bridge SPEC §3–§4.3

---

## 3. 可复制 Prompt 正文（帽链逐步）

```text
你正在执行单 task **gov-wiki-t4-expand** 帽链：**22 → 30 → 40 → 50 → 关账**（无 10）。

真值：
- docs/tasks/active/task_governance_wiki_t4_expand_v2.md
- docs/tasks/skills/SKILL-harness-task.md
- docs/tasks/skills/SKILL-docs-governance.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
- docs/harness/prompts/hats/22-task-audit.md … 50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md

semi_auto: true · 每帽 invoke §3 ≥15 行 · 每帽 commit

---

### 步骤 0 · 开帽前

git branch --show-current
确认 human_gate approved
创建 invoke/review 目录（若不存在）

---

### 步骤 1 · 22 任务审核

1. 按 22-task-audit.md 审 task + Bridge SPEC
2. 落盘 review：`docs/harness/reviews/by-task/gov-wiki-t4-expand/task_governance_wiki_t4_expand_audit_R1_YYYYMMDD.md`
3. 落盘 invoke：`invoke_YYYYMMDD_22_gov-wiki-t4-expand-v1.md`（§3 ≥15 行 · 元信息表）
4. **commit** → 报告 hash

---

### 步骤 2 · 30 执行编码

1. 按 task §范围交付（2 篇 synthesis graph_nodes + CODING_WIKI + RECENT）
2. 每个 node id 跑 graph_query neighbors 验证
3. 回填 task §实现备忘
4. invoke_YYYYMMDD_30_* · **commit**

---

### 步骤 3 · 40 自检

1. 跑 task §VERIFY 命令
2. 回填 task §自检结论
3. §验收项勾选 pass 项
4. invoke_YYYYMMDD_40_* · **commit**

---

### 步骤 4 · 50 独立复检

1. 零假设复检 task 验收 + git diff
2. 落盘 `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-expand_YYYYMMDD_v1.md`
3. invoke_YYYYMMDD_50_* · **commit**

---

### 步骤 5 · 关账

1. task 头部 `done（YYYY-MM-DD · GOV-T4-EXPAND@2026-05-27）`
2. `git mv` → `docs/tasks/done/task_governance_wiki_t4_expand_v2.md`（与 done 头部 **同 commit**）
3. `docs/tasks/_views/done.md` 一行
4. docs-governance H1–H5（reinspect 名 / RECENT §8 / 交叉引用）
5. invoke_YYYYMMDD_CLOSE_* · **commit**
6. 对话输出 **HANDOFF_CLOSE_TRACE**

---

硬约束：docs-only · 非 Loop · 下一 task（L2 CI）须 **新分支** `task/gov-l2-manifest-ci-v1`
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：单 task 22→关账 逐步模板 |
