# Task：ChatBI V2 Agent（P1-D）— Intent 误判调优（Prompt / 阈值 / 超时策略）（v1）

状态：**done**（2026-05-07：`intent_eval` 已跑并归档 `intent_llm_20260507_160444_p1d_live.*`；见 `docs/diary/2026-05-07-p1-intent-p1d.md` 前后表）  
范围：仅后端 `ai-ink-brain-api-python`  
前置：
- **P1-Eval**：已有可复跑 `intent_eval` + 归档 JSONL/CSV；**冻结/对照口径**以 `docs/diary/2026-05-06-p1-intent-benchmark.md` 与 **`docs/tasks/done/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`** 为准（勿虚构数字）。
- **P1-C**：`docs/tasks/done/task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md` 已 **done**；本任务**不**改 LRU/TTL/复合 key 语义，除非缺陷修复。

关联：
- `docs/tasks/done/task_chatbi_v2_agent_p1_behavior.md`（P1 总览 §D）
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`（**§7.4** 全量对照、**§7.5** 深度回归 L1/L2）
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Intent.md`（工具定义、输出 JSON 约定）
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Gap-Checklist.md`（与 Overview 对齐时的缺口跟踪）

---

## 背景与目标

冻结轮后 **macro-F1 已达标**，但 **RAG 桶（24 条 `rag_search`）相对总览「>90%」仍可能未闭合**（历史约 **21/24**）；另有少量 **`v1_fallback`**（超时 → V1）与 **真 LLM 边界误判**（如「通用概念 vs 项目内文档」「多轮澄清 vs rag」）。

**目标**：在 **不引入新 SSE 事件类型**、**CI 仍不调真实 LLM** 的前提下，通过 **Prompt 迭代** 与 **（必要时）置信度 / fallback / 超时策略** 的可解释调整，提升 **RAG 召回** 与 **稳定性指标（`v1_fallback` 占比）**，且每次改动可对照 **同一套 60 条** 做前后对比。

---

## 范围 / 非范围

### 范围（WBS）

- [x] **D1. Prompt 调优**
  - **落点**：`api/intent_agent.py` 中 `_llm_decide_v2` 的 **user prompt** 与（如需）**system** 侧约束；工具说明以 `tests/test_intent_agent_accuracy.py` / `api/tools.py` registry 为准，避免与线上描述漂移。
  - **策略建议**（实现时择一或多轮）：
    - 强化 **「须检索项目内文档 / 规范 / 任务单 / 仓库约定」** 与 **「可仅凭通用知识 direct」** 的边界；
    - 对 **多轮** 显式要求结合 `history` 判断省略主语、指代是否仍属「需查资料」类；
    - 可选 **few-shot**（短、可维护，避免 prompt 爆炸导致延迟上升）。
  - **验收**：至少 **1 轮** 可合并的 Prompt 变更，附带 **前后** `intent_eval` 汇总（macro-F1、**RAG 24 条**、**`v1_fallback` 条数**、Top 误判 diff）。（**数字回填**：见 `docs/diary/2026-05-07-p1-intent-p1d.md`「待真实 LLM 跑批」。）

- [x] **D2. 置信度与 fallback / 超时（按需）**
  - **落点**：`api/intent_agent.py`（`_fallback_tool_by_low_confidence`、与 `min_confidence` 相关逻辑）；`api/agent.py`（`INTENT_MIN_CONFIDENCE` 读取）；`CHATBI_V2_INTENT_TIMEOUT_S` 与超时后 **`v1_fallback`** 行为说明。
  - **约束**：默认路径行为变化须被 **stub 单测** 或 **评测用例** 覆盖意图；禁止「为刷分」无原则抬高超时掩盖慢上游。
  - **验收**：若有参数变更，更新 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`；**`v1_fallback` 与误判** 在 diary 或本任务「实现备忘」中 **前后对照**。（本轮：**代码默认值未改**；已增补 `CHATBI_V2_INTENT_TIMEOUT_S` / `INTENT_MIN_CONFIDENCE` 真值说明。）

### 非范围

- 不新增 **SSE `type`**、不扩展契约 payload 新事件（`debug_router` 下已有字段除外）。
- 不改 **前端**（`ai-ink-brain`）。
- 不在本任务内 **批量改 60 条金标**；若争议样例需改金标，单开评审或子任务并注明版本号。
- 不重写 **P1-C 缓存** 核心语义（key / TTL / LRU）。

---

## 设计约束

- **CI**：`pytest` 默认 **零外呼**；真实 LLM 评测仅本地 `CHATBI_V2_INTENT_LLM=true` + 密钥。
- **可回滚**：Prompt/阈值变更建议小步提交，便于 bisect。
- **指标诚实**：`v1_fallback` 与「模型判错」分列归因；macro-F1 与分桶同步报告。

---

## 验收标准（阻断项）

### 功能与质量

- [x] **对照跑批**：已完成 **`pytest … -m intent_eval`**（真实 LLM），归档 **`tests/_out/intent_llm_20260507_160444_p1d_live.{jsonl,csv}`**，过程日志 **`…_p1d_live.log`**（`tee`）。
- [x] **RAG 桶**：**22/24**，相对冻结基线 **持平（≥22/24）**；剩余 **`ok=false`：i=36、i=38**，均为 **`v1_fallback`**（`latency_ms`≈65s），归因 **超时/上游**，非金标争议。
- [x] **macro-F1**：**≈0.966**，高于冻结 **≈0.948** 红线。
- [x] **`v1_fallback`**：**3**/60（基线 **1**/60）；其中 **2** 条导致 RAG 误判，**1** 条（i=43）超时后 V1 仍落在 `direct_answer` 故 **acc 仍计 ok**；典型 **`latency_ms`≈60.6–65.3s**，与 `CHATBI_V2_INTENT_TIMEOUT_S=60` 顶满一致。

### 工程

- [x] **PROJECT_CONFIG**：新增或变更的 env 写入 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`。
- [x] **契约**：若动到对外可见字段（极少），同步 `docs/_tech_graph/_contract_manifest.json` 并跑 `python tools/tech_graph_contract_check.py`。（**未改契约**；`tech_graph_contract_check.py` 已本地 **OK**。）
- [x] **回归**：`pytest`（含 `tests/test_intent_agent_accuracy.py` stub 路径、`tests/test_intent_cache.py`）与 contract_check **全绿**。（**命令**：`pytest tests/test_intent_agent_accuracy.py -k "not smoke" tests/test_intent_cache.py -q` — 排除 `intent_eval` smoke，避免 `.env` 打开评测时全量外呼。）

---

## 交付物

| 交付物 | 说明 |
|--------|------|
| `api/intent_agent.py`（及必要时 `api/agent.py`） | Prompt / 阈值 / 超时相关可审计 diff |
| `docs/diary/YYYY-MM-DD-p1-intent-p1d.md` 或增补既有 benchmark diary | **前后对比表** + 复跑命令 + 归档文件名 |
| `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | env 真值增量 |

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 基线归档文件名 | `tests/_out/intent_llm_20260507_1529_v1fb1_acc9500_macro9484_tout60.{jsonl,csv}`（见 `2026-05-06-p1-intent-benchmark.md` 复跑五） |
| 本轮归档文件名 | `tests/_out/intent_llm_20260507_160444_p1d_live.{jsonl,csv,.log}` |
| 涉及 PR / commit | 待补 |
| 本轮汇总 | **ok=58/60，acc≈0.967，macro-F1≈0.966**；T2S **20/20**；RAG **22/24**；Direct **16/16**；**`v1_fallback`=3**（i=36/38 误判，i=43 侥幸 ok） |
| 仍存争议金标 | 无强制改标建议；**RAG 缺口**归因为 **Intent LLM 超时**（i=36、38），非 i=33/56 类 prompt 边界 |
| Prompt 变更摘要 | `_llm_decide_v2`：项目内 vs 通识边界、多轮查库澄清、2 条针对性 few-shot、`history` 6×200；`system` 收紧 JSON-only |
| 回归验证 | `pytest … -k "not smoke" …` + `tech_graph_contract_check.py` 已通过（Agent 环境） |

---

## 风险与应对

| 风险 | 应对 |
|------|------|
| Prompt 变长导致延迟升、`v1_fallback` 反增 | 对比 B1 或 JSONL `latency_ms`；必要时回滚或拆 few-shot |
| 过拟合 60 条 | 变更说明写清「动了哪类边界」；争议样例单列 |
| 与 P1-C 缓存命中语义耦合 | 命中路径不得依赖「未写入缓存的 volatile 字段」；沿用 P1-C 单测 |

---

## 给 Cursor

验收、非范围、依赖、图谱、`_tech_graph`、`intent_eval`、macro-F1、RAG 24、`v1_fallback`、Prompt、`INTENT_MIN_CONFIDENCE`、`CHATBI_V2_INTENT_TIMEOUT_S`、前后对比、CI 不外呼。
