# docs/tasks/ 使用规则（v1）

> 目标：让新任务“落盘位置一致、状态可追踪、索引可直达”，并避免 `active/` 长期堆积。

---

## 目录结构（以当前仓为准）

```
docs/tasks/
  README.md                # 本文件：落盘规则
  _views/                  # 状态视图索引（聚合，不改原任务正文）
  active/                  # 设计中/待开始/进行中（task_*.md）
  done/                    # 已完成（task_*.md）
  specs/                   # 规格文档（SPEC-*.md）
  templates/               # 模板（TASK_TEMPLATE.md）
  legacy/                  # 历史命名/缺少状态/待补齐字段
```

---

## 新增任务如何落盘（必须遵守）

- **新建位置**：一律放在 `docs/tasks/active/`
- **命名规则**：`task_<domain>_<topic>_vN.md`（示例：`task_tech_graph_p8_xxx_v1.md`）
- **必须字段**：任务头部必须包含 `> **状态**：...`

允许状态集合（与现有模板兼容）：
- `draft`（等价 design）
- `pending`
- `in_progress`
- `done`

---

## 什么时候从 active 移到 done

当任务验收通过（满足任务文档里的“验收标准”）：
- 将任务头部 `状态` 改为 `done（YYYY-MM-DD 验收通过）`
- 使用 `git mv` 把文件从 `active/` 移到 `done/`
- 同步更新索引：`docs/tasks/_views/done.md`

> 说明：`_views/*.md` 只做链接聚合，不作为真值；真值以任务文件头部 `状态` 为准。

---

## specs / legacy 的边界

- **`specs/`**：只放规格（`SPEC-*.md`），可被多个 task 引用。
- **`legacy/`**：只放历史遗留（命名不规范/缺少状态/待补齐字段）。后续“修复命名与状态”应通过独立 task 执行，避免一次性大改造成漂移。

---

## 视图索引维护规则（最小集）

- `docs/tasks/_views/design.md`：列出 `draft/design` 的任务 + “缺少状态字段”清单（统一维护在此）
- `docs/tasks/_views/in_progress.md`：列出 `in_progress`
- `docs/tasks/_views/done.md`：列出 `done`

---

## 常见坑（强制避免）

- 不要把已完成任务留在 `active/`（会误导新 Agent 判断“还在做”）
- 不要在任务文件里写“已完成但状态还是 pending”（状态必须与事实一致）
- 不要在 `docs/tasks/` 顶层混放 task/spec/template（统一按目录归类）
