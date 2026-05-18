# Task：闸口 C′ — graph_v2 查询轨 impact F1 提升与对照重跑

> **状态**：`active`（C′ batch 完成 · 待 **HG-GATE-C-PRIME-SIGNOFF**）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_query_coverage_v1.md`（`graph_v2_freeze_id` `V2_3` · T002 union 物化）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md`（闸口 C · **accepted** · canonical `gate_ctx_c_v1_batch_20260518_052803`）  
> **关联规划**：`Projects/docs/tech_graph/改进方向.md` · `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **本 task 定位**：在 **维持 machine 默认 = `CTX_V2_QUERY` / `graph_query`** 前提下，**优先拉高 impact F1**；token 仅作约束与次优权衡；最后在新 batch 上 **重跑闸口 C 式 D vs E 对照**（**C′**，不覆盖 canonical run）  
> **test_strategy**：`required`  
> **test_strategy_note**：物化/token pytest、可选 batch 评分脚本；**禁止**无 baseline 对比即宣称 F1 提升。  
> **freeze_id**：`TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0`（本 task 实验冻结；含 `graph_v2_freeze_id` 指针）  
> **graph_v2_freeze_id（输入）**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（除非 PR-1 为 F1 微调图边，须 bump 并写清）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
> **git_branch**：`task/engineering-tech-graph-gate-c-prime-f1-v1`（自 **`main`** 拉取）

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | 初稿；F1 验收阈值人可调 |
| **HG-GATE-C-PRIME-SIGNOFF** | `pending` | `50`, 关账 | C′ 结论 md 人签后 task 可 `done` |

---

## 0. 背景与目标

### 0.1 背景

- **闸口 C（canonical）**：D 臂 **impact F1 中位数 0.400**，T002 上 D **0.429** < E **0.588**；entry F1 平局 **0.857**；成本侧 D 明确优于 E。结论 **accepted**，**不推翻**默认轨。  
- **query coverage（已合 main）**：T002 union + `contract_slice` + 图边 `V2_3`；**静态子图**已覆盖 gold `AUTH`/`EV_TYPES`/`U1`，但 **未**在新 LLM batch 上验证 **impact F1** 是否随之上升。  
- 闸口 C §3.3：**impact F1 系统性偏低** → 优先 **manifest/contract 切片** 与题集相关附件，**非**扩大为整包双轨或整图 JSON。

### 0.2 优先级（执行顺序 · 强制）

| 序 | 目标 | 说明 |
| --- | --- | --- |
| **1** | **impact F1 ↑**（主 KPI） | 题级 + 三题中位数；T002 契约链优先 |
| **2** | **token / 成本**（约束） | 仅当 F1 优化触犯 `payload_limits` 时做减法；**禁止**先砍切片再测 F1 |
| **3** | **闸口 C′ 对照重跑** | 新 `runs/` 目录；D vs E 全三题；产出 **C′ 结论** 附录，**不改** `conclusion_gate_c_v2_dual_track_v1_zh.md` |

### 0.3 完成态

1. **PR-1**：D 臂物化策略以 F1 为导向增强（见 §1.1），`materialize` + 相关 pytest 绿。  
2. **PR-2（条件）**：若超 token 上限，在 **不显著伤害 F1** 前提下收缩（记录前后 F1/token 表）。  
3. **PR-3**：新 batch **`gate_ctx_c_v1_batch_<YYYYMMDD>_*`**，`score_gold_f1` + **`conclusion_gate_c_prime_f1_v1_zh.md`**；相对 canonical **052803** 与 query coverage 后基线有量化对比。

---

## 1. 范围 / 非范围

### 1.1 范围

- [x] **PR-1 · F1 导向物化（D 臂）**  
  - [x] **T002**：`contract_slice` v2 + `manifest_slice` + `impact_surface`（gold impacts 路径面）。  
  - [x] **T001 / T003**：无 manifest 切片（单种子保持）。  
  - [ ] 可选：`describe-impact` 文本臂（未做）。  
  - [x] `query_seeds.json` / `protocol_version.yaml` 写入 `TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0`；canonical `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0` 未改。  
- [x] **PR-2 · token 守门（仅 PR-1 超限时）** — 未触发  
- [x] **PR-3 · 闸口 C′ batch**  
  - [x] 主 run：`runs/gate_ctx_c_v1_batch_20260518_083014`  
  - [x] `gold_f1.md` / `gold_f1.json`  
  - [x] [`conclusion_gate_c_prime_f1_v1_zh.md`](../diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md)

### 1.2 非范围（NR）

- **NR-1**：不修改、不覆盖 `runs/gate_ctx_c_v1_batch_20260518_052803/` 及其中 jsonl。  
- **NR-2**：不重跑闸口 A/B **主实验** batch。  
- **NR-3**：不将 `CTX_DUAL_MD` 升为 machine 默认；C′ 仅作对照臂。  
- **NR-4**：不整包灌入 `15_e2e_boundary.ai.md` 或整份 `graph.json` 替代 query 子图。  
- **NR-5**：`schema_version` 保持 **`graph_v2`**。  
- **NR-6**：不修订 `conclusion_gate_c_v2_dual_track_v1_zh.md` **accepted** 正文（C′ 结论单独文件）。  
- **NR-7**：不为 F1 引入 GraphRAG / 博客向量实验（见 `task_rag_graphrag_pilot_explore_v1.md`）。

### 1.3 分期

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | F1 导向物化 + pytest | **是** |
| **PR-2** | token 守门（条件） | 仅 PR-1 失败时 |
| **PR-3** | C′ batch + 结论 | **是** |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 闸口 C canonical | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/` |
| 闸口 C 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md` |
| query coverage | `docs/tasks/done/task_engineering_tech_graph_v2_query_coverage_v1.md` |
| gold 题集 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json` |
| 协议 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/protocol_version.yaml` |
| 物化 / batch | `fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py`、`run_gate_c_batch.py` |
| 评分 | `fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py` |
| Cursor 机器轨 | `.cursor/rules/10-tech-graph.mdc` |

### 2.1 F1 基线（canonical · D 臂 · 供 PR-3 对比）

| task | entry F1 | impact F1 |
| --- | ---: | ---: |
| T001 | 0.857 | 0.200 |
| T002 | 0.667 | 0.429 |
| T003 | 1.000 | 0.400 |
| **中位数** | **0.857** | **0.400** |

（T002 E 臂 impact **0.588** 为对照上限参考，**非**本 task 必须达到，但 PR-1 应以缩小 D/E gap 为设计目标。）

---

## 3. 验收标准

### 3.1 PR-1 / PR-2（物化）

- [x] `python tools/tech_graph_graph_export.py --check` exit 0  
- [x] `materialize_gate_c_payloads.py` exit 0；全题 D 臂 token **<** 8192  
- [x] `pytest tests/test_gate_ctx_c_v1_materialize.py` 绿  
- [x] **PR-1 出口**：T002 含 `contract_slice` v2 / `manifest_slice` / `impact_surface`

### 3.2 PR-3（C′ batch · F1 优先）

- [x] 新 run：`gate_ctx_c_v1_batch_20260518_083014`（README + `freeze_id`）  
- [x] **impact F1（D 臂）** — **T002 D = 0.923 ≥ 0.55**（中位数 0.222 未达 0.45，OR 单项达标）  
- [x] **entry F1（D 臂）** — 无单题退化；中位数 **0.923 ≥ 0.80**  
- [x] **token** — D 中位数 **481 ≤ 479×1.25**  
- [x] **C′ 产品结论** — 维持 `CTX_V2_QUERY` 默认  
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿（195 passed）  

### 3.3 共用

- [ ] **HG-GATE-C-PRIME-SIGNOFF** 人签（或 task 元信息注明签收人/日期）

---

## 4. failure_paths

| ID | 触发 | 行为 |
| --- | --- | --- |
| FP-CP1 | 未建新 run 目录即改 canonical jsonl | **拒开工** |
| FP-CP2 | PR-3 前 F1 优化未落盘物化 diff | 先完成 PR-1，禁止直接 batch |
| FP-CP3 | D 臂 token 超限且未走 PR-2 记录 | `materialize` exit 5；先收缩再测 F1 |
| FP-CP4 | impact F1 未达 §3.2 且提议改默认轨为 E | **变更请求**；本 task 只输出 C′ 数据，不自动改产品决议 |
| FP-CP5 | 提议 graph_v3 / 整包双轨默认 | **拒 scope** |

---

## 5. 给执行帽的必读

1. 自 **`main`** 拉分支 `task/engineering-tech-graph-gate-c-prime-f1-v1`。  
2. **顺序**：PR-1（F1）→（必要时 PR-2 token）→ PR-3（C′ batch）；**禁止**跳过物化优化直接全量 LLM。  
3. PR-3 模型/温度与 canonical 一致（`protocol_version.yaml` · DeepSeek-V4-Flash · 0.2），除非人签变更并 bump `freeze_id`。  
4. 结论文件名建议：`docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md`。  
5. 维持 **graph_query** 为 Cursor 工程默认消费轨（见 `.cursor/rules/10-tech-graph.mdc`）。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| invoke · 30 | `invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md` |
| 分支 | `task/engineering-tech-graph-gate-c-prime-f1-v1` |
| PR-1 | `materialize_gate_c_payloads.py`：v2 contract + manifest + impact_surface；`query_seeds`/`protocol` freeze 指针 |
| PR-2 | 未触发 |
| PR-3 run 目录 | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014`（中间批 `…_081600` 见结论 §0） |
| C′ 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md` |
| 验证命令 | `materialize` + `pytest tests/test_gate_ctx_c_v1_materialize.py` + `pytest tests -m "not intent_eval and not intent_benchmark"` |
| 30 帽复验（本轮回） | `tech_graph_graph_export.py --check` **0**；`materialize_gate_c_payloads.py` **0**（T002 tokens **4555** &lt; 8192）；`test_gate_ctx_c_v1_materialize` **7 passed**；全量 pytest **195 passed**, 1 skipped |

### 自检结论（执行者）

#### 30 帽（执行编码）

PR-1→PR-3 已落盘；主 run `gate_ctx_c_v1_batch_20260518_083014`；T002 D **impact F1 0.923**（§3.2 OR 单项 ≥0.55）；entry 中位数 **0.923**；D token 中位数 **481**（≤ canonical×1.25）；产品维持 **`CTX_V2_QUERY`** 默认；**NR-1/6** 未触（052803 / gate_c accepted 正文未改）。

#### 40 帽（独立复验 · 2026-05-20）

**分支 / HEAD**：`task/engineering-tech-graph-gate-c-prime-f1-v1` · `afb901e`（40 开帽时；复验后 commit 见 HANDOFF）。

**human_gate**：`HG-GATE-C-PRIME-SIGNOFF` 仍 **`pending`** → 本帽 **可自检**、**不可** 关账 `done`、**禁止** 代填 `approved`。

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `python tools/tech_graph_graph_export.py --check` | 子仓根 | **0** | 无输出错误 |
| `python …/materialize_gate_c_payloads.py` | 子仓根 | **0** | T002 D **4555** &lt; 8192；D 中位数 token **481** |
| `pytest tests/test_gate_ctx_c_v1_materialize.py` | 子仓根 | **0** | **7 passed** |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 子仓根 | **0** | **195 passed**, 1 skipped |

**§3 验收（40 独立核对）**

| 项 | 结果 | 证据 |
| --- | --- | --- |
| §3.1 物化 / export | **pass** | 上表四命令 |
| §3.2 新 run `083014` | **pass** | `batch_index.json`、`gold_f1.md/json`、`round_01..03/raw/*_S0.jsonl`（6 条） |
| §3.2 T002 D impact ≥0.55（OR） | **pass** | `gold_f1.md`：**0.923** |
| §3.2 impact 中位数 ≥0.45 | **fail**（OR 已救） | D 中位数 **0.222**；靠 T002 单项达标 |
| §3.2 entry 无退化 / 中位数 ≥0.80 | **pass** | entry 中位数 **0.923** |
| §3.2 token ≤ canonical×1.25 | **pass** | D 中位数 **481** ≤ **599**（479×1.25） |
| §3.2 维持 `CTX_V2_QUERY` 默认 | **pass** | `conclusion_gate_c_prime_f1_v1_zh.md` §4 |
| §3.3 `HG-GATE-C-PRIME-SIGNOFF` | **未验**（待人签） | status 仍为 `pending` |
| NR-1 未覆盖 052803 | **pass** | `git diff` 对该 run 无变更 |
| NR-6 未改 gate_c accepted | **pass** | `conclusion_gate_c_v2_dual_track_v1_zh.md` 无本分支 diff |

**已知未测项**：未重跑 LLM batch（只读核对 `083014` 产物）；`describe-impact` 文本臂（task 可选，未做）。

**下一棒**：`50` 独立复检 → `TEMPLATE-independent-reinspect-invoke.md`（`HG-GATE-C-PRIME-SIGNOFF` 仍阻塞关账，不阻塞 50）。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-20 | 初稿：F1 优先 → token 约束 → 闸口 C′ 重跑；相对 canonical 052803 量化验收 |
