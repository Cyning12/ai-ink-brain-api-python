---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: explore
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
date: 2026-06-08
---

# explore_intent_retry_u1_5_impl_gap

## 1. 实现缺口

**结论：代码已完整，缺口仅剩文档/流程项。**

| 项 | 状态 | 说明 |
|---|---|---|
| `api/intent_agent.py` 重试包装 | 已存在 | `_llm_decide_v2_with_retries` (L513–561) |
| env 读取（RETRIES/BACKOFF/TIMEOUT_FACTORS） | 已存在 | `_intent_llm_max_retries` / `_intent_llm_retry_backoff_s` / `_intent_llm_retry_timeout_factors` |
| timeout 阶梯（1.0 / 0.65 / 0.4） | 已存在 | `_intent_llm_timeout_s_for_attempt` |
| 可观测（used=llm_retry + attempt + timeout_s） | 已存在 | retry_meta 注入 raw_response |
| 日志（will_retry / success / exhausted） | 已存在 | `_log_intent_retry_*` 三套 |
| `.env.example` 注释 | 已存在 | PR #110 已合入 main（CHATBI_V2_INTENT_LLM_RETRIES 等） |
| `tests/test_intent_llm_retry.py` | 已存在 | 6 个 case 全绿 |
| task 验收标准 §自检结论 | **待回填** | 验收标准 checkbox 仍空，须 50 reinspect 后闭合 |

### failure_paths F1–F4 映射

| Scenario ID | 测试覆盖 | 代码路径 |
|---|---|---|
| F1 `fp-u15-retry-exhausted` | `test_intent_llm_retry_exhausted_falls_back_v1` | `_llm_decide_v2_with_retries` 耗尽 → raise `asyncio.TimeoutError` → `decide_intent_v2` catch → `v1_fallback` |
| F2 `fp-u15-json-no-retry` | `test_intent_llm_json_error_not_retried` | `ValueError` 非 `_intent_llm_retryable` → 不重试 → `decide_intent_v2` 外层 catch → 启发式 |
| F3 `fp-u15-retry-success` | `test_intent_llm_retry_succeeds_on_third_attempt` | 第 3 轮成功 → `used=llm_retry` + `attempt=3` |
| F4 `fp-u15-agent-latency` | `test_intent_llm_retry_timeout_decreases_per_attempt` | timeout 阶梯 60→39→24（系数 1.0/0.65/0.4） |

---

## 2. 已有 pytest 状态

```
pytest tests/test_intent_llm_retry.py -q
============================= test session ==============================
6 passed, 3 warnings in 0.25s
```

| 测试函数 | 断言要点 |
|---|---|
| `test_intent_llm_retry_succeeds_on_third_attempt` | 3 次调用、used=llm_retry、attempt=3 |
| `test_intent_llm_retry_exhausted_falls_back_v1` | 3 次调用、used=v1_fallback |
| `test_intent_llm_json_error_not_retried` | 1 次调用、used=heuristic |
| `test_intent_llm_retry_timeout_decreases_per_attempt` | timeouts == [60.0, 39.0, 24.0] |
| `test_intent_llm_retry_logs_without_debug_intent_cache` | caplog 含 [intent-retry] will_retry + success |
| `test_intent_llm_retryable_classifier` | TimeoutError=True, ValueError=False |

**注意**：测试 fixture 已设 `CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S=0`，避免 sleep 拖慢 CI。

---

## 3. 30 帽 TDD 顺序建议

当前实现已完整，30 帽实际为 **验证/回归** 而非从头 TDD：

1. **确认 `.env.example` 注释已含 U1.5 三项 env**（已确认存在）
2. **`pytest tests/test_intent_llm_retry.py -q` 全绿**（已确认 6 passed）
3. **全集 pytest**：`pytest tests -m "not intent_eval and not intent_benchmark" -q`（须 30 帽执行后确认）
4. **若全集绿 → 无代码改动；若红 → 修回归后重跑**

> 30 硬约束（task §Harness 链式关账）：先确认测试绿再判定“无需改代码”。因本 explore 已确认代码存在且测试绿，30 帽可直接进入验证全集。

---

## 4. cherry-pick 来源分支说明

**代码已存在于 `main`**，无需 cherry-pick。

- **原始实现 PR**：`#110` — `feat(chatbi): Intent LLM 外呼重试与超时阶梯 (U1.5)`
- **合入 commit**：`9a01ebd`（已在 main 历史）
- **原始开发分支**：`task/chatbi-intent-llm-retry-u1.5`（已删除或已合，远端不可见；仅剩 `task/chatbi-intent-llm-retry-u1.5-chain-v1` 作为 B 轨链式关账分支）
- **当前链式关账分支**：`task/chatbi-intent-llm-retry-u1.5-chain-v1`（基于 `main@bb0258c`，仅含 harness invoke 文档 commit `f5ff882`）

**差分验证**：`git diff main..task/chatbi-intent-llm-retry-u1.5-chain-v1 -- api/ tests/` 为空，确认 api/tests 无增量改动。

---

## 回报

### Status
- explore 完成：实现已存在 main，测试 6/6 绿，无代码缺口。

### Deliverables
- 本文件：`docs/harness/invokes/by-task/chatbi-intent-retry-u1.5-chain/explore_intent_retry_u1_5_impl_gap.md`
- 前置 invoke：`invoke_20250608_explore_chatbi-intent-retry-u1.5-chain.md`

### Blockers
- 无。30 帽可直接进入全集 pytest 验证。

### Judgment
- B 轨 T1 本 task 为 **“已合代码的 harness 链式补关账”**，非新实现。22 帽可 skip 或仅做 env 注释确认；30 帽跑全集 pytest；40 帽补 RUNBOOK spot-check（可选）；50 落盘 reinspect 为必选项（task `test_strategy: required` + `kpi_aggregator: 50`）。
