# 图谱 + Coding Wiki 升级方案 · 问答实录（v1）

| 项 | 内容 |
| --- | --- |
| **版本** | v1.2 |
| **日期** | 2026-06-16 |
| **状态** | `proposal` · 待 task / Epic 立项 |
| **仓库** | `ai-ink-brain-api-python` |
| **关联 L0** | [`00_main.md`](./00_main.md) · [`00_main.graph.yaml`](./00_main.graph.yaml) · [`graph.json`](./graph.json) · [`graph_v2_schema.md`](./graph_v2_schema.md) |
| **关联清单** | [`_manifest.json`](./_manifest.json) · [`_contract_manifest.json`](./_contract_manifest.json) |
| **关联 L2** | [`docs/coding_wiki/`](../coding_wiki/) · [`WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) |
| **trace 示例** | [`examples/harness_trace_v1.example.json`](./examples/harness_trace_v1.example.json) |
| **理论背景** | 本体论 + OOP + 图论 + History · cyning-harness / HGM 提案 |

> **背景**：本文档记录后端「Mermaid 人类版 + `.ai.md` 机器版 + JSON 门禁/依赖」**历史时期**实践与升级方向。  
> **当前态（v1.3+）**：编辑源为 `*.graph.yaml` · export 读 YAML · **`.ai.md` 已物理删除**（Post-G0 · 2026-06-17）。下文 Q&A **保留历史讨论原文**。
> **定位**：Q&A 草稿 · 供未来 engineering task（如 tech_graph v3 / trace / wiki 编译层）起草引用；**非**已签收实现真值。

---

## 目录

1. [Q1 · 当前方案评价（本体 / OOP / 图论）](#q1--当前方案评价本体--oop--图论)
2. [Q1 续 · History 怎么融入](#q1-续--history-怎么融入)
3. [Q2 · Git + 文档落盘下的 History 升级](#q2--git--文档落盘下的-history-升级)
4. [Q2 · `.ai.md` 机器可读替代（YAML 双向绑定）](#q2--aimd-机器可读替代yaml-双向绑定)
5. [Q3 · `trace.json` 草案](#q3--tracejson-草案)
6. [总结与下一步（优先级）](#总结与下一步优先级)

---

## Q1 · 当前方案评价（本体 / OOP / 图论）

**问**：现在使用的是 Mermaid 正常给人类看的，有一套 `.ai.md` 如下机器读取，同时也配有 JSON 进行改动门禁和依赖查询：

- [`_contract_manifest.json`](./_contract_manifest.json)
- [`_manifest.json`](./_manifest.json)
- [`graph.json`](./graph.json)
- [`00_main.ai.md`](./00_main.ai.md)

**答**：你展示的这个实践非常扎实，而且恰好印证了「本体论 + OOP + 图论」融合落地的可行性——你已经在用一套 **多模态文档 + 结构化清单 + 图 JSON** 的组合，系统化地建模了一个真实 AI 系统的架构知识。

下面从 **本体论、OOP、图论** 三个维度评价当前方案，然后重点回答：**History 怎么融入**。

### 1. 本体论维度 ✅ 已经具备核心要素

本体论要求：类、属性、关系、公理、实例。

你已有：

| 层次 | 现状 |
| --- | --- |
| **类** | `_manifest.json` 中的 `endpoints`、`supabase.tables`、`env`、`anchors` —— 「端点类」「数据表类」「环境变量类」「代码锚点类」 |
| **属性** | 每个 endpoint 有 `method`、`path`、`handler`；table 有名称；env 有键名 |
| **关系** | `graph.json` 的 `edges`：`depends_on`、`branches`、`async_calls`、`merges`、`triggers`、`archives` 等 |
| **公理** | `_contract_manifest.json` 的 `sse.chain.payload_min_keys_by_type`、`allowed_events`、`envelope_keys` |
| **实例** | 具体 endpoint 列表、edge 列表 |

**评价**：已建立 **领域特定本体**（API + 数据流 + 代码锚点），JSON + Markdown 双轨存储 —— 即 ontology + 机器可读 + 人类可读的落地形式。

**改进空间**：

- 缺少显式 **类继承/特化**（如 `tool.call.start` / `tool.call.end`）→ 可在 `_contract_manifest.json` 增 `type_hierarchy`
- 缺少 **基数约束**（如 endpoint 至少一个 anchor）→ 在 manifest schema 补 `minItems` 等校验

### 2. OOP 维度 ✅ 隐式存在，可显式化

通过 **文件路径 + 锚点符号**（如 `api/index.py::unified_chat_route`）关联代码与架构图，相当于 OOP 中类/方法的文档化。

未直接在图中画 Python 继承/方法调用（通常非架构图目标）；`graph.json` 的 `depends_on` 可视为方法调用/数据流的抽象。

**评价**：用「节点-边」表达运行时拓扑，比硬套 UML 类图更清晰；OOP 细节留给代码，文档负责宏观连接。

**建议**：若需代码级关系（implements / extends），在 `_manifest.json` 增数组，并在 `graph.json` 引用。

### 3. 图论维度 ✅ 优秀实践，且已工业化

| 能力 | 实现 |
| --- | --- |
| 可视化 | 各 `.ai.md` 内 Mermaid |
| 结构化 | `graph.json`：`nodes` / `edges`，边类型 + `sync` + `anchors` |
| 分析 | 依赖分析 · 门禁 · 影响分析 |

边类型区分同步/异步、分支、合并等，比简单「依赖图」更细。

**缺失**：未显式存储路径或拓扑排序结果（可查询时动态计算）。

---

## Q1 续 · History 怎么融入

History **不是**传统图论的直接组成部分，但可通过 **事件节点** 或 **时序边** 无损加入现有模型。

需记录两类历史：

1. **架构图演进**（endpoint handler 从 chat → unified_chat）
2. **运行时事件历史**（某次请求经过哪些节点、耗时、错误）

### 2.1 架构演进历史（Schema 版本演进）

已有 `freeze_id`、`generated_at` —— 这是 **快照**，不是 **历史**。

可选方案：

- `graph.json` 同级 `history/` 存每次变更 patch（类 Git）
- 或 `freeze_id` 有序版本号 + `CHANGELOG.json` 记录节点/边增删改

查询示例：「2026-05-01 前 `/api/py/unified/chat` 是否存在？」「v2.0→v2.3 新增哪些依赖？」

→ 本体论 **概念演化**，属元本体层。

### 2.2 运行时调用历史（Execution Trace）

**静态蓝图**（`graph.json`）不改；新增 **traces/** 目录，每条 trace 一个 JSON。

```json
{
  "trace_id": "task_123_30_invoke",
  "started_at": "2026-06-15T10:00:00Z",
  "ended_at": "...",
  "steps": [
    {
      "node_id": "AUTH",
      "entered_at": "...",
      "exited_at": "...",
      "status": "success",
      "output": {}
    },
    {
      "edge_id": "U2--AUTH",
      "traversed_at": "...",
      "latency_ms": 12
    },
    {
      "node_id": "RAG",
      "status": "failure",
      "error": "embedding timeout"
    }
  ]
}
```

关联 Task：frontmatter 或 InvokeSnapshot 记录 `trace_id`。

→ **时序属性图**：静态节点/边 + 每次遍历的带时间戳足迹；可聚合「哪条边最慢」「哪节点失败率高」。

### 2.3 与 Harness 纪律包的集成点

ProcessTrack 的 **InvokeSnapshot**、**AuditReview** 可承载 trace：

- 扩展 InvokeSnapshot 模板，记录图足迹
- 30 执行：读 `graph.json` → 记录 node_id / edge_id → 写 `trace_<timestamp>.json`
- AuditReview 引用 trace + 聚合摘要（「4 节点 · 3 边 · 2.3s」）

→ 从「静态约束」升级为 **可观测执行闭环**。

---

## Q2 · Git + 文档落盘下的 History 升级

**问**：

1. 这是本体论+OOP+图论+History 完整想法落地前的摸索；现在要升级，尤其 **History** —— 仍基于 **Git commit + 过程落盘文档**（文档用 LLM Wiki 思想管理）。
2. `.ai.md` 是否用更适合机器读的格式替代？JSON / YAML / 更偏机器语言？人类已有 `.md`，可 **双向绑定**。
3. 起草 `trace.json`，看效果。

**答**：

### 1. 升级方案：基于 Git + 文档落盘的 History 增强

当前已有：

- **Git 历史**：文件级变更（架构图、本体、契约、task）
- **过程落盘**：InvokeSnapshot、AuditReview、Task（Markdown）

核心问题：如何把 Git「文件级历史」与「运行时调用足迹」关联，并支持查询分析。

#### 1.1 架构演进历史（Schema versioning）

不引入 DB，在 `docs/_tech_graph/` 维护 **版本索引**：

```text
docs/_tech_graph/
  .version/
    manifest.json          # 版本清单
    v2026-05-19/
      graph.json
      _manifest.json
      _contract_manifest.json
    v2026-06-01/
      ...
  current/                 # 符号链接或指向最新版本
    graph.json -> ../.version/v2026-06-01/graph.json
```

版本清单 `manifest.json` 示例：

```json
{
  "versions": [
    {
      "version_id": "v2026-05-19",
      "git_commit": "a3f2c9e",
      "generated_at": "2026-05-19T10:00:00Z",
      "freeze_id": "TECH_GRAPH_S2_FREEZE_20260519_V2_3"
    },
    {
      "version_id": "v2026-06-01",
      "git_commit": "b4d5e6f",
      "generated_at": "2026-06-01T14:30:00Z",
      "freeze_id": "TECH_GRAPH_S3_FREEZE_20260601_V1_0"
    }
  ],
  "current": "v2026-06-01"
}
```

**CLI（远期）**：

| 命令 | 作用 |
| --- | --- |
| `harness history diff --from v2026-05-19 --to v2026-06-01` | 节点/边差异 |
| `harness history list` | 版本列表 |
| `harness history checkout v2026-05-19` | 检出旧版到 `current/` |

→ 架构蓝图历史：**Git + JSON 索引**，无新依赖。

#### 1.2 运行时调用历史（Execution traces）

升级 InvokeSnapshot：

```text
docs/harness/invokes/by-task/fix_login_bug/
  invoke_30_20260615.md
  trace_20260615_143022.json
```

AuditReview 引用示例：

```markdown
## 执行轨迹
- Trace: [trace_20260615_143022.json](./trace_20260615_143022.json)
- 总耗时: 23.0s
- 通过节点: E, U2, AUTH, RAG, LLM, OUT
- 失败节点: 无
```

**CLI（远期）**：

| 命令 | 作用 |
| --- | --- |
| `harness trace list --task <slug>` | 该 task 全部 trace |
| `harness trace show --trace-id <id>` | 格式化轨迹 |
| `harness trace analyze --task <slug> --metric latency` | 聚合耗时/失败率 |

→ 运行时足迹与 task/审计绑定，不破坏现有文档结构。

---

### 2. `.ai.md` 的机器可读替代（YAML 双向绑定）

`.ai.md` 对 AI 友好，但解析 Mermaid + 注释仍有歧义。

**推荐：YAML 为机器真相源，脚本生成 `.ai.md`**

| 格式 | 结论 |
| --- | --- |
| **JSON** | 适合聚合（`_manifest.json`）；单图拓扑手写差 |
| **YAML** | 支持注释 · 与 frontmatter 一致 · **推荐单图源** |

**工作流**：

1. 编辑 `docs/_tech_graph/00_main.yaml`（结构化）
2. pre-commit / CI：`yaml → .ai.md`（Mermaid + 人类表格）
3. `.md` 保留供 GitHub 预览；或仅 CI 生成

**YAML 示例（节选）**：

```yaml
graph_id: "00_main"
title: "主路由图"
description: "API 入口分发与子流程路由"
nodes:
  - id: "Q"
    label: "用户请求"
    type: "input"
  - id: "E"
    label: "@router.dispatch"
    type: "decision"
    anchors:
      - path: "api/index.py"
        line: 434
edges:
  - from: "Q"
    to: "E"
    type: "depends_on"
  - from: "E"
    to: "U1"
    type: "depends_on"
    label: "POST /api/py/unified/chat"
    anchors:
      - path: "api/index.py"
        line: 561
```

**与 `_manifest.json`**：跨图聚合索引可继续手动或 CI 合并；YAML 只管单图拓扑；后期脚本做一致性对比。

**双向同步**：优先 **YAML → .ai.md**；反向 Mermaid → YAML 可行但解析成本高。

---

## Q3 · `trace.json` 草案

基于 `00_main` 与 unified chat 路径的完整示例见：

**[`examples/harness_trace_v1.example.json`](./examples/harness_trace_v1.example.json)**

### 关键字段

| 字段 | 说明 |
| --- | --- |
| `schema_version` | `harness_trace_v1` |
| `trace_id` / `task_slug` / `git_commit` | 与 InvokeSnapshot 关联 |
| `graph_freeze_id` / `graph_id` | 绑定静态蓝图版本 |
| `steps[]` | 时序混合 **节点**（entered/exited）与 **边**（traversed + latency_ms） |
| `details` | 节点级结构化信息（RAG 检索、LLM token） |
| `aggregated_metrics` | 快速分析，免遍历 steps |
| `related_artifacts` | invoke / review 路径 |

### 存储约定（proposal）

| 位置 | 说明 |
| --- | --- |
| 与 invoke 同目录 | `trace_<timestamp>.json` |
| 或集中 | `docs/harness/traces/` + 文件名关联 |

### 生成方式（proposal）

- 30 执行插桩（API 前后时间戳）
- 或 ingest 日志对齐 `graph.json` 节点 ID

---

## 总结与下一步（优先级）

| 维度 | 现状 | 升级方向 |
| --- | --- | --- |
| **本体论** | `_manifest` + `_contract_manifest` | `type_hierarchy` · schema 基数约束 |
| **OOP** | 锚点隐式 | 可选 `implements` / `extends` |
| **图论** | `graph.json` + Mermaid | 保持；可选 YAML 源 |
| **History · 架构** | `freeze_id` 快照 | `.version/` + history manifest |
| **History · 运行时** | 无 | `trace.json` + Harness 集成 |
| **Coding Wiki** | L2 编译层 + Git | trace / synthesis 链入 wiki 索引 |

**下一步（按优先级）**：

1. **YAML → Mermaid** 转换脚本（Python），建立 YAML 图源（试点 `00_main.yaml`）
2. **30 模板** 增 `--record-trace`，自动生成 `trace.json`
3. **`harness trace` CLI**（先 `list` / `show`）
4. **AuditReview 模板** 增 trace 引用段
5. **engineering task** 立项：tech_graph v3 · 与 [`graph_v2_schema.md`](./graph_v2_schema.md) / CI gate 对齐

---

## 已知遗留

### 幽灵节点

`graph.json` / `.graph.yaml` 中允许 **边引用未在 `nodes` 列表声明的节点**（俗称「幽灵节点」）。该行为继承自现有 `graph.json` 的设计，用于表达跨图引用或外部抽象；当前 task 不手改拓扑，也不引入 `external_ref` schema。后续若需显式建模，应单独立项并在 schema 层补 `external_ref` 字段。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.3 | 2026-06-17 | P1 export YAML 单源 · 7× `.ai.md` 物理删除（Post-G0）· 历史 Q&A 节保留 |
| v1.2 | 2026-06-16 | 增 §已知遗留 · 幽灵节点（边可引用未声明节点 · 继承 graph.json · `external_ref` 另 task） |
| v1.1 | 2026-06-16 | YAML 图源已落地 · `.ai.md` deprecated · `graph.json` export 仍为过渡方案 |
| v1.0 | 2026-06-16 | 初版 · Q&A 落盘 · trace 示例 JSON |
