# Task：技术图谱 — 闸口 C 对比实验（graph_v2 查询轨 vs 双轨原文）

> **状态**：`active`（**v0.1** · 10 帽初稿 · 待 `HG-TASK-DRAFT` 人签）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（闸口 B · `CTX_QUERY`）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_scheme2_completion_v1.md`（`has_path` / `describe_impact`）  
> **关联规划**：`Projects/docs/tech_graph/改进方向.md` **v1.1.3** **R4**；`scheme_2_graph_query.md`  
> **本 task 定位**：**闸口 C**（新协议 · 非重跑闸口 A/B 主实验）  
> **test_strategy**：`required`  
> **test_strategy_note**：新 `fixtures/gate_ctx_c_v1/` 须可 materialize + 至少 1 题 dry-run；pytest 覆盖 payload 构建与 query 种子；LLM batch 可 Phase 分步。  
> **freeze_id**：`TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0`（待 P0 锁定 `protocol_version.yaml`）  
> **gates_before_code**：`failure_paths`、`test_strategy`、`freeze_id`、§0.3 实验臂定义、§1.2 NR 清单  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
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
| **HG-TASK-DRAFT** | `pending` | `22-R1`, `30` | 本 v0.1 初稿后人扫 |
| **HG-AUDIT-R1** | `pending` | `30` | R1 零硬阻塞后人签执行 |
| **HG-P0-PROTOCOL** | `pending` | `30` | `gate_ctx_c_v1` 协议 + 题集人签 |
| **HG-GATE-C-SIGNOFF** | `pending` | `done`, `50` | 实验结论人签 |

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

- [ ] **P0 · 协议与 fixture**  
  - [ ] `gate_ctx_c_v1/protocol_version.yaml`（`freeze_id`、图路径、`graph_v2_freeze_id` 引用）  
  - [ ] `dual_track_manifest.json`（每题列出 `.ai.md` + `.md` 路径，上限 token 预算写明）  
  - [ ] `materialize_gate_c_payloads.py`（输出 D/E 主载荷；报告 `materialize_report.json`）  
  - [ ] `query_seeds.json`（对齐 v2 真值节点，**禁止**沿用已废弃示例 `AUTH→RAG` 若生产图无边）  
- [ ] **P1 · batch**  
  - [ ] 复用或薄封装既有 batch runner（与 `gate_ctx_b_v1` 同型入口，新 protocol id）  
  - [ ] S0 段 3 题 × 2 臂（D、E）最低跑通  
- [ ] **P2 · 结论**  
  - [ ] 轴：token（主载荷）、影响集抽样 F1/人工表、wall（可选）  
  - [ ] 链 `conclusion_gate_b` / `conclusion_gate_ctx_ab` 作背景，**不**推翻 B 已采纳的 CTX_QUERY 默认  
- [ ] **P3 · 文档（recommended）**  
  - [ ] `改进方向.md` 对比实验表增 **闸口 C**  
  - [ ] `docs/tech_graph/tasks/ai-ink-brain-api-python/README.md` 索引  

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

- [ ] `python …/materialize_gate_c_payloads.py` → exit 0；D/E payload 目录非空  
- [ ] pytest 覆盖：manifest 路径存在、query 种子节点在 `graph_v2` 中存在、D 臂子图节点数 < 整包 Mermaid 阈值（阈值写入 protocol）

### 3.2 P1

- [ ] `runs/gate_ctx_c_v1_batch_*` 含 `batch_index.json` + 每题 raw jsonl  
- [ ] 复现命令写入报告 §0

### 3.3 P2

- [ ] `conclusion_gate_c_v2_dual_track_v1_zh.md` 状态 `accepted` 前人签 **HG-GATE-C-SIGNOFF**  
- [ ] 明确 **D vs E** 胜负与是否建议调整 Agent 默认消费轨

### 3.3 共用

- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（实验代码不破坏主链）

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
| （待 30 帽） | |

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 | 路径 |
| --- | --- | --- |
| **10 需求帽** | v0.1 初稿 | `docs/harness/invokes/invoke_20260518_10_tech-graph-gate-c-v2-dual-track-requirements.md` |
| **22 R1** | 待 | `docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md`（建议名） |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-18 | 10 帽初稿：闸口 C · D/E 双臂 · 不复跑 A/B |
