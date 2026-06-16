# Task Audit R1 · graph-yaml-p0-00-main

## 元信息

| 字段 | 值 |
|------|-----|
| **task_path** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md` |
| **audit_round** | `R1` |
| **date** | `20260616` |
| **task_slug** | `graph-yaml-p0-00-main` |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/graph-yaml-p0-00-main/invoke_20260616_22_graph-yaml-p0-00-main.md` |
| **prev_review** | `无` |
| **auditor** | `Harness 22 任务审核 Agent` |

---

## 审查结论摘要

** verdict：PASS（零阻塞）—— 建议进入 30 执行帽，但须等待维护者人工签 `HG-AUDIT-R1 approved` 后方可开工。**

本 task 为 **P0 工程试点**（YAML 作为 `00_main` 编辑源 → 生成 `.md` + diff 校验），`audit_profile: full` + `test_strategy: required`。经逐条核对：

- 10 帽思考轮 **R0–R3 已闭合**，`early_stop=yes` 理由成立（R3 已收敛方案/CI/失败路径）。
- YAML schema 方案（方案 1：YAML → .md + diff 校验）与 QNA §2、graph_v2_schema 节点/边结构 **兼容**。
- CI 策略为 **追加校验**（不改动现有 `verify-tech-graph.sh` 核心链路），符合 P0 最小 diff 原则。
- 非范围 **守住**（不删 `.ai.md`、不接 cyning-harness、仅 00_main）。
- failure_paths **F1/F2/F3 均可操作**。
- 验收标准 **可观测**（≥1 pytest、diff 校验、00_main.md 生成）。

**残余风险 3 项已书面钉住**（见「非阻塞 · 残余风险」），不影响 30 开工，但须 30 帽在实现中显式处理或书面记录。

---

## 理论对齐检查表（P0 · `GOV-HARNESS-THEORY-ALIGN-P0`）

### §3.1 任务单最小字段

| # | 检查项 | 结论 |
|---|--------|------|
| 1 | 头部 Harness 元信息表：`test_strategy` 三选一 | ✅ `required` |
| 2 | `not_applicable` 时 `test_strategy_note` 非空 | N/A（为 `required`） |
| 3 | `failure_paths` ≥1 行（触发→行为→可重试→用户可见） | ✅ 3 行（F1/F2/F3） |
| 4 | 非范围 独立小节非空 | ✅ 6 条明确 |
| 5 | 验收标准 含 合并前必绿 条 | ✅ `pytest tests -m "not intent_eval and not intent_benchmark"` |
| 6 | （P1 抽检）`semi_auto` + `audit_profile` 已填 | ✅ `audit_profile: full`，`orchestration` 已填，`semi_auto` 未出现 |

### §3.2 合并前 CI 验收条

| # | 检查项 | 结论 |
|---|--------|------|
| 1 | 验收含：`PR 上 pytest workflow 全绿` + 本地等价命令 | ✅ 验收标准第 6 条 + 合并前必绿 |
| 2 | 40 自检 / PR 链接可核对（终轮 22 不得无证明签收） | ✅ 40 自检表已预留（待 40 回填） |

### §Blocking · 高敏须人判断

| # | 检查项 | 结论 |
|---|--------|------|
| 1 | 若触达 Blocking 任一行 → 上表已核对，缺项阻塞 | ✅ 未触达 Blocking 行；task 为纯 docs/工程管线，无对外 HTTP/SSE 契约变更 |

### §3.3 独立复检（50）触发

| 变更类型 | `test_strategy` | 50 |
|----------|-----------------|-----|
| 纯 `docs/`、索引、无行为 | `not_applicable` | 可选 |
| 一般功能 | `recommended` | 22 终轮可收口；可标 `reinspect: optional` |
| `api/`、HTTP/SSE 契约、鉴权、并发/背压 | `required` | **必须** `reinspect_results/` 落盘 |

本 task 为 **纯 docs/工程管线**（YAML → .md + diff 校验），但 `test_strategy: required` 且涉及 `scripts/` 新增工具代码。50 触发判定：
- 无 `api/` 或 HTTP/SSE 契约变更 → **非**强制 50 落盘；
- 但 `test_strategy: required` + `audit_profile: full` → **建议** 50 仍执行并落盘 `reinspect_results/`（task 验收标准已列「50 reinspect 落盘」）。

| # | 检查项 | 结论 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型匹配 | ✅ `required` 合理（新增脚本 + pytest 用例） |
| 2 | `required` 且涉 `api/`/契约 → 关账前 50 已落盘或显式阻塞 | N/A（不涉及 `api/`） |

### OpenSpec × TDD 勾选项（P0 · Loop R2 · T1+T2）

| # | 检查项 | 结论 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型一致（触达 `api/` 时 非 `not_applicable`） | ✅ 不涉及 `api/`，但 `required` 合理 |
| 2 | §行为变更 Delta 已填 或 显式「无」 | ✅ 显式「无 — 纯工程/文档管线；运行时 API 行为不变」 |
| 3 | `failure_paths` 含 **Scenario ID** 列且非空 | ✅ `fp-yaml-parse` / `fp-graph-diff` / `fp-gate-draft` |
| 4 | 验收含 **合并前 pytest** 条（或 task 模板等价表述） | ✅ 合并前必绿 + pytest 命令 |

---

## 思考轮审查（10 帽 R0–R3）

### 闭合性核对

| 轮次 | 状态 | 内容摘要 | 闭合判定 |
|------|------|----------|----------|
| R0 | ✅ 已填 | 范围/非范围清晰；缺口 3 项（YAML schema 未定、脚本路径未确认、AUTO 块策略待决策） | 缺口已落入 R2/R3 决策或残余风险 |
| R1 | ✅ 已填 | 00_main 26 节点 / 36 边（depends_on 32 + branches 4）；4 边带 anchors；CI 通过 `verify-tech-graph.sh` | 数据与 graph.json 一致 |
| R2 | ✅ 已填 | 方案 1（YAML→MD + diff 校验）推荐；方案 2/3 弃选理由充分 | 已收敛 |
| R3 | ✅ 已填 | F1/F2/F3 均可操作；CI only；P0 与 _manifest 不联动；early_stop=yes | 已收敛 |
| R4 | ⏭️ 跳过 | 执行期命令占位（见思考轮控制） | 合法：核心命令已在验收标准列出 |
| R5 | ⏭️ 跳过 | P1 路线图 + 关账条件（见思考轮控制） | 合法：远期规划，不影响 P0 执行 |

### early_stop=yes 审查

- **理由**：`R3 已收敛：方案推荐（YAML→MD 单向）明确；CI 仅追加 diff 校验不改动现有 workflow；failure_paths F1/F2/F3 均可操作；P0 与 _manifest 不联动；R4/R5 为执行期命令占位与远期规划，可在 22 审查中书面确认，无需额外思考轮`
- **判定**：理由 **充分**。R4 为命令占位（已落入验收标准），R5 为远期规划（不影响 P0 执行）。
- **residual_risks**：3 项已列出，均 **非阻塞**（见下节）。

---

## 阻塞 / 非阻塞清单

### 阻塞项

**无。**

### 非阻塞 · 已核对项

| # | 核对项 | 结论 | 证据 |
|---|--------|------|------|
| 1 | 10 帽 invoke 已落盘 | ✅ | `invoke_20260616_10_graph-yaml-p0-00-main.md` |
| 2 | task 头部 `HG-TASK-DRAFT` = approved | ✅ | task §人工闸 |
| 3 | `audit_profile: full` + `orchestration` 已填 | ✅ | task §Harness 元信息 |
| 4 | `test_strategy: required` + `test_strategy_note` 非空 | ✅ | 「YAML→MD 转换须可失败单测；与现有 graph.json diff 校验」 |
| 5 | `failure_paths` ≥1 行，含 Scenario ID | ✅ | F1/F2/F3 |
| 6 | 非范围 6 条明确 | ✅ | 不接 cyning-harness、不删 .ai.md、不迁移 10_flow_*、不改前端仓、不回灌 harness、不做 trace.json |
| 7 | 验收标准含合并前必绿 | ✅ | pytest 命令 |
| 8 | 行为变更 Delta 显式「无」 | ✅ | 纯工程/文档管线 |
| 9 | 00_main 节点/边数与 graph.json 一致 | ✅ | 26 节点 / 36 边（独立脚本验证） |
| 10 | 方案 1（YAML→MD + diff 校验）与 QNA §2 一致 | ✅ | QNA §2.2 推荐「YAML 为机器真相源，脚本生成 .ai.md」；task 微调为生成 `.md`（人类友好版）而非 `.ai.md`，符合 P0 不删 `.ai.md` 约束 |
| 11 | CI 策略不破坏现有 workflow | ✅ | 「追加 `graph_yaml` 校验步骤（或 pre-commit），但不改动现有 `verify-tech-graph.sh` 核心链路」 |
| 12 | `freeze_id` 待 30 完成后填 | ⚠️ 非阻塞 | task 已声明「30 完成后填」，符合惯例 |

### 非阻塞 · 残余风险（须 30 帽书面处理或记录）

| # | 风险 | 来源 | 30 帽处理建议 | 22 钉住位置 |
|---|------|------|---------------|-------------|
| R1 | `graph.json` 中 00_main 节点 **无 `kind` 字段**（P2-0 遗留） | 10 帽 R1 + graph_v2_schema §2 | YAML schema 设计时 **允许 `kind` 缺失** 或 **显式补 `kind: null`**；diff 校验脚本须兼容 `kind` 不存在的情况 | task §R3 残余风险 #1 |
| R2 | **锚点渲染格式**：仅 4 条边带 anchors（Q→E、U1→AUTH、U2→AUTH、U2→EV_TYPES），YAML→MD 生成时须与 `99_mermaid_protocol.md` §3 锚点规则对齐（`// → path#line` 或 `// → path::symbol`） | 10 帽 R1 + 99_mermaid_protocol.md | 脚本生成 Mermaid 时锚点注释格式须匹配 protocol；建议在 pytest 中增加锚点格式断言 | task §R3 残余风险 #2 |
| R3 | **AUTO 块策略**：P0 保留 `00_main.ai.md`（标记 `@deprecated · 源迁 YAML`），但 `00_main.ai.md` 中 `AUTO:ENDPOINTS_AND_ANCHORS` 块来自 `_manifest.json`。YAML→MD 生成的 `00_main.md` 是否复刻该块或改为静态引用？ | 10 帽 R0 缺口 #3 + R3 | 30 帽决策并 **书面记录** 于 task §实现备忘或审查 md；建议 P0 不嵌入 AUTO 块（保持 `00_main.md` 人类友好），`_manifest.json` 仍由现有工具维护 | task §R3 残余风险 #3 + §实现备忘 |

---

## 需任务帽回填清单（本 R1 无）

**零项。** 本 R1 审查无阻塞，无需退回 10 帽。

---

## 是否建议执行帽开工

**建议：是。**

理由：
- task 范围/非范围清晰，方案收敛（YAML → .md + diff 校验）。
- failure_paths F1/F2/F3 均可操作，验收标准可观测。
- CI 策略为追加而非改动现有链路，风险可控。
- 残余风险 3 项已书面钉住，30 帽可在实现中处理。

**前提**：
- **HG-AUDIT-R1 须由维护者人工签 `approved`**（本审查 md 产出后仍为 `pending`）。
- 30 帽开工前须确认 `HG-AUDIT-R1 = approved`，否则按 `fp-gate-draft`（F3）拒开工。

---

## 签收 / 关闭

**本 R1 审查结论：可进入执行帽。**

- 本 task **未关闭**；R1 为中间审查轮次。
- 终轮签收须待：30 执行 → 40 自检 → 50 复检 → HG-REINSPECT approved → HG-GRAPH-P0-SIGNOFF checklist 全勾 → CLOSE。
- 22 帽后续可能触发：若 30 实现偏离 task 范围或验收标准不可达，可触发 **R2 复审**。

---

## 下一棒可复制 Prompt

> **HG-AUDIT-R1 仍为 `pending`。** 以下 Prompt 供维护者签 `approved` 后复制给 30 执行帽。30 帽开工前须自行检查 `human_gate` 状态，遇 `pending` 则拒开工。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/hats/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8

输入（已由人工替换占位符；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/by-task/graph-yaml-p0-00-main/task_graph-yaml-p0-00-main_audit_R1_20260616.md
- 关联 SPEC / 总规（无则「无」）：
ai-ink-brain-api-python/docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md
ai-ink-brain-api-python/docs/_tech_graph/99_mermaid_protocol.md
ai-ink-brain-api-python/docs/_tech_graph/graph_v2_schema.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文** 按 `docs/harness/invokes/README.md` 落盘到 `docs/harness/invokes/by-task/graph-yaml-p0-00-main/invoke_YYYYMMDD_30_graph-yaml-p0-00-main.md`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 `human_gate`。若任一对 **本帽（30）** 为 `pending` → 仅输出须人改的 `gate_id` 与路径，**拒开工**；禁止代填 `approved`。
1. 通读 task 全文：头部 `gates_before_code`、`audit_profile`、`orchestration`、`test_strategy` / `test_strategy_note`、`freeze_id`、`failure_paths`、拒开工条件、验收标准、必读列表、非范围。
   - **failure_paths 硬性检查**：即使母单 / docs-only / draft，`failure_paths` 表也至少须 1 行数据；空表会在 CI `task_validate` 步骤触发 `FAILURE-PATHS-EMPTY`（tech-graph Required 门禁）。未满足 → 按拒开工处理，输出阻塞清单。
2. 若 task 明示拒开工条件未满足 → **仅输出 Markdown 阻塞清单**，**不写**业务实现代码。
3. `test_strategy: required` 时：先增加或调整 **可失败** 的自动化测试（或与实现同 PR 且满足 task 所述 red-green / 可复现失败语义），再改实现；禁止「只写实现、后补测」绕过 task 约定。
4. 在 `ai-ink-brain-api-python/` 内按 task 范围改代码/配置：
   - 创建 `docs/_tech_graph/00_main.graph.yaml`（对齐 graph_v2_schema 节点/边结构 + 99_mermaid_protocol.md 边标记）
   - 创建转换脚本（建议 `scripts/graph_yaml_compile.py` 或 `tools/`）
   - 生成 `docs/_tech_graph/00_main.md`（含 Mermaid + 结构化表格/元数据）
   - 与 `graph.json` / `00_main` 节点集 **diff 校验**（脚本 + 文档）
   - **保留** `00_main.ai.md`（标记 `@deprecated · 源迁 YAML`），P0 **不删除**
5. 执行 `pytest tests -m "not intent_eval and not intent_benchmark"`（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 `hats/40-self-check.md` 将结论与命令摘要 **回填** 至 task 正文 `### 自检结论（执行者）`。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 `docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md` 在 `ai-ink-brain-api-python/` 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
   - commit 前须 `git status` 核对：**task 正文 `### 自检结论` 回填** 是否已纳入暂存区；若未纳入 → 补 `git add` 后再 commit，禁止漏落。
9. **链式下一棒**：若 task 由 **Lead / 00** 按 `PROMPT_*_chain_serial_*` 编排 → **不**在本帽同会话自动换帽；仅输出下一棒 §3 或交还 Lead。

**残余风险处理（22 R1 钉住，30 须显式处理或书面记录）**：
- **R1-kind 缺失**：graph.json 00_main 节点无 `kind` 字段。YAML schema 须允许 `kind` 缺失或显式补 `kind: null`；diff 校验脚本须兼容。
- **R2-锚点渲染**：仅 4 条边带 anchors。YAML→MD 生成 Mermaid 时锚点注释格式须与 `99_mermaid_protocol.md` §3 对齐（`// → path#line` 或 `// → path::symbol`）。建议在 pytest 中增加锚点格式断言。
- **R3-AUTO 块策略**：`00_main.ai.md` 中 `AUTO:ENDPOINTS_AND_ANCHORS` 块来自 `_manifest.json`。P0 建议 `00_main.md` **不嵌入** AUTO 块（保持人类友好），`_manifest.json` 仍由现有工具维护。30 须决策并书面记录。

禁止：在未读完必读与 failure_paths 的情况下改代码；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出；引入 `.cyning-harness/` 或 `npx @cyning/harness`；删除 `.ai.md`。
**Fresh Context（P1）**：40→50/22 交接时 **禁止**粘贴本帽 invoke 全文或长思考链；仅交 diff 要点、验收表、`### 自检结论`。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-16 | R1 初审：零阻塞，PASS，建议 30 开工（待 HG-AUDIT-R1 人签） |
