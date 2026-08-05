# Task：ChatBI Intent LLM 外呼重试（U1.5 · micro-PR）

> **状态**：`done`  
> **Epic**：ChatBI Intent Hints · **U1.5**（独立于 Step1 · 不阻塞 Step2 U2）  
> **双轨 Epic**：[`task_harness_semi_auto_retirement_manifest_v1.md`](task_harness_semi_auto_retirement_manifest_v1.md) · **B 轨 / G2**（api 链式关账 · semi_auto 退场）  
> **前置**：Step1 #109 已合 main  
> **关联代码**：`api/intent_agent.py`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_intent_llm_retry_u1_5_v1` |
| **orchestration** | **Claude Code** · Lead + 串行 spawn `.claude/agents/harness-*` · **Git 仅 Lead** |
| **semi_auto** | `false` — **自 `true` 迁移** · 链式 PROMPT 替代同会话换帽 |
| **test_strategy** | `required` |
| **test_strategy_note** | 涉 `api/intent_agent.py` 重试/超时阶梯；须 `tests/test_intent_llm_retry.py` + 全集 pytest + **50 reinspect** |
| **audit_profile** | `full` |
| **git_branch** | `task/chatbi-intent-llm-retry-u1.5-chain-v1`（链式关账分支 · 实现可 cherry-pick 自 `task/chatbi-intent-llm-retry-u1.5`） |
| **merge_policy** | `docs_only_ci_green_merge` → 含 `api/` 时仍须 CI pytest 全绿 |
| **close_action** | `merge` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `50` |
| **experience_capture** | `required` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | 22-R1, 30 | task + 链式 PROMPT 人扫 · **2026-06-08 用户授权代填** |
| HG-CHAIN-B-EXEC | approved | explore, 22, 30, 40, 50, CLOSE | B 轨 T1 执行链 · **2026-06-08 用户授权代填** |
| HG-REINSPECT | approved | done | 50 落盘后人签 · merge 前 · **2026-06-08 用户授权预批** |

---

## 1. 背景与目标

Intent V2 LLM 外呼在 **瞬态失败**（超时、5xx、限流）时 **最多 3 次**（含首次），耗尽后走现有 **`v1_fallback`**；JSON 非法 / tool 不在白名单 **不重试**。二三轮单次 `wait_for` **递减**（默认 65% / 40%），避免 3× 全量 timeout 拖死 Agent 软超时。

---

## 2. 范围

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | `CHATBI_V2_INTENT_LLM_RETRIES` | 默认 `3`，上限 5 |
| 2 | `CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S` | 指数退避基数，默认 `0.15` |
| 3 | `CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS` | 默认 `1.0,0.65,0.4` |
| 4 | `_llm_decide_v2_with_retries` | 包装单次 `_llm_decide_v2` |
| 5 | 可观测 | `raw_response.used=llm_retry` + `attempt` + `timeout_s` |
| 6 | 单测 | `tests/test_intent_llm_retry.py` |
| 7 | RUNBOOK | §4.1 Q-INTENT（Step1 五问已验 · 不单独 reinspect 落盘） |

---

## 3. 非范围

- Intent hints YAML / Prompt 注入（Step1 #109）  
- Step2 router 仲裁（U2）  
- 前端 Timeline 专用 retry UX  
- `api/agent.py`（Step1 已含 `decide_intent_v1` import）

---

## 行为变更（Delta）

### ADDED

- `api/intent_agent.py`：Intent LLM 外呼重试 + 超时阶梯 + env 读取
- `tests/test_intent_llm_retry.py`
- RUNBOOK §4.1 Q-INTENT · `intent_hints.yaml` few_shot 对齐

### MODIFIED

- `.env.example`：U1.5 retry / timeout factors 注释

---

## 验收标准

- [x] `pytest tests/test_intent_llm_retry.py -q` **全绿**
- [x] `pytest tests -m "not intent_eval and not intent_benchmark" -q` **全绿**
- [x] Step1 五问 5/5 人验已通过（#109 · **不**单独 reinspect 落盘）
- [x] RUNBOOK §4.1 Q-INTENT spot-check（可选 · PR #137 说明）
- [x] `python tools/harness_task_validate.py docs/tasks/done/task_chatbi_intent_llm_retry_u1_5_v1.md` **OK**
- [x] Harness 链式：`docs/harness/invokes/by-task/chatbi-intent-retry-u1.5-chain/` 帽链齐全（explore/22/30/40/50/CLOSE）
- [x] **50** 落盘：`docs/tasks/reinspect_results/reinspect_chatbi_intent_llm_retry_u1_5_20260608_v1.md`

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md` §8）。

---

## Harness 链式关账（B 轨 · Round T1）

**Prompt**：[`PROMPT_claude_chain_serial_v1_T1_intent-retry-u1_5_zh.md`](../harness/prompts/PROMPT_claude_chain_serial_v1_T1_intent-retry-u1_5_zh.md)

**帽链**：explore → 22 → 30 → 40 → **50** → CLOSE（`test_strategy: required` · **不可 skip 50**）

**invoke slug**：`chatbi-intent-retry-u1.5-chain`

**30 硬约束**：先写/绿 `tests/test_intent_llm_retry.py` 再改 `api/intent_agent.py`（TDD）

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试（可选） |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | `fp-u15-retry-exhausted` | 3 次外呼均为可重试失败（超时/5xx/限流） | `asyncio.TimeoutError` → **`v1_fallback`** · reasoning「意图识别超时…」 | 否（已耗尽） | 仍走 V1 路由 · 可能 rag/text2sql | `test_intent_llm_retry_exhausted_falls_back_v1` |
| F2 | `fp-u15-json-no-retry` | LLM 返回非 JSON / tool 不在白名单 | **不重试** → 启发式 `used=heuristic` | 否 | 路由可能偏离 LLM 期望 | `test_intent_llm_json_error_not_retried` |
| F3 | `fp-u15-retry-success` | 前 1～2 次瞬态失败、末次成功 | `used=llm_retry` + `attempt` + 末轮 `timeout_s` | 是（内部） | 正常 Intent reasoning | `test_intent_llm_retry_succeeds_on_third_attempt` |
| F4 | `fp-u15-agent-latency` | 3 轮 timeout 总和 + RAG > `AGENT_MAX_LATENCY_MS` | Agent 软超时改 tool（与 Step1 F6 叠加） | 是 | RUNBOOK 探针 error | 演示 env `AGENT_MAX_LATENCY_MS=60000` |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 自 Step1 拆出 micro-PR |
| 2026-06-04 | 补 §失败路径 / §验收标准 · 修 CI task_validate |
| 2026-06-08 | Harness 30 链式关账：自检 6 passed + env 齐全 |

---

### 自检结论

- **pytest**：`tests/test_intent_llm_retry.py` **6 passed**，无失败。
- **.env.example**：`CHATBI_V2_INTENT_LLM_RETRIES`、`CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S`、`CHATBI_V2_INTENT_RETRY_TIMEOUT_FACTORS` 注释均已存在，无需补写。
- **api/intent_agent.py**：`_llm_decide_v2_with_retries` 段与 test 断言对齐（`used=llm_retry`、`attempt`、`timeout_s`、timeout 递减阶梯、可重试异常分类、JSON 错误不重试）。
- **判定**：30 自检通过，可进入 40。

---

### CLOSE 回溯（T1 B 轨 · 2026-06-08）

| 阶段 | 动作 | 落盘 | Commit |
|------|------|------|--------|
| explore | api 差分扫描 | `explore_intent_retry_u1_5_impl_gap.md` | `f5ff882`, `d2b3be0` |
| 22 R1 | 审查签收 | `task_chatbi_intent_llm_retry_u1_5_v1_audit_R1_20260608.md` | `b12ca03`, `0184c1b` |
| 30 | 验证性执行 | task 自检结论回填 | `eb42f28`, `f5a59fa` |
| 40 | 全集 pytest + task_validate | — | `4cd9b32` |
| 50 | 独立复检 | `reinspect_chatbi_intent_llm_retry_u1_5_20260608_v1.md` | `599902a`, `250ec8a` |
| CLOSE | invoke 落盘 + 索引 hygiene | `invoke_20260608_CLOSE_chatbi-intent-retry-u1.5-chain.md` | （本 PR） |
| CLOSE | task→done/、MANIFEST 更新 | — | `9a74ac5` |
| PR/merge | #137 squash merge | — | `5afccb5` |

- **pytest 全集**：323 passed, 1 skipped, 2 deselected
- **50 reinspect**：已落盘，建议合并
- **MANIFEST**：A+B 双轨均 done，`semi_auto 全面废弃` 条件满足
