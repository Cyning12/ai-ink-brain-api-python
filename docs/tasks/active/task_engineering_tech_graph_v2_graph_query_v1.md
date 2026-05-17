# Task：技术图谱 — 机器轨升级（graph_v2 + 方案2 图查询 + 闸口 B）

> **状态**：`draft`（**按审查 R1 回填** · 待 **R2 任务审核** 后再交执行帽）  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **前置验收**：方案1 `graph.json`（`task_engineering_tech_graph_graph_json_export_v1.md` · done）；闸口 A（`docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` · accepted）  
> **产品抉择 / 治理层**（权威）：`docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` **§8.2～§8.3**  
> **理论参照**：`docs/diary/jsonPKmermaid/三相塌缩等价性论文_拓扑综合.md`（**仅治理层消费类比**；禁止外推 SBM ARI=1，见 §7）  
> **审查**：`docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md`  
> **test_strategy**：`required`  
> **test_strategy_note**：v2 等价门禁与 query API 为机器轨核心；无 pytest + 闸口 B 复现则无法证明「优化机器轨」成立。  
> **freeze_id**（草案）：`TECH_GRAPH_S2_FREEZE_TBD`（merge 前与 `fixtures/gate_ctx_ab_v1/protocol_version.yaml` 对齐 bump）

---

## 0. 架构决议（G-END）

| 决议 ID | 内容 |
| --- | --- |
| **G-END-1** | **终局**是优化 **机器轨消费**（清单 + 拓扑 + 查询），**不是**给人轨 `*.md` 再加维护负担。 |
| **G-END-2** | **人读轨**：`docs/_tech_graph/*.md`（含 `00_main.md`、`10_flow_*.md` 及规范层专档）。 |
| **G-END-3** | **协议维护轨（短期真值）**：`*.ai.md` — Agent/协议与 **导出**；人主要在 PR diff 编辑，**非**日常扫读。 |
| **G-END-4** | **退役 `.ai.md` 为维护源** 仅当：(a) v2 等价验收通过；(b) 闸口 B 证 **v2+query** P1/P2 不劣 Mermaid 整包且 P3/P4 不劣基线；(c) 书面签收。**本 task 不含退役**。 |
| **G-END-5** | 闸口 A **否定** v1 **整包** `graph.json` 替 `*.ai.md` 主载荷；**禁止**交付默认「只灌 v1 整图」。 |
| **G-END-6** | **产品抉择（2026-05-17）**：① **抗漂移** = CI + `freeze_id` + v2 **等价门禁**（非「LLM 永不犯错」）；② **token 主因** = **少读子图（query）**，非 JSON 替 Mermaid；③ **同等信息量**下 JSON≈Mermaid 对理解边际极小 — 见治理层应用文 §8.3。 |

### 0.1 轨道分层

```text
人读轨：*.md（流程人读 + 01_struct / 02_version / 99_*）
协议维护轨（短期）：*.ai.md → 导出输入
机器轨 · 清单/契约：_manifest.json · _contract_manifest.json
机器轨 · 拓扑/消费：graph_v1 → graph_v2 · graph_query（本 task）
规范层（人机同读，按需）：01_struct · 99_spec · 99_mermaid_protocol
```

| 阶段 | 机器轨形态 |
| --- | --- |
| **旧** | manifest + contract + **整包** `.ai.md` 或 v1 `graph.json` |
| **新** | manifest + contract + **v2** + **`graph_query`**；`.ai.md` 仍为 export 源直至 G-END-4 |

---

## 1. 背景与目标

方案1 提供 **graph_v1**（有损拓扑投影）与 CI `--check`。闸口 A 表明：主载荷 token **~1:1**；v1 **有损**；**不签收**一律 JSON 主载荷。

本 task：**不**以「JSON 替换 `.ai.md` 提升 LLM 理解」为目标（治理层 §8.3）。目标是：

1. **graph_v2（P2-0 最小集）**：单图扁平 + **anchors / mark / label**，等价门禁；  
2. **graph_query**：确定性子图消费（SelectEnd 类比）；  
3. **闸口 B**：`CTX_QUERY` vs 整包 Mermaid / 整包 v1。

---

## 2. 范围 / 非范围

### 2.1 范围

#### A. graph_v2 schema 与导出

- [ ] 落盘 **graph_v2 schema 草案**（工作区 SPEC 或本仓 `docs/_tech_graph/` 旁）。  
- [ ] **落盘策略（默认，执行可偏离须 PR 说明）**：**同路径** `docs/_tech_graph/graph.json`，`schema_version: graph_v2`；**不**默认并列 `graph_v2.json`。CI `--check` 在过渡期可对比 v1→v2 迁移说明（见 §6 P2-1）。  
- [ ] 升级 `tools/tech_graph_graph_export.py`（或 v2 脚本）：自 `*.ai.md` 导出 **P2-0 最小 v2**。  
- [ ] `tools/tech_graph_graph_equivalence_check.py`：参考图（自 `.ai.md` 解析）vs 导出 v2 — **拓扑一致** + 锚点行覆盖率 ≥ **95%**（边 `label` 覆盖率 PR 可单列阈值，建议 ≥ 90%）。  
- [ ] pytest + `tech-graph.yml` 接入 v2 / 等价检查。

**P2-0 最小字段集（单图扁平 · 首版必达）**

| 字段/结构 | P2-0 | 说明 |
| --- | --- | --- |
| `schema_version` / `generated_at` / `freeze_id` | **必** | 与方案1 CI 惯例一致 |
| `nodes[]` · `id` | **必** | query 主键 |
| `nodes[]` · `label` | **必** | 补闸口 A 节点语义缺口 |
| `nodes[]` · `kind` | 延后 | → P2-4 |
| `edges[]` · `from` / `to` | **必** | 同 v1 |
| `edges[]` · `mark` | **必** | 协议边标记（`->`、`[ok]`、`::branches` 等） |
| `edges[]` · `type` / `sync` | **必** | 与 v1 分类兼容 |
| `edges[]` · `label` | **必** | HTTP 路径等，避免纯 `depends_on` |
| `edges[]` · `anchors[]` | **必** | `{ "path", "symbol", "line"? }` |
| **物化顺序** | **建议** | 节点/边 **稳定排序**（缓解表示畸变，见论文 P1 精神） |

**P2-4 / follow-up 延后（禁止 P2-0 依赖）**

| 字段/结构 | 说明 |
| --- | --- |
| `graphs[]` 多分图 | v1 已扁平合并；首版 query 用单图 k-hop 即可 |
| `edges[].ref` | 依赖分图；首版用 depth 查询代替跨图硬引用 |
| `nodes[].kind` | 非等价/BFS 必需 |
| manifest · `graph_node_id` 互引 | 另 follow-up |

#### B. graph_query（方案2）

- [ ] `tools/tech_graph_graph_query.py`：加载 **v2** `graph.json`（v1 仅文档化降级，**禁止**静默整包 v1 进 prompt）。  
- [ ] 最小查询：`downstream(id, depth)`、`upstream(id, depth)`、`neighbors(id)`；返回可序列化子图 + anchors。  
- [ ] CLI 示例：`python tools/tech_graph_graph_query.py downstream AUTH 2`  
- [ ] 更新 `.cursor/rules/10-tech-graph.mdc`：**query 优先**；禁止默认整包 v1。  
- [ ] MCP：**非**本 task 阻塞验收。

#### C. Agent 加载顺序（写入规则或 PROJECT_CONFIG 指针）

```text
graph_query(…) → _manifest 切片 → _contract（若 SSE）
→ 按需 01_struct → 按需 99_spec
→ 按需 10_flow_*.ai.md 片段（query 不足时）
```

#### D. 闸口 B

- [ ] 落盘闸口 B 报告（`docs/diary/jsonPKmermaid/` 或 `docs/tech_graph/`）。  
- [ ] arm **`CTX_QUERY`** = v2 query 结果 + manifest/contract（**非**整包 v2 文件）。  
- [ ] 对比组见 §4.2；主结论**不复测** v1 整包替 Mermaid。

### 2.2 非范围

- 方案3 Neo4j（**R2** 未满足）。  
- 本阶段退役 `*.ai.md` 或删人读 `10_flow_*.md`。  
- `01_struct` / `99_spec` **全文并入** 单一 `graph.json`（可另立 `struct.json` follow-up）。  
- **跨会话长期记忆**（向量记忆、会话摘要产品、S1/S2 β 策略优化）— **单独立项**；本 task 仅优化 **慢变图谱真值 + 当轮 α 裁剪**（治理层 §8A）。  
- 改写 `99_mermaid_protocol.md` 语义。  
- 前端仓（另 task）。  
- 合并 `tech_graph_contract_check` 与 graph 导出。

---

## 3. 依赖与引用

| 依赖项 | 路径 |
| --- | --- |
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| 方案1（done） | `docs/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md` |
| 闸口 A | `docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` |
| **治理层应用（产品抉择）** | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` |
| 机器轨 SPEC 草案 | `docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md` |
| SPEC 1/2 | `docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`query_graph/scheme_2_graph_query.md` |
| 规则 | `.cursor/rules/10-tech-graph.mdc`、`20-tech-graph-update.mdc` |
| 审查 R1 | `docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md` |

---

## 4. 验收标准

### 4.1 工程

- [ ] 导出 `graph.json`（`schema_version: graph_v2`）且 `--check` 通过。  
- [ ] 等价检查 CI **PASS**（§2.1 阈值）。  
- [ ] `graph_query` 对 `AUTH` / `RAG` / `E` 返回非空 JSON。  
- [ ] pytest：export v2、等价检查、query 各 ≥1 golden + 1 失败路径。  
- [ ] manifest_check、contract_check **仍独立绿**。  
- [ ] `10-tech-graph.mdc` 与 G-END 一致。

### 4.2 闸口 B（最低结构）

| 组 | 内容 |
| --- | --- |
| **A** | 整包 CTX_MERMAID（基线） |
| **B** | 整包 v1 CTX_JSON（对照 · 已证不宜默认） |
| **C** | **CTX_QUERY**（v2 query 输出 + manifest/contract） |

- [ ] 指标：token/墙钟、entry/impact F1（`score_gold_f1`）、P1 Rubric 子集（≥3 题，审查帽定样本量）。  
- [ ] 结论：是否推荐默认 **CTX_QUERY**；是否维持 `.ai.md` 为 export 源。  
- [ ] 路径回填 §9。

### 4.3 签收门槛（闸口 B 后）

| 规则 | 内容 |
| --- | --- |
| **B-1** | CTX_QUERY 的 P1/P2 **≥** 闸口 A CTX_MERMAID 臂中位数（或书面接受差距）。 |
| **B-2** | CTX_QUERY 的 P3/P4 **不劣于** CTX_JSON（session 中位数）。 |
| **B-3** | 等价检查 CI 连续绿 ≥ **5** PR（可调，记入 §9）。 |

---

## 5. failure_paths

| ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- |
| FP-1 | `.ai.md` 解析失败 | 非 0；行级 stderr | 修图 |
| FP-2 | v2 `--check` 漂移 | 非 0；diff 摘要 | 再生成/修源 |
| FP-3 | 等价阈值未达 | 非 0；缺失锚点 Top-N | 补 ai.md/导出器 |
| FP-4 | query 未知节点 | 非 0；示例 id 列表 | 改参 |
| FP-5 | 无 v2 却走 query | **FAIL**；禁止降级为整包 v1 作默认 | 部署 v2 |

---

## 6. 阶段划分

| 阶段 | 交付 | 依赖 |
| --- | --- | --- |
| **P2-0** | **最小 v2** schema 文档 + 等价检查草案（**无** `graphs[]`/`ref`） | — |
| **P2-1** | 导出器 v2 + CI + pytest（`graph.json` 升 `graph_v2`） | P2-0 |
| **P2-2** | `graph_query` CLI + 规则 | P2-1 |
| **P2-3** | 闸口 B + 结论文档 | P2-2 |
| **P2-4** | `graphs[]`、`ref`、`kind`、manifest↔node 互引、struct 切片 | 闸口 B |

---

## 7. 论文 / 闸口 A / 治理层（执行帽必读）

| 概念 | 说明 |
| --- | --- |
| **禁止外推** | 论文定理 4.1（SBM ARI=1）**不**等于 Ink 图已等价；Ink 只验收 §2.1 阈值。 |
| **有损 v1** | 闸口 A 已否定整包 v1 替 Mermaid。 |
| **SelectEnd** | `graph_query` 子图，非读全图。 |
| **P3 中层** | 不指望换格式；闸口 B 可链后续 **输出 schema** 实验（非本 task 阻塞）。 |
| **工程三相** | 传播=query；结构=拓扑+manifest；约束=spec/contract 按需 — 见治理层应用文 §2。 |

---

## 8. 给执行帽的必读列表

1. 治理层应用文 **§8.2～§8.3**（产品抉择）。  
2. 本 task **§2.1 P2-0** — **禁止** P2-0 实现 `graphs[]`/`ref`。  
3. 默认 **同文件** `graph.json` + `schema_version: graph_v2`。  
4. `tech_graph_contract_check` 与 graph 导出 **并行**，禁止合并。  
5. 闸口 B 必含 **CTX_QUERY** 臂。

---

## 9. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| v2 schema 路径 | （待填） |
| 等价检查脚本 | （待填） |
| query 脚本 | （待填） |
| 闸口 B 报告 | （待填） |
| freeze_id | （待填） |

---

## 10. 审查与交接（Harness）

| 轮次 | 状态 | 下一棒 |
| --- | --- | --- |
| **R1** | 已审查；B-D1=§2.1 过重 → **本版已按 R1 回填** | — |
| **R2** | **待** | **任务审核帽** `22-task-audit`：对照 R1 清单勾选 §2.1 分层、落盘默认、G-END-6、非范围记忆；无硬阻塞后再交 **执行帽** P2-0 |

工作区 invoke（R2 发起用）：`docs/harness/invokes/invoke_20260517_22_tech-graph-v2-task-audit-r2.md`（相对聚合仓 `Projects/`）

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-17 | 初稿 |
| v0.2 | 2026-05-17 | **按审查 R1 回填**：P2-0/P2-4 字段分层；`graph.json` 升版默认；G-END-6；治理层链；长期记忆非范围；§10 交接 |

---

## 给 Cursor

`graph_v2`、`P2-0`、`graph_query`、`CTX_QUERY`、G-END-6、治理层应用、R1 回填、等价检查、query 优先、长期记忆非范围、`docs/_tech_graph`
