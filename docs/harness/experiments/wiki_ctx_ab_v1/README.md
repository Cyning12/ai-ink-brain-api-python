# Wiki-CTX-AB v1 — 上下文消费对照实验

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **SPEC** | [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) |
| **task** | [`docs/tasks/active/task_wiki_ctx_ab_v1.md`](../../tasks/active/task_wiki_ctx_ab_v1.md) |

---

## 目录

| 文件 | 用途 |
| --- | --- |
| [`questions.md`](./questions.md) | Gold 题 + 标准答案要点（P1 锁定 slug） |
| [`payloads/TEMPLATE-H-full.md`](./payloads/TEMPLATE-H-full.md) | P1 对照臂：扫 by-task 全文 |
| [`payloads/TEMPLATE-H-lean.md`](./payloads/TEMPLATE-H-lean.md) | P1 基线臂：纪律消费 |
| `payloads/H-full_harness-p1-docs-consolidation.md` | P1 物化实例（**已生成** · 4 invoke + done 全文） |
| `payloads/H-lean_harness-p1-docs-consolidation.md` | P1 物化实例（**已生成** · README 摘录 + done 至验收节） |
| `scorecard.md` | P1/P2 填表（执行时创建） |
| `conclusion_p1_zh.md` | P1 结论文（执行后） |
| `conclusion_p2_zh.md` | P2 结论文（执行后） |
| [`PROMPT_third_party_agent_wiki_ctx_ab_p1.md`](./PROMPT_third_party_agent_wiki_ctx_ab_p1.md) | P1 三方 Agent Prompt |
| [`PROMPT_third_party_agent_wiki_ctx_ab_p2.md`](./PROMPT_third_party_agent_wiki_ctx_ab_p2.md) | **P2** 三方 Agent Prompt（H-lean vs W） |

**P2 工件**：[`payloads/TEMPLATE-W.md`](./payloads/TEMPLATE-W.md) · `payloads/W_harness-p1-docs-consolidation.md` · [`tools/wiki_ctx_ab_materialize_w.py`](../../../tools/wiki_ctx_ab_materialize_w.py)

**P2 帽链启动**（各帽新对话）：[`docs/harness/invokes/by-task/wiki-ctx-ab/`](../invokes/by-task/wiki-ctx-ab/) · 从 **22** 起。

---

## 执行顺序

### P1（done）

1. 物化 H-full / H-lean → 填 `scorecard.md` §P1 → `conclusion_p1_zh.md`。

### P2（当前）

1. **22** 审 P2 就绪（T1b Wiki 同 slug · W 载荷）。  
2. **30** 按 `questions.md` 跑 **H-lean vs W**（4 题 × 2 臂）→ §P2 + `conclusion_p2_zh.md`。  
3. **40 → 50 → 关账**（见 task 帽子顺序表）。
