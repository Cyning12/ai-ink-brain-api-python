# 验收落盘约定（人类可读 · 三方 Agent 可查收）

> **用途**：保证每个须关账的 task 不仅有对话结论，还有 **仓库内可打开、可 diff、可审计** 的 Markdown。  
> **三方 Agent**：指 **未参与实现的复检 Agent**（**50 帽**），输入裁剪为 diff + 日志 + 自检表，**禁止**用执行过程长文代替证据。

---

## 1. 三类落盘（本仓最小 Harness）

| 类型 | 路径 | 谁写 | 人类可读要点 |
|------|------|------|----------------|
| **任务审核（人择 A 路）** | `docs/harness/reviews/task_*_audit_R*_*.md` | **22 帽** | R1/R2、阻塞项、**签收/关闭**；**仅本仓** `docs/tasks/` |
| **执行自检** | task 正文 `### 自检结论（执行者）` | 40 帽 / 执行 Agent | 命令、退出码、摘要；**合并前必绿** 命令须写明 |
| **规格短评（可选）** | `docs/tasks/review_results/review_*.md` | 20 帽 | 缺口列表、可勾选回填 |
| **三方复检（关账必选）** | `docs/tasks/reinspect_results/reinspect_<slug>_YYYYMMDD_vN.md` | **50 帽** | **验收表** + **证据** + **是否建议合并** |

**禁止**：仅以聊天「过了」关账；**禁止** 50 帽只输出对话不写 `reinspect_results/`。

---

## 2. 22 与 10 的双路径（人择一）

10 帽结束 **必须** 给出两条下一棒 Prompt（见 `TEMPLATE-requirements-invoke` §3）：

- **路径 A**：22 R1 → 落盘 `docs/harness/reviews/`（**默认推荐**：`audit_profile: post_close|full`、`test_strategy: required`、新 task、跨仓契约、验收含糊）
- **路径 B**：直进 30（**人**择；10 帽可对 B 标 `（推荐）`：小改 docs、task 已人扫、紧急 hotfix 且 task 写明事后补 22）

**不是**「22 可选流程」：而是 **每次都提供 A/B 全文**，10 帽加 **推荐标注** 降认知负担；**禁止** Agent 因推荐自动执行下一帽。细则见 [`prompts/10-requirements.md`](prompts/10-requirements.md) **§下一棒 A/B**。

## 3. 何时必须跑 50 + 落盘

- task 头部 **`test_strategy: required`**，或验收标准含「合并前须复检」；  
- `human_gate` 含 **`HG-GLOBAL-SIGNOFF`** / **`HG-REINSPECT`** 且 `blocks_hats` 含 `done` 或合并；  
- `semi_auto` 链在 **40 通过后** 下一棒为 **50** 时（见 [`SDD_HAT_FLOW.md`](SDD_HAT_FLOW.md)）。

`test_strategy: recommended`：PR 作者自选；`not_applicable` 须在 task 写一行理由。

---

## 4. `reinspect_results/` 正文最小结构

1. **元信息**：`task` 路径、`git_branch`、commit 短哈希、复检日期、复检 Agent（可选）。  
2. **验收表**：`验收项 | pass/fail | 证据 | 备注`（证据须可定位：路径:行 / 测试名 / 日志片段）。  
3. **阻塞合并项**（若无写「无」）。  
4. **结论**：`建议合并` / `不建议合并` / `证据不足待补`。  
5. **给需求帽回填**（仅文档缺口时；无则「无」）。

命名：`reinspect_<主题>_YYYYMMDD_vN.md`（见 [`../tasks/reinspect_results/README.md`](../tasks/reinspect_results/README.md)）。

---

## 5. 与 invoke 快照的关系

- **50 开帽**：将 [`prompts/TEMPLATE-independent-reinspect-invoke.md`](prompts/TEMPLATE-independent-reinspect-invoke.md) §3 落盘至 [`invokes/invoke_*_50_*.md`](invokes/README.md)（首次）。  
- **50 关帽**：**必须先** 写入 `reinspect_results/*.md` 并 commit，再输出对话摘要 / `HANDOFF_CLOSE_TRACE`。

---

## 6. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：最小 harness 恢复 50 |
| 2026-05-22 | v2：恢复 **本仓** `docs/harness/reviews/`（22）；10 双路径 A/B |
