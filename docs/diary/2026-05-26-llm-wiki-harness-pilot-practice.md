# Harness 下的 LLM Wiki 初探：用「编译层」减轻历史回溯，并用两轮对照实验验证

| 项 | 内容 |
| --- | --- |
| **状态** | `published` · P0 关账后自 `docs/diary/tmp/` 迁入；真值以 SPEC / 实验 conclusion 为准 |
| **日期** | 2026-05-26 |
| **仓库** | `ai-ink-brain-api-python`（Ink 后端） |
| **关联真值** | `docs/coding_wiki/CODING_WIKI.md` · `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` · `docs/harness/experiments/wiki_ctx_ab_v1/` |

---

## 摘要

Ink 后端在 **Harness 工程**（多角色帽子、invoke/review 落盘、关账链）跑顺之后，遇到的新痛点不是「没有文档」，而是 **历史过程文档太多**：Agent 每次理解项目、回溯某次 Epic，都要扫大量 `invokes/`、`reviews/` 和长 done task，上下文迅速膨胀。

我们引入 **Karpathy 提出的 LLM Wiki 思路的工程化裁剪版**——本仓 `docs/coding_wiki/`（编译层 L2）：关账后把任务蒸馏成短页 + 索引，让 Agent **先读 Wiki，再按需回 L1 真值**。并用 **两轮 A/B 对照实验** 量化「省了多少上下文、题还能不能答对」。

结论概要：

1. **仅整理 Harness 目录结构**（对照实验一 · 精简包 vs 完整包）即可在固定四题上减少约 **38%** 字符且 **4/4** 正确。
2. **在精简包之上再只读 Coding Wiki**（对照实验二）可再减约 **79%** 字符（相对精简包），仍 **4/4** 正确。
3. Wiki **不是**架构第二真值；改代码、查依赖仍以技术图谱（L0）和 task/SPEC（L1）为准。
4. 下一步扩域方向包括 **测试迭代过程存档**（不是替 pytest 算覆盖率），以及更多 slug 上的复验。

---

## 1. 背景：Harness 解决了「过程」，没解决「回顾」

Harness 把需求→实现→审计→关账变成可复现的落盘链（`docs/harness/invokes/by-task/`、`reviews/by-task/` 等）。Epic 越多，**回顾成本**越高：

- 「这次 Epic 范围边界在哪？」
- 「和排期里上一项有什么关系？」
- 「关账时 freeze_id、测试策略是什么？」

若每次都把 invoke、review、done task **全文**塞进 Agent 上下文，相当于 **每问一次都重新发现一遍知识**——这正是 Karpathy 批评的「只有 RAG、没有复利」模式。

LLM Wiki 的核心替代方案是：**把知识编译一次，并保持更新**——在本仓里，编译产物就是 `coding_wiki/`。

---

## 2. 本仓三层：图谱、过程真值、编译 Wiki

避免与「图谱测评报告里的 L2 工具链」混淆，本仓约定：

| 层 | 是什么 | 典型路径 |
| --- | --- | --- |
| **L0** | 架构与契约真值 | `docs/_tech_graph/`、`graph_query`、`_contract_manifest` |
| **L1** | 单次交付与 Harness 过程真值 | `docs/tasks/`、`docs/harness/`、`docs/spec/` |
| **L2** | **Coding Wiki**（编译叙事） | `docs/coding_wiki/`：`index.md`、`syntheses/`、`concepts/` |

Wiki 的职责：**跨 task 的理解、回溯、why**；**不**替代 L0 做影响分析，**不**复制 Harness 帽子全文。

---

## 3. 试点做了什么（与「完整 LLM Wiki」的差别）

理论上的 LLM Wiki 往往包含：Raw 原文库、大量实体/概念页、每次 ingest 改十几页、Query 结果写回 Wiki。

本仓 **试点 v1** 刻意收窄：

| 理论能力 | 本仓试点 |
| --- | --- |
| 独立 Raw 库 | **L1 即原文**；过大时 `sources/` stub，不默认复制全文 |
| 实体/概念网 | 仅 1 个概念页 + 3 条关账 synthesis；模块/表靠 L0 |
| 每源多页维护 | **每个 done task 一页 synthesis** + 更新 index/log |
| 验证方式 | 固定 gold 四题 + 两轮 A/B |

**首要目标**：减少 **扫 Harness 历史** 的 token，提升 **项目理解与会话回溯** 效率，而不是先做个人知识库式的织网。

---

## 4. 两轮 A/B 对照实验（用语说明）

实验固定同一 Epic slug：`harness-p1-docs-consolidation`（Harness P1 文档巩固），四道 gold 题（交付项、测试策略、freeze_id、排期边界等）。详见 `wiki_ctx_ab_v1/scorecard.md`。

### 4.1 对照实验一（阶段 P1）：完整 Harness 包 vs 精简 Harness 包

| 臂 | 含义 | 载荷约量（四题合计） | 正确性 |
| --- | --- | --- | --- |
| **臂 A · 完整包** | 按旧习惯组装的 **较全** Harness 相关材料（含较多历史落盘） | 约 15 928 字符 | 4/4 |
| **臂 B · 精简包** | **按目录纪律消费**：`by-task` 指针、done task **截断/摘要版**，不塞无关长文 | 约 9 896 字符 | 4/4 |

**降幅**：约 **37.9%**（≥30% 阈值）· **正确性不降**。

**说明改进从哪来**：

- 不是删真值，而是 **消费纪律**：invoke/review 按 task 目录找，不全仓 grep 扁平历史。
- 与 **T3 · 全仓 Harness taxonomy 推广**（工作区 + 本仓 `by-task`）同源；实验为推广提供了数据依据。

**局限**：仍要读较长 done task；且只在 **一个文档类 Epic** 上验过。

### 4.2 对照实验二（阶段 P2）：精简 Harness 包 vs 仅 Coding Wiki

| 臂 | 含义 | 载荷约量 | 正确性 |
| --- | --- | --- | --- |
| **臂 B · 精简包**（基线） | 同实验一 | 约 9 896 字符 | 4/4 |
| **臂 C · 仅 Wiki** | 只给 `coding_wiki/index` + 对应 `syntheses/<slug>.md`；**实验纪律下**不为答题回读 done task 全文 | 约 2 096 字符 | 4/4 |

**相对精简包降幅**：约 **78.8%** · **正确性仍 4/4**。

**签收动作**：关账类任务 Agent **默认先读** `docs/coding_wiki/index.md`，再按 slug 打开 synthesis；实现类问题仍 **L0 + L1**。

**局限**：

- 仍单 slug；不能外推 ChatBI、图谱闸口等题型。
- 有一题依赖 synthesis 里已蒸馏的「排期边界 / 另 task」表述，**未**在 Wiki 载荷里放 `RECENT_TASK_SCHEDULE` 全文——日常应 **Wiki 优先、按需回 L1**，而非永远禁止读 L1。

### 4.3 两轮实验合在一起说明了什么

```text
完整 Harness 包  ──(实验一 -38%)──►  精简 Harness 包  ──(实验二 -79%)──►  仅 Coding Wiki
     15.9k 字符                         9.9k 字符                          2.1k 字符
```

- **第一层收益**：Harness **目录与消费纪律**（taxonomy）。
- **第二层收益**：关账后 **编译 Wiki**（synthesis）。
- 二者叠加，回顾类问题的上下文可从「万字级」降到「千字级」量级（本 slug、本题集下）。

---

## 5. 对「项目理解、回溯」的具体提升

| 场景 | 以前 | 试点后 |
| --- | --- | --- |
| **新会话接续某 Epic** | 扫多条 invoke/review | 先读 1 页 synthesis + index |
| **问范围/非范围** | 翻 done task + 排期 | synthesis 写清边界 + pointer 到 L1 |
| **问 freeze_id / 关账日** | 读 task 头 | synthesis frontmatter 即可 |
| **改 API / 查依赖** | 仍易误扫 Harness | 纪律：走 L0 `graph_query`，Wiki 不冒充架构真值 |
| **跨 Epic 为什么** | 散落多份 L1 | 逐步用 `concepts/`、`decisions/` 编织（待扩） |

Wiki 提升的是 **「回忆与综合」**；**「执行与校验」** 仍在 Harness 链 + CI + 图谱。

---

## 6. 已知局限与演进（含测试过程存档）

### 6.1 实验局限

- **样本**：一个文档治理 Epic、四道回顾题。
- **Wiki 不含排期全文**：边界题靠 ingest 时写入 synthesis；漏蒸馏则需回 L1。
- **不等于** Karpathy 式概念/实体全网（index 已设计，页尚未铺开）。

### 6.2 计划扩域（非 coverage 机器真值）

Wiki **不**跑覆盖率、**不**维护与 `tests/` 同步的用例表，而存档 **测试增删改查的过程**：

- 某次 done task：新增/删除了哪些测试、覆盖哪些 failure path（pointer 到图谱 `ERR_*` 与 task `failure_paths`）。
- `decisions/`：退役用例、暂不测分支的缘由。
- 与治理仓「测试 ↔ 图谱 failure path **工具链校验**」**并行**：工具负责硬一致，Wiki 负责 **变更史与意图**。

Schema 见 `CODING_WIKI.md` §8；路线图 **T1c** 见治理 SPEC §5.1。

### 6.3 原文（Raw）何时才需要

工程原文已在 L1。仅当单文件过大、或需对外部剪报库做摘要时，才考虑 `sources/` stub 或独立 Raw——**不是**当前试点主线。

---

## 7. 下一步优先级（与 SPEC 同步）

| 优先级 | 事项 |
| --- | --- |
| **P0** | 试点 task / 实验文档完全关账；本篇 draft 定稿迁入 `docs/diary/` |
| **P1** | **T1c**：1～2 个测试相关 done task ingest + 可选 `concepts/test-strategy-*` |
| **P1** | 对 `tech-graph-gate-d-v2-tasks` 等 **再跑对照实验二**，验证非文档 slug |
| **P2** | 图谱锚点 / 测试 manifest 工具链（与 Wiki 并行） |
| **P2** | **T4** Wiki ↔ 图谱 frontmatter 桥接 |
| **P3** | 前端 Harness parity（P1-4） |

---

## 8. 给读者的 takeaway

1. **LLM Wiki 在本项目不是「又一套 RAG」**，而是 Harness 关账后的 **编译层**，专门对付 **历史回溯上下文爆炸**。
2. **对照实验一** 证明：先把 Harness **收拢成精简包**，回顾类题就能明显省 token。
3. **对照实验二** 证明：在精简包之上，**只读 Wiki 摘要** 还能再省一个数量级（本 slug 下），且 gold 题可保持全对。
4. **默认读序可以升级**，但 **真值纪律不能丢**：实现改图谱，冲突信 L0/L1；Wiki 是入口，不是宪法。
5. **未来扩 Wiki**，优先 **过程档案**（含测试迭代叙事），而不是把 CI 该做的事搬进 Markdown。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | 初稿 tmp；P0 迁入 `docs/diary/` |
