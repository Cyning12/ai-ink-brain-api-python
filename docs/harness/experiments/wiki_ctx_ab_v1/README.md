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
| `payloads/H-full_harness-p1-docs-consolidation.md` | P1 物化实例（执行 AB 时生成） |
| `payloads/H-lean_harness-p1-docs-consolidation.md` | P1 物化实例 |
| `scorecard.md` | P1/P2 填表（执行时创建） |
| `conclusion_p1_zh.md` | P1 结论文（执行后） |
| `conclusion_p2_zh.md` | P2 结论文（Wiki 就绪后） |
| [`PROMPT_third_party_agent_wiki_ctx_ab_p1.md`](./PROMPT_third_party_agent_wiki_ctx_ab_p1.md) | **三方 Agent** 可复制 Prompt + 验收测试集 T1–T8 |

**P2 新增**：`payloads/TEMPLATE-W.md`、`payloads/W_<slug>.md`（T1b pilot 完成后）。

---

## 执行顺序

1. 按 `questions.md` 物化 H-full / H-lean（复制模板并替换 `{{...}}`）。  
2. 同一模型回答 3 题 × 2 臂 → 填 `scorecard.md` §P1。  
3. 写 `conclusion_p1_zh.md` → 再开 T1b / T2。
