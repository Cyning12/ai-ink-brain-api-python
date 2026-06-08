---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: 50
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
date: 2026-06-08
---

# 50 · 独立复检报告

## 复检摘要

本 task 为 B 轨补关账（代码已合 main，PR #110 / commit 9a01ebd）。当前分支 `task/chatbi-intent-llm-retry-u1.5-chain-v1` 基于 `main@bb0258c`，`api/`、`tests/`、`.env.example` 与 main 无差分。

- **pytest 单测**：`tests/test_intent_llm_retry.py` **6 passed**（实测 2026-06-08）。
- **pytest 全集**：`pytest tests -m "not intent_eval and not intent_benchmark"` **323 passed, 1 skipped, 2 deselected**（实测 2026-06-08）。
- **harness_task_validate.py**：`OK`（实测 2026-06-08）。
- **代码安全**：无密钥硬编码、无注入风险、日志不泄露 query、超时/重试边界已 clamp。

---

## 重试阶梯核对（3 次含首次，上限 5）

| 检查项 | 任务单要求 | 代码实现 | 结论 |
|---|---|---|---|
| 默认重试次数 | 3（含首次） | `_intent_llm_max_retries()` L457–465，默认 `3` | 一致 |
| 上限 | 5 | `max(1, min(5, int(raw)))` L462 | 一致 |
| 下限 | 1 | `max(1, min(5, int(raw)))` L462 | 一致 |
| 重试包装器 | `_llm_decide_v2_with_retries` | L513–561，循环 `range(1, max_retries + 1)` | 一致 |

**核对结果**：重试阶梯实现与任务单要求一致。

---

## 超时递减核对（1.0 / 0.65 / 0.4）

| 检查项 | 任务单要求 | 代码实现 | 结论 |
|---|---|---|---|
| 默认系数 | `1.0,0.65,0.4` | `_intent_llm_retry_timeout_factors()` L480–490 | 一致 |
| 首轮 timeout | 全量（系数 1.0） | `_intent_llm_timeout_s_for_attempt(base, 1)` → `base * 1.0` | 一致 |
| 次轮 timeout | 65%（系数 0.65） | `_intent_llm_timeout_s_for_attempt(base, 2)` → `base * 0.65` | 一致 |
| 三轮 timeout | 40%（系数 0.4） | `_intent_llm_timeout_s_for_attempt(base, 3)` → `base * 0.4` | 一致 |
| 边界 clamp | — | `max(0.5, min(120.0, scaled))` L498 | 安全 |
| 测试验证 | `timeout_s == 24.0`（base=60） | `test_intent_llm_retry_timeout_decreases_per_attempt` L109–129 | 通过 |

**测试实测**：`timeouts == [60.0, 39.0, 24.0]`（60 * 1.0 = 60；60 * 0.65 = 39；60 * 0.4 = 24）。

**核对结果**：超时递减实现与任务单要求一致。

---

## failure_paths F1–F4 与测试映射核对

| Scenario ID | 触发条件 | 系统行为 | 测试函数 | 代码路径 | 结论 |
|---|---|---|---|---|---|
| F1 `fp-u15-retry-exhausted` | 3 次均为可重试失败（超时/5xx/限流） | `asyncio.TimeoutError` → `v1_fallback`，reasoning「意图识别超时…」 | `test_intent_llm_retry_exhausted_falls_back_v1` | `_llm_decide_v2_with_retries` 耗尽 raise `TimeoutError` → `decide_intent_v2` catch → `used=v1_fallback` | **覆盖** |
| F2 `fp-u15-json-no-retry` | LLM 返回非 JSON / tool 不在白名单 | **不重试** → `used=heuristic` | `test_intent_llm_json_error_not_retried` | `ValueError` 非 `_intent_llm_retryable` → 直接 raise → 外层 catch → `used=heuristic` | **覆盖** |
| F3 `fp-u15-retry-success` | 前 1～2 次瞬态失败、末次成功 | `used=llm_retry` + `attempt` + 末轮 `timeout_s` | `test_intent_llm_retry_succeeds_on_third_attempt` | 第 3 轮成功 → `meta["used"]="llm_retry"` + `attempt=3` | **覆盖** |
| F4 `fp-u15-agent-latency` | 3 轮 timeout 总和 + RAG > `AGENT_MAX_LATENCY_MS` | Agent 软超时改 tool（与 Step1 F6 叠加） | `test_intent_llm_retry_timeout_decreases_per_attempt` | timeout 阶梯 60→39→24，缩短单次 wait_for 以降低总 latency | **覆盖** |

**补充测试**：
- `test_intent_llm_retry_logs_without_debug_intent_cache`：可观测日志验证（`[intent-retry]` / `will_retry` / `success attempt=2`）。
- `test_intent_llm_retryable_classifier`：重试分类器边界（`TimeoutError` → True；`ValueError` → False）。

**核对结果**：6 case 完整覆盖 F1–F4 + 可观测 + 分类器，映射无误。

---

## scope creep 判断

| 范围项 | 状态 | 说明 |
|---|---|---|
| `CHATBI_V2_INTENT_LLM_RETRIES` | 在范围 | 默认 3，上限 5 |
| `CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S` | 在范围 | 默认 0.15 |
| `CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS` | 在范围 | 默认 `1.0,0.65,0.4` |
| `_llm_decide_v2_with_retries` | 在范围 | 包装单次 `_llm_decide_v2` |
| 可观测（`used=llm_retry` + `attempt` + `timeout_s`） | 在范围 | retry_meta 注入 raw_response |
| 单测 | 在范围 | `tests/test_intent_llm_retry.py` |

**非范围项确认**：
- Intent hints YAML / Prompt 注入（Step1 #109）—— 未改动。
- Step2 router 仲裁（U2）—— 未改动。
- 前端 Timeline 专用 retry UX —— 未改动。
- `api/agent.py` —— 未改动。

**结论**：无 scope creep。

---

## 结论

**建议合并**。

理由：
1. 代码实现与任务单要求一致（重试阶梯、超时递减、failure_paths）。
2. 6 个测试 case 全绿，全集 pytest 323 passed。
3. `harness_task_validate.py` OK。
4. 无 scope creep，无安全红线问题。
5. 22 R1 审查结论已确认代码侧无问题；本 50 复检重点为「元信息 + 测试映射 + env 注释 + 流程完整性」，均通过。

---

## 回报

### Status
- 50 独立复检完成。代码实现完整、测试覆盖到位、安全无虞、流程项齐全。

### Deliverables
- 本报告：`docs/tasks/reinspect_results/reinspect_chatbi_intent_llm_retry_u1_5_20260608_v1.md`

### Blockers
- 无阻塞项。50 落盘后可直接进入 CLOSE（task `git mv` → `done/` + 更新 `_views/done.md` + PR merge）。

### Judgment
- **建议合并**。本 task 为「已合代码的 harness 链式补关账」，非新实现。代码侧与流程侧均无问题，可闭合。
