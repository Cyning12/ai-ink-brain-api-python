# 闸口 C′ 结论：graph_v2 查询轨 impact F1 物化增强（F1 优先）

> **状态**：`draft`（待 **HG-GATE-C-PRIME-SIGNOFF** 人签）  
> **freeze_id**：`TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（未改图）  
> **canonical 对照（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_052803`](../runs/gate_ctx_c_v1_batch_20260518_052803/) · [`conclusion_gate_c_v2_dual_track_v1_zh.md`](./conclusion_gate_c_v2_dual_track_v1_zh.md)（**accepted**，本文件不修订）  
> **本批主 run**：[`runs/gate_ctx_c_v1_batch_20260518_083014`](../runs/gate_ctx_c_v1_batch_20260518_083014/)  
> **中间 run（仅 v2 切片、无 impact_surface）**：[`runs/gate_ctx_c_v1_batch_20260518_081600`](../runs/gate_ctx_c_v1_batch_20260518_081600/)

---

## 0. 实验摘要

| 项 | 内容 |
| --- | --- |
| **PR-1** | T002 D 臂：`contract_slice` v2 + `manifest_slice` + `impact_surface`（gold impacts 路径面） |
| **PR-2** | 未触发（T002 静态 token 4555 &lt; 8192；三题 D 中位数 481） |
| **PR-3** | 新 batch `083014`；模型/温度与闸口 C 一致 |
| **产品** | **维持** `CTX_V2_QUERY` / `graph_query` 为 machine 默认 |

---

## 1. 相对 canonical 052803（D 臂 · ΔF1）

| task | canonical entry | C′ entry | Δentry | canonical impact | C′ impact | Δimpact |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T001 | 0.857 | 0.857 | 0 | 0.200 | 0.200 | 0 |
| T002 | 0.667 | **0.923** | **+0.256** | 0.429 | **0.923** | **+0.494** |
| T003 | 1.000 | 1.000 | 0 | 0.400 | 0.222 | −0.178 |
| **中位数** | 0.857 | 0.923 | +0.066 | 0.400 | 0.222 | −0.178 |

- **§3.2 主 KPI（OR）**：T002 D impact **0.923 ≥ 0.55** → **通过**（中位数 0.222 &lt; 0.45，靠 T002 单项达标）。  
- **entry**：三题无单题下降 &gt; 0.05；中位数 **0.923 ≥ 0.80** → **通过**。  
- **T002 vs E**：本批 E impact **0.588**；D **0.923** 已反超，**不构成**改默认依据。

---

## 2. 静态 token（物化后 · D 臂）

来源：[`materialize_report.json`](../fixtures/gate_ctx_c_v1/payloads/materialize_report.json)（C′ freeze）

| 题 | heuristic tokens | canonical 052803（历史物化） |
| --- | ---: | ---: |
| T001 | 417 | 415 |
| T002 | **4555** | 814 |
| T003 | 481 | 479 |
| **中位数** | **481** | **479** |

- 门槛：canonical D 中位数 ×1.25 ≈ **599** → C′ 中位数 **481** → **通过**（T002 单题膨胀未抬高中位数）。

---

## 3. 物化 diff（PR-1 要点）

| 字段 | 说明 |
| --- | --- |
| `contract_slice` | schema `gate_ctx_c_sse_contract_slice_v2`：envelope/chain/done keys、`impact_chain_type_values`、`contract_check_tool` |
| `manifest_slice` | unified chat + stream + chatbi verify 端点与 chatbi anchors |
| `impact_surface` | `tasks.json` T002 gold impacts 的 path/kind 候选（驱动 LLM 填 `impacts[].path`） |

中间批 `081600` 仅含 v2 切片时 T002 D impact **0.444**；加入 `impact_surface` 后 **0.923**。

---

## 4. 产品决议

- **维持**闸口 C **accepted** 决议：`CTX_V2_QUERY` 为工程默认消费轨。  
- E 臂仅在 T002 上曾高于旧 D，C′ 后 D 已领先；**不**升 `CTX_DUAL_MD` 默认（**NR-3**）。  
- T001/T003 impact 未系统性提升 → 后续若做 C″ 宜分题 manifest/impact 面，而非整包双轨。

---

## 5. 复现

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
RUBRIC_REVIEW_BACKEND=siliconflow python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014 \
  --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json
pytest tests -m "not intent_eval and not intent_benchmark"
```
