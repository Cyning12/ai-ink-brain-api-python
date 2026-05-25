# 执行编码 · 对话调用模板（与 `30-execute-code` 配套）

> **用途**：复制下文 **§3 可复制 Prompt 正文** 到对话，替换 **§2 必填占位符** 后发起 **执行帽** 实现与验证。  
> **下一棒（仅验证与回填自检）**：若仅需补跑命令与 **`### 自检结论（执行者）`**（无新实现）→ [`templates/TEMPLATE-self-check-invoke.md`](templates/TEMPLATE-self-check-invoke.md) **§3** + [`hats/40-self-check.md`](hats/40-self-check.md)。  
> **帽子真值**：[`hats/30-execute-code.md`](hats/30-execute-code.md)（身份、拒开工、`test_strategy`、交接物）。  
> **自检回填**：[`hats/40-self-check.md`](hats/40-self-check.md)（命令证据、`### 自检结论（执行者）`）。  
> **字段约定**：[`../HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) **§5**（`test_strategy`、`failure_paths`、`gates_before_code`）。

---

## 1. Agent 前置规则（占位符未替换 → 必须追问，不得代填）

在按 **执行帽** 读 task、改代码之前，须先做 **占位符扫描**：

1. **若用户粘贴的 Prompt 中仍含有任一未替换占位符**（见 **§2 表「占位符字面量」列**），**禁止**开始改业务代码与配置；**必须先向用户追问**，一次列出所有缺失项，请用户逐条补全后再继续。  
2. **禁止**用假设路径、假设子仓根 **静默替换** 占位符（避免在错误仓库跑 `pytest` / 改错目录）。  
3. **例外**：无关联审查落盘时，`{{AUDIT_REVIEW_PATH_OR_NONE}}` 可填字面 **`无`**；若 task 头部已写明 **`gates_before_code`** 且你未持有审查文档，仍须自证已读完 task 内 **`failure_paths` / `freeze_id` / 必读列表`**，否则按 **拒开工** 仅输出阻塞清单（见 `hats/30-execute-code.md`）。  
4. **关联 SPEC 无**：`{{SPEC_PATHS_OPTIONAL}}` 整段替换为 **`无`**（一字段），不得保留占位符。

---

## 2. 占位符（每次调用前由人替换）

| 占位符字面量（须全部消失于最终粘贴体） | 含义 | 示例 |
|----------------------------------------|------|------|
| `{{TASK_PATH}}` | 主 task 路径（相对工作区根 `Projects/`） | `ai-ink-brain-api-python/docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` |
| `{{SUBPROJECT_ROOT}}` | **逻辑子仓名**（相对 `Projects/`；用于 task 路径前缀，如 `ai-ink-brain/content/tasks/...`） | `ai-ink-brain` |
| `{{WORKTREE_ROOT}}` | **命令与改代码的 cwd**（相对 `Projects/`）；并行任务 **须** 与 invoke/task 的 `worktree_root` 一致；非并行填与 `SUBPROJECT_ROOT` 相同 | `ai-ink-brain` 或 `ai-ink-brain-wt-mermaid-audit` |
| `{{VERIFY_COMMAND}}` | 合并前须绿的 **单条**验证命令（与子仓 CI / task 正文一致；多命令可写「先 X 再 Y」在同格） | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| `{{AUDIT_REVIEW_PATH_OR_NONE}}` | 本轮依赖的 **任务审核** 书面结论路径（相对 `Projects/`）；无则 **`无`** | `ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_v3_sql_ast_and_prompt_injection_audit_R1_20260514.md` 或 `无` |
| `{{SPEC_PATHS_OPTIONAL}}` | 关联 SPEC / 总规，多行时每行一条；无则 **`无`** | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` |

---

## 3. 可复制 Prompt 正文（从下一行起复制到对话）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/hats/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8（合并前必绿命令真值，若与本条 VERIFY 冲突以 task + 子仓 workflow 为准）

输入（已由人工替换占位符；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
{{TASK_PATH}}
- 逻辑子仓（task 路径前缀；相对 Projects/）：
{{SUBPROJECT_ROOT}}
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致，见 docs/harness/README.md「并行分支与 Git worktree」）：
{{WORKTREE_ROOT}}
- 合并前须跑通的验证命令（与 CI / task 一致）：
{{VERIFY_COMMAND}}
- 关联任务审核书面结论路径（无则「无」）：
{{AUDIT_REVIEW_PATH_OR_NONE}}
- 关联 SPEC / 总规（无则「无」）：
{{SPEC_PATHS_OPTIONAL}}

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 `human_gate`（见 docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md）。若任一对 **本帽（30）** 为 `pending` → 仅输出须人改的 `gate_id` 与路径，**拒开工**；禁止代填 `approved`。**例外**：若 invoke 声明 gate 已「人 kickoff 预批」但文件仍为 `pending`，Agent 须向用户二次确认（见 HANDOFF_SEMI_AUTO.md §2.3 预批与二次确认），获得明确文字授权后方可代填，且须在 commit message 注明 `human_gate 由 Agent 按人授权代填`。
1. 通读 task 全文：头部 `gates_before_code`、`audit_profile`、`semi_auto`、`test_strategy` / `test_strategy_note`、`freeze_id`、`failure_paths`、拒开工条件、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足（缺 failure_paths 可操作性、缺验收命令、必读未覆盖等）→ **仅输出 Markdown 阻塞清单**（缺什么、建议回填的小节标题、推荐下一棒角色），**不写**业务实现代码。
3. `test_strategy: required` 时：先增加或调整 **可失败** 的自动化测试（或与实现同 PR 且满足 task 所述 red-green / 可复现失败语义），再改实现；禁止「只写实现、后补测」绕过 task 约定。
4. 在 `{{WORKTREE_ROOT}}` 内按 task 范围改代码/配置（**禁止**在并行另一 worktree/checkout 改同一子仓）；禁止静默扩大 scope；SPEC/task 矛盾走变更请求或交回需求帽，不擅自调和为代码假设。
5. 在 `{{WORKTREE_ROOT}}` 执行 `{{VERIFY_COMMAND}}`（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 `hats/40-self-check.md` 将结论与命令摘要 **回填** 至 task 正文 **`### 自检结论（执行者）`**（无则新增该小节）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 在 {{SUBPROJECT_ROOT}} 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
9. **半自动下一棒（可选）**：若 task `semi_auto: true` 且下一棒（如 40）无 `human_gate` 阻塞：先将 **下一棒 §3 全文** 落盘新 invoke 并 commit，再切换角色执行；规则见 HANDOFF_SEMI_AUTO.md §3。否则仅输出下一棒 Prompt 供人开新会话。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出。
```

---

## 4. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：与 `templates/TEMPLATE-task-audit-invoke` 对称；链 `30` / `40` / HARNESS §5 |
| 2026-05-14 | v1.1：用途链 **自检** 调用模板 `templates/TEMPLATE-self-check-invoke`（仅验证路径） |
| 2026-05-14 | v1.2：§3 增第 7 条对话收口；自检回填与「下一棒可复制 Prompt」分拆 |
| 2026-05-14 | v1.3：§3 可复制正文增第 **0** 条 **Invoke 快照（开帽起点）** |
| 2026-05-20 | v1.4：§2/§3 增 **`{{WORKTREE_ROOT}}`**；并行分支 cwd 真值见 `docs/harness/README.md` |
| 2026-05-24 | v1.5：§3 第 0b 条人工闸增加「预批二次确认」与 commit message 注明要求

---

## 给 Cursor

`Harness`、`templates/TEMPLATE-execute-invoke`、`30-execute-code`、`40-self-check`、`templates/TEMPLATE-self-check-invoke`、`拒开工`、`test_strategy`、`VERIFY_COMMAND`、`SUBPROJECT_ROOT`、`自检结论`
