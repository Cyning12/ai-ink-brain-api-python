# Task：技术图谱 — 方案2 补全（API 缺口 + 文档对齐 + 可选 MCP/Harness）

> **状态**：`active`（10 帽初稿 · 待 `HG-TASK-DRAFT` / `HG-AUDIT-R1`）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（P2-0～P2-3 · **方案2 核心** + 闸口 B 已签收）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_p4_bc_followup_v1.md`（P2-4 延伸 · 不重复本 task）  
> **关联规划**：`Projects/docs/tech_graph/改进方向.md` **v1.1.3** §方案2；`Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **实现真值（已有）**：`tools/tech_graph_graph_query.py`（`downstream` / `upstream` / `neighbors` + CLI）  
> **闸口 B（已归档 · 勿重做）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md`  
> **test_strategy**：`required`  
> **test_strategy_note**：新增 API 须有 pytest 正反例；文档对齐须链到现有 `test_tech_graph_graph_query.py` 与全量 `pytest` 回归。  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_2`（继承；无 schema 语义变更则不 bump）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/engineering-tech-graph-scheme2-completion-v1`（建议） |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `pending` | `22-R1`, `30` | 10 帽结构化后人扫 task |
| **HG-AUDIT-R1** | `pending` | `30` | R1 零硬阻塞后人签执行 |
| **HG-AUDIT-CLOSE** | `pending` | `done`, `50` | 关账签收 |

> Agent：**不得**代填 `approved`。

---

## 0. 背景与目标

### 0.1 背景

`task_engineering_tech_graph_v2_graph_query_v1` 已交付 **graph_v2 + `tech_graph_graph_query.py` + 闸口 B 定稿**（`HG-P2-3-GATE-B` approved）。相对 `改进方向.md` §方案2 原文，仍有 **API 名/函数表**、**MCP**、**Harness 模板挂钩**、**规划文档勾选** 等缺口；本 task **补全方案2 工程与文档一致性**，**不**重开 graph_v2 主链或闸口实验。

### 0.2 与「对比实验」的关系（必读）

| 层级 | 是否含对比实验 | 说明 |
| --- | --- | --- |
| **`改进方向.md` 总规 R4** | **有** | **闸口 A**（方案1 后）、**闸口 B**（方案2 后）为 **阶段门闸**；已在独立 task / 报告中归档 |
| **本 task** | **无** | **禁止**将闸口 A/B **主实验**纳入范围（继承 **NR-1**）；仅允许引用既有 `conclusion_gate_b_ctx_query_v1_zh.md` |
| **关账口径** | — | 不以「重跑 batch」验收；以 **pytest + 文档对齐 + 可选 MCP 冒烟** 为准 |

### 0.3 目标（完成态）

1. **S2-A**：在 `tech_graph_graph_query.py` 补 **规划层缺口 API**（至少 `has_path`；`describe_impact` 或等价人类可读输出二选一必做）+ pytest。  
2. **S2-B**：**文档对齐**：`scheme_2_graph_query.md` 与 `改进方向.md` §2.3～2.7 反映 **实际模块名/CLI/已实现 op**；§2.7 勾选与「闸口 B 已由 graph_query task 完成」交叉引用。  
3. **S2-C（recommended）**：**MCP 或 Harness 挂钩** 二选一交付（见 §1.1）；未做须在 CLOSE 注明理由。  
4. **不破坏** P2-4：`export --check`、等价、`test_tech_graph_graph_query.py`、manifest 互引 pytest **仍 pass**。

---

## 1. 范围 / 非范围

### 1.1 范围

- [ ] **S2-A · API 补全（必做）**  
  - [ ] `has_path(from_id, to_id) -> bool`（或 CLI 子命令）+ 未知节点 FP-4 行为与现有一致  
  - [ ] `describe_impact(node_id, depth=2)` **或** 文档化「由 `downstream`+`upstream` 子图 JSON 替代」并给 pytest 快照断言（二选一须在 R1 前定稿）  
  - [ ] 可选：`get_all_affected(nodes[], depth)` 薄封装（若与 `tech_graph_gate_b_query_union` 职责重叠则 **非范围** 并写清）  
- [ ] **S2-B · 文档对齐（必做）**  
  - [ ] 更新 `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`：模块名 `tech_graph_graph_query.py`、已实现 op、闸口 B 报告路径（`docs/diary/jsonPKmermaid/reports/…`）  
  - [ ] 更新 `Projects/docs/tech_graph/改进方向.md` §2.3～2.7：与实现一致；§2.7 对 **闸口 B** 项注明 **已完成（graph_query task）** 并链结论 md  
  - [ ] `docs/_tech_graph/graph_v2_schema.md` §9 工具表若有新 CLI 子命令则补一行  
- [ ] **S2-C · 调用面（recommended · 至少一项）**  
  - [ ] **C1**：子仓 `.cursor/mcp.json` 示例 + 最小 MCP 入口（stdio）调用现有 query；**或**  
  - [ ] **C2**：工作区 `docs/harness/prompts/TEMPLATE-task-audit-invoke.md`（或 `22` 审查清单）增 **可选**「影响分析：调用 graph_query CLI」步骤（**禁止**改母版语义为硬阻塞，除非 R1 单列）  

### 1.2 非范围

- **闸口 A / 闸口 B 主实验重跑**（`run_gate_b_batch` 全 arms · NR-1）。  
- **新对比实验计划 / 新 freeze 实验 task**（门闸产物已存在，本 task 只 **引用**）。  
- **方案3 Neo4j**（`改进方向.md` R2）。  
- **graph_v2 schema 语义变更**（`graphs[]` / `ref` / `kind`）。  
- **改 `.github/workflows/`**（新 API 走 pytest；不扩 CI scope）。  
- **退役 `.ai.md`**（G-END-4）。  
- **重命名** `tech_graph_graph_query.py` → `graph_query.py`（除非 R1 明确收益；默认保持现名避免大面积 import 漂移）。

### 1.3 分期建议

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | S2-A + S2-B | **是** |
| **PR-2** | S2-C（可选） | **否**（recommended） |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 方案2 核心（done） | `docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md` |
| 闸口 B 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` |
| 方案2 SPEC | `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| 规划总规 | `Projects/docs/tech_graph/改进方向.md` |
| 查询实现 | `tools/tech_graph_graph_query.py` |
| Harness §5 | `Projects/docs/harness/HARNESS_V2_PLAN.md` §5 |

---

## 3. 验收标准

### 3.1 工程 — S2-A

- [ ] `has_path` 正反例 pytest（含不存在节点 → FP-4）  
- [ ] `describe_impact` 或等价文档化路径 + 可失败断言  
- [ ] `test_tech_graph_graph_query.py` 原有用例 **仍 pass**

### 3.2 文档 — S2-B

- [ ] `scheme_2_graph_query.md` 无「待需求方补充」中与实现冲突的悬空项（或标为 **已实现 / 刻意不做**）  
- [ ] `改进方向.md` §2.7 与 graph_query task 闸口 B 结论 **交叉引用一致**

### 3.3 共用回归

- [ ] `python tools/tech_graph_graph_export.py --check` **PASS**  
- [ ] `python tools/tech_graph_graph_equivalence_check.py` **PASS**  
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` **绿**

### 3.4 S2-C（若做）

- [ ] MCP：本地 `mcp` 或文档化冒烟步骤可复现一次 `downstream` 调用；**或** Harness 模板 PR 可展示 diff  
- [ ] 若 **不做** S2-C：task §6 与 CLOSE 审查写明 **recommended 顺延理由**

---

## 4. failure_paths

| ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- |
| FP-S2-1 | `has_path` 破坏 BFS/ref 语义 | pytest 失败 | 回滚 |
| FP-S2-2 | 误将闸口 B batch 纳入验收 | **拒开工**（scope） | 改 task |
| FP-S2-3 | 文档宣称 MCP 已交付但无入口 | 审查阻塞 | 补实现或改文档 |
| FP-S2-4 | 默认整包 v2 进 prompt | **禁止**（继承 FP-5） | — |

---

## 5. 给执行帽的必读

1. **NR-1**：禁止 `run_gate_b_batch` 全 arms；本 task **不是** 实验 task。  
2. **真值模块名**：`tech_graph_graph_query.py`，勿假设 `graph_query.py` 已存在。  
3. **闸口 B**：只 **引用** `conclusion_gate_b_ctx_query_v1_zh.md`，不重跑。  
4. **工作区文档**（`Projects/docs/tech_graph/`）与子仓代码 **同 PR 或双 PR** 须链在同一个 Harness invoke 中说明。  
5. **FP-4-3**：`ref` 边仍不参与 BFS；`has_path` 与现 query 语义一致。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| **S2-A** | （待填） |
| **S2-B** | （待填） |
| **S2-C** | （待填） |

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 |
| --- | --- |
| **10 需求帽** | （待 invoke） |
| **22 R1** | （待） |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-18 | 10 帽初稿：方案2 补全；明确无新对比实验 |
