# PROMPT · 30 执行帽（governance-tasks-done-hygiene）

> **阶段**：30 execute  
> **目标**：按 task 范围完成 `docs/tasks/` done 索引治理 + Coding Wiki 链路同步，40 自检通过，为 50 复检做准备。  
> **约束**：**禁止写 `api/**`；禁止改业务代码；文档-only PR。**

---

## 0. 开帽前检查

- [ ] `HG-TASK-DRAFT` 状态为 `approved`
- [ ] `HG-AUDIT-R1` 状态为 `approved`
- [ ] 已读 [`docs/tasks/active/task_governance_tasks_done_index_hygiene_v1.md`](../../active/task_governance_tasks_done_index_hygiene_v1.md) 全文
- [ ] 已读本 Prompt 的「必读」与「执行清单」

若任一闸为 `pending`：立即停止，只输出阻塞的 `human_gate_id` 与文件路径。

---

## 1. 必读（按顺序）

1. [`docs/tasks/active/task_governance_tasks_done_index_hygiene_v1.md`](../../active/task_governance_tasks_done_index_hygiene_v1.md)
2. [`docs/tasks/README.md`](../../../tasks/README.md)
3. [`docs/tasks/_views/done.md`](../../../tasks/_views/done.md)
4. [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../../tasks/RECENT_TASK_SCHEDULE.md) §6.1 / §6.6
5. [`docs/coding_wiki/CODING_WIKI.md`](../../../coding_wiki/CODING_WIKI.md)
6. [`docs/coding_wiki/index.md`](../../../coding_wiki/index.md)
7. [`docs/coding_wiki/concepts/task-schedule-ink-backend.md`](../../../coding_wiki/concepts/task-schedule-ink-backend.md)
8. [`cyning-harness/harness/templates/TASK_done_README.md`](../../../../../../cyning-harness/harness/templates/TASK_done_README.md)
9. [`cyning-harness/harness/templates/VIEW_done_by_domain.md`](../../../../../../cyning-harness/harness/templates/VIEW_done_by_domain.md)
10. [`cyning-harness/harness/templates/VIEW_done_thin_pointer.md`](../../../../../../cyning-harness/harness/templates/VIEW_done_thin_pointer.md)
11. [`cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md`](../../../../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)
12. [`docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md`](../../../prompts/handoff/HANDOFF_CLOSE_TRACE.md)

---

## 2. 执行清单

### A) `docs/tasks` 索引层

#### A1 · 新建 `docs/tasks/done/README.md`

- 用途：日常浏览只打开本文件；`_views/done.md` 为薄指针。
- 真值：task 头部 `状态` + `docs/tasks/done/<domain>/` 物理位置。
- 按域分组表：
  - `harness`：`task_harness_*`（非产品里程碑）
  - `governance`：`task_governance_*` · `task_gov_*`
  - `chatbi`：`task_chatbi_*`
  - `engineering`：`task_engineering_*`
  - `standards`：`task_standards_*`
  - `epics`：Epic / MANIFEST / Loop 母单
- 每行格式：`关账日 | [task_slug](../done/task_*.md) | freeze_id / 一行摘要`
- Epic 母单单独一节。
- 底部链 `FRAGMENT_task_domain_infer_v1_zh.md`。

#### A2 · 新建 `docs/tasks/_views/done_by_domain.md`

- 与 Hub 语义一致，路径用 `../done/task_*.md`（P0 仍扁平）。
- 每域一张表：`关账日 | 链接 | 一行摘要`。
- Epic 母单单独一节。

#### A3 · 重写 `docs/tasks/_views/done.md` 为薄指针

- ≤15 行。
- 内容：
  - 标题「Tasks 状态视图：已完成（done）」
  - 说明：完整导航见 `../done/README.md`；分组表见 `done_by_domain.md`。
  - 快速入口表：Hub、`done_by_domain.md`、`in_progress.md`。
  - 维护纪律：关账时更新 Hub / `done_by_domain`；勿在本文件追加长列表。

#### A4 · `docs/tasks/done/<domain>/` 目录结构声明

- 在 `done/README.md` 顶部或对应域节前说明：P0 不 mass `git mv`，目标子目录 slug 见域表。

#### A5 · 索引表链到现有 `done/task_*.md`

- 路径仍用扁平相对路径。
- 确保所有链接相对 `_views/` 或 `done/README.md` 有效。

#### A6 · 更新 `docs/tasks/README.md`

- 在「任务归档流程」checklist 中新增：
  - 第 4 步（或插入）：更新 `done/README.md` Hub 对应域表一行。
  - 第 5 步：更新 `_views/done_by_domain.md`。
  - 原第 4 步 `_views/done.md` 改为「保持薄指针，不追加长列表」。
- 新增「域子目录 + Hub 纪律」段落：
  - 说明 `done/<domain>/` 规划。
  - 引用 `FRAGMENT_task_domain_infer_v1_zh.md`。

### B) Coding Wiki 同步

#### B1 · `docs/coding_wiki/concepts/task-schedule-ink-backend.md`

- 在「链接」节或「Epic 分区」前增 Hub 指针：
  - `docs/tasks/done/README.md` — done 任务按域 Hub
  - `docs/tasks/_views/done_by_domain.md` — 按域分组表
- 写明：L1 真值仍在 `RECENT` 与 `done/task_*.md`，L2 Wiki 只链不替代。

#### B2 · `docs/coding_wiki/index.md`

- 在「综合」表下方或「维护」前增一段说明：
  - syntheses `source_task` 指向 L1 `done/` 扁平路径。
  - 浏览历史任务优先用 `docs/tasks/done/README.md` Hub。
  - Hub 不替代 `source_task` 真值。

#### B3 · `docs/coding_wiki/CODING_WIKI.md`

- §4.1 ingest：关账后除更新 `index.md` / `log.md` 外，还需在 `docs/tasks/done/README.md` Hub 对应域表追加一行。
- §4.2 query：Agent 读序增「浏览 done 任务先 Hub / `done_by_domain`」。
- 链 `FRAGMENT_task_domain_infer_v1_zh.md`。

#### B4 · 保持 syntheses `source_task` 有效

- P0 不改 frontmatter 路径。
- 若发现已有 synthesis 链到将迁移的子目录路径，本 task 不改动，留待 P1 子 task 统一处理。

---

## 3. 40 自检（执行后必须做）

运行以下检查并回填 task §8：

```bash
# 1. 行数检查
wc -l docs/tasks/_views/done.md

# 2. 相对链接检查（手动或脚本）
python tools/verify_markdown_links.py docs/tasks/done/README.md docs/tasks/_views/done_by_domain.md docs/tasks/_views/done.md docs/tasks/README.md docs/coding_wiki/concepts/task-schedule-ink-backend.md docs/coding_wiki/index.md docs/coding_wiki/CODING_WIKI.md

# 3. ruff（若 CI 配置）
ruff check .
```

若 `verify_markdown_links.py` 不存在，可用以下等价命令：

```bash
grep -nE '\[([^\]]+)\]\(([^)]+)\)' docs/tasks/done/README.md docs/tasks/_views/done_by_domain.md docs/tasks/_views/done.md | while read line; do ...; done
```

要求：

- `_views/done.md` ≤15 行。
- 所有相对链接 zero BROKEN。
- `done_by_domain.md` 与 Hub 无域级不一致。

---

## 4. 验收标准（逐条勾选）

- [ ] `done/README.md` 已创建，覆盖主域
- [ ] `_views/done.md` ≤15 行，指向 Hub
- [ ] `_views/done_by_domain.md` 已创建，与 Hub 一致
- [ ] `docs/tasks/README.md` 归档流程已更新
- [ ] Coding Wiki 三文件已链 Hub 并写明 L1 vs L2
- [ ] 链接自检 zero BROKEN
- [ ] 40 自检结论已回填 task §8
- [ ] 未修改 `api/**` 或业务代码

---

## 5. 禁止

- **不写 `api/**`。**
- **不改 `packages/**`。**
- **不批量 `git mv` `done/` 文件。**
- **不修改 `HG-*` 人工闸状态。**
- **不为本 task 新建 synthesis。**
- **不改现有 syntheses 的 `source_task` 路径（除非发现明显 404）。**

---

## 6. 输出 / 交接

30 完成后输出：

1. 修改文件列表（相对仓库根）。
2. 40 自检结果（命令 + 结论 + 要点）。
3. 是否建议进入 40/50（yes/no + 理由）。
4. 若自检失败，列出阻塞项与修复建议。

---

## 给 Cursor

`governance-tasks-done-hygiene`、30 execute、文档-only、`done/README.md`、`_views/done.md`、`_views/done_by_domain.md`、链接自检、禁止写 api
