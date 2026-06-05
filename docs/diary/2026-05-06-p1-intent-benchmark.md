# 2026-05-06 — ChatBI V2 P1-Eval 评测与基准（v1 落盘）

关联任务：`docs/tasks/active/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`  
Spec：`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`（P50/P95 目标表）、`SPEC-ChatBI-V2-Intent.md`（60 条约定）

## 归档产物（防覆盖改名）

历史与最新归档（文件名内嵌关键统计，便于对比）：

| 批次 | JSONL / CSV（`tests/_out/`） |
|------|-------------------------------|
| 复跑二（网络差，不冻结） | `intent_llm_latest_20260506_171351_v1fb15_acc0817.{jsonl,csv}` |
| 复跑三（**前**冻结验收轮，历史对照） | `intent_llm_latest_20260507_113718_v1fb3_acc0933_macro0932.{jsonl,csv}` |
| **复跑四（本地 rerun，补充归档）** | `intent_llm_20260507_1509_v1fb1_acc9500_macro9492.{jsonl,csv}` |
| **冻结验收轮（复跑五，`CHATBI_V2_INTENT_TIMEOUT_S=60`）** | `intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.{jsonl,csv}` |

命名含义（**当前冻结轮·复跑五**）：`v1fb1` = `v1_fallback` **1** 条；`acc9500` ≈ **57/60**；`macro9484` ≈ **macro-F1 0.948**；`tout60` = 评测时 **`CHATBI_V2_INTENT_TIMEOUT_S=60`**。  
**历史**：复跑三文件名中 `v1fb3` / `acc0933` / `macro0932` 含义见下文「复跑三」专节。  
**下次跑批**：显式 `export CHATBI_V2_INTENT_EVAL_OUT=tests/_out/intent_llm_latest.jsonl`（或新时间戳路径）；归档后仓库内**可能暂无**无后缀 `intent_llm_latest.*`，勿误读旧路径。

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

## 复跑三（**前**冻结验收轮，历史对照；**2026-05-07 总设同意**后由复跑五接任冻结）

| 项 | 值 |
|----|-----|
| 归档 | `intent_llm_latest_20260507_113718_v1fb3_acc0933_macro0932.jsonl` / `.csv` |
| `v1_fallback` | **3** / 60 |
| 汇总 | **ok=56**，**acc≈0.933**，**macro-F1≈0.932**（**> 0.90**） |
| per-class F1 | text2sql **≈0.974**，rag **≈0.933**，direct **≈0.889** |
| 分桶 | Text2SQL **19/20**；RAG **21/24**；Direct **16/16**；多轮 **9/10** |
| `raw_response.cache` | 评测集 60 条均为 **`miss`**（逐条独立 `(query,history)`，无重复键；**不表示**线上缓存失效） |

### 混淆矩阵（复跑三，expected → predicted）

| expected \\ predicted | text2sql_query | rag_search | direct_answer |
|------------------------|----------------|------------|----------------|
| text2sql_query | 19 | 0 | 1 |
| rag_search | 0 | 21 | 3 |
| direct_answer | 0 | 0 | 16 |

### `ok=false`（共 4）

- **i=16** `text2sql_query`→`direct_answer`：`v1_fallback`（超时降级）。  
- **i=26** `rag_search`→`direct_answer`：`v1_fallback`。  
- **i=33** `rag_search`→`direct_answer`：真 LLM（「如何计算 confusion matrix」判 direct）。  
- **i=56** `rag_search`→`direct_answer`：真 LLM（多轮「那需要查数据库吗」判 direct）。

### Intent 延迟粗算（复跑三，`latency_ms` 顶层字段）

| 子集 | n | P50 | P95 |
|------|---|-----|-----|
| 全量 | 60 | ≈4496 ms | ≈28424 ms |
| 剔除 `v1_fallback` | 57 | ≈4327 ms | ≈12492 ms |

**结论**：本轮满足 P1-Eval **macro-F1 > 90%** 与分桶门槛；**曾为冻结验收轮**，总设已同意切换至 **复跑五**（见上表与「复跑五」节），本段保留作历史对照。

---

## 复跑四（本地 rerun，补充归档）

> **与冻结轮关系**：冻结验收已切换至 **复跑五**；本条仍为 **2026-05-07** 使用 `.env` 的对照跑批（默认超时口径下 **RAG 21/24**），便于与复跑五（`TIMEOUT_S=60`、**RAG 22/24**）对比。后续误判优化走 **P1-D**。

| 项 | 值 |
|----|-----|
| 归档 | `tests/_out/intent_llm_20260507_1509_v1fb1_acc9500_macro9492.{jsonl,csv}` |
| 命名 | `v1fb1` = `v1_fallback` **1**；`acc9500`≈**0.950**（57/60）；`macro9492`≈**macro-F1 0.949** |
| 汇总 | **ok=57/60**，**acc≈0.950**，**macro-F1≈0.949** |
| `v1_fallback` | **1**/60 |
| 分桶 | Text2SQL **20/20**；RAG **21/24**；Direct **16/16**；多轮 i=51–60 **9/10** |
| 相对复跑三 | acc / macro 略升，`v1_fallback` 更少；**RAG 正确数未变**（仍为 21） |

### `ok=false`（共 3）

1. **i=21** `rag_search`→`direct_answer`：**`v1_fallback`**（超时降级，`latency_ms`≈32118，`conf=0.60`），query「什么是RAG」。
2. **i=33** `rag_search`→`direct_answer`：真 LLM，`conf=0.95`，query「如何计算 confusion matrix」。
3. **i=56** `rag_search`→`direct_answer`：真 LLM（多轮），`conf=0.85`，query「那需要查数据库吗」。

### Intent 延迟粗算（复跑四，顶层 `latency_ms`）

| 子集 | n | P50 | P95 | P99 |
|------|---|-----|-----|-----|
| 全量 | 60 | ≈6983 ms | ≈16345 ms | ≈25016 ms |

### 复跑命令（密钥已在 `.env`，一行）

```bash
cd ai-ink-brain-api-python && CHATBI_V2_INTENT_EVAL=true CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_EVAL_OUT=tests/_out/intent_llm_rerun.jsonl python -m pytest tests/test_intent_agent_accuracy.py -m intent_eval -s
```

跑完后将 `intent_llm_rerun.{jsonl,csv}` **改名**为带统计的 stem（见上表「归档」行），避免覆盖。

**提示**：逐条进度依赖 **`pytest -s`**（关闭输出捕获）；否则长时间无打印属正常现象。

---

## 复跑五 / **当前冻结验收轮**（`CHATBI_V2_INTENT_TIMEOUT_S=60`）

> **总设裁定（2026-05-07）**：同意将 **P1-Eval 冻结验收**从复跑三切换至本轮（本文件名）。复跑三保留为历史对照。  
> **目的**：在 **`CHATBI_V2_INTENT_TIMEOUT_S=60`** 下复跑 60 条，降低 `v1_fallback` 条数并改善 RAG 桶（相对复跑三/四）。

| 项 | 值 |
|----|-----|
| 归档 | `tests/_out/intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.{jsonl,csv}` |
| 环境 | `.env` 中 **`CHATBI_V2_INTENT_TIMEOUT_S=60`**（与复跑四默认超时对比） |
| 汇总 | **ok=57/60**，**acc≈0.950**，**macro-F1≈0.948** |
| `v1_fallback` | **1**/60 |
| 分桶 | Text2SQL **19/20**；RAG **22/24**；Direct **16/16**；多轮 i=51–60 **9/10** |
| 相对复跑四 | **RAG +1**（22/24）；**Text2SQL −1**（`v1_fallback` 从 i=21 迁至 **i=16「本季度销售额趋势」**，`latency_ms` 仍顶高） |

### `ok=false`（共 3）

1. **i=16** `text2sql_query`→`direct_answer`：**`v1_fallback`**，`latency_ms` 很高（≈65s 量级），仍为超时降级链路。  
2. **i=33** `rag_search`→`direct_answer`：真 LLM（与复跑四同类）。  
3. **i=56** `rag_search`→`direct_answer`：真 LLM，多轮（与复跑四同类）。

### Intent 延迟粗算（复跑五，顶层 `latency_ms`）

| 子集 | n | P50 | P95 | P99 |
|------|---|-----|-----|-----|
| 全量 | 60 | ≈7336 ms | ≈16211 ms | ≈41945 ms |
| 剔除 `v1_fallback` | 59 | ≈7336 ms | ≈14281 ms | — |

---

## 待网络稳定后（任务跟踪）

- [x] **（2026-05-07）** 已归档复跑三 `intent_llm_latest_20260507_113718_v1fb3_acc0933_macro0932.*`（**前**冻结轮，历史对照）。
- [x] **（2026-05-07 总设同意）** **冻结验收轮已切换为复跑五** `intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.*`（`TIMEOUT_S=60`）；任务单 `task_chatbi_v2_agent_p1_eval_benchmark_v1.md` 已同步。
- [x] **（2026-05-07 补充）** **复跑四** 仍为对照跑批；**P1-Eval 数值门槛**以冻结轮（复跑五）为准仍满足；残余 3 条误判与 1 条 `v1_fallback` 进入 **P1-D** / 上游稳定性跟踪。
- 可选：跑前记录上游 RTT / 并发；仍不达标再进入 **P1-D**（超时阈值、重试、prompt、金标口径）。

---

## 复跑命令（与 PROJECT_CONFIG 对齐）

### A) 60 条准确率 + JSONL + CSV

```bash
export CHATBI_V2_INTENT_EVAL=true
export CHATBI_V2_INTENT_LLM=true
export SILICONFLOW_API_KEY="..."
export INTENT_LLM_MODEL="Qwen/Qwen2.5-7B-Instruct"   # 或 deepseek-ai/DeepSeek-V4-Pro 等
# 若控制台出现「意图识别超时」且 latency≈3s：上游慢于默认 wait_for，请加大例如：
# export CHATBI_V2_INTENT_TIMEOUT_S=20
# 可选（推荐写入仓库内，便于归档）：相对路径二选一（与 pytest cwd 无关）
# export CHATBI_V2_INTENT_EVAL_OUT="tests/_out/intent_llm_latest.jsonl"
# export CHATBI_V2_INTENT_EVAL_OUT="_out/intent_llm_latest.jsonl"
# 仍可用绝对路径：export CHATBI_V2_INTENT_EVAL_OUT="/tmp/intent_run.jsonl"

python -m pytest tests/test_intent_agent_accuracy.py -m intent_eval -s
# `-s` 建议保留：否则 pytest 捕获 stdout，长时间看不到 `[intent_eval]` 进度。
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

## 验收数值对照表（首轮 / 复跑二 / **冻结轮·复跑五**）

| 项 | 目标 / 备注 | 首轮（较早） | 复跑二（网络差，已归档） | **冻结轮（复跑五，`tout60`，已归档）** |
|----|-------------|--------------|--------------------------|----------------------------------------|
| macro-F1 | > 90% | **≈0.868**（未） | **≈0.821**（未） | **≈0.948**（**达标**） |
| Text2SQL | ≥ 17/20 | **18/20** | **16/20** | **19/20** |
| RAG（24 条 `rag_search`） | 见任务单 | **18/24** | **17/24** | **22/24** |
| Direct | 当前 16 条 | **16/16** | **16/16** | **16/16** |
| 多轮 i=51–60 | ≥ 8/10 | **8/10** | **7/10** | **9/10** |
| `v1_fallback` | 过程性 | **10** | **15** | **1** |
| Intent P50 / P95（JSONL 粗算） | Overview 仍远未达理想 | 见上文 | 全量 P50≈8498ms，P95≈31037ms | 全量 P50≈7336ms，P95≈16211ms；剔除 fallback 后 P50≈7336ms，P95≈14281ms |
| B2 | diary 链 | **TBD** | **TBD** | **TBD** |

**附（复跑三，前冻结轮）**：macro≈0.932、RAG 21/24、`v1_fallback=3`、延迟粗算见「复跑三」专节。  
**附（复跑四）**：Intent 全量粗算 P50≈6983ms、P95≈16345ms，见「复跑四」专节。

---

## 备注

- **2026-05-07**：总设**书面同意**将 P1-Eval **冻结验收轮**由复跑三切换为复跑五（`intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.*`）；任务单 `task_chatbi_v2_agent_p1_eval_benchmark_v1.md` 与 `task_chatbi_v2_agent_p1_behavior.md` 已同步。
- 更早模板见 `docs/diary/2026-04-30-p1-intent-benchmark.md`；本文件为 **P1-Eval v1** 当日归档与复跑入口。
- CI：`pytest` 默认不设置 `CHATBI_V2_INTENT_EVAL` / `CHATBI_V2_INTENT_BENCH_RUN`，相关用例跳过；stub 用例覆盖导出与零外呼门禁。
