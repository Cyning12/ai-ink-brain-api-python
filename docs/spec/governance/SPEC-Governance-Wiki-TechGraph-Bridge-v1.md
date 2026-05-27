# SPEC — 治理：Wiki ↔ 技术图谱桥接（T4 · v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
| **扩面 task** | [`task_governance_wiki_t4_expand_v2.md`](../../tasks/done/task_governance_wiki_t4_expand_v2.md) · `GOV-T4-EXPAND@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §2 **T4** |
| **姊妹 SPEC** | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md)（锚点/测试 manifest · 可同 Epic 不同 round） |
| **L0 真值** | `docs/_tech_graph/` · `tools/tech_graph_graph_query.py` |
| **L2 Wiki schema** | [`docs/coding_wiki/CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) |
| **工作区对照** | `Projects/docs/harness/guides/COMPARISON_tech_graph_coding_wiki_graph_memory_v1_zh.md` |

---

## 0. 完成态（一句话）

在 **不替代 L0 拓扑真值**、**不手改 `graph.json`** 的前提下，为 `docs/coding_wiki/` 增加可选 **`graph_nodes` frontmatter** 与 **pointer 纪律**，使 Agent 从 Wiki 页可 **一跳定位** 到 `_tech_graph` 节点 / manifest 切片；`relation` 字段对齐 Mermaid **元关系名**（及 COMPARISON 提议的 Wiki 扩展），并与 `graph_query` 子图查询 **分工明确**。

---

## 1. 背景与目标

| 痛点 | 本 SPEC 应对 |
| --- | --- |
| Wiki 叙事与 L0 节点 **无机器可读链** | `graph_nodes` + 文内 pointer |
| Agent 用 Wiki 代替 `graph_query` 做影响分析 | 读序与 **禁止项** 写清 |
| T4 在 Roadmap 仅一行 **planned** | 本文件为 **可执行 L1 子规** |

**非目标**：图即记忆全栈、Neo4j、将 Mermaid 全文迁入 Wiki。

---

## 2. 规格层级（与 L0 / L2 编译层）

```text
L0  docs/_tech_graph/*.ai.md → graph.json / _manifest / _contract   【拓扑与清单真值】
L1  docs/spec/governance/（本文件）                                    【桥接应然】
L2  docs/coding_wiki/（ingest 摘要）                                  【叙事 + graph_nodes 指针】
```

| 冲突时 | 裁决 |
| --- | --- |
| Wiki prose vs `01_struct` / manifest | **L0 为准** |
| Wiki `graph_nodes` vs 已删除的 node id | lint **fail**，标 `deprecated` 或修 frontmatter |
| 影响面遍历 | **必须** `graph_query`；`graph_nodes` 仅 **入口种子**，非子图替代品 |

---

## 3. Frontmatter 扩展（`graph_nodes`）

在 [`CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md) §3 最小集之上，**syntheses / concepts / entities** 可选增加：

```yaml
graph_nodes:
  - id: rag-unified-chat-stream          # graph_v2 node id（与 graph_query 一致）
    relation: documents                  # Wiki 桥接语义 · 见 §3.1 对照表
    manifest_ref: optional               # 如 endpoints.POST /api/py/unified/chat/stream
  - id: flow-rag-recall
    relation: triggers                   # 与 99_mermaid_protocol §1.3 ::triggers 同名（YAML 无 ::）
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `graph_nodes` | 否 | **数组**；缺省表示「纯叙事页，无图谱锚点」 |
| `graph_nodes[].id` | 是（若存在项） | `graph.json` / `graph_query` 使用的 **稳定 node id** |
| `graph_nodes[].relation` | 推荐 | **枚举**见 §3.1；为 **Wiki→节点** 语义，**≠** `graph.json` 边字段 `type`（如 `depends_on`） |
| `graph_nodes[].manifest_ref` | 否 | 指向 `_manifest.json` 内 path/kind 的 **短键**（非整段 JSON） |
| `graph_nodes[].note` | 否 | 人读一句；**禁止** 替代 L0 边语义 |

### 3.1 `relation` 与 `99_mermaid_protocol` 对照（2026-05-27 核对）

YAML 中 **不写** `::` 前缀；语义对应 Mermaid 边上的 `::meta`（[`99_mermaid_protocol.md`](../../_tech_graph/99_mermaid_protocol.md) §1.3）。

| `relation`（Wiki） | 协议 §1.3 | `graph.json` `edges[].type` | 说明 |
| --- | --- | --- | --- |
| `yields` | `::yields` | `yields` | 流式 / 生成器 |
| `triggers` | `::triggers` | `triggers` | 后台任务等 |
| `gates` | `::gates` | — | Depends / 门禁；图中可能无独立 type |
| `branches` | `::branches` | `branches` | 并行分支 |
| `merges` | `::merges` | `merges` | 归并 |
| `signoff` | `::signoff` | — | 提交确认 |
| `archives` | `::archives` | `archives` | 日志 / 归档 |
| `documents` | **未入 §1.3**（COMPARISON **P1 提议**） | — | 本页 **叙述/记录** 该 node（`// → coding_wiki/...` 或 task done） |
| `evidence` | **未入 §1.3**（COMPARISON **P1 提议**） | — | 本页为设计 **证据**（链 invoke/review 锚点，非正文） |

| **禁止 / 不用** | 原因 |
| --- | --- |
| `depends`、`depends_on` 作 Wiki `relation` | 属 **graph_v2 边 type**，非 §1.3 元关系；影响面用 `graph_query downstream/upstream` |
| 自造未上表字符串 | lint **fail** |

**Pilot 建议**：每项 `graph_nodes` 优先用 **协议 §1.3 已有** 名；若用 `documents` / `evidence`，须在 `note` 或 ingest 说明中标注「待 protocol 增补」（见 COMPARISON `::documents` / `::evidence`）。

**版本**：首版 **不强制** 全站 syntheses 补齐；Pilot 见 §6。

---

## 4. 行为纪律

### 4.1 Agent 读序（含 Wiki 时）

1. `docs/coding_wiki/index.md` → 目标 `syntheses/<slug>.md`  
2. 若 frontmatter 含 `graph_nodes`：记 **种子 id 列表**  
3. 对每个种子：`python tools/tech_graph_graph_query.py neighbors <id>`（1-hop；更深用 `downstream`/`upstream <id> <depth>`）  
4. 需端点/RPC/表/env 清单 → `_manifest.json` / `_contract_manifest.json` 切片  
5. 需流程拓扑叙述 → 对应 `10_flow_*.ai.md` 片段  

**禁止**：仅读 Wiki 即改 `api/` 或推断未在 L0 出现的 RPC/表。

### 4.2 维护纪律（改 L0 时）

| 触发 | 动作 |
| --- | --- |
| 新增/改名 graph node | 改 `.ai.md` → export `graph.json` → CI；**可选** 更新关联 Wiki 页 `graph_nodes` |
| 仅 ingest 新 done task | 更新 synthesis + `graph_nodes`（若该 Epic 涉图谱）；**不** 要求全站回填 |
| 手改 `graph.json` | **禁止**（见 `99_spec.md`、`.cursor/rules/10-tech-graph.mdc`） |

### 4.3 Wiki lint（T4 增量）

**`graph_nodes[].id` 存在性（写死 · 不另增 manifest 脚本）**：

```bash
# 对每个 id：exit 0 = 存在于 graph_v2；exit 4 = FP-4 未知节点
python tools/tech_graph_graph_query.py neighbors <node_id> >/dev/null
```

| 检查 | pass 条件 |
| --- | --- |
| `graph_nodes[].id` 存在性 | 上式 **exit 0**（**禁止** 改用 `manifest_check` 推断 node） |
| `relation` 枚举 | 须在 §3.1 表内（含 `documents`/`evidence` 扩展行） |
| 与 `source_task` 一致性 | synthesis 引用的 Epic 与 node 领域 **不明显矛盾**（50 复检可抽样） |

**VERIFY 增补（Pilot PR）**：

```bash
# 从 Pilot synthesis 抽取 id 并逐条 query（示例；实施可换成小脚本）
python tools/tech_graph_graph_query.py neighbors <pilot-node-id>
```

---

## 5. 范围 / 非范围

### 5.1 范围

- [ ] 本 SPEC 定稿（`draft` → `active`）并链入 Roadmap §2 T4。  
- [ ] 更新 `CODING_WIKI.md` §3/§6（`graph_nodes` 字段 + lint 行）。  
- [ ] **Pilot**：≥1 页 `syntheses/*.md` 带 `graph_nodes`（建议 slug：`query-rewrite-observability` 或当前默认读序 slug）。  
- [ ] `docs/_tech_graph/99_spec.md` 或 `00_main.md` **增一小节 pointer** 链回 Wiki 桥接（≤30 行）。  
- [ ] 验收脚本或文档化 VERIFY（§7）。  

### 5.2 非范围

- 图数据库、Neo4j、INK-P7 全栈。  
- 替换 `graph_query` / 闸口 C/C′/C″ 已 accepted 的 machine 轨。  
- 将 `reviews/` / `invokes/` 全文迁入 Wiki 或 SPEC。  
- 修改 `docs/harness/prompts/` 帽子正文。  
- 本阶段 **强制** 所有 syntheses 补全 `graph_nodes`。  

---

## 6. Pilot 建议（供 task / Loop 引用）

| 项 | 建议值 |
| --- | --- |
| **Pilot 页** | `docs/coding_wiki/syntheses/query-rewrite-observability.md`（或 Multi slug 已 ingest 页） |
| **种子 nodes** | 与 RAG / unified chat 相关的 2～4 个 id（由 `graph_query` 从 `rag` 入口展开后 **人择** 固定） |
| **交付 PR** | 纯 docs；单 PR 可与 L2 工具链 SPEC 分 round |

---

## 7. 验收标准（VERIFY）

```bash
# V1 · Pilot 页含 graph_nodes
rg -n '^graph_nodes:' docs/coding_wiki/syntheses/*.md

# V2 · CODING_WIKI 已引用本 SPEC 或 §graph_nodes
rg -n 'graph_nodes' docs/coding_wiki/CODING_WIKI.md

# V3 · 图谱 CI 仍绿（未改 api 时亦应绿）
python tools/tech_graph_manifest_check.py
python tools/tech_graph_graph_export.py --check
```

| # | 验收项 | 通过条件 |
| --- | --- | --- |
| A1 | SPEC 状态 | 本文件 `active` · `GOV-T4-SPEC-ACTIVE@2026-05-27` |
| A2 | Pilot frontmatter | ≥1 synthesis 含合法 `graph_nodes` |
| A3 | 读序文档 | `CODING_WIKI.md` 已更新 lint/字段 |
| A4 | L0 指针 | `99_spec` 或 `00_main` 含 Wiki 桥接链 |

---

## 8. 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
| --- | --- | --- | --- |
| F1 | Wiki 被当作唯一拓扑真值改代码 | 22/50 **阻塞**；回 L0 + graph_query | 是 |
| F2 | `graph_nodes.id` 不存在于 graph_v2 | lint/VERIFY **fail** | 修 id 或删项 |
| F3 | 手改 `graph.json` 未改 `.ai.md` | CI `graph_export --check` **fail** | 改源图 |
| F4 | 将 invoke/review 全文写入 Wiki | lint **fail**；删正文 | 改 ingest |

---

## 9. 与 Harness / Loop 的关系

| 项 | 约定 |
| --- | --- |
| **test_strategy** | 本子规交付 **建议** `not_applicable`（纯 docs）；若 round 改 `tools/` 仅做 query 烟雾则 `recommended` |
| **Loop Batch** | 可作为 **R1/R2** 子 round 主题；母单须链本 SPEC + [`SKILL-harness-loop-batch.md`](../../tasks/skills/SKILL-harness-loop-batch.md) |
| **关账** | 须 `REPORT_completion_*` §1～§5 落盘（§6 后续仅对话） |

### 9.1 扩面 synthesis 索引（`graph_nodes` · ≥3 篇）

Post-Pilot 扩面 **done**（`GOV-T4-EXPAND@2026-05-27`）。Agent 从 Wiki 跳转 L0 时优先打开：

| synthesis slug | `freeze_id`（页 frontmatter） | 种子 `id`（示例） |
| --- | --- | --- |
| [`query-rewrite-observability`](../../coding_wiki/syntheses/query-rewrite-observability.md) | `task_05_query_rewrite_obs@2026-05-22` | `C1` · `RAG` · `RAG_DOC` · `FTS` |
| [`chatbi-v3-text2sql-tool-latency-obs`](../../coding_wiki/syntheses/chatbi-v3-text2sql-tool-latency-obs.md) | `CHATBI-V3-TEXT2SQL-OBS@2026-05-11` | `T2S` · `SSE` · `U2` |
| [`tech-graph-gate-d-v2-tasks`](../../coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md) | `TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0` | `CR1` · `E2E_DOC` |

汇总页：[`governance-wiki-t4-expand`](../../coding_wiki/syntheses/governance-wiki-t4-expand.md)。

---

## 10. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1 草案：T4 专文 · `graph_nodes` · 读序/lint/VERIFY · Pilot |
| 2026-05-27 | v1.1：§3.1 协议对照 · lint 写死 `graph_query neighbors` · 读序修正 |
| 2026-05-27 | v2 **active**：P2 Loop R1 · `GOV-T4-SPEC-ACTIVE@2026-05-27` · §9.1 扩面 synthesis 索引 |

---

## 给 Cursor

`GOV-WIKI-T4-BRIDGE`、`graph_nodes`、`::documents`、`::evidence`、`graph_query`、`coding_wiki`、T4、Wiki 图谱桥接
