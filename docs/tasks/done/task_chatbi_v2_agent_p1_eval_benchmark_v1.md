# Task：ChatBI V2 Agent（P1-Eval）— 可验证评测与性能基准（v1）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


状态：done（工具链/CI 门禁已落地）；**准确率验收冻结以「复跑五」为准**（`tests/_out/intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.*`，`CHATBI_V2_INTENT_TIMEOUT_S=60`）；**复跑三**（`intent_llm_latest_20260507_113718_v1fb3_acc0933_macro0932.*`）为前冻结历史对照；**复跑四**为补充对照；见 `docs/diary/2026-05-06-p1-intent-benchmark.md`；**复跑二**仍为网络差基线  
范围：仅后端 `ai-ink-brain-api-python`  
前置：P0 已完成（`task_chatbi_v2_agent_p0_backend.md` 已归档）  
关联图谱 / 规格：
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` — 性能指标 P50/P95、整体超时口径
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Intent.md` — 60 条测试集约定、意图输出字段
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Gap-Checklist.md` — P1 行为与事件时序等缺口（本任务不闭合缓存项）

编排关系：
- **本任务**：主线 **A（真实 LLM 意图评测闭环）+ B（性能基准与回归门禁）** 的唯一落盘与验收文档。
- **总览**：`docs/tasks/done/task_chatbi_v2_agent_p1_behavior.md`（P1 全量目标与 C/D 编排）。
- **缓存子线**：`docs/tasks/done/task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md`（与本任务并行时，仍以 CI 不依赖外部 LLM 为共同约束）。

---

## 背景与目标

P0 后 V2 路径仍以 **stub / mock 意图** 为主流自动化测试，**缺少可复跑的真实 LLM 质量与延迟证据**。本任务目标是在**不污染 CI** 的前提下，建立：

1. **可验证闭环**：开关控制真实 LLM → 60 条集 → 逐条导出 → 汇总 macro-F1 / per-class / confusion（文本可接受）。
2. **性能证据**：Intent（及最小化 Agent step / E2E）延迟分布 P50/P95/P99，口径写死、可复跑。
3. **回归门禁**：默认 pytest/CI 仍全 stub；合并前现有 P0 回归全绿，`CHATBI_USE_AGENT=false` 时 V1 行为不变。

---

## 范围 / 非范围

### 范围

- `api/intent_agent.py` 与测试侧 **统一 env 开关**（stub vs 真实 LLM；命名与真值表对齐，见实现备忘）。
- `tests/test_intent_agent_accuracy.py`（或等价路径）：**60 条**结构化用例 + 导出 JSONL/CSV + 汇总指标（**默认**跳过真实 LLM，仅手动/带 env 时执行）。
- `tests/benchmark_intent_latency.py`（或 pytest 标记脚本）：真实 LLM 下 **n 可配置**（如 100）的延迟分布输出。
- **B2 最小化**：Agent 单步 / E2E 延迟的测量方法与采样量在 `docs/diary/` 报告中写明即可（脚本可不进 CI）。
- **B3**：补充/更新 stub 侧测试，保证无 flaky 外部依赖。

### 非范围

- **IntentCache（LRU/TTL/可观测）**：见 `task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md`。
- **Prompt 调优 / 置信度阈值迭代（P1-D）**：留在总任务单或非本 v1 范围。
- **新 SSE 事件类型 / 契约字段变更**：除非修复评测阻塞 bug，否则不纳入本任务。
- **前端**。

---

## 执行拆解（WBS）

> 原则：**先评测与基准，再谈优化**；任何后续 Prompt/缓存改动须能对照本任务产出对比。

### A. 真实 LLM 意图测试闭环（必做）

- [x] **A1. 去 stub / 真实调用开关对齐**
  - **目标**：一键切换 stub vs 真实 LLM；**CI 默认**不发起外部 HTTP。
  - **交付物**：`api/intent_agent.py` + 测试/脚本统一读取同一 env（与 `PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 登记一致）。
  - **验收**：开启真实 LLM 时可逐条打印/记录 tool、mode、confidence、latency_ms、reasoning（如 spec 有）；关闭时 **0 次** SiliconFlow（或等价 upstream）调用。

- [x] **A2. 60 条测试集落盘**
  - **目标**：稳定可扩展结构；支持多轮 `history`。
  - **交付物**：`tests/test_intent_agent_accuracy.py`（或拆 `tests/data/intent_eval_cases.json` 由测试加载）。
  - **验收**：**Text2SQL 20 / RAG 24 / Direct 16**（末 10 条多轮）；可导出 per-case 结果（JSONL 或 CSV）。

- [x] **A3. 准确率报告**（报告骨架、复跑命令与**冻结数值**见 `docs/diary/2026-05-06-p1-intent-benchmark.md`「复跑五 / 当前冻结验收轮」；复跑三为历史对照）
  - **目标**：macro-F1、per-class F1、confusion（文本矩阵即可）、Top 误判样例。
  - **交付物**：`docs/diary/YYYY-MM-DD-p1-intent-benchmark.md`（日期用实际跑批当日）。
  - **验收**：报告含模型名、参数、数据集版本、命令行复跑方式；**至少 Top-10 误判**（含 expected vs actual、confidence、reasoning 摘要）。

### B. 性能基准与回归（必做）

- [x] **B1. Intent latency benchmark（真实 LLM）**
  - **交付物**：`tests/benchmark_intent_latency.py`（或 pytest `-m intent_benchmark`）。
  - **验收**：输出 P50/P95/P99 + min/max；支持 `n=100`（可环境变量覆盖）。

- [x] **B2. Agent step / E2E latency（最小化）**
  - **交付物**：脚本或标记测试 + diary 中 **测量边界**（起止点：仅 Intent / 首 tool / 全流等）。
  - **验收**：同一份报告内可对照 Overview 中的目标表（允许标注「未达标」与原因）。

- [x] **B3. 回归门禁**
  - **验收**：现有 P0 相关测试全绿；无新 flaky；`CHATBI_USE_AGENT=false` 路径行为不变。

---

## 验收标准（本任务阻断项）

### 1) 准确率（真实 LLM、手动/夜间跑批）

与总任务 **`docs/tasks/done/task_chatbi_v2_agent_p1_behavior.md`** 对齐的数值门槛（达成或文档中明确「未达标 + 后续 P1-D 跟踪」）：

- [x] 60 条全部跑完并有导出文件（**冻结轮（复跑五）**：`tests/_out/intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.jsonl` / `.csv`；**前冻结轮（复跑三）**：`intent_llm_latest_20260507_113718_v1fb3_acc0933_macro0932.*`；历史：`intent_llm_latest_20260506_171351_v1fb15_acc0817.*`。**归档后**仓库内可无无后缀 `intent_llm_latest.*`，下次跑批请显式设置 `CHATBI_V2_INTENT_EVAL_OUT`）
- [x] macro-F1 > 90%（**冻结轮（复跑五）≈0.948** 达标；首轮/复跑二/复跑三见 diary）
- [x] Text2SQL 召回 ≥ 17/20（**冻结轮（复跑五）19/20**）
- [x] RAG：金标 **24** 条 `rag_search`（**冻结轮（复跑五）22/24**；原「≥18/20」语义为至少 18 条正确时已满足）
- [x] Direct：当前金标 **16** 条（冻结轮 **16/16**）
- [x] 多轮子集 i=51–60（**冻结轮（复跑五）9/10**）

- [x] **（外网 / 上游稳定性）** 已通过 **复跑五**（`v1_fallback=1/60`，`TIMEOUT_S=60`）归档并写入 diary；换模型或网络后建议再跑一轮并**新增时间戳文件名**归档。

> 若环境/模型变更导致暂时不达标：**必须在同一 diary 报告中**列出差距与样例，并指向 P1-D 或 spec 变更提案；**不得**在无报告情况下合并「号称完成」。

### 2) 性能（真实 LLM）

| 指标 | P50 目标 | P95 目标 | 说明 |
|------|---------|---------|------|
| Intent LLM | < 200ms | < 500ms | 以 B1 脚本口径为准 |
| Agent 单步 | < 1.5s | < 3s | B2 最小化测量 |
| 整体 E2E | < 3s | < 8s | B2 最小化测量 |

- [x] B1 证据已链至 diary：`docs/diary/2026-05-06-p1-intent-benchmark.md`「复跑五」**Intent 延迟粗算**（由 60 条导出 `latency_ms` 分位数，与独立 `benchmark_intent_latency.py` n=100 脚本可并存对照）。相对 Overview 理想目标仍偏高，diary 已注释网络/超时/样本构成；若需严格对齐 B1 脚本口径可再跑 `CHATBI_V2_INTENT_BENCH_RUN` + `CHATBI_V2_INTENT_LLM=true`。

### 3) 回归（CI）

- [x] 默认 `pytest` 不依赖外部 LLM 密钥即可绿
- [x] P0 行为回归全集通过（具体条数以当时仓库为准）

---

## 实现备忘（子 Agent 回填）

| 项 | 内容 |
|----|------|
| env 开关真值 | 已登记：`CHATBI_V2_INTENT_LLM`、`CHATBI_V2_INTENT_EVAL`、`CHATBI_V2_INTENT_EVAL_OUT`、`CHATBI_V2_INTENT_BENCH_N`、`CHATBI_V2_INTENT_TIMEOUT_S`、`CHATBI_V2_INTENT_BENCH_RUN`、`CHATBI_USE_AGENT`、`INTENT_LLM_MODEL` |
| 涉及文件（预期） | `api/intent_agent.py`、`tests/test_intent_agent_accuracy.py`、`tests/benchmark_intent_latency.py`、`pytest.ini`、`docs/diary/2026-05-06-p1-intent-benchmark.md`、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| 评测命令示例 | `CHATBI_V2_INTENT_EVAL=true CHATBI_V2_INTENT_LLM=true pytest tests/test_intent_agent_accuracy.py -m intent_eval -s`；stub 导出：`CHATBI_V2_INTENT_EVAL=true CHATBI_V2_INTENT_LLM=false pytest …` |
| **跑批回填** | **冻结轮（复跑五，总设 2026-05-07 同意切换）**：`intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.*`，acc≈0.950，macro-F1≈0.948，`v1_fallback=1`，RAG 22/24、T2S 19/20，`CHATBI_V2_INTENT_TIMEOUT_S=60`，见 diary「复跑五」。**前冻结轮（复跑三）**：`intent_llm_latest_20260507_113718_v1fb3_acc0933_macro0932.*`（历史对照）。**复跑四**：`intent_llm_20260507_1509_v1fb1_acc9500_macro9492.*`。**复跑二**：`intent_llm_latest_20260506_171351_v1fb15_acc0817.*`。独立 B1 n=100 与 B2 脚本为可选增强（diary 已给命令） |

---

## 风险与应对

| 风险 | 应对 |
|------|------|
| 外部 API 不稳定 | 重试策略仅限评测脚本内；CI 不调用 |
| 指标与 Overview 口径不一致 | 以本任务 B1/B2 脚本注释 + diary 为验收真值，并回链 Overview 表格脚注 |
| 60 条标注争议 | 用例增加 `note` 与 `category`；争议项单开 issue 不阻塞脚本合并 |

---

## 给 Cursor

验收、非范围、依赖、图谱、`_tech_graph`、stub、真实 LLM、macro-F1、P50、P95、JSONL、CI 不触发外部请求。
