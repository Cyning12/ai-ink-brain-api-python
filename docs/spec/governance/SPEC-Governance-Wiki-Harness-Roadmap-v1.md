# SPEC — 治理线：Harness 推广 · Coding Wiki · Wiki-CTX-AB（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **日期** | 2026-05-25 |
| **freeze_id** | `GOV-WIKI-HARNESS-ROADMAP@2026-05-25` |
| **排期同步** | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) §0、§1、§6.6 |
| **实验** | [`docs/harness/experiments/wiki_ctx_ab_v1/`](../../harness/experiments/wiki_ctx_ab_v1/README.md) |
| **任务** | [`task_coding_wiki_pilot_v1.md`](../../tasks/active/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../../tasks/active/task_wiki_ctx_ab_v1.md) |
| **工作区指导意见** | `Projects/docs/harness/guides/GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md` · `COMPARISON_tech_graph_coding_wiki_graph_memory_v1_zh.md` |

---

## 0. 规格层级（本仓）

```text
L0 架构/契约     docs/_tech_graph/ + graph.json + PROJECT_CONFIG
L1 过程真值      docs/tasks/ + docs/harness/（invokes/reviews by-task）
L2 编译层（试点） docs/coding_wiki/（Karpathy LLM Wiki 映射）
SDD 行为规格     docs/spec/v3-agent/（ChatBI 等）
治理规格（本文件） docs/spec/governance/（推广顺序、消费纪律、AB 闸口）
```

**原则**：SPEC 写 **应然与顺序**；invoke/review **不进 SPEC 正文**；疗效用 **Wiki-CTX-AB** 实验结论驱动推广，不靠假设。

---

## 1. 背景与目标

| 痛点 | 应对 |
| --- | --- |
| `invokes/`、`reviews/` 随 Epic 膨胀，Agent 扫历史 → **上下文爆炸** | L2 **Coding Wiki**（ingest 摘要 + index） |
| 工作区 `docs/harness/` 仍为扁平旧布局，后端已 **by-task** | **延后全仓推广**，待 AB 结论 |
| 需证明 taxonomy / Wiki **疗效** | **Wiki-CTX-AB** 两阶段实验 |

**目标**：在 **不改动 Harness 执行链 / CI** 前提下，确定 (1) 全项目 Harness taxonomy 是否推广；(2) 是否将 `coding_wiki/` 写入 Agent 默认读序。

---

## 2. 时间线（强制顺序）

| 阶段 | 代号 | 内容 | 状态（2026-05-25） |
| --- | --- | --- | --- |
| **T0** | Harness-taxonomy | 本仓 `docs/harness/`：`prompts/{hats,templates,handoff}`、`invokes/by-task/`、`reviews/by-task/` | **done** |
| **T1a** | Wiki-CTX-AB **P1** | H-full vs H-lean；**不依赖** `coding_wiki/` | **进行中**（`wiki_ctx_ab_v1/questions.md`） |
| **T1b** | Coding-Wiki-pilot | `docs/coding_wiki/` 骨架 + 与 P1 **同 slug** ingest | `draft`（`task_coding_wiki_pilot_v1`） |
| **T2** | Wiki-CTX-AB **P2** | H-lean vs **W**（仅 Wiki 载荷） | **blocked by T1b** 最小 ingest |
| **T3** | Harness 全仓推广 | 工作区 `docs/harness/` + 前端 parity（P1-4） | **等待 T1a + T2 结论** |
| **T4** | 图谱桥接（可选） | `::documents` / `::evidence`、Wiki `graph_nodes` frontmatter | `planned` |

```text
T0 ──► T1a（P1 AB）──┬──► T3（推广 Harness）
                     │
         T1b（pilot）─┴──► T2（P2 AB）──► T3 是否默认 coding_wiki
```

**并行**：T1a 与 T1b **可同时进行**（不同分支/工作树）；T2 **必须在** 同一 `task_slug` 的 Wiki 页存在后。

---

## 3. Wiki-CTX-AB 实验（摘要）

| 子阶段 | 对照臂 | 回答问题 |
| --- | --- | --- |
| **P1** | **H-full** vs **H-lean** | 仅 Harness taxonomy，是否已显著省 token 且答案仍对？ |
| **P2** | **H-lean** vs **W** | 在 H-lean 基线上，Coding Wiki 是否再省 token 且不降正确性？ |

- **Gold slug（锁定）**：`harness-p1-docs-consolidation`  
- **题集 / 模板**：[`wiki_ctx_ab_v1/questions.md`](../../harness/experiments/wiki_ctx_ab_v1/questions.md)  
- **任务单**：[`task_wiki_ctx_ab_v1.md`](../../tasks/active/task_wiki_ctx_ab_v1.md)

### 3.1 推广签收（草案）

| 结论条件 | 动作 |
| --- | --- |
| P1：H-lean 相对 H-full token 降且正确性可接受 | 执行 **T3** Harness 推广 |
| P2：W 相对 H-lean 再优 | T3 读序增加 **先 `coding_wiki/index`** |
| P2：W 无优势 | 仅 **关账后可选** ingest；不写默认读序 |
| P1 失败 | 先修 README/消费纪律，**不推广** by-task |

---

## 4. 任务与 SPEC 分工

| 工件 | 路径 | 角色 |
| --- | --- | --- |
| **本 SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` | 整体安排、阶段闸口 |
| **排期表** | `docs/tasks/RECENT_TASK_SCHEDULE.md` | 状态勾选、与 V3 队列并列 |
| **Wiki 试点 task** | `docs/tasks/active/task_coding_wiki_pilot_v1.md` | 交付 `coding_wiki/` |
| **AB task** | `docs/tasks/active/task_wiki_ctx_ab_v1.md` | scorecard + conclusion |
| **ChatBI SDD** | `docs/spec/v3-agent/*` | 业务行为；**不**替代治理线 |

---

## 5. 非范围

- 图即记忆 T/K/H 全栈、Neo4j（INK-P7）、改 `docs/harness/prompts/` 帽子正文。  
- 将 invoke/review 全文迁入 SPEC 或 `graph.json`。  
- 在 P2 结论前全仓 `git mv` 工作区 harness（可与 T1b 并行准备 pointer 草案，但不升为默认消费）。

---

## 6. 关联引用

| 用途 | 路径 |
| --- | --- |
| Harness taxonomy | [`docs/harness/README.md`](../../harness/README.md) §2.1 |
| 图谱消费 | `docs/_tech_graph/` · `AGENT_GRAPH_CONSUMPTION`（治理仓 methodology） |
| LLM Wiki 译文 | `ai_coding_governance/lib/llm-wiki_zh.md` |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：整体安排表；T0～T4；Wiki-CTX-AB P1/P2 闸口 |

---

## 给 Cursor

`SPEC-Governance`、`Wiki-CTX-AB`、`T1a`、`T1b`、`H-full`、`H-lean`、`coding_wiki`、`RECENT_TASK_SCHEDULE`
