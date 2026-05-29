# 三方 Agent · 任务排期读序 smoke（v1）

> **用途**：测评 **未参与本仓 Wiki/排期建设** 的 Agent，能否在 **无显式路径提示** 下找到 L1 排期真值并答对。  
> **freeze_id**：`TASK-SCHEDULE-READ-SMOKE@2026-05-29`  
> **基线快照**：`GOV-TASK-SCHEDULE-WIKI@2026-05-29` · `main` 合入排期 hub 后  
> **题集**：[`questions.md`](./questions.md)  
> **人填结论**：[`scorecard.md`](./scorecard.md)（可选）

---

## 元信息（执行前由人填写）

| 字段 | 值 |
| --- | --- |
| **model** | |
| **Agent 平台** | Cursor / Claude Code / 其它 |
| **Open Folder** | `ai-ink-brain-api-python/`（仅子仓根） |
| **date** | YYYY-MM-DD |
| **是否 @ 了 AGENTS.md / RECENT / concept** | 否（本 smoke **禁止** 在 Prompt 里写路径） |

---

## §0 硬约束（测评纪律）

1. **禁止** 在发给 Agent 的用户消息里写出：`RECENT_TASK_SCHEDULE`、`task-schedule-ink-backend`、`§1.1 #0b` 等 **答案路径**。  
2. **允许** Agent 自行打开仓库内任意文件；记录其 **首条打开路径**（若可观测）。  
3. 每题 **独立会话**（或清空上下文），避免上一题泄漏。  
4. 仅依据 **仓库只读** 作答；禁止假设未写入文档的排期。

---

## §1 测评目标

| # | 能力 |
| --- | --- |
| T1 | 能否找到 **当前后端实现优先棒**（非治理/docs） |
| T2 | 能否说明 **P2-1b 与 P2-1c 先后** 及依据 |
| T3 | 能否区分 **L1 排期真值 vs L2 Wiki 导航**（不混淆） |
| T4 | 能否指出 **Wiki 治理线是否仍占「当前棒」**（陷阱题） |

---

## §2 执行顺序

```text
FOR q IN [Q1, Q2, Q3, Q4]:
  新会话 · Open ai-ink-brain-api-python/
  仅粘贴 §3 调用体（替换 {{Q_ID}}）
  记录：首读路径（可选）· 回答 · pass/fail（对照 questions.md）
```

---

## §3 可复制 Prompt（单题 · 无路径引导）

```text
你是刚接入本后端仓库的工程师 Agent。请 **只读** 仓库文档与任务单，回答下列问题。

【仓库】ai-ink-brain-api-python（FastAPI · RAG / ChatBI）

【题号】{{Q_ID}}

【要求】
- 用简体中文回答，结论先行，再列依据（文件路径或 task 名即可，勿粘贴长文）。
- 若文档无法确定，写「文档未明确」并说明缺什么。
- 不要猜测未写入仓库的排期。

【题目】
{{QUESTION_BODY}}
```

### 题面替换表

| {{Q_ID}} | {{QUESTION_BODY}} |
| --- | --- |
| Q1 | 从仓库现有文档来看，**接下来优先应该落地的是哪一项后端实现工作**（主题 + task 文件名即可）？为什么不是其它 active 项？ |
| Q2 | ChatBI V3 **韧性（P2）** 子线里，**限流** 和 **熔断** 哪个应先做？依据应来自哪里？ |
| Q3 | 若要做 **跨 Epic 排期规划**，本仓 **排期真值** 应读哪一类文档？Coding Wiki 在该场景下扮演什么角色（一句话）？ |
| Q4 | Wiki 治理 / T4 运营化是否仍是 RECENT 里的 **「当前棒」**？当前文档状态下，治理线与业务线谁优先？ |

---

## §4 填表与通过线

- 逐题对照 [`questions.md`](./questions.md) §gold 要点判 pass/fail。  
- **smoke 通过**：Q1–Q3 **至少 3/4 pass**，且 Q4 **必须 pass**（防治理线误判为当前棒）。  
- 可选：记录 Agent **首读文件** 是否经过 `concepts/task-schedule-ink-backend` 或 `RECENT`（仅统计，不作硬门禁）。

---

## §5 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-29 | v1：排期 hub 合入后 smoke · 四题无路径引导 |
