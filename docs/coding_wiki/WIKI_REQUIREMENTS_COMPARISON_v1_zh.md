# Coding Wiki / LLM Wiki — 需求逐项对比 v1

| 项 | 内容 |
| --- | --- |
| **版本** | v1.0 |
| **日期** | 2026-05-26 |
| **状态** | `active` — 随试点/T1c 演进时增量修订 |
| **用途** | Karpathy 理论、治理 SPEC、本仓 Schema、实验结论、对话共识的 **逐项对照** |
| **关联** | [`CODING_WIKI.md`](CODING_WIKI.md) · [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) · [`wiki_ctx_ab_v1/`](../harness/experiments/wiki_ctx_ab_v1/README.md) |

**术语**：本文件中的 **编译层 L2** = `docs/coding_wiki/`；**工具链 L2** = 图谱测评报告（`11_REVIEW_L3_L2理论层缺口分析`）中的 CI / manifest，二者勿混。

**对照实验用语**（全文统一，避免项目内缩写）：

| 用语 | 含义 |
| --- | --- |
| **对照实验一（阶段 P1）** | **臂 A** = 完整 Harness 材料包 · **臂 B** = 精简 Harness 材料包（by-task 纪律 + done task 摘要） |
| **对照实验二（阶段 P2）** | **臂 B** = 精简包（基线）· **臂 C** = 仅 Coding Wiki（`index` + 单条 `synthesis`） |

---

## 0. 四条需求线（权威来源）

| 线 | 权威文档 | 本阶段目标 |
| --- | --- | --- |
| **A** | 治理仓 `ai_coding_governance/lib/llm-wiki.md`（及 `llm-wiki_zh.md`） | 通用 LLM Wiki 模式 |
| **B** | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` | 治理顺序、AB 闸口、推广 |
| **C** | `docs/coding_wiki/CODING_WIKI.md` + 磁盘树 | 本仓 Schema 与交付物 |
| **D** | 试点结论文 + `11_REVIEW_L3_L2…` + Schema §8 | 测试过程存档、图谱工具链分工 |

**图例**：✅ 已满足 · ⚠️ 部分 / 靠纪律 · ❌ 未做或刻意不做 · ⏸ 远期

---

## 1. 架构与动机

| # | 需求项 | 来源 | 应然 | 现状 | 差距 / 下一步 |
| --- | --- | --- | --- | --- | --- |
| 1 | 解决「每问重扫原文、无复利」 | A | 持久 Wiki，跨源综合 | 编译层 L2 + 关账 ingest | ✅；范围限于 **Harness 回顾** |
| 2 | 首要痛点是 Harness 历史爆炸 | B §1 | ingest 摘要 + index | T1b done | ✅ |
| 3 | 不改 Harness 执行链 / CI | B | 只增 `coding_wiki/` | 未改 prompts/CI | ✅ |
| 4 | Wiki 非架构第二真值 | B、C §1 | 冲突以 L0/L1 为准 | §1、§7 明文 | ✅ |
| 5 | 三层：Raw / Wiki / Schema | A | 三层分离 | L1=原文、L2=Wiki、Schema=`CODING_WIKI` | ⚠️ **有意裁剪**；见 §4 |
| 6 | 与图谱分工：拓扑 vs 叙事 | C、D | 表/RPC/依赖走 L0 | `llm-wiki-layers` | ✅ |
| 7 | 测试「过程存档」非 coverage 真值 | D、C §8 | Wiki 记变更史/意图 | §8 + `decisions/` + 2× synthesis §测试变更 | ✅ **T1c done** |
| 8 | 测试↔`ERR_*` 机器校验 | D | `_test_manifest` 等 | 未建 | ❌ **工具链 L2**；SPEC §5.1 P2 |

---

## 2. 目录与内容类型

| # | 需求项 | 来源 | 应然 | 现状（磁盘） | 差距 / 下一步 |
| --- | --- | --- | --- | --- | --- |
| 9 | `index.md` 分类目录 | A、C | 每 ingest 更新 | 有；1 concept + 3 syntheses | ✅ 结构有；体量小 |
| 10 | `log.md` 时间线 | A、C | append-only | 有 | ✅ |
| 11 | `syntheses/` 关账蒸馏 | B T1b、C | done task 一页 | **3 页** | ✅；待扩 slug |
| 12 | `concepts/` 跨 task 概念 | A、C | 多页织网 | **1 页** | ⚠️ T1c 可增 `test-strategy-*` |
| 13 | `entities/` 实体页 | A、C 可选 | 产品/模块等 | **未建目录** | ❌ 可选；模块/表优先 L0 |
| 14 | `sources/` 源 stub | C §9 | L1 过大时 | **未建** | ⏸ 按需 |
| 15 | `decisions/` 决策 append | C §8、D | 删测/暂不测等 | `2026-05-26-unit-first-test-archive.md` | ✅ **T1c done** |
| 16 | 每源 touch 10～15 页 | A | 密集互链 | 1 task → 1 synthesis | ❌ **工程裁剪，不采纳** |
| 17 | Query 结果写回 Wiki | A | 好答案沉淀 | 大改走 task 再 ingest | ⚠️ 弱化为关账 ingest |

---

## 3. 三操作（Ingest / Query / Lint）

| # | 需求项 | 来源 | 应然 | 现状 | 差距 / 下一步 |
| --- | --- | --- | --- | --- | --- |
| 18 | Ingest 仅 done | C §4.1 | 进行中只写 log | 3 syntheses 符合 | ✅ |
| 19 | 禁止复制 review/SPEC 全文 | C | pointer + 摘要 | 试点页均短摘要 | ✅ |
| 20 | Query：先 index 再 1～3 页 | C、P2 签收 | 默认读序 | 先 index + synthesis | ✅ |
| 21 | 影响面用 graph_query | C §4.2 | 不以 Wiki 替代 L0 | 明文 | ✅ 纪律 |
| 22 | 不够再开 L1 | D、C §7 | Wiki 优先、按需 L1 | §7 读序 | ✅ 日常；实验二臂 C 曾禁止回 L1 |
| 23 | Lint：孤儿/404/矛盾 | C §4.3 | 检查项已列 | **无** 自动化脚本 | ⚠️ 可选工具 |
| 24 | Lint：矛盾/过时/缺页 | A | 周期 health-check | 未制度化 | ❌ T1c 或周期任务 |
| 25 | 可选 CLI 搜索（qmd 等） | A | 规模大时用 | 未做 | ⏸ |

---

## 4. Raw 与 L1

| # | 需求项 | 来源 | 应然 | 现状 | 差距 / 下一步 |
| --- | --- | --- | --- | --- | --- |
| 26 | Raw 不可变原文库 | A | LLM 只读不改 | **L1** task/spec/review | ✅ 映射不同、等价 |
| 27 | 原文过大再处理 | C §9、D | pointer→synthesis→L1→sources | §9 四级 | ✅ 已规范 |
| 28 | 外部剪报库 | A、demo | 独立 source/ | 非本仓试点 | ⏸ |

---

## 5. 治理时间线与实验（SPEC）

| # | 需求项 | 代号 | 应然 | 现状 | 差距 / 下一步 |
| --- | --- | --- | --- | --- | --- |
| 29 | Harness 目录 taxonomy | T0 | by-task | **done** | ✅ |
| 30 | 对照实验一 | T1a | ≥30% 降、4/4 | **-37.9%**，4/4 | ✅ |
| 31 | 工作区 Harness 推广 | T3 | 与 P1 联动 | **done** 2026-05-26 | ✅ |
| 32 | Coding Wiki 骨架 | T1b | 同 slug ingest | **done**，3 syntheses | ✅ |
| 33 | 对照实验二 | T2 | 再优且不降 | **-78.8%**（相对臂 B），4/4 | ✅；**单 slug** |
| 34 | 默认 Agent 读序 | P2 签收 | 关账先 Wiki | conclusion_p2 | ✅ |
| 35 | 测试过程扩域 | **T1c** | CODING_WIKI §8 | **done** 2026-05-26 | ✅ `task_coding_wiki_t1c_test_archive_v1` |
| 36 | Wiki↔图谱 frontmatter | T4 | graph_nodes | planned | ❌ P2 |
| 37 | 前端 Harness parity | P1-4 | 前端仓 | 远期 | ⏸ |
| 38 | 多 slug 对照实验二 | SPEC §5.1 P1 | 削弱外推局限 | **done** · Multi slug AB 2026-05-26 | ✅ `task_wiki_ctx_ab_multi_slug_v1` |
| 39 | 试点关账 P0 | SPEC §5.1 | 归档、排期、diary | task 在 `done/`；`_views`；diary 已发布 | ✅ 2026-05-26 |
| 40 | SPEC §4 pilot 路径 | SPEC §4 | 与 done 一致 | 已改 `done/task_coding_wiki_pilot_v1` | ✅ |

---

## 6. 实验结论 vs 日常需求

| # | 需求/主张 | 实验是否证明 | 日常应然 |
| --- | --- | --- | --- |
| 41 | 仅 Wiki 可答关账四题 | ✅（文档 Epic、实验二臂 C） | 关账回顾可先用编译层 L2 |
| 42 | 可外推 ChatBI / 图谱闸口 | ❌ | 实现类 L0+L1；另跑 AB |
| 43 | 不需排期全文 | ⚠️ 依赖 synthesis 蒸馏 | 漏写 → 回 L1 |
| 44 | 不需 invoke/review 全文 | ✅（实验二） | 日常可按 by-task 片段 |
| 45 | Wiki 完整性可消「边界靠摘要」局限 | 部分 | ingest 纪律 + 回 L1 |
| 46 | 多 slug + L1/L0 兜底「单 Epic 外推」局限 | **部分** | T1c + Multi slug AB **done** · slug B W 3/4（test_strategy 缺口） |

---

## 7. SPEC §5.1 与 task 工件

| SPEC §5.1 项 | active task？ | done / 实验 | 建议 |
| --- | --- | --- | --- |
| P0 试点关账 | 无（收口，不新建） | `task_wiki_ctx_ab_v1` 等 **done** | ✅ 2026-05-26；**T1c 起需 active task** |
| P1 T1c | **无** | **done** · `done/task_coding_wiki_t1c_test_archive_v1.md` | ✅ 2026-05-26 关账 |
| P1 多 slug AB | **无** | **done** · `done/task_wiki_ctx_ab_multi_slug_v1.md` · 2026-05-26 | ✅ 部分外推 |
| P2 锚点/test manifest | **无** | 11_REVIEW | 独立 engineering task |
| P2 T4 | **无** | planned | 未来 task |
| P3 前端 parity | 前端仓 | 远期 | 不在本仓 |

---

## 8. 能力：项目理解 / 回溯

| # | 能力 | 完整包时代 | 精简包（实验一） | 仅 Wiki（实验二） | 未来 T1c+ |
| --- | --- | --- | --- | --- | --- |
| 47 | 接续 Epic | 扫大量 invoke/review | 按 task 目录 | 1 页 synthesis | + 测试变更史 |
| 48 | 范围/非范围 | 长 done task | 略短 | synthesis 边界 | ingest 必填 |
| 49 | freeze/关账日 | task 头 | 同左 | frontmatter | ✅ |
| 50 | 改 API / 依赖 | 易误扫 Harness | 仍可能 | 须走 L0 | T4 |
| 51 | 测试为何这样测 | 散落 L1 | 同左 | 未覆盖 | §8 + decisions |
| 52 | 跨 Epic why | 多份 L1 | 同左 | 弱 wikilink | concepts/decisions |

---

## 9. 汇总

| 状态 | 约计 | 含义 |
| --- | --- | --- |
| ✅ | ~20 项 | 试点核心、AB 签收、Schema、读序 |
| ⚠️ | ~10 项 | 概念网、lint 自动化、文档漂移 |
| ❌ | ~8 项 | entities 网、T1c 交付、多 slug AB、manifest |
| ⏸ | ~4 项 | sources、qmd、P1-4、外部 Raw |

```text
应然（SPEC / CODING_WIKI）→ 已验收（done task + conclusion）→ 未开工（§5.1，无 active task）
```

**建议顺序**：~~P0 关账~~（**done** 2026-05-26）→ **新建 T1c active task**（§5.1 P1）→ 工具链 L2 与 T1c **并行**、不混单。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1.0：自对话与试点文档蒸馏的 52 项对比表 |
| 2026-05-26 | v1.1：P0 关账勾选；§7 task 分工；建议顺序更新 |
