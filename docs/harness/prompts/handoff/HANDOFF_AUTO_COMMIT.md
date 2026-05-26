# Harness 通则：下一棒 Prompt 产出后自动 Git Commit

> **适用范围**：凡在 **本轮对话** 中产出 **「下一棒可复制 Prompt」**（及各帽子 **交接物** 要求的同内容落盘）的 **所有 Harness 帽子**（`10` / `20` / `22` / `30` / `40` / `50` 及对应 `templates/TEMPLATE-*-invoke`）。  
> **真值层级**：本文件为 **Guides**；与 [`HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) §3 并列；**不替代** CI。  
> **用户显式豁免**：用户在本轮消息中写明 **「本轮不要 commit」** 或 **「仅草稿不落盘」** 时，**跳过**本章 commit 义务（仍须完成 Prompt 与约定落盘）。  
> **流程关闭（无下一棒）**：不产出下一棒 Prompt；改按 [`handoff/HANDOFF_CLOSE_TRACE.md`](handoff/HANDOFF_CLOSE_TRACE.md) 输出 **执行路线与 Commit 回溯**（本轮落盘仍须 commit）。  
> **半自动链式戴帽**：见 [`handoff/HANDOFF_SEMI_AUTO.md`](handoff/HANDOFF_SEMI_AUTO.md)——自动下一棒前 **须先** invoke 落盘 + commit；遇 `human_gate: pending` **不得**执行阻塞帽。

---

## 1. 为什么要 commit

- **下一棒** 常在新会话粘贴 Prompt；若审查 md / invoke / task 回填 **仅在本机未提交**，下一棒 Agent **看不到** 真值路径内容。  
- 与 **Invoke 快照**、**`reviews/` 落盘** 形成同一 **可追溯链环**：磁盘 → git → 下一帽只读已提交历史。

---

## 2. 触发条件（须同时满足）

| # | 条件 |
|---|------|
| T1 | 本轮已输出 **「下一棒可复制 Prompt」** 全文（对话内 `text` 围栏，占位符已替换） |
| T2 | 本轮已按该帽规则完成 **应落盘工件**（如 `reviews/*_audit_*.md`、`invokes/invoke_*.md`、用户授权的 **task 正文修改** 等） |
| T3 | 用户 **未** 声明本轮豁免 commit |

**不要求**为「仅对话、零文件变更」的纯咨询 commit 空提交。

---

## 3. 提交什么（范围）

**只提交本轮帽子交付相关路径**，按实际改动分仓：

| 常见落点 | 典型仓库 |
|----------|----------|
| `ai-ink-brain-api-python/docs/tasks/`、`docs/harness/reviews/`、`docs/harness/invokes/`（子仓） | `ai-ink-brain-api-python` |
| `docs/harness/`、`docs/tech_graph/`（工作区级） | 工作区根 `Projects/`（若该目录为 git 根） |
| 业务实现（`30` 帽） | 对应子仓 |

**禁止** 纳入无关 WIP（其他 task、未请求的工具改动、`.env`、密钥）。若工作区仅部分文件属本轮，**禁止** `git add -A` 扫入杂项。

---

## 4. 执行顺序（Agent 在本轮结束前）

1. **落盘优先**：审查 md / invoke / task 修改等 **先写入磁盘**。  
2. **分仓 `git status`**：对每个涉及的 git 根分别查看。  
3. **暂存**：仅 `git add` 本轮相关路径。  
4. **Commit**：每个有改动的仓库 **至少 1 个 commit**；message 用 HEREDOC，建议格式：

```text
docs(harness): <帽子编号> <简短主题>

<一句说明：如 R1 审查落盘 + 下一棒 10 帽 invoke；或 task v0.3 回填>
```

示例：

```text
docs(harness): 22 R2 任务审核落盘与下一棒 30 执行 invoke

审查全文在子仓 reviews/；含下一棒可复制 Prompt。
```

5. **对话收尾**：在输出「下一棒可复制 Prompt」**之后**（或同一回复末尾），用 **一行** 列出本次 commit（**禁止**只写「已提交」而无 hash）：

```text
已提交：ai-ink-brain-api-python @ <short-hash> — <message 首行>
已提交：Projects @ <short-hash> — …（若适用）
```

**Loop Batch invoke C2（commit 前 · 与 commit 纪律并列）**：

| 检查 | 行为 |
|------|------|
| invoke §3 **< 15 行** 或文件 **< 800 B** | **不得 commit**；补全 §3 可复制 Prompt 后再提交 |
| §3 仅为「交付摘要 + commit」 | 同上 |
| 元信息表缺 `task_slug`（或 round/hat/task/freeze_id/git_branch） | 补全后再 commit |
| 用户显式豁免 | 对话声明「本轮 invoke stub 豁免」并说明理由 |

真值：[`SKILL-harness-loop-batch.md`](../../tasks/skills/SKILL-harness-loop-batch.md) §invoke 质量门禁 · 实例 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md) 步骤内自检句。

6. **禁止** 除非用户明确要求：`git push`、`git config` 修改、`--no-verify`、`--amend`（除用户规则允许情形）。

---

## 5. 与各帽子的衔接

| 帽子 | 通常提交内容 |
|------|----------------|
| **10** | 更新后的 `task_*.md`；可选工作区 invoke |
| **20** | 通常仅对话 Prompt；若用户要求留痕 md 则一并提交 |
| **22** | `reviews/task_*_audit_R*_*.md`；工作区 invoke / 指针（若有） |
| **30** | 代码 + 测试 + task 自检结论；**不** 把未跑通的验证硬提交 |
| **40** | task 内 `### 自检结论` |
| **50** | 复检报告 md（若有落盘） |

各 `templates/TEMPLATE-*-invoke.md` **§3** 末尾应含一步：**按 [`handoff/HANDOFF_AUTO_COMMIT.md`](handoff/HANDOFF_AUTO_COMMIT.md) 提交本轮工件后再结束对话**。

---

## 6. 失败与阻塞

| 情况 | 行为 |
|------|------|
| `git commit` 被 hook 拒绝 | 修复后 **新 commit**（**禁止** 擅自 `--no-verify`）；在对话说明阻塞原因 |
| 无 git 仓库 / 只读环境 | 在对话 **显式声明**「无法 commit」并列出落盘路径，请用户本地提交 |
| 子仓与工作区嵌套 | 分别在 **各自 git 根** 提交，**禁止** 假设单次 commit 覆盖全部 |

---

## 7. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-17 | v1：初版 — 下一棒 Prompt 后自动 commit 通则 |
| 2026-05-17 | v1.1：互链 [`handoff/HANDOFF_CLOSE_TRACE.md`](handoff/HANDOFF_CLOSE_TRACE.md)（无下一棒分支） |
| 2026-05-26 | v1.2：Loop Batch invoke C2 — commit 前 §3 行数/体量自检（SKILL v1.5 第三批联动） |

---

## 给 Cursor

`handoff/HANDOFF_AUTO_COMMIT`、`handoff/HANDOFF_CLOSE_TRACE`、`下一棒可复制 Prompt`、`自动 commit`、`reviews`、`invokes`、`分仓提交`、`禁止 git add -A`
