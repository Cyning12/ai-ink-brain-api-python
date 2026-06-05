# 闸口 C 定稿结论：CTX_V2_QUERY vs CTX_DUAL_MD（graph_v2 查询轨 vs 精选双轨原文）

> **状态**：`accepted`（待 **HG-GATE-C-SIGNOFF** 人签后改 `accepted`）  
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
- **模型**：`deepseek-ai/DeepSeek-V4-Pro` · `temperature=0.2` · 策略 α（与闸口 B 对齐）。  
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

## 1. 轴 II：静态主载荷 token（启发式）

来源：[`gate_ctx_c_v1/payloads/materialize_report.json`](../fixtures/gate_ctx_c_v1/payloads/materialize_report.json)

### 1.1 D · CTX_V2_QUERY（子图 JSON）

| 题 | 启发式 tokens ↓ | 子图 nodes |
| --- | ---: | ---: |
| T001 | 415 | 2 |
| T002 | 814 | 7 |
| T003 | 479 | 4 |
| **中位数** | **479** | — |

相对整包 Mermaid（5026）：**≈0.10×**（越少越好）。

### 1.2 E · CTX_DUAL_MD（精选双轨原文）

| 题 | 启发式 tokens ↓ | 双轨文件 |
| --- | ---: | --- |
| T001 | 1316 | `10_flow_rag.ai.md` + `.md` |
| T002 | 1262 | `15_e2e_boundary.ai.md` + `.md` |
| T003 | 973 | `13_flow_supabase_rpc.ai.md` + `.md` |
| **中位数** | **1262** | — |

相对整包 Mermaid（5026）：**≈0.25×**（越少越好）。选材 `selected_ai_md_count=3`（仓库共 7 个 `*.ai.md`，**非**整包灌入）。

### 1.3 D vs E（静态 · 中位数）

| 指标 | D · CTX_V2_QUERY | E · CTX_DUAL_MD | 粗判 |
| --- | ---: | ---: | --- |
| 启发式 tokens ↓ | **479** | 1262 | **D 胜**（E ≈ 2.6× D） |
| 相对 Mermaid ↓ | ≈0.10× | ≈0.25× | **D 胜** |

- **与闸口 B 对照（引用）**：B 已采纳 **CTX_QUERY** 静态中位数 **427** ↓（见 [`conclusion_gate_b`](./conclusion_gate_b_ctx_query_v1_zh.md) §1）；本批 **D** **479** ↓ 与之同量级（+12% 属题种子图规模差，**不构成**改默认轨依据）。

**结论（轴 II）**：在「少读」维度上 **D 胜 E**；D 与闸口 B 的 query 子图叙事一致，**维持 B 的 machine 默认**。

---

## 2. 轴 I：行为向 S0（段·S0 · 单轮）

F1 来源：[`gold_f1.md`](../runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md) · `score_gold_f1.py`；用量来自 6 条 `raw/*_S0.jsonl`。

### 2.1 D · CTX_V2_QUERY 本批（LLM 实测）

| 题 | prompt_tokens ↓ | completion ↓ | total ↓ | wall_s ↓ | entry F1 ↑ | impact F1 ↑ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T001 | 4487 | 783 | 5270 | 5.2 | **0.857** | 0.200 |
| T002 | 4992 | 1132 | 6124 | 37.4 | 0.667 | 0.429 |
| T003 | 4601 | 1417 | **6018** | 8.6 | **1.000** | **0.400** |
| **中位数** | **4601** | **1132** | **6018** | **8.6** | **0.857** | **0.400** |

`parse_ok`：3/3 为 `true`。

### 2.2 E · CTX_DUAL_MD 本批（LLM 实测）

| 题 | prompt_tokens ↓ | completion ↓ | total ↓ | wall_s ↓ | entry F1 ↑ | impact F1 ↑ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T001 | 5969 | 1050 | 7019 | 42.3 | **0.857** | **0.333** |
| T002 | 5798 | 1328 | 7126 | 29.8 | **0.833** | **0.588** |
| T003 | 5455 | 1257 | 6712 | 55.9 | 0.909 | 0.353 |
| **中位数** | **5798** | **1257** | **7019** | **42.3** | **0.857** | **0.353** |

`parse_ok`：3/3 为 `true`。

### 2.3 D vs E 对照（中位数 · 本批 S0）

| 指标 | D · CTX_V2_QUERY | E · CTX_DUAL_MD | 粗判 |
| --- | ---: | ---: | --- |
| prompt_tokens ↓ | **4601** | 5798 | **D 胜** |
| completion ↓ | **1132** | 1257 | **D 胜** |
| total tokens ↓ | **6018** | 7019 | **D 胜**（3/3 题 D ≤ E） |
| wall_s ↓ | **8.6** | 42.3 | **D 粗胜**\* |
| entry F1 ↑ | **0.857** | 0.857 | **平局** |
| impact F1 ↑ | **0.400** | 0.353 | **D 弱胜**（T002 E 更高） |

\* **T002** D wall **37.4s** > E **29.8s**，受 API 波动与子图+附件体积影响，**不宜**单独作为「省时」硬签收。

**要点**：

- **省钱（total ↓）**：D 中位数 **6018** vs E **7019** → **3/3 胜**（约 **14%↓**）。  
- **省时（wall ↓）**：D 中位数 **8.6s** vs E **42.3s** → 粗判 D 优，但 T002 反例。  
- **入口（entry F1 ↑）**：中位数 **打平**；T003 D **1.000** 全覆盖；T002 E **0.833** > D **0.667**（缺子图外 `AUTH`/`EV_TYPES` 时 D 更弱）。  
- **影响（impact F1 ↑）**：中位数 D **0.400** > E **0.353**，题间方差大；T002 契约链 E **0.588** > D **0.429**。  
- 与闸口 B 对照（引用）：B 的 CTX_QUERY impact 中位数 **0.267** ↑；本批 D **0.400** 不可直接横比（freeze / 附件 / 单次样本），仅说明 **子图轨仍难覆盖远距契约 gold**。

---

## 3. D vs E 胜负与 Agent 默认消费轨建议

### 3.1 胜负汇总（本批 S0 · 3 题）

| 维度 | 指标方向 | 胜者 | 说明 |
| --- | --- | --- | --- |
| 静态主载荷 | tokens ↓ | **D** | 479 vs 1262 中位数 |
| 运行时成本 | total ↓ | **D** | 6018 vs 7019 中位数 |
| 入口正确性 | entry F1 ↑ | **平局** | 0.857 vs 0.857 |
| 影响正确性 | impact F1 ↑ | **D（弱优）** | 0.400 vs 0.353；T002 E 更高 |
| 墙钟 | wall_s ↓ | **D（粗判）** | 8.6s vs 42.3s；T002 反例 |

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
| 2026-05-18 | v0.1：轴 I 拆 D/E 分表；全表补 ↑/↓ 优劣方向（对齐闸口 B） |
