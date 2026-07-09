# 50 Reinspect R1 · P1-3 Clarify 路由

| 项 | 内容 |
| --- | --- |
| **task** | `docs/harness/tasks/active/task_ops_chat_session_sink_p0_p1_v1.md` |
| **subproject** | `ai-ink-brain-api-python` |
| **phase** | P1-3 Clarify 路由：FALLBACK 先澄清 · 减少默认 `#545` |
| **reviewer** | 50 独立复检 + 全局验收帽 |
| **timestamp** | 2026-07-09 |
| **30 commit** | `ai-ink-brain-api-python @ 8f90cb5a` |
| **40 commit** | `ai-ink-brain-api-python @ ea31eae8` · `Projects @ 9cd2340` |

## 复核方法

- 独立阅读 task 正文「### 自检结论（执行者）· P1-3」与「### 自检结论（40 复核）· P1-3」小节。
- 独立阅读本轮 P1-3 改动代码：
  - `api/ops/orchestrator/clarify.py`
  - `api/ops/orchestrator/__init__.py`
  - `api/ops/chat_service.py`
  - `tests/ops/test_clarify.py`
  - `tests/ops/test_chat_service.py`
  - `tests/ops_desk/test_react_fallback.py`
- 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 执行 `git diff origin/main...HEAD --stat`（在 `ai-ink-brain-api-python` 内）核对全量变更路径，确认未扩 scope 到 P1-4 LLM Router、P1-1 artifact、P1-2 checkpoint、Session 生产图、Agently lab、前端。
- 与 30 commit `8f90cb5a`、40 commit `ea31eae8` / `Projects@9cd2340`、R2 任务审核书面结论逐条核对。

## 命令输出

```text
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q
............................................s........................... [ 22%]
........................................................................ [ 45%]
........................................................................ [ 67%]
...................................ss......................sssssss...... [ 90%]
................................                                         [100%]
=============================== warnings summary ================================
../../../miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1
  /Users/cyning/miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/howto-capture-warnings.html
=========================== short test summary info ============================
SKIPPED [1] tests/ops/test_events_schema.py:181: 需要真实 Supabase 连接；本地/CI 环境缺失时跳过
SKIPPED [2] tests/ops_desk/test_run_schema_p1.py:102: public 中表已存在，跳过写测试以避免破坏数据
SKIPPED [7] tests/ops_desk/test_schema_p0.py:102: public 中表已存在，跳过写测试以避免破坏数据
310 passed, 10 skipped, 1 warning in 36.18s

ruff check api/ops
All checks passed!
```

- pytest 退出码：`0`。
- ruff 退出码：`0`。
- 10 skipped 中：1 个为 `tests/ops/test_events_schema.py::test_append_event_integration_with_real_store`（显式 skip，需真实 Supabase 连接）；其余 9 个为 `tests/ops_desk/test_run_schema_p1.py` / `tests/ops_desk/test_schema_p0.py` 中环境感知跳过（表已存在），与 P1-3 改动无关。

## 全量变更路径核对

```text
 api/ops/chat_service.py                            |  50 +++-
 api/ops/orchestrator/__init__.py                   |   3 +
 api/ops/orchestrator/clarify.py                    | 134 +++++++++
 ...709_1921_30_ops_chat_session_sink_p0_p1_P1-3.md |  80 ++++++
 ...709_1921_40_ops_chat_session_sink_p0_p1_P1-3.md |  69 +++++
 ...709_1938_40_ops_chat_session_sink_p0_p1_P1-3.md |  59 +++++
 ...709_1938_50_ops_chat_session_sink_p0_p1_P1-3.md |  62 +++++
 tests/ops/test_chat_service.py                     | 308 +++++++++++++++++++++
 tests/ops/test_clarify.py                          | 168 +++++++++++
 tests/ops_desk/test_react_fallback.py              |  11 +
 10 files changed, 941 insertions(+), 3 deletions(-)
```

- 代码变更仅涉及 `api/ops/orchestrator/clarify.py`、`api/ops/orchestrator/__init__.py`、`api/ops/chat_service.py`、测试文件。
- 文档变更为本轮 invoke 快照，属 harness 落盘工件。
- 未涉及 P1-4 LLM Router、P1-1 artifact、P1-2 checkpoint、`harness_runtime` 生产图、Agently lab、前端代码。

## 与 30 / 40 结论差异核对

| 30 / 40 声称项 | 50 独立复核 | 结果 |
| --- | --- | --- |
| 新增 `api/ops/orchestrator/clarify.py`：`clarify_if_fallback(query, session_id, transcript, slots)` | 文件存在；函数实现含 LLM 1 轮澄清、规则兜底、LLM 失败降级（`clarify.py:106-134`） | 一致 |
| `ClarifyResult` 含 `needs_clarification` / `clarify_question` / `intent` / `slots` | `clarify.py:24-36` dataclass 定义四字段 | 一致 |
| `api/ops/orchestrator/__init__.py` 导出 `ClarifyResult` / `clarify_if_fallback` | `__init__.py:5` 导入并 `__all__` 列出 | 一致 |
| `chat_service.py` FALLBACK 路由先 clarify 再路由 | `chat_service.py:129-178` 在 FALLBACK 分支调用 `load_chat_transcript` + `clarify_if_fallback`；需要澄清时返回 clarify 响应并记录 `clarify.asked`；否则按 fast/deep/react 路由 | 一致 |
| 减少默认 `#545` | FALLBACK 测例不再默认 issue #545；clarify 需要澄清时响应不含 issue_number；解析为具体 intent 时按补齐 slots 路由 | 一致 |
| 利用 P0-3 transcript 能力 | `chat_service.py:130` 调用 `load_chat_transcript`；`clarify.py:45-62` 与 `clarify.py:123` 将 transcript 拼入 LLM prompt | 一致 |
| clarify LLM 调用失败降级为 ReAct fallback | `clarify.py:132-134` 捕获异常返回 `_rule_fallback`；无多 issue 时返回 `intent=FALLBACK`；`test_clarify_degrades_to_react_on_llm_failure` 通过 | 一致 |
| 原有失败路径未被破坏 | artifact / checkpoint 相关测例全绿；`react_loop.py` 与 `store/artifacts.py` 未改动 | 一致 |
| 新增单测覆盖 | `tests/ops/test_clarify.py` 6 测例全绿；`tests/ops/test_chat_service.py` 5 测例全绿；`tests/ops_desk/test_react_fallback.py` 旁路 clarify 后 ReAct 行为覆盖仍通过 | 一致 |
| 最终验证命令绿 | 本轮独立跑通 `310 passed, 10 skipped` + `ruff check api/ops` 全绿 | 一致 |
| 未扩 scope | 全量 diff 仅 P1-3 clarify 相关文件 + invoke；未涉及 P1-4、P1-1、P1-2、Session 生产图、Agently lab、前端 | 一致 |

**差异项**：无。

## 验收项复核表

| 验收项 | 状态 | 证据 | 备注 |
| --- | --- | --- | --- |
| `api/ops/orchestrator/clarify.py` 存在且实现 `clarify_if_fallback(query, session_id, transcript, slots)` | pass | 文件新增；LLM 1 轮澄清 + 规则兜底 + LLM 失败降级 | — |
| `ClarifyResult` 含 `needs_clarification` / `clarify_question` / `intent` / `slots` | pass | `clarify.py:24-36` | — |
| `api/ops/orchestrator/__init__.py` 导出 `ClarifyResult` / `clarify_if_fallback` | pass | `__init__.py:5` 与 `__all__` | — |
| `chat_service.py` FALLBACK 分支先 clarify 再按结果路由 | pass | `chat_service.py:129-178`；需要澄清时返回 `route=clarify` 并记录 `clarify.asked`；否则按 fast/deep/react 路由 | — |
| 减少默认 `#545` | pass | clarify 需要澄清时响应不含 issue_number；解析为具体 intent 时按补齐 slots 路由 | — |
| 复用 P0-3 transcript | pass | `chat_service.py:130` 调用 `load_chat_transcript`；`clarify.py` prompt 含 transcript | — |
| LLM 失败降级为 ReAct fallback | pass | `clarify.py:132-134`；`test_clarify_degrades_to_react_on_llm_failure` 通过 | — |
| 原有 artifact/checkpoint 失败路径未被破坏 | pass | 对应测例全绿；P1-1/P1-2 实现文件未改动 | — |
| `tests/ops/test_clarify.py` / `tests/ops/test_chat_service.py` 覆盖目标场景 | pass | 6 + 5 测例全绿 | — |
| `tests/ops_desk/test_react_fallback.py` 适配 clarify 旁路后仍覆盖 ReAct 行为 | pass | pytest 输出包含该文件且通过 | — |
| 最终验证命令绿 | pass | pytest `310 passed, 10 skipped` + ruff `All checks passed!`；退出码均为 `0` | — |
| 未静默扩大 scope | pass | 全量 diff 路径清单见上文 | 未改 P1-4、P1-1、P1-2、Session 生产图、Agently lab、前端 |

## 阻塞项清单

无。

## 合并建议

**建议合并**。P1-3 Clarify 路由实现、测试、30 执行、40 自检、50 独立复检均通过，无 scope creep，人工闸 `HG-TASK-DRAFT` / `HG-AUDIT-R1` 已 approved。

## 执行路线与 Commit 回溯

| 阶段 | 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|------|----------|----------|-------------|
| P1-3 | 30 execute | Clarify 模块 + chat_service FALLBACK 路由改造 + 测试 | `api/ops/orchestrator/clarify.py`, `api/ops/orchestrator/__init__.py`, `api/ops/chat_service.py`, `tests/ops/test_clarify.py`, `tests/ops/test_chat_service.py`, `tests/ops_desk/test_react_fallback.py` | `ai-ink-brain-api-python@8f90cb5a` |
| P1-3 | 40 self-check | 复核 P1-3 验收 | task 内 P1-3 30/40 自检结论 | `ai-ink-brain-api-python@ea31eae8` · `Projects@9cd2340` |
| P1-3 | 50 reinspect R1 | 独立复检 + 全局验收 | `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260709_50_P1-3.md` | 待本审查落盘后 commit |

## Judgment（50）

- **experience_capture**: `required` — P1-3 clarify 路由模式（FALLBACK 先澄清、LLM 失败降级、transcript 复用）可复用到 P1-4 LLM Router 及后续多轮上下文场景。
- **gate/risk**: 无 — `HG-TASK-DRAFT` / `HG-AUDIT-R1` 均为 `approved`；50 未遇 pending 人工闸。
- **hat_self**: `pass` — 独立复检与 30/40 结论一致，验证命令绿，输出 pass/fail 表、阻塞项清单、合并建议与执行路线回溯。
