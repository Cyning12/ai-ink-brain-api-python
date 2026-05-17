# 2026-04-30 — ChatBI V2 Intent Benchmark（P1-P0）

## 目标

- 验证 **真实 LLM** 的意图分类（`rag_search` / `text2sql_query` / `direct_answer`）在 60 条测试集上的准确率表现
- 输出可复跑的 **macro-F1 / per-class F1 / confusion matrix**
- 输出 Intent 决策 **延迟分布（P50/P95/P99）**

## 运行方式（可复跑）

### 1) 准确率评测（60 条）

```bash
# 真实 LLM（本地手动评测）
export CHATBI_V2_INTENT_LLM=true
export CHATBI_V2_INTENT_EVAL=true
export SILICONFLOW_API_KEY="..."
export INTENT_LLM_MODEL="deepseek-ai/DeepSeek-V3"   # 或 Qwen/Qwen2.5-7B-Instruct / qwen turbo

python -m pytest -q tests/test_intent_agent_accuracy.py -s
```

输出：
- 控制台：macro-F1 / per-class F1 / confusion matrix / JSONL 输出路径
- JSONL：`tests/_out/intent_accuracy.jsonl`（可用 `CHATBI_V2_INTENT_EVAL_OUT` 自定义）

### 2) 性能基准（Intent 延迟）

```bash
export CHATBI_V2_INTENT_LLM=true
export SILICONFLOW_API_KEY="..."
export INTENT_LLM_MODEL="deepseek-ai/DeepSeek-V3"
export CHATBI_V2_INTENT_BENCH_N=100

python tests/benchmark_intent_latency.py
```

## 评测配置

- **模型**：`INTENT_LLM_MODEL=...`
- **开关**：`CHATBI_V2_INTENT_LLM=true`（真实 LLM）/ `false`（不触发外部调用，走启发式/降级）
- **timeout**：`CHATBI_V2_INTENT_TIMEOUT_S`（脚本默认 3s）
- **温度**：固定 0（由 `api/intent_agent.py` 内部控制）

## 结果（填写区）

### 1) 准确率

- **macro-F1**：`TBD`
- **per-class F1**：
  - `text2sql_query`: `TBD`
  - `rag_search`: `TBD`
  - `direct_answer`: `TBD`
- **confusion matrix（expected -> predicted）**：
  - `text2sql_query`: `TBD`
  - `rag_search`: `TBD`
  - `direct_answer`: `TBD`
- **JSONL 路径**：`TBD`

### 2) 性能

- **Intent latency（n=100）**：
  - P50: `TBD` ms
  - P95: `TBD` ms
  - P99: `TBD` ms
  - Min/Max: `TBD` / `TBD` ms

## Top-10 误判样例（填写区）

> 建议从 `tests/_out/intent_accuracy.jsonl` 里筛选 `ok=false`，按 `confidence desc` 或 `latency desc` 排序贴入。

1. query: `...`
   - expected: `...`
   - predicted: `...`
   - confidence: `...`
   - latency_ms: `...`
   - reasoning: `...`
2. ...

## 结论与下一步（P1 后续）

- **误判最多的边界**：TBD（通常是 Text2SQL vs RAG、以及“要查数” vs “问方法”）
- **优化方向**：
  - Prompt：TBD
  - few-shot：TBD
  - 阈值/回退：TBD
- **缓存（P1-C）**：命中率、延迟收益待补（完成 `_intent_cache` 的 history_hash key 后再复测）
