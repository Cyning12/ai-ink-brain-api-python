# Task：技术图谱 — 闸口 C 对比实验（graph_v2 查询轨 vs 双轨原文）

> **状态**：`done（2026-05-18 · 闸口 C 实验收口 · 50 关账）`  
> **P2 结论（accepted）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md`  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（闸口 B · `CTX_QUERY`）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_scheme2_completion_v1.md`（`has_path` / `describe_impact`）  
> **关联规划**：`Projects/docs/tech_graph/改进方向.md` **v1.1.3** **R4**；`scheme_2_graph_query.md`  
> **本 task 定位**：**闸口 C**（新协议 · 非重跑闸口 A/B 主实验）  
> **test_strategy**：`required`  
> **test_strategy_note**：新 `fixtures/gate_ctx_c_v1/` 须可 materialize + 至少 1 题 dry-run；pytest 覆盖 payload 构建与 query 种子；LLM batch 可 Phase 分步。  
> **freeze_id**：`TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0`（[`protocol_version.yaml`](../diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/protocol_version.yaml)）  
> **gates_before_code**：`failure_paths`、`test_strategy`、`freeze_id`、§0.3 实验臂定义、§1.2 NR 清单  
> **Harness 通则**：`Projects/docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
> **需求帽 invoke**：`docs/harness/invokes/invoke_20260518_10_tech-graph-gate-c-v2-dual-track-requirements.md`  
> **git_branch**：`task/engineering-tech-graph-gate-c-v2-dual-track-v1`

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | 本 v0.1 初稿后人扫 |
| **HG-AUDIT-R1** | `approved` | `30` | R1 零硬阻塞后人签执行 |
| **HG-P0-PROTOCOL** | `approved` | `30` | `gate_ctx_c_v1` 协议 + 题集人签 |
| **HG-GATE-C-SIGNOFF** | `approved` | `done`, `50` | 实验结论人签 |

---

## 0. 背景与目标

### 0.1 背景

闸口 **A**（整包 Mermaid vs v1 JSON）与闸口 **B**（+ `CTX_QUERY` 子图）已归档。尚未在 **同一题集** 下对比：

- **臂 D · `CTX_V2_QUERY`**：`graph_v2` + `tech_graph_graph_query` 子图（含 `describe_impact` / `downstream` 等，与闸口 B 一致但 **freeze 与协议版本独立**）；  
- **臂 E · `CTX_DUAL_MD`**：按需选取的 **`*.ai.md` + 配对 `*.md` 双轨原文**（人读轨 + 协议轨，**非**整仓 seven 文件灌入）。

本 task **立项并跑通闸口 C**，回答：在影响分析类任务上，**v2 查询轨**相对 **双轨原文** 是否在 token/正确性/可复现上净收益。

### 0.2 与闸口 A/B 的关系（必读）

| 闸口 | 状态 | 本 task |
| --- | --- | --- |
| **A** | `conclusion_gate_ctx_ab_final_zh.md` · accepted | **禁止**重跑为主结论（**NR-1**） |
| **B** | `conclusion_gate_b_ctx_query_v1_zh.md` · accepted | **禁止**重跑 `gate_ctx_b_v1` 全 arms（**NR-2**） |
| **C（本 task）** | 未做 | **新** `gate_ctx_c_v1`；主对比 **D vs E**；可 **引用** A/B 题集 `tasks.json` |

### 0.3 实验臂定义（v0.1 锁定 · R1 可审不可默改）

| 臂 ID | 代号 | 主载荷 | 说明 |
| --- | --- | --- | --- |
| **D** | `CTX_V2_QUERY` | `graph_v2` 子图 JSON + query 元数据 | 由 `query_seeds.json` 驱动 `downstream`/`describe-impact`；**`ref` 边不参与** |
| **E** | `CTX_DUAL_MD` | 选定图的 `10_flow_*.ai.md` **+** 同 stem 的 `10_flow_*.md`（若存在） | **非**整包 `docs/_tech_graph/*.ai.md`；由 `dual_track_manifest.json` 列出路径 |
| — | （对照引用） | `CTX_MERMAID` / `CTX_JSON` | 仅 **引用** 闸口 A/B 历史 run；**本 task 不新跑** 除非人签扩容 scope |

**题集**：默认复用 `fixtures/gate_ctx_ab_v1/tasks.json`（T001～T003）；每题绑定 D/E 的 materialize 规则。

### 0.4 目标（完成态）

1. **P0**：`fixtures/gate_ctx_c_v1/`（`protocol_version.yaml`、`tasks.json` 或链出、`query_seeds.json`、`dual_track_manifest.json`、materialize 脚本）。  
2. **P1**：至少 1 次 **可复现 batch**（允许 S0 单段先行）+ `runs/gate_ctx_c_v1_batch_*`。  
3. **P2**：定稿 `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md`。  
4. **P3（recommended）**：同步 `改进方向.md` 增 **闸口 C** 行 + §2.7 文档勾选维护（**非**阻塞 P2）。

---

## 1. 范围 / 非范围

### 1.1 范围

- [x] **P0 · 协议与 fixture**  
  - [x] `gate_ctx_c_v1/protocol_version.yaml`（`freeze_id`、图路径、`graph_v2_freeze_id` 引用）  
  - [x] `dual_track_manifest.json`（每题列出 `.ai.md` + `.md` 路径，上限 token 预算写明）  
  - [x] `materialize_gate_c_payloads.py`（输出 D/E 主载荷；报告 `materialize_report.json`）  
  - [x] `query_seeds.json`（对齐 v2 真值节点，**禁止**沿用已废弃示例 `AUTH→RAG` 若生产图无边）  
- [x] **P1 · batch**  
  - [x] 复用或薄封装既有 batch runner（与 `gate_ctx_b_v1` 同型入口，新 protocol id）  
  - [x] S0 段 3 题 × 2 臂（D、E）最低跑通  
- [x] **P2 · 结论**  
  - [x] 轴：token（主载荷）、影响集抽样 F1/人工表、wall（可选）  
  - [x] 链 `conclusion_gate_b` / `conclusion_gate_ctx_ab` 作背景，**不**推翻 B 已采纳的 CTX_QUERY 默认  
- [x] **P3 · 文档（recommended）**  
  - [x] `改进方向.md` 对比实验表增 **闸口 C**  
  - [x] `docs/tech_graph/tasks/ai-ink-brain-api-python/README.md` 索引  

### 1.2 非范围

- **闸口 A/B 主实验重跑**（**NR-1**、**NR-2**）。  
- **方案3 Neo4j**、**退役 `.ai.md`**（G-END-4）。  
- **`graph_v2` schema 语义变更**。  
- **MCP stdio 服务**（后置；见 scheme2 completion §8 **F-mcp**）。  
- **§2.7 本地/Agent 冒烟**（**F-2.7-local/agent** · 另 task，不阻塞本实验）。  
- **前端子仓** graph 实验（默认仅后端 `docs/_tech_graph/`；前端 CI 另 task）。

### 1.3 分期

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | P0 + materialize pytest | **是** |
| **PR-2** | P1 batch + P2 报告 | **是** |
| **PR-3** | P3 文档 | **否** |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 闸口 A 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md` |
| 闸口 B 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` |
| 题集（复用） | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json` |
| B materialize 参考 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_b_v1/scripts/materialize_gate_b_payloads.py` |
| 查询真值 | `tools/tech_graph_graph_query.py` |
| graph_v2 | `docs/_tech_graph/graph.json` |
| 治理层 | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` §8 |

---

## 3. 验收标准

### 3.1 P0

- [x] `python …/materialize_gate_c_payloads.py` → exit 0；D/E payload 目录非空  
- [x] pytest 覆盖：manifest 路径存在、query 种子节点在 `graph_v2` 中存在、D 臂子图节点数 < 整包 Mermaid 阈值（阈值写入 protocol）

### 3.2 P1

- [x] `runs/gate_ctx_c_v1_batch_*` 含 `batch_index.json` + 每题 raw jsonl（canonical：`gate_ctx_c_v1_batch_20260518_052803`）  
- [x] 复现命令写入 batch `README` / `batch_index.reproduce_commands`（供 P2 报告 §0 引用）

### 3.3 P2

| 验收项 | 40 帽 | 说明 |
| --- | --- | --- |
| 结论报告 `accepted` 且 §0～§3 与证据链数字一致 | **pass** | 50 帽只读核对；人改 `accepted` |
| 明确 D vs E 胜负与 Agent 默认轨建议 | **pass** | 报告 §3；维持 B 的 CTX_QUERY |
| `accepted` + 关账 | **pass** | **HG-GATE-C-SIGNOFF** `approved` + 50 帽 |

- [x] `conclusion_gate_c_v2_dual_track_v1_zh.md` 状态 `accepted`（人签 · 2026-05-18）  
- [x] 明确 **D vs E** 胜负与是否建议调整 Agent 默认消费轨（见报告 §3；**维持** B 的 CTX_QUERY 默认）

### 3.3 共用

- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（实验代码不破坏主链）

---

## 4. failure_paths

| ID | 触发 | 行为 |
| --- | --- | --- |
| FP-C-1 | 误将本 task 当作闸口 B 重跑 | **拒开工**（改 task） |
| FP-C-2 | `dual_track_manifest` 含不存在路径 | materialize exit 非 0 |
| FP-C-3 | query 种子节点不在 graph_v2 | exit 4 对齐 FP-4 |
| FP-C-4 | D/E 主载荷 token 超 protocol 上限 | materialize 失败并报告 |
| FP-C-5 | 无 LLM API key 跑 batch | P1 阻塞；P0 仍可验收 |

---

## 5. 给执行帽的必读

1. **新协议目录** `gate_ctx_c_v1`，**勿**覆盖 `gate_ctx_ab_v1` / `gate_ctx_b_v1` 历史 run。  
2. **CTX_DUAL_MD** = **精选**双轨文件，非整仓 `.ai.md` 打包。  
3. **query 种子**须对照当前 `graph.json` 真值节点（如 `ENV`/`C1`/`U2`）。  
4. batch 模型/温度与 B 对齐除非 protocol 显式变更。  
5. **HG-P0-PROTOCOL** 未 approved 时仅可做 P0 草案，**不得**跑付费 batch。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| P0 fixture | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/`（protocol、seeds、manifest、`tasks_ref.json`） |
| materialize | `fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py` → `payloads/CTX_V2_QUERY/*.subgraph.json`、`CTX_DUAL_MD/*.dual_track.md` |
| pytest | `tests/test_gate_ctx_c_v1_materialize.py`（5 项） |
| 30 invoke P0 | `docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-v2-dual-track-execute.md` |
| 30 invoke P1 | `docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-p1-batch.md` |
| P1 runner | `run_s0_gate_c.py`、`run_gate_c_batch.py`（schema `gate_ctx_c_*`） |
| P1 batch run | `runs/gate_ctx_c_v1_batch_20260518_052803/`（`dry_run: false`，含 `gold_f1.json`） |
| P1 pytest | `tests/test_gate_ctx_c_v1_batch.py`（4 项 dry-run / 臂映射） |

### 自检结论（执行者）

#### PR-1（P0）

- **命令**：`python …/materialize_gate_c_payloads.py` → **exit 0**；D 臂 median heuristic tokens **479**（< 5026）。  
- **命令**：`pytest tests/test_gate_ctx_c_v1_materialize.py` → **5 passed**。  
- **阻塞**：无；§3.1 满足。

#### PR-2（P1 · batch · 30 帽交付）

- **命令**：`pytest tests/test_gate_ctx_c_v1_batch.py` → **4 passed**；`pytest tests -m "not intent_eval and not intent_benchmark"` → **193 passed**, 1 skipped。  
- **命令**：`RUBRIC_REVIEW_BACKEND=siliconflow python …/run_gate_c_batch.py` → **exit 0**；canonical run **`gate_ctx_c_v1_batch_20260518_052803`**（3 题 × `CTX_V2_QUERY` + `CTX_DUAL_MD`，`batch_index.json` + 6× `raw/*_S0.jsonl` + `gold_f1.json`）。  
- **复现**：见 run `README.md` / `batch_index.reproduce_commands`（模型 **DeepSeek-V4-Flash** · **0.2**）。  
- **范围**：未改 `gate_ctx_ab_v1` / `gate_ctx_b_v1` 历史 run；未调用 `run_gate_b_batch`。  

#### 40 帽（PR-2 · 独立复验 · 2026-05-18）

**human_gate**：无 `blocks_hats` 含 `40` 且 `pending` 的闸；可开工。

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `pytest tests/test_gate_ctx_c_v1_materialize.py -q` | `ai-ink-brain-api-python` | **0** | **5 passed** in 0.15s |
| `pytest tests/test_gate_ctx_c_v1_batch.py -q` | 同上 | **0** | **4 passed** in 0.16s |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 同上 | **0** | **193 passed**, 1 skipped, 2 deselected (~60.6s) |
| `python …/materialize_gate_c_payloads.py` | 同上 | **0** | `OK` → `payloads/materialize_report.json`；D 臂 median **479** heuristic tokens |

**P1 产物只读核对**（canonical `runs/gate_ctx_c_v1_batch_20260518_052803/`）：

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| `batch_index.json` | pass | `dry_run: false`；`schema: gate_ctx_c_batch_v1` |
| `round_01`～`03/index.json` + `raw/*_S0.jsonl` | pass | 6 条 jsonl（3 题 × D/E） |
| `gold_f1.json` / `gold_f1.md` | pass | 6 条 `parse_ok`；entry/impact F1 表齐全 |
| 复现命令 | pass | README 三行与 `batch_index.reproduce_commands` 一致 |
| NR-1/2 | pass | 未改 A/B 历史 run；未调用 `run_gate_b_batch` |

**§3 验收摘要（40 帽）**：§3.1 P0 **pass** · §3.2 P1 **pass** · §3.3 共用 **pass** · §3.3 P2 结论报告 **未测**（交下一棒 30 帽）。  
**阻塞**：无。

#### PR-2（P2 · 结论报告 · 30 帽 · 2026-05-18）

**human_gate**：`HG-GATE-C-SIGNOFF` 仅阻塞 `done`/`50`，不阻塞 30；其余闸无 `blocks_hats` 含 `30` 且 `pending` → 可开工。

| 项 | 结果 | 证据 |
| --- | --- | --- |
| P2 报告 | **draft** | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md` |
| 静态 token D vs E | pass | `materialize_report.json`：D median **479** · E **1262** |
| S0 gold F1 | pass | `runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md`（6/6 `parse_ok`） |
| 不推翻 B 默认 | pass | 报告 §3.2 明确维持 CTX_QUERY / `CTX_V2_QUERY` machine 轨 |
| pytest 主链 | pass | `pytest tests -m "not intent_eval and not intent_benchmark"` → **193 passed**, 1 skipped |
| NR-1/2 | pass | 未重跑 A/B batch；未改历史 runs |

**§3.3 P2（30 帽）**：结论正文与 D vs E 建议 **已交付（draft）**；`accepted` + 关账待结论 md 人改 `accepted` 后 **50** 帽。  
**阻塞**：无（关账前须结论 `accepted`）。

#### 40 帽（PR-2 · P2 独立复验 · 2026-05-18）

**human_gate**：无 `blocks_hats` 含 `40` 且 `pending` → 可开工。

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `pytest tests/test_gate_ctx_c_v1_materialize.py tests/test_gate_ctx_c_v1_batch.py -q` | `ai-ink-brain-api-python` | **0** | **9 passed** in 0.28s |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 同上 | **0** | **193 passed**, 1 skipped, 2 deselected (~68.5s) |
| `python …/materialize_gate_c_payloads.py` | 同上 | **0** | `OK`；D median **479** · E **1262**（与报告 §1 一致） |

**P2 报告只读核对**（`conclusion_gate_c_v2_dual_track_v1_zh.md` · 状态 **`draft`**）：

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 状态非 `accepted` | pass | 报告 L4 `draft`；40 帽未代填 |
| §0 复现命令 | pass | 与 `batch_052803/README.md`、`batch_index.reproduce_commands` 三行一致 |
| §1 静态 token D/E | pass | `materialize_report.json`：D median **479** · E **1262**；每题 tokens 415/814/479 · 1316/1262/973 |
| §2.1 运行时 token/wall | pass | 6× `raw/*_S0.jsonl` `usage`；D total 中位 **6018** · E **7019**；wall D **8.6s** · E **42.3s** |
| §2.2 gold F1 | pass | `gold_f1.md` 与报告表一致；6/6 `parse_ok: true` |
| §3 D vs E + 不推翻 B | pass | 成本 D 胜；entry 平局；impact D 弱优；§3.2 维持 CTX_QUERY |
| NR-1/2 | pass | A/B 历史 run 无 diff；未重跑 `gate_ctx_c` LLM batch |

**§3 验收摘要（40 帽 · P2 复验）**：§3.1 P0 **pass** · §3.2 P1 **pass** · §3.3 P2 证据链 **pass**（结论仍 **draft**）· §3.3 共用 **pass**。  
**阻塞**：无；关账须人将结论改 `accepted` 后戴 **50** 帽。

#### 50 帽（关账 · 独立复检 · 2026-05-18）

**human_gate**：`HG-GATE-C-SIGNOFF` **approved**；无 `blocks_hats` 含 `50` 且 `pending` → 可开工。  
**结论状态**：`conclusion_gate_c_v2_dual_track_v1_zh.md` L3 **`accepted`**（50 帽未代填）。

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `pytest tests/test_gate_ctx_c_v1_materialize.py tests/test_gate_ctx_c_v1_batch.py -q` | `ai-ink-brain-api-python` | **0** | **9 passed** |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 同上 | **0** | **193 passed**, 1 skipped |
| `python …/materialize_gate_c_payloads.py` | 同上 | **0** | D median **479** · E **1262** |

| 验收项（§3） | pass/fail | 证据 |
| --- | --- | --- |
| §3.1 P0 | **pass** | `fixtures/gate_ctx_c_v1/` + `test_gate_ctx_c_v1_materialize.py` |
| §3.2 P1 | **pass** | `runs/gate_ctx_c_v1_batch_20260518_052803/` · `dry_run: false` |
| §3.3 P2 `accepted` | **pass** | `reports/conclusion_gate_c_v2_dual_track_v1_zh.md` |
| §3.3 共用 pytest | **pass** | 193 passed |
| §1.1 P3（recommended） | **pass** | 30 帽 `invoke_20260518_35` · 40 帽 `invoke_20260518_36` 独立复验 |
| NR-1/2 | **pass** | 未重跑 A/B batch |

**§3 验收摘要（50 帽）**：PR-1/PR-2 **pass** · P3 **open（非阻塞 · 关账时）** · **建议合并**（P3 已由 30/40 帽于 2026-05-18 收口）。  
**关闭回溯**：`docs/harness/invokes/invoke_20260518_34_tech-graph-gate-c-50-close.md`

#### PR-3（P3 · 规划文档对齐 · 30 帽 · 2026-05-18）

**human_gate**：无 `blocks_hats` 含 `30` 且 `pending` → 可开工。

| 项 | 结果 | 说明 |
| --- | --- | --- |
| `Projects/docs/tech_graph/改进方向.md` | **pass** | 对比实验门闸表增 **C**；§2.7 勾选；三者关系方案2 注 **闸口 C** |
| `Projects/docs/tech_graph/tasks/ai-ink-brain-api-python/README.md` | **pass** | 闸口 C task → `done/` + 链结论 md |
| 业务代码 / fixture / run | **未改** | NR-1/2；未重跑 `run_gate_c_batch.py` |
| 结论 `accepted` | **未改** | 只读引用 P2 报告 |

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | `ai-ink-brain-api-python` | **0** | **193 passed**, 1 skipped, 2 deselected (~98s) |

**§1.1 P3**：**pass**（recommended · 已交付）。

#### 40 帽（PR-3 · 独立复验 · 2026-05-18）

**human_gate**：无 `blocks_hats` 含 `40` 且 `pending` → 可开工。  
**上一棒**：30 帽 P3 · `invoke_20260518_35` · 子仓 `cf48ee9` · 工作区 `738045c`。

| 命令 | cwd | 退出码 | 要点 |
| --- | --- | ---: | --- |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | `ai-ink-brain-api-python` | **0** | **193 passed**, 1 skipped, 2 deselected (~68.9s) |

**P3 规划文档只读核对**（对照 30 交付 · 未改 `accepted`）：

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| `改进方向.md` 对比实验表 **闸口 C** 行 | **pass** | L29：D/E 对比组 · 链 `conclusion_gate_c_v2_dual_track_v1_zh.md`（`accepted`）· `freeze_id` `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0` · canonical run `gate_ctx_c_v1_batch_20260518_052803` |
| **不推翻 B** 默认表述 | **pass** | L29「**不推翻** B 已采纳的 **CTX_QUERY / `graph_query` machine 默认**」；L30 方案3 立项仍依赖 **B** + **R2**（**不**以 C 替代 B） |
| §2.7 **闸口 C** 验收勾选 | **pass** | L223：`[x]` 闸口 C 已完成 · **维持** B 的 CTX_QUERY machine 默认 · E 为人读/按需双轨 |
| 「三者关系」方案2 注记 | **pass** | L68：深化实验 **闸口 C**（D vs E）已归档，**不改变** 方案3 对 **闸口 B** 的依赖 |
| `tasks/ai-ink-brain-api-python/README.md` | **pass** | 闸口 C task → `docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md` · 链 `conclusion_gate_c_v2_dual_track_v1_zh.md` |
| 结论 `accepted` | **未改** | 只读 L3 `accepted`；40 帽未代填 |
| NR-1/2 / batch | **pass** | 未重跑 `gate_ctx_c` / A/B batch；未改 fixture/run |

**§1.1 P3（40 帽）**：**pass**（pytest 绿 + 文档链一致；§1.1 两项 `[x]` 维持）。  
**阻塞**：无。

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 | 路径 |
| --- | --- | --- |
| **10 需求帽** | v0.1 初稿 | `docs/harness/invokes/invoke_20260518_10_tech-graph-gate-c-v2-dual-track-requirements.md` |
| **22 R1** | 通过 | `docs/harness/reviews/by-task/engineering_tech_graph_gate_c_v2_dual_track_v1/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md` |
| **30 PR-1** | P0 完成 | `docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-v2-dual-track-execute.md` |
| **30 PR-2** | P1 batch 完成 | `docs/harness/invokes/invoke_20260518_30_tech-graph-gate-c-p1-batch.md` |
| **40 PR-2** | P1 独立复验 pass | `docs/harness/invokes/invoke_20260518_31_tech-graph-gate-c-40-self-check.md` |
| **30 PR-2** | P2 结论 draft | `docs/harness/invokes/invoke_20260518_32_tech-graph-gate-c-p2-report.md` |
| **30 PR-3** | P3 规划文档对齐 | `docs/harness/invokes/invoke_20260518_35_tech-graph-gate-c-p3-docs.md` |
| **40 PR-3** | P3 独立复验 pass | `docs/harness/invokes/invoke_20260518_36_tech-graph-gate-c-40-p3-self-check.md` |
| **40 PR-2** | P2 独立复验 pass | `docs/harness/invokes/invoke_20260518_33_tech-graph-gate-c-40-p2-self-check.md` |
| **50 关账** | 独立复检 pass · task `done` | `docs/harness/invokes/invoke_20260518_34_tech-graph-gate-c-50-close.md` |

**关闭回溯（commit 索引）**：见对话「执行路线与 Commit 回溯」；末条关账 commit 见 `invoke_20260518_34` 提交 hash。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-18 | 10 帽初稿：闸口 C · D/E 双臂 · 不复跑 A/B |
| v0.2 | 2026-05-18 | 30 帽 PR-1：P0 fixture + materialize + pytest 绿 |
| v0.3 | 2026-05-18 | 30 帽 PR-2：P1 batch runner + dry-run pytest + `gate_ctx_c_v1_batch_20260518_052803` |
| v0.3 | 2026-05-18 | 30 帽 PR-2：P1 batch runner + dry-run pytest + LLM batch `052803` |
| v0.4 | 2026-05-18 | 40 帽：PR-2 独立复验；§3.1/3.2/共用 pass；P2 报告待 30 帽 |
| v0.5 | 2026-05-18 | 30 帽 P2：`conclusion_gate_c_v2_dual_track_v1_zh.md` draft；§1 P2 勾选；待 HG-GATE-C-SIGNOFF |
| v0.6 | 2026-05-18 | 40 帽 P2 复验：§0～§3 与证据链一致；pytest 绿；结论仍 draft → 待 50 关账 |
| v1.0 | 2026-05-18 | **关账**：结论 `accepted` + HG-GATE-C-SIGNOFF；50 复检；归档 `done/`；P3 open |
| v1.1 | 2026-05-18 | **P3**：`改进方向` / 工作区 README 索引；§1.1 P3 勾选；§6 PR-3 自检 |
| v1.2 | 2026-05-18 | **40 帽 PR-3**：规划文档只读复验 + pytest 绿；`invoke_20260518_36` |
