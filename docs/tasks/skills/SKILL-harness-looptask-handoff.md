# SKILL：Harness LoopTask 止于 50 · 交接（50 Prompt + 签收 + 人改 gate 清单）

> **SKILL ID**：`harness-looptask-handoff`  
> **状态**：`active`（2026-06-01）  
> **适用**：`harness_mode: looptask` 且 `stop_after_hat: 50`；50 落盘后或 CLOSE 前；维护者索要 **50 Prompt / 签收文档**  
> **Cursor 入口**： [`.cursor/skills/harness-looptask-handoff/SKILL.md`](../../.cursor/skills/harness-looptask-handoff/SKILL.md)  
> **配对前端**：`ai-ink-brain/.cursor/skills/harness-looptask-handoff/SKILL.md`（路径以 `content/` 为 task/harness 根）

---

## 何时选用

| 适用 | 不适用 |
|------|--------|
| LoopTask 在 **50 + reinspect 落盘后 STOP**（不关账） | 单 task 无 `stop_after_hat: 50`（见 [`SKILL-harness-task.md`](SKILL-harness-task.md)） |
| 维护者要 **50 全文 Prompt**、**R1/R2/50 路径**、**HG-REINSPECT 改哪一行** | 工作区 `Projects/docs/harness/tasks/` 跨仓 task（Open `Projects/`，见工作区规则） |
| **CLOSE** 帽关账前交接 | Loop Batch 母单（见 [`SKILL-harness-loop-batch.md`](SKILL-harness-loop-batch.md)） |

---

## Agent 必须交付的三件事

### 1. 50 Prompt（占位符须全部替换）

| 项 | 本子仓路径 |
|----|------------|
| 规范（若已链出） | `docs/tasks/specs/PROMPT_50_invoke_<slug>_v1_zh.md` 或 task 依赖列出的路径 |
| invoke 快照 | `docs/harness/invokes/by-task/<task_slug>/invoke_YYYYMMDD_50_<task_slug>.md` |
| 帽真值 | [`docs/harness/prompts/hats/50-independent-reinspect.md`](../harness/prompts/hats/50-independent-reinspect.md) |

对话中输出 **§4 Handoff + §5 子 Agent 正文** 合并的 **单一 `text` 围栏**（可 `Task` 粘贴）。**禁止**只写「见 PROMPT_50」而不贴全文（除非用户 **只要路径**）。

### 2. 签收文档路径清单（按帽序 · 相对本子仓根）

| 帽 | 典型路径 |
|----|----------|
| 22 R1 | `docs/harness/reviews/by-task/<task_slug>/task_<slug>_audit_R1_YYYYMMDD.md` |
| 22 R2 | `docs/harness/reviews/by-task/<task_slug>/task_<slug>_audit_R2_YYYYMMDD.md` |
| 40 | `docs/tasks/active/task_<slug>.md` → **`### 自检结论（执行者）`** |
| 50 | `docs/tasks/reinspect_results/task_<slug>_reinspect_YYYYMMDD.md` |
| invoke 链 | `docs/harness/invokes/by-task/<task_slug>/invoke_*` |

> **历史扁平路径**：若 reviews 在 `docs/harness/reviews/task_*_audit_*.md`（无 `by-task/`），以 **task 实现备忘 / invoke 元信息** 为准，仍须在清单中写出 **实际相对路径**。

未落盘 → 写 **「未落盘 · 阻塞」**，不得省略。

### 3. 人工改动：文件 + 位置 + 改什么（禁止笼统）

**禁止**只说「需要人签 HG-REINSPECT」「请改 gate」。

**必须**用表：

| 步骤 | 文件（相对本子仓根） | 位置 | 改什么 |
|------|----------------------|------|--------|
| … | … | … | … |

**禁止 Agent**：`human_gate` 的 `pending` → `approved`；代填 **`### KPI（00）`**；`git mv` → `done/`（除非用户 **明示** 授权代关账）。

---

## CLOSE 关账（人 / 新会话 CLOSE 帽）

1. **HG-REINSPECT** → 见下节「本子仓 task 示例」或当前 task 的 `human_gate` 表  
2. **KPI** → 同一 task **`### KPI（00）`** · [`docs/harness/guides/KPI_RUBRIC_v1_2.md`](../harness/guides/KPI_RUBRIC_v1_2.md)  
3. **归档** → [`docs/tasks/README.md`](../tasks/README.md)：`git mv docs/tasks/active/… docs/tasks/done/`，更新 `docs/tasks/_views/done.md`  
4. **回溯** → [`docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md`](../harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md)

---

## 本子仓 task 关账示例（字段位置模板）

任意 `docs/tasks/active/task_*.md` 含 LoopTask 元信息时，人改 gate 通常如下：

| 步骤 | 文件 | 位置 | 改什么 |
|------|------|------|--------|
| 1 | `docs/tasks/active/task_<slug>.md` | **`### 人工闸 human_gate`** · 行 **`HG-REINSPECT`** · 列 **`status`** | `pending` → **`approved`** |
| 2 | 同上 | **`### KPI（00）`** | 删占位；CLOSE 按 KPI_RUBRIC_v1_2 填写 |
| 3 | 同上 | 文首 **`> 状态`** 或元信息 **状态** | 关账后 **`done`**（与 `git mv` 同步） |
| 4 | Git | — | `git mv docs/tasks/active/task_<slug>.md docs/tasks/done/task_<slug>.md` |

---

## 跨仓 · Portfolio Epic（前端 W5 / 后端 W6 协作）

后端 Agent **只读** 前端落盘时，路径相对 **`ai-ink-brain/`**：

| 文档 | 路径 |
|------|------|
| 前端 W5 task | `content/tasks/active/task_portfolio_content_sync_script_v1.md` |
| 50 Prompt 规范 | `content/tasks/specs/PROMPT_50_invoke_portfolio_content_sync_w5_v1_zh.md` |
| R1 / R2 / 50 | `content/harness/reviews/task_portfolio_content_sync_v1_audit_R*.md` · `content/tasks/reinspect_results/task_portfolio_content_sync_v1_reinspect_20260601.md` |
| 后端 ingest SPEC | `docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md` |

**后端人改（ingest 烟测 · 非关账阻塞）**：

| 步骤 | 文件 | 位置 | 改什么 |
|------|------|------|--------|
| 可选 | `.env`（**勿提交 Git**） | 键 **`CONTENT_ROOT`** | `<绝对路径>/ai-ink-brain/content` |
| 可选 | 本机 shell | — | 前端 BFF `POST /api/admin/sync` + `x-admin-token`（见前端 `tools/README-portfolio-content-sync.md`） |

---

## 新 LoopTask 从模板复制时

1. 22 R2 链出 `PROMPT_50_invoke_<slug>_v1_zh.md`（或 task specs 目录）  
2. R2 审查 md **须**含「下一棒 50 Prompt」或指向 PROMPT 文件  
3. STOP 回复须含 `reinspect:` **完整相对路径**  
4. 关账交接 **须**含「人改 gate」四列表（见上）

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-01 | v1：源于前端 Portfolio W5 LoopTask；后端双轨 + 跨仓 Portfolio 指针 |
