# Reinspect · gov-wiki-t4-expand · 2026-05-27

> **task_slug**: gov-wiki-t4-expand  
> **freeze_id**: GOV-T4-EXPAND@2026-05-27  
> **分支**: task/gov-t4-l2-followup-v1  
> **复检人**: Agent（独立重跑）  
> **结论**: **建议合并 · 无阻塞项**

---

## §1 独立 VERIFY

### 1.1 graph_nodes 覆盖

| # | 检查项 | 命令 | 结果 |
|---|--------|------|------|
| 1 | ≥3 篇 synthesis 含 graph_nodes | `rg -l '^graph_nodes:' docs/coding_wiki/syntheses/ \| wc -l` | **pass**（3） |
| 2 | 扩面 2 slug 各 ≥2 个 graph_nodes | 读 frontmatter | **pass**（chatbi: 3 个；gate-d: 2 个） |

### 1.2 Node id 存在性

| id | 命令 | 结果 |
|----|------|------|
| T2S | `graph_query neighbors T2S` | exit 0 · pass |
| SSE | `graph_query neighbors SSE` | exit 0 · pass |
| U2 | `graph_query neighbors U2` | exit 0 · pass |
| CR1 | `graph_query neighbors CR1` | exit 0 · pass |
| E2E_DOC | `graph_query neighbors E2E_DOC` | exit 0 · pass |

### 1.3 Relation 合法性

全部 relation 在 SPEC §3.1 枚举内：`documents` ×7、`triggers` ×2。

### 1.4 图谱 CI

| 命令 | 结果 |
|------|------|
| `manifest_check` | exit 0 · pass |
| `graph_export --check` | exit 0 · pass |

### 1.5 范围纪律

| 检查项 | 结果 | 备注 |
|--------|------|------|
| 未改 api/ | pass | diff 无 api/ 路径 |
| 未改 tests/ | pass | diff 无 tests/ 路径 |
| 未改 prompts/ | pass | diff 无 prompts/ 路径 |
| 未改 CI workflow | pass | diff 无 .github/ 路径 |
| 未手改 graph.json | pass | diff 无 graph.json |

---

## §2 抽样精读

### 2.1 chatbi-v3-text2sql-tool-latency-obs.md

- frontmatter `graph_nodes`: T2S/SSE/U2，relation 分别为 documents/triggers/documents。
- 正文 T4 pointer 指向 Bridge SPEC §4.1，与 Pilot 风格一致。
- `source_task` 指向 done task，路径正确。

### 2.2 tech-graph-gate-d-v2-tasks.md

- frontmatter `graph_nodes`: CR1/E2E_DOC，relation 均为 documents。
- 正文 T4 pointer 同样指向 Bridge SPEC §4.1。
- 摘要与 L1 task 一致，未漂移。

---

## §3 结论

**10/10 pass · 建议合并。**

无返工项。下一棒：关账（git mv → done/ + _views + CLOSE_TRACE）。
