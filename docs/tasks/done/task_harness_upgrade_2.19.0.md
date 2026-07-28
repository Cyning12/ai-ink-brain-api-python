# Task：Harness 升级至 2.19.0 · lint-wiki-delta

> **状态**：`completed`  
> **类型**：基础设施（过程轨 upgrade + 文档对齐）  
> **关联**：npm `@cyning/harness@2.19.0` · `task lint-wiki-delta` · 前置 `task/harness-upgrade-2-18-migrate`（PR #238）  
> **Open Folder**：`ai-ink-brain-api-python/`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness-upgrade-2.19.0` |
| **git_branch** | `task/harness-upgrade-2-19-0` |
| **graph_change_layer** | `none` |
| **graph_delta** | `none` |
| **graph_delta_note** | 仅过程轨 / 钉版本 / 文档；不改业务图谱 |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 本波只升版本 + lint-wiki-delta；未改 `docs/coding_wiki/`（RUNBOOK POINTER 落在 `docs/harness/`） |
| **review_hat** | `20` |
| **thinking_profile** | `shortest` |
| **invoke_retention_profile** | `minimal` |
| **required_invoke_hats** | `30` |
| **experience_capture** | `recommended` |
| **test_strategy** | `recommended` |
| **test_strategy_note** | `upgrade --yes`；`check`；`task lint-wiki-delta --scope all`；`ruff` / `pytest`（本仓惯例） |
| **code_quality_bar** | `not_applicable` |
| **freeze_id** | `HARNESS-UPGRADE-2.19.0@2026-07-28` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **orchestration** | Cursor Agent · 棒 A 升级 |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-GRAPH-MODULES** | approved | **30** | 00 代签：仅过程轨，不改模块边界 |
| **HG-TASK-DRAFT** | approved | 22-R1 | 维护者：升 2.19.0 + 字段扫描 + overlay |
| **HG-AUDIT-R1** | approved | **30** | 00 代签：无业务 API 变更 |

---

## 背景与目标

在已钉 `@cyning/harness@2.18.0` 且存量 `wiki_delta` 已补的前提下，一把升到 **2.19.0**，跑 `task lint-wiki-delta --scope all`，恢复 upgrade 冲掉的 overlay，跑本仓质量门。

**完成态**：

- [x] `upgrade --yes --target .`（不带 `--ide`）→ manifest **2.19.0**
- [x] overlay 恢复（AGENTS / CLAUDE / FRAGMENT_30 / `06-harness-pointer` / `11-coding-wiki-readorder` / prompts README）
- [x] `check` → 已是最新
- [x] `lint-wiki-delta --scope all` → missing=0 · PASS（补齐 10 个遗漏归档/PROMPT/RUNBOOK）
- [x] `harness.pin.json` → 2.19.0
- [x] 拷贝 RUNBOOK POINTER 至 `docs/harness/`（**未**覆盖 `docs/coding_wiki/`）
- [x] ruff / pytest 质量门（见 invoke）

**不做**：用 ops-desk 模板覆盖 `coding_wiki`；改 `profile.wiki=true`；关闭其它 active 业务 task；默认 `--allow-wiki-gap`

---

## 失败路径

| 触发条件 | 系统行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- |
| lint-wiki-delta missing>0 | 补 `wiki_delta` 后再关 | 是 | CLI FAIL |
| upgrade 冲 overlay | 从升级前快照恢复 | 是 | diff 可见 |
| pytest 预存红（非本波） | 记摩擦，不改业务 API | 视情况 | CI |

---

## 验收标准

- [x] manifest / pin = `2.19.0` · `check` 已是最新
- [x] `lint-wiki-delta --scope all` PASS · missing=0
- [x] overlay 与升级前一致（AGENTS harness 段 · FRAGMENT · wiki 读序规则）
- [x] `docs/coding_wiki/` **无**本波 diff
- [x] 仅本 upgrade task 走 `task close --file … --yes`（禁止 `--target .`）

---

### 自检结论（执行者）

| 项 | 内容 |
| --- | --- |
| **日期** | 2026-07-28 |
| **结论** | **PASS · 建议 CLOSE + PR** |
| **manifest** | `2.19.0`（from `2.18.0`） |
| **lint-wiki-delta** | scanned=197 · missing=0 · PASS |
| **coding_wiki** | 未改动 |

### 经验总结

- 每次 `upgrade` 后必 diff 并恢复 AGENTS / FRAGMENT / Cursor 规则 overlay。
- `lint-wiki-delta --scope all` 会扫到 `done_*` / `*_AGENT_PROMPT` / `*_RUNBOOK` / `Task 04.md` 等非标准名；缺字段须补，勿假设仅 `task_*.md`。
- `task close` 的 `--target` 是归档目标路径，**不是**仓根；关账用 `--file <task> --yes`。

### KPI

| 项 | 分 |
| --- | --- |
| Task_KPI% | 100 |

## CLOSE

| 项 | 内容 |
| --- | --- |
| **日期** | 2026-07-28 |
| **PR** | （开 PR 后回填） |
| **manifest** | `2.19.0` |
