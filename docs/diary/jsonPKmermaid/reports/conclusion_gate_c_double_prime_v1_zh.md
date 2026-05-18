# 闸口 C″ 结论：T003 分题物化 manifest / impact_surface（graph_query 轨）

> **状态**：`accepted`（2026-05-20 · **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** `approved` · 策略 B 豁免）  
> **freeze_id**：`TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`（未改图）  
> **canonical 对照（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_052803`](../runs/gate_ctx_c_v1_batch_20260518_052803/)  
> **C′ 对照（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_083014`](../runs/gate_ctx_c_v1_batch_20260518_083014/) · [`conclusion_gate_c_prime_f1_v1_zh.md`](./conclusion_gate_c_prime_f1_v1_zh.md)（**accepted**，本文件不修订）  
> **闸口 C D/E 叙事（只读）**：[`conclusion_gate_c_v2_dual_track_v1_zh.md`](./conclusion_gate_c_v2_dual_track_v1_zh.md)（**accepted** · batch `052803`）  
> **本批主 run**：[`runs/gate_ctx_c_v1_batch_20260518_102810`](../runs/gate_ctx_c_v1_batch_20260518_102810/)（**D + E 同批同步**）

---

## 0. 实验摘要

| 项 | 内容 |
| --- | --- |
| **PR-1** | T003 D 臂：`manifest_slice` v2 compact + `impact_surface` v2 compact（gold path/kind）；T002 **继承** C′ 三切片 |
| **PR-2** | T003 `downstream(A2, depth=1)` + 紧凑切片；D 中位数 **561**（C′ 481、门槛 ≈601） |
| **PR-3** | 新 batch `102810`；模型/温度与闸口 C 一致；**D vs E 同批**（见 §3） |
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

## 3. D vs E（闸口 C 同型 · batch `102810`）

> 表结构与 [`conclusion_gate_c_v2_dual_track_v1_zh.md`](./conclusion_gate_c_v2_dual_track_v1_zh.md) §1–§3 对齐；F1 来自 [`gold_f1.md`](../runs/gate_ctx_c_v1_batch_20260518_102810/gold_f1.md)，运行时 token 来自 6 条 `raw/*_S0.jsonl`；闸口 C 列引用 batch `052803`（物化不同，仅作历史参照）。

### 3.1 轴 II · 静态主载荷（启发式 tokens ↓）

| 题 | D · C″ | E · C″ | D · 闸口 C `052803` | E · 闸口 C |
| --- | ---: | ---: | ---: | ---: |
| T001 | 418 | 1316 | 415 | 1316 |
| T002 | **4556** | 1262 | 814 | 1262 |
| T003 | **561** | 973 | 479 | 973 |
| **中位数** | **561** | **1262** | **479** | **1262** |

| 指标 | D · C″ | E · C″ | 粗判（对齐闸口 C §1.3） |
| --- | ---: | ---: | --- |
| 中位数 tokens ↓ | **561** | 1262 | **D 胜**（E ≈ **2.25×** D；闸口 C 为 **2.6×**） |
| C″ D token 门槛 | ≤ **≈601** | — | D 中位数 **561** → **过** |

PR-2：T003 切片 + `downstream(A2,1)`；E 双轨选材与闸口 C **相同**（`dual_track_manifest.json` 未改）。

### 3.2 轴 I · 行为 S0（F1 ↑ · 运行时 total ↓）

#### D · `CTX_V2_QUERY`（C″ 本批）

| 题 | prompt ↓ | completion ↓ | total ↓ | entry F1 ↑ | impact F1 ↑ |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 | 4492 | 1153 | 5645 | 0.857 | 0.200 |
| T002 | **9276** | 1489 | **10765** | **0.923** | **0.800** |
| T003 | 4716 | 1074 | 5790 | 0.923 | **0.857** |
| **中位数** | **4716** | **1153** | **5790** | **0.923** | **0.800** |

`parse_ok`：3/3 为 `true`。

#### E · `CTX_DUAL_MD`（C″ 本批）

| 题 | prompt ↓ | completion ↓ | total ↓ | entry F1 ↑ | impact F1 ↑ |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 | 5974 | 673 | 6647 | 0.857 | 0.364 |
| T002 | 5803 | 1601 | 7404 | 0.909 | 0.471 |
| T003 | 5460 | 1105 | 6565 | 0.909 | 0.429 |
| **中位数** | **5803** | **1105** | **6565** | **0.909** | **0.429** |

`parse_ok`：3/3 为 `true`。

#### D vs E · 中位数（对齐闸口 C §2.3）

| 指标 | D · C″ | E · C″ | 闸口 C D / E 中位数 | 粗判 |
| --- | ---: | ---: | ---: | --- |
| total tokens ↓ | **5790** | 6565 | 6018 / 7019 | **D 胜**（约 **12%↓**；3 题 **2 胜 1 负**） |
| entry F1 ↑ | **0.923** | 0.909 | 0.857 / 0.857 | **D 略胜**（闸口 C **平局**） |
| impact F1 ↑ | **0.800** | 0.429 | 0.400 / 0.353 | **D 胜**（闸口 C 亦为 D 弱胜） |
| prompt ↓ | 4716 | 5803 | 4601 / 5798 | **D 胜**（T002 D **9276** 为 C′ 三切片所致） |

**题级要点（相对闸口 C）**

| 题 | 闸口 C D / E impact | C″ D / E impact | 解读 |
| --- | --- | --- | --- |
| T001 | 0.200 / **0.333** | 0.200 / **0.364** | 与 C 同型：**E impact 高于 D** |
| T002 | 0.429 / **0.588** | **0.800** / 0.471 | C 时 **E 胜**；C″ **D 反超 E**（仍 &lt; C′ 单臂 **0.923**） |
| T003 | **0.400** / 0.353 | **0.857** / 0.429 | C 时 D 仅弱胜；C″ **D 大幅领先 E**（主 KPI 题） |

### 3.3 胜负与默认轨（对齐闸口 C §3.1–§3.2）

| 维度 | 闸口 C 胜者 | C″ 胜者 | 对「维持 D 默认」 |
| --- | --- | --- | --- |
| 静态 tokens ↓ | **D** | **D** | 一致 |
| 运行时 total ↓ | **D**（3/3） | **D**（2/3；T002 反例） | 仍偏 D |
| entry F1 ↑ | **平局** | **D 略胜** | 不削弱 |
| impact F1 ↑ | **D 弱胜** | **D 明显胜** | **加强**（尤其 T003） |
| 升 E 为默认？ | **否**（accepted） | **仍否** | 无 E 全面碾压 D 证据 |

**与 C″ §3.2 门槛交叉**

| 门槛 | D/E 对照含义 |
| --- | --- |
| T003 D impact 主 KPI | D **0.857** ≫ E **0.429** → 物化有效，**非**改升 E 能更优 |
| T002 守卫 ≥0.873 | D **0.800** 未过，但 **&gt; E 0.471** → 回落非「E 更优」 |
| entry vs C′ | T003 D **0.923**、E **0.909** → 非 D 独降 |

**结论（§3）**：在 C″ 门槛与同批 D/E 实验下，**维持**闸口 C **accepted** 决议——**`CTX_V2_QUERY` 为 machine 默认**；E 为人读/按需轨。C″ 为 T003 补物化后，**相对 E 的 D 臂证据强于闸口 C**，尤其 T003 impact。

---

## 4. 静态 token（物化后 · D 臂 · 历史对照）

来源：[`materialize_report.json`](../fixtures/gate_ctx_c_v1/payloads/materialize_report.json)（C″ freeze）

| 题 | heuristic tokens | C′ `083014` | canonical `052803` |
| --- | ---: | ---: | ---: |
| T001 | 418 | 417 | 415 |
| T002 | 4556 | 4555 | 814 |
| T003 | **561** | 481 | 479 |
| **中位数** | **561** | **481** | **479** |

---

## 5. 物化 diff（PR-1 / PR-2）

| 题 | 字段 | 说明 |
| --- | --- | --- |
| **T003** | `manifest_slice` | `gate_ctx_c_manifest_slice_v2_compact`：`endpoint_paths` + `anchor_paths` |
| **T003** | `impact_surface` | `gate_ctx_c_impact_surface_v2_compact`：gold impacts path/kind（无长 note） |
| **T002** | （继承 C′） | `contract_slice` v2 + `manifest_slice` + `impact_surface` **未改分支** |
| **T003** | `query` | depth **2→1**（PR-2 token 守门） |

---

## 6. 产品决议（accepted · 策略 B）

- **维持** `CTX_V2_QUERY` / `graph_query` 为 machine 默认（§3 D vs E + T003 主 KPI；**不**因 T002 回落改默认轨；**不推翻** [`conclusion_gate_c_v2_dual_track_v1_zh.md`](./conclusion_gate_c_v2_dual_track_v1_zh.md)）。  
- **T003**：分题 manifest/impact 物化 **有效**（impact **0.222→0.857**）；**PR-4** 升格 `.cursor/rules/10-tech-graph.mdc` 在 **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** `approved` 后执行（见 task §6.1）。  
- **豁免（策略 B）**：§3.2 中 **T002 守卫**（D impact **0.800** &lt; **0.873**）与 **T003 entry**（相对 C′ **−0.077**）未达，**不阻止** 本结论 `accepted` 与 rules 升格；不改为默认 E。  
- **follow-up（非阻塞）**：T002 可单独复跑；T001 impact 仍弱于 E，非本闸口范围。

---

## 7. 复现

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
RUBRIC_REVIEW_BACKEND=siliconflow python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_102810 \
  --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-20 | v0.1：PR-1–3 与 §1–§2 D 臂双基线 |
| 2026-05-20 | v0.2：§3 D vs E 同批对照（对齐闸口 C 结论文 §1–§3） |
| 2026-05-20 | v0.3：`accepted` + 策略 B 豁免；HG 人签 |
