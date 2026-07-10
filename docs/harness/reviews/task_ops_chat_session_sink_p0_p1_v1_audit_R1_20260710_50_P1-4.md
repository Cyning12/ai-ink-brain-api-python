# 50 独立复检 + 全局验收报告 · Ops Chat Session Sink P0+P1 · P1-4 LLM Router

| 项 | 内容 |
| --- | --- |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **scope** | P1-4 LLM Router：`OPS_CHAT_LLM_ROUTER` · JSON intent · 规则 fallback |
| **hat** | 50-independent-reinspect |
| **date** | 2026-07-10 |
| **30 commit** | `ai-ink-brain-api-python@760179a5` |
| **40 commit** | `ai-ink-brain-api-python@5c4f05c6` · `Projects@9fef12f` |

---

## 复核方法

1. 独立阅读 task 正文「### 自检结论（执行者）· P1-4」与「### 自检结论（40 复核）· P1-4」小节。
2. 独立阅读本轮 P1-4 改动代码：
   - `api/ops/intent_router.py`
   - `api/ops/orchestrator/core.py`（`classify_intent` / `_rule_classify_intent`）
   - `tests/ops/test_intent_router.py`
3. 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令：
   ```bash
   pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
   ```
4. 单独执行失败路径验证命令：
   ```bash
   pytest tests/ops/test_intent_router.py -k fallback -q
   ```
5. 执行 `git diff origin/main...HEAD --stat` 核对全量变更路径，确认未扩 scope 到 P1-1 artifact、P1-2 checkpoint、P1-3 clarify、`harness_runtime` 生产图、Agently lab、前端代码。
6. 与 30 commit `760179a5`、40 commit `5c4f05c6` / `Projects@9fef12f`、R2 任务审核书面结论逐条核对。

---

## 命令输出

### 完整验证命令

```text
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q
............................................s........................... [ 22%]
........................................................................ [ 44%]
........................................................................ [ 66%]
.........................................ss......................sssssss [ 88%]
......................................                                   [100%]
=============================== warnings summary ================================
../../../miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1
  /Users/cyning/miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/howto/capture-warnings.html
=========================== short test summary info ============================
SKIPPED [1] tests/ops/test_events_schema.py:181: 需要真实 Supabase 连接；本地/CI 环境缺失时跳过
SKIPPED [2] tests/ops_desk/test_run_schema_p1.py:102: public 中表已存在，跳过写测试以避免破坏数据
SKIPPED [7] tests/ops_desk/test_schema_p0.py:102: public 中表已存在，跳过写测试以避免破坏数据
316 passed, 10 skipped, 1 warning in 57.58s

ruff check api/ops
All checks passed!
```

- pytest 退出码：`0`
- ruff 退出码：`0`
- 10 skipped 中：1 个为 `tests/ops/test_events_schema.py::test_append_event_integration_with_real_store`（显式 skip，需真实 Supabase 连接）；其余 9 个为 `tests/ops_desk/test_run_schema_p1.py` / `tests/ops_desk/test_schema_p0.py` 中环境感知跳过（表已存在），与 P1-4 改动无关。

### 失败路径额外验证

```text
pytest tests/ops/test_intent_router.py -k fallback -q
...                                                                      [100%]
3 passed, 3 deselected in 0.38s
```

- pytest 退出码：`0`
- 覆盖：低置信度 fallback、非法 JSON fallback、LLM 超时 fallback；均记录 `intent_router.fallback` event。

---

## 全量变更路径核对

```text
 api/ops/intent_router.py                           | 174 ++++++++++++++++
 api/ops/orchestrator/core.py                       |  21 +-
 docs/_tech_graph/02_version.md                     |   1 +
 ...710_0929_30_ops_chat_session_sink_p0_p1_P1-4.md |  79 +++++++
 ...710_0930_40_ops_chat_session_sink_p0_p1_P1-4.md |  75 +++++++
 ...710_0947_40_ops_chat_session_sink_p0_p1_P1-4.md |  67 ++++++
 ...710_0947_50_ops_chat_session_sink_p0_p1_P1-4.md |  69 ++++++
 tests/ops/test_intent_router.py                    | 231 +++++++++++++++++++++
 8 files changed, 716 insertions(+), 1 deletion(-)
```

- 代码变更仅涉及 `api/ops/intent_router.py`、`api/ops/orchestrator/core.py`、`tests/ops/test_intent_router.py`。
- `docs/_tech_graph/02_version.md` 追加版本时间点，属技术图谱例行更新，未改生产代码。
- 文档变更为本轮 invoke 快照、task 自检结论与本 50 复检报告，属 harness 落盘工件。
- 未涉及 P1-1 artifact、P1-2 checkpoint、P1-3 clarify、`harness_runtime` 生产图、Agently lab、前端代码。

---

## 与 30 / 40 结论差异核对

| 30 / 40 声称项 | 50 独立复核 | 结果 |
| --- | --- | --- |
| 新增 `api/ops/intent_router.py` 轻量 JSON LLM router | 文件存在；`_build_prompt` / `llm_classify_intent` / `classify_intent_with_llm` 实现完整；输出含 `intent` / `slots` / `confidence` | 一致 |
| `OPS_CHAT_LLM_ROUTER=1` 时 `classify_intent` 优先调用 LLM router | `core.py:118-133` 委托 `_intent_router.classify_intent_with_llm`；集成测 `test_classify_intent_uses_llm_router` 通过 | 一致 |
| 低置信度降级规则 fallback | `intent_router.py:169-172` 在 `confidence < _MIN_CONFIDENCE` 时调用 fallback；`test_llm_router_low_confidence_fallback` 通过 | 一致 |
| 非法 JSON / LLM 异常降级规则 fallback | `_extract_json_obj` 抛异常与 `chat_completion` 异常均在 `classify_intent_with_llm` 捕获并 fallback；对应测例通过 | 一致 |
| 默认未开启时行为与之前一致 | `_is_enabled()` 仅在 `OPS_CHAT_LLM_ROUTER=1` 时启用；`test_llm_router_disabled_uses_rule` 通过 | 一致 |
| 记录 `intent_router.fallback` event | `_record_fallback_event` 复用 P0-2 `append_event`；fallback 测例断言 store 中存在 `event_type=intent_router.fallback` | 一致 |
| `router.latency` 日志 | `llm_classify_intent` 在成功/失败路径均记录 `router.latency` | 一致 |
| 最终验证命令绿 | 本轮独立跑通 `316 passed, 10 skipped` + ruff 全绿 | 一致 |
| 未扩 scope | 全量 diff 仅 P1-4 router 相关文件 + docs 版本时间点 + invoke；未涉及 P1-1/2/3、Session 生产图、Agently lab、前端 | 一致 |
| P0 ~ P1-3 已有实现未被破坏 | `review/rules.py`、`events_schema.py`、`store/runs.py`、`chat_context.py`、`chat_service.py`、`orchestrator/clarify.py` 未改动；相关测例全绿 | 一致 |

**差异项**：无。

---

## 验收项复核表

| 验收项 | 状态 | 证据 | 备注 |
| --- | --- | --- | --- |
| `api/ops/intent_router.py` 存在且实现 LLM JSON intent router | pass | 文件新增；`_build_prompt` / `llm_classify_intent` / `classify_intent_with_llm` 完整；返回含 `intent` / `slots` / `confidence` | — |
| `OPS_CHAT_LLM_ROUTER=1` 时 `classify_intent` 优先调用 LLM router | pass | `core.py:118-133`；集成测 `test_classify_intent_uses_llm_router` 通过 | — |
| 低置信度降级规则 fallback | pass | `intent_router.py:169-172`；`test_llm_router_low_confidence_fallback` 通过 | — |
| 非法 JSON / LLM 异常降级规则 fallback | pass | `classify_intent_with_llm` 异常捕获分支；`test_llm_router_invalid_json_fallback` / `test_llm_router_timeout_fallback` 通过 | — |
| 默认未开启时行为与之前一致 | pass | `_is_enabled()` 仅在 `OPS_CHAT_LLM_ROUTER=1` 时启用；`test_llm_router_disabled_uses_rule` 通过 | — |
| 记录 `intent_router.fallback` event | pass | `_record_fallback_event` 复用 P0-2 `append_event`；fallback 测例断言 event 存在 | — |
| `router.latency` 日志 | pass | `llm_classify_intent` 成功/失败路径均记录 `router.latency` | — |
| `tests/ops/test_intent_router.py` 覆盖目标场景 | pass | 6 测例全绿：启用返回合法 intent、低置信度 fallback、非法 JSON fallback、超时 fallback、默认规则、集成路径 | — |
| task §失败路径验证命令绿 | pass | `pytest tests/ops/test_intent_router.py -k fallback -q` → `3 passed, 3 deselected` | — |
| 最终验证命令绿 | pass | pytest `316 passed, 10 skipped` + ruff `All checks passed!`；退出码均为 `0` | — |
| 未静默扩大 scope | pass | 全量 diff 路径清单见上文 | 未改 P1-1/2/3、Session 生产图、Agently lab、前端 |
| P0 ~ P1-3 已有实现未被破坏 | pass | `review/rules.py`、`events_schema.py`、`store/runs.py`、`chat_context.py`、`chat_service.py`、`orchestrator/clarify.py` 未改动；相关测例全绿 | — |

---

## 阻塞项清单

无。

---

## 是否建议合并

**建议合并**。P1-4 LLM Router 实现、测试、30 执行、40 自检、50 独立复检均通过，无 scope creep，人工闸 `HG-TASK-DRAFT` / `HG-AUDIT-R1` 已 approved。

---

## 执行路线与 Commit 回溯

| 阶段 | 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|------|----------|----------|-------------|
| P1-4 | 30 execute | LLM intent router + `classify_intent` 混合分类器 + 测试 | `api/ops/intent_router.py`, `api/ops/orchestrator/core.py`, `tests/ops/test_intent_router.py` | `ai-ink-brain-api-python@760179a5` |
| P1-4 | 40 self-check | 复核 P1-4 验收 | task 内 P1-4 30/40 自检结论 | `ai-ink-brain-api-python@5c4f05c6` · `Projects@9fef12f` |
| P1-4 | 50 reinspect R1 | 独立复检 + 全局验收 | `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260710_50_P1-4.md` | 待本审查落盘后 commit |

---

## Judgment（50）

- **experience_capture**: `required` — LLM router JSON intent、confidence 阈值、规则 fallback、事件记录模式可复用到后续 ChatBI / Session 路由。
- **gate/risk**: 无 — `HG-TASK-DRAFT` / `HG-AUDIT-R1` 均为 `approved`；50 未遇 pending 人工闸。
- **hat_self**: `pass` — 独立复检与 30/40 结论一致，验证命令绿，失败路径额外验证绿，输出 pass/fail 表、阻塞项清单、合并建议与执行路线回溯。
