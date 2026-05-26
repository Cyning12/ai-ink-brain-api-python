# 22 审查（R1）· Wiki-CTX-AB P2 开工就绪

## 元信息

| 字段 | 值 |
| --- | --- |
| task_path | `docs/tasks/active/task_wiki_ctx_ab_v1.md` |
| invoke_snapshot | `docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_22_wiki-ctx-ab-p2-v1.md` |
| freeze_id | `WIKI-CTX-AB@2026-05-25` |
| audit_round | `R1` |
| phase | `P2` |
| git_branch | `task/wiki-ctx-ab-p2-v1` |

---

## 审查结论摘要

- **结论**：`R1 无阻塞`，准许进入 P2 执行（30 帽）。
- `human_gate` 核对：`HG-AB-SLUG=approved`、`HG-AB-P1-DONE=approved`，满足开工闸。
- T1b 前置核对：`docs/tasks/done/task_coding_wiki_pilot_v1.md` 已 `done`，且同 slug Wiki 页 `test -f` 存在。
- SPEC §3.1 P2 对照核对：本轮仍是 **H-lean vs W**，题集保持 `questions.md` 四题（Q1-Q4），未要求改 harness prompts/api。

---

## P2 开工焦点

1. **边界焦点**：W 臂必须保持“仅 Wiki 载荷”（`index.md` + 同 slug syntheses），不得回读 `docs/harness/` 与 `docs/tasks/done/` 全文。  
2. **对照焦点**：H-lean 作为 P1 基线臂复用，不得删改 P1 冻结内容行。  
3. **题集焦点**：P2 仍使用 `questions.md` 已锁定 gold 要点，覆盖 Q1–Q4，不增删题。  
4. **流程焦点**：本轮仅做就绪审；答题、填 `scorecard` §P2、产出 `conclusion_p2_zh.md` 全归属 30 帽。

---

## 阻塞 / 非阻塞

### 阻塞（Blocking）

- 无。

### 非阻塞（Non-blocking）

- `payloads/TEMPLATE-W.md` 与 `payloads/W_harness-p1-docs-consolidation.md` 已存在，且 W 物化实例已填 `payload_char_count=2096`。  
- `payloads/H-lean_harness-p1-docs-consolidation.md` 保持 P1 基线信息（含 `payload_char_count=9896` 与 P1 题集语义），当前未见 P2 越界改动。  
- `PROMPT_third_party_agent_wiki_ctx_ab_p2.md` 与实验目录 README 的 P2 跑法说明已就绪。  
- `scorecard.md` 的 §P2 仍为空表待填，符合“22 不跑题答题”的职责边界。

---

## 是否建议 30 帽开工

- **建议开工：是**（前提：沿用本审查边界与禁止项，不跨入载荷外读盘）。

---

## 签收 / 关闭

- **R1 裁定**：`准许进入 P2 执行`。  
- 关闭条件（后续帽链）：30 完成 P2 对照与结论 → 40 自检 → 50 复检 → CLOSE 关账。  
- 本轮不执行 30，不改 `docs/harness/prompts/`、`api/`、CI。

---

## 下一棒可复制 Prompt

> 文件：`docs/harness/invokes/by-task/wiki-ctx-ab/PROMPT_30_startup_wiki-ctx-ab-p2-v1.md`  
> 帽链：**30 → 40 → 50 → CLOSE**

```text
你正在扮演 Harness「执行帽（30）」（本 Epic：Wiki-CTX-AB **P2** · 纯文档实验 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（文档 Epic：无 api 代码）
- docs/harness/prompts/templates/TEMPLATE-execute-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc
- **禁止**改 docs/harness/prompts/ 帽子正文

【开帽】将本 user 消息全文落盘至：
docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_30_wiki-ctx-ab-p2-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_v1.md
- git_branch：task/wiki-ctx-ab-p2-v1
- freeze_id：WIKI-CTX-AB@2026-05-25
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md
- 实验真值：
  docs/harness/experiments/wiki_ctx_ab_v1/questions.md
  docs/harness/experiments/wiki_ctx_ab_v1/PROMPT_third_party_agent_wiki_ctx_ab_p2.md
- gold slug：harness-p1-docs-consolidation
- test_strategy：not_applicable

0b. 人工闸 HG-AB-SLUG、HG-AB-P1-DONE 须 approved。

你必须完成（P2 执行 · 按序）：

1. **物化 W 臂**（若 22 指出缺失或 char_count 空）：
   python tools/wiki_ctx_ab_materialize_w.py --slug harness-p1-docs-consolidation
   确认：docs/harness/experiments/wiki_ctx_ab_v1/payloads/W_harness-p1-docs-consolidation.md
   对照 payloads/TEMPLATE-W.md

2. **跑 P2 对照**（H-lean vs W · 同 questions.md Q1–Q4）：
   - 严格按 PROMPT_third_party_agent_wiki_ctx_ab_p2.md §0–§3
   - 每臂每题 **独立会话**（或独立 thread）
   - 载荷仅允许：
     · H-lean：payloads/H-lean_harness-p1-docs-consolidation.md（P1 已物化 · **勿改**）
     · W：payloads/W_harness-p1-docs-consolidation.md
   - **禁止**读盘载荷外文件

3. **填表**：docs/harness/experiments/wiki_ctx_ab_v1/scorecard.md **§P2**（8 行 + 汇总 + 逐题原文可选）

4. **结论文**：docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md
   - 须回答：W 相对 H-lean 是否再省 token（建议阈值 ≥30%）且正确性不降（SPEC §3.1）
   - 明确：是否推荐 Agent **默认先读** `docs/coding_wiki/index` + 相关 syntheses

5. 更新 task：§范围 P2 勾选；实现备忘（模型名、日期、payload_char_count）；**勿**关账（属 CLOSE）。

6. **Commit**（禁止 git add -A）：
   docs/harness/experiments/wiki_ctx_ab_v1/
   tools/wiki_ctx_ab_materialize_w.py
   docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_30_*.md
   docs/tasks/active/task_wiki_ctx_ab_v1.md

7. 对话末尾：📋 Harness 状态栏；**下一棒 = 40**（新对话 · PROMPT_40）。

禁止：改 api/、改 docs/harness/prompts/、重跑 P1 改 H-full/H-lean 源文件

关键词：30、P2、H-lean、W、scorecard、conclusion_p2、Wiki-CTX-AB
```
