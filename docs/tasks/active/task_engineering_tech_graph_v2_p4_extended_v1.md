# Task：技术图谱 — graph_v2 扩展（P2-4）与闸口 B follow-up 切片

> **状态**：`active`（**30 · P2-4a 已交付** · 可选 **4b/4c** · 待关账）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（P2-0～P2-3 · 闸口 B 已签收）  
> **终轮关账参考**：`docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_CLOSE_20260517.md`  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**；`docs/_tech_graph/graph_v2_schema.md`  
> **闸口 B follow-up（可选 · P2-4c）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` §5.4（T002 类加深 query/manifest）  
> **test_strategy**：`required`  
> **test_strategy_note**：P2-4 字段须 `tech_graph_graph_v2_schema.py` 门禁 + `export --check` + 等价 CI + `tests/test_tech_graph_graph_query.py` 单图回归；**禁止**无测试静默扩 `graphs[]`/`ref`/`kind`。  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_2`（P2-4a-2 bump；与 `fixtures/gate_ctx_ab_v1/protocol_version.yaml` · `graph_v2_freeze_id` 对齐）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`、`HANDOFF_CLOSE_TRACE.md`  
> **需求帽 invoke**：`docs/harness/invokes/invoke_20260517_10_tech-graph-v2-p4-requirements.md`

### Harness 元信息（半自动 · `post_close`）

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/engineering-tech-graph-v2-p4-extended-v1` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | **10 帽 v0.2 已结构化**；人扫 task 全文后改 `approved`，方可 **22 R1** |
| **HG-AUDIT-R1** | `approved` | `30` | R1 审查落盘、零硬阻塞后人签 |
| **HG-AUDIT-CLOSE** | `pending` | `done`, `50` | 关账签收 |

---

## 0. 背景与目标

### 0.1 背景

前置 task 已交付：**P2-0** 最小 `graph_v2`、`graph_query` CLI、**闸口 B**（`CTX_QUERY` 默认 · B-1 部分满足已人签）。CLOSE 审查明确 **P2-4**（`graphs[]`、`edges[].ref`、`nodes[].kind`、manifest↔node 互引）与 **闸口 B §5.4 follow-up** **延后至本 task**。

### 0.2 架构决议继承（前置 §0 · 仍有效）

| 决议 / 约束 | 本 task 含义 |
| --- | --- |
| **G-END-4** | 不退役 `.ai.md` 为维护源 |
| **G-END-5 / FP-5** | **禁止**默认整包 v1/v2 `graph.json` 作 query 载荷 |
| **NR-1** | **禁止**重跑闸口 A / 闸口 B **主实验**（结论以 `conclusion_gate_*` 为准） |
| **NR-2～7** | 见前置 task §0.2；含「论文 SBM 不外推」「方案3 Neo4j 单独立项」等 |

### 0.3 目标（完成态）

1. 在 **不破坏** 现有单图 `graph_query` 与等价 CI 的前提下，落地 **P2-4a** 最小可用子集（§2.1 表）。  
2. （可选 **P2-4b**）`_manifest` / `_contract` 与 graph `node id` 互引校验或文档化约定。  
3. （可选 **P2-4c**）闸口 B follow-up：T002 类契约题 — `query_seeds` 增 `upstream`/`neighbors` 组合 + 可复现说明；**不重跑** NR-1 整包对比。  
4. 更新 `graph_v2_schema.md`、等价阈值（变更须书面 + `freeze_id`）；`export --check` 与 `tech-graph.yml` **仍绿**。

---

## 1. 范围 / 非范围

### 1.1 范围

- [x] **P2-4a（必做 · 关账阻塞）**  
  - [x] **P2-4a-1** `nodes[].kind`（`flow|struct|external` · 可选 · schema 校验）  
  - [x] **P2-4a-2** `graphs[]` 多分图元数据 + 导出器（每 `*.ai.md` 一条 · `graph_id`）  
  - [x] **P2-4a-2** `edges[].ref`（`{ graph_id?, node_id }` · 与 from/to 互斥 · FP-4-2 校验）  
  - [x] `tech_graph_graph_v2_schema.py`：无 P2-4 键时 P2-0 兼容（FP-4-4）；`graph_query` 忽略 ref 边  
- [ ] **P2-4b（可选 · 不阻塞关账）**  
  - [ ] manifest↔node 互引字段或脚本校验（`_manifest.json` / `_contract_manifest.json` ↔ `nodes[].id`）  
- [ ] **P2-4c（可选 · recommended）**  
  - [ ] `gate_ctx_b_v1/query_seeds.json` 增 T002 类 `upstream`/`neighbors` 组合种子  
  - [ ] 落盘 follow-up 说明 md（**不**重跑 `run_gate_b_batch` 全 arms 对比）  
- [x] 等价门禁阈值延续；`freeze_id` bump **V2_2**（P2-4a-2）  
- [ ] `.cursor/rules/10-tech-graph.mdc` 增量（仅当消费路径变更）

### 1.2 非范围

- **闸口 A / 闸口 B 主实验重跑**（NR-1）。  
- **默认整包 v2 替 `*.ai.md` 进 prompt**（G-END-5；FP-5）。  
- **退役 `.ai.md`**（G-END-4 未满足）。  
- **方案3 Neo4j**（`改进方向.md` R2 · 单独立项）。  
- **跨会话长期记忆 / 向量库**（前置 NR-5）。  
- **`01_struct` / `99_spec` 全文并入单一 `graph.json`**（另立 struct 切片 task）。  
- **`graph_query` 默认多读分图**（P2-4a 仅扩展 schema/导出；query API **默认行为不变**，多分图消费另阶段）。

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 前置 done task | `docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md` |
| v2 schema（P2-0 基线） | `docs/_tech_graph/graph_v2_schema.md` |
| 导出 / 等价 / query | `tools/tech_graph_graph_export.py`、`tech_graph_graph_equivalence_check.py`、`tech_graph_graph_query.py`、`tools/tech_graph_graph_v2_schema.py` |
| 闸口 B follow-up 真值 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` §5.4 |
| 治理层 | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` |
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| Harness §5 | `Projects/docs/harness/HARNESS_V2_PLAN.md` §5 |

### 2.1 P2-4 字段分层（执行前真值）

| 字段/结构 | 阶段 | P2-0 现状 | P2-4 最小语义 |
| --- | --- | --- | --- |
| `graphs[]` | **4a** | **禁止出现** | 分图目录；节点/边可带 `graph_id` 或默认单图 `main` |
| `nodes[].kind` | **4a** | **禁止** | 节点类型；缺省可省略（等价 P2-0）或默认 `flow`（须在 schema 定一句） |
| `edges[].ref` | **4a** | **禁止** | 指向他图节点；与 `from`/`to` 同图边互斥规则须在 schema 写明 |
| manifest↔node | **4b** | 无 | 清单项 `node_id` 须在 `nodes[]` 存在 |
| query 加深种子 | **4c** | 已有 T001–T003 | T002 类增 `upstream`/`neighbors` 参数组合 |

**默认落盘**：仍为 `docs/_tech_graph/graph.json`，`schema_version: graph_v2`（**不**并列 `graph_p4.json`）。

### 2.2 分期与阻塞关系

```text
P2-4a（kind + graphs[] + ref + schema/导出/等价）
  ├─ 阻塞：关账工程验收、HG-AUDIT-CLOSE 前必须绿
  ├─ 阻塞：若破坏单图 graph_query → 须先修 FP-4-3 再扩展 query
  └─ 不阻塞：P2-4b / P2-4c（可并行文档，但代码依赖 4a schema）

P2-4b（manifest 互引）— 可选；依赖 4a 的 nodes[].id 稳定

P2-4c（闸口 B follow-up 种子/文档）— recommended；依赖 4a 不破坏前提下可独立 PR
```

| 阶段 | 交付 | 阻塞关账 | 备注 |
| --- | --- | --- | --- |
| **P2-4a** | schema + 导出 + 等价 + query 单图回归 | **是** | 首 PR 建议仅 4a |
| **P2-4b** | manifest↔node 校验 | 否 | 可与 4a 同 PR 或拆分 |
| **P2-4c** | query_seeds + follow-up md | 否 | **禁止** NR-1 重跑 |

---

## 3. 验收标准

### 3.1 工程（P2-4a 必达）

- [x] `schema_version` 仍为 `graph_v2`；`export --check` **PASS**（2026-05-17 · V2_2）  
- [x] `tech_graph_graph_equivalence_check.py` **PASS**（拓扑边；排除 ref）  
- [x] 无 P2-4 键时 schema 接受（FP-4-4）；含 `graphs[]`/`graph_id` 导出绿（`test_tech_graph_graph_v2_p4_export`）  
- [x] `ref` 未知节点 / ref+from 互斥非 0（`test_tech_graph_graph_v2_p4_schema`）  
- [x] `pytest tests/test_tech_graph_graph_query.py` **PASS**（单图 BFS 不变）  
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` **176 passed**（2026-05-17）

### 3.2 文档

- [x] `graph_v2_schema.md` v0.3（P2-4a 全字段）  
- [ ] task 关账 `HANDOFF_CLOSE_TRACE`（待终轮 22 CLOSE）

### 3.3 可选阶段（不阻关账）

- [ ] **P2-4b**：manifest 互引校验脚本或 pytest 用例绿  
- [ ] **P2-4c**：`query_seeds.json` 变更 + follow-up 说明（引用 §5.4，**无**新 batch 主实验）

---

## 4. failure_paths

| ID | 触发 | 行为 | 可重试 | 用户/CI 可见 |
| --- | --- | --- | --- | --- |
| FP-4-1 | P2-4 字段与 P2-0 最小集冲突、未迁移 | 等价非 0；列差异 | 修 schema/导出 | CI `equivalence` 失败 |
| FP-4-2 | `ref` 指向未知 `graph_id` / `node_id` | 校验非 0 | 修源 `.ai.md` 或导出 | `export --check` 失败 |
| FP-4-3 | `graph_query` 默认路径误读多分图或改变 hop 默认 | **禁止**合入；单图 API 不变 | 回滚 query 变更 | pytest query 失败 |
| FP-4-4 | 无 P2-4 字段时新门禁拒绝合法 P2-0 图 | 导出/校验非 0 | 修 schema 条件分支 | CI 红 |
| FP-5 | 沿用前置 | 默认 CTX 禁止整包 v1/v2 | — | 治理/规则 |

---

## 5. 给执行帽的必读列表

1. 前置 task **§0.2 NR-1～7** 仍有效；本 task **仅** 扩展 schema/导出，**不** 重开闸口主实验。  
2. **P2-0 禁止项** 仅在 **P2-4a 显式升级** `tech_graph_graph_v2_schema.py` 后解除；**禁止** 单 PR 塞满 4a+4b+4c+query 多分图。  
3. 闸口 B **§5.4** = 加深 **query 种子/文档**，非 `run_gate_b_batch` 全 arms 重跑。  
4. **merge 前** `freeze_id` bump 与 `protocol_version.yaml` · `graph_v2_freeze_id` 对齐。  
5. CLOSE 审查 follow-up 原文：`conclusion_gate_b_ctx_query_v1_zh.md` §5 项 4。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| **P2-4a-1** | `kind` 可选枚举；`tests/test_tech_graph_graph_v2_p4_schema.py` |
| **P2-4a-2** | `graphs[]` + `graph_id` 导出；`ref` 互斥校验；`graph_query` 跳过 ref 边 |
| **freeze** | `TECH_GRAPH_S2_FREEZE_20260517_V2_2` · `graph.json` 已再导出 |
| **待选** | P2-4b manifest 互引；P2-4c 闸口 B follow-up 种子 |

### 自检结论（执行者）

**自检帽 · 2026-05-17**（复核 commit `3828e0c` · freeze `TECH_GRAPH_S2_FREEZE_20260517_V2_2`）

| 命令 | cwd | 退出码 | 摘要 |
| --- | --- | --- | --- |
| `python tools/tech_graph_graph_export.py --check` | `ai-ink-brain-api-python` | **0** | 无 stderr；`graph.json` 含 `graphs[]` |
| `python tools/tech_graph_graph_equivalence_check.py` | 同上 | **0** | 拓扑/锚点阈值 PASS |
| `pytest tests/test_tech_graph_graph_v2_p4_schema.py tests/test_tech_graph_graph_v2_p4_export.py -q` | 同上 | **0** | **9 passed** |
| `pytest tests/test_tech_graph_graph_query.py -q` | 同上 | **0** | **8 passed**（FP-4-3 单图路径） |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 同上 | **0** | **176 passed**, 1 skipped |

#### 验收表（§3.1 P2-4a）

| 验收项 | 结果 | 证据 |
| --- | --- | --- |
| export `--check` | **pass** | exit 0 |
| 等价 CI | **pass** | exit 0 |
| FP-4-4 / graphs 导出 | **pass** | `test_tech_graph_graph_v2_p4_*` 9 passed |
| FP-4-2 ref 门禁 | **pass** | schema 测试含未知 ref / 互斥 |
| graph_query 回归 | **pass** | 8 passed |
| 全量 pytest | **pass** | 176 passed |

**已知未测 / 非范围**：P2-4b manifest 互引、P2-4c query_seeds follow-up、闸口 B 主实验重跑（NR-1）、`.cursor/rules` 增量。

**阶段**：**P2-4a 完成**（4a-1 + 4a-2）；**4b/4c 未做** · 关账待 **22 CLOSE** + `HANDOFF_CLOSE_TRACE`。  
**invoke**：`invoke_20260517_40_tech-graph-v2-p4-a2-self-check.md`

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 | 下一棒 |
| --- | --- | --- |
| **10 需求帽** | v0.2 | `invoke_20260517_10_…` |
| **22 R1** | 零硬阻塞 | `…_audit_R1_20260517.md` |
| **40 自检** | **2026-05-17 pass** | `invoke_20260517_40_tech-graph-v2-p4-a2-self-check.md` |
| **30 P2-4a** | **已交付** | 可选 4b/4c · 关账 **22 CLOSE** |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-17 | 初稿：P2-4 扩展 + 可选闸口 B follow-up |
| v0.2 | 2026-05-17 | **10 帽结构化**：字段分层表、分期阻塞、验收/failure_paths 可操作化 |
| v0.3 | 2026-05-17 | **30 · P2-4a-1**：kind schema + pytest + freeze V2_1 |
| v0.4 | 2026-05-17 | **30 · P2-4a-2**：graphs[]/ref/schema/导出 + freeze V2_2 |
| v0.5 | 2026-05-17 | **40 自检**：§3.1 P2-4a 全 pass（复核 3828e0c） |

---

## 给 Cursor

`P2-4`、`graphs[]`、`edges[].ref`、`nodes[].kind`、`graph_v2`、前置 task done、`HANDOFF_SEMI_AUTO`、`human_gate`、`HG-TASK-DRAFT`、`test_strategy: required`、`NR-1`
