# 三方 Agent · Wiki-CTX-AB P2 验收 Prompt（可复制 §3）

> **角色**：未参与本 Epic 的 **评测 Agent**（或 30 帽内严格执行）。  
> **freeze_id**：`WIKI-CTX-AB@2026-05-25`  
> **phase**：**P2** · H-lean vs **W**  
> **题集**：[`questions.md`](./questions.md)（与 P1 相同四题）  
> **填表**：[`scorecard.md`](./scorecard.md) §P2 → 人审后写 [`conclusion_p2_zh.md`](./conclusion_p2_zh.md)

---

## 元信息（执行前由人填写）

| 字段 | 值 |
| --- | --- |
| **model** | |
| **temperature** | `0` 或 `0.1`（两臂须相同） |
| **date** | YYYY-MM-DD |
| **payload 实例** | `payloads/H-lean_harness-p1-docs-consolidation.md` · `payloads/W_harness-p1-docs-consolidation.md` |
| **slug** | `harness-p1-docs-consolidation` |

---

## §0 硬约束（违反则本次 run 作废）

1. **禁止** 读取载荷清单以外的任何仓库文件。  
2. 每个 **臂 × 每题** 为 **独立会话**：不得同上下文先答 H-lean 再答 W。  
3. 仅依据载荷内 `--- FILE: ... ---` 区块作答；无信息则 **「载荷未提供」**。  
4. W 臂 **禁止** 使用 `docs/harness/`、`docs/tasks/done/` 全文（载荷外）。

---

## §1 任务说明

在 **H-lean（P1 基线）** 与 **W（仅 Wiki）** 上，用同一 gold 题集比较：

- **正确性**（对照 `questions.md` 要点）  
- **载荷规模**（各臂 `payload_char_count` 见物化统计表）  
- **幻觉**（载荷外路径 / freeze_id / Epic 名）

---

## §2 执行顺序

```text
FOR arm IN [H-lean, W]:
  打开 payloads/{arm}_harness-p1-docs-consolidation.md
  FOR q IN [Q1, Q2, Q3, Q4]:
    新开会话 → 粘贴 §3 调用体（替换 {{ARM}} {{Q_ID}}）
    记录回答 → 填入 scorecard.md §P2
```

---

## §3 可复制 Prompt（单题）

```text
你是 Wiki-CTX-AB P2 的答题 Agent。你只能使用用户下一条消息附带的「载荷正文」。

【臂】{{ARM}}
【题号】{{Q_ID}}
【freeze_id】WIKI-CTX-AB@2026-05-25

规则：
- 禁止引用载荷外信息。
- 答案用简体中文。
- 无相关信息只答「载荷未提供」。

【本题提问】
（从 questions.md 复制对应 Q 的「提问（原文）」）

【载荷正文】
（粘贴当前臂完整 payload）
```

### 题面速查（勿改字）

**Q1**  
> 本 Epic（`task_harness_p1_docs_consolidation_v1`）在 **范围** 内必须完成的两项文档交付是什么？请各用一句话说明路径。

**Q2**  
> 该 done task 头部 `test_strategy` 取值是什么？`test_strategy_note` 用一句话说明原因。

**Q3**  
> 该 task 的 `freeze_id` 是什么？状态行显示的关账日期（YYYY-MM-DD）？

**Q4**  
> `RECENT_TASK_SCHEDULE` §0.4 中的 **P1-1**（工作区 reviews pointer）是否在本 task 的 **范围** 内？为什么？

---

## §4 验收测试集（P2 · 人工打分）

| ID | 检查项 | pass 条件 |
| --- | --- | --- |
| **T1** | 覆盖率 | Q1–Q4 × H-lean × W 共 **8** 条落盘 scorecard §P2 |
| **T2–T5** | 正确性 | 同 P1 要点（见 questions.md） |
| **T6** | 无幻觉 | 8 条均无载荷外编造 |
| **T7** | 载荷效率 | W 总 char **显著小于** H-lean（建议 ≥30%，人定） |
| **T8** | 正确性不降 | W 正确题数 **≥** H-lean（允许相等） |

**P2 签收（草案）**

- **T7 + T8 同时满足** → `conclusion_p2_zh.md` 写「推荐默认先读 coding_wiki」  
- **T8 失败** → 不升 Wiki 默认读序；仅关账后可选 ingest  
- **T7 失败、T8 通过** → Wiki 可用但不写默认读序

---

## §5 产出

1. 已填 `scorecard.md` §P2。  
2. 异常说明（若有）。  
3. **不** 修改 `payloads/` 源与 `questions.md`。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：P2 H-lean vs W |
