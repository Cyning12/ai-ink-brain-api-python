# Task：技术图谱 — 方案2 补全（API 缺口 + 文档对齐 + 可选 MCP/Harness）

> **状态**：`active`（**v0.2** · S2-A/B 已交付 · 待关账 `HG-AUDIT-CLOSE` 人签）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（P2-0～P2-3 · **方案2 核心** + 闸口 B 已签收）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_p4_bc_followup_v1.md`（P2-4 延伸 · 不重复本 task）  
> **关联规划**：`Projects/docs/tech_graph/改进方向.md` **v1.1.3** §方案2；`Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`  
> **实现真值（已有）**：`tools/tech_graph_graph_query.py`（`downstream` / `upstream` / `neighbors` + CLI）  
> **闸口 B（已归档 · 勿重做）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md`  
> **test_strategy**：`required`  
> **test_strategy_note**：`has_path` / `describe_impact` 须 **先** 在 `tests/test_tech_graph_graph_query.py` 写可失败用例再实现；文档对齐后全量 `pytest tests -m "not intent_eval and not intent_benchmark"` 回归。  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_2`（继承；无 schema 语义变更则不 bump）  
> **gates_before_code**：`failure_paths`、`test_strategy`、`freeze_id`、§0.4 矛盾裁定、§2 API 映射表  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`  
> **需求帽 invoke**：`docs/harness/invokes/invoke_20260518_10_tech-graph-scheme2-completion-requirements.md`

### Harness 元信息

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/engineering-tech-graph-scheme2-completion-v1` |

#### 人工闸 `human_gate`（初值 · **仅人**可改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `22-R1`, `30` | v0.2 结构化后人扫 task |
| **HG-AUDIT-R1** | `approved` | `30` | R1 零硬阻塞后人签执行 |
| **HG-AUDIT-CLOSE** | `approved` | `done`, `50` | 关账签收 |

> Agent：**不得**代填 `approved`。下一帽 ∈ `blocks_hats` 且 `pending` 时 **拒执行**。

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

1. **S2-A**：在 `tech_graph_graph_query.py` 补 **`has_path`**、**`describe_impact`**（见 §0.5 裁定）+ pytest。  
2. **S2-B**：**文档对齐**：`scheme_2_graph_query.md` 与 `改进方向.md` §2.3～2.7 反映 **实际模块名/CLI/已实现 op**；§2.7 勾选与闸口 B 结论交叉引用。  
3. **S2-C（recommended）**：**MCP 或 Harness 挂钩** 二选一（见 §1.1）；未做须在 CLOSE 注明理由。  
4. **不破坏** P2-4：`export --check`、等价、`test_tech_graph_graph_query.py`、manifest 互引 pytest **仍 pass**。

### 0.4 文档矛盾与真值裁定（10 帽 · 不做和稀泥）

| ID | 矛盾 A（出处） | 矛盾 B（出处） | **裁定（本 task 真值）** |
| --- | --- | --- | --- |
| **C-1** | 模块 `tools/graph_query.py`（`改进方向.md` §2.3～2.4、§2.7） | 已实现 `tools/tech_graph_graph_query.py`（graph_query task · 本仓代码） | **保持现模块名**；S2-B 将规划/SPEC 改为 `tech_graph_graph_query.py`；**禁止**为对齐规划而重命名文件（§1.2 NR-重命名） |
| **C-2** | 函数名 `get_downstream` / `get_upstream`（规划表） | 实现 `query_downstream` / `query_upstream`（`tech_graph_graph_query.py`） | **实现名不变**；文档用 §2 **映射表** 标注「规划别名 → 实现符号」 |
| **C-3** | `scheme_2_graph_query.md`「待需求方补充」模块名/CLI | 已交付 `downstream`/`upstream`/`neighbors` CLI | S2-B **删除或改写**悬空项为 **已实现**；闸口 B 路径指向子仓 `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` |
| **C-4** | `改进方向.md` §2.6「Harness 强制步骤」 | 本 task S2-C 为 **recommended** | **不**在 R1 前把母版 `TEMPLATE-task-audit-invoke.md` 改为硬阻塞；若做 S2-C 仅增 **可选** 步骤（C2） |
| **C-5** | `get_all_affected(nodes[], depth)`（规划 §2.3） | `tools/tech_graph_gate_b_query_union.py`（P2-4c · done） | **非范围**于 `tech_graph_graph_query.py`；多起点并集 **引用** gate_b union 模块，见 §1.2 |

### 0.5 S2-A 设计裁定（v0.2 锁定 · R1 可审不可默改）

| 项 | 裁定 |
| --- | --- |
| **`has_path(from_id, to_id) -> bool`** | 有向路径存在性；**复用** `_bfs_reachable` / `store.downstream`；**`ref` 边不参与**（与现 query 一致）；未知节点 → **FP-4**（`EXIT_FP4`）；CLI 增加 `op` 或子命令 `has-path` |
| **`describe_impact(node_id, depth=2) -> str`** | **必做实现**（非「仅文档化 JSON 替代」）；内部组合 `query_downstream` + `query_upstream` 结果格式化为人类可读字符串（禁止第三套独立 BFS 语义）；pytest 对固定 fixture 图断言子串（直接/间接影响节点 id 或 label） |
| **`get_all_affected`** | **不做**于本模块；见 **C-5** |

---

## 1. 范围 / 非范围

### 1.1 范围

- [x] **S2-A · API 补全（必做）**  
  - [x] `has_path(from_id, to_id) -> bool` + CLI + pytest（含 FP-4、正反例路径）  
  - [x] `describe_impact(node_id, depth=2) -> str` + CLI + pytest（§0.5）  
  - [x] `tests/test_tech_graph_graph_query.py` 扩展；**原有用例仍 pass**  
- [x] **S2-B · 文档对齐（必做）**  
  - [x] 更新 `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`：真值模块名、op 表、CLI 示例、闸口 B 报告路径  
  - [x] 更新 `Projects/docs/tech_graph/改进方向.md` §2.3～2.7：与 §2 映射表及实现一致；§2.7 **闸口 B** 项标 **已完成（graph_query task）** 并链 `conclusion_gate_b_ctx_query_v1_zh.md`  
  - [x] `docs/_tech_graph/graph_v2_schema.md` §9 工具表：新增 `has-path` / `describe-impact` 各一行  
- [x] **S2-C · 调用面（recommended · 至少一项）**  
  - [x] **C1**：子仓 `.cursor/mcp.json.example`（downstream 示例）  
  - [x] **C2**：工作区 `TEMPLATE-task-audit-invoke.md` 可选影响分析步骤

### 1.2 非范围

- **闸口 A / 闸口 B 主实验重跑**（`run_gate_b_batch` 全 arms · **NR-1**）。  
- **新对比实验 / 新 freeze 实验 task**（仅引用既有门闸文档）。  
- **方案3 Neo4j**（`改进方向.md` R2）。  
- **`graph_v2` schema 语义变更**（`graphs[]` / `ref` / `kind`）。  
- **改 `.github/workflows/`**（新 API 仅 pytest 覆盖）。  
- **退役 `.ai.md`**（G-END-4）。  
- **重命名** `tech_graph_graph_query.py` → `graph_query.py`（**NR-重命名**）。  
- **`get_all_affected` / 多起点并集** 在 query 模块内重做（**NR-union**：用 `tech_graph_gate_b_query_union.py`）。

### 1.3 分期建议

| 切片 | 内容 | 阻塞关账 |
| --- | --- | --- |
| **PR-1** | S2-A + S2-B | **是** |
| **PR-2** | S2-C（recommended） | **否** |

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 方案2 核心（done） | `docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md` |
| P2-4 并集（done · 非本模块重做） | `docs/tasks/done/task_engineering_tech_graph_v2_p4_bc_followup_v1.md` · `tools/tech_graph_gate_b_query_union.py` |
| 闸口 B 结论 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` |
| 方案2 SPEC | `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| 规划总规 | `Projects/docs/tech_graph/改进方向.md` |
| 查询实现 | `tools/tech_graph_graph_query.py` |
| 单测 | `tests/test_tech_graph_graph_query.py` |
| Harness §5 | `Projects/docs/harness/HARNESS_V2_PLAN.md` §5 |

### 2.1 规划别名 → 实现符号（文档对齐用）

| 规划（`改进方向.md` §2.3） | 实现（`tech_graph_graph_query.py`） | 状态 |
| --- | --- | --- |
| `get_downstream(node, depth)` | `query_downstream(store, node_id, depth)` → JSON 子图 | **已有** |
| `get_upstream(node, depth)` | `query_upstream(store, node_id, depth)` | **已有** |
| — | `query_neighbors(store, node_id)` | **已有**（规划未单列） |
| `has_path(from, to)` | `has_path` | **已有** |
| `describe_impact(node)` | `describe_impact` | **已有** |
| `get_all_affected(nodes[], depth)` | `tech_graph_gate_b_query_union` 等 | **非本模块**（C-5） |

### 2.2 CLI 真值（当前 + 本 task 扩展）

```text
# 已有
python tools/tech_graph_graph_query.py downstream <node_id> <depth>
python tools/tech_graph_graph_query.py upstream <node_id> <depth>
python tools/tech_graph_graph_query.py neighbors <node_id>

# 本 task 新增（命名以执行帽实现为准，审查须与 §9 工具表一致）
python tools/tech_graph_graph_query.py has-path <from_id> <to_id>
python tools/tech_graph_graph_query.py describe-impact <node_id> [depth]
```

---

## 3. 验收标准

### 3.1 工程 — S2-A

- [x] `has_path`：pytest 覆盖 **存在路径 / 不存在路径 / 未知节点 → exit 4（FP-4）**  
- [x] `describe_impact`：pytest 对 fixture 图 **可失败** 断言输出含预期节点语义  
- [x] `pytest tests/test_tech_graph_graph_query.py` **绿**（含新增 + 原有）

### 3.2 文档 — S2-B

- [x] `scheme_2_graph_query.md` 无与实现冲突的「待补充」悬空项  
- [x] `改进方向.md` §2.7 闸口 B 与 `conclusion_gate_b_ctx_query_v1_zh.md` **一致**  
- [x] 读者仅读工作区文档即可得到正确模块名 **`tech_graph_graph_query.py`**（非 `graph_query.py`）

### 3.3 共用回归（命令化）

- [x] `python tools/tech_graph_graph_export.py --check` → exit 0  
- [x] `python tools/tech_graph_graph_equivalence_check.py` → exit 0  
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` → 绿  

### 3.4 S2-C（若做）

- [x] MCP 示例（`.cursor/mcp.json.example`）+ Harness 模板可选步骤（C1+C2）  
- [x] 未顺延

---

## 4. failure_paths

| ID | 触发 | 行为 | 可重试 | 用户/Agent 可见 |
| --- | --- | --- | --- | --- |
| FP-S2-1 | `has_path` 破坏 BFS/`ref` 跳过语义 | pytest 失败 | 回滚实现 | CI / 本地 pytest |
| FP-S2-2 | 误将闸口 B batch 纳入验收 | **拒开工**（scope） | 改 task | 审查/执行帽 |
| FP-S2-3 | 文档宣称 MCP 已交付但无入口 | R1/CLOSE **阻塞** | 补实现或改文档 | 审查清单 |
| FP-S2-4 | 默认整包 v2 进 prompt | **禁止**（继承 FP-5） | — | query 模块 exit 5 |
| FP-S2-5 | `has_path` 未知 `from_id`/`to_id` | stderr + **exit 4**（FP-4） | 修正 id | 与现 `downstream` 一致 |
| FP-S2-6 | 非 graph_v2 图文件 | **exit 5**（FP-5） | 先 export 升版 | 与现 loader 一致 |

---

## 5. 给执行帽的必读

1. **NR-1**：禁止 `run_gate_b_batch` 全 arms；本 task **不是** 实验 task。  
2. **真值模块名**：`tech_graph_graph_query.py`；勿创建 `graph_query.py`（**C-1**）。  
3. **闸口 B**：只 **引用** `conclusion_gate_b_ctx_query_v1_zh.md`，不重跑。  
4. **工作区文档**（`Projects/docs/tech_graph/`）与子仓代码 **同 PR 或双 PR**；invoke/审查中写明 PR 关系。  
5. **`ref` 边**：不参与 BFS；`has_path` 与 `query_*` 语义一致。  
6. **`test_strategy: required`**：新增 API **先红测再绿**（或同 PR 内可见测试先于实现提交）。  
7. **§0.5**：`describe_impact` 必须实现为 **str**，不得仅用「调用 downstream JSON」代替而无格式化函数。

---

### 自检结论（执行者）

> **40 帽复检**：2026-05-18 · invoke `docs/harness/invokes/invoke_20260518_40_tech-graph-scheme2-completion-self-check.md`

| 验收块 | 结果 | 证据摘要 |
| --- | --- | --- |
| §3.1 S2-A | pass | `pytest tests/test_tech_graph_graph_query.py` → **16 passed** |
| §3.2 S2-B | pass | 工作区 `scheme_2_graph_query.md`、`改进方向.md` §2.3～2.7；子仓 `graph_v2_schema.md` §9 |
| §3.3 回归 | pass | 见下表命令与退出码 |
| §3.4 S2-C | pass | C1 `.cursor/mcp.json.example` + C2 `TEMPLATE-task-audit-invoke.md` 可选节 |

**命令（cwd=`ai-ink-brain-api-python`）**

| 命令 | 退出码 |
| --- | --- |
| `pytest tests/test_tech_graph_graph_query.py -q` | 0（16 passed） |
| `python tools/tech_graph_graph_export.py --check` | 0 |
| `python tools/tech_graph_graph_equivalence_check.py` | 0 |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0（184 passed, 1 skipped；40 帽复检 ~92s） |

**已知未测**：仓内 `has-path AUTH RAG` 在真实拓扑上可为 false（与 golden fixture 不同）；CLI 用例以 `--graph` fixture 覆盖。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| **S2-A** | `has_path` / `describe_impact` in `tools/tech_graph_graph_query.py`；CLI `has-path` / `describe-impact`；pytest `tests/test_tech_graph_graph_query.py` 新增 ~8 用例 |
| **S2-B** | 工作区 `docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md`、`改进方向.md` §2.3～2.7；子仓 `docs/_tech_graph/graph_v2_schema.md` §9 |
| **S2-C** | C1 `.cursor/mcp.json.example`；C2 `docs/harness/prompts/TEMPLATE-task-audit-invoke.md` 可选影响分析 |

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 | 路径 |
| --- | --- | --- |
| **10 需求帽** | v0.2 完成 | `docs/harness/invokes/invoke_20260518_10_tech-graph-scheme2-completion-requirements.md` |
| **22 R1** | 待（`HG-TASK-DRAFT` 后人扫） | `docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md`（建议名） |

### Invoke 快照（可选索引）

- 10：`docs/harness/invokes/invoke_20260518_10_tech-graph-scheme2-completion-requirements.md`
- 22 R1：`docs/harness/invokes/invoke_20260518_22_tech-graph-scheme2-completion-audit-r1.md`
- 30：`docs/harness/invokes/invoke_20260518_30_tech-graph-scheme2-completion-execute.md`
- 40：`docs/harness/invokes/invoke_20260518_40_tech-graph-scheme2-completion-self-check.md`

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-18 | 10 帽初稿：方案2 补全；明确无新对比实验 |
| v0.2 | 2026-05-18 | 10 帽结构化：§0.4 矛盾裁定、§0.5 S2-A 锁定、`§2.1` 映射表、命令化验收、`gates_before_code`；`describe_impact` 必做实现 |
