# Task：闸口 C′ — graph_v2 查询轨 impact F1 提升与对照重跑

> **状态**：`draft`  
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

- [ ] **PR-1 · F1 导向物化（D 臂）**  
  - [ ] **T002**：在现有 `contract_slice` 上，按 `tasks.json` gold **impact** 字段补 **SSE / unified chat 契约段**（`_contract_manifest.json` 定向切片，非整文件）。  
  - [ ] **T001 / T003**：评估是否需 **manifest 切片**（embedding / ingest 相关条目）；无 gold 收益则保持单种子。  
  - [ ] 可选：对单题试用 `describe-impact` **文本臂** 与 JSON 子图 **并列**（须 pytest 与 token 门禁）；默认仍以子图 + 切片为主。  
  - [ ] 更新 `query_seeds.json` / `protocol_version.yaml` 中 **本 task `freeze_id`** 指针；**不**改 canonical `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0`。  
- [ ] **PR-2 · token 守门（仅 PR-1 超限时）**  
  - [ ] 每题 D 臂 `heuristic_tokens` **<** `max_heuristic_tokens_per_task_arm`（8192）且 **<** `d_arm_nodes_lt_whole_mermaid_heuristic_tokens`（5026）。  
  - [ ] 收缩顺序建议：`contract_slice` 字段裁剪 → union 深度 `-1` → 最后才减 `queries[]` 臂（**须记录 F1 变化**）。  
- [ ] **PR-3 · 闸口 C′ batch**  
  - [ ] `materialize_gate_c_payloads.py` → `run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD`（**非 dry_run** 或按成本先 1 题 smoke 再全量，写入 run README）。  
  - [ ] `score_gold_f1.py` → run 内 `gold_f1.md` / `gold_f1.json`。  
  - [ ] 结论 md：相对 **052803** 的 Δimpact F1、Δentry F1、Δtokens；**产品决议是否维持 D 默认**（仅当 E 在 **impact+entry 双维度** 显著优于 D 且 token 不可接受时才建议讨论改默认——预期 **维持**）。

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

- [ ] `python tools/tech_graph_graph_export.py --check` exit 0（若未改图）  
- [ ] `python …/materialize_gate_c_payloads.py` exit 0；全题 D 臂 token **<** 8192  
- [ ] `pytest tests/test_gate_ctx_c_v1_materialize.py` 绿（含 T002 `contract_slice`/gold 相关断言，按实现扩展）  
- [ ] **PR-1 出口**：相对 **post-coverage 物化**（当前 main 载荷），T002 D 臂 payload 已含 **可追踪的契约/manifest 切片变更**（代码或配置说明）

### 3.2 PR-3（C′ batch · F1 优先）

- [ ] 新 run 目录已生成且 README 含复现命令 + **`freeze_id`**  
- [ ] **impact F1（D 臂）**  
  - [ ] 三题 **中位数 ≥ 0.45**（较 canonical **+0.05**），或  
  - [ ] **T002 D impact F1 ≥ 0.55**（较 canonical T002 **+0.12**）  
- [ ] **entry F1（D 臂）**：任题相对 canonical **下降 ≤ 0.05**；三题中位数 **≥ 0.80**  
- [ ] **token（次优）**：D 臂静态 token 中位数 **≤** canonical D **× 1.25**（约 **600** 上限量级）；若超出须 PR-2 记录取舍表  
- [ ] **C′ 产品结论**：新 md 写明 **是否维持** B/C 的 **`CTX_V2_QUERY` 默认**（预期：**维持**）；若 E 仅在 T002 impact 更高，须写清 **不构成** 改默认依据  
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿  

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
| invoke · 30 | （待填） |
| 分支 | |
| PR-1 | |
| PR-2 | |
| PR-3 run 目录 | |
| C′ 结论 | |
| 验证命令 | |

### 自检结论（执行者）

（40 帽回填）

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-20 | 初稿：F1 优先 → token 约束 → 闸口 C′ 重跑；相对 canonical 052803 量化验收 |
