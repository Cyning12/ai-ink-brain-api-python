---
task_slug: chatbi_intent_llm_retry_u1_5_v1
round: T1
hat: 22
freeze_id: GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08
git_branch: task/chatbi-intent-llm-retry-u1.5-chain-v1
audit_profile: full
date: 2026-06-08
---

# 22 R1 · Harness 审查报告

## 审查摘要

本 task 为 **B 轨补关账**（代码已合 main，PR #110 / commit 9a01ebd）。当前分支 `task/chatbi-intent-llm-retry-u1.5-chain-v1` 基于 `main@bb0258c`，`api/`、`tests/`、`.env.example` 与 main 无差分。审查结论：**代码实现完整、测试覆盖到位、安全无虞，流程项待 50 reinspect 后闭合。**

---

## 逐项核对

### 1. 元信息（task 文件）

| 字段 | 任务单值 | 审查结论 |
|---|---|---|
| `semi_auto` | `false`（自 `true` 迁移） | 已确认迁移；链式 PROMPT 替代同会话换帽 |
| `test_strategy` | `required` | 已确认；50 不可 skip |
| `audit_profile` | `full` | 已确认 |
| `git_branch` | `task/chatbi-intent-llm-retry-u1.5-chain-v1` | 当前分支匹配 |
| `merge_policy` | `docs_only_ci_green_merge` → 含 api/ 时仍须 pytest 全绿 | 已确认 |
| `close_action` | `merge` | 已确认 |
| `kpi_rubric` | `KPI_RUBRIC_v1_2` | 已确认 |
| `kpi_aggregator` | `50` | 已确认 |

### 2. human_gate 状态

| human_gate_id | status | blocks_hats | 审查结论 |
|---|---|---|---|
| HG-TASK-DRAFT | approved | 22-R1, 30 | 用户授权代填，日期 2026-06-08 |
| HG-CHAIN-B-EXEC | approved | explore, 22, 30, 40, 50, CLOSE | 用户授权代填，日期 2026-06-08 |
| HG-REINSPECT | approved | done | 用户预批，日期 2026-06-08 |

**注意**：HG-REINSPECT 为预批，50 落盘时须 reinspect 人签确认后方可 merge。

### 3. 验收标准

| 验收项 | 状态 | 审查结论 |
|---|---|---|
| `pytest tests/test_intent_llm_retry.py -q` 全绿 | 已勾选 | **6 passed**（实测 2026-06-08） |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` 全绿 | 已勾选 | **323 passed, 1 skipped, 2 deselected**（实测 2026-06-08） |
| Step1 五问 5/5 人验已通过 | 已勾选 | #109 已合，不单独 reinspect |
| RUNBOOK §4.1 Q-INTENT spot-check | 未勾选 | 可选；建议 40 帽或 50 时补 |
| `harness_task_validate.py` OK | 未勾选 | **实测 OK**（2026-06-08） |
| Harness 链式 invoke 齐全 | 未勾选 | explore + 22 已落盘；30/40/50 待续 |
| 50 reinspect 落盘 | 未勾选 | **必须**（test_strategy: required） |

### 4. failure_paths F1–F4 与测试映射

| Scenario ID | 触发条件 | 测试函数 | 代码路径 | 审查结论 |
|---|---|---|---|---|
| F1 `fp-u15-retry-exhausted` | 3 次可重试失败 | `test_intent_llm_retry_exhausted_falls_back_v1` | `_llm_decide_v2_with_retries` 耗尽 → raise `TimeoutError` → `decide_intent_v2` catch → `v1_fallback` | **覆盖** |
| F2 `fp-u15-json-no-retry` | 非 JSON / tool 不在白名单 | `test_intent_llm_json_error_not_retried` | `ValueError` 非 `_intent_llm_retryable` → 不重试 → 外层 catch → `used=heuristic` | **覆盖** |
| F3 `fp-u15-retry-success` | 前 1~2 次瞬态失败、末次成功 | `test_intent_llm_retry_succeeds_on_third_attempt` | 第 3 轮成功 → `used=llm_retry` + `attempt=3` | **覆盖** |
| F4 `fp-u15-agent-latency` | 3 轮 timeout 总和 + RAG > 软超时 | `test_intent_llm_retry_timeout_decreases_per_attempt` | timeout 阶梯 60→39→24（系数 1.0/0.65/0.4） | **覆盖** |

**补充测试**：`test_intent_llm_retry_logs_without_debug_intent_cache`（可观测日志）、`test_intent_llm_retryable_classifier`（重试分类器）。6 case 完整覆盖 F1–F4 + 可观测 + 分类器。

### 5. api 范围 bounded（无 scope creep）

| 范围项 | 状态 | 审查结论 |
|---|---|---|
| `CHATBI_V2_INTENT_LLM_RETRIES` | 在范围 | `_intent_llm_max_retries()` 默认 3，上限 5 |
| `CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S` | 在范围 | `_intent_llm_retry_backoff_s()` 默认 0.15 |
| `CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS` | 在范围 | `_intent_llm_retry_timeout_factors()` 默认 `1.0,0.65,0.4` |
| `_llm_decide_v2_with_retries` | 在范围 | L513–561，包装单次 `_llm_decide_v2` |
| 可观测（used=llm_retry + attempt + timeout_s） | 在范围 | retry_meta 注入 raw_response |
| 单测 | 在范围 | `tests/test_intent_llm_retry.py` |

**非范围项确认**：Intent hints YAML / Prompt 注入（Step1 #109）、Step2 router 仲裁（U2）、前端 Timeline retry UX、`api/agent.py` 均 **未** 在本 task 中改动。

### 6. 代码安全

| 检查项 | 结论 | 说明 |
|---|---|---|
| 密钥硬编码 | **无** | API key 均读 env；`_llm_decide_v2_with_retries` 不直接持有 key |
| 注入风险 | **无** | query/history 仅用于 prompt 拼接，无 SQL/命令拼接；`_extract_json_obj` 仅做 JSON 提取 |
| 日志泄露 | **无** | `_log_intent_retry_*` 仅打 attempt/timeout/backoff/err_label，**不打 query 明文**；cache log 仅打 key_hash |
| 超时边界 | **安全** | `_intent_llm_timeout_s_for_attempt` clamp 到 [0.5, 120.0]；`_intent_llm_max_retries` clamp 到 [1, 5] |
| 退避边界 | **安全** | `_intent_llm_retry_backoff_s` base clamp 到 [0.0, 5.0]；指数退避上限可控 |

### 7. .env.example 注释

| env 键 | 注释存在 | 说明 |
|---|---|---|
| `CHATBI_V2_INTENT_LLM_RETRIES` | 是 | L131–132，含「最大尝试次数（含首次）」说明 |
| `CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S` | 是 | L133，含「指数退避基数」说明 |
| `CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS` | 是 | L134–135，含「各轮 wait_for 相对首轮系数」及默认值说明 |

---

## 签收或阻塞项

### 签收项（本帽可确认）

1. **semi_auto → false 迁移确认**：task 元信息已正确标记 `semi_auto: false`。
2. **failure_paths F1–F4 与测试一一对应**：6 个 test case 完整覆盖。
3. **api 范围 bounded**：无 scope creep，非范围项未改动。
4. **代码安全**：无密钥硬编码、无注入风险、日志不泄露 query。
5. **env 注释齐全**：.env.example 已含 U1.5 三项 env 及说明。
6. **pytest 全绿**：单测 6/6 + 全集 323 passed。
7. **`harness_task_validate.py` OK**：实测通过。

### 阻塞项（须后续帽解决）

1. **50 reinspect 落盘**：`test_strategy: required` + `kpi_aggregator: 50`，**不可 skip**。当前 `docs/tasks/reinspect_results/` 下 **无** `reinspect_chatbi_intent_llm_retry_u1_5_*` 文件。
2. **Harness 链式 invoke 待续**：30/40/50/CLOSE 帽 invoke 尚未落盘。

---

## 下一棒建议

| 帽 | 建议动作 |
|---|---|
| **30** | 全集 pytest 已绿（本审查实测），30 帽可直接确认「无需代码改动」，invoke 落盘后转 40。 |
| **40** | 可选：RUNBOOK §4.1 Q-INTENT spot-check（task 标为可选）；或确认「无需补充」后直接 invoke 落盘转 50。 |
| **50** | **必做**：reinspect 落盘 `docs/tasks/reinspect_results/reinspect_chatbi_intent_llm_retry_u1_5_*`。因代码已合 main 且测试全绿，reinspect 重点为「元信息 + 测试映射 + env 注释 + 流程完整性」人签。 |
| **CLOSE** | 50 人签后，task 文件 `git mv` → `done/` + 更新 `_views/done.md` + PR merge（当前分支仅含 harness 文档，CI 绿即可合）。 |

---

## 回报

### Status
- 22 R1 审查完成。代码实现完整、测试覆盖到位、安全无虞。

### Deliverables
- 本报告：`docs/harness/reviews/by-task/chatbi-intent-retry-u1.5-chain/task_chatbi_intent_llm_retry_u1_5_v1_audit_R1_20250608.md`

### Blockers
- 50 reinspect 落盘为唯一阻塞项（test_strategy: required，不可 skip）。

### Judgment
- **本 task 为“已合代码的 harness 链式补关账”**，非新实现。22 帽结论：代码侧无问题，流程侧待 50 落盘后闭合。
