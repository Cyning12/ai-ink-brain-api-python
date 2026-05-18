# Task：技术图谱 — graph_v2 查询可达性优化（闸口 C follow-up）

> **状态**：`done（2026-05-19 · graph_v2 查询可达性 follow-up · 50 关账）`  
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

- [x] **PR-1 · 图真值**  
  - [x] export：`00_main.ai.md` 增 `U1↔U2`、`U1/U2→AUTH`、`U2→EV_TYPES`；`graph_v2_freeze_id=TECH_GRAPH_S2_FREEZE_20260519_V2_3`  
  - [x] `python tools/tech_graph_graph_export.py --check`  
  - [x] 相关 pytest（`test_tech_graph_graph_export.py` 等）  
- [x] **PR-2 · 查询与物化**  
  - [x] `query_seeds.json`：T002 `queries[]` union（downstream/upstream/neighbors）  
  - [x] `materialize_gate_c_payloads.py`：`_merge_subgraphs` + T002 `contract_slice`  
  - [x] `pytest tests/test_gate_ctx_c_v1_materialize.py` 扩展（T002 gold + freeze）  
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

- [x] `graph.json` 通过 v2 校验且 `--check` 绿  
- [x] T002 gold 节点（`U2`/`U1`/`AUTH`/`EV_TYPES`）在 v2 上 **BFS** 可核对（`test_t002_subgraph_covers_gold_graph_ids`）  

### 3.2 PR-2

- [x] `materialize_gate_c_payloads.py` → exit 0；T002 D 臂 **3494** tokens **<** 8192  
- [x] T002 载荷含 `AUTH`、`EV_TYPES`、`U1`（union 17 nodes）+ `contract_slice`  
- [x] `pytest tests/test_gate_ctx_c_v1_materialize.py` 绿  

### 3.3 共用

- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（195 passed）  

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
| 分支 | `task/engineering-tech-graph-v2-query-coverage-v1` |
| PR-1 | `docs/_tech_graph/00_main.ai.md`（U1↔U2、AUTH、EV_TYPES 边）；`graph.json` freeze `TECH_GRAPH_S2_FREEZE_20260519_V2_3`；`tools/tech_graph_graph_export.py` FREEZE_ID |
| PR-2 | `query_seeds.json`（T002 `queries[]`）；`materialize_gate_c_payloads.py`（union + contract_slice）；`protocol_version.yaml` graph_v2_freeze_id |
| 物化 | T002 D 臂 3494 tokens / 17 nodes；已重写 `fixtures/gate_ctx_c_v1/payloads/CTX_V2_QUERY/T002_*.subgraph.json` 与 `materialize_report.json` |
| 测试 | `tests/test_gate_ctx_c_v1_materialize.py` 增 T002 gold、coverage freeze 断言 |
| PR-3 | 未做（可选；不阻塞） |
| 验证命令 | `tech_graph_graph_export.py --check` exit 0；materialize exit 0；pytest 195 passed |

### 自检结论（执行者）

**40 帽 · 2026-05-19** · invoke：`docs/harness/invokes/invoke_20260519_37_tech-graph-v2-query-coverage-40-self-check.md`  
**cwd**：`ai-ink-brain-api-python` · **分支**：`task/engineering-tech-graph-v2-query-coverage-v1` · **diff 基线**：`main...HEAD`（实现 `05c1b39` · 含 40 落盘 `ab187fa`）

#### 命令与退出码

| # | 命令 | 退出码 | 输出要点 |
| --- | --- | ---: | --- |
| 1 | `python tools/tech_graph_graph_export.py --check` | 0 | 无 stderr；v2 export 校验通过 |
| 2 | `python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py` | 0 | T002 D 臂：`nodes=17`，`heuristic_tokens=3494`（&lt; 8192）；`OK: …/materialize_report.json` |
| 3 | `pytest tests/test_gate_ctx_c_v1_materialize.py tests/test_tech_graph_graph_export.py tests/test_tech_graph_graph_query.py -q` | 0 | **31 passed** in 0.53s |
| 4 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | **195 passed**, 1 skipped, 2 deselected in 64.74s |

#### 验收 pass/fail（对照 §3）

| 验收项 | 结果 | 证据 |
| --- | --- | --- |
| §3.1 `graph.json` + `--check` 绿 | **pass** | 命令 #1 exit 0 |
| §3.1 T002 gold（U2/U1/AUTH/EV_TYPES）BFS 可核对 | **pass** | 命令 #3 含 `test_t002_subgraph_covers_gold_graph_ids` |
| §3.2 materialize exit 0；T002 tokens &lt; 8192 | **pass** | 命令 #2：3494 tokens |
| §3.2 T002 含 AUTH/EV_TYPES/U1 + union 17 nodes + contract_slice | **pass** | 命令 #2/#3 materialize 与 `test_gate_ctx_c_v1_materialize.py` |
| §3.2 `test_gate_ctx_c_v1_materialize.py` 绿 | **pass** | 命令 #3 |
| §3.3 全量 pytest 仍绿 | **pass** | 命令 #4：195 passed |
| §1.1 PR-3（可选消融） | **未测** | task 声明不阻塞；保持 `[ ]` |

#### 已知未测 / 阻塞

- **PR-3**：T002 消融 dry-run / 新 batch — 非阻塞，未执行（符合 task §1.3）。
- **NR-1/2**：未重跑闸口 A/B/C 主 batch（符合非范围）。

**40 帽结论**：PR-1/PR-2 验收项 **全部 pass**；可交 **50 复检帽**。

#### 50 帽（关账 · 独立复检 · 2026-05-19）

**human_gate**：无 `blocks_hats` 含 `50` 且 `pending` → 可开工。  
**PR**：[#33](https://github.com/Cyning12/ai-ink-brain-api-python/pull/33) **MERGED** → `origin/main` `71eff22`；CI pytest / tech-graph / contract / verify **SUCCESS**。

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | `ai-ink-brain-api-python` | **0** | **195 passed**, 1 skipped, 2 deselected (~70s) |
| `pytest tests/test_tech_graph_graph_export.py tests/test_tech_graph_graph_query.py tests/test_gate_ctx_c_v1_materialize.py -q` | 同上 | **0** | **31 passed** in 0.58s |
| `python tools/tech_graph_graph_export.py --check` | 同上 | **0** | v2 export 校验通过 |
| `python …/materialize_gate_c_payloads.py` | 同上 | **0** | T002 D：**17 nodes** · **3494** tokens；`graph_v2_freeze_id` **V2_3** |

| 验收项（§3） | pass/fail | 证据 |
| --- | --- | --- |
| §3.1 PR-1 graph + `--check` | **pass** | `FREEZE_ID` `TECH_GRAPH_S2_FREEZE_20260519_V2_3` · `protocol_version.yaml` L8 |
| §3.1 T002 gold BFS | **pass** | `test_t002_subgraph_covers_gold_graph_ids` |
| §3.2 materialize + T002 载荷 | **pass** | `materialize_report.json` T002 · 3494 &lt; 8192 |
| §3.3 共用 pytest | **pass** | 195 passed |
| §1.1 PR-3（可选） | **open** | 非阻塞；保持 `[ ]` |
| NR-1/2/3/6 | **pass** | 未重跑 A/B/C batch；未改 `conclusion_gate_c` **accepted** |
| 闸口 C §3.3 follow-up 意图 | **pass** | 图可达 + union 物化；**维持** query machine 默认 |

**§3 验收摘要（50 帽）**：PR-1/PR-2 **pass** · PR-3 **open（非阻塞）** · **已合并 #33** · **建议流程关闭**。  
**关闭回溯**：`docs/harness/invokes/invoke_20260519_39_tech-graph-v2-query-coverage-50-close.md`

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 | 路径 |
| --- | --- | --- |
| **30** | PR-1/2 完成 | `docs/harness/invokes/invoke_20260519_36_tech-graph-v2-query-coverage-execute.md` |
| **40** | 独立复验 pass | `docs/harness/invokes/invoke_20260519_37_tech-graph-v2-query-coverage-40-self-check.md` |
| **50** | 关账 · task `done` | `docs/harness/invokes/invoke_20260519_39_tech-graph-v2-query-coverage-50-close.md` |

**配对 PR**：子仓 [#33](https://github.com/Cyning12/ai-ink-brain-api-python/pull/33)（已合并）；工作区 P3 [#1](https://github.com/Cyning12/cyning-ink-workspace/pull/1)（可选并行）。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-19 | 初稿：闸口 C follow-up · 图可达性 + query/materialize |
| v1.0 | 2026-05-19 | **关账**：#33 合并；50 复检；归档 `done/` |
