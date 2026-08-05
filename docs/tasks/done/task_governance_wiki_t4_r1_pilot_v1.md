# Task：治理 — T4 Wiki 图谱桥接 Pilot（R1）

> **状态**：active  
> **母 Loop**：[`task_harness_wiki_loop_t4_l2_v1.md`](task_harness_wiki_loop_t4_l2_v1.md) · round **R1**  
> **SPEC**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；**本 round** 负责 RECENT §6.6 **in_progress** 行（**不**标 done）。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | T4 Pilot · 纯 docs；不改 api/tests。 |
| **freeze_id** | `GOV-T4-R1-PILOT@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-spec-t4-l2-v1` |
| **task_slug** | `wiki-t4-r1-pilot` |
| **wiki_delta** | `docs/coding_wiki` |
| **wiki_delta_note** | 存量迁移 · 本 task 触及 docs/coding_wiki（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 继承 [`HG-LOOP-BATCH`](task_harness_wiki_loop_t4_l2_v1.md) |

---

## 帽子顺序（**跳过 10** · Loop R1）

| 序 | 帽 | 启动 |
|----|-----|------|
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_LOOP_22_to_CLOSE_v1.md) · **round=R1** |

---

## 背景与目标

落实 T4 专文 **Pilot**：单页 synthesis 带 `graph_nodes`，并更新 `CODING_WIKI` 字段/读序/lint。Pilot 页固定为 **`query-rewrite-observability`**（Wiki-CTX 默认 slug · RAG 域清晰）。

**完成态**：

- `docs/coding_wiki/syntheses/query-rewrite-observability.md` frontmatter 含 2～4 个合法 `graph_nodes`（id 经 `graph_query neighbors` 验证）。  
- [`CODING_WIKI.md`](../coding_wiki/CODING_WIKI.md) §3/§4.2/§4.3/§6 已链 Bridge SPEC。  
- RECENT §6.6 增 **Wiki Loop T4+L2** 行（**in_progress**）。

---

## 范围

- [ ] Pilot synthesis `graph_nodes` + 正文图谱 pointer 一行。  
- [ ] `CODING_WIKI.md` T4 字段与 lint。  
- [ ] `RECENT_TASK_SCHEDULE.md` §6.6 in_progress 行 + §8 修订（若惯例需要）。  
- [ ] 22/30/40/50 invoke **C2 全绿**。

## 非范围

- `99_spec` / `00_main` L0 指针（**R2**）。  
- `_test_manifest.json`（**R3**）。  
- 第二页 synthesis 批量 `graph_nodes`。  
- api / tests / Harness prompts / CI。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | 母闸 pending | 22 拒开工 |
| F2 | `graph_nodes.id` 不存在 graph_v2 | 40/50 fail |
| F3 | `relation` 不在 Bridge SPEC §3.1 | lint fail |
| F4 | RECENT 误标 done | 50 fail（属 R3） |

---

## 验收标准

- [ ] `rg '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md`  
- [ ] `rg 'graph_nodes' docs/coding_wiki/CODING_WIKI.md`  
- [ ] 每个 seed id：`python tools/tech_graph_graph_query.py neighbors <id>` exit 0  
- [ ] `python tools/tech_graph_graph_export.py --check` exit 0  

**VERIFY**：

```bash
rg -n '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md
rg -n 'graph_nodes' docs/coding_wiki/CODING_WIKI.md
for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; done
python tools/tech_graph_graph_export.py --check
```

---

## 实现备忘（执行者回填）

| 项 | 内容 |
| --- | --- |
| graph_nodes ids | C1, RAG, RAG_DOC, FTS |
| commits | b1afaf6 (22 review), f2f7505 (30 交付), e4a58d3 (30 invoke) |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| graph_nodes frontmatter 存在 | pass | `rg '^graph_nodes:' query-rewrite-observability.md` line 10 |
| CODING_WIKI 引用 graph_nodes | pass | 5 处命中（§3 字段、§4.2 读序、§4.3 lint、§6 边界、修订记录） |
| seed id 存在 graph_v2 | pass | C1/RAG/RAG_DOC/FTS 全部 `graph_query neighbors` exit 0 |
| graph_export --check | pass | exit 0 |
| CODING_WIKI 链 Bridge SPEC | pass | 头部 T4 桥接 SPEC 链接 |
| RECENT §6.6 in_progress | pass | line 322 T4+L2 in_progress 行 |
| 99_spec T4 指针 | pass | `+Wiki↔图谱桥接（T4·叙事指针）` 小节 |
