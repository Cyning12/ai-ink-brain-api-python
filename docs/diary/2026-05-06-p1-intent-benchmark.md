# 2026-05-06 — ChatBI V2 P1-Eval 评测与基准（v1 落盘）

关联任务：`docs/tasks/active/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`  
Spec：`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`（P50/P95 目标表）、`SPEC-ChatBI-V2-Intent.md`（60 条约定）

## 跑批元信息（2026-05-06 回填）

| 项 | 值 |
|----|-----|
| 产物 | `tests/_out/intent_llm_latest.jsonl`、`tests/_out/intent_llm_latest.csv`（同次跑批；另有带时间戳副本见 `tests/_out/intent_llm_20260506_*.jsonl`） |
| 模型 / 密钥 | `INTENT_LLM_MODEL` 以跑批环境为准（与 SiliconFlow 一致）；本批 `raw_response.used=v1_fallback` 共 **10** 条（多为 `CHATBI_V2_INTENT_TIMEOUT_S` 边界触发） |
| 汇总 | **n=60**，**ok=52**，**acc=0.867**，**macro-F1≈0.868**；per-class F1：text2sql **0.947**，rag **0.857**，direct **0.800** |
| 分桶（与当前 `_cases()` 一致：T2S 20 / RAG 24 / Direct 16，多轮 10 条混在三类内） | Text2SQL **18/20**；RAG（expected=`rag_search` 共 24 条）**18/24**；Direct **16/16**；多轮子集 **i=51–60** 共 10 条 **8/10** |
| 对照门槛（任务单原「RAG≥18/20」按 20 条金标写法） | macro-F1 **未达** >0.90；RAG 在 **24** 条上为 **18/24**；Text2SQL **18/20**（≥17 **达标**）；Direct **16/16**；多轮 **8/10**（达标）→ 未过项 **链 P1-D**（超时、prompt、金标/任务口径） |

## 复跑命令（与 PROJECT_CONFIG 对齐）

### A) 60 条准确率 + JSONL + CSV

```bash
export CHATBI_V2_INTENT_EVAL=true
export CHATBI_V2_INTENT_LLM=true
export SILICONFLOW_API_KEY="..."
export INTENT_LLM_MODEL="Qwen/Qwen2.5-7B-Instruct"   # 或 deepseek-ai/DeepSeek-V3 等
# 若控制台出现「意图识别超时」且 latency≈3s：上游慢于默认 wait_for，请加大例如：
# export CHATBI_V2_INTENT_TIMEOUT_S=20
# 可选（推荐写入仓库内，便于归档）：相对路径二选一（与 pytest cwd 无关）
# export CHATBI_V2_INTENT_EVAL_OUT="tests/_out/intent_llm_latest.jsonl"
# export CHATBI_V2_INTENT_EVAL_OUT="_out/intent_llm_latest.jsonl"
# 仍可用绝对路径：export CHATBI_V2_INTENT_EVAL_OUT="/tmp/intent_run.jsonl"

python -m pytest tests/test_intent_agent_accuracy.py -m intent_eval -s
# 等价：python tests/test_intent_agent_accuracy.py
```

关闭真实 LLM（启发式全量、仍写导出，用于链路自检）：

```bash
export CHATBI_V2_INTENT_EVAL=true
export CHATBI_V2_INTENT_LLM=false
python -m pytest tests/test_intent_agent_accuracy.py -m intent_eval -s
```

### B1) Intent 延迟分布（P50/P95/P99）

```bash
export CHATBI_V2_INTENT_LLM=true
export SILICONFLOW_API_KEY="..."
export CHATBI_V2_INTENT_BENCH_N=100
python tests/benchmark_intent_latency.py
```

或经 pytest（默认跳过，需显式打开）：

```bash
export CHATBI_V2_INTENT_BENCH_RUN=true
export CHATBI_V2_INTENT_LLM=true
export SILICONFLOW_API_KEY="..."
python -m pytest tests/benchmark_intent_latency.py -m intent_benchmark -s
```

**测量边界（B1 真值）**：`decide_intent_v2` 入口至返回的 wall-clock（毫秒），含 `asyncio.to_thread` 内同步 `chat.completions.create`。与 Overview 表对照时以此为准。

### B2) Agent 单步 / E2E（最小化，不依赖真实 RAG/SQL）

脚本：`tests/benchmark_agent_e2e_latency.py`

```bash
export CHATBI_USE_AGENT=true
export CHATBI_V2_INTENT_LLM=false    # 默认脚本内 setdefault；可改为 true 测真实 intent
export CHATBI_V2_AGENT_BENCH_N=50
python tests/benchmark_agent_e2e_latency.py
```

**测量边界**：

- **E2E**：`POST /api/py/unified/chat` 返回的 `events[]` 中 `type=latency` 的 `payload.total_ms`（stub 工具、内存 registry）。
- **单步**：同一次响应中 `type=tool.call.end` 的 `payload.latency_ms` 列表的分位数。

与 Overview 目标（Intent P50/P95、Agent 单步、整体 E2E）对照时，在表中注明「B2 为 stub 工具链」或「已切换真实 intent」等变量。

## 验收数值（须本地跑批后填写）

| 项 | 目标 / 备注 | 本次跑批 |
|----|-------------|----------|
| macro-F1 | > 90%（未达标则列样例并链 P1-D） | **0.868**（未达标） |
| Text2SQL 召回 | ≥ 17/20（金标 20 条） | **18/20** |
| RAG 召回 | ≥ 18/20（任务单按 20 条写法；当前集为 **24** 条 `rag_search`） | **18/24**（未达原「18/20」比例意涵时请改任务门槛或切片口径） |
| Direct 召回 | ≥ 9/10 | **16/16**（当前集为 16 条 `direct_answer`，**全部正确**） |
| 多轮 召回 | ≥ 8/10（子集 i=51–60） | **8/10** |
| Intent P50 / P95 | < 200ms / < 500ms（B1 口径） | **未达标**：本批为评测循环内 `latency_ms`（60 条全量）**P50≈7431ms，P95≈20938ms**；剔除 `v1_fallback` 后 **n=50**，**P50≈3768ms，P95≈16030ms**（仍远高于 Overview 理想值，属上游延迟 + 长 prompt） |
| Agent 单步 P50 / P95 | < 1.5s / < 3s（B2 口径） | 未跑 B2 脚本，**TBD** |
| E2E P50 / P95 | < 3s / < 8s（B2 口径） | 未跑 B2 脚本，**TBD** |

### 混淆矩阵（expected → predicted，本次）

| expected \\ predicted | text2sql_query | rag_search | direct_answer |
|------------------------|----------------|------------|----------------|
| text2sql_query | 18 | 0 | 2 |
| rag_search | 0 | 18 | 6 |
| direct_answer | 0 | 0 | 16 |

## Top-10 误判（从 `ok=false` 按 confidence 降序）

本次共 **8** 条 `ok=false`（按 confidence 降序；与 `intent_llm_latest.jsonl` 一致）：

1. **i=33** expected=`rag_search` actual=`direct_answer` conf=**0.90** — 「如何计算 confusion matrix」：模型判为通用知识直接回答（金标为 rag；可议）。
2. **i=56** expected=`rag_search` actual=`direct_answer` conf=**0.90** — 「那需要查数据库吗」（**多轮**）：模型判为元问题直接回答（金标为 rag；可议）。
3. **i=3** expected=`text2sql_query` actual=`direct_answer` conf=**0.60** — 「最近7天收入多少」：**意图识别超时 → V1 降级**。
4. **i=20** expected=`text2sql_query` actual=`direct_answer` conf=**0.60** — 「用户增长趋势」：**超时降级**。
5. **i=26** expected=`rag_search` actual=`direct_answer` conf=**0.60** — 「Text2SQL 的原理是什么」：**超时降级**。
6. **i=29** expected=`rag_search` actual=`direct_answer` conf=**0.60** — 「如何写一份 _tech_graph 的流程图」：**超时降级**。
7. **i=31** expected=`rag_search` actual=`direct_answer` conf=**0.60** — 「如何做意图缓存（LRU+TTL）」：**超时降级**。
8. **i=52** expected=`rag_search` actual=`direct_answer` conf=**0.60** — 「那怎么优化」（**多轮**）：**超时降级**。

**归因小结**：**expected=`rag_search` 共 24 条**中错 6 条：纯 RAG 段内多为 **超时降级**（如 i=26/29/31）+ **i=33** 模型判 direct；多轮里 **i=52** 超时、**i=56** 模型判 direct。macro-F1 未过 0.90 → **P1-D**：`CHATBI_V2_INTENT_TIMEOUT_S`、prompt、或金标/切片口径与任务单对齐。

## 备注

- 更早模板见 `docs/diary/2026-04-30-p1-intent-benchmark.md`；本文件为 **P1-Eval v1 任务** 当日归档与复跑入口。
- CI：`pytest` 默认不设置 `CHATBI_V2_INTENT_EVAL` / `CHATBI_V2_INTENT_BENCH_RUN`，相关用例跳过；stub 用例覆盖导出与零外呼门禁。
