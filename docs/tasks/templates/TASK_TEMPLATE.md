# Task：<动词 + 范围>

> **状态**：draft / pending / in_progress / done  
> **关联图谱**：`docs/_tech_graph/xx_flow_xxx.md`  
> **关联 Issue/PR**：#xxx  
> **前端依赖**：`<前端任务文件名>`（如 API 变更需前端配合，否则填 "无"）

> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/*.md` 索引。

---

## 背景与目标

<短段落，描述完成态行为。>

---

## 范围

- [ ] <具体事项 1>
- [ ] <具体事项 2>

## 非范围

- <明确排除的事项，减少越界>

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_xxx.md` |
| API 契约 | `POST /api/py/xxx` |
| 数据库表 | `public.xxx` |
| 图谱文件 | `docs/_tech_graph/xx_xxx.md` |

---

## 验收标准

- [ ] <验收项 1>
- [ ] <验收项 2>
- [ ] <验收项 3>

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `<文件列表>` |
| 关键 env | `<新增/变更的环境变量>` |
| SQL 执行顺序 | `<init.sql → migration.sql>` |
| 接口变更 | `<新增/修改的端点>` |
| 图谱变更点 | `<_tech_graph/ 中更新的文件>` |
