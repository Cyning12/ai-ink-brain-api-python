# 三方 Agent · Wiki-CTX-AB P1 验收 Prompt（可复制 §3）

> **角色**：未参与本 Epic 实现的 **复检 / 评测 Agent**（等同 Harness **50 帽** 裁剪输入，但本实验 **不要求** 改代码）。  
> **freeze_id**：`WIKI-CTX-AB@2026-05-25`  
> **题集真值**：[`questions.md`](./questions.md)  
> **填表**：[`scorecard.md`](./scorecard.md) → 人审后写 [`conclusion_p1_zh.md`](./conclusion_p1_zh.md)

---

## 元信息（执行前由人填写）

| 字段 | 值 |
| --- | --- |
| **model** | （例：`gpt-4o` / `claude-sonnet-4`） |
| **temperature** | `0` 或 `0.1`（两臂须相同） |
| **date** | YYYY-MM-DD |
| **payload 实例** | `payloads/H-full_harness-p1-docs-consolidation.md` · `payloads/H-lean_harness-p1-docs-consolidation.md` |
| **slug** | `harness-p1-docs-consolidation` |

---

## §0 硬约束（违反则本次 run 作废）

1. **禁止** 读取载荷清单以外的任何仓库文件（含 invoke 原文、联网、本对话历史中的其它路径）。  
2. 每个 **臂 × 每题** 为 **独立会话**（或独立 thread）：不得在同一上下文中先答 H-lean 再答 H-full 同一题。  
3. 仅依据载荷内 `--- FILE: ... ---` 区块作答；无信息则答 **「载荷未提供」**，不得猜测。  
4. 输出须可被 `scorecard.md` 逐题勾选；不得省略题号。

---

## §1 任务说明

对比 **H-full**（扫 by-task 全过程）与 **H-lean**（README 摘录 + done task + schedule 片段）在 **同一 gold 题集** 下的：

- **正确性**（对照 `questions.md` 标准答案要点）  
- **载荷规模**（`payload_char_count` 由人在物化时已写入 payload 文首统计表）  
- **幻觉**（是否出现载荷未出现的路径、freeze_id、Epic 名）

---

## §2 执行顺序（必须按序）

```text
FOR arm IN [H-full, H-lean]:
  打开 payloads/{arm}_harness-p1-docs-consolidation.md
  FOR q IN [Q1, Q2, Q3, Q4]:
    新开会话 → 粘贴 §3 调用体（替换 {{ARM}} {{Q_ID}}）
    记录回答 → 填入 scorecard.md
```

---

## §3 可复制 Prompt（单题 · 替换后发给模型）

```text
你是 Wiki-CTX-AB P1 的答题 Agent。你只能使用用户下一条消息附带的「载荷正文」。

【臂】{{ARM}}
【题号】{{Q_ID}}
【freeze_id】WIKI-CTX-AB@2026-05-25

规则：
- 禁止引用载荷外信息。
- 答案用简体中文，条理清晰。
- 若载荷无相关信息，只回答「载荷未提供」。

---

【本题提问】
（从 questions.md 复制对应 Q 的「提问（原文）」全文）

---

【载荷正文】
（粘贴当前臂的完整 payload 文件正文，含 FILE 分隔符）
```

### 题面速查（嵌入 questions.md · 勿改字）

**Q1**  
> 本 Epic（`task_harness_p1_docs_consolidation_v1`）在 **范围** 内必须完成的两项文档交付是什么？请各用一句话说明路径。

**Q2**  
> 该 done task 头部 `test_strategy` 取值是什么？`test_strategy_note` 用一句话说明原因。

**Q3**  
> 该 task 的 `freeze_id` 是什么？状态行显示的关账日期（YYYY-MM-DD）？

**Q4**  
> `RECENT_TASK_SCHEDULE` §0.4 中的 **P1-1**（工作区 reviews pointer）是否在本 task 的 **范围** 内？为什么？

---

## §4 验收测试集（人工打分 · pass/fail）

> 真值要点见 [`questions.md`](./questions.md)；下表为三方 Agent 交付物检查清单。

| ID | 检查项 | pass 条件 |
| --- | --- | --- |
| **T1** | 覆盖率 | Q1–Q4 × H-full × H-lean 共 **8** 条回答均已落盘 scorecard |
| **T2** | Q1 正确性 | 两臂均命中 P1-3（`human_gate` 速查）+ P1-2（`skills/README` 六类 SKILL） |
| **T3** | Q2 正确性 | 两臂均为 `not_applicable` + 纯文档理由 |
| **T4** | Q3 正确性 | 两臂均为 `HARNESS-P1-DOCS@2026-05-23` + **2026-05-23** |
| **T5** | Q4 正确性（陷阱） | 两臂均答 **不在范围** + 非范围/工作区 pointer 依据 |
| **T6** | 无幻觉 | 8 条回答均 **未** 编造载荷外路径或错误 Epic |
| **T7** | 载荷效率 | 记录 H-full 与 H-lean 的 `payload_char_count`；H-lean 总 char **显著小于** H-full（建议 ≥30%，人定阈值见 SPEC §3.1） |
| **T8** | 正确性不降 | H-lean 正确题数 **≥** H-full 正确题数（允许相等，不得少 2 题以上） |

**P1 实验签收（草案）**

- **T7 + T8 同时满足** → `conclusion_p1_zh.md` 写「推荐推进 Harness taxonomy 全仓推广（T3）」  
- **T8 失败** → 先修 H-lean 载荷边界或 README，**暂停 T3**  
- **T7 失败但 T8 通过** → 推广 taxonomy，但不承诺默认 Wiki

---

## §5 三方 Agent 须提交的产出

1. 已填写的 [`scorecard.md`](./scorecard.md)（§P1 八行 + 汇总表）。  
2. 简短 **异常说明**（若有）：某题拒答、载荷损坏、模型违规读盘等。  
3. **不** 修改 `payloads/` 源文件与 `questions.md`。

人审后由维护者撰写 `conclusion_p1_zh.md` 并更新 `task_wiki_ctx_ab_v1.md` / [`RECENT_TASK_SCHEDULE.md`](../../../tasks/RECENT_TASK_SCHEDULE.md) §6.6。

---

## §6 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：P1 三方验收 Prompt + 测试集 T1–T8 |

---

## 给 Cursor

`Wiki-CTX-AB`、`50`、`H-full`、`H-lean`、`scorecard`、`questions.md`、三方 Agent
