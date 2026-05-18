# Task：技术图谱 — graph_v2 查询可达性优化（闸口 C follow-up）

> **状态**：`active`（v0.1 初稿 · 待 30 执行）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md`（闸口 C · accepted）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（闸口 B · CTX_QUERY 默认）  
> **关联规划**：`Projects/docs/tech_graph/改进方向.md` · `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **本 task 定位**：在 **不推翻闸口 B/C 产品决议** 前提下，提升 **graph_v2 + graph_query** 对题集 gold 的可达性（**T002 优先**）  
> **test_strategy**：`required`  
> **test_strategy_note**：export `--check`、graph_query pytest、gate_ctx_c materialize 扩展须同 PR 可失败再绿。  
> **freeze_id**：`TECH_GRAPH_QUERY_COVERAGE_FREEZE_20260519_V1_0`（本 task 工程冻结；图内容快照见 `graph_v2_freeze_id`）  
> **graph_v2_freeze_id（目标）**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（PR-1 落地后写入 `graph.json`）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
> **git_branch**：`task/engineering-tech-graph-v2-query-coverage-v1`（自 `main` 拉取；**勿**基于 `task/engineering-tech-graph-gate-c-p3-docs-v1`）

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | 初稿后人可扫；已预填 approved 便于 30 接力 |
| **HG-AUDIT-R1** | `approved` | `30` | 继承闸口 C 范围；无新实验门闸 · 仅工程 follow-up |

> **并行**：闸口 C **P3 文档**在分支 `task/engineering-tech-graph-gate-c-p3-docs-v1` 执行；本 task **不改** `Projects/docs/tech_graph/改进方向.md` 闸口 C 表（除非人签合并后另 PR）。

---

## 0. 背景与目标

### 0.1 背景

闸口 **C** 已签收（`conclusion_gate_c_v2_dual_track_v1_zh.md` · **accepted**）：**machine 默认维持** `graph_query` / `CTX_V2_QUERY`；**不采纳** 精选双轨 `CTX_DUAL_MD` 作默认。  

闸口 C §3.3 follow-up 指出：T002 上 D 臂子图 **缺** gold 中的 `AUTH`、`EV_TYPES`、U1 姊妹入口等——根因是 **v2 图可达性 + 单种子 `downstream(U2)`**，非「应改默认轨」。

### 0.2 与闸口 A/B/C 的关系

| 闸口 / 线 | 本 task |
| --- | --- |
| **A / B** | **禁止**重跑主实验（**NR-1**、**NR-2**） |
| **C 结论** | **禁止**改 `accepted` 正文；可选 PR-3 新 batch 目录做 **C′ 消融**，不覆盖 `gate_ctx_c_v1_batch_20260518_052803` |
| **P3 文档** | 另一分支；本 task **不替代** P3 |

### 0.3 目标（完成态）

1. **PR-1**：`graph.json`（仍 `schema_version: graph_v2`）补 T002 相关 **边/锚点/ref**，`tech_graph_graph_export.py --check` 绿，新 `graph_v2_freeze_id`。  
2. **PR-2**：`gate_ctx_c_v1/query_seeds.json` 支持 **多查询 union**；`materialize_gate_c_payloads.py` 合并子图 + 可选 **SSE contract/manifest 小切片**；pytest 覆盖 T002 载荷含 gold 关键 `graph_id`/锚点。  
3. **PR-3（可选）**：T002 × D 臂 dry-run 或文档说明「须新 batch + 新 freeze」；**不阻塞** PR-1/2 合并。

---

## 1. 范围 / 非范围

### 1.1 范围

- [ ] **PR-1 · 图真值**  
  - [ ] export：`U2` ↔ `EV_TYPES`（`15_e2e_boundary`）、`AUTH`（`chatbi_principal`）、`U1` 姊妹入口可达（边或 `ref` + `anchors`，以 export 规则为准）  
  - [ ] `python tools/tech_graph_graph_export.py --check`  
  - [ ] 相关 pytest（`test_tech_graph_graph_export.py` 等）  
- [ ] **PR-2 · 查询与物化**  
  - [ ] `query_seeds.json`：T002 多查询（示例：`downstream(U2,2)` + `upstream(U2,1)` + `neighbors(U2)`；协议 token 上限内）  
  - [ ] `materialize_gate_c_payloads.py`：子图并集去重；可选契约切片 + anchor 索引块  
  - [ ] `pytest tests/test_gate_ctx_c_v1_materialize.py` 扩展（T002）  
- [ ] **PR-3（可选）**  
  - [ ] T002 消融说明或 dry-run jsonl（**新** run 目录）  

### 1.2 非范围（NR）

- **NR-1 / NR-2**：不重跑闸口 A/B（及 C）**主实验**、不改历史 `runs/gate_ctx_*` 目录内容。  
- **NR-3**：不将 `CTX_DUAL_MD` 升为 machine 默认。  
- **NR-4**：不整包灌入 `15_e2e_boundary.ai.md` 替代 query 子图。  
- **NR-5**：`schema_version` 保持 **`graph_v2`**；若 breaking → 另立项 graph_v3，本 task 拒扩 scope。  
- **NR-6**：不改闸口 C **accepted** 结论；不抢 P3 分支的 `改进方向.md` / README 闸口 C 表（除非人签合并协调）。

### 1.3 分期

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | 图 export + freeze | **是** |
| **PR-2** | query_seeds + materialize + pytest | **是** |
| **PR-3** | 可选消融 | **否** |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 闸口 C 结论 · follow-up | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md` §3.3 |
| 闸口 B 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` |
| 题集 gold | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json` |
| gate_ctx_c 协议 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/protocol_version.yaml` |
| export / query | `tools/tech_graph_graph_export.py`、`tools/tech_graph_graph_query.py` |
| graph_v2 | `docs/_tech_graph/graph.json` |
| 治理层 | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` |

---

## 3. 验收标准

### 3.1 PR-1

- [ ] `graph.json` 通过 v2 校验且 `--check` 绿  
- [ ] T002 gold 节点（`U2`/`U1`/`AUTH`/`EV_TYPES`）在 v2 上 **BFS/ref/anchors** 可核对（脚本或 pytest 断言）  

### 3.2 PR-2

- [ ] `materialize_gate_c_payloads.py` → exit 0；T002 D 臂 heuristic tokens **<** `protocol_version.yaml` `payload_limits`  
- [ ] T002 载荷含 `AUTH`、`EV_TYPES`、U1 相关锚点或 `graph_id`（与 `tasks.json` gold 对齐）  
- [ ] `pytest tests/test_gate_ctx_c_v1_materialize.py` 绿  

### 3.3 共用

- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿  

---

## 4. failure_paths

| ID | 触发 | 行为 |
| --- | --- | --- |
| FP-QC-1 | 误重跑闸口 A/B/C 主 batch | **拒开工** |
| FP-QC-2 | export `--check` 失败 | 先修图/源 `.ai.md`，不改 query 配方 |
| FP-QC-3 | materialize token 超上限 | 缩小 union 或契约切片，禁止整包双轨 |
| FP-QC-4 | 提议 graph_v3 breaking | **变更请求**，不本 task 静默扩 scope |

---

## 5. 给执行帽的必读

1. 自 **`main`** 拉分支 `task/engineering-tech-graph-v2-query-coverage-v1`。  
2. **勿**与 P3 文档分支混改。  
3. 优先 **T002**；T001/T003 若无回归可保持单种子。  
4. 结论 **维持** 闸口 C：**query 默认、双轨按需**。  

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| invoke · 30 | `docs/harness/invokes/invoke_20260519_36_tech-graph-v2-query-coverage-execute.md` |

### 自检结论（执行者）

（30 / 40 帽回填）

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-19 | 初稿：闸口 C follow-up · 图可达性 + query/materialize |
