# Task：闸口 D — `gate_ctx_ab_v2` 题集扩域（v1 三题 + T004/T005）

> **状态**：`done（2026-05-21 · 闸口 D v2 五题扩域 · HG-GATE-D-SIGNOFF 人签 · PR #41 · merge abb08f4）`  
> **结论（accepted）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`  
> **50 关账复检**：`docs/harness/reviews/task_engineering_tech_graph_gate_d_v2_tasks_v1_reinspect_R1_20260521.md`  
> **路线图**：[`docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md`](../../../../docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md) **INK-P5** · §3 **B1**  
> **方法论**：[`ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md`](../../../../ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md) §6.1、§7  
> **草案来源**：[`ai_coding_governance/methodology/graph/drafts/draft_gate_ctx_ab_v2_expansion_v1.md`](../../../../ai_coding_governance/methodology/graph/drafts/draft_gate_ctx_ab_v2_expansion_v1.md)  
> **前置（done · 只读）**：`docs/tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md` · `docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md`  
> **关联结论（accepted · 禁止修订正文）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md` · `conclusion_gate_c_v2_dual_track_v1_zh.md` · `conclusion_gate_c_prime_f1_v1_zh.md`  
> **本 task 定位**：**闸口 D** — 金标题 **v1→v2**（保留 T001～T003 + 增量 **T004 ChatBI/Text2SQL**、**T005 Intent/路由**）；**维持** `CTX_V2_QUERY` 为 machine 默认；**沿用 C″ 分题物化策略**；新 batch **D vs E** + 分表结论文  
> **test_strategy**：`required`  
> **test_strategy_note**：`pytest` 门禁（物化 / 题集 schema / 可选 batch dry-run）；PR-3 batch 须可复现命令；全仓 `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿。  
> **freeze_id（占位 · 执行帽落盘时写入 protocol）**：`TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id（输入）**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（图语义变更须 bump 并书面说明）  
> **gates_before_code**：`["failure_paths", "freeze_id", "test_strategy", "deps_installed"]`  
> **Harness 通则**：`Projects/docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
> **需求帽 invoke**：`docs/harness/invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md`  
> **git_branch**：`task/engineering-tech-graph-gate-d-v2-tasks-v1`

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | 本 task 初稿；人扫验收阈值与 NR 后改 `approved` |
| **HG-AUDIT-R1** | `approved` | `30` | 任务审核 R1 零硬阻塞后执行帽可开工 |
| **HG-GATE-D-SIGNOFF** | `approved` | `50`, `done` | 闸口 D 结论文 `accepted` 后人签关账 |

---

## 0. 背景与目标

### 0.1 闸口分工（C 系 vs D）

| 闸口 | freeze / canonical run | 题集 | 主变量 | 产品决议 |
| --- | --- | --- | --- | --- |
| **C** | `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0` · `…_052803` | v1 三题 | D vs E | **accepted**：维持 `CTX_V2_QUERY` 默认 |
| **C′** | `…_PRIME…` · `…_083014` | v1 三题 | T002 物化切片 | **accepted**：维持 D 默认 |
| **C″** | `…_DOUBLE_PRIME…` · `…_102810` | v1 三题 | T003 分题物化 | **accepted**：维持 D 默认；T003 impact **0.857** |
| **D（本 task）** | `TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0` · 新 `…_<ts>` | **v2 五题** | +T004/T005 gold + 物化/种子/双轨 | 待实验 + 人签 |

### 0.2 动机

- C″ 已在 **RAG / SSE 契约 / Admin ingest** 三题验证 **graph_query + 分题物化**；方法论 §6.1 要求 **本仓扩域** 以支撑团队内推广（ChatBI、Intent 等横切模块）。  
- **不** 用 v2 新题分数直接覆盖 C/C′/C″ 历史叙事；**表 1 回归** vs `102810`，**表 2 扩展** 仅评 T004/T005。

### 0.3 架构决议（强制）

| 优先级 | 内容 |
| --- | --- |
| **P0** | **维持** `CTX_V2_QUERY` / `graph_query` 为 Agent **machine 默认**；E=`CTX_DUAL_MD` 仅对照 |
| **P0** | **沿用 C″ 物化策略**：T001～T003 **继承** C″ 已验收切片（勿回退 canonical 小图）；T004 参照 T002（contract + manifest + impact）；T005 按 §7 方法论种子对齐 intent 子图 |
| **P-禁止** | 升 `CTX_DUAL_MD` 为默认；覆盖 `052803`/`083014`/`102810`；改写 C 系 **accepted** 结论文；前端仓金标；Neo4j / 方案 3 |

### 0.4 完成态

1. **PR-1**：`fixtures/gate_ctx_ab_v2/tasks.json`（v1 三题 + T004/T005 gold，**rg + 图谱核对**）+ 扩展 `query_seeds.json` / `dual_track_manifest.json` / `materialize_gate_c_payloads.py` + `protocol_version.yaml` bump `gate_d_v2_tasks_freeze_id`  
2. **PR-2（条件）**：D 臂 token 超 §3.2 门槛时收缩并记录  
3. **PR-3**：新 batch（5 题 × D/E）+ `score_gold_f1` + **`conclusion_gate_d_ctx_v2_tasks_v1_zh.md`**（回归表 + 扩展表）  
4. **PR-4（recommended · 非阻塞关账）**：`改进方向.md` 闸口 **D** 行由「规划」改为链本结论文；**不** 默认改 `.cursor/rules`（除非 HG 另批）

---

## 1. 范围 / 非范围

### 1.1 范围（PR 切片）

#### PR-1 · v2 题集与物化（主交付）

- [ ] **`fixtures/gate_ctx_ab_v2/tasks.json`**  
  - [ ] `schema_version`: `gate_ctx_ab_tasks_v2`；`fixture_set`: `gate_ctx_ab_v2`  
  - [ ] **保留** v1 三题 `task_id` / `gold` 与 `gate_ctx_ab_v1/tasks.json` **一致**（或显式 diff 说明 + 审查签收）  
  - [ ] **T004** `T004_chatbi_text2sql_chain`：gold 按方法论 §7 T004（`api/unified_chat.py` Text2SQL、`api/index.py` 路由、`supabase/sql`、相关 flow 节点）；**禁止**默认整包 `15_e2e` 作 E 臂  
  - [ ] **T005** `T005_intent_routing`：gold 按 §7 T005（intent 路由、SSE typ、低置信澄清路径）  
- [ ] **`protocol_version.yaml`**：`tasks_ref` → `gate_ctx_ab_v2/tasks.json`；新增 `gate_d_v2_tasks_freeze_id: TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0`；保留 C/C′/C″ freeze 指针  
- [ ] **`query_seeds.json`**：为 T004/T005 增加 `node_id` / `op` / `depth`（仍 **graph_query**；禁止整图）  
- [ ] **`dual_track_manifest.json`**：T004/T005 各选 **≤2** 对 `.ai.md`+`.md`（ChatBI/e2e 相关 flow，**非** 七文件整灌）  
- [ ] **`materialize_gate_c_payloads.py`**：  
  - [ ] T001～T003：**继承 C″** 物化分支（manifest_slice / impact_surface / depth）  
  - [ ] T004：**contract_slice** v2 + **manifest_slice** + **impact_surface**（对齐 T002 模式）  
  - [ ] T005：**manifest_slice** + **impact_surface** + intent 对齐种子  
- [ ] **pytest**：扩展 `tests/test_gate_ctx_c_v1_materialize.py`（或新增 `test_gate_ctx_ab_v2_tasks.py`）：五题 payload 非空、T004/T005 种子节点存在于 `graph_v2`、ab_v2 JSON schema

#### PR-2 · token 守门（仅 PR-1 超限时）

- [ ] 触发：任题 D 臂 `heuristic_tokens` ≥ **8192**，或五题 D 中位数 > **max(601, C″×1.25)**（C″ D 中位数 **561** → 门槛约 **701**；执行时可写入 `materialize_report`）  
- [ ] 收缩顺序：裁 slice → 降 depth → 减 union query；每步记入 `materialize_report.json`

#### PR-3 · batch + 结论文

- [ ] **物化**（子仓根）：

```bash
python tools/tech_graph_graph_export.py --check
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
pytest tests/test_gate_ctx_c_v1_materialize.py
```

- [ ] **batch**（须 `SILICONFLOW_API_KEY`；模型/温度与 `protocol_version.yaml` 一致）：

```bash
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py
# 执行帽：扩展 TASKS 为五题或从 ab_v2 tasks.json 读取；禁止覆盖 052803/083014/102810
```

- [ ] **评分**：

```bash
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --run-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_<YYYYMMDD>_<HHMMSS>
```

- [ ] **run 目录约定**：`docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_<YYYYMMDD>_<HHMMSS>/`（**新** `<ts>`；`batch_index.json` 注明 `gate_d_v2_tasks_freeze_id`）  
- [ ] **结论文**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`  
  - [ ] **表 1 · v1 回归**：T001～T003 D 臂 impact/entry F1 vs **`102810`**（单题下降 ≤ **0.10**，人可调）  
  - [ ] **表 2 · v2 扩展**：T004/T005；至少 1 题 impact F1 ≥ **0.45** 或相对「无题专属物化」基线 Δ ≥ **+0.15**  
  - [ ] **表 3 · D vs E**：token 中位数 + F1（同 C 报告结构）  
- [ ] **全仓 pytest**：`pytest tests -m "not intent_eval and not intent_benchmark"`

#### PR-4 · 文档索引（recommended）

- [ ] `ai_coding_governance/methodology/graph/改进方向.md` 闸口 **D** 行：链 `conclusion_gate_d_ctx_v2_tasks_v1_zh.md`（**不**改 C/C′/C″ accepted 行）  
- [ ] 方法论 §6.1 `task 落盘` 指针改指向本 task `done/` 路径（关账后）

### 1.2 非范围（NR）

| ID | 非范围 |
| --- | --- |
| **NR-1** | **禁止** 重跑闸口 A/B **主实验** 或改写其 accepted 结论文 |
| **NR-2** | **禁止** 覆盖或改写 `runs/gate_ctx_c_v1_batch_20260518_052803` · `…_083014` · `…_102810` 内 jsonl / `gold_f1` |
| **NR-3** | **禁止** 修订 `conclusion_gate_c_*` 系列 **accepted** 正文 |
| **NR-4** | **禁止** 将 `CTX_DUAL_MD` 升为 machine 默认 |
| **NR-5** | **禁止** 修改 `ai-ink-brain` 前端仓图谱 / 金标（阶段 D 外仓 PoC 另立项） |
| **NR-6** | **禁止** 方案 3 Neo4j、graph_v3、整包 `graph.json` / 七文件 `.ai.md` 灌 prompt |
| **NR-7** | **禁止** 用 T004/T005 单题分数宣称「优于 C″」而不分 **表 1/表 2** |
| **NR-8** | 本 task **不写** batch runner 以外 ChatBI/Intent **产品行为** 变更（仅实验题集 + 物化） |

### 1.3 分期与阻塞

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | v2 题集 + 物化 + pytest | **是** |
| **PR-2** | token 守门（条件） | 仅 PR-1 超限 |
| **PR-3** | batch + 结论文 | **是** |
| **PR-4** | 方法论/改进方向索引 | **否** |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| v1 题集（只读对照） | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json` |
| C 协议 / 物化 / batch | `fixtures/gate_ctx_c_v1/protocol_version.yaml` · `scripts/materialize_gate_c_payloads.py` · `scripts/run_gate_c_batch.py` |
| C″ 主 run（回归基线） | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_102810/` |
| C″ 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md` |
| 评分 | `fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py` |
| 机器轨 | `docs/_tech_graph/graph.json` |
| 查询 SPEC | `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| 路线图 | `Projects/docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md` §3 B1 |

### 2.1 v1 回归基线（D 臂 · 来自 C″ `102810`）

| task | C″ D impact | C″ D entry | 回归守卫（草案） |
| --- | ---: | ---: | --- |
| T001 | 0.200 | 0.857 | impact Δ ≥ **−0.10** |
| T002 | 0.800 | 0.923 | impact Δ ≥ **−0.10** |
| T003 | 0.857 | 0.923 | impact Δ ≥ **−0.10** |

### 2.2 T004/T005 gold 要点（执行起稿 · 须 rg 核验）

| 题 | prompt 意图 | 入口点（草案） | 影响面（草案） | E 臂双轨（草案） |
| --- | --- | --- | --- | --- |
| **T004** | Text2SQL / AST 闸门 | `api/unified_chat.py` T2S 分支、`api/index.py` | `supabase/sql`、manifest、相关 pytest、graph T2S 节点 | 含 ChatBI 的 `10_flow_*.ai.md`（**非**整包 `15_e2e`） |
| **T005** | intent 阈值 / 路由 | `api/unified_chat.py` 路由决策 | 观测日志、SSE event typ、clarify 路径 | intent 相关 flow 双轨 |

正式 `gold` 写入 `tasks.json` 前须 **`rg` + `graph.json` 节点 id** 双核验。

---

## 3. 验收标准

### 3.1 PR-1（题集 + 物化）

- [ ] `gate_ctx_ab_v2/tasks.json` 含 **5** 题且 T001～T003 gold 与 v1 **一致**（或审查批准的 diff 记录）  
- [ ] T004/T005 各 ≥ **3** entrypoints、≥ **3** impacts（path/kind/graph_id 可评分）  
- [ ] `materialize_gate_c_payloads.py` exit 0；五题 D/E payload 目录非空  
- [ ] `pytest tests/test_gate_ctx_c_v1_materialize.py`（及 ab_v2 若有）绿  

### 3.2 PR-3（batch · 主 KPI）

**产品（硬）**

- [x] **维持** `CTX_V2_QUERY` 为 machine 默认  
- [x] **不**修订 C 系 accepted 结论文正文  

**表 1 · v1 回归（D 臂 vs `102810`）**

- [x] T001～T003：单题 impact F1 **相对 C″ 下降 ≤ 0.10**（阈值 HG-TASK-DRAFT 可调）  

**表 2 · v2 扩展（D 臂）**

- [x] T004 **或** T005：impact F1 ≥ **0.45**，**或** 相对执行帽记录的「无专属物化」基线 Δ ≥ **+0.15**  

**token（D 臂 · 五题）**

- [x] 中位数 ≤ **max(601, C″×1.25)**（约 **701**；以 `materialize_report` 为准）  
- [x] 单题 heuristic tokens **< 8192**  

**工程**

- [x] 新 `runs/gate_ctx_c_v1_batch_*` + `conclusion_gate_d_ctx_v2_tasks_v1_zh.md`（含复现命令）  
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿  

### 3.3 关账

- [x] **HG-GATE-D-SIGNOFF** = `approved`；结论文状态 `accepted`  
- [ ] `git mv` 至 `docs/tasks/done/`；**PRIORITY_ROADMAP** INK-P5 / §3 B1 → `done（YYYY-MM-DD）`

---

## 4. failure_paths

| ID | 触发 | 行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- |
| FP-GD1 | 未建新 run 即改 `052803`/`083014`/`102810` | **拒开工** | 否 | N/A |
| FP-GD2 | T004/T005 gold 未 rg/图谱核验即 batch | **拒 PR-3**；先 PR-1 | 是 | task 阻塞清单 |
| FP-GD3 | `materialize` 失败 / 种子节点不在 `graph_v2` | exit 非 0；修种子或图 | 是 | `materialize_report` 错误节 |
| FP-GD4 | D token 超限且无 PR-2 记录 | 禁止 batch；先收缩 | 是 | 日志含题号/token |
| FP-GD5 | v2 题 F1 低且提议升 `CTX_DUAL_MD` 默认 | **变更请求**；仅输出数据表 | 否 | 结论 draft |
| FP-GD6 | 用 T004/T005 覆盖 C″ 主叙事或改 C accepted 正文 | **拒 scope**（NR-3/7） | 否 | N/A |
| FP-GD7 | batch 无 API Key（同 FP-C-5） | 停止；自检写明环境阻塞 | 是 | 不伪造 jsonl |
| FP-GD8 | `pytest` 主链红 | 禁止宣称 PR-1/3 完成 | 是 | CI 日志 |

---

## 5. 给执行帽的必读

1. 分支 **`task/engineering-tech-graph-gate-d-v2-tasks-v1`**；**禁止**与 `task/chatbi-v3-prompt-injection-closeout-v1` 共用。  
2. **顺序**：PR-1（ab_v2 + 物化扩展）→（PR-2）→ PR-3（batch + 评分 + 结论文）→ PR-4 文档。  
3. **继承 C″**：T001～T003 物化逻辑 **勿回退**；仅增量 T004/T005 配置。  
4. **batch**：扩展 `run_gate_c_batch.py` 题列表为五题；**新** run 目录；`batch_index` 写 `gate_d_v2_tasks_freeze_id`。  
5. **结论文文件名**：`conclusion_gate_d_ctx_v2_tasks_v1_zh.md`；**表 1/表 2 分表**。  
6. 回归基线 **仅读** `102810`；**禁止**重跑三历史 batch 作主结论。  
7. 开帽前扫描 **HG-AUDIT-R1**；`pending` → **拒开工**（仅阻塞清单）。  
8. **全仓 pytest** 为合并前必绿（根 `AGENTS.md` §8）。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 路径 / 命令 |
| --- | --- |
| ab_v2 tasks | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v2/tasks.json` |
| protocol bump | `fixtures/gate_ctx_c_v1/protocol_version.yaml` · `gate_d_v2_tasks_freeze_id` |
| 物化 / PR-2 | `fixtures/gate_ctx_c_v1/payloads/materialize_report.json` · D 中位数 **658** |
| batch dry-run | `runs/gate_ctx_c_v1_batch_20260521_065655/`（5×round · `dry_run: true`） |
| 主 run（LLM） | `runs/gate_ctx_c_v1_batch_20260521_091709/` · `dry_run: false` · 10 jsonl |
| 结论文 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_d_ctx_v2_tasks_v1_zh.md`（`accepted` · 表 1/2/3） |

### 自检结论（执行者）

**执行帽 30 + 自检 40（2026-05-21 · PR-3）· cwd**：`ai-ink-brain-api-python-wt-gate-d-v2` · 分支 `task/engineering-tech-graph-gate-d-v2-tasks-v1`

| 命令 | 退出码 | 要点 |
| --- | ---: | --- |
| `python tools/tech_graph_graph_export.py --check` | 0 | graph export OK（PR-1 已验；本轮未重跑） |
| `python …/materialize_gate_c_payloads.py` | 0 | D 中位数 **658** ≤ **701**（PR-2 pass） |
| `pytest tests/test_gate_ctx_ab_v2_tasks.py tests/test_gate_ctx_c_v1_materialize.py` | 0 | 13 passed（PR-1） |
| `run_gate_c_batch.py`（实跑 LLM） | 0 | 主 run **`…_091709`** · 5 round × D/E · `gate_d_v2_tasks_freeze_id` |
| `score_gold_f1.py --batch-dir …_091709 --tasks ab_v2/tasks.json` | 0 | `gold_f1.md/json` · 10 条评分 |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | 0 | **204 passed**, 1 skipped |

**NR 核对**：`052803` / `083014` / `102810` **无 git diff**；未升 `CTX_DUAL_MD` 默认；未改 C 系 accepted 结论文。

**验收摘要（PR-1）**

| 项 | 结果 |
| --- | --- |
| ab_v2 五题 + v1 gold 一致 | pass |
| T004/T005 ≥3 entry/impact | pass |
| 物化五题 payload 非空 | pass |
| pytest 物化 / schema | pass（13） |

**验收摘要（PR-3 · §3.2）**

| 项 | 结果 | 证据 |
| --- | --- | --- |
| 表 1 · v1 回归 impact Δ ≤ 0.10 | **pass** | T001 0.000 · T002 +0.123 · T003 +0.143 |
| 表 2 · T004/T005 impact ≥ 0.45 | **pass** | **0.750** / **0.857** |
| D 静态 token 中位数 ≤ 701 | **pass** | **658**（`materialize_report.json`） |
| D 单题静态 &lt; 8192 | **pass** | max **4355**（T002） |
| 新 batch + 结论文表 1/2/3 | **pass** | `…_091709` + `conclusion_gate_d_*.md` |
| 维持 `CTX_V2_QUERY` 默认 | **pass** | D impact/total 中位数优于 E |
| 全仓 pytest | **pass** | 204 |
| 结论文 `accepted` | **pass** | 结论文 + **HG-GATE-D-SIGNOFF** `approved`（2026-05-21 关账） |

**已知未测项**：表 2「无专属物化」ablation 基线（未跑；以绝对门槛 0.45 验收）；PR-4 `改进方向.md` 索引（recommended · 非阻塞）。

---

## 7. 矛盾与待决（需求帽记录）

| 矛盾 | 出处 A | 出处 B | 本 task 裁定（待 22 帽可改） |
| --- | --- | --- | --- |
| 题集目录名 **`gate_ctx_ab_v2`** vs batch/协议仍名 **`gate_ctx_c_v1`** | 方法论 §6.1 · 草案 | C″ task 沿用 `gate_ctx_c_v1` 脚本 | **ab_v2** 仅 `tasks.json`；协议/batch **沿用** `gate_ctx_c_v1` 目录，以 `gate_d_v2_tasks_freeze_id` 区分实验 |
| 草案写「新建 `fixtures/gate_ctx_ab_v2/`」 vs 仅 `tasks.json` | `draft_gate_ctx_ab_v2_expansion_v1.md` | C 系 `tasks_ref` 单文件 | **最小**：`ab_v2/tasks.json` + 扩展 c_v1 侧车文件；**不**复制整套 B/C 独立 fixture 树 |
| 路线图 M2 文档路径 `AGENT_GRAPH…` 在 `docs/tech_graph/` vs 治理仓 `methodology/graph/` | PRIORITY_ROADMAP §4 | 治理仓真值 | 依赖以 **治理仓** `ai_coding_governance/methodology/graph/` 为准；SPEC 用 `Projects/docs/tech_graph/SPEC/…` |

---

## 8. Invoke 快照（可选）

- `docs/harness/invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md`

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-20 | v1.0：10 帽自草案立正式 task；INK-P5/B1 立项 |
| 2026-05-21 | v1.1：PR #41 合 main；结论文 accepted；路线图 INK-P5/B1/M2 → done |
