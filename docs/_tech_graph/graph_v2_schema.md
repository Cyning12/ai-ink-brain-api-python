# graph_v2 schema（P2-0 + P2-4a）

> **状态**：`draft` · P2-0 + **P2-4a**（`kind` + `graphs[]` + `edges[].ref`）  
> **落盘路径（默认）**：与本目录 `graph.json` 同文件，`schema_version: graph_v2`  
> **关联 task**：`docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md`  
> **导出**：自 `*.ai.md` 导出时写入 `graphs[]` 与各节点/边的 `graph_id`；**无** `graphs` 键时仍按 P2-0 验收（FP-4-4）

---

## 1. 根对象

| 字段 | 类型 | P2-0 | P2-4a | 说明 |
| --- | --- | --- | --- | --- |
| `schema_version` | string | **必** | **必** | 固定 `graph_v2` |
| `generated_at` | string | **必** | **必** | ISO-8601 UTC（`Z` 后缀） |
| `freeze_id` | string | **必** | **必** | 与 `protocol_version.yaml` · `graph_v2_freeze_id` 对齐 |
| `nodes` | array | **必** | **必** | 见 §2 |
| `edges` | array | **必** | **必** | 见 §3 |
| `graphs` | array | **禁** | **导出必有** | 分图目录；元素见 §5 |

---

## 2. nodes[]

| 字段 | 类型 | P2-0 | P2-4a | 说明 |
| --- | --- | --- | --- | --- |
| `id` | string | **必** | **必** | `graph_query` 主键（全局扁平） |
| `label` | string | **必** | **必** | 人类可读标签 |
| `kind` | string | **禁** | **可选** | `flow` \| `struct` \| `external` |
| `graph_id` | string | **禁** | **导出必有** | 须存在于 `graphs[].id` |

**物化顺序**：`(graph_id, id)` 字典序（导出器）。

---

## 3. edges[]

### 3.1 拓扑边（与 P2-0 同型）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `from` / `to` | string | 源/目标节点 id |
| `mark` / `type` / `sync` / `label` / `anchors` | 同 P2-0 | |
| `graph_id` | string | 可选；导出时写入来源分图 |

### 3.2 引用边（P2-4a-2）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ref` | object | `{ "node_id": string, "graph_id"?: string }` |
| `mark` / `type` / `sync` / `label` / `anchors` | **必** | 与拓扑边相同 |

**互斥**：含 `ref` 时 **不得** 出现 `from`/`to`。`graph_query` **忽略** ref 边（单图 BFS 不变）。

---

## 4. anchors[]

同 P2-0（`path`、`symbol`、可选 `line`）。

---

## 5. graphs[]

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 分图 id（默认与 `*.ai.md` 文件名去后缀一致） |
| `title` | string | 展示用标题（导出默认同 `id`） |
| `source_ai_path` | string | 可选；来源 `.ai.md` 仓库相对路径 |

---

## 6. 等价门禁

拓扑比较 **仅** 含 `from`/`to` 的边（排除 `ref`）。阈值同 P2-0：锚点 ≥95%、边 label ≥90%。

---

## 7. failure_paths（P2-4）

| ID | 触发 | 行为 |
| --- | --- | --- |
| FP-4-1 | 字段冲突 | 等价非 0 |
| FP-4-2 | `ref` 未知节点/graph | `validate_graph_v2` 非 0 |
| FP-4-3 | query 默认多读分图 | **禁止**；ref 不参与 BFS |
| FP-4-4 | 无 P2-4 键的 P2-0 图被拒 | schema 须接受 |

---

## 8. 工具入口

| 脚本 | 用途 |
| --- | --- |
| `tools/tech_graph_graph_v2_schema.py` | 结构校验 |
| `tools/tech_graph_graph_v2_reference.py` | 参考 v2（含 P2-4） |
| `tools/tech_graph_graph_export.py` | 导出 `graph.json` |
| `tools/tech_graph_graph_equivalence_check.py` | 等价 CI |
| `tools/tech_graph_graph_query.py` | 单图 query（忽略 ref） |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-17 | P2-0 最小 schema |
| v0.2 | 2026-05-17 | P2-4a-1：`kind` |
| v0.3 | 2026-05-17 | P2-4a-2：`graphs[]`、`ref`、导出 graph_id |
