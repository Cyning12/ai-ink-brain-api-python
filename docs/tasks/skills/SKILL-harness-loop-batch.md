# SKILL：Harness Loop Batch（母单 + 多子 task · 单 PR）

> **SKILL ID**：`harness-loop-batch`  
> **状态**：`draft`（人审前草案；**未**经第二次 Loop 验证前 **不得**标 `accepted`）  
> **适用阶段**：10 帽 **Batch 一次** → 各子 round **22→30→40→50→关账** → 母单 **META** 关账；**禁止**执行阶段再开 10。  
> **Cursor 项目 skill**：[`.cursor/skills/harness-loop-batch/SKILL.md`](../../../.cursor/skills/harness-loop-batch/SKILL.md)。

---

## 来源与目录（模板 vs 实例）

| 层级 | 说明 | 路径 |
|------|------|------|
| **实例（试点）** | 第一次完整 Loop 的落盘与关账证据 | task：[`../done/task_harness_wiki_loop_a1_a4_v1.md`](../done/task_harness_wiki_loop_a1_a4_v1.md) · invoke：[`../../harness/invokes/by-task/wiki-loop-a1-a4/`](../../harness/invokes/by-task/wiki-loop-a1-a4/) |
| **新 Loop 实例** | 从试点 **复制改编** 到 | `docs/harness/invokes/by-task/<loop-slug>/` |
| **本 SKILL** | 模式与字段真值；**不**替代实例目录内 Prompt 正文 | 本文 |

> **round 命名（文档层）**：**R1…Rn + META**（n = 子 task 数，可变）。  
> **试点示例**：Wiki Loop 用 **A1–A4** 表示 R1–R4，下文出现 A1/A4 时均指「示例实例」，非强制代号。

---

## 何时选用

| 适用 | 不适用 |
|------|--------|
| 多个 **docs / 治理** 子 task，**单 PR**、固定顺序 | 单 task、改 `api/` 的 `test_strategy: required` 实现 |
| 子 task 间有 **占位回填**（如 R1 产出 → R2 规范） | 改 Harness 帽子 prompts 正文（用 `harness-task`） |
| 希望 **Batch-10 起草一次**，执行走 Loop | 跨仓多 git 根无协调 |

---

## 工件清单（模式名 · N 子 task 可变）

在新目录 `docs/harness/invokes/by-task/<loop-slug>/` 中维护：

| 模式文件名 | 职责 |
|------------|------|
| `PROMPT_BATCH_10_<loop-slug>_v1.md` | 一次性：母 task + **N** 个子 task 初稿（N 由 Batch 定义，非固定 4） |
| `LOOP_MANIFEST.md` | round **R1…Rn + META** → task_path / slug / freeze_id / 占位回填 |
| `PROMPT_START_<loop-slug>_full_chain_v1.md` | **全链启动（推荐）**：**R1** 粘贴一次 + 【授权】cross-round |
| `PROMPT_LOOP_22_to_CLOSE_v1.md` | **单 round 模板**（可跨 Loop 复用文件名；**无**会话级【授权】） |
| `README.md` | 本实例流程索引 |

**试点实例对照**（仅示例）：

| 模式 | Wiki Loop 实例文件名 |
|------|----------------------|
| `PROMPT_BATCH_10_<loop-slug>_v1` | `PROMPT_BATCH_10_four_tasks_v1.md` |
| `PROMPT_START_<loop-slug>_full_chain_v1` | `PROMPT_START_loop_a1_full_chain_v1.md` |

---

## Harness 默认值

### 母 task（编排）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 交付 docs；母 task 不直接改业务正文 |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/<loop-slug>-v1`（示例） |
| **human_gate** | `HG-LOOP-BATCH` · 仅母 task；子 task 写「继承母闸」 |

### 子 task（docs / 治理）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` + 一行 note |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | 与母 task 相同（单 PR） |

---

## 流程（三选一 · 勿写死「三会话」）

人/Agent 按场景择一；**可**在同一物理会话内完成多段（如 Batch 后立即全链）。

```text
[A · Batch 一次 · 必做（每个 Loop 一次）]
  PROMPT_BATCH_10_<loop-slug> → 母 + N 子 active/task_*.md + invoke_10_batch → commit
  HG-LOOP-BATCH = pending → 人 approved → commit（建议人单独 commit gate）

[B · 全链一次 · 推荐]
  PROMPT_START_<loop-slug>_full_chain §3（含 §2【授权】cross-round）
  → 同会话 semi_auto：R1→…→Rn 各 22→30→40→50→关账 → META 关账
  → 每帽：invoke §3 全文落盘 + commit（HANDOFF_AUTO_COMMIT）
  → 某 round 关账：按 MANIFEST 回填下一子 PLACEHOLDER（若有）

[C · 断点续跑 · 可选]
  读最新 invoke + MANIFEST 当 round → PROMPT_LOOP §3 替换占位符
  若首份 R1·22 invoke 含 cross_round_semi_auto: true → 不必再贴【授权】
  可新会话；**不**要求与 A/B 同一会话计数
```

**试点**：Wiki Loop 采用 **B**（单会话 R1→R4→META）；非唯一合法形态。

---

## cross-round【授权】放哪（硬）

| 放 | 不放 |
|----|------|
| `PROMPT_START_<loop-slug>_full_chain_v1.md` §2（会话级，**一次**） | `PROMPT_LOOP_22_to_CLOSE_v1.md` §3 模板正文 |
| 首份 **R1·22** invoke 元信息 `cross_round_semi_auto: true` | 每个 round 的 30/40/50 invoke |

**断点凭据**：Git 内首份含 `cross_round_semi_auto` 的 invoke commit。

---

## 母 task 正文必含

- 子 task **顺序表**（**R1→…→Rn→META**）+ 链 `LOOP_MANIFEST.md`
- **单 PR**、**禁止**改 `api/` / `tests/` / `docs/harness/prompts/` / CI（按 Loop 可调）
- **哪一 round 负责改排期/索引**（若适用；见下「排期」— **须母 task 明示**，非全局定律）
- 子 task 路径（active → done 后仍可用文件名链 done/）
- §验收：全部子 task `done/` 后 META 关账

---

## 子 task 正文必含

- **帽子顺序**：跳过 10；链 `PROMPT_LOOP` + MANIFEST **round=Rx**
- **failure_paths** 2–4 条（含：母闸 pending、占位未回填、越界改 api）
- **PLACEHOLDER**（若依赖上一 round）：HTML 注释块 + 「22 前须已回填」
- ### 自检结论（执行者）空表

---

## LOOP_MANIFEST 列（每 round 一行）

| 列 | 说明 |
|----|------|
| round | **R1…Rn**、**META** |
| task_path | active 路径（关账后变 done/） |
| task_slug | invoke/review 目录名 |
| freeze_id | commit message 须含 |
| 上一轮回填 | 本 task 内 PLACEHOLDER id |
| 关账后回填 | 下一 task PLACEHOLDER id |

---

## 每帽落盘（不可省略）

| 帽 | 路径 |
|----|------|
| 22 | `docs/harness/reviews/by-task/<loop-slug>/task_*_audit_R1_*.md` |
| 22/30/40/50/关账 | `docs/harness/invokes/by-task/<loop-slug>/invoke_*_{22,30,40,50,CLOSE}_*.md` |
| 50 | `docs/tasks/reinspect_results/reinspect_<slug>_*.md` |
| 关账 | `git mv` → `docs/tasks/done/` · `_views/done.md` · 排期/索引 **若** 本 round 职责含此项 |

**排期（RECENT 等）**：试点 Wiki Loop 由 **R4 / META** 改 `RECENT_TASK_SCHEDULE` — **仅该实例约定**。**须**在母 task 写清「哪 round 改哪张表」；**禁止**从 SKILL 推断全局「永远最后一轮改排期」。

**invoke 质量**：§3 须 **全文**（含元信息表），禁止仅一行标题 stub。

**commit**：每帽结束 **须 commit** 后再戴下一帽（[`HANDOFF_AUTO_COMMIT.md`](../../harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md)）。

---

## failure_paths 模板（母 task）

| # | 触发 | 行为 |
|---|------|------|
| F1 | `HG-LOOP-BATCH` = `pending` | 拒执行任一子 22/30 |
| F2 | 子 task 跳过 MANIFEST 顺序 | 22 阻塞，列依赖 |
| F3 | 占位未回填即开下一子 22 | 拒开工 |
| F4 | 误改 api/tests/prompts/CI | 50 fail / revert |

---

## 验收模板（母 task）

- [ ] 全部子 task 在 `docs/tasks/done/`，`_views/done.md` 已更新
- [ ] 每子 task 有 review + reinspect（若 task 要求 50）
- [ ] invoke 链可追溯（22→…→CLOSE × n + META）
- [ ] 单 PR；Required CI 绿（或平台 incident 时本地 pytest + 延后 merge）
- [ ] META 关账含 `HANDOFF_CLOSE_TRACE`

---

## Agent 常见偏差（试点复盘 · 抽象表述）

| 偏差 | 纠正 |
|------|------|
| R1 关账后停，要求「新对话贴 R2 Prompt」 | 已【授权】cross-round → 读 MANIFEST 同会话续 |
| invoke 仅标题、无 §3 | 换帽前写满 invoke，与 R1 首份对齐 |
| 【授权】写在 PROMPT_LOOP 模板 | 迁至 PROMPT_START；模板只描述单 round |
| 多帽结束不 commit | 每帽 HANDOFF_AUTO_COMMIT |
| 每 round 改 RECENT | **仅**母 task 指定 round 改排期 |

---

## 与相邻 SKILL

| SKILL | 关系 |
|-------|------|
| [`docs-governance`](SKILL-docs-governance.md) | 子 task 若为纯 docs，范围/非范围可叠加 |
| [`harness-task`](SKILL-harness-task.md) | 改 prompts/模板用 harness-task，非本 SKILL |
| [`harness-meta-reinspect`](SKILL-harness-meta-reinspect.md) | **可选**：META 关账 / PR 合并后做流程元复检（invoke 链、gate commit diff）；Wiki Loop 试点 **未**落盘 meta 复检 |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-26 | v1：自 Wiki Loop 关账蒸馏 · 人审前草案 |
| 2026-05-26 | v1.1：人审泛化 — 模式文件名、R1…Rn、三选一流程、排期母 task 明示、模板/实例目录 |
