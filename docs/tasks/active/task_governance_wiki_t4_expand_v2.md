# Task：治理 — T4 Wiki `graph_nodes` 扩面（Post-Pilot）

> **状态**：draft  
> **前置**：Wiki Loop T4+L2 **实例 4** R1 Pilot · [`task_governance_wiki_t4_r1_pilot_v1.md`](../done/task_governance_wiki_t4_r1_pilot_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)  
> **SKILL**：[`SKILL-docs-governance.md`](../skills/SKILL-docs-governance.md) · [`SKILL-harness-task.md`](../skills/SKILL-harness-task.md)（**单 task**，非 Loop）

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6/§8。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs / Wiki frontmatter；node 存在性用 `graph_query neighbors` 手工 VERIFY，不增 pytest。 |
| **freeze_id** | `GOV-T4-EXPAND@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-wiki-t4-expand-v1` |
| **task_slug** | `gov-wiki-t4-expand` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22, 30 | 本 task + 扩面 slug 列表人扫 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 落盘 `docs/harness/reviews/by-task/gov-wiki-t4-expand/` 后人签 |

---

## 帽子顺序

| 序 | 帽 | 启动 |
|----|-----|------|
| 0（可选） | **10** | 需求帽 · 若 task 已冻结可 **跳过** |
| 1–5 | **22→50→关账** | [`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · invoke · [`PROMPT_START_full_chain_v1.md`](../../harness/invokes/by-task/gov-wiki-t4-expand/PROMPT_START_full_chain_v1.md) |

---

## 背景与目标

Loop 实例 4 **R1** 仅完成 **1 篇** Pilot（`query-rewrite-observability`）。本 task 将 T4 从 **Pilot** 推进到 **小批量扩面**：再为 **2 篇** 高价值 synthesis 补 `graph_nodes` + 正文图谱 pointer，并更新 RECENT / `CODING_WIKI` 覆盖说明。

**完成态**：

- 仓内 **≥3 篇** synthesis 含合法 `graph_nodes`（含既有 Pilot）。  
- 每篇 2～4 个 `graph_nodes[].id`，经 `graph_query neighbors` **exit 0**。  
- RECENT §6.6 **T4** 行反映扩面进度（**勿**误删 T4+L2 done 行）。

---

## 范围

### 必做 slug（2 篇）

| slug | 建议种子域 | 说明 |
|------|------------|------|
| `chatbi-v3-text2sql-tool-latency-obs` | Text2SQL / Unified Chat 相关 node | 正文已有 `11_flow_text2sql` pointer；补 frontmatter |
| `tech-graph-gate-d-v2-tasks` | `graph_query` / 图谱消费相关 node | 与闸口 D / v2 题集叙事一致 |

### 交付清单

- [ ] 上述 2 篇 `docs/coding_wiki/syntheses/*.md`：`graph_nodes` + 一行 L0 pointer（Bridge SPEC §4.1 读序）。  
- [ ] [`CODING_WIKI.md`](../../coding_wiki/CODING_WIKI.md)：§3/§4 增「T4 扩面覆盖表」或更新 lint 说明（列出已覆盖 slug）。  
- [ ] [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §6.6 T4 行 + §8 修订一行。  
- [ ] 22/30/40/50 invoke + review + reinspect（单 task 标准 · invoke §3 ≥15 行）。  
- [ ] 关账 hygiene：[`SKILL-docs-governance.md`](../skills/SKILL-docs-governance.md) H1–H5。

### 可选（有余力）

- [ ] 第三篇：`harness-p1-docs-consolidation`（Harness 域 · `documents` relation）。  
- [ ] Bridge SPEC `draft`→`active` **人审准备**（Agent **不改** status，仅 checklist 备注）。

## 非范围

- `_test_manifest.json` / L2 CI（→ [`task_governance_l2_manifest_ci_v1.md`](task_governance_l2_manifest_ci_v1.md)）。  
- `99_spec` / `00_main` L0 大改（R2 级 VERIFY 已做；本 task 仅 Wiki）。  
- 新增 `tools/` lint 脚本（T4 用 `graph_query` 即可）。  
- `api/`、`tests/`、Harness prompts 正文、CI workflow。

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| T4 SPEC | `docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` §3–§4.3 |
| Pilot 样例 | `docs/coding_wiki/syntheses/query-rewrite-observability.md` |
| graph_query | `python tools/tech_graph_graph_query.py neighbors <id>` |
| Loop 先例 | `docs/harness/invokes/by-task/wiki-loop-t4-l2/REPORT_completion_20260527_v1.md` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | `HG-TASK-DRAFT` pending | 22 拒开工 | 人批后 |
| F2 | `graph_nodes.id` query exit 4 | 40/50 **fail** | 修 id |
| F3 | `relation` 不在 Bridge §3.1 | lint **fail** | 改枚举 |
| F4 | 越界改 api/tests | 50 **fail** · revert | 拆 task |
| F5 | RECENT 与 §8 矛盾 | hygiene H4 **fail** | 人工对齐 |

---

## 验收标准

- [ ] `rg -l '^graph_nodes:' docs/coding_wiki/syntheses/*.md | wc -l` **≥ 3**  
- [ ] 扩面 2 slug 各 ≥2 个合法 `graph_nodes` 项  
- [ ] 对每个新增 id：`python tools/tech_graph_graph_query.py neighbors <id>` → **exit 0**  
- [ ] `python tools/tech_graph_manifest_check.py` · `graph_export --check` 仍绿（未误改 L0）  
- [ ] `docs/harness/reviews/by-task/gov-wiki-t4-expand/` 有 22 R1  
- [ ] `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-expand_YYYYMMDD_v1.md`  
- [ ] 关账：`done/` + `_views/done.md` + RECENT §8

**VERIFY（40 帽）**：

```bash
# 列出含 graph_nodes 的 synthesis
rg -l '^graph_nodes:' docs/coding_wiki/syntheses/

# 示例：逐 id 校验（实施时替换为实际 id）
python tools/tech_graph_graph_query.py neighbors <node-id>

python tools/tech_graph_manifest_check.py
python tools/tech_graph_graph_export.py --check
```

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | （待填） |
| 图谱变更点 | **无**（仅 Wiki frontmatter；禁止手改 `graph.json`） |
| node id 来源 | `graph_query` / `_manifest.json` 切片 · 22 帽记录 |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | （待填） |
| 结论 | pass / fail |
| 要点 | （待填） |

---

## 给 Cursor

`gov-wiki-t4-expand`、T4 扩面、`graph_nodes`、`graph_query`、单 task、`SKILL-harness-task`、`SKILL-docs-governance`
