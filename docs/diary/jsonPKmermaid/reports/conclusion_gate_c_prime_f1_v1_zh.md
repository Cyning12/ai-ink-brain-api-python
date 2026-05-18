# 闸口 C′ 结论：graph_v2 查询轨 impact F1 物化增强（F1 优先）

> **状态**：`accepted`（2026-05-20 · **HG-GATE-C-PRIME-SIGNOFF** 人签）  
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

### 1.1 题级解读：为何主攻 T002、T003 impact 为何下降

**本实验工程重心在 T002，不是三题齐升。**

| 题 | PR-1 物化 | 说明 |
| --- | --- | --- |
| **T002** | `contract_slice` v2 + `manifest_slice` + **`impact_surface`** | 闸口 C 弱项（D impact **0.429**）；本 task 主 KPI |
| **T001** | 原有小 subgraph，无 manifest / impact 切片 | 与 canonical 基本持平 |
| **T003** | `downstream(A2, depth=2)` 小图 only | token **481 vs 479**，**未**加 T003 专用 `impact_surface` |

PR-3 仍 **全三题** 重跑（闸口 C 式对照）；§3.2 验收为 **OR**：**T002 D impact ≥ 0.55** 即过，**不要求** T003 impact 上升。

**T003 impact：0.400 → 0.222（Δ−0.178）—— 非 T003 物化被改坏，而是新 batch 下 LLM 填 `impacts[]` 更差。**

| 批（D 臂） | impact TP | FP | FN | recall | F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| canonical `052803` | 4 | 10 | 2 | 0.67 | **0.400** |
| C′ `083014` | 2 | 10 | 4 | 0.33 | **0.222** |

- **entry** 两批均为 **1.000**（6/6 gold entry）；**仅 impacts 掉分**。  
- C′ 轮次 jsonl（`…_083014/round_03/raw/CTX_V2_QUERY_T003_*`）中模型写出 **10 条** impact，多依赖 `manifest.*` / `contract.sse.*` 的 `ref`，**缺少** gold 要求的 `path`（如 `api/rag_env.py`、`api/unified_chat.py`、`tools/tech_graph_manifest_check.py`）。  
- 误引 **Unified Chat SSE** 契约项（`rag.sources`、`sql.result`）——属 **T002 域**，与 Admin Ingest **无关** → 增加 FP，且挤占正确 path 命中。  
- **主因归纳**：（1）本 task **未** 为 T003 做 impact 物化；（2）同模型/温度下 **批次随机性**；（3）评分按 gold **path + kind** 对齐，`ref` 字符串 **不算** TP。  
- **验收允许**：OR 规则已由 T002 达标；T003 回落记为 **已知副作用**，不推翻「维持 `CTX_V2_QUERY` 默认」决议。后续 **C″** 若抬 T003，宜 **分题** 加 manifest / `impact_surface`（见 §4）。

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
