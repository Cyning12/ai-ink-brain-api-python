# Task：技术图谱 — 机器轨升级（graph_v2 + 方案2 图查询 + 闸口 B）

> **状态**：`done（2026-05-17 验收通过）`  
> **终轮审查**：`docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_CLOSE_20260517.md`  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **前置验收**：方案1 `graph.json`（`task_engineering_tech_graph_graph_json_export_v1.md` · done）  
> **闸口 A（已完成 · 勿重复实验）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` · `accepted` — 见 **§0.2**  
> **本 task 行为实验**：仅 **闸口 B**（`CTX_QUERY` vs 整包 Mermaid / 整包 v1）— 见 §4.2、§6 P2-3  
> **产品抉择 / 治理层**（权威）：`docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` **§8.2～§8.3**  
> **理论参照**：`docs/diary/jsonPKmermaid/三相塌缩等价性论文_拓扑综合.md`（**仅治理层消费类比**；禁止外推 SBM ARI=1，见 §7）  
> **审查**：`docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md`  
> **test_strategy**：`required`  
> **test_strategy_note**：v2 等价门禁与 query API 为机器轨核心；无 pytest + 闸口 B 复现则无法证明「优化机器轨」成立。  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_0`（与 `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/protocol_version.yaml` · `graph_v2_freeze_id` 对齐）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`、`HANDOFF_CLOSE_TRACE.md`

### Harness 元信息（半自动 · `post_close`）


| 字段                | 值                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------- |
| **semi_auto**     | `true`（P2-x 段：30→40 可同 Agent 链式；**下一棒 §3 须先**落盘 `docs/harness/invokes/` 并 commit）       |
| **audit_profile** | `post_close`（闸 1：R1/R2 已落盘；闸 2：关账时 `HANDOFF_CLOSE_TRACE` + 终轮签收）                        |
| **git_branch**    | `task/engineering-tech-graph-v2-graph-query-v1`（子仓 **禁止**在 `main` 上连续 semi_auto commit） |


#### 人工闸 `human_gate`（仅人可将 `pending` 改为 `approved`）


| human_gate_id      | status     | blocks_hats  | 说明                                       |
| ------------------ | ---------- | ------------ | ---------------------------------------- |
| **HG-TASK-DRAFT**  | `approved` | `22-R1`      | 初稿 task 已人/Agent 定稿                      |
| **HG-AUDIT-R1**    | `approved` | `30`         | R1 审查已回填 v0.2；见 `…_audit_R1_20260517.md` |
| **HG-AUDIT-R2**    | `approved` | `30`         | R2 零硬阻塞；见 `…_audit_R2_20260517.md`       |
| **HG-P2-3-GATE-B** | `approved`  | `done`       | P2-3 闸口 B 报告落盘后人签（§9）                    |
| **HG-AUDIT-CLOSE** | `approved` | `done`, `50` | 终轮 CLOSE 签收（`…_audit_CLOSE_20260517.md`）     |


> Agent：**不得**代填 `approved`。下一帽 ∈ `blocks_hats` 且该闸为 `pending` 时 **拒执行**。关闭流程时产出 **执行路线与 Commit 回溯**（`HANDOFF_CLOSE_TRACE`）。

---

## 0. 架构决议（G-END）


| 决议 ID       | 内容                                                                                                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **G-END-1** | **终局**是优化 **机器轨消费**（清单 + 拓扑 + 查询），**不是**给人轨 `*.md` 再加维护负担。                                                                                                                       |
| **G-END-2** | **人读轨**：`docs/_tech_graph/*.md`（含 `00_main.md`、`10_flow_*.md` 及规范层专档）。                                                                                                           |
| **G-END-3** | **协议维护轨（短期真值）**：`*.ai.md` — Agent/协议与 **导出**；人主要在 PR diff 编辑，**非**日常扫读。                                                                                                          |
| **G-END-4** | **退役 `.ai.md` 为维护源** 仅当：(a) v2 等价验收通过；(b) 闸口 B 证 **v2+query** P1/P2 不劣 Mermaid 整包且 P3/P4 不劣基线；(c) 书面签收。**本 task 不含退役**。                                                          |
| **G-END-5** | 闸口 A **否定** v1 **整包** `graph.json` 替 `*.ai.md` 主载荷；**禁止**交付默认「只灌 v1 整图」。                                                                                                         |
| **G-END-6** | **产品抉择（2026-05-17）**：① **抗漂移** = CI + `freeze_id` + v2 **等价门禁**（非「LLM 永不犯错」）；② **token 主因** = **少读子图（query）**，非 JSON 替 Mermaid；③ **同等信息量**下 JSON≈Mermaid 对理解边际极小 — 见治理层应用文 §8.3。 |


### 0.1 轨道分层

```text
人读轨：*.md（流程人读 + 01_struct / 02_version / 99_*）
协议维护轨（短期）：*.ai.md → 导出输入
机器轨 · 清单/契约：_manifest.json · _contract_manifest.json
机器轨 · 拓扑/消费：graph_v1 → graph_v2 · graph_query（本 task）
规范层（人机同读，按需）：01_struct · 99_spec · 99_mermaid_protocol
```


| 阶段    | 机器轨形态                                                                           |
| ----- | ------------------------------------------------------------------------------- |
| **旧** | manifest + contract + **整包** `.ai.md` 或 v1 `graph.json`                         |
| **新** | manifest + contract + **v2** + `**graph_query`**；`.ai.md` 仍为 export 源直至 G-END-4 |


### 0.2 闸口分工与防重复（Agent / 任务帽必读）

> **闸口** = 阶段对比实验门闸（`[docs/tech_graph/改进方向.md](../../../../docs/tech_graph/改进方向.md)` **R4**），与 CI（`export --check`、manifest、contract）**分工不同**：CI 证「仓库真值不漂」；闸口证「Agent 用法是否净收益」。

#### 闸口 A vs 本 task（闸口 B）


| 闸口    | 方案                                | 状态            | 真值文档                                                                                                         | 本 task 是否重做                 |
| ----- | --------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------- |
| **A** | 方案1 · `graph_v1` 整包 vs 整包 Mermaid | **已完成**       | `[conclusion_gate_ctx_ab_final_zh.md](../../diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md)` | **否** — 结论沿用，禁止当作本 task 主实验 |
| **B** | 方案2 · **v2 + `CTX_QUERY`**        | **本 task 交付** | §9 回填路径                                                                                                      | **是** — §4.2、P2-3           |


**闸口 A 已采纳结论（勿再争论，除非新 freeze + 新协议版本 + 新 task）：**

- 主载荷 token **~1:1**；**不签收**「一律 `graph.json` 整包替 `*.ai.md`」。  
- v1 为**有损投影**；P1/P2 **偏 Mermaid**；省钱/省时不能靠**换格式读同样多**。  
- 详见治理层应用文 `[治理层三相塌缩_Ink技术图谱应用.md](../../diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md)` **§8.2～§8.3**。

#### 禁止重复立项 / 重复实验（除非书面新开 task 并 bump 协议）


| ID       | 禁止项                                                 | 原因               | 应做替代                          |
| -------- | --------------------------------------------------- | ---------------- | ----------------------------- |
| **NR-1** | 再跑一轮「整包 CTX_JSON vs 整包 CTX_MERMAID」并当作**本 task**主结论 | 闸口 A 已覆盖         | 闸口 B：**CTX_QUERY** 臂          |
| **NR-2** | 把 **v1 整包** `graph.json` 定为生产 Agent **默认主载荷**       | G-END-5、闸口 A     | **graph_query** + manifest 切片 |
| **NR-3** | 以「JSON 替 `.ai.md` 提升 LLM 理解/记忆」为**本 task 目标**       | 同等信息量下边际极小（§8.3） | 优化**机器轨消费**与**少读子图**          |
| **NR-4** | 用论文 SBM **ARI=1** 证明 Ink 图已等价                       | §7 禁止外推          | 本仓 **等价检查阈值**（§2.1）           |
| **NR-5** | 在本 task 做**跨会话长期记忆**（向量库、β 摘要策略等）                   | §2.2 非范围         | **另立 task**；图谱只服务慢变真值 + 当轮 α  |
| **NR-6** | P2-0 实现 `graphs[]`、`edges[].ref`                    | R1 延后至 P2-4      | §2.1 P2-0 最小集                 |
| **NR-7** | 再开「三文件 = 论文三相 B/F/G」论证而不做等价/query                   | 概念混用             | 治理层应用文 §2「工程三相」               |


#### 闸口 / CI / Harness 索引（防漂移）


| 类型           | 路径                                                                          |
| ------------ | --------------------------------------------------------------------------- |
| 闸口 A 定稿      | `docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md`       |
| 闸口 A 收口（工作区） | `docs/harness/tasks/done/task_engineering_tech_graph_gate_a_closeout_v1.md` |
| 闸口 B（待填）     | §9 · `docs/diary/jsonPKmermaid/` 或 `docs/tech_graph/`                       |
| 改进方向 R4      | `docs/tech_graph/改进方向.md`                                                   |
| 治理层抉择        | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md`                             |


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

- 落盘 **graph_v2 schema 草案**（`docs/_tech_graph/graph_v2_schema.md` + `tools/tech_graph_graph_v2_schema.py`）。  
- **落盘策略（默认）**：**同路径** `docs/_tech_graph/graph.json`，`schema_version: graph_v2`。  
- 升级 `tools/tech_graph_graph_export.py`：自 `*.ai.md` 导出 **P2-0 最小 v2**（委托 `build_reference_graph_v2`）。  
- `tools/tech_graph_graph_equivalence_check.py`：参考 vs 导出；阈值 95%/90%；重复拓扑边 multiset 匹配（P2-1 修复）。  
- pytest（export v2 golden / 等价 PASS+失败 / FP-5）；`tech-graph.yml` 接入 v2 等价 step。

**P2-0 最小字段集（单图扁平 · 首版必达）**


| 字段/结构                                           | P2-0   | 说明                                |
| ----------------------------------------------- | ------ | --------------------------------- |
| `schema_version` / `generated_at` / `freeze_id` | **必**  | 与方案1 CI 惯例一致                      |
| `nodes[]` · `id`                                | **必**  | query 主键                          |
| `nodes[]` · `label`                             | **必**  | 补闸口 A 节点语义缺口                      |
| `nodes[]` · `kind`                              | 延后     | → P2-4                            |
| `edges[]` · `from` / `to`                       | **必**  | 同 v1                              |
| `edges[]` · `mark`                              | **必**  | 协议边标记（`->`、`[ok]`、`::branches` 等） |
| `edges[]` · `type` / `sync`                     | **必**  | 与 v1 分类兼容                         |
| `edges[]` · `label`                             | **必**  | HTTP 路径等，避免纯 `depends_on`         |
| `edges[]` · `anchors[]`                         | **必**  | `{ "path", "symbol", "line"? }`   |
| **物化顺序**                                        | **建议** | 节点/边 **稳定排序**（缓解表示畸变，见论文 P1 精神）   |


**P2-4 / follow-up 延后（禁止 P2-0 依赖）**


| 字段/结构                         | 说明                             |
| ----------------------------- | ------------------------------ |
| `graphs[]` 多分图                | v1 已扁平合并；首版 query 用单图 k-hop 即可 |
| `edges[].ref`                 | 依赖分图；首版用 depth 查询代替跨图硬引用       |
| `nodes[].kind`                | 非等价/BFS 必需                     |
| manifest · `graph_node_id` 互引 | 另 follow-up                    |


#### B. graph_query（方案2）

- `tools/tech_graph_graph_query.py`：加载 **v2** `graph.json`（v1 仅文档化降级，**禁止**静默整包 v1 进 prompt）。  
- 最小查询：`downstream(id, depth)`、`upstream(id, depth)`、`neighbors(id)`；返回可序列化子图 + anchors。  
- CLI 示例：`python tools/tech_graph_graph_query.py downstream AUTH 2`  
- 更新 `.cursor/rules/10-tech-graph.mdc`：**query 优先**；禁止默认整包 v1。  
- MCP：**非**本 task 阻塞验收。

#### C. Agent 加载顺序（写入规则或 PROJECT_CONFIG 指针）

```text
graph_query(…) → _manifest 切片 → _contract（若 SSE）
→ 按需 01_struct → 按需 99_spec
→ 按需 10_flow_*.ai.md 片段（query 不足时）
```

#### D. 闸口 B

- 落盘闸口 B 报告（`docs/diary/jsonPKmermaid/` 或 `docs/tech_graph/`）。  
- arm `**CTX_QUERY**` = v2 query 结果 + manifest/contract（**非**整包 v2 文件）。  
- 对比组见 §4.2；主结论**不复测** v1 整包替 Mermaid（A/B 引用闸口 A）。

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


| 依赖项             | 路径                                                                                             |
| --------------- | ---------------------------------------------------------------------------------------------- |
| PROJECT_CONFIG  | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`                                          |
| 方案1（done）       | `docs/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md`                          |
| 闸口 A            | `docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md`                          |
| **治理层应用（产品抉择）** | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md`                                                |
| 机器轨 SPEC 草案     | `docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md`          |
| SPEC 1/2        | `docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`query_graph/scheme_2_graph_query.md` |
| 规则              | `.cursor/rules/10-tech-graph.mdc`、`20-tech-graph-update.mdc`                                   |
| 审查 R1           | `docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R1_20260517.md`      |


---

## 4. 验收标准

### 4.1 工程

- 导出 `graph.json`（`schema_version: graph_v2`）且 `--check` 通过。  
- 等价检查 CI **PASS**（§2.1 阈值）。  
- `graph_query` 对 `AUTH` / `RAG` / `E` 返回非空 JSON。  
- pytest：export v2、等价检查、query 各 ≥1 golden + 1 失败路径。  
- manifest_check、contract_check **仍独立绿**（P2-2 执行帽未单独复跑）。  
- `10-tech-graph.mdc` 与 G-END 一致。

### 4.2 闸口 B（最低结构）


| 组     | 内容                                             |
| ----- | ---------------------------------------------- |
| **A** | 整包 CTX_MERMAID（基线）                             |
| **B** | 整包 v1 CTX_JSON（对照 · 已证不宜默认）                    |
| **C** | **CTX_QUERY**（v2 query 输出 + manifest/contract） |


- 指标：token/墙钟、entry/impact F1（`score_gold_f1`）、P1 Rubric 子集（≥3 题，审查帽定样本量）。  
- 结论：是否推荐默认 **CTX_QUERY**；是否维持 `.ai.md` 为 export 源。  
- 路径回填 §9。

### 4.3 签收门槛（闸口 B 后）


| 规则      | 内容                                                      |
| ------- | ------------------------------------------------------- |
| **B-1** | CTX_QUERY 的 P1/P2 **≥** 闸口 A CTX_MERMAID 臂中位数（或书面接受差距）。 |
| **B-2** | CTX_QUERY 的 P3/P4 **不劣于** CTX_JSON（session 中位数）。        |
| **B-3** | 等价检查 CI 连续绿 ≥ **5** PR（可调，记入 §9）。                       |


---

## 5. failure_paths


| ID   | 触发              | 行为                      | 可重试         |
| ---- | --------------- | ----------------------- | ----------- |
| FP-1 | `.ai.md` 解析失败   | 非 0；行级 stderr           | 修图          |
| FP-2 | v2 `--check` 漂移 | 非 0；diff 摘要             | 再生成/修源      |
| FP-3 | 等价阈值未达          | 非 0；缺失锚点 Top-N          | 补 ai.md/导出器 |
| FP-4 | query 未知节点      | 非 0；示例 id 列表            | 改参          |
| FP-5 | 无 v2 却走 query   | **FAIL**；禁止降级为整包 v1 作默认 | 部署 v2       |


---

## 6. 阶段划分


| 阶段       | 交付                                                   | 依赖   |
| -------- | ---------------------------------------------------- | ---- |
| **P2-0** | **最小 v2** schema 文档 + 等价检查草案（**无** `graphs[]`/`ref`） | —    |
| **P2-1** | 导出器 v2 + CI + pytest（`graph.json` 升 `graph_v2`）      | P2-0 |
| **P2-2** | `graph_query` CLI + 规则                               | P2-1 |
| **P2-3** | 闸口 B + 结论文档                                          | P2-2 |
| **P2-4** | `graphs[]`、`ref`、`kind`、manifest↔node 互引、struct 切片   | 闸口 B |


---

## 7. 论文 / 闸口 A / 治理层（执行帽必读）


| 概念            | 说明                                                        |
| ------------- | --------------------------------------------------------- |
| **禁止外推**      | 论文定理 4.1（SBM ARI=1）**不**等于 Ink 图已等价；Ink 只验收 §2.1 阈值。      |
| **有损 v1**     | 闸口 A 已否定整包 v1 替 Mermaid。                                  |
| **SelectEnd** | `graph_query` 子图，非读全图。                                    |
| **P3 中层**     | 不指望换格式；闸口 B 可链后续 **输出 schema** 实验（非本 task 阻塞）。            |
| **工程三相**      | 传播=query；结构=拓扑+manifest；约束=spec/contract 按需 — 见治理层应用文 §2。 |


---

## 8. 给执行帽的必读列表

1. 治理层应用文 **§8.2～§8.3**（产品抉择）。
2. 本 task **§2.1 P2-0** — **禁止** P2-0 实现 `graphs[]`/`ref`。
3. 默认 **同文件** `graph.json` + `schema_version: graph_v2`。
4. `tech_graph_contract_check` 与 graph 导出 **并行**，禁止合并。
5. 闸口 B 必含 **CTX_QUERY** 臂。

---

## 9. 实现备忘（执行 Agent 回填）


| 项                | 内容                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| v2 schema 路径     | `docs/_tech_graph/graph_v2_schema.md`；校验 `tools/tech_graph_graph_v2_schema.py`                                                 |
| 参考图构建            | `tools/tech_graph_graph_v2_reference.py`（自 `*.ai.md`）                                                                          |
| 等价检查脚本           | `tools/tech_graph_graph_equivalence_check.py`（`--check`；v1 已提交 → **FP-5** 退出码 5）                                               |
| pytest           | `tests/test_tech_graph_graph_v2_equivalence.py`（8 项：schema 禁止字段、参考 golden、等价指标、FP-5、合成 v2 PASS）                                |
| query 脚本         | `tools/tech_graph_graph_query.py`（`load_graph_v2`；`downstream`/`upstream`/`neighbors`；FP-4=4、FP-5=5）                           |
| pytest P2-2      | `tests/test_tech_graph_graph_query.py`（golden + FP-4/FP-5 + 仓内 AUTH/RAG/E + CLI）                                               |
| invoke（执行 P2-2）  | `docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-2-exec.md`                                                           |
| invoke（自检 P2-2）  | `docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-2-self-check.md`                                                     |
| 闸口 B 报告          | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md`                                                        |
| gate B fixtures  | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_b_v1/`                                                                             |
| gate B batch run | `docs/diary/jsonPKmermaid/runs/gate_ctx_b_v1_batch_20260517_095228/`                                                           |
| invoke（执行 P2-3）  | `docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-3-gate-b-exec.md`                                                    |
| invoke（自检 P2-3）  | `docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-3-self-check.md`                                                     |
| freeze_id        | `TECH_GRAPH_S2_FREEZE_20260517_V2_0` · `protocol_version.yaml` · `graph_v2_freeze_id`                                          |
| 导出器 v2           | `tools/tech_graph_graph_export.py` → `build_reference_graph_v2`；`FREEZE_ID` 同上                                                 |
| CI               | `.github/workflows/tech-graph.yml`：`export --check` + `tech_graph_graph_equivalence_check.py`（manifest/contract 仍独立）           |
| pytest P2-1      | `tests/test_tech_graph_graph_export.py`（v2 golden、FP-2 漂移）；`tests/test_tech_graph_graph_v2_equivalence.py`（+committed v2 PASS） |
| invoke（执行 P2-1）  | `docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-1-exec.md`                                                           |
| invoke（自检 P2-1）  | `docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-1-self-check.md`                                                     |
| invoke（执行 P2-0）  | `docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-0-exec.md`                                                           |
| invoke（自检 P2-0）  | `docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-0-self-check.md`                                                     |


**P2-3 已做**：闸口 B 报告 + batch run（见上表）。**P2-4 未做**：`graphs[]` / `edges[].ref`。

---

### 自检结论（执行者）


| 项                  | 结果                                                                          |
| ------------------ | --------------------------------------------------------------------------- |
| **执行日**            | 2026-05-17                                                                  |
| **阶段**             | **P2-3 自检签收**（闸口 B 证据核对 · **pass**）                                         |
| **invoke（自检）**     | `docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-3-self-check.md`  |
| **invoke（执行）**     | `docs/harness/invokes/invoke_20260517_30_tech-graph-v2-p2-3-gate-b-exec.md` |
| **闸口 B 报告**        | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md`     |
| **batch run**      | `docs/diary/jsonPKmermaid/runs/gate_ctx_b_v1_batch_20260517_095228/`        |
| **HG-P2-3-GATE-B** | **`approved`**（人签 2026-05-17 · 接受 B-1 部分满足 + §5 决议）                      |
| **P2-2 签收**        | **pass**（`invoke_20260517_40_tech-graph-v2-p2-2-self-check.md`）             |


**验证命令**（子仓根 `ai-ink-brain-api-python` · **40 自检帽复跑**）：

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
```


| 命令                | cwd                       | 退出码   | 摘要                                            |
| ----------------- | ------------------------- | ----- | --------------------------------------------- |
| 全量 pytest（VERIFY） | `ai-ink-brain-api-python` | **0** | `167 passed, 1 skipped, 2 deselected`（11.25s） |


**闸口 B 工件核对（只读 · 与执行帽一致）**


| 核对项                                          | 结果       | 证据                                                                                                                                       |
| -------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `materialize_report.json` · CTX_QUERY 非整包 v2 | **pass** | `forbidden_checks.CTX_QUERY_not_whole_graph_v2: true`；`CTX_QUERY_uses_graph_query_cli: true`；启发式 tokens 中位数 **427**（整包 Mermaid **5026**） |
| batch 3× `parse_ok`                          | **pass** | `round_01`/`02`/`03` 各 `index.json` → `arms[0].parse_ok: true`；`gold_f1.json` 同                                                          |
| F1 与报告 §2 一致                                 | **pass** | `gold_f1.md`：T001 ep **0.857**/imp **0.200**；T002 **0.667**/**0.286**；T003 **1.000**/**0.267**                                           |
| CTX_QUERY 载荷为子图非整包                           | **pass** | 各题 `*.subgraph.json`（如 T002：7 nodes / 8 edges）；**非**默认整包 v1/v2                                                                           |


**验收表（§4.1 / §4.2 / §4.3 · 仅有证据项）**


| 区块   | 验收项                                      | pass/fail            | 证据                                                                                                                                                 |
| ---- | ---------------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| §4.1 | 工程项（导出/等价/query/pytest/规则）               | **pass**             | VERIFY 含 `test_tech_graph_graph_`*；执行帽 P2-0～P2-2 已签收                                                                                               |
| §4.1 | manifest_check、contract_check 独立复跑       | **未测**               | 本帽未单独执行；CI 仍独立 step（与 P2-2 自检相同缺口）                                                                                                                 |
| §4.2 | 三组 A/B/C、指标、结论、§9 路径                     | **pass**             | 报告 §0–§5；batch `batch_index.json`                                                                                                                  |
| §4.2 | CTX_QUERY = query 子图 + manifest/contract | **pass**             | `materialize_report` + 子图路径                                                                                                                        |
| §4.3 | **B-1** P1/P2 ≥ 闸口 A Mermaid 中位数         | **部分满足**             | entry F1 中位数 **0.857** vs Mermaid **0.939**（略低）；T001/T003 单题达标；impact F1 **0.267** vs **0.340** 系统性偏低 → 报告 §3 建议加深 hop / manifest 切片，**非**整包 v2 默认 |
| §4.3 | **B-2** P3/P4 不劣 CTX_JSON                | **P3 pass / P4 未全胜** | total tokens 中位数 **5992** vs JSON **12159**；墙钟中位数 **46.6s**（报告 §2.2）                                                                               |
| §4.3 | **B-3** 等价 CI 连续绿 ≥5 PR                  | **工程已绿 · 计数待关账**     | pytest + `tech-graph.yml` equivalence PASS；「连续 5 PR」留终轮统计                                                                                          |
| §4.2 | 推荐默认 **CTX_QUERY**                       | **建议采纳**             | 报告 §5；维持 `*.ai.md` export 源                                                                                                                        |


**自检裁定**：P2-3 **pass**（工程 VERIFY + 闸口 B 报告/batch 路径与数值可复现核对一致）。

**关账（2026-05-17）**：`HG-P2-3-GATE-B` 已人签；终轮 **`…_audit_CLOSE_20260517.md`** + `HANDOFF_CLOSE_TRACE`；task 归档 **`docs/tasks/done/`**。

**已知未测（不阻关闭）**：manifest/contract 脚本未在 40 帽单跑（CI 独立 step）；Phase·P1 双人盲审未重跑（NR-1）；B-3「连续 5 PR」留 merge 后统计。

---

## 10. 审查与交接（Harness）


| 轮次          | 状态                                | 下一棒                                                                                                     |
| ----------- | --------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **R1**      | 已审查；B-D1=§2.1 过重 → **本版已按 R1 回填** | —                                                                                                       |
| **R2**      | 已审查（零硬阻塞）                         | 见 `docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md`             |
| **P2-0 执行** | 已落盘草案                             | invoke：`invoke_20260517_30_tech-graph-v2-p2-0-exec.md`                                                  |
| **P2-0 自检** | **pass**                          | invoke：`invoke_20260517_40_tech-graph-v2-p2-0-self-check.md`                                            |
| **P2-1 执行** | 已落盘                               | invoke：`invoke_20260517_30_tech-graph-v2-p2-1-exec.md`                                                  |
| **P2-1 自检** | **pass**                          | invoke：`invoke_20260517_40_tech-graph-v2-p2-1-self-check.md`                                            |
| **P2-2 执行** | 已落盘                               | invoke：`invoke_20260517_30_tech-graph-v2-p2-2-exec.md`                                                  |
| **P2-2 自检** | **pass**                          | invoke：`invoke_20260517_40_tech-graph-v2-p2-2-self-check.md`                                            |
| **P2-3 执行** | 已落盘                               | invoke：`invoke_20260517_30_tech-graph-v2-p2-3-gate-b-exec.md`；报告 `conclusion_gate_b_ctx_query_v1_zh.md` |
| **P2-3 自检** | **pass**                          | invoke：`invoke_20260517_40_tech-graph-v2-p2-3-self-check.md`                                            |
| **终轮 CLOSE**  | **签收**                            | `…_audit_CLOSE_20260517.md` · invoke `invoke_20260517_22_tech-graph-v2-close.md`                         |
| **关闭回溯**    | **已落盘**                           | 见终轮审查 **「执行路线与 Commit 回溯」**                                                                      |


工作区 invoke（R2 发起用）：`docs/harness/invokes/invoke_20260517_22_tech-graph-v2-task-audit-r2.md`（相对聚合仓 `Projects/`）  
**半自动字段**：见文首 **Harness 元信息**；真值 `[HANDOFF_SEMI_AUTO.md](../../../../docs/harness/prompts/HANDOFF_SEMI_AUTO.md)`

---

## 修订记录


| 版本   | 日期         | 说明                                                                                                     |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------ |
| v0.1 | 2026-05-17 | 初稿                                                                                                     |
| v0.2 | 2026-05-17 | **按审查 R1 回填**：P2-0/P2-4 字段分层；`graph.json` 升版默认；G-END-6；治理层链；长期记忆非范围；§10 交接                             |
| v0.3 | 2026-05-17 | **§0.2** 闸口 A/B 分工与 NR-1～7 防重复清单                                                                       |
| v0.4 | 2026-05-17 | 文首 **Harness 元信息**：`semi_auto`、`audit_profile: post_close`、`human_gate` 表、`git_branch`；§10 交接与 P2-2 状态 |
| v1.0 | 2026-05-17 | **关账**：P2-3 自检 + 闸口 B 人签；终轮 CLOSE；归档 `done/` |


---

## 给 Cursor

`graph_v2`、`P2-0`、`graph_query`、`CTX_QUERY`、闸口 A 已完成、闸口 B、NR-1`、`§0.2`、勿重复 gate_ctx_ab、G-END-6、治理层应用、query 优先、`docs/_tech_graph`、`semi_auto`、`human_gate`、`HG-AUDIT-R2`、`audit_profile`、`HANDOFF_SEMI_AUTO`