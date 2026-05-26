# SKILL：Harness Loop Batch（母单 + 多子 task · 单 PR）

> **SKILL ID**：`harness-loop-batch`  
> **状态**：`draft` — 两 Loop 实例（A1–A4、B-Q3 Recheck）+ meta-reinspect **条件通过**；C3 第二 Loop 已绿，**C2 仍 FAIL**（R2/R3 的 30/40/50 stub）。晋升 `accepted` **阻塞**，须第三次 Loop C2 全绿或 meta-reinspect **C1–C7 全 pass**。  
> **适用阶段**：10 帽 **Batch 一次** → 各子 round **22→30→40→50→关账** → 母单 **META** 关账；**禁止**执行阶段再开 10。  
> **Cursor 项目 skill**：[`.cursor/skills/harness-loop-batch/SKILL.md`](../../../.cursor/skills/harness-loop-batch/SKILL.md)。

---

## 来源与目录（模板 vs 实例）

| 层级 | 说明 | 路径 |
|------|------|------|
| **实例 1（试点）** | 第一次完整 Loop | task：[`../done/task_harness_wiki_loop_a1_a4_v1.md`](../done/task_harness_wiki_loop_a1_a4_v1.md) · invoke：[`../../harness/invokes/by-task/wiki-loop-a1-a4/`](../../harness/invokes/by-task/wiki-loop-a1-a4/) |
| **实例 2（第二 Loop）** | B-Q3 Recheck + meta-reinspect | task：[`../done/task_harness_wiki_loop_bq3_recheck_v1.md`](../done/task_harness_wiki_loop_bq3_recheck_v1.md) · invoke：[`../../harness/invokes/by-task/wiki-loop-bq3-recheck/`](../../harness/invokes/by-task/wiki-loop-bq3-recheck/) · meta-reinspect：[`../reinspect_results/reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md`](../reinspect_results/reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md) |
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
| `PROMPT_START_<loop-slug>_batch10_only_v1.md` | **仅 Batch-10**（可选）：落盘 N+1 task 后 **停**；不链 22 |
| `PROMPT_LOOP_22_to_CLOSE_v1.md` | **单 round 模板**（可跨 Loop 复用文件名；**无**会话级【授权】） |
| `README.md` | 本实例流程索引 |

**试点实例对照**（仅示例）：

| 模式 | Wiki Loop 实例文件名 |
|------|----------------------|
| `PROMPT_BATCH_10_<loop-slug>_v1` | `PROMPT_BATCH_10_four_tasks_v1.md` |
| `PROMPT_START_<loop-slug>_full_chain_v1` | `PROMPT_START_loop_a1_full_chain_v1.md` |
| `PROMPT_START_<loop-slug>_batch10_only_v1` | `PROMPT_START_new_agent_batch10_only_v1.md` |

---

## Batch-10 Prompt 正文必含（`PROMPT_BATCH_10_<loop-slug>_v1` §3）

> 新 Loop **不必**从试点实例反推；按下列字段写 ` ```text ` 可复制块即可。

| 块 | 必含内容 |
|----|----------|
| **角色与纪律** | 10 帽 Batch；引用 `10-requirements`、`TASK_TEMPLATE`、`SKILL-docs-governance`、HARNESS §5；**禁止**本 Prompt 内执行 22/30 |
| **开帽** | invoke 落盘路径 `invoke_*_10_batch_*` |
| **背景 1 段** | 为何 Loop、单 PR、N 个子 task 主题（业务相关） |
| **须落盘文件列表** | **1 母 + N 子** `docs/tasks/active/task_*.md`（路径 + freeze_id + task_slug） |
| **母 task 字段** | `HG-LOOP-BATCH` = **`pending`**；子单顺序 R1…Rn→META；链 MANIFEST / PROMPT_LOOP |
| **每子 task 字段** | Harness 表、`not_applicable`、继承母闸、跳过 10、范围/非范围/验收 `- [ ]`/failure_paths/自检空表 |
| **占位** | 若 Rx 依赖 R(x-1)：子 task 内 `<!-- PLACEHOLDER:... -->` 块 |
| **commit** | 五（或 N+1）task + invoke；message 含母 `freeze_id` |
| **停** | 勿执行 22；下一棒 = 人批闸 → `PROMPT_START_*_full_chain` 或 `PROMPT_LOOP` round=R1 |

**示例一句（背景）**：「Multi 结论建议补 ingest 字段；本 Batch 起草 N 个 docs 子单，执行走 Loop。」

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
| **human_gate** | `HG-LOOP-BATCH` · **仅母 task**；子 task 写「继承母闸」 |

**`HG-LOOP-BATCH` 人批口径（统一）**：

1. **仅人** 将母 task 表中 `HG-LOOP-BATCH` 的 `status` 从 `pending` 改为 `approved`（**禁止** Agent 代填）。  
2. **建议** 该字段变更 **单独一次 commit**（便于 `git blame` 指向人）；可与其它 docs 同 PR，但 **不得**与 Agent 代填混在同一语义 commit。  
3. 子 task **不**再设 pending 的 `HG-LOOP-BATCH`；写「继承母闸 · 母 task 已 approved 后方可 22」。

**与其它 `human_gate` 的关系**：本 Loop 模式 **只定义** `HG-LOOP-BATCH`。若某 round **越界**改 `api/`（违反母 task 非范围），**不**触发「另开 HG-CODE-REVIEW」等未声明闸 — 按 **F4** **50 fail / revert / 拆出 Loop**；整 Loop 仍以 docs-only 为前提。

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
  人：母 task 内 HG-LOOP-BATCH pending→approved（建议单独 commit）→ 再启 Loop

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

**META round（母单关账）**：子 round **R1…Rn 均 `done/`** 后执行。

| 条件 | META 帽链 |
|------|-----------|
| 默认（本 SKILL · docs-only Loop） | **仅关账**：invoke `CLOSE_*` + `HANDOFF_CLOSE_TRACE` + `_views/done.md`；**不**强制 22→50 |
| 母 task `audit_profile: full` | META **须** 22→30→40→50→关账（与 [`harness-task`](SKILL-harness-task.md) 一致） |
| 任一子 round 交付含 **`api/` / `tests/` / CI** 变更 | META **须** 22→50；且该 Loop **可能不应**使用本 SKILL（见 §何时选用） |
| 试点 Wiki Loop | docs-only · META **仅关账**（已验证） |

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

**invoke 质量（概要）**：§3 须 **全文**（含元信息表），禁止仅一行标题 stub；**可执行标准**见下节 **invoke 质量门禁（C2）**。

**commit**：每帽结束 **须 commit** 后再戴下一帽（[`HANDOFF_AUTO_COMMIT.md`](../../harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md)）。

### invoke 质量门禁（C2 · 可执行）

> cross-round【授权】**不降低** 30/40/50 invoke 质量；**每换帽**须独立生成该帽 §3 全文，禁止「续跑摘要一行 + commit」。同会话 **旧帽 Prompt 仍影响新帽** 的机理与 role switch 纪律见 [`HANDOFF_SEMI_AUTO.md`](../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md) **§3.5**（通则，非 Loop 专有）。

| 检查 | pass 条件 |
|------|-----------|
| **元信息表** | 含 `round` / `hat` / `task` / `task_slug` / `freeze_id` / `git_branch` |
| **§3 正文** | ` ```text ` 块内为 **可复制 Prompt**（引用对应 `prompts/hats/{22,30,40,50}-*.md` + 本 round `PROMPT_LOOP` 步骤节），**非**交付摘要 |
| **行数 / 体量** | §3 正文 **≥ 15 行**；或 invoke 文件 **≥ 800 B**（二者满足其一；meta-reinspect 抽检常用 **≥ 15 行**） |
| **semi_auto 续跑** | R2…Rn 的 30/40/50 **与 R1 同标准**；禁止 `R2·30 交付：… commit。` 式 stub |
| **40 / 50 额外** | 须含 task 内 VERIFY 项或 `reinspect_*` 落盘路径（可抄 `PROMPT_LOOP` 步骤 3/4） |

**FAIL 时**：50 或 META meta-reinspect 标 **C2 fail**；**不要求** retrofix 已合并 Loop 的 stub invoke（记入过程债）；**下一 Loop** 或全 pass 复检须达标。

**执行层（第三批）**：实例 `PROMPT_LOOP_22_to_CLOSE_v1.md` 步骤 1–5 含 invoke C2 自检句；[`HANDOFF_AUTO_COMMIT.md`](../../harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md) commit 前体量检查；[`HANDOFF_SEMI_AUTO.md`](../../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md) P5 cross-round 不断质。

---

## failure_paths 模板（母 task）

| # | 触发 | 行为 |
|---|------|------|
| F1 | `HG-LOOP-BATCH` = `pending` | 拒执行任一子 22/30 |
| F2 | 子 task 跳过 MANIFEST 顺序 | 22 阻塞，列依赖 |
| F3 | 占位未回填即开下一子 22 | 拒开工 |
| F4 | 误改 api/tests/prompts/CI | 50 fail / revert；**不**以 HG-LOOP-BATCH 替代代码审查闸 — 应拆单或终止 Loop |
| F5 | 子 round 需 `HG-*` 未在母 task 声明 | 22 **阻塞**；Loop 只认 `HG-LOOP-BATCH` |

---

## 验收模板（母 task）

- [ ] 全部子 task 在 `docs/tasks/done/`，`_views/done.md` 已更新
- [ ] 每子 task 有 review + reinspect（若 task 要求 50）
- [ ] invoke 链可追溯（22→…→CLOSE × n + META）
- [ ] 单 PR；Required CI 绿（或平台 incident 时本地 pytest + 延后 merge）
- [ ] META 关账含 `HANDOFF_CLOSE_TRACE`

---

## SKILL 合规自检（META / 开 PR 前）

> 对照 **目标态**；实例 1/2 **未全绿** 见下节「两 Loop 过程债矩阵」。

| # | 检查 | pass 条件 |
|---|------|-----------|
| C1 | 母闸 | 母 task 中 `HG-LOOP-BATCH`：**人**改字段 `pending`→`approved`（**禁止** Agent）；**建议**单独 commit |
| C2 | invoke 链 | 每 **Rn** 有 22/30/40/50/CLOSE invoke；各 invoke §3 **满足 invoke 质量门禁**（见上节）。抽检：任一 30/40/50 若 §3 **< 15 行**或元信息表缺 `task_slug` → **FAIL** |
| C3 | cross-round | 首份 **R1·22** invoke 元信息含 `cross_round_semi_auto: true`（若走 **B** 全链） |
| C4 | 占位 | MANIFEST 所列 PLACEHOLDER 在下一 Rn **22 前**已替换 |
| C5 | 50 | 各子 task 有 `reinspect_*`（Loop 子单 **建议** 50，与 `ACCEPTANCE_LANDING` docs 关账一致） |
| C6 | 排期 | 仅母 task 指定 round 改 `RECENT` / `_views` |
| C7 | diff 纪律 | 单 PR diff 无母 task 禁止路径（`api/`、`tests/`、prompts 正文等） |

**晋升 `accepted`**（**人审** · 须 **C1–C7 全 pass**，非「条件通过」）：

```text
accepted 须同时满足其一：
1. ≥2 次独立 Loop 实例，且至少一次 C1–C7 全 pass（含 C2 invoke 质量门禁）；或
2. 1 次 Loop + harness-meta-reinspect 元复检，且 C1–C7 全 pass。

当前阻塞（仍 draft）：
- 实例 1 A1–A4：C2 stub（A2–A4 30 等）· C3 缺 cross_round 字段
- 实例 2 B-Q3：C3 ✅ · C2 ❌（R2/R3 的 30/40/50 stub）
→ 下一动作：第三次 Loop（C2 前置清单）或 meta-reinspect 全 pass 复检。
```

已合并 Loop 的 stub invoke **不要求 retrofix**；债记入过程债矩阵，下轮或复检须达标。

---

## 两 Loop 过程债矩阵（已知 · 勿复制）

| 项 | 实例 1 · A1–A4 | 实例 2 · B-Q3 Recheck | 目标态（本 SKILL） |
|----|----------------|----------------------|-------------------|
| **C3** cross_round 字段 | R1·22 **缺** | R1·22 **有** ✅ | 首份 R1·22 invoke |
| 首 round 30/40/50 | R1 部分合格 | R1 基本合格 | invoke 质量门禁 |
| **跨 round 续跑 30/40/50** | A2–A4 **stub** | R2/R3 **全 stub** ❌ | C2 |
| 业务关账 / 单 PR | done ✅ | done ✅ | 不受影响 |
| meta-reinspect | 无 | **条件通过**（C2 fail） | C1–C7 全 pass 方可 accepted |

> **⚠️ 晋升 `accepted` 硬门槛**  
> **C2 + C3 须全 pass**（见合规自检表）。**不得**因「子 task done / PR 已 merge」 alone 标 `accepted`。  
> 过程债 **不要求** retrofix 已合并 invoke；**下轮 Loop** 或 **全 pass meta-reinspect** 须达标。

第二次 Loop + meta-reinspect 已 **显式核对 C2/C3**；B-Q3 复检结论：**accepted 阻塞：C2**（见 [`reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md`](../reinspect_results/reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md)）。

---

## Agent 常见偏差（试点复盘 · 抽象表述）

| 偏差 | 纠正 |
|------|------|
| R1 关账后停，要求「新对话贴 R2 Prompt」 | 已【授权】cross-round → 读 MANIFEST 同会话续 |
| invoke 仅标题、无 §3 | 换帽前写满 invoke，与 R1·22 / R1·30 全文对齐 |
| cross-round 续跑时 30/40/50 只写「交付摘要 + commit」 | 换帽前从 `PROMPT_LOOP` **步骤 2/3/4** 展开 §3；**每帽同标准** |
| R1·22 全文、后续帽 stub | semi_auto 不断链 **也不断质** |
| 【授权】写在 PROMPT_LOOP 模板 | 迁至 PROMPT_START；模板只描述单 round |
| 多帽结束不 commit | 每帽 HANDOFF_AUTO_COMMIT |
| 每 round 改 RECENT | **仅**母 task 指定 round 改排期 |

---

## 与相邻 SKILL

| SKILL | 关系 |
|-------|------|
| [`docs-governance`](SKILL-docs-governance.md) | 子 task 若为纯 docs，范围/非范围可叠加 |
| [`harness-task`](SKILL-harness-task.md) | 改 prompts/模板用 harness-task，非本 SKILL |
| [`harness-meta-reinspect`](SKILL-harness-meta-reinspect.md) | META 关账 / PR 合并后 **可选**流程元复检；B-Q3 已落盘 [`reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md`](../reinspect_results/reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md) → **条件通过**（C2 fail，**不**等于 accepted） |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-26 | v1：自 Wiki Loop 关账蒸馏 · 人审前草案 |
| 2026-05-26 | v1.1：人审泛化 — 模式文件名、R1…Rn、三选一流程、排期母 task 明示、模板/实例目录 |
| 2026-05-26 | v1.2：META 关账约定、Batch-only 入口、合规自检 C1–C7、试点过程债、accepted 晋升条件 |
| 2026-05-26 | v1.3：三方测评吸收 — Batch-10 §必含、META 判定表、HG-LOOP-BATCH 口径、F5、C2/C3 阻断警告 |
| 2026-05-26 | v1.4：第二 Loop 试点关账（Wiki Loop B-Q3 Recheck · `task/wiki-loop-bq3-recheck-v1`）— **status 仍 draft** |
| 2026-05-26 | v1.5：第二 Loop + meta-reinspect 吸收 — invoke 质量门禁（C2）、两 Loop 过程债矩阵、晋升决策树澄清；**status 仍 draft** |
| 2026-05-26 | v1.5.1：第三批联动 — `PROMPT_LOOP` / `PROMPT_START` / `HANDOFF_*` 已写入 C2 自检（执行层；**非** accepted） |
| 2026-05-26 | 第三 Loop C2 Verify 试点 @2026-05-26（invoke C2 全绿目标 · **status 仍 draft**） |
