# T002（Unified SSE）— S0 批跑结论

> **题**：`T002_unified_sse_chain_contract`（`topic_id: unified_chat_sse`）  
> **批跑**：[`gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253`](../runs/gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253/)  
> **模型**：`deepseek-ai/DeepSeek-V4-Flash`（SiliconFlow）  
> **日期**：2026-05-16

---

## 1. 实验范围

在 **与 T001 相同的静态载荷**（轴 II：`graph.json` 20224 B / Mermaid 20953 B；启发式 token 5056 vs 5026）下，仅改变主上下文形态，对 **Unified Chat SSE 契约变更** 题做 **S0 冷启动**（策略 α，3 轮并行）。

---

## 2. 定量结果（clean，n=3，无离群剔除）

| 指标 | CTX_JSON | CTX_MERMAID | 相对 |
|------|--------:|------------:|------|
| **wall_median_s** | **38.97** | 47.63 | JSON 约快 **18%** |
| **total_tokens_median** | **12044** | 12571 | JSON 约低 **4%** |
| **parse_ok** | 3/3 | 3/3 | 均合法 JSON |
| **status** | 3/3 ok | 3/3 ok | 无失败 |

### 全量墙钟（看抖动）

| round | CTX_JSON (s) | CTX_MERMAID (s) | 备注 |
|------:|-------------:|----------------:|------|
| 1 | 61.96 | 66.58 | 双分支均偏长，疑似冷启动 |
| 2 | 38.97 | **7.13** | Mermaid 暖缓存极快，勿单独解读 |
| 3 | 23.65 | 47.63 | — |

主表见 [`aggregate.md`](../runs/gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253/aggregate.md)。

---

## 3. 与 T001 对照（同协议，不同题）

| 题 | batch | clean n | JSON wall 中位数 | Mermaid wall 中位数 | token 中位数（J / M） |
|----|-------|--------:|-----------------:|--------------------:|----------------------|
| T001 向量维度 | [`…_111037`](../runs/gate_ctx_ab_v1_batch_20260516_111037/) | 2 / 2 | **17.4s** | 32.5s | 12159 / 12609 |
| **T002** Unified SSE | **本批** | 3 / 3 | **39.0s** | 47.6s | 12044 / 12571 |

- 两题 **clean 中位数均为 JSON 略优**（墙钟 + token），但绝对墙钟 **不可横比**（题面与 completion 不同）。
- T001 网关离群更多（各剔 1 条）；T002 六条全保留，**稳定性略好**，仍 **n=3**。
- 迄今 **未出现**「换题后 Mermaid 全面胜出」。

T001 综合叙述：[`conclusion_gate_ctx_ab_comprehensive_zh.md`](./conclusion_gate_ctx_ab_comprehensive_zh.md)。

---

## 4. 内容质量（round_03 粗评，未做 gold F1）

| 维度 | CTX_JSON | CTX_MERMAID |
|------|----------|-------------|
| 核心路由 | `unified_chat_stream_route` ✓ | 同左 + `handle_unified_chat_stream` ✓ |
| 契约/CI | manifest、`contract_check` 等 ✓ | `type_values`、CI ✓ |
| 与 gold 偏差 | 鉴权误写 `_require_auth`；缺 `handle_unified_chat_stream`、`_event` | 多命中 `_event`；误写 `_sse`；`require_chatbi_principal` 路径挂错 |

两形态均能答到 SSE/contract 主题；**均未稳定对齐** [`tasks.json`](../fixtures/gate_ctx_ab_v1/tasks.json) 人工 gold 全集。

---

## 5. 能说什么 / 不能说什么

**能说**

1. T002 下两分支 **6/6** 产出可解析 schema。  
2. 本轮中位数：**JSON 墙钟与 token 略优于 Mermaid**（n=3）。  
3. 与 T001 合并：两题均未观察到 Mermaid 全面胜出。

**不能说**

1. 不能签收「生产一律 JSON」——仅 2 题、仅 S0、无 gold F1 / S1/S2。  
2. 不能用 round 2 Mermaid **7.1s** 证明 Mermaid 常态更快。  
3. 不能据 spot check 断言「SSE 题 Mermaid 理解更深」——仍有符号幻觉。

---

## 6. 一句话结论

**T002 minimal S0：JSON 与 Mermaid 均可完成 Unified SSE 结构化分析；本轮 JSON 在墙钟与 token 中位数上略优，Mermaid 在部分样本对 gold 入口略好，样本小且无正式计分——选型须扩题 + S1/S2 + gold F1 后再定稿。**

---

## 7. 复现

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/materialize_payloads.py
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_batch.py \
  --task-id T002_unified_sse_chain_contract --rounds 3
```
