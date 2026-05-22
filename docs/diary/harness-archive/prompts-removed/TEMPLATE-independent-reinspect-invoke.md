# 独立复检 + 全局验收 · 对话调用模板（与 `50-independent-reinspect` 配套）

> **用途**：复制下文 **§3 可复制 Prompt 正文** 到对话，替换 **§2 占位符** 后发起 **`50`**：**§一 独立复检** 与/或 **§二 全局验收**（人签 checklist 辅助）。  
> **帽子真值**：[`50-independent-reinspect.md`](50-independent-reinspect.md)（复检输入裁剪、输出形状、全局验收禁止项）。  
> **前置**：task 内 **`### 自检结论（执行者）`** 应已存在（见 [`40-self-check.md`](40-self-check.md)、[`TEMPLATE-self-check-invoke.md`](TEMPLATE-self-check-invoke.md)）；缺失则复检帽须在 **阻塞项** 首条写明。  
> **可选输入**：终轮任务审核 **`签收 / 关闭`** 节路径（`docs/harness/reviews/` 或子仓 `…/harness/reviews/` 下 `*_audit_*.md`）。  
> **全量升级（可选）**：需要结构化输出节（`failure_paths` 逐项、`test_strategy` 专节、按子仓 checklist、PR 小结等）时，改用 [`TEMPLATE-independent-reinspect-invoke-full.md`](TEMPLATE-independent-reinspect-invoke-full.md)；占位符已填示例见 [`EXAMPLE-invoke-independent-reinspect-both-chatbi-p1-1.md`](EXAMPLE-invoke-independent-reinspect-both-chatbi-p1-1.md)。**§3 短版仍为默认轻量入口**，全量模板不替代短版与 `50` 正文。

---

## 1. Agent 前置规则（占位符未替换 → 必须追问，不得代填）

在按 **复检 / 全局验收帽** 输出表格与合并建议之前，须先做 **占位符扫描**：

1. **若用户粘贴的 Prompt 中仍含有任一未替换占位符**（见 **§2 表**），**禁止**开始评审；**必须先向用户追问**，一次列出所有缺失项后再继续。  
2. **`{{REINSPECT_MODE}}`** 必须为以下**字面之一**（不可自创）：`独立复检`、`全局验收`、`两者`。否则须追问让用户三选一。  
3. **`{{AUDIT_REVIEW_PATH_OR_NONE}}`**：无审查文档时填 **`无`**；留空视为未替换，须追问。  
4. **`{{DIFF_RANGE_OR_NOTE}}`**：在 **独立复检** 或 **两者** 模式下若写 **`无`**，须在输出中声明「diff 证据不足」风险并列入阻塞或非阻塞建议；**全局验收** 单独模式下可填 **`无`**（以 checklist 为主）。

---

## 2. 占位符（每次调用前由人替换）

| 占位符字面量（须全部消失于最终粘贴体） | 含义 | 示例 |
|----------------------------------------|------|------|
| `{{TASK_PATH}}` | 主 task 路径（相对工作区根 `Projects/`） | `…/docs/tasks/active/task_….md` |
| `{{SUBPROJECT_ROOT}}` | 理解与拉取 **git diff** 时的 cwd（相对 `Projects/`）；仅做全局验收且不需 diff 时仍建议填子仓根 | `ai-ink-brain-api-python` |
| `{{REINSPECT_MODE}}` | **`独立复检`** \| **`全局验收`** \| **`两者`**（三选一，照抄其一） | `独立复检` |
| `{{DIFF_RANGE_OR_NOTE}}` | 供复检对照的 diff 说明：如 `git diff origin/main...HEAD`、或 patch 路径、或 `无` | `origin/main...HEAD` |
| `{{AUDIT_REVIEW_PATH_OR_NONE}}` | 任务审核终轮文档路径（读取 **签收/关闭**）；无则 **`无`** | `无` |

---

## 3. 可复制 Prompt 正文（从下一行起复制到对话）

```text
你正在扮演工作区 Harness「独立复检 + 全局验收帽」，严格遵循：
- docs/harness/prompts/50-independent-reinspect.md（§一 独立复检；§二 全局验收）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: required 时关注测试与实现关系）
- 根目录 AGENTS.md §8、docs/harness/HARNESS_V2_P0_ACCEPTANCE.md（若本次变更触及合并前必绿子仓）

输入（已由人工替换占位符；若你仍看到 {{…}} 或 REINSPECT_MODE 非三选一字面，须先追问用户，不得开工）：
- 主 task 路径：
{{TASK_PATH}}
- 子仓根（相对 Projects/；用于理解 diff 与路径）：
{{SUBPROJECT_ROOT}}
- 模式（必须恰好为以下之一：独立复检 / 全局验收 / 两者）：
{{REINSPECT_MODE}}
- diff 或变更范围说明（全局验收单独模式可写「无」）：
{{DIFF_RANGE_OR_NOTE}}
- 任务审核书面结论路径（无则「无」）：
{{AUDIT_REVIEW_PATH_OR_NONE}}

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列分节实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。

【当模式为「独立复检」或「两者」时 — 对应 hat §一】
1. 读取 task 内「### 自检结论（执行者）」；若缺失 → 阻塞首条：要求先跑 TEMPLATE-self-check-invoke + 40。
2. 输入裁剪：以 diff、命令输出要点、自检验收表为主；避免执行过程长文。
3. 对 task 每条验收项输出表格：验收项 | pass/fail | 证据（文件:行 / 测试名 / 日志片段）| 备注；fail 须写复现步骤或缺失证据。
4. 汇总阻塞合并项；给出是否建议合并（供维护者决策）。
5. 禁止：替执行者改代码（除非用户明确要求复检提交 patch）；缺口退回需求/审查帽。

【当模式为「全局验收」或「两者」时 — 对应 hat §二】
6. 若 task 声明 freeze_id：核对 PR 变更是否在冻结基准内；契约升级是否在 SPEC/task 显式记录。
7. 输出 checklist 表（项 / 状态 / 签注栏「待人工」）；不伪造已签核；不跳过 CI 红灯叙事。

对话回复：若建议合并且无返工 → 输出「执行路线与 Commit 回溯」（docs/harness/prompts/HANDOFF_CLOSE_TRACE.md），勿编造下一棒 Prompt；若须打回 → 输出下一棒可复制 Prompt（含打回、二次审查、上一棒修复）。
8. **自动 commit**：落盘后按 docs/harness/prompts/HANDOFF_AUTO_COMMIT.md 分仓 commit。仅对话、零文件变更则不必空提交；用户写明「不要 commit」则跳过。
```

---

## 4. 与全量模板的关系（升级落盘）

| 版本 | 文件 | 何时用 |
|------|------|--------|
| 短版（默认） | 本文 **§3** | token 紧、仅需 hat 级指令与最小输出条款 |
| 全量（升级） | [`TEMPLATE-independent-reinspect-invoke-full.md`](TEMPLATE-independent-reinspect-invoke-full.md) **§3** | 需要 **A～D 输出节**、`failure_paths` / `test_strategy` 专节、按 `SUBPROJECT_ROOT` 拆 checklist、可选 `PR_OR_CI` |
| 已填示例 | [`EXAMPLE-invoke-independent-reinspect-both-chatbi-p1-1.md`](EXAMPLE-invoke-independent-reinspect-both-chatbi-p1-1.md) | ChatBI P1-1；由全量模板复制后替换占位符 |

---

## 5. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：与 `50-independent-reinspect` 关联；MODE 三选一；占位符未替换则 Agent 追问 |
| 2026-05-14 | v1.1：链全量模板 `TEMPLATE-independent-reinspect-invoke-full` 与 EXAMPLE；增 **§4 关系表** |
| 2026-05-14 | v1.2：§3 对话收口改为「下一棒可复制 Prompt」（含打回、二次审查、上一棒修复） |
| 2026-05-14 | v1.3：§3 可复制正文增第 **0** 条 **Invoke 快照（开帽起点）** |

---

## 给 Cursor

`Harness`、`TEMPLATE-independent-reinspect-invoke`、`TEMPLATE-independent-reinspect-invoke-full`、`EXAMPLE-invoke-independent-reinspect-both-chatbi-p1-1`、`50-independent-reinspect`、`复检`、`全局验收`、`自检结论`、`reviews`、`占位符`、`追问`
