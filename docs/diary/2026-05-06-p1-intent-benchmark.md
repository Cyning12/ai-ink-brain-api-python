# 2026-05-06 — ChatBI V2 P1-Eval 评测与基准（v1 落盘）

关联任务：`docs/tasks/active/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`  
Spec：`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`（P50/P95 目标表）、`SPEC-ChatBI-V2-Intent.md`（60 条约定）

## 归档产物（防覆盖改名）

**复跑二**结束后已将 `intent_llm_latest` 改名归档（避免后续跑批覆盖）：

- `tests/_out/intent_llm_latest_20260506_171351_v1fb15_acc0817.jsonl`
- `tests/_out/intent_llm_latest_20260506_171351_v1fb15_acc0817.csv`

命名含义：`v1fb15` = 本文件内 `raw_response.used=v1_fallback` 共 **15** 条；`acc0817` ≈ **49/60** 准确率。  
**下次跑批**：请显式设置 `CHATBI_V2_INTENT_EVAL_OUT=tests/_out/intent_llm_latest.jsonl`（或新时间戳路径）；当前仓库内**无** `intent_llm_latest.jsonl`，避免误以为仍有「最新」文件。

---

## 首轮跑批（同日较早，环境相对正常）

| 项 | 值 |
|----|-----|
| 产物 | 当时为 `tests/_out/intent_llm_latest.*`（已被复跑二覆盖前已提交 git 的摘要；原始 JSONL 未保留） |
| `v1_fallback` | **10** / 60 |
| 汇总 | **n=60**，**ok=52**，**acc≈0.867**，**macro-F1≈0.868** |
| per-class F1 | text2sql **≈0.947**，rag **≈0.857**，direct **≈0.800** |
| 分桶 | Text2SQL **18/20**；RAG（`rag_search` 共 24）**18/24**；Direct **16/16**；多轮 **i=51–60** **8/10** |
| 混淆矩阵 | T2S 18/0/2；RAG 0/18/6；Direct 0/0/16 |

---

## 复跑二（网络不稳，`v1_fallback` 过多 — **不作为最终验收冻结**）

| 项 | 值 |
|----|-----|
| 归档 | 见上文 `intent_llm_latest_20260506_171351_v1fb15_acc0817.*` |
| `v1_fallback` | **15** / 60（`reasoning` 均为「意图识别超时，降级到 V1 规则路由。」） |
| 汇总 | **ok=49**，**acc≈0.817**，**macro-F1≈0.821** |
| per-class F1 | text2sql **≈0.889**，rag **≈0.829**，direct **≈0.744** |
| 分桶 | Text2SQL **16/20**（**低于** ≥17/20）；RAG **17/24**；Direct **16/16**；多轮 **7/10**（**低于** ≥8/10） |
| 真 LLM 分歧（非 `v1_fallback`） | **2** 条：`i=33`（`rag_search`→`direct_answer`）、`i=56`（多轮，`rag_search`→`direct_answer`） |

### 混淆矩阵（复跑二，expected → predicted）

| expected \\ predicted | text2sql_query | rag_search | direct_answer |
|------------------------|----------------|------------|----------------|
| text2sql_query | 16 | 0 | 4 |
| rag_search | 0 | 17 | 7 |
| direct_answer | 0 | 0 | 16 |

### Intent 延迟粗算（复跑二，`latency_ms`）

| 子集 | n | P50 | P95 |
|------|---|-----|-----|
| 全量 60 条 | 60 | ≈8498 ms | ≈31037 ms |
| 剔除 `v1_fallback` | 45 | ≈7906 ms | ≈18795 ms |

### 复跑二 `ok=false` 一览（共 11，按 confidence 降序）

1. **i=33** `rag_search`→`direct_answer` conf=**0.90** — 真 LLM：「如何计算 confusion matrix」判为通用知识直接答。
2. **i=56** `rag_search`→`direct_answer` conf=**0.85** — 真 LLM：多轮「那需要查数据库吗」判 direct。
3. 其余 9 条均为 **`v1_fallback` + conf=0.60**（超时后 V1 路由，多为判成 `direct_answer` 或少数侥幸对齐金标）：i=**1,6,10,12**（T2S）、**27,28,32**（RAG）、**51,52**（多轮 RAG）。

**归因**：本轮 **`v1_fallback` 15 条**，`latency_ms` 在 fallback 样本上多集中在 **~30.6–31.7s**，与 **`CHATBI_V2_INTENT_TIMEOUT_S`≈30s** 顶满一致；**优先怀疑外网/上游不稳定**，而非 RAG prompt 单独失效。  
**结论**：**须在更稳定网络下复跑 60 条**，再更新任务单验收数字；本轮仅作归档与对比基线。

---

## 待网络稳定后（任务跟踪）

- [ ] 固定时段或更换网络后，**重新执行** `pytest … -m intent_eval`，导出新的 `intent_llm_latest.jsonl`（或带时间戳文件名），对比 **`v1_fallback` 条数**与 macro-F1；若 fallback 明显下降，再以该次作为「环境正常」主报告。
- 可选：跑前记录上游 RTT / 并发；仍不达标再进入 **P1-D**（超时阈值、重试、prompt、金标口径）。

---

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

---

## 验收数值对照表（首轮 vs 复跑二）

| 项 | 目标 / 备注 | 首轮（较早） | 复跑二（网络差，已归档） |
|----|-------------|--------------|--------------------------|
| macro-F1 | > 90% | **≈0.868**（未达标） | **≈0.821**（未达标） |
| Text2SQL | ≥ 17/20 | **18/20** | **16/20** |
| RAG（24 条 `rag_search`） | 见任务单口径 | **18/24** | **17/24** |
| Direct | 当前 16 条 | **16/16** | **16/16** |
| 多轮 i=51–60 | ≥ 8/10 | **8/10** | **7/10** |
| `v1_fallback` | 越少越好（过程性） | **10** | **15** |
| Intent P50 / P95（JSONL 粗算） | Overview 理想值仍远未达 | 首轮见历史 git / 上文摘要 | 全量 P50≈8498ms，P95≈31037ms；剔除 fallback 后 P50≈7906ms，P95≈18795ms |
| B2 | diary 链 | **TBD** | **TBD** |

---

## 备注

- 更早模板见 `docs/diary/2026-04-30-p1-intent-benchmark.md`；本文件为 **P1-Eval v1** 当日归档与复跑入口。
- CI：`pytest` 默认不设置 `CHATBI_V2_INTENT_EVAL` / `CHATBI_V2_INTENT_BENCH_RUN`，相关用例跳过；stub 用例覆盖导出与零外呼门禁。
