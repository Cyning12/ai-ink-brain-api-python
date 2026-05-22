# 需求 / 任务分析 · 对话调用模板（与 `10-requirements` 配套）

> **用途**：复制下文 **§3 可复制 Prompt 正文** 到对话，替换 **§2 占位符** 后发起 **需求与任务分析帽**（不写业务代码、不改 CI）。  
> **下一棒（书面再审）**：task 正文已按清单回填后 → [`TEMPLATE-task-audit-invoke.md`](TEMPLATE-task-audit-invoke.md) **§3** + [`22-task-audit.md`](22-task-audit.md) 产出 **R+1**。  
> **帽子真值**：[`10-requirements.md`](10-requirements.md)（身份、禁止项、输出形状、与 `22` 回填交接）。  
> **字段约定**：[`../HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) **§5**（`test_strategy`、`failure_paths` 等）。  
> **上一棒（可选）**：若由任务审核驱动回填，先读 [`docs/harness/reviews/`](../reviews/README.md) 中对应 `*_audit_*.md` 的清单；发起 **书面再审** 请用 [`TEMPLATE-task-audit-invoke.md`](TEMPLATE-task-audit-invoke.md) + [`22-task-audit.md`](22-task-audit.md)。

---

## 1. Agent 前置规则（占位符未替换 → 必须追问，不得代填）

在按 **需求帽** 产出结构化草案或缺口清单之前，须先做 **占位符扫描**：

1. **若用户粘贴的 Prompt 中仍含有任一未替换占位符**（见 **§2 表**），**禁止**开始分析与「代写进仓」；**必须先向用户追问**，一次列出所有缺失项，请用户补全后再继续。  
2. **禁止**编造未给出的 SPEC/task 路径或审查文件名。  
3. **`{{AUDIT_REVIEW_PATH_OR_NONE}}`**：无审查驱动时填字面 **`无`**；留空视为未替换，须追问。

---

## 2. 占位符（每次调用前由人替换）

| 占位符字面量（须全部消失于最终粘贴体） | 含义 | 示例 |
|----------------------------------------|------|------|
| `{{GOAL_AND_CONTEXT}}` | 目标与上下文：要解决什么、约束、读者是谁（**必填**） | 「把 X 写成可验收 task 草案」 |
| `{{SPEC_OR_TASK_PATHS_OR_PASTE_NOTE}}` | 已存在的 SPEC/task **相对路径**（`Projects/` 起），多行一条一路径；若正文将贴在**下一条消息**，此处写 **`全文见下一条消息`**（五字照抄） | `ai-ink-brain-api-python/docs/tasks/active/task_….md` |
| `{{AUDIT_REVIEW_PATH_OR_NONE}}` | 若按 **`22`** 审查回填：填 `docs/harness/reviews/…_audit_R….md`；否则 **`无`** | `无` |

---

## 3. 可复制 Prompt 正文（从下一行起复制到对话）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
{{GOAL_AND_CONTEXT}}

【已有材料路径或粘贴说明】
{{SPEC_OR_TASK_PATHS_OR_PASTE_NOTE}}

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
{{AUDIT_REVIEW_PATH_OR_NONE}}

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 [`../invokes/README.md`](../invokes/README.md) 落盘到 `docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
3. 若 AUDIT 路径非「无」：按该审查文档的回填清单逐条映射到 task 小节建议，并在建议文末注明「按审查 R<n> 回填」应指向的文件名。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值。
5. 对话回复 — **下一棒须输出两条 Prompt（由人择一执行，不可只给一条）**：
   - 先输出 **推荐判定**（1～3 行）：依据 [`10-requirements.md`](10-requirements.md) **§下一棒 A/B** 规则表与 task 元信息（`audit_profile`、`test_strategy`、显式声明）；写明 **推荐 A 或 B** 及一行理由。
   - **路径 A · 22 任务审核**：标题 `### 下一棒 A：22 任务审核 R1`；若推荐 A 则 `### 下一棒 A：22 任务审核 R1（推荐）`。正文 = 已替换占位符的 [`TEMPLATE-task-audit-invoke.md`](TEMPLATE-task-audit-invoke.md) **§3 全文**（`{{TASK_PATH}}` 等指向本仓 task；审查落盘 `docs/harness/reviews/task_<slug>_audit_R1_YYYYMMDD.md`）。
   - **路径 B · 30 执行（跳过 22）**：标题 `### 下一棒 B：30 执行（跳过 22）`；若推荐 B 则 `### 下一棒 B：30 执行（跳过 22）（推荐）`。正文 = 已替换占位符的 [`TEMPLATE-execute-invoke.md`](TEMPLATE-execute-invoke.md) **§3 全文**。**选 B 时** 须在推荐判定中注明：人承担闸 1；hotfix 须 task 写明事后补 22 或 `post_close` 闸 2。
   - 两条均须 **全文**、可独立复制进新对话；**禁止** 因推荐只给一条或自动执行下一帽。
6. 回复末尾输出 **[`HANDOFF_SEMI_AUTO.md`](HANDOFF_SEMI_AUTO.md) §3.4** `📋 Harness 状态栏（版本 B）`（`下一棒` 行列出 A/B；`推荐` 行与第 5 条一致；**不得** 代填 `human_gate: approved`）。
7. **自动 commit**：若本轮已落盘 invoke 或已按用户授权写入 task，在输出下一棒 Prompt 与状态栏后按 [`HANDOFF_AUTO_COMMIT.md`](HANDOFF_AUTO_COMMIT.md) 分仓 commit（仅本轮路径；对话报 short-hash）。仅对话、零文件变更则不必空提交；用户写明「不要 commit」则跳过。

不强制落盘；若用户要求写入某 task 文件，须由用户明确路径后再编辑（本模板不预置写文件占位符）。
```

---

## 4. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：与 `10-requirements` 关联；占位符未替换则 Agent 追问 |
| 2026-05-14 | v1.1：§3 增对话收口「下一棒可复制 Prompt」（含打回、二次审查、上一棒修复） |
| 2026-05-14 | v1.2：§3 可复制正文增第 **0** 条 **Invoke 快照（开帽起点）** |
| 2026-05-22 | v1.3：§3 第 5–7 条 — A/B `（推荐）`、推荐判定、§3.4 状态栏；禁止自动走路径 |

---

## 给 Cursor

`Harness`、`TEMPLATE-requirements-invoke`、`10-requirements`、`下一棒 A`、`下一棒 B`、`（推荐）`、`人择一`、`failure_paths`、`test_strategy`、`Harness 状态栏`、`reviews`、`追问`
