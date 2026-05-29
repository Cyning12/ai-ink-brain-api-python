# Wiki 治理线 · 阶段性验收（2026-05-29）

> **性质**：里程碑签字稿 · diary 留证 · **非** L0/L1 真值  
> **freeze 锚点**：`GOV-WIKI-T4-OPS@2026-05-29` · PR [#83](https://github.com/Cyning12/ai-ink-brain-api-python/pull/83)（已合 `main`）  
> **实验真值**：`docs/harness/experiments/wiki_ctx_ab_v1/` · `wiki_ctx_ab_multi_slug_v1/` · `wiki_ctx_ab_representative_v1/`

---

## 1. 验收结论（草案）

| 项 | 结果 | 说明 |
| --- | --- | --- |
| 机器门禁（§3 VERIFY） | **pass** | 本机 `main` 六条命令全绿（见 §3 留证） |
| AB 证据链 | **pass** | P1 → P2 → Multi → Representative 均已 accepted |
| 工程化交付 | **pass** | syntheses **25/25** · `coding_wiki_graph_nodes_lint` · L2 manifest Phase C CI |
| Wiki 治理线阶段收口 | **pass** | 可切业务线；后续 ingest 按 `CODING_WIKI.md` §4 关账纪律 |

**验收人签字**：已批准 · 日期：2026-05-29

---

## 2. 对外一句话

在后端 Ink-Brain 仓，三轮对照实验表明：关账回顾场景下 **Coding Wiki（L2）** 相对精简 Harness 包可再省约 **60%–79%** 物化字符，且多数 gold 题 **4/4**；随后以 **25 篇 synthesis + graph_nodes lint + L2 manifest CI** 将试点固化为可运维基建，**不替代** L0 技术图谱。

**限定语**：字符数为载荷代理指标，非 API token 账单；场景为关账回顾，非线上 RAG 准确率。

---

## 3. 机器门禁留证（本机 · main · 2026-05-29）

执行环境：`ai-ink-brain-api-python` · 分支 `main` · Python 3.11.15

```bash
python tools/coding_wiki_graph_nodes_lint.py
pytest tests/test_coding_wiki_graph_nodes_lint.py -q
pytest tests -m "not intent_eval and not intent_benchmark" -q
python tools/tech_graph_graph_export.py --check
python tools/tech_graph_manifest_check.py
python tools/tech_graph_test_manifest_check.py --check-failure-paths
```

### 3.1 输出要点

| # | 命令 | 结果 |
| --- | --- | --- |
| 1 | `coding_wiki_graph_nodes_lint.py` | `coding_wiki_graph_nodes_lint: OK` |
| 2 | lint pytest | **7 passed** in 0.03s |
| 3 | 全仓 pytest | **249 passed**, 1 skipped, 2 deselected（82.18s） |
| 4 | `graph_export --check` | OK |
| 5 | `manifest_check` | OK: manifest matches code/SQL truth |
| 6 | `test_manifest_check --check-failure-paths` | OK: 12 entries, failure-paths |

**跳过项（已知）**：`tests/test_tech_graph_graph_v2_equivalence.py:154` — 已升 graph_v2，改测 v2 路径。

**warnings**：Supabase client `timeout`/`verify` DeprecationWarning（55 条，非本里程碑阻塞）。

### 3.2 终端原文摘要

```
coding_wiki_graph_nodes_lint: OK
7 passed in 0.03s
249 passed, 1 skipped, 2 deselected, 55 warnings in 82.18s
OK: manifest matches code/SQL truth (endpoints/rpc/tables/env + anchors resolvable).
OK: test manifest valid (12 entries, test_paths globs resolved) [failure-paths].
```

---

## 4. AB 测试 · 成果对比（引用仓内 accepted 结论）

### 4.1 实验阶梯

| 阶段 | 对照 | 降幅（字符） | 正确性 | 证据 |
| --- | --- | --- | --- | --- |
| **P1** | H-full → H-lean | **37.9%**（15928→9896） | 4/4 = 4/4 | `wiki_ctx_ab_v1/conclusion_p1_zh.md` |
| **P2** | H-lean → W | **78.8%**（9896→2096） | 4/4 = 4/4 | `wiki_ctx_ab_v1/conclusion_p2_zh.md` |
| **Multi · 图谱** | H-lean → W | **86.3%**（21666→2978） | 4/4 | `wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md` |
| **Multi · RAG** | H-lean → W | **61.4%**（8796→3395） | 4/4（B-Q3 Recheck 后） | 同上 §5 |
| **Representative** | 6 slug | **60.8%–77.3%** | **5/6** 域 W **4/4** | `wiki_ctx_ab_representative_v1/conclusion_representative_zh.md` |

### 4.2 Representative 六域摘要

| slug | 域 | W 降幅 | W 正确性 |
| --- | --- | --- | --- |
| harness-p1-docs-consolidation | Harness P1 | 64.7% | 4/4 |
| tech-graph-gate-d-v2-tasks | 图谱闸口 D | 77.3% | 4/4 |
| chatbi-v3-p2-health-ready | ChatBI 探针 | 61.2% | 4/4 |
| governance-l2-manifest-ci | L2 manifest | 60.8% | 4/4 |
| wiki-ctx-ab-v1 | Wiki 元实验 | 73.6% | 4/4 |
| harness-wiki-loop-t4-l2 | Loop 母单 | 65.4% | 3/4（母单 `test_strategy` 未 ingest） |

### 4.3 工程交付对比

| 维度 | 试点前（~2026-05-25） | 里程碑后（2026-05-29） |
| --- | --- | --- |
| syntheses | 1（Pilot） | **25** |
| `graph_nodes` 键 | 零星 | **25/25** |
| Wiki↔图谱 | SPEC draft | Bridge SPEC active · §5.1 全勾 |
| 自动化 | 手工 graph_query | `coding_wiki_graph_nodes_lint.py` + pytest |
| L2 manifest | 草案 6 条 | **12** 条 + Phase C CI Required（#80/#81） |
| Agent 读序 | 无 | AGENTS 必读第 5 条 |
| 前端 parity | 无 | Ink PR #44 done |
| 治理 PR 链 | — | #79–#83（Unit A/B + T4 ops） |

---

## 5. 文档 / Harness 勾选

- [x] `docs/tasks/done/task_governance_wiki_t4_ops_v1.md` 已归档
- [x] `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-ops_20260529_v1.md`
- [x] `RECENT_TASK_SCHEDULE.md` §6.6 T4 ops **done**
- [x] P1/P2/Multi/Representative conclusion **accepted** 在仓内可链
- [ ] `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` v1.6（T4 ops 行，可选 hygiene）

---

## 6. 任务排期读序 smoke（2026-05-29 · accepted）

> **实验轨**：`docs/harness/experiments/task_schedule_read_smoke_v1/` · **非** L0 真值  
> **freeze_id**：`TASK-SCHEDULE-READ-SMOKE@2026-05-29` · 关联 `GOV-TASK-SCHEDULE-WIKI@2026-05-29`

| 项 | 结果 |
| --- | --- |
| Agent 平台 | Claude Code |
| model | Kimi-code |
| Prompt | 无路径引导 §3（未写 RECENT/concept 路径） |
| Q1 当前棒 | **pass** · P2-1b 限流 |
| Q2 P2 先后 | **pass** · 限流 → 熔断 |
| Q3 L1 vs L2 | **pass** · RECENT 真值 · Wiki 叙事 |
| Q4 陷阱 | **pass** · Wiki/T4 **非**当前棒 |
| **汇总** | **4/4 pass** · smoke **通过** |

**观测**：本 run 经 **RECENT / AGENTS / 母单** 可达真值；concept hub 为增强导航，**非唯一入口**。  
**证据**：[`scorecard.md`](../harness/experiments/task_schedule_read_smoke_v1/scorecard.md) · [`conclusion_smoke_zh.md`](../harness/experiments/task_schedule_read_smoke_v1/conclusion_smoke_zh.md)

---

## 7. 边界与后续（非本验收阻塞）

| 可外推 | 不可外推 |
| --- | --- |
| 关账回顾、已 ingest Epic 的跨会话理解 | 未 ingest 的运行时细节、生产配置 |
| 六域载荷降幅 >60%、5/6 四题全中 | 前端 Next/BFF（须 Ink 仓） |
| 默认读序：index → synthesis → L0 | ChatBI 实现级排障、RAG 线上指标 |

**业务线同步 Wiki**：无自动同步；**done task 关账后 ingest**（`CODING_WIKI.md` §4.1）· 批量可开 Batch-N · 可选 P3 lint 升 CI。

**可选后续（不挡业务开工）**：Batch-4 ingest · P3 lint CI Required · Roadmap/RECENT hygiene 小 PR。

---

## 8. 公众稿蒸馏 · 系列落点与扩充清单（草案）

> **用途**：指导《AI 编程可闭环协作》公众连载如何从本里程碑取材；**不**直接复制进公众稿。  
> **Skill**：私仓 `public-narrative-zh` · 公众仓 OUTLINE 卷四 §14–15 已链本文件。

### 8.1 系列落点（推荐）

| 优先级 | 卷 · 节 | 用法 |
| --- | --- | --- |
| **主** | **卷四 §15** 闭环后：经验卡片与团队 Skill | AB 数字、Representative 六域、与卷一结语「经验卡片 / Skill」呼应 |
| **辅** | **卷四 §14** 从 SPEC 到归档 | 关账 → 可选 ingest；不写 AB 降幅 |
| **轻** | **卷三 §12/§13 末** | 阶段流关账后多一步「可选编译摘要」，指针卷四 |
| **案例** | **卷五 §17–19** | 匿名试点一周；FAQ「Harness 会不会越积越厚」 |
| **勿主放** | 卷二 §8.5 | 该节「Wiki」= **产品/需求 Wiki**；关账编译摘要见卷四，避免混称 |

**写作顺序**：卷三关账指针 → 卷四 §14 → 卷四 §15（主文）→ 卷五 FAQ（可选复述数字）。

### 8.2 公众稿扩充清单（定稿前必勾）

- [ ] **术语**：按 `public-narrative-zh`；正文不用 L0/L1/L2、freeze_id、slug 作主语；表头注明「笔者项目示例（不唯一）」
- [ ] **通俗名对照**：技术图谱（地图轨）· 协作过程留痕（Harness 轨）· **关账编译摘要**（Coding Wiki 轨，卷四展开）
- [ ] **数字边界**：每条指标附 **题集规模 + 单后端仓 + 关账回顾**；写明 **字符降幅 ≠ API token 账单**
- [ ] **失败样本**：`harness-wiki-loop-t4-l2` **3/4** 须进正文（母单 `test_strategy` 未 ingest）作诚实边界范本
- [ ] **脱敏**：公众稿不写 PR #、freeze 锚点、仓内路径；pytest 条数改「合并前机器验收全绿」或脚注「对内另备验收单」
- [ ] **与卷二划界**：三列小表——**产品 Wiki** / **技术图谱** / **关账编译摘要**（勿与卷二 §8.5 产品 Wiki 混为一谈）
- [ ] **OUTLINE**：公众仓 `ARTICLE_*_OUTLINE` 卷四 §14–15 标注素材来源（本文件）
- [ ] **核心句保留**：Wiki **不替代** 技术图谱；图谱答「改哪里」，编译摘要答「关账后少翻 invoke 全文」

### 8.3 三轨分工表（公众稿可用草稿）

| 通俗名 | 回答什么 | 与本篇里程碑关系 |
| --- | --- | --- |
| **技术图谱** | 改哪里、会影响谁 | L0 · 卷二已讲 · **不被 Wiki 替代** |
| **协作过程留痕** | 谁来做、任务/审查/invoke | L1 · 会持续增长 · 不宜默认全量灌 Agent |
| **关账编译摘要** | 跨任务概念与决策（synthesis） | L2 · 本篇里程碑主题 · 关账后 ingest |
| **产品 Wiki / PRD** | 产品语义 | 与上表不同域 · 卷二 §8.5 已述 |

### 8.4 蒸馏状态

| 项 | 状态 |
| --- | --- |
| 对内里程碑（§1–6） | 草案 · 待验收人签字 |
| 公众稿扩充清单（§8.2） | 已落盘 · 待卷四起草时逐项勾选 |
| 公众仓 OUTLINE 链 | 见同级 PR `ai-coding-closed-loop-articles` |

---

## 9. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-29 | 初稿：VERIFY 本机留证 + AB 数字表 + 阶段收口建议 |
| 2026-05-29 | §7：公众稿系列落点 + 扩充清单 + 三轨分工表 |
| 2026-05-29 | §6：task schedule read smoke · Claude Code · Kimi-code · 4/4 accepted |
| 2026-05-29 | §1：Wiki 治理线阶段收口 **pass** · 里程碑验收批准 |
