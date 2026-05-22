# 任务审核 · 对话调用模板（与 `22-task-audit` 配套）

> **用途**：复制下文 **§3 可复制 Prompt 正文** 到对话，替换 **§2 必填占位符** 后发起 **任务审核帽** 审查。  
> **下一棒（回填 task）**：审查含 **需任务帽回填** 清单时 → [`TEMPLATE-requirements-invoke.md`](TEMPLATE-requirements-invoke.md) **§3** + [`10-requirements.md`](10-requirements.md)；回填后再用本模板 **R+1** 复审。  
> **下一棒（执行）**：审查无阻塞后，可复制 [`TEMPLATE-execute-invoke.md`](TEMPLATE-execute-invoke.md) **§3** 发起 **执行帽**（占位符规则同型）。  
> **帽子真值**：[`22-task-audit.md`](22-task-audit.md)（身份、禁止项、落盘路径、闭环）。  
> **审查产出命名**：[`../reviews/README.md`](../reviews/README.md)。  
> **字段约定**：[`../HARNESS_V2_PLAN.md`](../HARNESS_V2_PLAN.md) **§5**（`test_strategy`、`failure_paths` 等）。

---

## 1. Agent 前置规则（占位符未替换 → 必须追问，不得代填）

在按 **任务审核帽** 阅读 task、撰写审查 md 之前，须先做 **占位符扫描**：

1. **若用户粘贴的 Prompt 中仍含有任一未替换占位符**（见 **§2 表「占位符字面量」列**），**禁止**开始审查与落盘；**必须先向用户追问**，一次列出所有缺失项，请用户逐条补全后再继续。  
2. **禁止**用假设路径、假设 slug、假设日期 **静默替换** 占位符（避免审查文件命名与关联 task 错位）。  
3. **例外**：无复审时，`{{PREV_REVIEW_PATH_OR_NONE}}` 的合法取值为字面 **`无`**（一字）；若用户留空该占位符，视为未替换，仍须追问「首轮填 `无`，或提供上一轮 `reviews` 文件路径」。

---

## 2. 占位符（每次调用前由人替换）

| 占位符字面量（须全部消失于最终粘贴体） | 含义 | 首轮示例 | 复审示例 |
|----------------------------------------|------|----------|----------|
| `{{TASK_PATHS}}` | 待审 task 路径（相对工作区根 `Projects/`），多行时每行一条 | `ai-ink-brain-api-python/docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` | 同左或多条 |
| `{{SPEC_PATHS_OPTIONAL}}` | 关联 SPEC，无则整段替换为 **`无`** | `ai-ink-brain-api-python/docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` | 同左或 `无` |
| `{{PREV_REVIEW_PATH_OR_NONE}}` | 上一轮审查文档相对路径（**工作区根**）；**首轮**填 **`无`** | `无` | `ai-ink-brain-api-python/docs/harness/reviews/task_…_audit_R1_20260514.md` |
| `{{AUDIT_ROUND}}` | 本轮轮次，与文件名 `R<n>` 一致 | `R1` | `R2` |
| `{{YYYYMMDD}}` | 落盘日期 | `20260514` | `20260515` |
| `{{SLUG}}` | 审查文件名用短名，建议与 task 文件名主体一致（不含 `task_` 前缀亦可，但须与本轮 `reviews` 文件一致） | `chatbi_v3_sql_ast_text2sql_gate_v1` | 同左 |

---

## 3. 可复制 Prompt 正文（从下一行起复制到对话）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths 等与 task 字段对齐）

输入（已由人工替换占位符；若你仍看到 {{…}} 或本段「待填」字样，须先追问用户，不得开工）：
- 待审 task 路径（相对工作区根 Projects/）：
{{TASK_PATHS}}
- 关联 SPEC / 总规路径（无则写「无」）：
{{SPEC_PATHS_OPTIONAL}}
- 上一轮审查文档路径（首轮写「无」；复审必填）：
{{PREV_REVIEW_PATH_OR_NONE}}

落盘文件建议名（须与文内元信息一致；若与用户输入冲突以用户为准并追问）：
- 待审 task 在 **`ai-ink-brain-api-python/docs/tasks/`** 下：`ai-ink-brain-api-python/docs/harness/reviews/task_{{SLUG}}_audit_{{AUDIT_ROUND}}_{{YYYYMMDD}}.md`（全文真值）；工作区 `docs/harness/reviews/` 可仅存指针链至此路径。  
- 否则：`docs/harness/reviews/task_{{SLUG}}_audit_{{AUDIT_ROUND}}_{{YYYYMMDD}}.md`

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。你在步骤 3 落盘审查 md 时，须在文首元信息表增加 **`invoke_snapshot`** 指向该 invoke 文件（相对 `Projects/`）。同一会话内追问 **不** 再新增快照文件。
1. 通读待审 task 全文及头部元信息（状态、freeze_id、gates_before_code、test_strategy、failure_paths、验收、必读链接）。
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性、required 与可失败自动化测试说明。
3. 落盘一篇审查文档至 **上表路径**（与 `reviews/README.md`、`22-task-audit.md` 子仓规则一致）。
4. 文内结构：元信息 → 审查结论摘要 → 阻塞 / 非阻塞 → 需任务帽回填清单（若有）→ 是否建议执行帽开工 → 「签收 / 关闭」→ 收尾二选一：**有下一棒** → **「下一棒可复制 Prompt」**（`text` 围栏，§3 全文）；**终轮无下一棒** → **「执行路线与 Commit 回溯」**（见 docs/harness/prompts/HANDOFF_CLOSE_TRACE.md，含阶段表 + 分仓 commit 列表）。
5. 禁止仅在对话里说「过了」而不写 reviews；禁止在仍有阻塞时指示执行帽开工。
6. 不要写业务实现代码；不要擅自改写 task 正文。
7. **对话与归档**：与步骤 4 审查 md 末节 **逐字或语义一致**——有下一棒则对话输出完整 Prompt；无下一棒则输出完整回溯表，**禁止**用空 Prompt 占位。
8. **自动 commit**：完成步骤 3–7 后，按 docs/harness/prompts/HANDOFF_AUTO_COMMIT.md 在相关 git 根分别 commit（仅本轮路径；对话末尾一行报 short-hash）。用户本轮写明「不要 commit」则跳过。
```

### 影响分析（可选 · 方案2）

当 task 涉及架构模块变更且后端子仓已升 **graph_v2** 时，审查者可 **可选** 执行：

```text
cd ai-ink-brain-api-python
python tools/tech_graph_graph_query.py describe-impact <node_id> 2
```

将输出摘要写入审查 md「非阻塞」或 task `impact` 字段；**非** §3 硬阻塞步骤。

---

## 4. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1.1：后端 `docs/tasks` 绑定 task → 全文落盘 `ai-ink-brain-api-python/docs/harness/reviews/` |
| 2026-05-14 | v1.2：用途链 **执行** 调用模板 `TEMPLATE-execute-invoke`；给 Cursor 关键词增补 |
| 2026-05-14 | v1.3：用途链 **需求帽** 调用模板 `TEMPLATE-requirements-invoke`（回填 → 再审） |
| 2026-05-14 | v1.4：§3 对话收口改为「下一棒可复制 Prompt」（含打回、二次审查、上一棒修复） |
| 2026-05-14 | v1.5：§3 可复制正文增第 **0** 条 **Invoke 快照**；审查落盘时元信息填 `invoke_snapshot` |
| 2026-05-15 | v1.6：§3 文内结构增 **「下一棒可复制 Prompt」**；步骤 7 明确对话与审查 md 须逐字一致 |

---

## 给 Cursor

`Harness`、`TEMPLATE-task-audit-invoke`、`TEMPLATE-requirements-invoke`、`TEMPLATE-execute-invoke`、`22-task-audit`、`10-requirements`、`reviews`、`占位符`、`追问`、`下一棒可复制 Prompt`、`HARNESS_V2_PLAN` §5
