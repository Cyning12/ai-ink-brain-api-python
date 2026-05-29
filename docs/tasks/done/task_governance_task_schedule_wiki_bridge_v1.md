# Task：治理 — 任务排期 Wiki 桥接（防孤岛）

> **状态**：done（2026-05-29）  
> **前置**：Wiki 治理线里程碑收口（T4 ops #83 · diary 验收草案）  
> **规划**：[`docs/coding_wiki/concepts/task-schedule-ink-backend.md`](../../coding_wiki/concepts/task-schedule-ink-backend.md)

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs · L2 concept + RECENT/README 指针；无 `api/` 变更。 |
| **freeze_id** | `GOV-TASK-SCHEDULE-WIKI@2026-05-29` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-task-schedule-wiki-bridge-v1` |
| **task_slug** | `gov-task-schedule-wiki-bridge` |
| **schedule_ref** | RECENT §0 · 排期桥接优先于 V3 P2-1b |
| **epic** | 治理 · Wiki / 排期 hygiene |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 30 | 人同意 task-schedule concept 方向 |
| HG-REINSPECT | approved | done | docs 关账（可选 50） |

---

## 背景与目标

`RECENT_TASK_SCHEDULE.md` 为 L1 排期真值，但 active task 与 Wiki 图谱之间缺少 **统一导航 hub**，易导致任务孤岛。本 task 在 **不替代 RECENT** 前提下，增加 L2 concept 页与维护常模。

**完成态**：

1. `docs/coding_wiki/concepts/task-schedule-ink-backend.md`（排期 hub · pointer 至 RECENT）  
2. `index.md` · `CODING_WIKI.md` §4.2 · `docs/tasks/README.md` 读序/字段更新  
3. RECENT §0/§1 快照与 §8 修订  
4. **范例**：P2-1b task 头补 `schedule_ref` / `epic` / `blocked_by`  
5. `log.md` 一行 · 关账归档

---

## 范围

- [x] concept 页 `task-schedule-ink-backend.md`  
- [x] `index.md` concepts 表增行  
- [x] `CODING_WIKI.md` §4.2 规划读序  
- [x] `tasks/README.md` schedule_ref 常模  
- [x] `RECENT_TASK_SCHEDULE.md` §0/§1/§8 同步  
- [x] P2-1b 头字段范例  
- [x] `log.md` 追加
- [x] 三方读序 smoke **4/4 pass**（Claude Code · Kimi-code · [`conclusion_smoke_zh.md`](../../harness/experiments/task_schedule_read_smoke_v1/conclusion_smoke_zh.md)）

## 非范围

- `_task_index.json` 机器轨  
- 全 active task 批量改头（仅 1 篇范例）  
- RECENT 全文迁入 Wiki  
- graph.json 增 task 节点

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | Wiki 替代 RECENT 作排期真值 | 22/审查阻塞 · 回 L1 |
| F2 | concept 复制 RECENT 长表 | lint/人审 fail · 改 pointer |

---

## 验收标准

- [x] concept 可链 RECENT · active 表与 §1.1 一致  
- [x] `python tools/coding_wiki_graph_nodes_lint.py` 仍 OK（`graph_nodes: []`）  
- [x] 关账 `git mv` · `_views/done.md`

**VERIFY**：

```bash
rg -n 'task-schedule-ink-backend' docs/coding_wiki/index.md docs/coding_wiki/CODING_WIKI.md docs/tasks/README.md
python tools/coding_wiki_graph_nodes_lint.py
```

---

## 实现备忘

| 项 | 内容 |
|----|------|
| 涉及文件 | concept · index · CODING_WIKI · tasks/README · RECENT · P2-1b task · log.md · `harness/experiments/task_schedule_read_smoke_v1/` |
| PR | （待开 · 含 smoke 落盘 `fc6f69c`+） |
| smoke | `TASK-SCHEDULE-READ-SMOKE@2026-05-29` · Claude Code · Kimi-code · **4/4 pass** |

---

## 给 Cursor

`gov-task-schedule-wiki-bridge`、task-schedule、RECENT、防孤岛、排期 hub
