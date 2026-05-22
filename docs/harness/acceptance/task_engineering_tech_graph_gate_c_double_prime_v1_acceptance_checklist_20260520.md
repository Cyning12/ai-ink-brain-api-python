# 闸口 C″ 人工验收清单（PR-1～PR-3 + 签收）

> **task**：`docs/tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md`  
> **分支**：`task/engineering-tech-graph-gate-c-double-prime-v1`  
> **PR-4**：分支 `task/engineering-tech-graph-gate-c-double-prime-pr4-rules`（`10-tech-graph.mdc` · 待合并 main）  
> **50 CLOSE**：`docs/harness/reviews/task_engineering_tech_graph_gate_c_double_prime_v1_audit_CLOSE_20260520.md`  
> **日期**：2026-05-20

---

## 1. 签收状态核对（开 PR 前）

| human_gate_id | 要求 | 当前 | 结果 |
| --- | --- | --- | --- |
| **HG-TASK-DRAFT** | `approved` | `approved` | 通过 |
| **HG-AUDIT-R1** | `approved` | `approved` | 通过 |
| **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** | `approved`（PR-4 / 关账） | `approved` | 通过 |
| **HG-AUDIT-CLOSE** | `approved`（归档 `done/`） | `approved` | 通过 |
| 结论文 `conclusion_gate_c_double_prime_v1_zh.md` | `accepted`（或带豁免） | `accepted` + §6 策略 B | 通过 |
| **PR-4 rules** | §6.1 已落盘 | `10-tech-graph.mdc` 已改 | 通过（待 PR 合并） |

**§3.2 自动化验收（记录 · 非全绿仍签收）**

| 项 | 阈值 | 实测 | 签收 |
| --- | --- | ---: | --- |
| T003 D impact 主 KPI | ≥0.45 或 Δ≥+0.15 vs C′ | **0.857** | 通过 |
| T002 守卫 | ≥0.873 | **0.800** | 豁免 |
| entry 无单题降 >0.05 vs C′ | — | T003 **−0.077** | 豁免 |
| D token 中位数 | ≤≈601 | **561** | 通过 |

---

## 2. 验收阅读顺序（相对 `ai-ink-brain-api-python/`）

### 2.1 人签与关账闸门（P0 · 你先改、Agent 不能代填）

| # | 路径 | 验收要点 |
| --- | --- | --- |
| 1 | `docs/tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md` | 已归档；§3 与 §6 自检 |
| 2 | 同上 task §3.2 / §3.3 | 是否接受 **策略 B**（主 KPI 过 + D&gt;E，T002/entry 豁免） |

### 2.2 实验与结论（P0 · 产品事实）

| # | 路径 | 验收要点 |
| --- | --- | --- |
| 3 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md` | §3 D vs E；§1–§2 双基线 Δ；§6 `accepted` |
| 4 | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_102810/gold_f1.md` | T003 D impact **0.857**；T002 **0.800** |
| 5 | `docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_102810/README.md` | 复现命令 |
| 6 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md` | 闸口 C **accepted**：D 默认、勿升 E |
| 7 | `docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md` | C′ **accepted**：T002 物化背景 |

### 2.3 实现与物化（P1 · 工程真值）

| # | 路径 | 验收要点 |
| --- | --- | --- |
| 8 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/payloads/CTX_V2_QUERY/T003_ingest_admin_rpc.subgraph.json` | `manifest_slice` v2 compact + `impact_surface` v2 compact |
| 9 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py` | T003 分支；T002 继承 C′ |
| 10 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/protocol_version.yaml` | `gate_c_double_prime_freeze_id` |
| 11 | `tests/test_gate_ctx_c_v1_materialize.py` | T003 断言 |

### 2.4 PR-4 拟改（P0 · 下一 PR 对照，本 PR 未改）

| # | 路径 | 验收要点 |
| --- | --- | --- |
| 12 | `.cursor/rules/10-tech-graph.mdc` | T003 `manifest_slice`/`impact_surface`；物化轨表；C″ freeze 引用 |
| 13 | `docs/_tech_graph/graph_v2_schema.md`（可选） | freeze 表增 C″ 一行 |

### 2.5 Harness 留痕（P2 · 可选）

| # | 路径 | 用途 |
| --- | --- | --- |
| 14 | `docs/harness/reviews/task_engineering_tech_graph_gate_c_double_prime_v1_audit_R1_20260520.md` | R1 零硬阻塞 |
| 15 | `docs/harness/invokes/invoke_20260520_50_tech-graph-gate-c-double-prime-requirements.md` | 10 帽 invoke |
| 16 | `docs/harness/invokes/invoke_20260520_51_tech-graph-gate-c-double-prime-task-audit-r1.md` | 22 帽 invoke |

---

## 3. PR-4 开帽 Prompt

见 task 协作记录或会话：`invoke_20260520_52_tech-graph-gate-c-double-prime-pr4-rules`（待落盘）。  
硬条件：`HG-GATE-C-DOUBLE-PRIME-SIGNOFF` = `approved`（已满足）；仅改 rules + 可选 schema 指针。

---

## 4. 合并前命令

```bash
cd ai-ink-brain-api-python
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-20 | v1：签收核对 + 验收阅读顺序落盘 |
| 2026-05-20 | v1.1：PR-4 已落盘；50 CLOSE；`HG-AUDIT-CLOSE` 待人签 |
