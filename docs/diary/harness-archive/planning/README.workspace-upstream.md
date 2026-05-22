# docs/harness（工作区级 Harness 文档）

| 文件 | 说明 |
|------|------|
| [`../../ai_coding_governance/methodology/harness/HARNESS_ADOPTION_METHODOLOGY_v1_zh.md`](../../ai_coding_governance/methodology/harness/HARNESS_ADOPTION_METHODOLOGY_v1_zh.md) | **方法论 v1（过程态）** · 私有仓 |
| [`../../ai_coding_governance/methodology/harness/HARNESS_ADOPTION_TARGET_STATE_v1_zh.md`](../../ai_coding_governance/methodology/harness/HARNESS_ADOPTION_TARGET_STATE_v1_zh.md) | **目标态** · 私有仓 |
| [`../../ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_TARGET_STATE_v1_zh.md`](../../ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_TARGET_STATE_v1_zh.md) | 图谱 **目标态**（姊妹篇） |
| [HARNESS_V2_PLAN.md](HARNESS_V2_PLAN.md) | Harness V2 初版规划：分层落盘、三支柱、`test_strategy` 等 task 字段、CI 批次 |
| [HARNESS_V2_P0_ACCEPTANCE.md](HARNESS_V2_P0_ACCEPTANCE.md) | **P0 验收单**：已落地 workflow、代码变更摘要、本地/ GitHub 勾选验收、与 Actions 关系说明 |
| [VERIFICATION_CI_PATTERN.md](VERIFICATION_CI_PATTERN.md) | **P2 可选 Verification**：`verify-fast` 与 `quality`/`pytest` 边界、形态 A/B、分支保护要点 |
| [tasks/README.md](tasks/README.md) | **工作区 Harness 任务**：`active/`、`done/`、`_views/` 规则与索引（跨子仓流程/CI/帽子等） |
| [prompts/README.md](prompts/README.md) | **角色帽子 Prompt**（`*.md`）：与 [`HARNESS_V2_PLAN.md`](HARNESS_V2_PLAN.md) **§3** 同步；**对话调用模板**见 [`prompts/TEMPLATE-requirements-invoke.md`](prompts/TEMPLATE-requirements-invoke.md)（`10`）、[`prompts/TEMPLATE-review-spec-task-invoke.md`](prompts/TEMPLATE-review-spec-task-invoke.md)（`20`）、[`prompts/TEMPLATE-task-audit-invoke.md`](prompts/TEMPLATE-task-audit-invoke.md)（`22`）、[`prompts/TEMPLATE-execute-invoke.md`](prompts/TEMPLATE-execute-invoke.md)（`30`）、[`prompts/TEMPLATE-self-check-invoke.md`](prompts/TEMPLATE-self-check-invoke.md)（`40`）、[`prompts/TEMPLATE-independent-reinspect-invoke.md`](prompts/TEMPLATE-independent-reinspect-invoke.md)（`50`） |
| [reviews/README.md](reviews/README.md) | **任务审核产出**：每轮审查必落盘；闭环 R1/R2…；**签收 / 关闭** 与 task 状态对齐 |
| [invokes/README.md](invokes/README.md) | **新帽节 Invoke 快照**：每帽首次发起时落盘已替换占位符的 §3 调用体；与 `reviews/`、task 自检并列可追溯 |
| [`../../ai_coding_governance/methodology/harness/Harness工程测评-Desktop-Projects-ai-ink.md`](../../ai_coding_governance/methodology/harness/Harness工程测评-Desktop-Projects-ai-ink.md) | Ink 全栈测评 · 私有仓 |
| [SDD_HAT_FLOW.md](SDD_HAT_FLOW.md) | **SDD 与帽子编号流程**：10→…→50 推荐链、**22 签收 vs 50 可选**、**40 与 22 分工**、审核/实现两类 **打回** 回流示例 |

**入口**：根目录 [`README.md`](../../README.md)（**cyning-ink-workspace**）、[`AGENTS.md`](../../AGENTS.md) **§8**。

---

## 并行分支与 Git worktree（强制 · 多 Agent）

同一子仓（如 `ai-ink-brain`）**两条及以上** `task/*` 分支并行时，**禁止**多个 Agent 共用同一 checkout 目录（会互抢 `git checkout`、混未提交改动、踩 `.next/` / `node_modules`）。

| 层级 | 落点 | 写什么 |
|------|------|--------|
| **规范（一次）** | 本节 + [`invokes/README.md`](invokes/README.md) §4 元信息 | 须 `git worktree add` 或独立 clone；Cursor **Open Folder** 对准 **worktree 目录** |
| **模板（一行）** | [`prompts/TEMPLATE-execute-invoke.md`](prompts/TEMPLATE-execute-invoke.md)、[`TEMPLATE-self-check-invoke.md`](prompts/TEMPLATE-self-check-invoke.md) §2 | 占位符 `{{WORKTREE_ROOT}}`；并行时 **命令 cwd** 以 invoke/task 为准 |
| **任务真值（每线）** | invoke 元信息表 + task 头 | `git_branch` + **`worktree_root`**（相对 `Projects/` 的目录名） |

**约定**

1. **`worktree_root`**：该任务 **唯一** 研发目录（相对工作区根 `Projects/`），所有 `git` / `pnpm` / `pytest` 默认 **cwd** 在此目录。  
2. **`SUBPROJECT_ROOT`（模板）**：逻辑子仓名，用于 task 路径前缀（如 `ai-ink-brain/content/tasks/...`）；与 `worktree_root` **可不同**（worktree 目录名常为 `ai-ink-brain-wt-<slug>`，仍属同一 Git 仓库）。  
3. **非并行**：`worktree_root` 可省略，视为与 `SUBPROJECT_ROOT` 相同（如均为 `ai-ink-brain`）。  
4. **Harness 工件**（`reviews/`、`invokes/`、`task`）须在 **该任务 `git_branch` 上 commit**，禁止只落在并行另一分支。  
5. **禁止**在并行期对共用主目录执行 `git switch` / `git checkout` 切到另一任务分支。

**Ink 前端 parity 并行示例（2026-05-20）**

| 子项 | `git_branch` | `worktree_root` |
|------|--------------|-----------------|
| T5 manifest | `task/tech-graph-v2-frontend-manifest-v1` | `ai-ink-brain` |
| T3 mermaid | `task/tech-graph-v2-mermaid-audit-v1` | `ai-ink-brain-wt-mermaid-audit` |

子仓入口：[`ai-ink-brain/AGENTS.md`](../../ai-ink-brain/AGENTS.md) **并行 worktree** 指针。

**后端 api-python 并行示例（2026-05-20）**

| 子项 | `git_branch` | `worktree_root` |
|------|--------------|-----------------|
| P1-2 关账 | `task/chatbi-v3-prompt-injection-closeout-v1` | `ai-ink-brain-api-python-wt-chatbi-closeout` |
| 闸口 D | `task/engineering-tech-graph-gate-d-v2-tasks-v1` | `ai-ink-brain-api-python-wt-gate-d-v2` |
| manifest | `task/tech-graph-v2-frontend-manifest-v1` | `ai-ink-brain-api-python-wt-frontend-manifest` |
| 基线 | `main` | `ai-ink-brain-api-python` |

初始化脚本：[`ai-ink-brain-api-python/scripts/git-worktree-parallel.sh`](../../ai-ink-brain-api-python/scripts/git-worktree-parallel.sh)

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-13 | v1.1：索引增补 `reviews/README.md`（任务审核落盘与终点点） |
| 2026-05-13 | v1.2：入口链指向根目录 `README.md` / `AGENTS.md`（`../../`）；标注工作区名 **cyning-ink-workspace** |
| 2026-05-14 | v1.3：远端 PR 验收与运维结论落盘 — [`HARNESS_V2_P0_ACCEPTANCE.md`](HARNESS_V2_P0_ACCEPTANCE.md) §4/§6/§6.1；[`HARNESS_V2_PLAN.md`](HARNESS_V2_PLAN.md) §10；[`tasks/README.md`](tasks/README.md)「当前状态」；[`VERIFICATION_CI_PATTERN.md`](VERIFICATION_CI_PATTERN.md) §5.1 |
| 2026-05-14 | v1.4：任务审核对话模板 [`prompts/TEMPLATE-task-audit-invoke.md`](prompts/TEMPLATE-task-audit-invoke.md)（与 `22` / `reviews` 关联；占位符未替换则 Agent 追问） |
| 2026-05-14 | v1.5：`10` / `20` 调用模板 [`prompts/TEMPLATE-requirements-invoke.md`](prompts/TEMPLATE-requirements-invoke.md)、[`prompts/TEMPLATE-review-spec-task-invoke.md`](prompts/TEMPLATE-review-spec-task-invoke.md)；索引表链四模板 |
| 2026-05-14 | v1.6：`40` / `50` 调用模板 [`prompts/TEMPLATE-self-check-invoke.md`](prompts/TEMPLATE-self-check-invoke.md)、[`prompts/TEMPLATE-independent-reinspect-invoke.md`](prompts/TEMPLATE-independent-reinspect-invoke.md)；索引表链六模板 |
| 2026-05-14 | v1.7：[`invokes/README.md`](invokes/README.md)（新帽节 Prompt 快照约定与 `reviews` 互链） |
| 2026-05-15 | v1.8：Invoke 快照 **首份示例** 落盘（子仓 `ai-ink-brain-api-python/docs/harness/invokes/` + 工作区 [`invokes/pointer_invoke_chatbi_v3_task_audit_r2.md`](invokes/pointer_invoke_chatbi_v3_task_audit_r2.md) 指针） |
| 2026-05-15 | v1.9：[`SDD_HAT_FLOW.md`](SDD_HAT_FLOW.md)（帽子数字链、22/50/40 关系、打回流） |
| 2026-05-20 | v2.0：[`HARNESS_ADOPTION_METHODOLOGY_v1_zh.md`](HARNESS_ADOPTION_METHODOLOGY_v1_zh.md) + 推广收口 task 草案 |
| 2026-05-20 | v2.1：本节 **并行分支与 Git worktree**；与 `invokes` 元信息 `worktree_root`、`30`/`40` 模板占位符对齐 |
