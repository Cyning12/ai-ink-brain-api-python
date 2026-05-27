# SPEC — 治理：后端 Agent · Coding Wiki 默认读序（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-WIKI-AGENT-READORDER@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) · Wiki-CTX-AB P2 签收后 **常模化** |
| **实验依据** | [`docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md`](../../harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md)（W 相对 H-lean **-78.8%** · 4/4） |
| **Schema** | [`docs/coding_wiki/CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §4.2 Query |
| **L2 manifest** | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) · Phase B **done**（`GOV-L2-MANIFEST-CI@2026-05-27`） |
| **执行 task** | [`task_governance_wiki_agent_readorder_v1.md`](../../tasks/active/task_governance_wiki_agent_readorder_v1.md) |

---

## 0. 完成态（一句话）

将 Wiki-CTX-AB **P2 推荐读序** 写入本仓 **Agent 必读链**（`AGENTS.md` + 可选 `.cursor/rules`），使 **关账回顾 / 跨 Epic 理解 / 已 ingest 主题** 默认先走 `docs/coding_wiki/`，**不** 替代 L0 改代码与 L1 单 task 执行真值。

---

## 1. 背景与目标

| 痛点 | 本 SPEC 应对 |
| --- | --- |
| P2 结论仅在实验结论文，**未**进入 Agent 导航 | 升格为 **必读顺序** 一条 |
| Agent 仍默认扫 `invokes/`、`reviews/` 长文 | 先 `index` + `syntheses/<slug>` |
| L2 manifest 已 CI 化，读序未 pointer | 读序中 **可选** 链 `_test_manifest` 与校验脚本 |

**非目标**：前端仓 parity（→ P1-4 另 Epic）；全仓 79 个 done task 强制 ingest（→ Ingest Batch SPEC）。

---

## 2. 读序纪律（强制表述 · 写入 AGENTS）

### 2.1 何时必须先读 Coding Wiki

| 场景 | 读序 |
| --- | --- |
| **关账回顾**、验收对照、跨 Epic 「上次做了什么」 | ① `docs/coding_wiki/index.md` → ② `syntheses/<slug>.md`（1～3 页）→ ③ pointer 打开 L1 `docs/tasks/done/…` |
| **改 `api/` / 表 / 契约 / 流程拓扑** | **仍** L0：`graph_query` + `_manifest` / `_contract` + 对应 `10_flow_*.ai.md`；Wiki **不** 替代 |
| **执行 `docs/tasks/active/` 单 task** | L1 task 正文 + Harness invoke；Wiki **仅** 背景 |
| **失败路径 / ERR 与测试映射** | L2 `_test_manifest.json` + `python tools/tech_graph_test_manifest_check.py`；叙事见 Wiki §8 pointer |

### 2.2 禁止项

- **禁止** 为答题或影响分析 **仅** 读 Wiki 而不跑 `graph_query`（当 task 涉拓扑时）。
- **禁止** 将 Wiki 标为 L0 架构真值；与 `freeze_id` / manifest 矛盾时 **L0/L1 为准**。
- **禁止** 默认 `glob` 整个 `docs/harness/invokes/`（按 task_slug / README / pointer 精读）。

### 2.3 `AGENTS.md` 落盘位置（最小）

在 **「必读（按顺序）」** 中，于 `docs/tasks/` 与 `docs/harness/` 之间（或紧接 `docs/tasks/` 后）插入 **一条**：

- 标题：**Coding Wiki（L2 编译层 · 关账回顾默认读序）**
- 链：`CODING_WIKI.md` · 本 SPEC · `index.md`
- 一句读序：index → syntheses → L1 pointer；改代码仍 L0

### 2.4 可选 `.cursor/rules`（推荐）

新增或增补 **一条** 短规则（≤40 行）：重复 §2.1～2.2；运行 `python tools/gen_agents_md.py` 同步 `AGENTS.md` **自动同步规则** 小节（若改 `.mdc`）。

---

## 3. 与 L2 / T4 的关系

| 项 | 约定 |
| --- | --- |
| **L2 manifest** | 读序文案 **可** 写「查 ERR↔测试映射见 `_test_manifest`」；**不** 要求每次对话跑 check |
| **T4 `graph_nodes`** | synthesis 含 `graph_nodes` 时：读序 **Reminder** = 打开页后对每个 `id` 跑 `graph_query neighbors` |
| **ingest 覆盖** | 无 synthesis 的 Epic **仍** 走 L1；读序 **不** 承诺全覆盖 |

---

## 4. 验收标准（VERIFY）

```bash
rg -n 'coding_wiki|Coding Wiki' AGENTS.md
test -f docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md
# 可选：rules 存在
test -f .cursor/rules/11-coding-wiki-readorder.mdc || true
```

| # | 项 | 通过条件 |
| --- | --- | --- |
| R1 | AGENTS 必读链 | 含 Coding Wiki 条 · 链本 SPEC + `index.md` |
| R2 | 禁止项 | AGENTS 或 rules 含「不替代 L0」「不默认扫全 invokes」 |
| R3 | L2 pointer | 提及 `_test_manifest` 或链 L2 SPEC（一行即可） |
| R4 | 图谱脚本 | `tech_graph_manifest_check.py` exit 0（关账 hygiene） |

---

## 5. 失败路径

| # | 触发 | 行为 |
| --- | --- | --- |
| F1 | 仅改 AGENTS 不写禁止项 | 50 **fail** |
| F2 | 读序写「Wiki 即真值」 | 违反 Roadmap · revert |
| F3 | 删 L0 必读项 | 50 **fail** |

---

## 6. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：P2 签收后后端 Agent 必读链常模化 · 链 L2 Phase B done |

---

## 给 Cursor

`GOV-WIKI-AGENT-READORDER`、Agent 必读、coding_wiki、默认读序、关账回顾、graph_query 优先
