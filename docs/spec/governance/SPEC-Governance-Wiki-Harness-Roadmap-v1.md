# SPEC — 治理线：Harness 推广 · Coding Wiki · Wiki-CTX-AB（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **日期** | 2026-05-25 |
| **freeze_id** | `GOV-WIKI-HARNESS-ROADMAP@2026-05-25` |
| **排期同步** | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) §0、§1、§6.6 |
| **实验** | [`docs/harness/experiments/wiki_ctx_ab_v1/`](../../harness/experiments/wiki_ctx_ab_v1/README.md) |
| **任务** | [`task_coding_wiki_pilot_v1.md`](../../tasks/done/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../../tasks/done/task_wiki_ctx_ab_v1.md) |
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
| 工作区 `docs/harness/` 曾为扁平旧布局 | **T3 已推广**（by-task + pointer/MIGRATION · 2026-05-26）；前端 **P1-4 parity** 仍远期 |
| 需证明 taxonomy / Wiki **疗效** | **Wiki-CTX-AB** 两阶段实验 |

**目标**：在 **不改动 Harness 执行链 / CI** 前提下，确定 (1) 全项目 Harness taxonomy 是否推广；(2) 是否将 `coding_wiki/` 写入 Agent 默认读序。

---

## 2. 时间线（强制顺序）

| 阶段 | 代号 | 内容 | 状态（2026-05-26） |
| --- | --- | --- | --- |
| **T0** | Harness-taxonomy | 本仓 `docs/harness/`：`prompts/{hats,templates,handoff}`、`invokes/by-task/`、`reviews/by-task/` | **done** |
| **T1a** | Wiki-CTX-AB **P1** | H-full vs H-lean；**不依赖** `coding_wiki/` | **done**（[`conclusion_p1_zh.md`](../../harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md) · 2026-05-25） |
| **T3** | Harness 工作区推广 | 工作区 `docs/harness/` taxonomy（pointer/MIGRATION · §2.1） | **done**（工作区 [`task_harness_workspace_taxonomy_promote_v1.md`](../../../../docs/harness/tasks/done/task_harness_workspace_taxonomy_promote_v1.md) · 2026-05-26；子仓 [pointer](../../tasks/done/task_harness_workspace_taxonomy_promote_v1.md)） |
| **T1b** | Coding-Wiki-pilot | `docs/coding_wiki/` 骨架 + 与 P1 **同 slug** ingest | **done**（2026-05-26 · [`task_coding_wiki_pilot_v1.md`](../../tasks/done/task_coding_wiki_pilot_v1.md)） |
| **T2** | Wiki-CTX-AB **P2** | H-lean vs **W**（仅 Wiki 载荷） | **done**（2026-05-26 · [`task_wiki_ctx_ab_v1.md`](../../tasks/done/task_wiki_ctx_ab_v1.md) · 推荐默认 `coding_wiki/` 读序） |
| **P1-4** | 前端 Harness parity | `ai-ink-brain` 模板/rsync/规则 | **远期**（≠ T3 工作区交付） |
| **T4** | 图谱桥接 | `::documents` / `::evidence`、Wiki `graph_nodes` | **draft** · [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) |
| **T1c** | Wiki 扩域（过程档案） | 测试迭代 `syntheses`/`decisions`/`concepts`；见 [`CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §8 | **done**（2026-05-26 · [`task_coding_wiki_t1c_test_archive_v1.md`](../../tasks/done/task_coding_wiki_t1c_test_archive_v1.md)） |
| **Multi slug** | Wiki-CTX-AB 多 slug | 2 slug · 部分外推；链 [`conclusion_multi_slug_zh.md`](../../harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md) | **done**（2026-05-26 · [`task_wiki_ctx_ab_multi_slug_v1.md`](../../tasks/done/task_wiki_ctx_ab_multi_slug_v1.md)） |
| **Wiki Loop** | A1–A4 ingest 纪律 | `test_strategy` synthesis + `CODING_WIKI` §8.1 + SPEC/排期同步；单 PR | **done**（2026-05-26 · [`task_harness_wiki_loop_a1_a4_v1.md`](../../tasks/done/task_harness_wiki_loop_a1_a4_v1.md)） |
| **Wiki Loop B-Q3** | B-Q3 Recheck | R1 载荷 §Recheck + R2 conclusion/#46 + R3 治理；单 PR | **done**（2026-05-26 · [`task_harness_wiki_loop_bq3_recheck_v1.md`](../../tasks/done/task_harness_wiki_loop_bq3_recheck_v1.md) · 第二 Loop 试点） |

```text
T0 ──► T1a（P1 AB）──► T3（工作区 Harness）✓
         │
         T1b（pilot）──► T2（P2 AB）✓ ──► 默认 coding_wiki 读序（2026-05-26 签收）
         │
         T1c（测试过程档案）✓ · Multi slug AB ✓
         Wiki Loop A1–A4（ingest test_strategy）✓
         Wiki Loop B-Q3 Recheck ✓
         T4（图谱桥接）· draft SPEC
         P1-4（前端 parity）· 远期
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
- **任务单**：[`task_wiki_ctx_ab_v1.md`](../../tasks/done/task_wiki_ctx_ab_v1.md)

### 3.1 推广签收（草案）

| 结论条件 | 动作 |
| --- | --- |
| P1：H-lean 相对 H-full token 降且正确性可接受 | **T3 已执行**（2026-05-26 工作区关账） |
| P2：W 相对 H-lean 再优 | **done**（2026-05-26）· 读序增加 **先 `docs/coding_wiki/index.md` + `syntheses/<slug>.md`**（[`conclusion_p2_zh.md`](../../harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md) accepted · W 降幅 78.8%、4/4 pass） |
| P2：W 无优势 | 仅 **关账后可选** ingest；不写默认读序 |
| P1 失败 | 先修 README/消费纪律，**不推广** by-task |

---

## 4. 任务与 SPEC 分工

| 工件 | 路径 | 角色 |
| --- | --- | --- |
| **本 SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` | 整体安排、阶段闸口 |
| **排期表** | `docs/tasks/RECENT_TASK_SCHEDULE.md` | 状态勾选、与 V3 队列并列 |
| **Wiki 试点 task** | `docs/tasks/done/task_coding_wiki_pilot_v1.md` | 交付 `coding_wiki/`（**done**） |
| **AB task** | `docs/tasks/done/task_wiki_ctx_ab_v1.md` | scorecard + conclusion（P1+P2 **done**） |
| **T4 专文** | [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) | Wiki↔图谱桥接（**draft**） |
| **L2 工具链专文** | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) | 锚点/测试 manifest（**draft**） |
| **ChatBI SDD** | `docs/spec/v3-agent/*` | 业务行为；**不**替代治理线 |

---

## 5. 非范围

- 图即记忆 T/K/H 全栈、Neo4j（INK-P7）、改 `docs/harness/prompts/` 帽子正文。  
- 将 invoke/review 全文迁入 SPEC 或 `graph.json`。  
- 在 P2 结论前将 **`coding_wiki/` 升为 Agent 默认读序**（T3 工作区 harness 已关账；T1b/T2 仍管 Wiki 疗效）。
- 用 Wiki 替代 pytest / `_test_manifest` 做 **coverage 真值或 CI 映射**（仅允许 **测试变更过程** 存档，见 `CODING_WIKI.md` §8）。

---

## 5.1 下一步优先级（2026-05-26 草案 · 试点关账后）

| 优先级 | 代号 | 内容 | 依赖 |
| --- | --- | --- | --- |
| **P0** | 试点关账 | Wiki-CTX-AB task 归档、`RECENT_TASK_SCHEDULE` / `_views` 同步；实践文 → `docs/diary/` | **done**（2026-05-26 · task 已在 `done/`；见 diary 与对比表） |
| **P1** | T1c 扩域 | 选 1～2 个 **测试相关 done task** ingest；可选 `concepts/test-strategy-ink-backend`；`decisions/` 首条 append | `CODING_WIKI` §8 |
| **P1** | 多 slug AB | 对 `tech-graph-gate-d-v2-tasks` 等再跑 **对照实验二**（精简 Harness 包 vs 仅 Wiki），削弱「单 Epic 外推」局限 | **done**（2026-05-26 · [`task_wiki_ctx_ab_multi_slug_v1`](../../tasks/done/task_wiki_ctx_ab_multi_slug_v1.md) · B-Q3 Recheck 后 slug B W 4/4） |
| **P1** | B-Q3 Recheck Loop | 重物化 W 载荷 + conclusion/#46 同步 | **done**（2026-05-26 · [`task_harness_wiki_loop_bq3_recheck_v1.md`](../../tasks/done/task_harness_wiki_loop_bq3_recheck_v1.md)） |
| **P2** | L2 工具链 | 锚点 + `_test_manifest` | **draft** · [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) |
| **P2** | T4 | Wiki `graph_nodes` ↔ L0 | **draft** · [`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](./SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) |
| **P3** | P1-4 | 前端 Harness parity | 远期 |

---

## 6. 关联引用

| 用途 | 路径 |
| --- | --- |
| Harness taxonomy | [`docs/harness/README.md`](../../harness/README.md) §2.1 |
| 图谱消费 | `docs/_tech_graph/` · `AGENT_GRAPH_CONSUMPTION`（治理仓 methodology） |
| LLM Wiki 译文 | `ai_coding_governance/lib/llm-wiki_zh.md` |
| 需求逐项对比 | [`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：整体安排表；T0～T4；Wiki-CTX-AB P1/P2 闸口 |
| 2026-05-26 | v1.2：T2 **done** · SPEC §3.1 P2 签收 · 推荐默认 `coding_wiki/` 读序 |
| 2026-05-26 | v1.3：T1c 扩域（测试过程档案）· §5.1 下一步优先级 · §5 非范围补 Wiki≠coverage |
| 2026-05-26 | v1.4：§4 pilot → done 路径 · §6 链出需求对比表 |
| 2026-05-26 | v1.6：§5.1 P1 多 slug AB **done** · 链至 `task_wiki_ctx_ab_multi_slug_v1` |
| 2026-05-26 | v1.7：§2 T1c/Multi slug **done** · Wiki Loop 行（A3 同步） |
| 2026-05-26 | v1.8：§2 Wiki Loop B-Q3 Recheck **done** · §5.1 B-Q3 行 · 链第二 harness-loop-batch Loop |
| 2026-05-27 | v1.9：T4 / L2 工具链 **draft 专文** · §2 §4 §5.1 链出 |

---

## 给 Cursor

`SPEC-Governance`、`Wiki-CTX-AB`、`T1a`、`T1b`、`H-full`、`H-lean`、`coding_wiki`、`RECENT_TASK_SCHEDULE`
