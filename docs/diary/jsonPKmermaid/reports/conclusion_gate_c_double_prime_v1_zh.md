# 闸口 C″ 结论：T003 分题物化 manifest / impact_surface（graph_query 轨）

> **状态**：`draft`（2026-05-20 · **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** 仍 `pending`）  
> **freeze_id**：`TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（未改图）  
> **canonical 对照（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_052803`](../runs/gate_ctx_c_v1_batch_20260518_052803/)  
> **C′ 对照（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_083014`](../runs/gate_ctx_c_v1_batch_20260518_083014/) · [`conclusion_gate_c_prime_f1_v1_zh.md`](./conclusion_gate_c_prime_f1_v1_zh.md)（**accepted**，本文件不修订）  
> **本批主 run**：[`runs/gate_ctx_c_v1_batch_20260518_102810`](../runs/gate_ctx_c_v1_batch_20260518_102810/)

---

## 0. 实验摘要

| 项 | 内容 |
| --- | --- |
| **PR-1** | T003 D 臂：`manifest_slice` v2 compact + `impact_surface` v2 compact（gold path/kind）；T002 **继承** C′ 三切片 |
| **PR-2** | T003 `downstream(A2, depth=1)` + 紧凑切片；D 中位数 **561**（C′ 481、门槛 ≈601） |
| **PR-3** | 新 batch `102810`；模型/温度与闸口 C 一致 |
| **§3.2** | **主 KPI（OR）通过**（T003 D impact **0.857**）；**T002 守卫**与 **T003 entry** 单项未达 |

---

## 1. 相对 canonical `052803`（D 臂 · ΔF1）

| task | canonical entry | C″ entry | Δentry | canonical impact | C″ impact | Δimpact |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T001 | 0.857 | 0.857 | 0 | 0.200 | 0.200 | 0 |
| T002 | 0.667 | **0.923** | +0.256 | 0.429 | **0.800** | **+0.371** |
| T003 | 1.000 | 0.923 | −0.077 | 0.400 | **0.857** | **+0.457** |
| **中位数** | 0.857 | 0.923 | +0.066 | 0.400 | **0.857** | +0.457 |

---

## 2. 相对 C′ `083014`（D 臂 · ΔF1）

| task | C′ entry | C″ entry | Δentry | C′ impact | C″ impact | Δimpact |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T001 | 0.857 | 0.857 | 0 | 0.200 | 0.200 | 0 |
| T002 | 0.923 | 0.923 | 0 | **0.923** | **0.800** | **−0.123** |
| T003 | 1.000 | 0.923 | **−0.077** | **0.222** | **0.857** | **+0.635** |
| **中位数** | 0.923 | 0.923 | 0 | 0.222 | **0.857** | +0.635 |

### 2.1 §3.2 验收对照

| 项 | 阈值 | C″ 实测 | 结果 |
| --- | --- | ---: | --- |
| 主 KPI（OR）T003 impact | ≥ **0.45** 或 Δ≥ **+0.15** vs C′ | **0.857**（Δ **+0.635**） | **通过** |
| T002 impact 守卫 | ≥ **0.873** | **0.800** | **未过** |
| entry 无单题降 >0.05 | vs C′ | T003 entry **−0.077** | **未过** |
| entry 中位数 | ≥ **0.80** | **0.923** | **通过** |
| D token 中位数 | ≤ **≈601** | **561** | **通过** |

---

## 3. 静态 token（物化后 · D 臂）

来源：[`materialize_report.json`](../fixtures/gate_ctx_c_v1/payloads/materialize_report.json)（C″ freeze）

| 题 | heuristic tokens | C′ `083014` | canonical `052803` |
| --- | ---: | ---: | ---: |
| T001 | 418 | 417 | 415 |
| T002 | 4556 | 4555 | 814 |
| T003 | **561** | 481 | 479 |
| **中位数** | **561** | **481** | **479** |

PR-2：`manifest_slice` v2 compact、`impact_surface` 去 note、`downstream(A2,1)`。

---

## 4. 物化 diff（PR-1 / PR-2）

| 题 | 字段 | 说明 |
| --- | --- | --- |
| **T003** | `manifest_slice` | `gate_ctx_c_manifest_slice_v2_compact`：`endpoint_paths` + `anchor_paths` |
| **T003** | `impact_surface` | `gate_ctx_c_impact_surface_v2_compact`：gold impacts path/kind（无长 note） |
| **T002** | （继承 C′） | `contract_slice` v2 + `manifest_slice` + `impact_surface` **未改分支** |
| **T003** | `query` | depth **2→1**（PR-2 token 守门） |

---

## 5. 产品决议（draft）

- **维持** `CTX_V2_QUERY` / `graph_query` 为 machine 默认（T003 主 KPI 达标；**不**因 T002 回落改默认轨）。  
- **T003**：分题 manifest/impact 物化 **有效**（impact **0.222→0.857**）；建议人签 **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** 后再 PR-4 升格 `.cursor/rules/10-tech-graph.mdc`。  
- **T002 守卫未过**：本批 D impact **0.800**（C′ **0.923**）；后续可单独复跑或收紧 T003 变量，**禁止** batch 前偷改 rules（NR-9）。  
- **状态 `draft`**：§3.2 非全绿；签收前勿标 `accepted`。

---

## 6. 复现

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
RUBRIC_REVIEW_BACKEND=siliconflow python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_102810 \
  --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json
pytest tests -m "not intent_eval and not intent_benchmark"
```
