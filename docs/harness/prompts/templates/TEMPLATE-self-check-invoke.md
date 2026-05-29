# 自检（执行者）· 对话调用模板（与 `40-self-check` 配套）

> **用途**：复制下文 **§3 可复制 Prompt 正文** 到对话，替换 **§2 占位符** 后发起 **自检帽**：跑命令、对验收表打 pass/fail、将 **`### 自检结论（执行者）`** 写回 task。  
> **帽子真值**：[`hats/40-self-check.md`](hats/40-self-check.md)（身份、禁止项、输出形状、交接物）。  
> **上一棒（可选）**：[`templates/TEMPLATE-execute-invoke.md`](templates/TEMPLATE-execute-invoke.md) + [`hats/30-execute-code.md`](hats/30-execute-code.md) 完成实现后，**仍须**由本模板独立跑通验证（不得凭记忆宣称已测）。  
> **下一棒（独立复检）**：[`templates/TEMPLATE-independent-reinspect-invoke.md`](templates/TEMPLATE-independent-reinspect-invoke.md) **§3** + [`hats/50-independent-reinspect.md`](hats/50-independent-reinspect.md)（模式选 **`独立复检`** 或 **`两者`**）。  
> **字段约定**：[`../HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) **§5**（与 task 中 `test_strategy` 等对齐）。

---

## 1. Agent 前置规则（占位符未替换 → 必须追问，不得代填）

在按 **自检帽** 跑命令、回填 task 之前，须先做 **占位符扫描**：

1. **若用户粘贴的 Prompt 中仍含有任一未替换占位符**（见 **§2 表**），**禁止**开始跑命令与写 **`### 自检结论`**；**必须先向用户追问**，一次列出所有缺失项后再继续。  
2. **禁止**无命令输出却勾选验收项；禁止编造退出码或路径。  
3. **`{{DIFF_NOTE_OR_NONE}}`**：无额外 diff 说明时填字面 **`无`**；留空视为未替换，须追问。

---

## 2. 占位符（每次调用前由人替换）

| 占位符字面量（须全部消失于最终粘贴体） | 含义 | 示例 |
|----------------------------------------|------|------|
| `{{TASK_PATH}}` | 主 task 路径（相对工作区根 `Projects/`） | `ai-ink-brain-api-python/docs/tasks/active/task_….md` |
| `{{SUBPROJECT_ROOT}}` | 逻辑子仓名（task 路径前缀；相对 `Projects/`） | `ai-ink-brain` |
| `{{WORKTREE_ROOT}}` | 执行验证命令时的 **cwd**（相对 `Projects/`）；并行须与 invoke/task `worktree_root` 一致 | `ai-ink-brain` |
| `{{VERIFY_COMMAND}}` | 与 task / 子仓 CI 对齐的 **主**验证命令（一条）；task 若列多条，须 **通读 task 后逐条执行** 并在自检表中分别给证据 | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| `{{DIFF_NOTE_OR_NONE}}` | 如何理解本次变更范围（如 `git diff origin/main...HEAD`、或 PR 链接摘要）；无则 **`无`** | `无` |

---

## 3. 可复制 Prompt 正文（从下一行起复制到对话）

```text
你正在扮演工作区 Harness「自检帽（执行者）」，严格遵循：
- docs/harness/prompts/hats/40-self-check.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 的 test_strategy 等一致）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：
- 主 task 路径（相对工作区根 Projects/）：
{{TASK_PATH}}
- 逻辑子仓（task 路径前缀；相对 Projects/）：
{{SUBPROJECT_ROOT}}
- Worktree 研发目录（运行验证命令的 cwd；见 docs/harness/README.md「并行分支与 Git worktree」）：
{{WORKTREE_ROOT}}
- 主验证命令（与 CI / task 一致；task 另有命令须一并执行并在结论中分列）：
{{VERIFY_COMMAND}}
- 变更范围说明（无则写「无」）：
{{DIFF_NOTE_OR_NONE}}

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 通读 task 全文中的验收标准与「验证 / 自检 / 合并前」相关命令列表；逐条运行所列命令（至少包含 {{VERIFY_COMMAND}}），在对话中给出：命令、cwd、退出码、关键通过/失败行或断言摘要。
2. 输出 **验收表**（每项 pass/fail + 证据：命令名/测试名/日志摘录）；fail 时写明是否可重试（环境/flaky）。
3. 将 **`### 自检结论（执行者）`** 写入 **{{TASK_PATH}}** 指向的 task 正文（若尚无该小节则新增；位置与团队习惯一致即可）：含命令列表、退出码、验收摘要、已知未测项。
4. 禁止：凭记忆声称「测过」；把独立复检的深度走查塞进本帽（本帽以命令与验收表为主）。
5. **Fresh Context（P1）**：交接 50/22 时 **禁止**粘贴 30 invoke 全文；仅交 diff 要点、验收表、`### 自检结论`。

对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
6. **自动 commit**：在输出下一棒 Prompt 且 task 内「### 自检结论（执行者）」已写入后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 分仓 commit（仅本轮路径；对话报 short-hash）。用户写明「不要 commit」则跳过。
```

---

## 4. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：与 `40-self-check` 关联；占位符未替换则 Agent 追问 |
| 2026-05-14 | v1.1：§3 对话收口改为「下一棒可复制 Prompt」（含打回、二次审查、上一棒修复） |
| 2026-05-14 | v1.2：§3 可复制正文增第 **0** 条 **Invoke 快照（开帽起点）** |
| 2026-05-20 | v1.3：§2/§3 增 **`{{WORKTREE_ROOT}}`**；与 `docs/harness/README.md` 并行 worktree 对齐 |

---

## 给 Cursor

`Harness`、`templates/TEMPLATE-self-check-invoke`、`40-self-check`、`自检结论`、`VERIFY_COMMAND`、`SUBPROJECT_ROOT`、`占位符`、`追问`
