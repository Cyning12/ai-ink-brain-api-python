# graph_v2 schema（P2-0 + P2-4a 渐进）

> **状态**：`draft` · P2-0 + **P2-4a-1**（`kind`）  
> **落盘路径（默认）**：与本目录 `graph.json` 同文件，`schema_version: graph_v2`（**不**默认并列 `graph_v2.json`）  
> **关联 task**：`docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md`  
> **P2-4a-1 已启用**：`nodes[].kind`（可选）  
> **P2-4a-2 未启用**：`graphs[]`、`edges[].ref`

---

## 1. 根对象

| 字段 | 类型 | P2-0 | 说明 |
| --- | --- | --- | --- |
| `schema_version` | string | **必** | 固定 `graph_v2` |
| `generated_at` | string | **必** | ISO-8601 UTC（`Z` 后缀），与方案1 CI 惯例一致 |
| `freeze_id` | string | **必** | 与 `fixtures/gate_ctx_ab_v1/protocol_version.yaml` 对齐（merge 前 bump） |
| `nodes` | array | **必** | 对象数组，见 §2 |
| `edges` | array | **必** | 对象数组，见 §3 |

**P2-4a-2 未启用（不得出现）**：`graphs[]`、`edges[].ref`。

---

## 2. nodes[]

| 字段 | 类型 | P2-0 | P2-4a-1 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | string | **必** | **必** | 与 Mermaid 节点 id 一致；`graph_query` 主键 |
| `label` | string | **必** | **必** | 自 `[[...]]` / `{...}` / `[...]` 等形状解析的人类可读标签；无形状时可为 `id` |
| `kind` | string | **禁** | **可选** | 枚举：`flow` \| `struct` \| `external`；**缺省**等价 P2-0（FP-4-4） |

**物化顺序（建议）**：按 `id` 字典序稳定排序。

---

## 3. edges[]

| 字段 | 类型 | P2-0 | 说明 |
| --- | --- | --- | --- |
| `from` | string | **必** | 源节点 id |
| `to` | string | **必** | 目标节点 id |
| `mark` | string | **必** | 协议边标记原文或归一标记（`->`、`~>`、`::branches`、`[ok]` 等） |
| `type` | string | **必** | 与 v1 分类兼容（`depends_on`、`async_calls`、`condition`、`branches` 等） |
| `sync` | boolean | **必** | 与 v1 一致 |
| `label` | string | **必** | HTTP 路径、动作语义等；纯协议边可为 `""` |
| `anchors` | array | **必** | 锚点对象列表，见 §4 |

**P2-4a-2 未启用**：`ref`（跨分图引用；与 `from`/`to` 互斥规则在 4a-2 定稿）。

**物化顺序（建议）**：`(from, to, mark, type, sync, label)` 字典序。

---

## 4. anchors[]

| 字段 | 类型 | P2-0 | 说明 |
| --- | --- | --- | --- |
| `path` | string | **必** | 仓库相对路径或 `docs/...` |
| `symbol` | string | **必** | `#L123` 行号或 `::func` 符号；无则 `""` |
| `line` | integer | 可选 | 自 `#Lnnn` 解析的行号 |

锚点来源：`.ai.md` mermaid 块内边后的 `// → ...` 注释（见 `99_mermaid_protocol.md` §3）。

---

## 5. 等价门禁（P2-0 草案阈值）

对照 **参考图**（自 `*.ai.md` 解析）与 **导出 `graph.json`**：

| 指标 | 阈值 | FP |
| --- | --- | --- |
| 拓扑（节点集 + 无向边集 `(from,to,mark)`） | 一致 | FP-3 |
| 锚点行覆盖率 | ≥ **95%** | FP-3 |
| 边 `label` 非空覆盖率（相对参考中有语义 label 的边） | 建议 ≥ **90%**（PR 可单列） | FP-3 |

> **禁止外推**：论文 SBM ARI=1 **不等于** 本仓已等价；仅以本节阈值验收（task §7）。

---

## 6. 与 graph_v1 差异摘要

| 维度 | graph_v1 | graph_v2（P2-0） |
| --- | --- | --- |
| `nodes` | `string[]` | `{ id, label }[]` |
| 边协议标记 | 合并在 `type` 推断 | 显式 `mark` + `label` |
| 锚点 | 无 | `anchors[]` |
| 多分图 | 扁平合并 | P2-4a-2 才引入 `graphs[]` |
| `nodes[].kind` | 无 | P2-4a-1 可选 |

---

## 7. failure_paths（P2-4 映射）

| ID | 触发 | 校验行为 |
| --- | --- | --- |
| FP-4-1 | P2-4 与 P2-0 冲突 | 等价非 0 |
| FP-4-2 | 非法 `ref` / 未知引用 | `validate_graph_v2` 非 0（4a-2） |
| FP-4-3 | query 误读多分图 | pytest `test_tech_graph_graph_query` |
| FP-4-4 | 无 kind 的合法 P2-0 图被拒 | schema **须接受** 无 `kind` |

---

## 8. 工具入口

| 脚本 | 用途 |
| --- | --- |
| `tools/tech_graph_graph_v2_schema.py` | 结构校验、禁止字段门禁 |
| `tools/tech_graph_graph_v2_reference.py` | 自 `.ai.md` 构建参考 v2 |
| `tools/tech_graph_graph_equivalence_check.py` | 参考 vs 已提交 `graph.json`（`--check`） |

导出器升 v2 属 **P2-1**；本阶段不修改 `tech_graph_graph_export.py` 默认输出。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-17 | P2-0 最小 schema 与等价阈值草案 |
| v0.2 | 2026-05-17 | P2-4a-1：`nodes[].kind` 可选枚举；graphs/ref 仍禁 |
