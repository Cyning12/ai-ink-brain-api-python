# Harness 通则：半自动链式执行（人工闸 + 自动戴帽）

> **用途**：同一 Agent 在 **无需人工** 的环节自动切换下一顶帽子继续执行；在 **必须人工** 的环节 **硬停止**，直至人改标识后才可继续。  
> **关联**：[`HANDOFF_AUTO_COMMIT.md`](HANDOFF_AUTO_COMMIT.md)（每步 commit）、[`HANDOFF_CLOSE_TRACE.md`](HANDOFF_CLOSE_TRACE.md)（关账回溯）、[`../invokes/README.md`](../invokes/README.md)（Prompt 落盘）。  
> **真值层级**：Guides；与 [`HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) **§5.5–§5.6** 字段对齐。

---

## 1. 总原则

| # | 原则 |
|---|------|
| P1 | **须人审**：必须在工件中写明 **`human_gate` 标识**；Agent **不得**代填 `approved`、不得勾选人检框。 |
| P2 | **不须人审**：同 Agent 可 **自动戴下一棒**；但 **下一棒 §3 Prompt 须先落盘**（`invokes/`）并 **commit**，再切换角色执行。 |
| P3 | **审核节奏**：见 **§3 `audit_profile`**——`full` 多轮 `22`；`post_close` 开头轻闸 + 关账后统一人审（§4）。 |
| P4 | **Git 形态**：半自动链式执行 **强烈建议** 在 **任务专用分支** 上进行（§5），`main` 仅通过 PR / 人签合并。 |

---

## 2. 人工闸 `human_gate`（必须人改标识才继续）

### 2.1 何时必须设闸

| 场景 | 建议 `gate_id` 示例 | 阻塞的下一棒 |
|------|---------------------|--------------|
| 初稿 task / SPEC 人扫 | `HG-TASK-DRAFT` | `22` R1、`30` |
| 22 书面审 R1 通过前 | `HG-AUDIT-R1` | `30` |
| 三方复检落盘后 | `HG-REINSPECT` | `done`、合并 PR |
| 关账前人签（可选） | `HG-GLOBAL-SIGNOFF` | 合并 `main` |
| 用户自定义 | `HG-<自定义>` | task 元信息 `blocks_hats` 列出 |

### 2.2 落盘格式（二选一，同一 task 内请统一）

**A. task 头部元信息表（推荐）**

```markdown
| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-AUDIT-R1 | pending | 30 | R1 审查后人改 approved |
```

- **`status`** 仅允许：`pending` | `approved`（**禁止** `skipped` 除非 task 明文允许且人写过理由）。  
- **`blocks_hats`**：帽子编号列表，如 `30`、`40`、`22-R2`；Agent 在 **status ≠ approved** 时 **拒执行** 所列帽子。

**B. 审查 md / 清单中的机器可读行**

```markdown
<!-- human_gate:HG-AUDIT-R1 status=pending blocks=30 -->
```

人审通过后 **仅改一行**：

```markdown
<!-- human_gate:HG-AUDIT-R1 status=approved blocks=30 -->
```

或把同行 `- [ ]` 改为 `- [x]` **且** 邻行含 `HG-AUDIT-R1` 关键字（见 `reviews/` 模板建议）。

### 2.3 Agent 行为（硬规则）

1. 开帽前扫描 **task + 本轮关联 `reviews/*`** 中全部 `human_gate`。  
2. 若下一计划帽子 ∈ 某闸的 `blocks_hats` 且该闸 `status: pending` → **仅输出**：阻塞说明、**须人修改的路径与标识**、当前 gate 表；**禁止**写业务代码、禁止自动戴帽。  
3. **禁止**将 `pending` 改为 `approved`；**禁止**替用户勾选「已人工审核」。  
4. 人改后 **新会话或同会话用户明示「HG-xxx 已 approved」** 方可继续；Agent 须 **复读** 工件确认 `status: approved` 后再落盘下一 invoke。

---

## 3. 自动戴帽（同 Agent、无须人审的下一步）

### 3.1 前置条件（须同时满足）

| # | 条件 |
|---|------|
| A1 | task 元信息 **`semi_auto: true`**（或审查/用户明示「本段可链式自动」） |
| A2 | 下一棒 **不在** 任何 `pending` 的 `human_gate.blocks_hats` 中 |
| A3 | 本轮验收 / 自检（若适用）已通过，或下一棒为纯文档帽且 task 允许 |
| A4 | 无用户「停」「不要自动下一棒」类指令 |

### 3.2 顺序（不可打乱）

```text
1. 完成本帽交付物（代码 / 审查 md / 自检回填 / **50→`reinspect_results/*.md`** 等）
2. 生成下一棒 §3 全文（占位符已替换）
3. 落盘 → `docs/harness/invokes/invoke_*`（新帽节）及 **50 帽** → `docs/tasks/reinspect_results/reinspect_*.md`（见 [`../ACCEPTANCE_LANDING.md`](../ACCEPTANCE_LANDING.md)）
4. 按 HANDOFF_AUTO_COMMIT 仅 add 本轮路径并 commit
5. 切换角色语义，按刚落盘的 invoke 执行下一帽（同 Agent 会话）
```

**复盘**：任何事后追问「当时怎么调用的」→ 以 **invoke 文件 commit** 为准，不以对话记忆为准。

### 3.3 与「对话内 Prompt」关系

- 自动链式时：**对话可摘要**，但 **invoke 须完整 §3**；禁止只 commit 代码不落 invoke。  
- 若下一步是 **关账无下一棒**：改走 [`HANDOFF_CLOSE_TRACE.md`](HANDOFF_CLOSE_TRACE.md)，不生成空 invoke。

### 3.4 每棒状态栏（版本 B · 对话默认）

> **裁决**：Harness 评价回复 **§3.2** — 版本 **B**（结构化多行）为 **每帽结束** 的对话默认输出；与 [`HANDOFF_CLOSE_TRACE.md`](HANDOFF_CLOSE_TRACE.md) **分工**：状态栏 = 会话内「**现在在哪**」；CLOSE_TRACE = 关账时 **全链路** commit 回溯，**互补不替代**。

#### 3.4.1 何时必须输出

| # | 时机 |
|---|------|
| S1 | **每一顶帽子** 在本轮回复 **末尾**（在「下一棒可复制 Prompt」或阻塞说明 **之前或之后** 均可，但须 **同条回复** 内可见） |
| S2 | **遇 `human_gate: pending` 硬停** 时：仍须输出状态栏，**下一棒** 填 `—（阻塞）` |
| S3 | **关账无下一棒**：**不** 用状态栏代替 CLOSE_TRACE；可最后一棒先输出状态栏，再输出 **执行路线与 Commit 回溯** |

#### 3.4.2 版本 B 格式（复制块）

标题固定为 **`📋 Harness 状态栏（版本 B）`**，正文用 **树形多行**（与 Execution Report 习惯一致）：

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：<10|20|22|30|40|50> · <短标题>
├── task：<task 文件名或 slug> · audit_profile：<full|post_close|human_only>
├── 分支：<git_branch 或 git branch --show-current>
├── human_gate：<gate_id> <pending|approved>（blocks <帽子>）· …；无则写「无」
├── 本棒交付：<本轮落盘/结论一句>
├── 下一棒：A=<路径简述> · B=<路径简述>（10 帽 **须** 给 A/B；仅一路则 B=—）
├── 推荐：（可选）<A|B>（<一行理由>）— **不得**因推荐自动执行
└── 阻塞：<无 | HG-xxx pending → 停，须改 <路径>>
```

**硬规则**：

| # | 规则 |
|---|------|
| R1 | **禁止** 用单行省略版代替 B（除非用户明示「不要状态栏」） |
| R2 | **禁止** 因「推荐」自动走路径 A/B；推荐仅标注，**人择** 不变 |
| R3 | **禁止** 在状态栏写 `human_gate: approved` 若工件仍为 `pending` |
| R4 | `semi_auto: false` 或 `human_only` 时，**下一棒** 可写 `—（须人发起）` |

#### 3.4.3 版本 C（可选 · invoke / review 锚点）

跨会话续跑时，可在 **`docs/harness/invokes/invoke_*.md` 元信息表** 或 **22 review 文首** 追加 **表格版**（与 B 语义一致，便于扫读）：

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| task | `active/task_05_*.md` |
| audit_profile | post_close |
| git_branch | `task/query-rewrite-obs` |
| human_gate | HG-AUDIT-R1 pending |
| next | A=30 · B=22-R2 |
| block | HG-AUDIT-R1 |

- **invoke 正文 §3** 仍为完整 Prompt 真值；C 表为 **摘要**，不可替代 §3。

#### 3.4.4 与各帽衔接

| 帽子 | 状态栏要点 |
|------|------------|
| **10** | **必须** 列出下一棒 **A（22）+ B（30）**；推荐行见 P0-A3 模板 |
| **22** | `human_gate` 与 `reviews/` 落盘路径写入 **本棒交付** |
| **30→40→50** | 本棒交付含命令/pytest 结论摘要；50 后下一棒常为 **关账** |
| **阻塞** | **仅** 输出状态栏 + 须改的 `gate_id` 与文件路径，**禁止** 代填 approved |

---

## 4. 审核节奏：`audit_profile`（并入 §3 两闸模型）

在 **task 头部** 增加（见 `HARNESS_V2_PLAN` §5.5）：

| 取值 | 含义 | 人工闸建议 | 中途 `22` |
|------|------|------------|-----------|
| **`full`** | 大改架构、跨仓契约、高风险 | R1、关键阶段可再加 `HG-*` | 多轮 R1/R2… |
| **`post_close`**（推荐用于工程流水线 task） | 执行期靠 CI + `40` | **HG-TASK-DRAFT**、**HG-AUDIT-R1**（执行前最小闸） | 仅 **终轮签收** + 关账回溯 |
| **`human_only`** | 纯文档 / 产品决策 | 全部关键步 `pending` | 人驱动，不自动戴帽 |

### 4.1 两闸 + 一表（`post_close` 推荐路径）

```text
[闸 0 · 人]  10 产出 **下一棒 A（22）/ B（30）** → **人择一路**
[闸 1 · 人]  若选 A：22 R1 落盘 `docs/harness/reviews/` → HG-AUDIT-R1 approved；若选 B：确认跳过 22 理由
[流水线 · 机+Agent]  semi_auto: 30 → 40 → 50（`reinspect_results/` 落盘）→ CI
[关账]  HANDOFF_CLOSE_TRACE + task done
[闸 2 · 人]  HG-REINSPECT / HG-GLOBAL-SIGNOFF → approved → 合并
```

- **闸 1** 不可替代：缺 `failure_paths`、验收不可执行时，须在 **执行前** 拦住（`22` R1 或人扫 task）。  
- **闸 2** 适合「一次看清全链路 commit」；依赖 **CLOSE_TRACE** 与 PR diff，而非每阶段开人审会。

---

## 5. Git 分支策略（半自动 **强烈建议** 多分支）

| 做法 | 说明 |
|------|------|
| **每 task 一分支** | 如 `task/<slug>` 或 `feat/<slug>`；半自动链式 **只在该分支 commit** |
| **每大阶段一分支**（可选） | 如 `feat/<slug>-p2-0` 再合入 `task/<slug>`；适合超长 task |
| **禁止** | 在 `main` / `production` 上连续自动 30→40→30 无 PR |
| **PR = 闸 2 载体** | 人读 PR + 终轮 review + CLOSE_TRACE 表；CI 绿 + `HG-*` approved 再合并 |
| **工作区 + 子仓** | 各 git 根各自分支 **同名或链式 PR**；禁止假设一次 push 覆盖两仓 |

**理由**：半自动会产生 **多 commit**；分支隔离便于丢弃错误链、对比执行路线、与「仅对话无落盘」切割。

---

## 6. task 元信息示例（可复制块）

```markdown
| 字段 | 值 |
|------|-----|
| semi_auto | true |
| audit_profile | post_close |
| git_branch | task/engineering-tech-graph-v2-graph-query-v1 |

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1 | 人已过初稿 |
| HG-AUDIT-R1 | approved | 30 | R1 零阻塞后人签 |
| HG-AUDIT-CLOSE | pending | done,50 | 关账后人签 |
```

---

## 7. 与各帽衔接（摘要）

| 帽子 | 半自动注意 |
|------|------------|
| **10** | 产出 task 时 **列出** `human_gate` 初值与 `audit_profile` |
| **22** | R1 通过时 **不得** 代改 `HG-AUDIT-R1`；终轮设 `HG-AUDIT-CLOSE` |
| **30→40** | `post_close` 下可 auto；**30 前** 必查 `HG-AUDIT-R1` |
| **50** | 常对应 `HG-GLOBAL-SIGNOFF`；通过后 CLOSE_TRACE |
| **每帽结束** | 对话输出 **§3.4 版本 B 状态栏**；关账另用 CLOSE_TRACE |

---

## 8. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-17 | v1：人工闸标识、自动戴帽前置 invoke+commit、audit_profile 两闸、多分支建议 |
| 2026-05-22 | v1.1：§3.4 每棒状态栏（版本 B 对话默认 + 版本 C invoke 可选）；与 CLOSE_TRACE 分工 |

---

## 给 Cursor

`HANDOFF_SEMI_AUTO`、`Harness 状态栏`、`版本 B`、`版本 C`、`human_gate`、`HG-`、`pending`、`approved`、`semi_auto`、`audit_profile`、`post_close`、`full`、自动戴帽、`invokes`、多分支、`task/`、`HANDOFF_CLOSE_TRACE`
