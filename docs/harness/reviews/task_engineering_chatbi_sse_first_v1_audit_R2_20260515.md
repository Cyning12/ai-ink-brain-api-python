# 任务审核书面结论 · R2

## 元信息

| 字段 | 值 |
|------|-----|
| 关联 task | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_chatbi_sse_first_v1.md` |
| 审查轮次 | R2 |
| 落盘日期 | 20260515 |
| 关联 SPEC | 无（与 R1、invoke 输入一致） |
| 上一轮审查 | `ai-ink-brain-api-python/docs/harness/reviews/task_engineering_chatbi_sse_first_v1_audit_R1_20260515.md` |
| invoke_snapshot | **回填/修订环节（需求帽 10）**：`docs/harness/invokes/invoke_20260515_0000_10_engineering-chatbi-sse-first-v1.md`（相对工作区根 `Projects/`）。**R1 任务审核开帽（22，链上参考）**：`docs/harness/invokes/invoke_20260515_0000_22_engineering-chatbi-sse-first-v1.md`。**说明**：本轮 R2 由用户消息直接发起任务审核帽；工作区内**未检出**新建 `invoke_*_22_*` 专用于 R2 的快照文件时，以需求帽 invoke 为与本轮回填成果的并列锚点。 |

**给下一棒**：Harness **任务审核**链条上本 task **已无文档阻塞**；R2 宣告见下文「签收 / 关闭」。**勿**以执行业务代码语义验收本单。若将来仅做「验收首条满足后的仓内归档」，可用文末「下一棒可复制 Prompt」开需求帽（占位符已替换）。

---

## 审查结论摘要

- **对照 R1 非阻塞**：task **§5** 已按 `docs/harness/HARNESS_V2_PLAN.md` **§5.3** 写明四要素口径，并以表格列 **触发 → 行为 → 是否可重试 → 用户可见文案类型**；FP-1 对用户可见列显式 **`N/A`**，与规划「不适用列显式 N/A」一致。  
- **§4 第 2 条**：task 已勾选 `[x]` 并指回本仓 [`docs/tasks/README.md`](../../tasks/README.md)；抽查该文件 **「工程纪律索引」** 小节（约 L33–L35）已含指向本 task 与 R1 审查的相对链接，**回链落锚成立**。  
- **新增观察（非阻塞）**：`README.md` 工程纪律索引条目的审查链接文案仍为「书面审查 **R1**」；R2 落盘后，维护者可**按需**将该链接更新为 R2 或并列 R1/R2，以免索引与「最新审查」语义轻微漂移——**不构成**任务审核打回条件。  
- **§4 首条**仍为 `[ ]`：属**持续性组织验收**（后续含 Unified 行为变更的 task 写法），**不由**本审查帽代为勾选；与「本单为纪律/流程类、非业务实现验收」一致。

---

## 阻塞 / 非阻塞

| 类型 | 项 |
|------|-----|
| **阻塞** | 无。 |
| **非阻塞** | `docs/tasks/README.md`「工程纪律索引」中审查链接仍标 R1；可选更新为 R2 或并列链。 |

---

## 需任务帽回填清单

无（R1 可选清单已在 task 修订记录与正文中闭合）。

---

## 是否建议执行帽开工

**不建议**以「执行本 task 的业务代码」语义启动执行编码帽：本 task **范围**不含 `unified_chat` / `unified_chat_stream` 等实现变更，仅约束后续含 Unified 行为变更的 task 的写法与评审习惯。功能类 task 在通过各自任务审核后，再按 `TEMPLATE-execute-invoke.md` 开工。

---

## 签收 / 关闭（Harness · 终轮 R2）

1. **任务审核帽（`22`）侧**：自本文 **`task_engineering_chatbi_sse_first_v1_audit_R2_20260515.md`** 起，**本 task 在 Harness「书面审查 → 回填对齐」链路上可终局签收**——即：相对 R1 所列非阻塞项，当前 task 与 `docs/tasks/README.md` 锚点已与 **`HARNESS_V2_PLAN.md` §5.3** 及 §4 第 2 条约定对齐，**无待审文档缺口**。  
2. **与 task 头部 `状态` / 物理归档**：**不**等同于「业务交付完成」。task 仍为 `todo`、§4 首条未勾，属**纪律持续生效**与**组织侧待办**；若团队定义「纪律落盘即可 `done`」或首条已满足，须由**人/需求帽**按 `docs/tasks/README.md`「任务归档流程」自行完成头部、`git mv`、`_views` 等——**不在本 Harness 审查帽职责内代为执行**。  
3. **小结**：**Harness 侧本 task 的审核闭环可关闭**；**仓内 `active`→`done` 与全量验收勾选**仍遵循该 task 正文与 `docs/tasks/README.md`，与「非业务代码语义验收」区分。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
任务审核 R2 已签收 `task_engineering_chatbi_sse_first_v1` 的 Harness 文档链闭环（见 `ai-ink-brain-api-python/docs/harness/reviews/task_engineering_chatbi_sse_first_v1_audit_R2_20260515.md`「签收 / 关闭」）。当团队认定 **§4 验收首条**（后续含 Unified 行为变更的 task 显式写明 SSE/JSON 交付关系）已满足或已附书面豁免说明时，请**仅**按 `ai-ink-brain-api-python/docs/tasks/README.md`「任务归档流程」更新本 task：勾选/说明验收、头部 `done`、**git mv** 至 `docs/tasks/done/`、更新 `docs/tasks/_views/done.md` 等；可选同步「工程纪律索引」中的审查链接至 R2。禁止业务实现代码与 CI 变更；禁止在 task 中写绝对本机路径。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_chatbi_sse_first_v1.md

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
无

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
3. 若 AUDIT 路径非「无」：按该审查文档的回填清单逐条映射到 task 小节建议，并在建议文末注明「按审查 R<n> 回填」应指向的文件名。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值。
5. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。

不强制落盘；若用户要求写入某 task 文件，须由用户明确路径后再编辑（本模板不预置写文件占位符）。
```
