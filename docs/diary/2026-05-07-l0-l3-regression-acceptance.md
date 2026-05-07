# 深度回归 L0–L3 验收归档（2026-05-07）

> 口径：`SPEC-ChatBI-V2-Agent-Overview.md` **§7.5**（L0–L7）；本页仅归档 **L0–L3** 本轮结果。  
> **L4–L7** 操作细则见同文件 **§7.5.3–§7.5.6**。

---

## 1. 验收结论（是否通过）

| 层级 | 结论 | 备注 |
|------|:----:|------|
| **L0** | **通过** | `tech_graph_contract_check` **OK**；`pytest tests` **53 passed + 2 skipped**（`intent_eval` / `intent_benchmark` 默认 skip）。 |
| **L1** | **通过** | 真实 LLM：`n=60`，**ok=60**，acc=**1.000**，macro-F1=**1.000**；pytest **≈404.75s**；导出 **`tests/_out/intent_llm_20260507_181334.jsonl`**、**`.csv`**。 |
| **L1′**（可选） | 管道 OK | `CHATBI_V2_INTENT_LLM=false` stub：**40/60**、macro≈0.643；**仅**验证评测链路与导出，**不参与** L1 质量结论。 |
| **L2** | **通过** | `pytest … -m intent_benchmark`：`n=100`，P50/P95≈**0**（缓存命中为主），P99/Max **秒级**尾部；**≈14.33s**。 |
| **L2′**（可选） | **通过** | `python tests/benchmark_intent_latency.py`：同脚本入口；Avg/Max 与 L2 可因随机与抖动略有差异。 |
| **L3** | **通过** | `test_unified_chat_backend_v2_agent.py`：**8 passed**，**≈11.09s**。 |

**总评**：在 **「契约 + 全仓 pytest 门禁 + 60 条 Intent 金标 + Intent 延迟基准 + Unified V2 单测」** 定义下，本轮 **L0–L3 可签验收**；**不**等价于总规 **§7.4** 全行「已对齐」（尤其 SSE 实链、error_code 矩阵、跨仓、生产 DB 仍待 **L4–L7**）。

---

## 2. 证据索引（文件 / 命令）

| 证据 | 路径或命令摘要 |
|------|----------------|
| L1 导出 | `tests/_out/intent_llm_20260507_181334.jsonl`、`tests/_out/intent_llm_20260507_181334.csv` |
| L0 命令 | `unset CHATBI_V2_INTENT_EVAL CHATBI_V2_INTENT_BENCH_RUN`（及可选 `CHATBI_V2_INTENT_LLM`）→ `tech_graph_contract_check` → `pytest tests -q --tb=short` |
| L1 命令 | `CHATBI_V2_INTENT_EVAL=true CHATBI_V2_INTENT_LLM=true` + `CHATBI_V2_INTENT_EVAL_OUT=…` → `pytest … -m intent_eval -v -s` |
| L2 / L3 | 见 Overview **§7.5.2** 表内一行命令 |

---

## 3. 环境与复现备忘

- **Intent 超时**：`decide_intent_v2` 内 **`CHATBI_V2_INTENT_TIMEOUT_S` 优先于** 调用方传入的 `timeout`（见 `api/intent_agent.py::_effective_intent_llm_timeout_s`）；本轮 L1 全对且总时长 **~6.7min**，与 **60× 外呼** 及 env 超时配置一致。  
- **复现 L1**：须在 shell / `.env` 中配置 **`SILICONFLOW_API_KEY`**（及按需 **`INTENT_LLM_MODEL`**），勿将密钥写入本 diary。

---

## 4. 后续（未纳入本轮）

- 执行 **L4–L7** 并更新 **Gap 快照 / §7.4** 对应行后，方可对外称「总规级全量回归」闭合。详见 Overview **§7.5.3–§7.5.6**。
