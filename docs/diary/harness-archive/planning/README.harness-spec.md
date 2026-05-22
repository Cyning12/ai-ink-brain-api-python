# docs/harness/invokes（新帽节 · Invoke 快照）

> **用途**：在 **每一顶帽子新开局**（新对话节 / 新 Agent 会话中 **首次** 按某 `TEMPLATE-*-invoke.md` **§3** 发起执行）时，将 **占位符已全部替换后的可复制 Prompt 正文** 落盘一份，作为与 `reviews/`、task 内 **`### 自检结论`** 等 **并列的可追溯链环**（**非**每一轮聊天都写；**非**替代审查 md 的结论真值）。  
> **真值**：本节命名与元数据表；与 [`../prompts/README.md`](../prompts/README.md) 使用方式中的 **Invoke 快照** 描述一致。**各 `TEMPLATE-*-invoke.md` §3 可复制正文**已内嵌第 **0** 条（或全量模板 **【五·附】**）与本节对齐。

---

## 1. 何时必须写（环节起止点）

| 场景 | 是否落盘 |
|------|----------|
| **新帽**：新开对话（或明确切换角色），且本节的 **第一条** 用户消息为某调用模板 **§3 已替换占位符** 的全文 | **建议强约束**（团队采纳后升为「须」）：**先于或紧挨** 模型首答写入本目录 |
| **同一帽**内追问、补材料、多轮澄清 | **不写** 新快照；沿用本节首条已链路径（可在 task 或审查文内脚注「延续会话」） |
| **同一模板**因打回再次粘贴（仍算「新节」：如执行失败 → 新开执行帽） | **可** 新文件，`seq` 或时间后缀递增，避免覆盖 |
| **规格短评 `20`**（仅对话、默认不落盘 reviews） | **仍建议** 快照：否则该段只有聊天记录，仓库侧无锚点 |

**与 `reviews/` 分工**：`reviews/*_audit_*.md` 承载 **审查结论与签收**；本目录承载 **当时交给模型的调用体**，便于复现「当时到底下了什么指令」。

---

## 2. 放哪（与 task 所在仓对齐）

| 主 task 路径（相对 `Projects/`） | 建议快照目录 |
|----------------------------------|--------------|
| `ai-ink-brain-api-python/docs/tasks/**` | **`ai-ink-brain-api-python/docs/harness/invokes/`**（与 [`../reviews/README.md`](../reviews/README.md) 子仓落盘规则对称） |
| `docs/tech_graph/**`（专题：graph.json / 三方案；子仓正式 task 仍在各仓 `docs/tasks` 或 `content/tasks`） | **`docs/tech_graph/invokes/`**（见 [`../../tech_graph/invokes/README.md`](../../tech_graph/invokes/README.md)） |
| 其他（仅工作区级 task 等） | **`docs/harness/invokes/`**（本目录） |

> **布局注意**：若工作区根 `.gitignore` **整路径忽略** 某子仓目录（嵌套独立 git、上层仓不收录其文件），则 **Git 可提交的真值** 仅为根目录 **`docs/harness/invokes/`**；仍建议在快照元信息 `task_paths` 中写清子仓 task 相对路径，语义上与「该子仓 task 开帽」一致。子仓内 `docs/harness/invokes/README.md`（若存在）供 **仅在子仓仓库内** 开发时对照。

**指针**：若快照在子仓且 **上层仓可收录** 子仓路径，工作区 `docs/harness/invokes/` 可存 **仅含元数据 + 相对链** 的短 md，避免双份正文漂移（与 reviews「指针 md」策略同型）。**示例**：[pointer_invoke_chatbi_v3_task_audit_r2.md](pointer_invoke_chatbi_v3_task_audit_r2.md)（→ 子仓 `22` 任务审核 R2 启动体快照）。

---

## 3. 命名建议

| 片段 | 含义 | 示例 |
|------|------|------|
| 固定前缀 | 一眼区分 Harness 工件 | `invoke_` |
| `YYYYMMDD` | 发起日（与 reviews 日期习惯一致） | `20260514` |
| `HHmm` | 同日多开帽时分（可选；无时可用 `0000` 或省略后靠 `seq`） | `1530` |
| 帽代号 | 与规划 **§3** 对齐 | `10` / `20` / `22` / `30` / `40` / `50` |
| `slug` | 与 task 文件名主体或审查 slug 一致，**小写**、连字符 | `chatbi-v3-sql-ast-gate` |
| `seq`（可选） | 同日同帽同 task 再次开节 | `_2`、`_r2` |

**完整示例**：`invoke_20260514_1530_22_chatbi-v3-sql-ast-gate.md`

---

## 4. 文件正文结构（建议复制本骨架再贴 Prompt）

````markdown
# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| template | docs/harness/prompts/TEMPLATE-task-audit-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/done/task_….md |
| related_review_or_none | 无 或 docs/harness/reviews/… / 子仓 … |
| git_branch | 本任务 **唯一** 分支名（并行时 **禁止** 与 `parallel_with` 共用） |
| worktree_root | 相对 `Projects/` 的 **研发目录名**；所有 `git`/`pnpm`/`pytest` 默认 cwd；非并行可省略（= 子仓根目录名） |
| parallel_with | 可选：并行 invoke 路径或任务 ID（如 T3∥T5） |
| created_utc_or_local | 2026-05-14 15:30 CST（人填） |
| notes | 可选：PR 号、`git worktree list` 摘要 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
（整段粘贴 §3 已替换占位符后的正文）
```
````

---

## 4.1 并行任务与 worktree（与 [`../README.md`](../README.md) 对齐）

- **真值字段**：invoke 元信息 **`git_branch`** + **`worktree_root`**；task 头部同名两行。  
- **执行帽 / 自检帽**：`TEMPLATE-execute-invoke` / `TEMPLATE-self-check-invoke` 的 **`{{WORKTREE_ROOT}}`** 须与 invoke 表一致；**禁止**在并行另一 worktree 改代码。  
- **审查 / 需求帽**：可在任意 worktree 只读；落盘 `reviews/`、`task`、`invokes` 时须在 **本任务分支** 上 commit（避免 R1 审查 md 漂到错误分支）。  
- **Cursor**：每个并行 Agent 会话 **Open Folder** 对准该任务的 `worktree_root` 目录，勿与工作区根 `Projects/` 混用同一子仓 checkout。

---

## 5. 与 task / 审查的链接方式（形成闭环）

- **审查 md**：在文首 **元信息** 表增一行 **`invoke_snapshot`** → 相对 `Projects/` 路径（可多行：首轮 + 复审各一条）。  
- **task**：可选小节 **`### Invoke 快照（可选）`** 下挂路径列表（与 `### 自检结论` 分列）。  
- **下一棒可复制 Prompt**（各模板 §3 末尾约定）：鼓励在生成的 Prompt 中 **显式写出**「上一节 invoke 快照路径」，便于接收方回溯。

---

## 6. 安全与体积

- **禁止**在快照中保存 API Key、`.env` 全文；占位符替换时若夹带密钥，**脱敏后再落盘**。  
- 正文过长仍允许：真值是 **文件路径**；必要时可只落盘 **摘要 + 指向** 本地导出 zip（不推荐默认）。  
- **Git**：快照与代码同 PR 提交，便于 review 时对照「指令 → 改动」。

---

## 7. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：目录说明、触发条件、命名、正文骨架、与 reviews/task 链接、安全 |
| 2026-05-14 | v1.1：§2 增补工作区 gitignore 子仓时的真值与「指针」说明 |
| 2026-05-14 | v1.2：真值段声明与各 `TEMPLATE-*-invoke` §3 第 0 条 / 【五·附】对齐 |
| 2026-05-15 | v1.3：工作区 **指针** 示例 [`pointer_invoke_chatbi_v3_task_audit_r2.md`](pointer_invoke_chatbi_v3_task_audit_r2.md)（子仓快照正文真值、上层链回） |
| 2026-05-14 | v1.4：`§2` 增补 **`docs/tech_graph/invokes/`** 与 Harness 本目录分工 |
| 2026-05-15 | v1.5：§4 嵌套示例外层改为四反引号围栏；内层快照由波浪线三围栏改为标准三个反引号加 `text` 信息串，与常见 Markdown 渲染器习惯一致。 |
| 2026-05-20 | v1.6：§4 元信息增 **`git_branch`** / **`worktree_root`** / **`parallel_with`**；§4.1 并行 worktree 与 [`../README.md`](../README.md) 互链 |

---

## 给 Cursor

`Harness`、`invokes`、`invoke 快照`、`新帽`、`TEMPLATE`、`可追溯`、`reviews`、`签收`、`子仓`、`指针`
