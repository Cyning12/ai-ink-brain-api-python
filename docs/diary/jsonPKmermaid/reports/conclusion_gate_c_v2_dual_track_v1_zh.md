# 闸口 C 定稿结论：CTX_V2_QUERY vs CTX_DUAL_MD（graph_v2 查询轨 vs 精选双轨原文）

> **状态**：`draft`（待 **HG-GATE-C-SIGNOFF** 人签后改 `accepted`）  
> **freeze_id**：`TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0`（[`protocol_version.yaml`](../fixtures/gate_ctx_c_v1/protocol_version.yaml)）  
> **graph_v2_freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_2`  
> **闸口 A 基线（NR-1 · 勿复做主实验）**：[`conclusion_gate_ctx_ab_final_zh.md`](./conclusion_gate_ctx_ab_final_zh.md)  
> **闸口 B 已采纳默认（本报告不推翻）**：[`conclusion_gate_b_ctx_query_v1_zh.md`](./conclusion_gate_b_ctx_query_v1_zh.md) · **CTX_QUERY / `graph_query` 子图**  
> **本批 run**：[`runs/gate_ctx_c_v1_batch_20260518_052803`](../runs/gate_ctx_c_v1_batch_20260518_052803/)

---

## 0. 实验设计摘要

| 臂 | 代号 | 主载荷 | 本批 LLM 调用 |
| --- | --- | --- | --- |
| **D** | `CTX_V2_QUERY` | `graph_v2` 子图 JSON + query 元数据（`downstream` depth=2） | **本批新跑**（3 题 × S0） |
| **E** | `CTX_DUAL_MD` | 精选 `10_flow_*.ai.md` + 配对 `*.md`（[`dual_track_manifest.json`](../fixtures/gate_ctx_c_v1/dual_track_manifest.json)） | **本批新跑**（3 题 × S0） |
| （引用） | `CTX_MERMAID` / `CTX_JSON` / `CTX_QUERY` | 闸口 A/B 历史 | **NR-1 / NR-2：不新跑** |

- **题集**：复用 [`tasks.json`](../fixtures/gate_ctx_ab_v1/tasks.json) 三题（`T001`/`T002`/`T003`）。  
- **D 种子**：[`query_seeds.json`](../fixtures/gate_ctx_c_v1/query_seeds.json)（节点 `ENV`/`U2`/`A2`，与闸口 B 同型、独立 freeze）。  
- **E 选材**：每题 1 组双轨（共 3 组 `.ai.md`+`.md`，**非**整仓 7 文件）。  
- **模型**：`deepseek-ai/DeepSeek-V4-Flash` · `temperature=0.2` · 策略 α（与闸口 B 对齐）。  
- **段**：仅 **S0**（冷启动单轮）；未跑 S1/S2。

### 0.1 复现命令

来源：[`runs/gate_ctx_c_v1_batch_20260518_052803/README.md`](../runs/gate_ctx_c_v1_batch_20260518_052803/README.md) · [`batch_index.json`](../runs/gate_ctx_c_v1_batch_20260518_052803/batch_index.json) `reproduce_commands`

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
RUBRIC_REVIEW_BACKEND=siliconflow python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803 \
  --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

## 1. 轴 II：静态主载荷 token（启发式 · D vs E）

来源：[`gate_ctx_c_v1/payloads/materialize_report.json`](../fixtures/gate_ctx_c_v1/payloads/materialize_report.json)

| arm | 每题启发式 tokens | 中位数 | 相对整包 Mermaid（5026） |
| --- | ---: | ---: | ---: |
| **D · CTX_V2_QUERY** | T001 415 · T002 814 · T003 479 | **479** | **≈0.10×** |
| **E · CTX_DUAL_MD** | T001 1316 · T002 1262 · T003 973 | **1262** | **≈0.25×** |

- D 子图节点数：T001 2 · T002 7 · T003 4（`ref` 边不参与）。  
- E 选材：`selected_ai_md_count=3`（仓库共 7 个 `*.ai.md`，**非**整包灌入）。  
- **D vs E（静态）**：E 中位数约为 D 的 **2.6×**（1262 / 479）；二者均远低于闸口 A 整包 Mermaid。  
- **与闸口 B 对照（引用）**：B 已采纳的 **CTX_QUERY** 静态中位数 **427**（见 [`conclusion_gate_b`](./conclusion_gate_b_ctx_query_v1_zh.md) §1）；本批 **D** 中位数 **479** 与之同量级（+12% 量级差，属题种子图规模差异，**不构成**改默认轨依据）。

**结论（轴 II）**：在「少读」维度上 **D 胜 E**；D 与闸口 B 的 query 子图叙事一致，**维持 B 的 machine 默认**。

---

## 2. 轴 I：行为向 S0（段·S0 · 单轮）

### 2.1 本批 LLM 用量（6 条 jsonl）

| 题 | arm | prompt | completion | total | wall_s |
| --- | --- | ---: | ---: | ---: | ---: |
| T001 | E · CTX_DUAL_MD | 5969 | 1050 | 7019 | 42.3 |
| T001 | D · CTX_V2_QUERY | 4487 | 783 | 5270 | 5.2 |
| T002 | E | 5798 | 1328 | 7126 | 29.8 |
| T002 | D | 4992 | 1132 | 6124 | 37.4 |
| T003 | E | 5455 | 1257 | 6712 | 55.9 |
| T003 | D | 4601 | 1417 | 6018 | 8.6 |
| **中位数** | **D** | **4601** | **1132** | **6018** | **8.6** |
| **中位数** | **E** | **5798** | **1257** | **7019** | **42.3** |

- **total tokens 中位数**：D **6018** vs E **7019** → D 约 **14%↓**（3/3 题 D 更低或持平）。  
- **wall 中位数**：D **8.6s** vs E **42.3s** → D 表面占优；**T002** D 墙钟高于 E，受 API 波动与子图+附件体积影响，**不宜**单独作为「省时」硬签收。  
- **parse_ok**：6/6 为 `true`（见 [`gold_f1.json`](../runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.json)）。

### 2.2 Gold F1（entrypoints / impacts）

来源：[`gold_f1.md`](../runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md) · `score_gold_f1.py`

| 题 | 指标 | **D · CTX_V2_QUERY** | **E · CTX_DUAL_MD** |
| --- | --- | ---: | ---: |
| T001 | entry F1 | 0.857 | 0.857 |
| T001 | impact F1 | 0.200 | **0.333** |
| T002 | entry F1 | 0.667 | **0.833** |
| T002 | impact F1 | 0.429 | **0.588** |
| T003 | entry F1 | **1.000** | 0.909 |
| T003 | impact F1 | **0.400** | 0.353 |
| **中位数** | entry F1 | **0.857** | **0.857** |
| **中位数** | impact F1 | **0.400** | 0.353 |

**要点**：

- **入口（entry）**：中位数 **打平**；T003 D 全覆盖（含 `code_ingest`），T002 E 召回更高（缺子图外 `AUTH`/`EV_TYPES` 时 D 更弱）。  
- **影响（impact）**：中位数 **D 略优**，但题间方差大；E 在 T002 契约链题上 impact 更高。  
- 与闸口 B 对照（引用）：B 的 CTX_QUERY impact 中位数 **0.267**；本批 D impact 中位数 **0.400** 不可直接横比（freeze / 附件 / 单次样本），仅说明 **子图轨仍难覆盖远距契约 gold**。

---

## 3. D vs E 胜负与 Agent 默认消费轨建议

### 3.1 胜负汇总（本批 S0 · 3 题）

| 维度 | 胜者 | 说明 |
| --- | --- | --- |
| 静态主载荷 token | **D** | 479 vs 1262 中位数 |
| 运行时 total tokens | **D** | 6018 vs 7019 中位数 |
| entry F1 中位数 | **平局** | 0.857 vs 0.857 |
| impact F1 中位数 | **D（弱优）** | 0.400 vs 0.353；非全胜 |
| wall 中位数 | **D（粗判）** | 8.6s vs 42.3s；T002 反例 |

**综合**：在影响分析类三题上，**D（v2 查询子图）在成本侧明确优于 E（精选双轨原文）**；正确性 **未出现 E 全面碾压 D** 的证据，题间互有胜负。

### 3.2 与闸口 B 的关系（不推翻已采纳默认）

1. **维持** 闸口 B §5：**Agent / CI 默认 machine 轨 = `graph_query` → 子图 + manifest/contract 切片**（代号链：`CTX_QUERY` → 本 task **`CTX_V2_QUERY`**，同一产品语义，独立 freeze）。  
2. **不采纳** 将 **CTX_DUAL_MD（精选双轨 `.ai.md`+`.md`）** 作为默认 prompt 主载荷：静态 token 约为 D 的 2.6×，运行时 total 更高，F1 无净收益。  
3. **不推翻** 闸口 A/B 对「禁止默认整包 v2 JSON / 整包 Mermaid」的决议（NR-1、NR-2 延续）。  
4. **E 的定位**：人读轨 / 按需 `@` 局部双轨原文；**非**替代 query 子图的 machine 默认。

### 3.3 follow-up（非阻塞 draft）

- T002：D 缺 `AUTH`/`EV_TYPES` → 与 B 相同，考虑 `upstream` 或第二 query 种子。  
- impact F1 系统性偏低 → 契约段 manifest 切片优先，而非扩大为整图双轨。  
- P3：在 `改进方向.md` 增闸口 C 行（task P3 · recommended）。

---

## 4. 复现与验收指针

| 项 | 路径 |
| --- | --- |
| materialize | `fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py` |
| batch | `fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py` |
| canonical run | `runs/gate_ctx_c_v1_batch_20260518_052803/` |
| pytest | `tests/test_gate_ctx_c_v1_materialize.py` · `tests/test_gate_ctx_c_v1_batch.py` |

关账前须：**HG-GATE-C-SIGNOFF** 人签 + 本文件状态 `accepted`。

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-18 | v0 draft：P2 闸口 C；canonical batch `052803`；不推翻闸口 B CTX_QUERY 默认 |
