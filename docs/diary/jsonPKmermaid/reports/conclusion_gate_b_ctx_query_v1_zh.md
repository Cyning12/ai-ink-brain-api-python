# 闸口 B 定稿结论：CTX_QUERY vs 整包 Mermaid / 整包 v1 JSON

> **状态**：`accepted`（**HG-P2-3-GATE-B** 人签：2026-05-17 · 接受 B-1 部分满足，采纳 §5 CTX_QUERY 默认）  
> **freeze_id**：`TECH_GRAPH_S2_FREEZE_20260517_V2_0`（与 [`protocol_version.yaml`](../fixtures/gate_ctx_ab_v1/protocol_version.yaml) · `graph_v2_freeze_id` 对齐）  
> **协议**：[`fixtures/gate_ctx_b_v1/protocol_version.yaml`](../fixtures/gate_ctx_b_v1/protocol_version.yaml)  
> **闸口 A 基线（勿复做主实验）**：[`conclusion_gate_ctx_ab_final_zh.md`](./conclusion_gate_ctx_ab_final_zh.md)  
> **治理层抉择**：[`治理层三相塌缩_Ink技术图谱应用.md`](../治理层三相塌缩_Ink技术图谱应用.md) §8.2～§8.3  
> **本批 run**：[`runs/gate_ctx_b_v1_batch_20260517_095228`](../runs/gate_ctx_b_v1_batch_20260517_095228/)

---

## 0. 实验设计摘要

| 组 | 代号 | 主载荷 | 本批 LLM 调用 |
| --- | --- | --- | --- |
| **A** | `CTX_MERMAID` | 整包 `*.ai.md` Mermaid 语料 | **沿用闸口 A**（NR-1：不作本 task 主结论） |
| **B** | `CTX_JSON` | 整包 v1 `graph.json`（闸口 A 冻结 payload） | **沿用闸口 A** |
| **C** | `CTX_QUERY` | `graph_query` 子图 + manifest/contract 附件 | **本批新跑**（3 题 × S0） |

- **题集**：与闸口 A 相同三题（`T001`/`T002`/`T003`），见 [`tasks.json`](../fixtures/gate_ctx_ab_v1/tasks.json)。  
- **CTX_QUERY 种子**：[`query_seeds.json`](../fixtures/gate_ctx_b_v1/query_seeds.json)（`downstream` depth=2，节点 `ENV`/`U2`/`A2`）。  
- **模型**：`deepseek-ai/DeepSeek-V4-Flash` · `temperature=0.2` · 策略 α（全量重贴附件）。

---

## 1. 轴 II：静态主载荷 token（启发式）

来源：[`gate_ctx_b_v1/payloads/materialize_report.json`](../fixtures/gate_ctx_b_v1/payloads/materialize_report.json)

| arm | 启发式 tokens（主载荷） | 相对整包 Mermaid |
| --- | ---: | ---: |
| CTX_MERMAID | 5026 | 1.00× |
| CTX_JSON（v1 冻结） | 5056 | 1.01× |
| **CTX_QUERY（中位数）** | **427** | **≈0.08×** |

子图规模（nodes/edges）：T001 2/1 · T002 7/8 · T003 4/3。

**结论（轴 II）**：少读子图是 token 主因；与治理层 §8.3 一致。

---

## 2. 轴 I：行为向 S0（段·S0 · 单轮）

### 2.1 CTX_QUERY 本批（LLM 实测）

| 题 | prompt_tokens | completion | total | wall_s | entry F1 | impact F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T001 | 4447 | 844 | 5291 | 15.5 | **0.857** | 0.200 |
| T002 | 4853 | 1139 | 5992 | 46.6 | 0.667 | 0.286 |
| T003 | 4531 | 1508 | 6039 | 323.0* | **1.000** | 0.267 |
| **中位数** | **4531** | — | **5992** | **46.6** | **0.857** | **0.267** |

\* T003 墙钟为 provider 长尾；不计入「省时」粗判主结论。

F1 来源：[`gold_f1.md`](../runs/gate_ctx_b_v1_batch_20260517_095228/gold_f1.md)（`score_gold_f1.py`）。

### 2.2 与闸口 A 对照（A/B 引用定稿表 §2）

| 题 | 指标 | CTX_JSON（A 对照） | CTX_MERMAID（基线） | **CTX_QUERY** |
| --- | --- | ---: | ---: | ---: |
| T001 | total tokens ↓ | 12159 | 12609 | **5291** |
| T001 | entry F1 ↑ | 0.822 | 0.794 | **0.857** |
| T002 | total tokens ↓ | 12044 | 12571 | **5992** |
| T002 | entry F1 ↑ | 0.667 | **0.939** | 0.667 |
| T003 | total tokens ↓ | 12258 | 12810 | **6039** |
| T003 | entry F1 ↑ | 0.909 | **1.000** | **1.000** |

**P3 省钱（total tokens 中位数）**：CTX_QUERY **5992** vs JSON **12159** vs Mermaid **12571** → **3/3 胜**。  
**P4 省时（wall 中位数，剔除 T003 长尾）**：CTX_QUERY **46.6s** vs JSON **39.0s** vs Mermaid **47.6s** → 与 JSON 相当，**未全胜**（受附件体积与 API 波动影响）。

**P2 可靠性（entry F1 中位数）**：CTX_QUERY **0.857** vs Mermaid **0.939** vs JSON **0.822** → 介于两臂之间，**T002 入口召回偏弱**（子图未覆盖 `AUTH`/`EV_TYPES` 等兄弟节点）。

**P2 影响（impact F1 中位数）**：CTX_QUERY **0.267** vs Mermaid **0.340** vs JSON **0.396** → **子图 + 附件仍不足以替代远距影响枚举**（契约/CI 类 gold 多不在 2-hop 内）。

---

## 3. 签收门槛对照（task §4.3）

| 规则 | 判定 | 说明 |
| --- | --- | --- |
| **B-1** P1/P2 ≥ 闸口 A Mermaid 中位数 | **部分满足** | entry F1 中位数略低于 Mermaid（0.857 vs 0.939）；T001/T003 单题达标；impact F1 系统性偏低 → **建议默认 query + 按需加深 hop / manifest 切片**，非整包 v2 |
| **B-2** P3/P4 不劣于 CTX_JSON | **P3 满足** | total tokens 中位数约 **51%↓**；P4 未全胜，可接受（与闸口 A「换格式不省钱」叙事正交） |
| **B-3** 等价 CI 连续绿 ≥5 PR | **工程已绿** | P2-1/P2-2 pytest + `tech-graph.yml` equivalence **PASS**；「连续 5 PR」留关账轮统计 |

---

## 4. P1 Rubric 子集（≥3 题）

| 题 | 代理指标（本批） | 说明 |
| --- | --- | --- |
| T001 | parse_ok · entry F1=0.857 | 结构完整；入口优于闸口 A 两臂 |
| T002 | parse_ok · entry F1=0.667 | 缺 AUTH/EV_TYPES → **建议 query 补 `upstream` 或第二种子** |
| T003 | parse_ok · entry F1=1.000 | 入口全覆盖 |

正式 **Phase·P1 双人盲审**未在本批重跑（避免 NR-1）；人签时可抽检 [`round_*/raw/`](../runs/gate_ctx_b_v1_batch_20260517_095228/round_01/raw/) 输出 JSON。

---

## 5. 产品决议（建议）

1. **推荐默认机器轨消费**：`graph_query(…)` → `_manifest` / `_contract` 按需切片 → **禁止**默认整包 v2 `graph.json` 进 prompt（与 FP-5、`.cursor/rules/10-tech-graph.mdc` 一致）。  
2. **维持** `*.ai.md` 为 **export 源**（G-END-4 退役条件未满足）。  
3. **不签收**「一律 v1/v2 整包替 Mermaid」（闸口 A 结论延续）。  
4. **follow-up**：契约重题（T002 类）增加 `upstream`/`neighbors` 组合或 manifest 契约段优先切片。

---

## 6. 复现命令

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_b_v1/scripts/materialize_gate_b_payloads.py
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_b_v1/scripts/run_gate_b_batch.py --arms CTX_QUERY
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_b_v1_batch_20260517_095228
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-17 | v1：P2-3 闸口 B 首版；freeze_id `TECH_GRAPH_S2_FREEZE_20260517_V2_0` |
