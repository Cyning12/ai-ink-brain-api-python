# Task：技术图谱 — 机器轨升级（graph_v2 + 方案2 图查询 + 闸口 B）

> **状态**：`draft`  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **前置验收**：方案1 `graph.json`（`task_engineering_tech_graph_graph_json_export_v1.md` · done）；闸口 A 行为实验（`docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` · accepted）  
> **理论参照**：`docs/diary/jsonPKmermaid/三相塌缩等价性论文_拓扑综合.md`（等价塌缩 vs 有损投影；SelectEnd / 查询消费）  
> **test_strategy**：`required`  
> **test_strategy_note**：v2 等价门禁与 query API 为机器轨核心；无 pytest + 闸口 B 复现则无法证明「优化机器轨」成立。  
> **freeze_id**（草案）：`TECH_GRAPH_S2_FREEZE_TBD`（实现 PR 定稿后与 `protocol_version.yaml` 同步 bump）

---

## 0. 架构决议（G-END · 草案）

| 决议 ID | 内容 |
| --- | --- |
| **G-END-1** | **终局**是优化 **机器轨消费**（清单 + 拓扑 + 查询），**不是**给人轨 `*.md` 再加一层维护负担。 |
| **G-END-2** | **人读轨**：`docs/_tech_graph/*.md`（含 `00_main.md`、`10_flow_*.md` 人读流程图，及下文「规范层」专档）。 |
| **G-END-3** | **协议维护轨（短期真值）**：`*.ai.md` — 供 Agent/协议与 **导出**；人主要在 PR diff 中编辑，**非**日常扫读面。 |
| **G-END-4** | **退役 `.ai.md` 作为维护源** 仅当：**(a)** v2 与 `.ai.md` 拓扑+锚点+边语义 **等价性验收通过**；**(b)** 闸口 B 证明 **v2+query** 在 P1/P2 **不劣于** Mermaid 整包臂，且 P3/P4 不劣于基线；**(c)** 书面签收。本 task **不**包含退役。 |
| **G-END-5** | 方案1 的 **v1 整包 `graph.json` 替代 `*.ai.md` 主载荷** 已由闸口 A **否定**；本 task **禁止**将「默认 Agent 只灌 v1 整图」作为交付默认。 |

### 0.1 轨道分层（消歧「三轨别扭」）

```text
┌─ 人读轨 ─────────────────────────────────────────────┐
│  *.md：流程人读版 + 01_struct / 02_version / 99_*    │
└────────────────────────────────────────────────────┘

┌─ 协议维护轨（短期）──────────────────────────────────┐
│  *.ai.md：flowchart 协议版 → 导出输入                  │
└────────────────────────────────────────────────────┘

┌─ 机器轨 · 清单/契约（已有，可增补）────────────────────┐
│  _manifest.json · _contract_manifest.json            │
└────────────────────────────────────────────────────┘

┌─ 机器轨 · 拓扑（本 task 升级）──────────────────────────┐
│  graph_v1 → graph_v2（富化/等价）                     │
│  graph_query（方案2 · 消费方式）                        │
└────────────────────────────────────────────────────┘

┌─ 人机同读 · 规范层（不并入 v1 flow graph；按需加载）───┐
│  01_struct.md · 02_version.md · 99_spec.md ·         │
│  99_mermaid_protocol.md                              │
└────────────────────────────────────────────────────┘
```

| 阶段 | 机器轨形态 |
| --- | --- |
| **旧（方案1 落地后）** | manifest + contract + **整包 `.ai.md` 或整包 v1 `graph.json`**（实验二选一；日常规则「先 JSON」） |
| **新（本 task 目标）** | manifest + contract + **v2 图真值/导出** + **`graph_query` 子图消费**；`.ai.md` 仍为维护/export 源直至 G-END-4 |

---

## 1. 背景与目标

方案1 已提供 **`graph_v1`**（从 `*.ai.md` 导出的拓扑边集）与 CI `--check`。闸口 A（`gate_ctx_ab`）表明：

- 主载荷 **token 近 1:1**（~5056 vs ~5026），**格式替换不是省钱主因**；
- **v1 相对 `.ai.md` 为有损投影**（锚点、边文案、节点标签等未落盘），P1/P2 **偏 Mermaid**；
- **不签收**「生产 Agent 一律 `graph.json` 主载荷」。

本 task 目标：在 **不推翻人读 `*.md`、不强制本阶段退役 `.ai.md`** 的前提下，将机器轨升级为：

1. **`graph_v2`**：在拓扑之上承载 **语义/锚点/分图**（向「等价塌缩」靠拢，见论文 §4.1 精神）；  
2. **`graph_query`（方案2）**：Agent **确定性查询** 上下游/影响集，**默认不**整包灌输 20KB 图；  
3. **等价性门禁 + 闸口 B**：可复现证明「机器轨升级」相对方案1 **有净收益**。

---

## 2. 范围 / 非范围

### 2.1 范围

**A. graph_v2 schema 与导出（方案1 演进）**

- [ ] 在工作区 SPEC 或本仓 `docs/_tech_graph/` 旁落盘 **`graph_v2` schema 草案**（字段名 PR 定稿）。  
- [ ] 最小字段集（草案，可裁剪）：

| 字段/结构 | 说明 |
| --- | --- |
| `graphs[]` | 分图 id，对应 `00_main`、`10_flow_*` 等 |
| `nodes[].id` / `label` / `kind` | 节点与中文/角色标签 |
| `edges[].from/to` | 有向边 |
| `edges[].mark` | 协议标记：`->`、`[ok]`、`::branches` 等 |
| `edges[].type` / `sync` | 与 v1 分类兼容并扩展 |
| `edges[].label` | HTTP 路径等边文案（避免塌缩为纯 `depends_on`） |
| `edges[].anchors[]` | `{ "path", "symbol", "line"? }` |
| `edges[].ref` | 子图引用，如 `graph:10_flow_rag` |
| `schema_version` / `generated_at` / `freeze_id` | 与现 CI 惯例一致 |

- [ ] 升级 `tools/tech_graph_graph_export.py`（或 v2 专用脚本）：`.ai.md` → `graph.json`（`schema_version: graph_v2`）或 **v2 并列文件**（PR 二选一，须写清迁移）。  
- [ ] **`tools/tech_graph_graph_equivalence_check.py`（建议新名）**：对比「从 `.ai.md` 解析的参考图」与「v2 导出图」— 拓扑一致 + 锚点/边标签覆盖率 ≥ 阈值（阈值 PR 定稿，建议先 95% 锚点行）。  
- [ ] pytest：v2 golden、等价检查失败路径。  
- [ ] CI：`tech-graph.yml` 接入 v2 校验（与 v1 过渡策略在 PR 说明）。

**B. graph_query（方案2）**

- [ ] `tools/tech_graph_graph_query.py`（名待定）：冷启动加载 v2（或 v1 降级只读拓扑，**文档写明差异**）。  
- [ ] 查询面（最小）：`downstream(node_id, depth)`、`upstream(node_id, depth)`、`neighbors(node_id)`；返回 **JSON 可序列化** 子图或边列表 + 关联 anchors。  
- [ ] CLI：`python tools/tech_graph_graph_query.py downstream AUTH 2`（参数名 PR 定稿）。  
- [ ] （可选 P1）MCP 注册 — 非阻塞本 task 核心验收，可 follow-up。  
- [ ] 更新 `.cursor/rules/10-tech-graph.mdc`：**影响分析必须优先 query**，禁止默认整包 v1 `graph.json` 进 prompt。

**C. 规范层与 manifest（按需切片，非全部 JSON 化）**

- [ ] 文档化 **Agent 加载顺序**（机器轨完整视图）：

```text
graph_query(…) → _manifest（端点/RPC/表锚点）→ _contract（若涉 SSE）
→ 按需 01_struct（改表）→ 按需 99_spec（Env/约束）
→ 按需 10_flow_*.ai.md 片段（仅当 query 结果不足）
```

- [ ] （可选）manifest 增补 `graph_node_id` 与 endpoint 的 ref，避免 path 重复 — 若超 scope 记入实现备忘 follow-up。

**D. 闸口 B（方案2 后）**

- [ ] 在 `docs/diary/jsonPKmermaid/` 或 `docs/tech_graph/` 落盘 **闸口 B** 报告（对比组见 §6）。  
- [ ] 新增实验 arm **`CTX_QUERY`**（v2 + query 结果 + manifest/contract），**不复测**「v1 整包 vs Mermaid」作为主结论。

### 2.2 非范围

- 方案3 Neo4j（**R2** 未满足前不立项）。  
- 本阶段 **退役 `*.ai.md`** 或 **删除人读 `10_flow_*.md`**。  
- 将 `01_struct` / `99_spec` **全文并入** 单一 `graph.json`（可做可选 `struct.json` follow-up，非本 task 必须）。  
- 改写 `99_mermaid_protocol.md` 协议语义（仅遵守）。  
- 前端仓实施（可另开 `ai-ink-brain` 镜像 task；本单仅后端）。  
- 合并 `tech_graph_contract_check` 与 graph 导出逻辑。

---

## 3. 依赖与引用

| 依赖项 | 路径/说明 |
| --- | --- |
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| 方案1 任务（done） | `docs/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md` |
| 闸口 A 定稿 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` |
| SPEC 方案1/2 | `docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| 规则 | `.cursor/rules/10-tech-graph.mdc`、`20-tech-graph-update.mdc` |
| 图谱目录 | `docs/_tech_graph/` |
| 论文（对照） | `docs/diary/jsonPKmermaid/三相塌缩等价性论文_拓扑综合.md` |

---

## 4. 验收标准

### 4.1 工程

- [ ] `python tools/tech_graph_graph_export.py`（或 v2 脚本）生成 `graph_v2` 合规文件；`--check` 通过。  
- [ ] `python tools/tech_graph_graph_equivalence_check.py`（名待定）在 CI 或同 workflow 中 **PASS**（阈值见 §2.1）。  
- [ ] `python tools/tech_graph_graph_query.py …` 对抽样节点（如 `AUTH`、`RAG`、`E`）返回非空、可解析 JSON。  
- [ ] `pytest` 覆盖 export v2、等价检查、query 至少各 1 条失败路径 + 1 条 golden。  
- [ ] `tech_graph_contract_check.py`、manifest_check **仍独立通过**。  
- [ ] 规则 `10-tech-graph.mdc` 已更新为 **query 优先** 叙述，且与 G-END 一致。

### 4.2 闸口 B（行为 · 最低结构）

- [ ] 对比组：**现状（整包 Mermaid）** vs **方案1（整包 v1 JSON）** vs **本交付（v2 + CTX_QUERY）**。  
- [ ] 指标：典型题 **token/墙钟**、**entry/impact F1**（脚本）、**P1 Rubric 子集**（可选 3 题 × 2 人 or 单 R）。  
- [ ] 结论写清：是否推荐生产默认 **CTX_QUERY**；是否维持 `.ai.md` 为维护源。  
- [ ] 结论文档路径回填 §8。

### 4.3 签收门槛（闸口 B 通过后建议）

| 规则 | 内容 |
| --- | --- |
| **B-1** | CTX_QUERY 的 P1/P2 **不低于** 闸口 A 中 CTX_MERMAID 臂的中位数（或明确接受的差距与产品签字）。 |
| **B-2** | CTX_QUERY 的 P3/P4 **不劣于** CTX_JSON 臂（或整体 session token 中位数不升）。 |
| **B-3** | 等价检查 CI **连续绿** ≥ N PR（N 由执行帽建议，默认 5）。 |

---

## 5. failure_paths

| ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- |
| FP-1 | `.ai.md` 解析失败 | 导出非 0；行级 stderr（沿用方案1） | 修图后重试 |
| FP-2 | v2 `--check` 漂移 | 非 0；diff 摘要 | 再生成或修源 |
| FP-3 | 等价检查：锚点/边标签覆盖率低于阈值 | 非 0；列缺失 Top-N | 补 `.ai.md` 或修导出器 |
| FP-4 | query 节点不存在 | 退出码非 0；提示合法 id 样本 | 改正参数 |
| FP-5 | 仅 v1 无 v2 时强制 query | 文档要求降级策略；若 v2 缺失应 FAIL 而非静默 v1 整包 | 部署 v2 |

---

## 6. 阶段划分（建议执行顺序）

| 阶段 | 交付 | 依赖 |
| --- | --- | --- |
| **P2-0** | `graph_v2` schema 文档 + 等价检查草案 | 无 |
| **P2-1** | 导出器 v2 + CI + pytest | P2-0 |
| **P2-2** | `graph_query` CLI + 规则更新 | P2-1 |
| **P2-3** | 闸口 B 实验 + 结论文档 | P2-2 |
| **P2-4** | （可选）manifest ref、struct 切片 follow-up task | 闸口 B 结论 |

---

## 7. 与论文 / 闸口 A 的对照（给执行帽）

| 概念 | 论文 | 本 task |
| --- | --- | --- |
| 等价塌缩 | Partition(B)≡Partition(F)≡Partition(G)，ARI=1 | **v2 等价检查**：拓扑 + 锚点/语义覆盖；**非** v1 边集 alone |
| 有损投影 | BLOCKER / 度量畸变 | v1 已证不宜整包替代；v2 补锚点与 label |
| SelectEnd | τ→0 硬路由 | **graph_query** 子图，非 Softmax 读全图 |
| P3 中层不塌缩 | FFN 实验 FAIL | 不指望「换 JSON」自动改善推理；靠 **query + 输出 schema**（可链接 jsonPKmermaid 后续实验） |

---

## 8. 实现备忘（由执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| v2 schema 文档路径 | （待填） |
| 脚本路径 | （待填） |
| CI workflow | （待填） |
| 闸口 B 报告路径 | （待填） |
| freeze_id 最终值 | （待填） |

---

## 给 Cursor

`graph_v2`、`graph_query`、`scheme_2`、闸口 B、`CTX_QUERY`、G-END、机器轨、等价检查、`.ai.md` 维护源、`01_struct`、`99_spec`、`gate_ctx_ab`、`test_strategy`、`failure_paths`、`docs/_tech_graph`
