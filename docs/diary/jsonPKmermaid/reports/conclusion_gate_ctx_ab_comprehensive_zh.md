# JSON vs Mermaid 上下文形态 — 综合结论（gate_ctx_ab_v1 · minimal S0）

> **执行批次（终）**：[`gate_ctx_ab_v1_batch_20260516_111037`](../runs/gate_ctx_ab_v1_batch_20260516_111037/)  
> **题**：`T001_embedding_dim_default`（`expected_embedding_dim()` 默认维度与全链路对齐）  
> **模型**：`deepseek-ai/DeepSeek-V4-Flash`（SiliconFlow）  
> **日期**：2026-05-16

---

## 1. 实验要回答什么

在 **同一题、同一 Rubric 输出 schema** 下，仅改变 LLM **主上下文载荷**：

| 分支 | 主载荷 |
|------|--------|
| **CTX_JSON** | `graph.json` 全文 |
| **CTX_MERMAID** | 与闸口 A 一致的 Mermaid 语料总串（`*.ai.md` fence 拼接） |

比较 **行为向**（墙钟、token、结构化 JSON 是否可解析），并与 **轴 II 静态**（字节/启发式 token，不进模型）分开叙述。

---

## 2. 方法与干扰控制

| 环节 | 做法 |
|------|------|
| 轴 II | 本机复现 `graph.json` **20224 B**；Mermaid **20953 B**；启发式 token **5056 vs 5026**（见 `payloads/materialize_report.json`） |
| S0 | 单题冷启动；输出 `entrypoints` / `impacts` / `evidence` / `unknowns` |
| 顺序偏差 | 每轮 **`parallel`** 同时发两请求，避免「串行第二条占便宜」 |
| 离群 | **3 轮**批跑；剔除 `wall>120s` 或 `>2.5×` 该 arm 三轮中位数；`status!=ok` 剔除 |
| 模型名 | 与官网一致 `deepseek-ai/DeepSeek-V4-Flash`；响应 `model_returned` 一致 |

---

## 3. 终批全量数据（`111037`）

| round | CTX_JSON wall_s | CTX_MERMAID wall_s | 计入 clean |
|------:|----------------:|-------------------:|:----------:|
| 1 | 60.58 | 23.82 | JSON 剔除（>2.5×中位数） |
| 2 | 22.91 | **333.32** | Mermaid 剔除（>120s） |
| 3 | 11.94 | 41.25 | 均保留 |

三轮 **parse_ok 均为 true**（6/6 次调用成功产出合法 schema）。

---

## 4. 剔除离群后的对比（主结论依据）

| 指标 | CTX_JSON | CTX_MERMAID | 相对 |
|------|--------:|------------:|------|
| **wall_median_s** | **17.4** | **32.5** | JSON 墙钟中位数更低（n=2） |
| **total_tokens_median** | **12159** | **12609** | JSON 略省约 **3.6%** token |
| 有效样本 n | 2 | 2 | 各剔除 1 个离群 |

**说明**：n=2 仍偏少；结论方向与前一批 `110751`（JSON 14.1s / Mermaid 22.3s）一致，但数值会有批次间抖动。

---

## 5. 对历史干扰的归因（为何曾以为「JSON 很慢」）

| 现象 | 解释 |
|------|------|
| 串行首轮 JSON **39–72s**、次轮 Mermaid **6–23s** | **首轮冷启动/排队**落在先执行的一支，**非**载荷形态固有 |
| `104123` JSON **612s**、`111037` R2 Mermaid **333s** | **网关/超时边界类离群**；剔除后不应进入主结论 |
| 调换 `arms-order` 或 `parallel` 后 JSON 亦可 **~7–22s** | 与「JSON 必然慢」不符 |

---

## 6. 轴 II vs 行为向（勿混写）

| 维度 | CTX_JSON | CTX_MERMAID | 含义 |
|------|--------:|------------:|------|
| 静态字节 | 20224 | 20953 | 塞进上下文前体积接近（B 约 **+3.6%**） |
| 启发式 token | 5056 | 5026 | 粗估亦接近 |
| LLM prompt（本实验） | ~11039 | ~11425 | 行为向输入略不同（含 manifest/contract） |
| 墙钟（clean 中位数） | **17.4s** | **32.5s** | **本次**终批：JSON 更快，但受 API 抖动影响大 |

**不能**用轴 II「体积相当」直接推出墙钟相当；**也不能**用单次串行 run 断言孰快孰慢。

---

## 7. 质量与验收（本阶段）

- **输出**：6/6 次合法 JSON；均命中 `api/rag_env.py` / 图谱节点类 evidence（未做 gold F1）。  
- **未做**：S1 多轮追问、S2 换题、P1/P2 双人 Rubric、入口/影响 F1。  
- **演示工件**：早期 `examples_builtin` Rubric 批跑已迁至 `_staging/`，**与**本实验无关。

---

## 8. 建议的下一步（若进入 `01_experiment` 全协议）

1. **批跑**：`run_s0_batch.py --rounds 5` 提高 n，或固定时段连跑。  
2. **题集**：`fixtures/gate_ctx_ab_v1/tasks.json` 增加 2–3 题 + gold，再谈 P1/P2。  
3. **报告**：行为向与轴 II 分节；主表用 **clean 中位数 + 全量附录**。  
4. **可选**：统一 **warmup** 请求（不计入统计）进一步压冷启动。

---

## 9. 一句话综合结论

**在静态载荷体积几乎相同的前提下，JSON 与 Mermaid 作为 LLM 主上下文均可完成 T001 结构化分析；剔除 API 离群与串行顺序偏差后，本终批（3 轮并行）显示 JSON 在墙钟与 token 中位数上略优于 Mermaid，但样本仍少、网关抖动大，尚不足以签收「生产环境一律选用 JSON」——需扩题集与 S1/S2 后再定稿。**

---

## 附录：复现命令

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/materialize_payloads.py
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_batch.py --rounds 3
```

主表：[`runs/.../111037/aggregate.md`](../runs/gate_ctx_ab_v1_batch_20260516_111037/aggregate.md)
