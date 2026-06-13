# SKILL：Docs / 治理文档（预填 + 关账 hygiene）

> **SKILL ID**：`docs-governance`  
> **状态**：`draft` — 蒸馏来源：Wiki Loop T4+L2 关账审计 N1–N4（2026-05-27）· 须人审后标 `active`。  
> **适用**：**单 task** 与 **Loop 子 round** 的纯 docs / 治理交付（`test_strategy: not_applicable`）。  
> **非替代**：[`../README.md`](../README.md) 归档硬规则 · [`../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md`](../../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md)

---

## 何时选用

| 适用 | 不适用 |
|------|--------|
| 改 `docs/tasks/`、`docs/spec/`、`docs/coding_wiki/`、`_tech_graph/` **文档** | 改 `api/`、`tests/`（用 `api-endpoint` / `bug-fix` 等） |
| 索引 / 排期 / SPEC 指针 / Wiki ingest | Harness 帽子 prompts 正文（用 `harness-task`） |
| Loop **关账后** 或 **单 task 关账后** 索引 hygiene | Loop Batch 编排（用 `harness-loop-batch`） |

---

## Harness 默认值（task 预填）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs/治理；不跑 pytest 作本 task 门禁（图谱脚本按验收另列） |
| **semi_auto** | `true`（推荐） |
| **audit_profile** | `post_close` |

---

## 范围 / 非范围（模板）

**范围**：

- [ ] 列出的 `.md` / `.json`（docs 轨）路径  
- [ ] 链接 / 索引 / frontmatter / 排期表同步  
- [ ] 22/30/40/50 invoke + review/reinspect（若走 Harness）

**非范围**：

- `api/`、`tests/`、`.github/workflows/`  
- `docs/harness/prompts/` 帽子正文  
- 手改 `graph.json`（须 `.ai.md` 导出）

---

## 关账后文档 hygiene（通用 · PR 前）

> **Loop META 后** 或 **单 docs task 关账后**、**开 PR 前** 执行。Loop 专有项（`REPORT_completion_*`、invoke 目录 README）见 [`SKILL-harness-loop-batch.md`](SKILL-harness-loop-batch.md) §长 Loop 完成汇报。

| # | 检查项 | 动作 | 真值 |
|---|--------|------|------|
| H1 | **reinspect 文件名** | `reinspect_{task_slug}_YYYYMMDD_vN.md`；**禁止** `reinspec_` 等 typo | 本节 + [`reinspect_results/README.md`](../reinspect_results/README.md) |
| H2 | **`_views/done.md`** | 关账时更新 `docs/tasks/done/README.md` Hub 对应域表一行 + `docs/tasks/_views/done_by_domain.md`；**禁止**向 `_views/done.md` 追加长列表（薄指针 ≤15 行） | [`../README.md`](../README.md) §归档 |
| H3 | **`RECENT_TASK_SCHEDULE` §8** | 修订记录增一行（日期 + task/Loop 摘要） | 与 §6.6 状态一致；**建议与 ST5/git mv 同批或下一 commit** |
| H4 | **§6.6 / Roadmap 行** | 若交付了 SPEC 阶段（如 T4 Pilot），同步 **planned → draft/done**；**勿删** Loop 专用行 | 治理 SPEC / 母 task；**与 task 头部 done 同步** |
| H5 | **交叉引用** | `_views`、invoke、reinspect 内链指向 **rename 后** 路径 | `rg` 旧文件名 |
| H6 | **SPEC 状态** | `draft`→`active` **仅人审**；Agent 可准备正文不改 status | 各 SPEC 文首 |

**VERIFY（ hygiene 批次）**：

```bash
# 无 reinspec_ typo 残留
! rg -l 'reinspec_' docs/tasks/reinspect_results/ docs/tasks/_views/done.md 2>/dev/null

# 关账 task 在 done/ 且 Hub / done_by_domain 已更新
test -f docs/tasks/done/<your-task>.md
rg '<your-task>' docs/tasks/done/README.md docs/tasks/_views/done_by_domain.md

# 薄指针未被改回长列表
test "$(wc -l < docs/tasks/_views/done.md)" -le 15
```

---

## failure_paths（模板）

| # | 触发 | 行为 |
|---|------|------|
| F1 | 仅改头部 `done` 未 `git mv` | 50 **fail** · 回 30 |
| F2 | reinspect 文件名 typo | hygiene H1 **fail** |
| F3 | RECENT §6.6 与 §8 矛盾 | 人工修正 |
| F4 | 越界改 api/tests | 50 **fail** · revert |

---

## 与 Loop / 单 task 的分工

| 场景 | 读本 SKILL | 另读 |
|------|------------|------|
| **单 docs task** 22→关账 | 预填 + **H1–H5**（若母 task 指定改 RECENT） | [`SKILL-harness-task.md`](SKILL-harness-task.md) |
| **Loop 子 round** | round §范围 + **H1–H5**（按母 task 指定 round） | [`SKILL-harness-loop-batch.md`](SKILL-harness-loop-batch.md) |
| **Loop META 后** | **H1–H5** + Loop README / REPORT | loop-batch §长 Loop 完成汇报 |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-13 | v1.1：H2 与 VERIFY 对齐 Hub 纪律（`done/README.md` + `done_by_domain` · 禁止 `_views/done.md` 长列表）；来源：`task_governance_tasks_done_index_hygiene_v1.md` |
| 2026-05-27 | v1 草案：预填模板 + 关账 hygiene H1–H6（T4+L2 Loop 蒸馏） |

---

## 给 Cursor

`docs-governance`、关账 hygiene、reinspect 命名、RECENT、_views、纯 docs task
