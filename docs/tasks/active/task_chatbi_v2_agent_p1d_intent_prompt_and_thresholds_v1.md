# Task：ChatBI V2 Agent（P1-D）— Intent 误判调优（Prompt / 阈值 / 超时策略）（v1）

状态：pending  
范围：仅后端 `ai-ink-brain-api-python`  
前置：
- **P1-Eval**：已有可复跑 `intent_eval` + 归档 JSONL/CSV；**冻结/对照口径**以 `docs/diary/2026-05-06-p1-intent-benchmark.md` 与 `task_chatbi_v2_agent_p1_eval_benchmark_v1.md` 为准（勿虚构数字）。
- **P1-C**：`task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md` 已 **done**；本任务**不**改 LRU/TTL/复合 key 语义，除非缺陷修复。

关联：
- `docs/tasks/active/task_chatbi_v2_agent_p1_behavior.md`（P1 总览 §D）
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Intent.md`（工具定义、输出 JSON 约定）
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Gap-Checklist.md`（与 Overview 对齐时的缺口跟踪）

---

## 背景与目标

冻结轮后 **macro-F1 已达标**，但 **RAG 桶（24 条 `rag_search`）相对总览「>90%」仍可能未闭合**（历史约 **21/24**）；另有少量 **`v1_fallback`**（超时 → V1）与 **真 LLM 边界误判**（如「通用概念 vs 项目内文档」「多轮澄清 vs rag」）。

**目标**：在 **不引入新 SSE 事件类型**、**CI 仍不调真实 LLM** 的前提下，通过 **Prompt 迭代** 与 **（必要时）置信度 / fallback / 超时策略** 的可解释调整，提升 **RAG 召回** 与 **稳定性指标（`v1_fallback` 占比）**，且每次改动可对照 **同一套 60 条** 做前后对比。

---

## 范围 / 非范围

### 范围（WBS）

- [ ] **D1. Prompt 调优**
  - **落点**：`api/intent_agent.py` 中 `_llm_decide_v2` 的 **user prompt** 与（如需）**system** 侧约束；工具说明以 `tests/test_intent_agent_accuracy.py` / `api/tools.py` registry 为准，避免与线上描述漂移。
  - **策略建议**（实现时择一或多轮）：
    - 强化 **「须检索项目内文档 / 规范 / 任务单 / 仓库约定」** 与 **「可仅凭通用知识 direct」** 的边界；
    - 对 **多轮** 显式要求结合 `history` 判断省略主语、指代是否仍属「需查资料」类；
    - 可选 **few-shot**（短、可维护，避免 prompt 爆炸导致延迟上升）。
  - **验收**：至少 **1 轮** 可合并的 Prompt 变更，附带 **前后** `intent_eval` 汇总（macro-F1、**RAG 24 条**、**`v1_fallback` 条数**、Top 误判 diff）。

- [ ] **D2. 置信度与 fallback / 超时（按需）**
  - **落点**：`api/intent_agent.py`（`_fallback_tool_by_low_confidence`、与 `min_confidence` 相关逻辑）；`api/agent.py`（`INTENT_MIN_CONFIDENCE` 读取）；`CHATBI_V2_INTENT_TIMEOUT_S` 与超时后 **`v1_fallback`** 行为说明。
  - **约束**：默认路径行为变化须被 **stub 单测** 或 **评测用例** 覆盖意图；禁止「为刷分」无原则抬高超时掩盖慢上游。
  - **验收**：若有参数变更，更新 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`；**`v1_fallback` 与误判** 在 diary 或本任务「实现备忘」中 **前后对照**。

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

- [ ] **对照跑批**：每次合并意图的 Prompt/阈值改动前或同 PR 内，完成一次 **`pytest … -m intent_eval`**（真实 LLM），导出 **带时间戳** 的 JSONL/CSV（避免覆盖 `tests/_out/` 既有归档）。
- [ ] **RAG 桶**：在 **24 条 `rag_search` 金标** 上，**相对进入本任务时的基线**（见 diary 冻结/复跑节）**提升或持平且不误伤**：若总览仍坚持「>90%（24 条）」，则以 **≥22/24** 为建议目标并在任务备忘中写明实际达成；未达标须列 **剩余误判 i 列表** 与 **归因**（prompt / 金标 / 超时）。
- [ ] **macro-F1**：**不得低于**进入本任务时的冻结轮 macro（**回归红线**）；若因收紧 direct 导致 macro 波动，须在 diary 说明取舍。
- [ ] **`v1_fallback`**：若有超时策略调整，报告 **条数 + 典型 latency**；禁止仅报告 acc 掩盖 fallback。

### 工程

- [ ] **PROJECT_CONFIG**：新增或变更的 env 写入 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`。
- [ ] **契约**：若动到对外可见字段（极少），同步 `docs/_tech_graph/_contract_manifest.json` 并跑 `python tools/tech_graph_contract_check.py`。
- [ ] **回归**：`pytest`（含 `tests/test_intent_agent_accuracy.py` stub 路径、`tests/test_intent_cache.py`）与 contract_check **全绿**。

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
| 基线归档文件名 | `<从 diary / tests/_out 拷贝>` |
| 本轮归档文件名 | `<待补>` |
| 涉及 PR / commit | `<待补>` |
| 仍存争议金标 | `<i=… 简述>` |

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
