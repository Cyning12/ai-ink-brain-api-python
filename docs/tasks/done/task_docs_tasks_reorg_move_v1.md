# Task：Docs Tasks 规整迁移（v1）— 按类型/状态移动 tasks 文档

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> 状态：done（2026-05-22 验收通过）  
> 范围：仅 `ai-ink-brain-api-python/docs/`（不涉及代码与 `_tech_graph/`）  
> 关联：`docs/README.md`、`docs/tasks/_views/*.md`

---

## 背景与目标

当前 `docs/tasks/` 混杂了：

- 任务（`task_*.md`）
- 规格（`SPEC-*.md`）
- 模板（`TASK_TEMPLATE.md`）
- 历史命名（如 `Task 04.md`、未声明 `状态` 的任务）

这会导致：

- 无法按“状态”快速找到在做什么
- spec 与 task 的职责边界不清晰
- 新增任务时命名与放置位置难以统一

目标：在**不改文档内容语义**的前提下，仅做**目录与文件位置规整**，并同步更新索引入口（README + views）。

---

## 范围

- [x] 新增 tasks 目录结构（只在 `docs/tasks/` 内）
- [x] 将现有文件按规则 `git mv` 到新位置（保留 git 历史）
- [x] 更新 `docs/README.md` 与 `docs/tasks/_views/*.md` 的链接/路径

## 非范围

- 不修改 `docs/_tech_graph/` 任何内容
- 不重写已有任务/spec 文档正文（除非为了修复链接路径）

---

## 目标目录结构（v1）

```
docs/tasks/
  _views/                 # 状态视图索引（已存在）
  active/                 # 设计中/进行中/待开始的任务（task_*.md）
  done/                   # 已完成任务（task_*.md）
  specs/                  # 规格文档（SPEC-*.md）
  templates/              # 模板（TASK_TEMPLATE.md）
  legacy/                 # 历史命名/缺少状态/待补齐字段的任务
```

---

## 迁移规则（v1）

### A. 模板

- `TASK_TEMPLATE.md` → `templates/`

### B. SPEC 文档

- `SPEC-*.md` → `specs/`

### C. 任务 task_*.md

按文档头部 `状态` 字段归类（兼容 `> **状态**：...` 与 `状态：...`）：

- `done` → `done/`
- `draft` / `design` → `active/`
- `pending` / `in_progress` → `active/`

### D. 例外与遗留

以下类型进入 `legacy/`，后续再补齐 `状态` 与命名：

- 文件名不符合 `task_*.md`（例如 `Task 04.md`）
- 未声明 `状态` 的任务文档

---

## 验收标准

- [x] `docs/tasks/` 顶层不再混放 `SPEC-*.md` 与 `TASK_TEMPLATE.md`
- [x] `docs/tasks/_views/*.md` 能正确链接到迁移后的文件路径
- [x] `docs/README.md` 的 tasks 导航更新为新结构（含 `_views` 入口）
- [x] `git status` 无丢失文件（只应体现移动与索引更新）

---

## 实现备忘

- 推荐用 `git mv` 保留历史
- 迁移完成后再统一跑一遍“状态扫描”确认没有漏网文件

