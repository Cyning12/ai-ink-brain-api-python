# Harness 工程 V2 初版规划

> **状态**：`draft`（初版 2026-05-13；**运维收口** 见 **§10** 2026-05-14、`HARNESS_V2_P0_ACCEPTANCE.md` §6.1）  
> **范围**：工作区 `Projects/` 下与 Ink-Brain 全栈研发相关的 **多 Agent + SDD + 分级 TDD + CI 背压**；不替代各仓 `AGENTS.md`、`PROJECT_CONFIG`、`_tech_graph/`。  
> **真值**：流程与字段约定以 **本文件 + 根目录 `AGENTS.md`** 为准；实现后应更新本节 **§修订记录**。

---

## 0. 背景与目标

### 0.1 现状摘要（对照三方测评）

Inform（告知）与 Constrain（约束）在前后端子仓及工作区根已较强：`AGENTS.md`、`PROJECT_CONFIG`、`docs/_tech_graph/`、`.cursor/rules/*.mdc`、后端 manifest/跨仓契约脚本等已形成体系。基线结论见仓内 **[`Harness工程测评-Desktop-Projects-ai-ink.md`](Harness工程测评-Desktop-Projects-ai-ink.md)**（**§8** 记录 P0 落地后的 workflow 对照）。

**Verify（验证）**：**P0–P1（2026-05-13）** 已落盘 **前端** `quality.yml`（`pnpm` install → lint → **`pnpm test`**（Vitest）→ `pnpm build`）与 **后端** `pytest.yml`（`pytest -m "not intent_eval and not intent_benchmark"` + CI 环境 dummy Key / 澄清闸关闭）。**2026-05-14**：两子仓 **GitHub PR** 上 **`quality`** / **`pytest`** 已通过；**`verify-fast` 不设 Required**（见 [`HARNESS_V2_P0_ACCEPTANCE.md`](HARNESS_V2_P0_ACCEPTANCE.md) §6.1、[`VERIFICATION_CI_PATTERN.md`](VERIFICATION_CI_PATTERN.md) §5.1）。后续仍按 **§4** 维护 checklist 与测评对照。

### 0.2 V2 目标（可验收）

- **分层真源**：工作区级 Harness 文档与入口在 `Projects/docs/harness/` 与根 `AGENTS.md`；各栈 **命令与 CI** 仍在子仓落盘，避免双份漂移。
- **SDD 不变**：SPEC → task → **规格短评（`20`）** → **任务审核落盘（`22` + `reviews/`）** → 执行 → 自检（结论回填 task）→ 复检 → 人工 checklist；流程继续由各仓任务目录与 `docs/harness/reviews/` 承载。可选 **`audit_profile: post_close`**（闸 1 轻审 + 关账后统一人审）与 **`semi_auto`** 链式戴帽，见 [`prompts/HANDOFF_SEMI_AUTO.md`](prompts/HANDOFF_SEMI_AUTO.md)。
- **显式 TDD 档位**：非「默认全盘 TDD」，而在 task 中 **声明** `test_strategy`，执行与复检据此门闸。
- **CI 背压（P0 已落地）**：Ink 前后端默认分支 PR 上具备 **lint + test + build** 与 **pytest** 门禁；**P1（2026-05-13）** 起前端 **`quality`** 增补 **`pnpm test`**（Vitest）。

---

## 1. 分层落盘：配置与文档放哪

| 层级 | 路径（相对 `Projects/`） | 职责 |
|------|--------------------------|------|
| **工作区** | `AGENTS.md`、`docs/harness/*.md`、`.cursor/rules/*.mdc` | 多子仓调度、阅读顺序、Harness 规划、跨仓流程与「帽子」索引 |
| **前端** | `ai-ink-brain/AGENTS.md`、`.github/workflows/`、`package.json` | Next/TS 的 lint、build、后续 test 脚本与 CI |
| **后端** | `ai-ink-brain-api-python/AGENTS.md`、`.github/workflows/`、`pytest` | Python 单测、图谱 CI、跨仓契约 CI、后续统一 pytest job |

**原则**：根目录管 **地图与纪律**；子仓管 **可执行命令与绿灯定义**。规划类长文放 `docs/harness/`，不在根 `AGENTS.md` 堆叠全文。  
**Invoke 快照**：每顶帽子 **新开局**（首次粘贴某 `TEMPLATE-*-invoke.md` **§3** 且占位符已替换）时，将 **同一份调用正文** 落盘至 [`invokes/README.md`](invokes/README.md) 约定路径，与 `reviews/`、task **`### 自检结论`** 形成 **环节起止可追溯链**（非每轮对话必写）。

---

## 2. Harness 三支柱 + 与「帽子」关系

| 支柱 | 含义（本规划口径） | V2 动作 |
|------|-------------------|---------|
| **Inform** | 人/Agent 知道读什么、真源在哪 | 保持各仓 AGENTS + PROJECT_CONFIG + 图谱；本文件作为 Harness 专章入口 |
| **Constrain** | 行为与代码边界可机械或规则约束 | 工作区 `.cursor/rules` + 子仓 rules；task **必读路径 / 非范围** |
| **Verify** | 合并前机器可重复验证 | **前端：PR 上 lint + test + build**；**后端：PR 上 pytest（排除 slow/真 LLM marker）**；文档化「合并前必绿」清单 |

**帽子（身份 Prompt）**：属于 **Guides** 层，与三支柱 **叠加**——短 system 前缀定义角色、输入裁剪、拒开工条件；**不能替代** CI。各帽详细句柄见 **[`prompts/README.md`](prompts/README.md)**（与 §3 同步修订）；下表为硬规则摘要。

---

## 3. 角色帽子（初版目录与硬规则）

每顶帽子建议统一骨架：**身份 → 只做什么 → 禁止什么 → 输入假设 → 输出形状 → 停止条件 → 交接物**。

| 帽子 | 硬规则摘要（执行时须满足） |
|------|---------------------------|
| **需求 / 任务分析** | 任务单须含 **验收可观测**、**失败路径**、**非范围**、依赖为链接；发现文档矛盾列矛盾点，不调和叙事；须能承接 **任务审核** 的回填清单 |
| **规格 / 任务审查** | **对话内**缺口与可测性短评；契约变更标 **冻结点升级**；**不替代** `reviews/` 落盘 |
| **任务审核** | **每次**审查须产出 `docs/harness/reviews/*.md`（无阻塞亦须「零阻塞」记录）；有改动则交任务帽回填后再 **R+1**；**签收 / 关闭** 节为 **任务正式结束点**（与 task 状态一致） |
| **执行编码** | 遵守 task **必读列表**与 **test_strategy**；缺失败路径或验收不可执行 → **仅输出阻塞清单**，不写业务代码；SPEC 错误走变更请求，不静默扩 scope |
| **自检（执行者）** | 必须运行 task 所列 **命令** 并保留 **原始输出要点**；结论须回填 task **`### 自检结论（执行者）`** |
| **独立复检** | 输入以 **diff + 日志 + 验收表** 为主；逐项 pass/fail，fail 须引用证据；可引用终轮 **任务审核** 文档 **签收** 节 |
| **全局验收** | 对照 **freeze_id** 与人签 checklist |

**Invoke 快照（环节锚点）**：各帽 **新开局** 时将 **占位符已全部替换** 的 **`TEMPLATE-*-invoke.md` §3 调用体** 落盘至 **`docs/harness/invokes/`**，与 **`reviews/`**、task **`### 自检结论`** 形成 **并列可追溯链**；触发条件、命名、与审查 **`invoke_snapshot`** 互链见 **§1** 与 [`invokes/README.md`](invokes/README.md)；可复制 Prompt 内嵌条款见 [`prompts/README.md`](prompts/README.md) 各模板 **§3 第 0 条** 或全量模板 **【五·附】**。

**与 TDD 衔接**：当 `test_strategy: required` 时，执行帽要求 **先失败测试再实现**（或等价：PR 中可见测试先于/与实现同提交且曾红过）；详见 §5。

**角色帽子可复制句柄**：[`prompts/README.md`](prompts/README.md)

---

## 4. CI 与质量门（V2 批次）

### P0（高优先级 · 闭环 Verify）— **已实现（2026-05-13）**

1. **前端 `ai-ink-brain`**：`.github/workflows/quality.yml`（workflow 名 **`quality`**，job **`lint-and-build`**）— `pull_request` + `push`（`main`、`production`）：`pnpm install --frozen-lockfile` → `pnpm lint` → **`pnpm test`**（Vitest，`vitest run`）→ `pnpm build`（**P1 2026-05-13** 起在 **Test** step 执行）。
2. **后端 `ai-ink-brain-api-python`**：`.github/workflows/pytest.yml` — 同上触发：`pytest tests -m "not intent_eval and not intent_benchmark"`；`env` 内 **dummy Key**、`CHATBI_V3_LOW_CONFIDENCE_CLARIFY=false` 等与本地 `conftest` 意图对齐。

**随 P0 修复的实现细节（后端）**：`api/unified_chat.py` 中 `_sse_emit_queue_maxsize()` 下限由 `8` 改为 `1`，避免单测 `CHATBI_SSE_EMIT_QUEUE_MAX=6` 被抬到 8 导致与注释矛盾；`test_sse_incremental_queue_backpressure_emits_truncated` 的 mock `run` 补齐 `plan_execution_token` 参数，并以 `iter_bytes()` 读完全流再断言。

### P1 — **已实现（2026-05-13，v1）**

3. **前端最小单测**：已引入 **Vitest**（`pnpm test` / `pnpm test:ci` → `vitest run`），单测覆盖 `lib/` 下纯函数（如 `lib/utils.ts`、`lib/text/chunk.ts`、`lib/ai/embeddings/dimension.ts`）；与 **`quality`** workflow 中 **Test** step 对齐；与 `test_strategy` 对齐。
4. **根 `AGENTS.md` 与本节**：**「合并前必绿」** 已显式链 **`quality`**、**`pnpm test`** 及本地等价命令（见根 `AGENTS.md` §8、`HARNESS_V2_P0_ACCEPTANCE.md` §3 前端块）。

### P2

5. **可选独立 Verification job**：**已实现 YAML（可选启用）** — 子仓 `verify-fast.yml`（`name: verify-fast`）与现有 `quality` / `pytest` 并行；合并前必绿真值仍以根 `AGENTS.md` §8 为准；决策与计费见 [`VERIFICATION_CI_PATTERN.md`](VERIFICATION_CI_PATTERN.md)。
6. **`docs/harness/prompts/`**、**`docs/harness/reviews/`** 与 **`docs/harness/invokes/`**：各帽独立 md + 任务审核落盘 + **Invoke 快照** 目录，版本化；与本规划 **§1**、**§3** 同步修订。

---

## 5. 任务单扩展字段（落盘细则）

以下字段建议写入 **各子仓 task 模板**（前端 `content/tasks/README.md`、后端 `docs/tasks/README.md` 等可引用本节）。

### 5.1 `test_strategy`（测试 / TDD 分级）

| 取值 | 含义 | 执行 Agent 行为 |
|------|------|----------------|
| `required` | 本 task 涉及 **资金路径、权限、并发、已知 bug 回归、核心纯算法** 等，必须有自动化测试背书 | 先增/改 **失败可复现** 的测试再改实现；自检须含 **测试命令与通过证明** |
| `recommended` | 有测试更佳，验收以 **命令 + 人工** 为主 | 鼓励补测；不强制 red-green 顺序 |
| `not_applicable` | 纯文案、纯图谱排版、无行为变更的配置注释等 | **须一行 `test_strategy_note`** 说明原因；禁止滥用 |

**与 SDD 关系**：SPEC 定义行为与失败语义；`required` 将关键语义 **钉在测试** 上，避免「文档写了、代码没钉住」。

### 5.2 `freeze_id`（可选）

- 与根流程中的 **冻结点** 对应：实现本 task 时 **以某版 SPEC/task 为契约基准**。
- 修订记录回答「改过什么」；`freeze_id` 回答「以哪一版为准」。可简化为 **日期 + 短哈希** 或 **SPEC 文件版本表** 中的一行 ID。

### 5.3 `failure_paths`（建议小节标题）

建议 task 内独立小节，每条包含：**触发条件** → **系统行为**（含错误码或 HTTP 状态）→ **是否可重试** → **用户可见文案类型**（不强制逐字稿）。  
若缺失或不可操作化，执行帽 **拒开工**（仅输出缺口清单）。

### 5.4 `gates_before_code`（可选布尔或列表）

- 默认隐式 `true`：执行前自检 **失败路径 + 验收命令 + 必读路径** 已齐。
- 显式列出时：如 `["failure_paths", "deps_installed", "freeze_id"]`。

### 5.5 `audit_profile`（审核节奏 · 可选）

| 取值 | 含义 |
|------|------|
| `full` | 多轮任务审核（R1/R2…）；适合架构 / 跨仓 / 高风险 task |
| `post_close` | **闸 1**：初稿 task + 执行前最小 `22` R1（`human_gate`）；**流水线**：30→40→CI；**闸 2**：关账后终轮签收 + [`HANDOFF_CLOSE_TRACE`](prompts/HANDOFF_CLOSE_TRACE.md) 统一人审 |
| `human_only` | 不自动链式戴帽；关键步均 `human_gate: pending` |

详见 [`prompts/HANDOFF_SEMI_AUTO.md`](prompts/HANDOFF_SEMI_AUTO.md) §4。

### 5.6 `human_gate` / `semi_auto`（半自动 · 可选）

- **`semi_auto: true`**：允许同 Agent 在 **无 pending 人工闸** 时自动执行下一帽；**下一棒 §3 须先** 落盘 `docs/harness/invokes/` 并 commit（[`HANDOFF_SEMI_AUTO.md`](prompts/HANDOFF_SEMI_AUTO.md) §3）。  
- **`human_gate`**：表列 `human_gate_id`、`status`（`pending` \| `approved`）、`blocks_hats`；**仅人** 可将 `pending` 改为 `approved`；Agent 遇阻塞帽 **拒执行**。  
- **`git_branch`**（建议）：半自动执行所在分支名（如 `task/<slug>`），**禁止**在 `main` 上连续自动链式提交。

---

## 6. 冻结点 vs 修订记录（再次落盘）

| 概念 | 回答的问题 | 落盘位置建议 |
|------|------------|--------------|
| **修订记录** | 改过什么、何时、摘要 | SPEC / 本文件 **§修订记录** / task 尾部变更日志 |
| **冻结点** | 以哪一版契约为准做实现 | SPEC 头部或 `freeze_id`；变更契约须 **显式升级** 并回流需求侧 |

---

## 7. 复检与模型选择（摘要）

- **换模型非必须**；优先 **输入隔离**（复检不读执行过程长文）与 **结构化输出**（逐项证据）。
- 同模型不同 Agent 仍可能顺杆爬：通过 **裁剪上下文 + 强制引用 diff/日志** 缓解。

---

## 8. 与现有仓库文件的衔接

| 已有资产 | V2 中的位置 |
|----------|-------------|
| `Projects/AGENTS.md` | §8 入口；§2.3 task 扩展字段摘要 |
| `ai-ink-brain-api-python/.github/workflows/tech-graph*.yml` | 保留；与 **`pytest.yml`** 并行 |
| `docs/harness/Harness工程测评-Desktop-Projects-ai-ink.md` | 基线测评；**§8** 增补 P0 workflow 与日期 |
| `docs/harness/README.md` | 本目录索引 |
| `docs/harness/HARNESS_V2_P0_ACCEPTANCE.md` | P0 验收单（与 CI 落地同步维护） |
| `docs/harness/tasks/README.md` | 工作区 Harness **任务目录**规则（`active` / `done` / `_views`） |
| `docs/harness/prompts/README.md` | 各角色 **帽子** Prompt 索引（与 **§3** 对照；可复制为 system 前缀） |
| `docs/harness/reviews/README.md` | **任务审核** 书面产出目录规则；**签收 / 关闭** 与 task 终态对齐 |
| `docs/harness/invokes/README.md` | **新帽节 Invoke 快照**：已替换占位符的 §3 调用体落盘与命名；与 `reviews`、task 自检 **互链** |
| `docs/harness/VERIFICATION_CI_PATTERN.md` | P2 可选 **`verify-fast`** workflow 与 `quality`/`pytest` 边界、分支保护要点 |

---

## 9. 风险与非目标

- **风险**：`not_applicable` 滥用导致回归洞 → 复检帽抽查 + Code Review 人检。
- **非目标**：V2 初版 **不** 强制引入新商业工具链；**不** 替代各仓 `_tech_graph` 拓扑协议。

---

## 10. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-13 | 初版：`draft`，落盘 `docs/harness/HARNESS_V2_PLAN.md`，与根 `AGENTS.md` §2.3 / §8 联动 |
| 2026-05-13 | P0：前后端 PR CI（`quality.yml` / `pytest.yml`）；测评文 §8；SSE 队列下限与 backpressure 单测修复；`README` 索引与子仓 task README 链 §5 |
| 2026-05-13 | 验收落盘：[`HARNESS_V2_P0_ACCEPTANCE.md`](HARNESS_V2_P0_ACCEPTANCE.md)（P0 勾选与 GitHub Actions 说明） |
| 2026-05-13 | 工作区 Harness 任务单迁至 **`docs/harness/tasks/`**（`README` + `_views` + P1 `done` / P2 `active`）；`AGENTS.md` §1/§2.2/§8、前后端 `docs/tasks` 或 `content/tasks/README` 链入；前端 `_views/done` 改链至 harness `_views` |
| 2026-05-13 | P2：`docs/harness/prompts/` 角色帽子落盘（README + 5 顶帽子 md）；`docs/harness/README` 索引；§2/§3/§8 链至 `prompts/README.md` |
| 2026-05-13 | P2 项 5：`VERIFICATION_CI_PATTERN.md`；前后子仓 `verify-fast.yml`（与 `quality`/`pytest` 对齐）；`README` 索引；§4/§8/§10 更新 |
| 2026-05-13 | **任务审核**：`prompts/22-task-audit.md`、`reviews/README.md`；§0.2 SDD、§3 增补 **任务审核** 与自检回填、§4 P2-6、§8 索引；`prompts/README` / `docs/harness/README` 链入 `reviews` |
| 2026-05-14 | **运维收口**：前后端仓库 PR 上 **`quality`** / **`pytest`** 已通过；**`verify-fast` 不设 Required**（与 `VERIFICATION_CI_PATTERN.md` 推荐策略 1 一致）；**无常驻 Harness-only `active` 任务**为预期态，日常纪律在各子仓 task（`HARNESS_V2_PLAN.md` §5）中落实；详见 [`HARNESS_V2_P0_ACCEPTANCE.md`](HARNESS_V2_P0_ACCEPTANCE.md) §6.1、`docs/harness/tasks/README.md`「当前状态」 |
| 2026-05-14 | **Invoke 快照**：新增 [`invokes/README.md`](invokes/README.md)；§1 原则、`§8` 索引、`reviews` README 与 `docs/harness/README` 互链 |
| 2026-05-14 | §3 表后脚注 **Invoke 快照**（链 §1、`invokes/`、`prompts` 各 `TEMPLATE-*-invoke` §3）；§4 **P2-6** 增补 `invokes/` 与 §1、§3 同步修订 |
| 2026-05-17 | §5.5 `audit_profile`、§5.6 `human_gate` / `semi_auto`；§0.2 链 [`HANDOFF_SEMI_AUTO.md`](prompts/HANDOFF_SEMI_AUTO.md) |

---

## 给 Cursor 的稳定关键词

`Harness`、`Verify`、`verification`、`verify-fast`、`test_strategy`、`freeze_id`、`failure_paths`、`gates_before_code`、`audit_profile`、`human_gate`、`semi_auto`、`HANDOFF_SEMI_AUTO`、`CI`、`帽子`、`prompts`、`reviews`、`invokes`、`invoke 快照`、`任务审核`、`签收`、`SDD`、`TDD`、`自检结论`
