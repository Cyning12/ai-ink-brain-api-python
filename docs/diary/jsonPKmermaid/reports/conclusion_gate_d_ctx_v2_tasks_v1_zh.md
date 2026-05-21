# 闸口 D 结论：v2 五题扩域（graph_query 轨 · accepted）

> **状态**：`accepted`（2026-05-21 · PR-3 batch `091709` · **HG-GATE-D-SIGNOFF** `approved`）  
> **freeze_id**：`TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`  
> **回归基线（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_102810`](../runs/gate_ctx_c_v1_batch_20260518_102810/)  
> **本批主 run**：[`runs/gate_ctx_c_v1_batch_20260521_091709`](../runs/gate_ctx_c_v1_batch_20260521_091709/) · `gold_f1.md` / `batch_index.json`

---

## 0. PR-1 / PR-2 / PR-3 工程摘要

| 项 | 内容 |
| --- | --- |
| **题集** | `fixtures/gate_ctx_ab_v2/tasks.json` · 五题 · v1 三题 gold 与 ab_v1 **一致** |
| **物化** | `materialize_gate_c_payloads.py` · T001～T003 继承 C″ 分支；T004/T005 增量 manifest/impact |
| **PR-2** | D 五题静态中位数 **658** ≤ **701**（T004/T005 `depth=1`；省略 T004/T005 `contract_slice`） |
| **PR-3** | batch `20260521_091709` · 10 条 jsonl · `score_gold_f1` + `gate_ctx_ab_v2/tasks.json` |
| **pytest** | `204 passed` · `pytest tests -m "not intent_eval and not intent_benchmark"` |

---

## 1. 表 1 · v1 回归（D 臂 vs `102810`）

> D = `CTX_V2_QUERY`；C″ 列来自 `102810` `gold_f1.json`；本批来自 `091709`。

| task | C″ D impact | C″ D entry | 本批 D impact | 本批 D entry | Δimpact |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 | 0.200 | 0.857 | 0.200 | 0.857 | 0.000 |
| T002 | 0.800 | 0.923 | 0.923 | 0.923 | +0.123 |
| T003 | 0.857 | 0.923 | 1.000 | 0.923 | +0.143 |

**§3.2 表 1 门槛**：单题 impact F1 相对 C″ **下降 ≤ 0.10** → **pass**（无回落；T002/T003 提升）。

---

## 2. 表 2 · v2 扩展（D 臂）

> 表 2 脚注：「无题专属物化」基线 = 关闭 T004/T005 专属 `manifest_slice`/`impact_surface` 的一次 ablation（**未在本批执行**；本批以绝对门槛 **≥ 0.45** 验收）。

| task | 本批 D impact | 本批 D entry | 备注 |
| --- | ---: | ---: | --- |
| T004 | 0.750 | 1.000 | `downstream(T2S,1)` + manifest/impact 增量 |
| T005 | 0.857 | 0.800 | `downstream(INT,1)` + manifest/impact 增量 |

**§3.2 表 2 门槛**：T004 **0.750**、T005 **0.857** 均 ≥ **0.45** → **pass**（OR 规则满足）。

---

## 3. 表 3 · D vs E（token / F1）

> 来源：本批 `round_*/index.json`（运行时 token）+ `gold_f1.json`（F1）+ [`materialize_report.json`](../fixtures/gate_ctx_c_v1/payloads/materialize_report.json)（静态 heuristic）。

### 3.1 轴 II · 静态主载荷（heuristic tokens）

| 题 | D · 本批 | E · 本批 |
| --- | ---: | ---: |
| T001 | 417 | 1316 |
| T002 | 4355 | 1262 |
| T003 | 560 | 973 |
| T004 | 658 | 1996 |
| T005 | 709 | 939 |
| **中位数** | **658** | **1262** |

| 指标 | D · 本批 | 粗判 |
| --- | ---: | --- |
| 中位数 ≤ **701** | **658** | **pass**（PR-2 已验；≤ max(601, C″×1.25)） |
| 单题 &lt; **8192** | max **4355**（T002） | **pass** |

### 3.2 轴 I · 行为 S0（F1 ↑ · 运行时 total ↓）

#### D · `CTX_V2_QUERY`（本批）

| 题 | prompt | completion | total | entry F1 | impact F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 | 4492 | 814 | 5306 | 0.857 | 0.200 |
| T002 | 9047 | 1192 | 10239 | 0.923 | 0.923 |
| T003 | 4716 | 1081 | 5797 | 0.923 | 1.000 |
| T004 | 4844 | 1576 | 6420 | 1.000 | 0.750 |
| T005 | 4825 | 1099 | 5924 | 0.800 | 0.857 |
| **中位数** | **4825** | **1099** | **5924** | **0.923** | **0.857** |

`parse_ok`：5/5 为 `true`。

#### E · `CTX_DUAL_MD`（本批）

| 题 | prompt | completion | total | entry F1 | impact F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 | 5974 | 746 | 6720 | 0.857 | 0.364 |
| T002 | 5803 | 1337 | 7140 | 0.909 | 0.500 |
| T003 | 5460 | 1050 | 6510 | 0.909 | 0.429 |
| T004 | 7349 | 1999 | 9348 | 1.000 | 0.400 |
| T005 | 5345 | 909 | 6254 | 0.857 | 0.167 |
| **中位数** | **5803** | **1050** | **6720** | **0.909** | **0.400** |

`parse_ok`：5/5 为 `true`。

#### D vs E · 中位数（对齐闸口 C″ §3.2）

| 指标 | D · 本批 | E · 本批 | C″ D / E 中位数（`102810`） | 粗判 |
| --- | ---: | ---: | ---: | --- |
| total tokens ↓ | **5924** | 6720 | 5790 / 6565 | **D 胜**（约 **12%↓**；5 题 **4 胜 1 负**，T002 反例） |
| entry F1 ↑ | **0.923** | 0.909 | 0.923 / 0.909 | **D 略胜** |
| impact F1 ↑ | **0.857** | 0.400 | 0.800 / 0.429 | **D 胜**（扩域后 D 中位数抬升） |
| prompt ↓ | 4825 | 5803 | 4716 / 5803 | **D 胜**（T002 D **9047** 仍为离群） |

**题级要点**

| 题 | C″ D / E impact | 本批 D / E impact | 解读 |
| --- | --- | --- | --- |
| T001 | 0.200 / 0.333 | 0.200 / 0.364 | 与 C″ 同型：E impact 高于 D |
| T002 | 0.800 / 0.471 | 0.923 / 0.500 | D 相对 C″ **提升**；仍 **&gt; E** |
| T003 | 0.857 / 0.429 | **1.000** / 0.429 | D 满分；E 持平 C″ |
| T004 | — | 0.750 / 0.400 | v2 新题；D 达扩展门槛 |
| T005 | — | **0.857** / 0.167 | v2 新题；D 明显优于 E |

### 3.3 §3.2 主 KPI 交叉（task `§3.2 PR-3`）

| 门槛 | 实测 | 判定 |
| --- | --- | --- |
| 维持 `CTX_V2_QUERY` 默认 | D 在 total / impact 中位数上 **优于** E；无升 E 证据 | **建议维持** |
| 表 1 · impact 相对 C″ 回落 ≤ 0.10 | 最大 Δ **+0.143**（T003），无负 Δ | **pass** |
| 表 2 · T004 或 T005 impact ≥ 0.45 | **0.750** / **0.857** | **pass** |
| D 静态 token 中位数 ≤ **701** | **658** | **pass** |
| D 单题静态 &lt; **8192** | max **4355** | **pass** |
| 不修订 C 系 accepted 正文 | 本稿仅增量闸口 D | **pass** |

**结论（§3）**：五题扩域 batch 下，**维持**闸口 C/C″ **accepted** 决议——**`CTX_V2_QUERY` 为 machine 默认**；E 为人读/按需轨。v1 三题无 impact 回归；T004/T005 D 臂达扩展 KPI；token 中位数 **658** 未触 PR-2/§3.2 上限。

---

## 4. 复现命令

```bash
python tools/tech_graph_graph_export.py --check
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
pytest tests/test_gate_ctx_c_v1_materialize.py tests/test_gate_ctx_ab_v2_tasks.py
# PR-3（须 SILICONFLOW_API_KEY + RUBRIC_REVIEW_BACKEND=siliconflow）
RUBRIC_REVIEW_BACKEND=siliconflow python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260521_091709 \
  --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v2/tasks.json
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-21 | 30 帽 PR-1/PR-2 落盘；PR-3 draft 占位（API Key 阻塞） |
| 2026-05-21 | PR-3 batch `091709` + `gold_f1`；表 1/2/3 与 §3.2 KPI 回填 |
