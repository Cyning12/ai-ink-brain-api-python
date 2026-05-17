# ChatBI V2 P1-Intent 评测会话 — 结果与操作备忘（独立归档）

> 本文档与 `2026-05-06-p1-intent-benchmark.md`（复跑命令与验收表）互补：**侧重本轮已落地行为、排障结论与文件索引**。  
> 关联任务：`docs/tasks/active/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`

---

## 1. 本轮结论摘要

| 主题 | 结论 |
|------|------|
| 「意图识别超时，降级到 V1 规则路由」 | 多为 **`asyncio.wait_for` 默认 3s** 短于 SiliconFlow 实际首包耗时；**不是模型坏了**。 |
| 缓解方式 | 在环境或 `.env` 设置 **`CHATBI_V2_INTENT_TIMEOUT_S`**（建议 `20`～`30`）；`api/intent_agent.py` 已让该变量作用于 `_llm_decide_v2`。 |
| 评测写入「像卡住」 | 60 次 LLM 结束后写 JSONL/CSV 本应极快；已增强 **分段进度 + 耗时/字节数 + `flush`**，便于区分「写盘」与「打印 Summary」。 |
| 60 条进度 | 每条 **`>>> 开始` / `<<< 结束`**；可用 **`CHATBI_V2_INTENT_EVAL_PROGRESS=false`** 关闭（CI stub 用例已强制关）。 |

---

## 2. 已改动文件（代码 / 配置文档）

| 路径 | 说明 |
|------|------|
| `api/intent_agent.py` | `_effective_intent_llm_timeout_s`：`CHATBI_V2_INTENT_TIMEOUT_S` 覆盖 Intent LLM `wait_for` 上限。 |
| `tests/test_intent_agent_accuracy.py` | 逐条进度；写入 JSONL/CSV 分段日志与 `json.dumps(..., default=str)`；`_print_report` 全 `flush=True`；stub 测试关进度。 |
| `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | `CHATBI_V2_INTENT_TIMEOUT_S`、`CHATBI_V2_INTENT_EVAL_PROGRESS` 等真值说明更新。 |
| `docs/diary/2026-05-06-p1-intent-benchmark.md` | 复跑命令处补充超时提示。 |
| `docs/diary/2026-05-06-p1-intent-eval-session-result.md` | **本文件**（会话结果单独落盘）。 |

---

## 3. 环境变量速查（评测常用）

| 变量 | 作用 |
|------|------|
| `CHATBI_V2_INTENT_EVAL=true` | 允许跑 `@pytest.mark.intent_eval` 的 smoke（60 条）。 |
| `CHATBI_V2_INTENT_LLM=true` / `false` | 真实 LLM / 启发式（零外呼）。 |
| `CHATBI_V2_INTENT_TIMEOUT_S` | Intent LLM 单次等待秒数（**缓解超时降级**）。 |
| `CHATBI_V2_INTENT_EVAL_OUT` | JSONL 路径；CSV 为同 stem `.csv`。 |
| `CHATBI_V2_INTENT_EVAL_PROGRESS` | 逐条与写入阶段日志，默认 `true`。 |
| `SILICONFLOW_API_KEY`、`INTENT_LLM_MODEL` | 真实 LLM 必需（与主对话 `SILICONFLOW_CHAT_MODEL` 独立）。 |

**优先级**：已在 shell 中 `export` 的变量 **优先于** `.env`（`rag_env.load_dotenv(..., override=False)`）。

---

## 4. 推荐复跑命令（真实 LLM 60 条）

```bash
cd /path/to/ai-ink-brain-api-python

export CHATBI_V2_INTENT_EVAL=true
export CHATBI_V2_INTENT_LLM=true
export CHATBI_V2_INTENT_TIMEOUT_S=25
export SILICONFLOW_API_KEY="..."
export INTENT_LLM_MODEL="deepseek-ai/DeepSeek-V4-Flash"

# 可选：避免覆盖历史结果
export CHATBI_V2_INTENT_EVAL_OUT="/tmp/intent_llm_$(date +%Y%m%d_%H%M).jsonl"

python -m pytest tests/test_intent_agent_accuracy.py -m intent_eval -s
```

完成后把指标与 Top 误判填入 `docs/diary/2026-05-06-p1-intent-benchmark.md` 的验收表。

---

## 5. 终止当前任务

在运行 `pytest … -m intent_eval` 的终端按 **`Ctrl+C`**（macOS 即 **SIGINT**）即可中断。

- **未写完 JSONL**：当前实现为 **60 条全部跑完后** 再一次性 `open("w")` 写盘；若中断发生在 **第 60 条结束之前**，`/tmp` 或默认路径下可能仍是 **上一轮完整文件** 或 **未刷新**；以文件时间戳为准。  
- **已在「写入 JSONL/CSV」之后中断**：一般已得到完整 JSONL/CSV。  
- **无副作用**：仅为本地评测进程，不修改数据库业务数据。

---

## 6. 启发式 vs 真实 LLM（避免误判日志）

`CHATBI_V2_INTENT_LLM=false` 时，`reasoning` 为 **`_heuristic_decide` 固定模板**，macro-F1 与金标不对齐属正常，**只验证导出链路**。

---

## 给 Cursor

验收、P1-Eval、`CHATBI_V2_INTENT_TIMEOUT_S`、超时降级、JSONL、pytest `-s`、`flush`。
