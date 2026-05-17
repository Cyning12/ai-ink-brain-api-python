# Task：技术图谱 — graph_v2 扩展（P2-4）与闸口 B follow-up 切片

> **状态**：`draft`（待 **10 需求帽** 结构化 + **22 R1** 书面审）  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（P2-0～P2-3 · 闸口 B 已签收）  
> **终轮关账参考**：`docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_CLOSE_20260517.md`  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**；`docs/_tech_graph/graph_v2_schema.md`  
> **闸口 B follow-up（可选本 task 子阶段）**：`docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` §5.4（T002 类加深 query/manifest）  
> **test_strategy**：`required`  
> **test_strategy_note**：schema 扩展与等价/query 回归须 pytest + `export --check`；禁止无测试扩 `graphs[]`/`ref`。  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_TBD`（P2-4 首 PR 前与 `protocol_version.yaml` · `graph_v2_freeze_id` 对齐 bump）  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_AUTO_COMMIT.md`、`HANDOFF_CLOSE_TRACE.md`

### Harness 元信息（半自动 · `post_close`）

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/engineering-tech-graph-v2-p4-extended-v1` |

#### 人工闸 `human_gate`（初值 · 人审后改 `approved`）

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `pending` | `22-R1`, `30` | 本草案人扫或 10 帽结构化后改 `approved` |
| **HG-AUDIT-R1** | `pending` | `30` | R1 审查落盘后改 `approved` |
| **HG-AUDIT-CLOSE** | `pending` | `done`, `50` | 关账签收 |

---

## 0. 背景与目标

**背景**：前置 task 已交付 **P2-0 最小 graph_v2**、`graph_query`、闸口 B（**CTX_QUERY** 默认 · B-1 部分满足已人签）。**P2-4 字段**（`graphs[]`、`edges[].ref`、`nodes[].kind`、manifest↔node 互引）与 **闸口 B §5.4 follow-up** 明确延后。

**目标（完成态）**：

1. 在 **不破坏** 现有单图 `graph_query` 与等价 CI 的前提下，扩展 **graph_v2** 导出与 schema，支持 P2-4 最小可用子集（见 §2.1 分期）。  
2. （可选 **P2-4b**）针对闸口 B T002 类契约题，补 **query 种子 / manifest 切片** 策略并落盘可复现说明（**不**重跑闸口 A/B 主实验）。  
3. 更新 `graph_v2_schema.md`、等价检查、pytest；`export --check` 与 `tech-graph.yml` 仍绿。

---

## 1. 范围 / 非范围

### 范围

- [ ] **P2-4a**：`nodes[].kind`（枚举或字符串 · 与 `01_struct` 对齐的草案）  
- [ ] **P2-4a**：`graphs[]` 多分图元数据 + 导出器/校验器（**禁止** 破坏默认单图 query 路径）  
- [ ] **P2-4a**：`edges[].ref`（跨分图引用 · 最小语义 + 校验）  
- [ ] **P2-4b（可选）**：`_manifest` / `_contract` 与 graph `node id` 互引字段或脚本校验  
- [ ] **P2-4c（可选）**：闸口 B follow-up — `query_seeds` 增 `upstream`/`neighbors` 组合；**不重跑** NR-1 整包对比  
- [ ] 等价门禁阈值延续或 **书面 bump**（附 `freeze_id`）  
- [ ] `.cursor/rules/10-tech-graph.mdc` 增量（若消费路径变更）

### 非范围

- **闸口 A / 闸口 B 主实验重跑**（NR-1；结论以 `conclusion_gate_*` 为准）。  
- **默认整包 v1/v2 替 `*.ai.md`**（G-END-5；FP-5）。  
- **退役 `.ai.md` 为维护源**（G-END-4 未满足）。  
- **方案3 Neo4j**（`改进方向.md` R2 · 单独立项）。  
- **跨会话长期记忆 / 向量库**（前置 task NR-5）。  
- **`01_struct` / `99_spec` 全文并入单一 `graph.json`**（可另立 struct 切片 task）。

---

## 2. 依赖与引用

| 依赖 | 路径 |
| --- | --- |
| 前置 done task | `docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md` |
| v2 schema（P2-0） | `docs/_tech_graph/graph_v2_schema.md` |
| 导出 / 等价 / query | `tools/tech_graph_graph_export.py`、`tech_graph_graph_equivalence_check.py`、`tech_graph_graph_query.py` |
| 治理层 | `docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md` |
| PROJECT_CONFIG | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| Harness §5 | `Projects/docs/harness/HARNESS_V2_PLAN.md` §5 |

### 2.1 分期建议（10 帽 / R1 可调整）

| 阶段 | 交付 | 备注 |
| --- | --- | --- |
| **P2-4a** | `kind` + `graphs[]` + `ref` 最小 schema/导出/等价 | **阻塞** query 扩展若破坏 FP-5 |
| **P2-4b** | manifest↔node 互引（若纳入范围） | 可与 4a 同 PR 或拆分 |
| **P2-4c** | 闸口 B follow-up 种子/文档 | **recommended** 非阻塞关账 |

---

## 3. 验收标准

### 3.1 工程

- [ ] `graph.json` 含 P2-4a 字段时 `schema_version` 仍为 `graph_v2`；`python tools/tech_graph_graph_export.py --check` **PASS**  
- [ ] 等价检查 CI **PASS**（阈值见 schema；变更须文档化）  
- [ ] 现有 `graph_query` 单图路径 **回归绿**（`tests/test_tech_graph_graph_query.py`）  
- [ ] pytest VERIFY：`pytest tests -m "not intent_eval and not intent_benchmark"` **PASS**  
- [ ] **禁止** 无 `graphs[]`/`ref` 时静默忽略校验失败

### 3.2 文档

- [ ] `graph_v2_schema.md` 更新 P2-4 字段表  
- [ ] task §9 回填路径与 invoke 链

---

## 4. failure_paths

| ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- |
| FP-4-1 | P2-4 字段与 P2-0 最小集冲突未迁移 | 等价非 0；列差异 | 修 schema/导出 |
| FP-4-2 | `ref` 指向未知 graph/节点 | 校验非 0 | 修源图 |
| FP-4-3 | query 在 v2 无 P2-4 扩展时误读多分图 | **禁止**；单图路径不变 | — |
| FP-5 | 沿用前置 | v1 整包禁止作 query 默认 | — |

---

## 5. 给执行帽的必读列表

1. 前置 task **§0.2 NR-1～7** 仍有效。  
2. **P2-0 禁止项** 仅在 P2-4a **显式升级** 后解除；不得一次 PR 塞满所有 P2-4 幻想字段。  
3. 闸口 B **§5.4** — follow-up 是 **加深 query**，非重开 B 主实验。  
4. 合并前 **freeze_id** bump 与 `protocol_version.yaml` 对齐。

---

## 6. 实现备忘（执行 Agent 回填）

| 项 | 内容 |
| --- | --- |
| （待填） | |

---

## 7. 审查与交接（Harness）

| 轮次 | 状态 | 下一棒 |
| --- | --- | --- |
| **草案** | 本文件 v0.1 | **10 需求帽** → **22 R1** → **30** |
| **invoke（需求）** | 待落盘 | `docs/harness/invokes/invoke_*_10_tech-graph-v2-p4-requirements.md` |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-05-17 | 初稿：P2-4 扩展 + 可选闸口 B follow-up；链前置 done task |

---

## 给 Cursor

`P2-4`、`graphs[]`、`edges[].ref`、`nodes[].kind`、`graph_v2`、前置 task done、`HANDOFF_SEMI_AUTO`、`human_gate`、`HG-TASK-DRAFT`
