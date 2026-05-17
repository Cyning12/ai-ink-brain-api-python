# Task：技术图谱 — graph_v2 扩展（P2-4）与闸口 B follow-up 切片

> **状态**：`done（2026-05-17 · P2-4a 验收通过）`  
> **终轮审查**：`docs/harness/reviews/task_engineering_tech_graph_v2_p4_extended_v1_audit_CLOSE_20260517.md`  
> **关闭回溯**：见终轮审查 **「执行路线与 Commit 回溯」**  
> **前置 task（done）**：`docs/tasks/done/task_engineering_tech_graph_v2_graph_query_v1.md`（P2-0～P2-3 · 闸口 B 已签收）  
> **关联规划**：`docs/tech_graph/改进方向.md` **v1.1.3**；`docs/_tech_graph/graph_v2_schema.md`  
> **test_strategy**：`required`  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_2`  
> **Harness 通则**：`Projects/docs/harness/prompts/HANDOFF_SEMI_AUTO.md`、`HANDOFF_CLOSE_TRACE.md`

### Harness 元信息（半自动 · `post_close`）

| 字段 | 值 |
| --- | --- |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/engineering-tech-graph-v2-p4-extended-v1` |

#### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | — | — |
| **HG-AUDIT-R1** | `approved` | — | — |
| **HG-AUDIT-CLOSE** | `pending` | `50` | **终轮 CLOSE 已落盘**；人签后合并 PR |

---

## 0. 背景与目标

前置 CLOSE（graph_query task）将 **P2-4** 延后至本 task。本轮回合交付 **P2-4a only**；**P2-4b / P2-4c** 未做（见 §1.1）。

---

## 1. 范围 / 非范围

### 1.1 范围（签收范围）

- [x] **P2-4a**：`kind` + `graphs[]` + `edges[].ref` schema/导出/等价/query 回归  
- [ ] **P2-4b**（未做 · follow-up）  
- [ ] **P2-4c**（未做 · follow-up）

### 1.2 非范围

闸口 A/B 主实验重跑、整包 v2 默认、退役 `.ai.md`、Neo4j、graph_query 多分图默认等 — 见归档全文 active 版 §1.2。

---

## 2. 验收标准（摘要）

§3.1 **P2-4a 全勾** · 40 自检 2026-05-17 pass · freeze `V2_2`。详见终轮审查与下文自检节。

---

## 3. 实现备忘

| 项 | 内容 |
| --- | --- |
| **P2-4a** | `tools/tech_graph_graph_v2_schema.py`；`tests/test_tech_graph_graph_v2_p4_*.py`；`graph.json` 含 `graphs[]` |
| **freeze** | `TECH_GRAPH_S2_FREEZE_20260517_V2_2` |
| **follow-up** | 4b manifest 互引；4c 闸口 B query 种子 |

### 自检结论（执行者）

**40 自检 · 2026-05-17 pass** — export / 等价 / P2-4 pytest 9 passed / graph_query 8 passed / 全量 **176 passed**。证据见关账前 task v0.5 与 `invoke_20260517_40_tech-graph-v2-p4-a2-self-check.md`。

---

## 4. 审查与交接（Harness）

| 轮次 | 状态 |
| --- | --- |
| 10 / 22 R1 / 30 P2-4a / 40 自检 | 完成 |
| **22 CLOSE** | `…_audit_CLOSE_20260517.md` |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1～v0.5 | 2026-05-17 | 见 git 历史（active 阶段） |
| v1.0 | 2026-05-17 | **done 归档** · CLOSE 签收 P2-4a only |
