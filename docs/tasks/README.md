# docs/tasks/ 使用规则（v1）

> 目标：让新任务“落盘位置一致、状态可追踪、索引可直达”，并避免 `active/` 长期堆积。

---

## 最近任务安排（排期真值）

**近期执行顺序、Harness P0、active 清单与时间线** 以 **[`RECENT_TASK_SCHEDULE.md`](RECENT_TASK_SCHEDULE.md)** 为准；规划或 `@task` 前先读该表，再打开具体 `active/task_*.md`。

**编码规范 L2（后端 · active）**：[`../standards/CODING_BACKEND_L2_v1_zh.md`](../standards/CODING_BACKEND_L2_v1_zh.md) · 索引 [`../standards/README.md`](../standards/README.md)

**写 task · 编码读序**：通用 [`GUIDANCE_task_coding_standards_v1_zh.md`](../../../docs/harness/guides/GUIDANCE_task_coding_standards_v1_zh.md) · 后端切片 [`GUIDANCE_backend_task_coding_l2_v1_zh.md`](../../../docs/harness/guides/GUIDANCE_backend_task_coding_l2_v1_zh.md)

**编码规范排期（§1.5）**：

- **P3+P4**：[`done/task_standards_backend_p3_p4_l3_ruff_v1.md`](done/task_standards_backend_p3_p4_l3_ruff_v1.md) · **done**（PR [#145](https://github.com/Cyning12/ai-ink-brain-api-python/pull/145) · 2026-06-09）
- **Tech-debt Epic（模块拆分）**：[`done/task_standards_backend_api_modularization_manifest_v1.md`](done/task_standards_backend_api_modularization_manifest_v1.md) · **Epic CLOSE**（W1～W8 done · 2026-06-09）

**Wiki 排期导航（L2 · 防孤岛）**：[`../coding_wiki/concepts/task-schedule-ink-backend.md`](../coding_wiki/concepts/task-schedule-ink-backend.md) — pointer 至 RECENT，**不**替代排期真值。

### active task 头建议字段（2026-05-29 起）

| 字段 | 说明 |
|------|------|
| **schedule_ref** | RECENT 锚点，如 `§1.1 #0b` |
| **epic** | Epic 归属，如 `ChatBI V3 · P2 韧性` |
| **blocked_by** / **blocks** | 任务先后（技术依赖仍走 L0 `graph_query`） |

与 Harness 元信息 `task_slug` · `git_branch` · `freeze_id` 并列维护。

---

## 工作区 Harness 任务（不在本目录）

与 **跨子仓流程 / CI 门禁对齐** 相关的 Harness **任务单** 仍统一在工作区：

- **`../../../docs/harness/tasks/active/`**、**`../../../docs/harness/tasks/done/`**  
- 索引：**[`../../../docs/harness/tasks/README.md`](../../../docs/harness/tasks/README.md)**

**帽子 Prompt / TEMPLATE / 链式常模** 已内嵌本仓，开发时读：

- **[`../harness/README.md`](../harness/README.md)** → **[`../harness/prompts/README.md`](../harness/prompts/README.md)** → [`SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md)（**全面生效**）
- **`semi_auto` 已 deprecated**（历史见 [`HANDOFF_SEMI_AUTO.md`](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)）

本目录 **`docs/tasks/`** 仅承载 **本后端仓** 任务；invoke / review 落盘见 **`docs/harness/invokes/`**、**`docs/harness/reviews/`**。

**Coding Wiki（关账后编译层 · L2）**：[`../coding_wiki/index.md`](../coding_wiki/index.md)

---

## 目录结构（以当前仓为准）

```
docs/tasks/
  README.md                # 本文件：落盘规则
  RECENT_TASK_SCHEDULE.md  # 最近任务安排表（排期真值）
  _views/                  # 状态视图索引（聚合，不改原任务正文）
  active/                  # 设计中/待开始/进行中（task_*.md）
  done/                    # 已完成（task_*.md）；本仓任务的**归档目录**（相对 `active/`）
  specs/                   # 规格文档（SPEC-*.md）
  templates/               # 模板（TASK_TEMPLATE.md）
  skills/                  # 蒸馏 SKILL 索引与类型说明（见 skills/README.md）
  legacy/                  # 历史命名/缺少状态/待补齐字段
  review_results/          # 审查帽输出归档（见该目录 README）；可交需求帽回填 task/SPEC
  reinspect_results/       # 独立复检帽输出归档（见该目录 README）；必要时交需求帽回填
```

### 工程纪律索引（防口头约定漂移）

- **ChatBI：新功能以 SSE 优先（团队纪律 task）**：[`done/task_engineering_chatbi_sse_first_v1.md`](done/task_engineering_chatbi_sse_first_v1.md) — 历史审查见 [`../diary/harness-archive/`](../diary/harness-archive/README.md)；**新 task** 22 帽落盘 [`../harness/reviews/`](../harness/reviews/README.md)。

### 审查与复检产出（非 task 单）

- **`review_results/`**：规格/任务 **审查帽**（`20`）结论归档；详见 [`review_results/README.md`](review_results/README.md)。  
- **`../harness/reviews/`**：**22 帽任务审核**（**仅本仓** `docs/tasks/` 绑定 task；勿混放总项目/他仓审查）。  
- **`reinspect_results/`**：**50 帽三方复检** — 关账必选。  
- **Harness**：[`../harness/README.md`](../harness/README.md)；10 结束输出 **下一棒 A（22）+ B（30）**，由人择一。

审查回填清单由 **需求帽**（[`../harness/prompts/hats/10-requirements.md`](../harness/prompts/hats/10-requirements.md)）更新本仓 `docs/tasks/`、`docs/spec/`。

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

## 什么时候从 active 移到 done（归档目录）

当任务验收通过（满足任务文档里的“验收标准”）后，**必须**完成归档：`done/` 为本仓任务单的归档目录，与仍在推进的 `active/` 分离，避免 Agent 误判「仍在进行」。

### 任务归档流程（维护检查清单）

按顺序执行（可随同一提交完成）：

1. **核对验收**：任务正文「验收标准」已全部勾选为完成，或等价说明已写明例外与签核人/日期。  
2. **更新头部状态**：将 `> **状态**：...` 改为 `done（YYYY-MM-DD 验收通过）`（日期为实际验收日）。  
3. **移动文件**：在仓库根执行 `git mv docs/tasks/active/<文件名>.md docs/tasks/done/`，**禁止**仅复制内容而遗留 `active/` 同名文件。  
   - **硬规则**：**禁止**只把头部改成 `done` 而文件仍留在 `active/`（会误导 Agent）；**`done` 状态与 `git mv` 须在同一提交内完成**，真值以 **目录位置 + 头部状态** 双一致为准。  
   - **禁止瘦身**：移入 `done/` 后仍须保留 Harness 元信息（含 `test_strategy`）、§失败路径、§验收标准；**不可**新建仅摘要版 done 稿（CI `task_validate` 会 FAIL）。  
4. **机械校验（push 前必跑）**：`python tools/harness_task_validate.py docs/tasks/done/<文件>.md` → **OK**（与 CI job `task_validate` 同脚本；`verify-tech-graph` / `pytest` **不能**替代）。  
5. **更新已完成索引**：
   - 在 `docs/tasks/done/README.md` Hub 对应域表追加一行（日期 · 链接 · freeze_id / 一行摘要）。
   - 同步在 `docs/tasks/_views/done_by_domain.md` 对应域表追加一行。
   - **`docs/tasks/_views/done.md` 保持薄指针（≤15 行），禁止追加长列表**。  
6. **若任务曾列入进行中视图**：检查 `docs/tasks/_views/in_progress.md`，移除或更新对该任务的引用（避免双轨）。  
7. **配对前端 / 跨仓任务**：若头部或正文引用了 `ai-ink-brain/content/tasks/active/task_*.md`，须在 `ai-ink-brain` 仓按 **`content/tasks/README.md`** 执行归档：**`git mv`** 至 **`content/tasks/done/`**，更新 **`content/tasks/_views/done.md`**，头部 **`状态`** 改为 `done（YYYY-MM-DD 验收通过）`。（**不**移动 `docs/spec/` 下规格文件，规格持续维护、不因任务归档而搬迁。）

> 说明：`_views/*.md` 只做链接聚合，不作为真值；真值以任务文件头部 `状态` + 文件所在目录（`active/` 或 `done/`）为准。

### 域子目录 + Hub 纪律（P0 起生效）

为降低 `done/` 扁平堆积与 `_views/done.md` 过长导致的浏览成本，引入 **域 Hub** 模式：

- **日常浏览入口**：`docs/tasks/done/README.md`（按域分组表）。
- **薄指针**：`docs/tasks/_views/done.md` ≤15 行，只链 Hub 与 `done_by_domain.md`。
- **分组视图**：`docs/tasks/_views/done_by_domain.md` 与 Hub 语义一致。
- **P0 不 mass `git mv`**：物理文件仍扁平存放于 `done/`，Hub 与 `done_by_domain.md` 中的链接仍使用 `../done/<file>.md`。
- **P1 批量迁移**：未来子 task 将物理文件 `git mv` 到 `done/<domain>/`，届时 Hub / `done_by_domain.md` 链接同步更新。
- **域推断**：[`FRAGMENT_task_domain_infer_v1_zh.md`](../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)。

| 域 slug | 说明 | 目标目录 |
|---------|------|----------|
| `harness` | 本仓流程 / CI / 帽子 | `done/harness/` |
| `governance` | Wiki / 索引 / 治理线 | `done/governance/` |
| `chatbi` | ChatBI V2/V3 · unified chat | `done/chatbi/` |
| `engineering` | 图谱闸口 / RAG / 跨仓工程 | `done/engineering/` |
| `standards` | 编码规范 · api 模块化 Epic | `done/standards/` |
| `epics` | 母单 · MANIFEST · Loop | `done/epics/` |

---

## specs / legacy 的边界

- **`specs/`**：只放规格（`SPEC-*.md`），可被多个 task 引用。
- **`legacy/`**：只放历史遗留（命名不规范/缺少状态/待补齐字段）。后续“修复命名与状态”应通过独立 task 执行，避免一次性大改造成漂移。

---

## 视图索引维护规则（最小集）

- `docs/tasks/_views/design.md`：列出 `draft/design` 的任务 + “缺少状态字段”清单（统一维护在此）
- `docs/tasks/_views/backlog.md`：列出 `backlog`（**需求池**，排期前一览）
- `docs/tasks/_views/in_progress.md`：列出 `in_progress`
- `docs/tasks/_views/done.md`：列出 `done`

---

## `test_strategy` 默认表（理论对齐 P0）

> 真值：[`SPEC-Governance-Harness-Theory-Align-P0-v1.md`](../spec/governance/SPEC-Governance-Harness-Theory-Align-P0-v1.md) **§4**；task 头可覆盖，**22 须核对合理性**。

| 变更类型 | 默认 |
|----------|------|
| 鉴权、计费、SSE/流式背压、核心算法回归 | `required` |
| 一般 API/功能 | `recommended` |
| 纯文档、图谱排版、无行为注释 | `not_applicable` + `test_strategy_note` |

**50 硬规则**（`required` + `api/`/契约）：关账前须有 `reinspect_results/` 落盘，见 RECENT **§0.0**。

**22 抽检（P1 运维）**：每季度抽查 1～2 份 active task 的 `test_strategy` 是否与上表及变更类型一致（见 P1 SPEC §4）。

### 本仓 TDD 实践口径（2026-05-30）

> **决策稿（主）**：[`docs/diary/tmp/2026-05-30-backend-TDD-architecture-assessment.md`](../diary/tmp/2026-05-30-backend-TDD-architecture-assessment.md) — 本仓架构是否加强 TDD、分层策略、优先路线（**非** OpenSpec 引入 TDD）。  
> **现状**：制度支持分级 TDD；多数 task 为 `not_applicable`；CI 以 **全量 pytest 回归** 为主。  
> **推荐模式**：**分层验证** — L1 纯逻辑可测试先行；L2 契约同 PR 补测；L3/L4 mock + 离线 eval；**不全员 strict red-green**。

| 档位 | 本仓实际含义 |
|------|--------------|
| `required` | 安全/闸门/核心回归；须专用 pytest +（高敏）50 |
| `recommended` | **`api/` 默认档**：实现 + 补测 + CI 绿 |
| `not_applicable` | 文档/图谱/Harness 治理；**禁止**滥用于 `api/` 行为变更 |

**Scenario ID**（`TASK_TEMPLATE` §失败路径）：可测场景命名，链 `_test_manifest.json`；**不要求** strict TDD 顺序。

OpenSpec 对照（次要）：[`docs/diary/tmp/2026-05-30-Harness-TDD-OpenSpec-analysis.md`](../diary/tmp/2026-05-30-Harness-TDD-OpenSpec-analysis.md)。

---

## 行为变更 Delta（OpenSpec 借鉴 · 2026-05-30）

> **不**引入 `openspec/` 目录；在 task 内用 **ADDED / MODIFIED / REMOVED** 描述相对 `docs/spec/` 的行为增量。  
> 模板见 [`templates/TASK_TEMPLATE.md`](templates/TASK_TEMPLATE.md) **§行为变更**；关账时可手工合并进主 SPEC。  
> 与 OpenSpec 差异对照：[`docs/diary/tmp/2026-05-30-Harness-vs-OpenSpec-diff-and-optimization.md`](../diary/tmp/2026-05-30-Harness-vs-OpenSpec-diff-and-optimization.md)。  
> **P0 执行安排**（O1–O3 完成态 · Loop R1–R3）：[`docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md`](../spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md)。

---

## `semi_auto` 决策表（理论对齐 P1）

> 真值：[`SPEC-Governance-Harness-Theory-Align-P1-v1.md`](../spec/governance/SPEC-Governance-Harness-Theory-Align-P1-v1.md) **§5**；通则 [`HANDOFF_SEMI_AUTO.md`](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)。

| `semi_auto` | 适用场景 | 链式帽序 | 仍须人做 |
|-------------|----------|----------|----------|
| `true` | 小改动、纯文档、单文件治理；无 `pending` 人工闸 | `10→30→40→22`（无闸时同会话） | 终轮 **22 签收**、合并 PR、`human_gate: approved` |
| `false` | 契约 / 跨仓 / 架构 / `test_strategy: required` 含 `api/` | 每帽可新会话；默认经 **22 R1** | 各 `HG-*` 按表；**50** 关账 |

task 头 **须**显式 `semi_auto` + `audit_profile`；22 R1 核对合理性。

---

## Harness V2 · 任务单扩展字段

**模板真值**：[`templates/TASK_TEMPLATE.md`](templates/TASK_TEMPLATE.md)（含 `test_strategy`、`failure_paths`、**行为变更 Delta**、**Scenario ID**、**规划 artifact**（大 task 可选）、`semi_auto`、`human_gate`、`audit_profile`、`git_branch` 等）；与 **`docs/harness/HARNESS_V2_PLAN.md` §5** 对齐。

新建 task 时 **复制模板** 再改占位符；链式常模见 [`SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md) + [`../harness/prompts/PROMPT_*_chain_serial_*`](../harness/prompts/README.md)。**`semi_auto` 已 deprecated**（历史见 [`HANDOFF_SEMI_AUTO.md`](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)）。

### 蒸馏 SKILL（高频场景预填）

按任务类型选用预填片段，与模板骨架叠加使用；类型定义、输入输出与关账蒸馏口径见 **[`skills/README.md`](skills/README.md)**。

---

## `human_gate` 场景速查

> **真值**：字段语义见 [`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5.6**；Agent 行为见 [`../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md`](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md) **§2**。  
> **硬规则**：**仅人** 可将 `status` 从 `pending` 改为 `approved`；Agent **禁止**代填、禁止勾选「已人工审核」。

| gate_id | status | blocks_hats | 典型场景 | 谁改 approved |
|---------|--------|-------------|----------|---------------|
| `HG-TASK-DRAFT` | `pending` / `approved` | `22-R1`, `30` | 10 帽产出 task 初稿；人扫字段完整性、验收可执行性、`failure_paths` 后再放行执行 | **任务负责人 / 审阅人**（扫完 task 正文与 Harness 元信息表） |
| `HG-AUDIT-R1` | `pending` / `approved` | `30` | 22 帽 R1 审查落盘 `docs/harness/reviews/` 后；执行编码前确认零阻塞或阻塞已回填 | **审查签收人**（读过 R1 review 全文） |
| `HG-REINSPECT` | `pending` / `approved` | `done`, `50`（可选） | 50 帽复检落盘 `reinspect_results/` 后；关账归档或合并 PR 前 | **复检签收人 / Tech Lead** |
| `HG-GLOBAL-SIGNOFF` | `pending` / `approved` | 合并 `main`（可选） | 关账 `HANDOFF_CLOSE_TRACE` 输出后；跨仓或大里程碑合并前总签 | **仓库维护者 / 发布负责人** |
| `HG-<自定义>` | `pending` / `approved` | task 元信息 `blocks_hats` 列明 | 产品决策、合规、外部依赖就绪等 task 自定义闸 | **task 正文或元信息表指定的签收角色** |

**Agent 开帽前**：扫描 task 与关联 `reviews/*` 中全部 `human_gate`；若计划执行的帽子 ∈ 某闸的 `blocks_hats` 且该闸 `status: pending` → **拒执行**，仅输出须人修改的 `gate_id` 与文件路径。

**落盘格式**（task 内推荐表格式，见 [`templates/TASK_TEMPLATE.md`](templates/TASK_TEMPLATE.md)）：

```markdown
| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | … |
```

---

## 常见坑（强制避免）

- 不要把已完成任务留在 `active/`（会误导新 Agent 判断“还在做”）
- 不要在任务文件里写“已完成但状态还是 pending”（状态必须与事实一致）
- 不要在 `docs/tasks/` **顶层**混放零散 `task_*.md` / `SPEC-*.md` / 模板（须进 `active/`、`done/`、`specs/`、`templates/`）；**`review_results/`、`reinspect_results/`** 为帽子产出专用子目录，见上节
