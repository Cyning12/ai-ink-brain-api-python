# 规格 / 任务审查（短评）· 对话调用模板（与 `20-review-spec-task` 配套）

> **用途**：复制下文 **§3 可复制 Prompt 正文** 到对话，替换 **§2 占位符** 后发起 **规格与 task 审查帽**（**仅对话内**缺口列表 + 建议补句；**默认不要求**写 `docs/harness/reviews/`）。  
> **帽子真值**：[`20-review-spec-task.md`](20-review-spec-task.md)（与 [`22-task-audit.md`](22-task-audit.md) 分工）。  
> **字段约定**：[`../HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) **§5**。  
> **需要书面闭环、签收 / 关闭**：改用 [`TEMPLATE-task-audit-invoke.md`](TEMPLATE-task-audit-invoke.md) + [`22-task-audit.md`](22-task-audit.md)。

---

## 1. Agent 前置规则（占位符未替换 → 必须追问，不得代填）

在按 **审查短评帽** 输出阻塞/非阻塞列表之前，须先做 **占位符扫描**：

1. **若用户粘贴的 Prompt 中仍含有任一未替换占位符**（见 **§2 表**），**禁止**开始评审；**必须先向用户追问**，一次列出所有缺失项后再继续。  
2. **禁止**假装已阅读未提供的 SPEC/task 全文（路径或粘贴说明必须真实）。  
3. **`{{FOCUS_OR_NONE}}`**：无额外重点时填字面 **`无`**；留空视为未替换，须追问。

---

## 2. 占位符（每次调用前由人替换）

| 占位符字面量（须全部消失于最终粘贴体） | 含义 | 示例 |
|----------------------------------------|------|------|
| `{{SPEC_OR_TASK_PATHS_OR_PASTE_NOTE}}` | 待审 SPEC 与/或 task 的**相对路径**（`Projects/` 起），多行一条一路径；若正文在**下一条消息**，写 **`全文见下一条消息`** | `…/SPEC-….md` 与 `…/task_….md` |
| `{{FOCUS_OR_NONE}}` | 希望评审侧重的词，如「验收可执行性」「freeze_id」「与 manifest」；无则 **`无`** | `无` |

---

## 3. 可复制 Prompt 正文（从下一行起复制到对话）

```text
你正在扮演工作区 Harness「规格 / 任务审查帽（短评）」，严格遵循：
- docs/harness/prompts/20-review-spec-task.md（身份、只做什么、禁止什么；不要求默认落盘 reviews）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、freeze_id 等可测性）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【待审材料路径或粘贴说明】
{{SPEC_OR_TASK_PATHS_OR_PASTE_NOTE}}

【评审侧重点（无则写「无」）】
{{FOCUS_OR_NONE}}

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 分栏或分列表输出：阻塞项（缺了执行帽不能开工）vs 非阻塞建议。
2. 每条阻塞/建议尽量给出：位置（章节/标题）→ 问题 → 建议补一句（短句）。
3. 对 test_strategy: required 的 task：检查是否存在可失败自动化测试计划或等价说明；缺失则列入阻塞项。
4. 契约变更须提示冻结点升级（freeze_id 或等价基准）。
5. 禁止：输出完整改写版 SPEC（除非用户明确要求「修订草案」）；在缺 failure_paths 或验收不可执行时写「可开工」。
6. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
7. **自动 commit**：在输出下一棒 Prompt 后，若本轮有 invoke 等磁盘变更，按 docs/harness/prompts/HANDOFF_AUTO_COMMIT.md 分仓 commit；仅对话、零文件变更则不必空提交。用户写明「不要 commit」则跳过。

若用户明确要求落盘审查文档，应提示其改用 docs/harness/prompts/TEMPLATE-task-audit-invoke.md（任务审核帽 22）。
```

---

## 4. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：与 `20-review-spec-task` 关联；占位符未替换则 Agent 追问 |
| 2026-05-14 | v1.1：§3 增对话收口「下一棒可复制 Prompt」（含打回、二次审查、上一棒修复） |
| 2026-05-14 | v1.2：§3 可复制正文增第 **0** 条 **Invoke 快照**；**22** 审查 md 须填 `invoke_snapshot` |

---

## 给 Cursor

`Harness`、`TEMPLATE-review-spec-task-invoke`、`20-review-spec-task`、`可测性`、`failure_paths`、`22-task-audit`、`追问`
