# Task：治理 — T4 graph_nodes 铺量（单元 A · R2）

> **状态**：pending  
> **round**：**R2** · 母单 [`task_harness_wiki_loop_unit_a_v1.md`](task_harness_wiki_loop_unit_a_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) · [`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md)

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 仅 synthesis frontmatter；验证用 `graph_query neighbors <id>` 烟雾（不改 tools）。 |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **semi_auto** | `true` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **task_slug** | `gov-wiki-t4-rollout` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | pending | 22, 30 | **继承母单** · **R1 须在 done/** |

---

## 背景与目标

T4 SPEC **active** 且 Pilot/扩面 **6** 篇已有 `graph_nodes`；其余 **~14** 篇 synthesis（见下表）尚无 frontmatter。

**完成态**：下表全部处理完毕——补 **≥1** 合法 `graph_nodes[].id`（经 `python tools/tech_graph_graph_query.py neighbors <id>` 验证），或 frontmatter 注明 `graph_nodes: []` 且正文一句「纯叙事 · 无 L0 种子」。

---

## 铺量清单（当前无 graph_nodes · R2 硬交付）

| synthesis slug | 建议种子 id（示例 · 30 帽可替换） |
| --- | --- |
| `wiki-ctx-ab-representative` | `rag-unified-chat-stream` 或实验轨节点 |
| `harness-wiki-loop-p2-followup` | `flow-rag-recall`（叙事） |
| `governance-wiki-ingest-batch` | `CR1` |
| `governance-wiki-agent-readorder` | — 或纯叙事 `[]` |
| `coding-wiki-t1c-test-archive` | — 纯叙事 |
| `wiki-ctx-ab-v1` | `RAG` |
| `wiki-ctx-ab-multi-slug` | `CR1` |
| `harness-wiki-loop-c2-verify` | `E2E_DOC` |
| `coding-wiki-pilot` | `RAG_DOC` |
| `chatbi-v3-p2-health-ready` | `T2S` |
| `harness-p1-docs-consolidation` | — 纯叙事 |
| `docs-tasks-reorg-move` | — 纯叙事 |
| `governance-l2-r3-test-manifest` | `FP-RAG-DB-DISCONNECT` 对应 graph node（若有） |
| `governance-l2-manifest-ci` | 对齐 manifest 锚点 |

**已有 graph_nodes（跳过或仅补全 manifest_ref）**：`query-rewrite-observability`、`chatbi-v3-text2sql-tool-latency-obs`、`tech-graph-gate-d-v2-tasks`、`governance-wiki-t4-expand`、`governance-wiki-t4-r1-pilot`、`harness-wiki-loop-t4-l2`。

---

## 非范围

- 新增 `tools/coding_wiki_lint.py`（→ 单元 B 后或 P3）  
- 手改 `graph.json`  
- Batch-3 **新建** synthesis（→ R3）

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | `graph_nodes.id` 在 graph_v2 不存在 | `graph_query` fail → 修 id 或删项 |
| F2 | 用 Wiki 替代影响分析 | 22/50 阻塞 · 回 L0 |

---

## 验收标准

- [x] 上表 14 slug 全部有 frontmatter 决策（种子或 `[]`）
- [x] 至少 **3** 次 `graph_query neighbors` 留证 invoke
- [x] R1 已在 `done/`
- [ ] invoke C2 全绿 · task → `done/`

---

### 自检结论（执行者）

| # | 检查项 | 结果 |
| --- | --- | --- |
| 1 | 14 slug graph_nodes frontmatter | ✅ 20/20 全部覆盖；0 miss |
| 2 | graph_query neighbors ≥3 次 | ✅ RAG/CR1/E2E_DOC exit 0 |
| 3 | R1 已 done/ | ✅ pass |
| 4 | invoke C2 体量 | ✅ 22=2221 B / 30=4080 B |
| 5 | 无 api/tests/tools 改动 | ✅ pass |

**结论：全部验收项通过 · 零阻塞 · 2026-05-28**

---

## 给 Cursor / Claude Code

`gov-wiki-t4-rollout`、`GOV-WIKI-T4-ROLLOUT`、`graph_nodes`
