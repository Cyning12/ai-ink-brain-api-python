# JSON vs Mermaid — minimal S0 对照（T001）

> **题**：`T001_embedding_dim_default`  
> **模型**：`deepseek-ai/DeepSeek-V4-Flash`（SiliconFlow）  
> **轴 II 静态**：见 [`../fixtures/gate_ctx_ab_v1/payloads/materialize_report.json`](../fixtures/gate_ctx_ab_v1/payloads/materialize_report.json)（**不与**下表 LLM token/墙钟混写）

## 1. 三轮 run 墙钟 / token（行为向）

| run_id | 调用顺序 | 首轮 arm | 首轮 wall_s | 次轮 arm | 次轮 wall_s | 说明 |
|--------|----------|----------|------------:|----------|------------:|------|
| `…_105006` | JSON → Mermaid | CTX_JSON | **39.6** | CTX_MERMAID | **6.1** | 改 runner 前；首轮冷启动落在 JSON |
| `…_104123` | JSON → Mermaid | CTX_JSON | **612.9** | CTX_MERMAID | **77.6** | 异常偏长（疑似无/长超时等待）；**不宜**作主结论 |
| `…_110007` | **Mermaid → JSON** | CTX_MERMAID | **10.9** | CTX_JSON | **13.7** | **推荐对照**；`s0_arms_order` 默认 |

**同 run 内 token（110007）**

| arm | prompt | completion | total |
|-----|-------:|-----------:|------:|
| CTX_MERMAID | 11425 | 774 | 12199 |
| CTX_JSON | 11039 | 798 | 11837 |

**同 run 内 token（105006）**

| arm | prompt | completion | total |
|-----|-------:|-----------:|------:|
| CTX_JSON | 11039 | 842 | 11881 |
| CTX_MERMAID | 11425 | 937 | 12362 |

## 2. 解读（粗）

1. **模型名正确**；各 run `parse_ok` 均为 true。  
2. **JSON 并非必然更慢**：`110007` 在 Mermaid 首轮之后，JSON 仅 **~14s**，与「JSON 载荷导致 40s+」不一致。  
3. **首轮顺序强相关**：`105006` 首轮 JSON **39.6s** vs 次轮 Mermaid **6.1s**；调换顺序后首轮 Mermaid **10.9s**、次轮 JSON **13.7s** — 更符合 **API 冷启动/排队落在第一次请求**。  
4. **P3（token）**：三轮内 JSON 分支 total 略低于或接近 Mermaid（~11.8k vs ~12.2k），差异不大。  
5. **`104123`** 仅作异常样本保留，不纳入胜负判断。

## 3. 复现

```bash
cd ai-ink-brain-api-python
# 默认：Mermaid → JSON（protocol s0_arms_order）
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_minimal.py

# 复现旧顺序 JSON → Mermaid
python …/run_s0_minimal.py --arms-order json,mermaid
```

## 4. 原始落盘

- 推荐：[`../runs/gate_ctx_ab_v1_minimal_s0_20260516_110007/`](../runs/gate_ctx_ab_v1_minimal_s0_20260516_110007/)  
- 旧顺序：[`../runs/gate_ctx_ab_v1_minimal_s0_20260516_105006/`](../runs/gate_ctx_ab_v1_minimal_s0_20260516_105006/)  
- 异常：[`../runs/gate_ctx_ab_v1_minimal_s0_20260516_104123/`](../runs/gate_ctx_ab_v1_minimal_s0_20260516_104123/)

## 5. 如何避免「谁先谁慢」（顺序偏差）

| 方案 | 能否完全避免 | 说明 |
|------|----------------|------|
| **串行 + 调换 `--arms-order`** | 否 | 只能把冷启动换到指定 arm，仍不公平 |
| **`--parallel` 同时发两请求** | **部分** | 两分支各自 `wall_total_s` 独立计时，**都不占「对方暖机后的第二条」**；网关仍可能排队，两路可能同时变慢 |
| **丢弃首轮 + 重复 R 次取中位数** | 否（但可减弱） | 例如每 arm 连跑 2 次，只记第 2 次；成本 ×2 |
| **统一 warmup** | 否（但可减弱） | 先发极小 prompt 不计入统计，再正式 S0 |

**推荐（minimal 阶段）**：正式对比用

```bash
python …/run_s0_minimal.py --parallel
```

`index.json` 会写 `execution_mode: parallel` 与 `batch_wall_total_s`（两请求并发时的外层墙钟）。

## 6. 多轮批跑（推荐对照）

**批次**：[`gate_ctx_ab_v1_batch_20260516_110751`](../runs/gate_ctx_ab_v1_batch_20260516_110751/)  
**设定**：**3 轮** × 每轮 **`--parallel`**（最小可剔除 1 个离群；稳健可 `--rounds 5`）

| round | CTX_JSON wall_s | CTX_MERMAID wall_s | 备注 |
|------:|----------------:|-------------------:|------|
| 1 | 72.45 | 22.33 | JSON **剔除**（>2.5×中位数） |
| 2 | 21.25 | 35.59 | 均保留 |
| 3 | 6.99 | 6.97 | 均保留 |

**剔除后中位数（clean）**

| 指标 | CTX_JSON | CTX_MERMAID |
|------|--------:|------------:|
| wall_median_s | **14.1** | **22.3** |
| total_tokens_median | 11871 | 12333 |
| n | 2 | 3 |

**解读**：剔除首轮 JSON 尖峰后，两分支墙钟同量级（~7–22s），**无「JSON 形态必然更慢」**；token 中位数 JSON 略低。完整表见批次 [`aggregate.md`](../runs/gate_ctx_ab_v1_batch_20260516_110751/aggregate.md)。

```bash
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_batch.py --rounds 3
```

## 7. 未覆盖

S1/S2、双人 Rubric、入口/影响 F1 对 gold 计分。
