# Harness P1-1 后端同步 handoff（Projects 关账后）

> **性质**：操作备忘；**非**工程真值。Projects 仓 P1-1 PR 合并后再执行本 handoff。  
> **前置**：Projects `task/harness-p1-reviews-pointers` → `main` 已合并（pointer 索引 + `docs/harness/tasks/done/task_harness_p1_reviews_pointers_v1.md`）。

---

## 1. 触发条件

- [x] Projects PR 已 merge（工作区 `docs/harness/reviews/` pointer 清理完成）
- [ ] 已知 Projects merge commit 短哈希：`c8f3d8c`（2026-05-23）

---

## 2. 后端小 PR（仅排期同步）

**分支**：`task/docs-schedule-p1-1-done`（从最新 `main` 拉出）

**改动的唯一文件**：`docs/tasks/RECENT_TASK_SCHEDULE.md`

### 2.1 §0.4 表

```markdown
| P1-1 | 工作区 `Projects/docs/harness/reviews/` pointer 改索引/删悬空 | **done** | Projects PR #___ · YYYY-MM-DD |
```

### 2.2 §1 快照（Harness P1 行）

```markdown
| **Harness P1** | P1-1～P1-3 **done**（YYYY-MM-DD）；Harness 前端 parity（P1-4）**远期** |
```

### 2.3 §2 时间线

- 删除或划掉「**当前** §0.4 P1-1 工作区 pointer」
- 可选新增：`Harness P1 巩固 **done**（P1-1～P1-3）`

### 2.4 §8 修订记录

```markdown
| YYYY-MM-DD | **Harness P1-1 done**：Projects reviews pointer 索引；后端排期同步 |
```

---

## 3. Commit / PR 文案

**Commit message**：

```text
docs(tasks): 排期同步 Harness P1-1（Projects reviews pointer done）
```

**PR title**：`docs(tasks): 排期同步 Harness P1-1 done`

**PR body 模板**：

```markdown
## Summary
- Projects 仓 P1-1 已合并（reviews pointer 索引/悬空清理）。
- 同步 `RECENT_TASK_SCHEDULE.md`：P1-1 → done；Harness P1-1～P1-3 全收口。

## Test plan
- [x] 文档-only
- [ ] 与 Projects merge commit / task done 路径交叉核对
```

---

## 4. 后端 Agent 可复制 Prompt（Projects PR 合并后）

```text
在后端仓 ai-ink-brain-api-python 执行：

1. git checkout main && git pull
2. git checkout -b task/docs-schedule-p1-1-done
3. 更新 docs/tasks/RECENT_TASK_SCHEDULE.md：
   - §0.4 P1-1 → done（链 Projects PR #___）
   - §1 Harness P1 行 → P1-1～P1-3 done
   - §2 时间线去掉 P1-1 当前项
   - §8 修订记录追加一行
4. 仅改 RECENT_TASK_SCHEDULE.md，不重复改 reviews/pointer（属 Projects 仓）
5. commit + 开 PR → main

参考：docs/diary/2026-05-23-harness-p1-1-backend-sync-handoff.md
Projects 关账 task：docs/harness/tasks/done/task_harness_p1_reviews_pointers_v1.md
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-23 | 初稿：Projects P1-1 合并后的后端排期同步 handoff |
