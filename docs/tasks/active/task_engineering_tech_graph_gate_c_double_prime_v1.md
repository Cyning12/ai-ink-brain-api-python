# Task：闸口 C″ — 分题物化修补 T003 impact（graph_v2 查询轨 · 实验先行）

> **状态**：`active`（PR-1～4 已落盘；**关账待** `HG-AUDIT-CLOSE`）  
> **结论（accepted）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md`  
> **50 关账审查**：`docs/harness/reviews/task_engineering_tech_graph_gate_c_double_prime_v1_audit_CLOSE_20260520.md`  
> **前置 task（done · 只读）**：`docs/tasks/done/task_engineering_tech_graph_gate_c_prime_f1_v1.md` · `docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md`  
> **关联结论（accepted · 不修订正文）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md` · `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md`  
> **本 task 定位**：在 **维持 `CTX_V2_QUERY` / `graph_query` 默认** 前提下，用 **最小变量**（分题 `manifest_slice` / `impact_surface`、必要时 T003 `query_seeds` 微调）做 **D vs E** 新 batch，相对 **canonical `052803`** 与 **C′ `083014`** 量化 **ΔF1 / Δtoken**；**胜出且人签后** 才升格 Cursor 消费规约（PR-4）  
> **test_strategy**：`required`  
> **test_strategy_note**：物化 / token pytest、batch 评分脚本；须相对 **052803** 与 **083014** 双基线对比，禁止无 baseline 宣称提升。  
> **freeze_id**：`TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id（输入）**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（除非 PR-1 为 F1 微调图边，须 bump 并写清）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
> **invoke（10 帽）**：`docs/harness/invokes/invoke_20260520_50_tech-graph-gate-c-double-prime-requirements.md`  
> **git_branch（建议）**：`task/engineering-tech-graph-gate-c-double-prime-v1`（自 **`main`** 拉取）

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **gates_before_code** | `["failure_paths", "freeze_id", "deps_installed"]` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | 初稿；验收阈值人可调 |
| **HG-AUDIT-R1** | `approved` | `30` | 任务审核 R1 通过后执行帽可开工 |
| **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** | `approved` | `PR-4`, `50`, 关账 | C″ 结论 accepted + 产品决议；**未 approved 禁止 PR-4** |
| **HG-AUDIT-CLOSE** | `pending` | `done`, `50` | 终轮 CLOSE 签收；**仅人**可改 `approved` 后归档 `docs/tasks/done/` |

---

## 0. 背景与目标

### 0.1 闸口分工（C / C′ / C″）

| 闸口 | freeze / run | 主变量 | 产品决议 |
| --- | --- | --- | --- |
| **C** | `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0` · `…_052803` | D=`CTX_V2_QUERY` vs E=`CTX_DUAL_MD` | **accepted**：维持 D 默认 |
| **C′** | `TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0` · `…_083014` | T002：`contract_slice` v2 + `manifest_slice` + `impact_surface` | **accepted**：维持 D 默认；T002 D impact **0.923** |
| **C″** | `TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0` · 新 `…_<YYYYMMDD>_*` | **主攻 T003**：Admin Ingest 域 `manifest_slice` + `impact_surface`；T002 **继承 C′** 物化 | 待实验 + 人签 |

### 0.2 动机（C′ follow-up）

| 题 | canonical D impact | C′ D impact | Δ vs C′ | C′ 物化 |
| --- | ---: | ---: | ---: | --- |
| T001 | 0.200 | 0.200 | 0 | 无 manifest / impact 切片 |
| T002 | 0.429 | **0.923** | — | v2 contract + manifest + **impact_surface** |
| T003 | **0.400** | **0.222** | **−0.178** | 仅 `downstream(A2,2)` 小图 |

- **entry** 三题 C′ 与 canonical 均稳（T003 entry **1.000**）；回落 **仅 impacts**（LLM 多写 `ref`、缺 gold `path`，误引 T002 契约域）。  
- **根因假设**：**分题物化缺失**（T003 未对齐 `tasks.json` gold path/kind），**非** 应改默认轨或整包 graph。  
- **C″ 不重斗 T002**：PR-1 **继承** C′ 对 T002 的物化策略；验收 **守卫** T002 不显著退化。

### 0.3 架构决议（产品优先级 · 强制）

| 优先级 | 内容 |
| --- | --- |
| **P0** | **实验对比先行**：`graph_v2` + **`CTX_V2_QUERY` 默认不变**；最小变量 → 新 batch **D vs E**；相对 **052803** 与 **083014** 量化 **ΔF1 / Δtoken** |
| **P1** | **关账后才改 Cursor rules**：仅当 C″ 结论 **accepted** 且写明可升格消费规约 → **PR-4** 更新 `.cursor/rules/10-tech-graph.mdc`（及必要 `graph_v2_schema` 指针） |
| **P-禁止** | 全面改 graph 拓扑后再对比；`graph_v3`；整包 `graph.json` / `15_e2e` 灌 prompt；升 `CTX_DUAL_MD` 默认；改写 C / C′ **accepted** 结论文 |

### 0.4 完成态

1. **PR-1**：T003 D 臂增加 Admin Ingest 域 `manifest_slice` + `impact_surface`（gold impacts）；T002 保持 C′ 三切片；T001 仅在有假设时轻量切片；`protocol_version.yaml` bump `gate_c_double_prime_freeze_id`；pytest 绿。  
2. **PR-2（条件）**：D 臂超 `payload_limits` 时收缩（裁 slice → depth → union），记录前后 token 表。  
3. **PR-3**：新 batch + `score_gold_f1` + **`conclusion_gate_c_double_prime_v1_zh.md`**（不改 C/C′ accepted 正文）。  
4. **PR-4（条件）**：`HG-GATE-C-DOUBLE-PRIME-SIGNOFF` = `approved` 后，按 §6.1 拟变更清单更新 `10-tech-graph.mdc`。

---

## 1. 范围 / 非范围

### 1.1 范围（PR 切片）

#### PR-1 · 分题物化（主变量 · 主攻 T003）

- [ ] **T003**（`T003_ingest_admin_rpc`）：在现有 `downstream(A2, depth=2)` 子图基础上增加：  
  - [ ] **`manifest_slice`**：admin ingest / sync 端点与 `tasks.json` 中 `A2`/`A1`/`AUTH` 相关 manifest 锚点（`api/index.py` admin 路由、`ingest_pipeline`、`_manifest.json` admin 段）。  
  - [ ] **`impact_surface`**：自 `fixtures/gate_ctx_ab_v1/tasks.json` T003 `gold.impacts[]` 抽取 **path + kind** 候选（如 `api/rag_env.py`、`supabase/sql`、`api/ingest_pipeline.py` RPC、`tools/tech_graph_manifest_check.py`），驱动 LLM 填 `impacts[].path`。  
  - [ ] **可选**：`query_seeds.json` 对 T003 第二 query（如 `upstream(A2,1)` 或 `neighbors`）— **仍须 graph_query**；禁止整图。  
- [ ] **T002**：**继承 C′**（`contract_slice` v2 + `manifest_slice` + `impact_surface`），**不**重做争论性切片实验。  
- [ ] **T001**：默认保持 C′/canonical 小图；仅在有书面假设时加 **轻量** manifest/impact（非本 task 主 KPI）。  
- [ ] `materialize_gate_c_payloads.py` 扩展；`tests/test_gate_ctx_c_v1_materialize.py` 断言 T003 含新切片字段。  
- [ ] `protocol_version.yaml`：新增 `gate_c_double_prime_freeze_id: TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0`；保留 `gate_c_prime_freeze_id` / canonical `freeze_id` 指针。

#### PR-2 · token 守门（仅 PR-1 超限时）

- [ ] 触发：`materialize_report.json` 任题 D 臂 `heuristic_tokens` ≥ 8192，或相对 C′ D 中位数 **481** 超 **×1.25** 且无 F1 收益记录。  
- [ ] 收缩顺序：**裁 slice 体积** → **降 depth** → **减 union query**；每步记录 token +（若已跑）F1。

#### PR-3 · C″ batch + 结论

- [ ] 新目录：`docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_<YYYYMMDD>_<HHMMSS>/`（**禁止**覆盖 `052803` / `083014`）。  
- [ ] 臂：`CTX_V2_QUERY` vs `CTX_DUAL_MD`（与闸口 C 同型）；模型/温度与 `protocol_version.yaml` 一致（`DeepSeek-V4-Flash` · `0.2`）。  
- [ ] 产出：`gold_f1.md` / `gold_f1.json`、`batch_index.json`、`README.md`（含复现命令）。  
- [ ] 结论文：`docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md` — 含相对 **052803** 与 **083014** 的 **Δentry / Δimpact / Δtoken** 表。

#### PR-4 · Cursor 消费规约升格（**条件 · 仅 HG 签收后**）

- [x] 合并前提：**§3.2 验收通过** + `conclusion_gate_c_double_prime_v1_zh.md` 状态 `accepted` + **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** = `approved`。  
- [x] 交付：按 **§6.1** 更新 `ai-ink-brain-api-python/.cursor/rules/10-tech-graph.mdc`（`graph_v2_schema.md` 无 freeze 表 → 跳过）。  
- [x] **阻塞**：上述 HG ≠ `approved` 时 **禁止** 提交 PR-4  diff（已解除）。

### 1.2 非范围（NR）

对齐 C′ **NR-1～7**，并增补：

| ID | 非范围 |
| --- | --- |
| **NR-1～7** | 同 `task_engineering_tech_graph_gate_c_prime_f1_v1.md` §1.2（含不覆盖 `052803`、不改 `conclusion_gate_c_v2_dual_track_v1_zh.md` accepted 正文、不升 `CTX_DUAL_MD` 默认等） |
| **NR-8** | 禁止「全面 graph 方案改进后再实验」作为主路径 |
| **NR-9** | 禁止 **batch 前 / 结论未签收前** 修改 `.cursor/rules/10-tech-graph.mdc` |
| **NR-10** | 禁止 GraphRAG / 博客向量试点混入本闸口 |

### 1.3 分期与阻塞

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | 分题物化 + pytest | **是** |
| **PR-2** | token 守门（条件） | 仅 PR-1 超限 |
| **PR-3** | C″ batch + 结论 | **是** |
| **PR-4** | rules 升格 | **是**（且须 HG 签收） |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 闸口 C canonical | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/` |
| 闸口 C′ 主 run | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014/` |
| 闸口 C / C′ 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md` · `conclusion_gate_c_prime_f1_v1_zh.md` |
| gold 题集 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json` |
| 协议 / 种子 | `fixtures/gate_ctx_c_v1/protocol_version.yaml` · `query_seeds.json` |
| 物化 / batch / 评分 | `fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py` · `run_gate_c_batch.py` · `fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py` |
| 机器轨 | `docs/_tech_graph/graph.json` |
| Cursor rules（**关账前只读**） | `.cursor/rules/10-tech-graph.mdc` |
| 规划 SPEC | `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |

### 2.1 F1 基线（D 臂 · 供 PR-3 对比）

| task | canonical `052803` impact | C′ `083014` impact | C″ 目标（§3.2） |
| --- | ---: | ---: | --- |
| T001 | 0.200 | 0.200 | 守卫：无单题降 >0.05 |
| T002 | 0.429 | **0.923** | 守卫：≥ **0.873**（C′−0.05） |
| T003 | **0.400** | **0.222** | 主 KPI：≥ **0.45** 或 Δ≥ **+0.15** vs C′ |
| **中位数** | 0.400 | 0.222 | entry 中位数 ≥ **0.80** |

### 2.2 静态 token 基线（D 臂 heuristic）

| 批 | T001 | T002 | T003 | 中位数 |
| --- | ---: | ---: | ---: | ---: |
| canonical | 415 | 814 | 479 | **479** |
| C′ | 417 | 4555 | 481 | **481** |

门槛（§3.2）：D 中位数 ≤ **max(479×1.25, 481×1.25) ≈ 599**；单题 < **8192**。

---

## 3. 验收标准

### 3.1 PR-1 / PR-2（物化）

- [ ] `python tools/tech_graph_graph_export.py --check` exit 0  
- [ ] `python …/materialize_gate_c_payloads.py` exit 0  
- [ ] `pytest tests/test_gate_ctx_c_v1_materialize.py` 绿；T003 payload 含 `manifest_slice` + `impact_surface`  
- [ ] 全题 D 臂 heuristic tokens **< 8192**（超则 PR-2 记录后通过）

### 3.2 PR-3（C″ batch · 主 KPI）

**产品（硬）**

- [ ] **维持** `CTX_V2_QUERY` / `graph_query` 为 machine 默认（E 臂仅对照）  
- [ ] **不**修订 `conclusion_gate_c_v2_dual_track_v1_zh.md` / `conclusion_gate_c_prime_f1_v1_zh.md` **accepted** 正文  

**impact F1（D 臂）**

- [ ] **主 KPI（OR）**：**T003** D impact F1 **≥ 0.45**，**或** 相对 C′ `083014` 的 T003 **Δimpact ≥ +0.15**（0.222 → **≥ 0.372**）  
- [ ] **守卫**：**T002** D impact **≥ 0.873**（C′ **0.923** − **0.05**）  
- [ ] **entry**：三题相对 C′ **无单题下降 > 0.05**；entry F1 **中位数 ≥ 0.80**

**token（D 臂）**

- [ ] 中位数 ≤ **max(canonical×1.25, C′×1.25)**（≈ **599**）  
- [ ] 单题 heuristic tokens **< 8192**

**工程**

- [ ] 新 run 目录 + `conclusion_gate_c_double_prime_v1_zh.md`（含 Δ 表）  
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿  

### 3.3 PR-4（rules 升格 · 条件）

- [x] **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** = `approved`  
- [x] §3.2 主 KPI + 结论 `accepted`（策略 B 豁免 T002 守卫 / T003 entry）  
- [x] `10-tech-graph.mdc` 变更与 §6.1 清单一致（无 batch 前偷跑）

### 3.4 关账

- [ ] 三枚 `human_gate` 终态符合上表；task 归档 `docs/tasks/done/`

---

## 4. failure_paths

| ID | 触发 | 行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- |
| FP-CDP1 | 未建新 run 即改 `052803`/`083014` jsonl | **拒开工** | 否 | N/A（内部） |
| FP-CDP2 | PR-3 前 T003 物化未落盘 | 先 PR-1；禁止直接 batch | 是 | N/A |
| FP-CDP3 | `materialize` token 超限且无 PR-2 记录 | exit 非 0；先收缩 | 是 | 日志含题号/token |
| FP-CDP4 | T003 未达 §3.2 且提议改默认轨为 E 或 `CTX_DUAL_MD` | **变更请求**；仅输出 C″ 数据 | 否 | 结论 draft 说明 |
| FP-CDP5 | 提议 graph_v3 / 整包双轨 / 先大改 graph 再实验 | **拒 scope**（NR-8） | 否 | N/A |
| FP-CDP6 | HG 未签收即改 `10-tech-graph.mdc` | **拒合并 PR-4** | 否 | N/A |
| FP-CDP7 | `graph_query` 空子图 / 种子节点不存在 | `materialize` 失败或显式 skip 并记入报告 | 是（修种子） | 物化报告错误节 |
| FP-CDP8 | batch LLM / 评分脚本失败 | 保留 partial run；不覆盖历史 batch | 是 | `batch_index` err 字段 |

---

## 5. 给执行帽的必读

1. 自 **`main`** 拉分支 `task/engineering-tech-graph-gate-c-double-prime-v1`。  
2. **顺序**：PR-1（T003 物化）→（必要时 PR-2）→ PR-3（C″ batch）→（签收后）PR-4。  
3. **禁止** batch 前修改 `.cursor/rules/10-tech-graph.mdc`（NR-9）。  
4. PR-3 模型/温度与闸口 C 一致，除非人签 bump `freeze_id`。  
5. 结论文件名：**`conclusion_gate_c_double_prime_v1_zh.md`**。  
6. 相对基线必须同时引用 **052803**（canonical）与 **083014**（C′）。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| invoke · 10 | `docs/harness/invokes/invoke_20260520_50_tech-graph-gate-c-double-prime-requirements.md` |
| 分支 | `task/engineering-tech-graph-gate-c-double-prime-v1` |
| PR-1 | T003 `manifest_slice` v2 compact + `impact_surface` v2；`protocol_version.yaml` / `query_seeds.json` C″ freeze |
| PR-2 | T003 depth 2→1 + 紧凑切片；D 中位数 **561** |
| PR-3 run | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_102810/` |
| C″ 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md`（**accepted** · 策略 B） |
| PR-4 | `.cursor/rules/10-tech-graph.mdc` · `.cursor/rules/README.md`（2026-05-20） |

### 6.1 PR-4 拟变更 diff 清单（`10-tech-graph.mdc` · **关账前勿改文件**）

> 仅供 PR-4 对照；内容须与 C″ **accepted** 结论一致。

| 节 | 拟增补（摘要） |
| --- | --- |
| **Agent 读取顺序 §1** | 影响分析除 `graph_query` 子图外，**实验/物化轨**可对 Admin Ingest 等题附加 **`manifest_slice` + `impact_surface`**（path/kind 来自 `tasks.json` gold），减少 `impacts[].ref` 无 path 的 FP |
| **禁止项** | 重申：物化 `impact_surface` **不**等于默认整包 `graph.json` 或 `15_e2e` 双轨 |
| **引用** | 链 `conclusion_gate_c_double_prime_v1_zh.md` + `TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0`（签收后） |
| **可选** | `docs/_tech_graph/graph_v2_schema.md` 增 C″ freeze 指针一行（若 schema 文档已有 freeze 表） |

### 自检结论（执行者）

| 验收项 | 结果 | 证据 |
| --- | --- | --- |
| HG-TASK-DRAFT / HG-AUDIT-R1 | pass | task 元信息表 `approved`（人签后开工） |
| PR-1 物化 + pytest materialize | pass | `pytest tests/test_gate_ctx_c_v1_materialize.py` **8 passed** |
| PR-2 token | pass | D 中位数 **561** ≤ max(479,481)×1.25 |
| §3.2 主 KPI T003 impact | pass | D impact **0.857**（`…_102810/gold_f1.md`） |
| §3.2 T002 守卫 | **fail** | D impact **0.800** &lt; **0.873** |
| §3.2 entry 无单题降 &gt;0.05 | **fail** | T003 entry **0.923** vs C′ **1.000**（Δ−0.077） |
| PR-4 / rules | pass | `10-tech-graph.mdc` + `README.md`；HG **approved**；结论 **accepted** |
| 全量 pytest | pass | 见下 |

**命令（cwd = `ai-ink-brain-api-python`）**

| 命令 | 退出码 |
| --- | ---: |
| `python tools/tech_graph_graph_export.py --check` | 0 |
| `python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py` | 0 |
| `pytest tests/test_gate_ctx_c_v1_materialize.py` | 0 |
| `RUBRIC_REVIEW_BACKEND=siliconflow python …/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD` | 0 |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 0（PR-1–3）；PR-4 见下 |

#### PR-4（2026-05-20 · 执行帽 30）

| 验收项 | 结果 | 证据 |
| --- | --- | --- |
| HG-GATE-C-DOUBLE-PRIME-SIGNOFF | pass | task 元信息 `approved` |
| 结论 `accepted` + §6 豁免 | pass | `conclusion_gate_c_double_prime_v1_zh.md` |
| §6.1 → `10-tech-graph.mdc` | pass | Agent 读取顺序 · 物化轨表 · 禁止项 · 引用 freeze |
| `graph_v2_schema.md` freeze 行 | skip | 文档无 freeze 表（§6.1 可选） |
| 全量 pytest（PR-4 后） | pass | 见下 |

| 命令 | 退出码 |
| --- | ---: |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 0（**199 passed**, 1 skipped） |

**改动路径**：`.cursor/rules/10-tech-graph.mdc`、`.cursor/rules/README.md`。

**已知未测**：关账归档 `docs/tasks/done/`（待 **`HG-AUDIT-CLOSE`** = `approved`）。

#### 50 帽关账（2026-05-20）

| 验收项 | 结果 | 证据 |
| --- | --- | --- |
| 50 全局验收 + CLOSE_TRACE | pass | `…_audit_CLOSE_20260520.md` |
| PR-4 分支待合并 main | 待 PR | `task/…-pr4-rules` · `api-python@2dc2755` |
| task → `done/` | **阻塞** | `HG-AUDIT-CLOSE` = `pending` |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-20 | 10 帽初稿：C″ 分题物化主攻 T003；实验先行 · rules 后置；相对 052803/083014 量化验收 |
