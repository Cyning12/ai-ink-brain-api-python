# 50 独立复检 + 全局验收报告 · P1-1 Artifacts → Supabase

| 项 | 内容 |
| --- | --- |
| **task** | `ops-chat-session-sink-p0-p1` |
| **subtask** | P1-1 Artifacts → Supabase |
| **reviewer** | 50-reinspect |
| **date** | 2026-07-09 |
| **30_commit** | `api-python@13eb0524` |
| **40_commit** | `Projects@59e4aae` · `api-python@197ce5b7` |
| **scope** | `supabase/sql/ops_desk_p1_artifacts.sql` · `supabase/sql/ops_desk_p1_artifacts_rollback.sql` · `api/ops/store/artifacts.py` · `api/ops/store/runs.py` · `api/ops/orchestrator/core.py` · `api/ops/react_loop.py` · `tests/ops/test_artifacts.py` |

---

## 复核方法

- 独立阅读 task 正文「### 自检结论（执行者）· P1-1」与「### 自检结论（40 复核）· P1-1」小节。
- 独立阅读本轮 P1-1 改动代码：
  - `supabase/sql/ops_desk_p1_artifacts.sql`
  - `supabase/sql/ops_desk_p1_artifacts_rollback.sql`
  - `api/ops/store/artifacts.py`
  - `api/ops/store/runs.py`
  - `api/ops/orchestrator/core.py`
  - `api/ops/react_loop.py`
  - `tests/ops/test_artifacts.py`
- 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令：
  ```bash
  pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
  ```
- 额外执行 task §失败路径所列的 `pytest tests/ops/test_artifacts.py -k write_failed -q`。
- 执行 `git diff origin/main...HEAD --stat`（在 `ai-ink-brain-api-python` 内）核对全量变更路径，确认未扩 scope 到 P1-2/3/4、Session 生产图、Agently lab、前端。
- 与 30 commit `api-python@13eb0524`、40 commit `Projects@59e4aae` / `api-python@197ce5b7`、R2 任务审核书面结论逐条核对。

---

## 命令输出

### 最终验证命令

```text
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q
..........................s............................................. [ 23%]
........................................................................ [ 47%]
........................................................................ [ 71%]
.................ss......................sssssss........................ [ 95%]
..............                                                           [100%]
=============================== warnings summary ===============================
../../../miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1
  /Users/cyning/miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
SKIPPED [1] tests/ops/test_events_schema.py:181: 需要真实 Supabase 连接；本地/CI 环境缺失时跳过
SKIPPED [2] tests/ops_desk/test_run_schema_p1.py:102: public 中表已存在，跳过写测试以避免破坏数据
SKIPPED [7] tests/ops_desk/test_schema_p0.py:102: public 中表已存在，跳过写测试以避免破坏数据
292 passed, 10 skipped, 1 warning in 70.97s (0:01:10)

ruff check api/ops
All checks passed!
```

- pytest 退出码：`0`。
- ruff 退出码：`0`。
- 10 skipped 中：1 个为 `tests/ops/test_events_schema.py::test_append_event_integration_with_real_store`（显式 skip，需真实 Supabase 连接）；其余 9 个为 `tests/ops_desk/test_run_schema_p1.py` / `tests/ops_desk/test_schema_p0.py` 中环境感知跳过（表已存在），与 P1-1 改动无关。

### 失败路径额外验证

```text
pytest tests/ops/test_artifacts.py -k write_failed -q
...                                                                      [100%]
3 passed, 7 deselected in 0.61s
```

- pytest 退出码：`0`。

---

## 全量变更路径核对

```text
git diff origin/main...HEAD --stat
 api/ops/orchestrator/core.py                       |  14 +
 api/ops/react_loop.py                              |  13 +
 api/ops/store/artifacts.py                         |  70 ++++
 api/ops/store/runs.py                              |  32 +
 ...709_1622_30_ops_chat_session_sink_p0_p1_P1-1.md |  79 +++++
 ...709_1622_40_ops_chat_session_sink_p0_p1_P1-1.md |  53 +++
 ...709_1650_50_ops_chat_session_sink_p0_p1_P1-1.md |  59 ++++
 supabase/sql/ops_desk_p1_artifacts.sql             |  14 +
 supabase/sql/ops_desk_p1_artifacts_rollback.sql    |   2 +
 tests/ops/test_artifacts.py                        | 382 +++++++++++++++++++++
 10 files changed, 718 insertions(+)
```

- 变更仅涉及 P1-1 Artifacts 相关实现、测试、SQL migration/rollback 与 invoke 文档。
- 未涉及 P1-2 checkpoint、P1-3 clarify、P1-4 LLM router、Session 生产图、Agently lab、前端。

---

## 与 30 / 40 结论差异核对

| 30 / 40 声称项 | 50 独立复核 | 结果 |
| --- | --- | --- |
| 新建 Supabase 表 `ops_run_artifacts` 含 `run_id`/`kind`/`payload`/`created_at`、FK `ops_runs`、唯一键 `(run_id, kind)`、可回滚 | `supabase/sql/ops_desk_p1_artifacts.sql:4-14` 创建表；`run_id uuid` FK `ops_runs(id)`；`UNIQUE (run_id, kind)`；`ops_desk_p1_artifacts_rollback.sql:2` 含 `DROP TABLE IF EXISTS` | 一致 |
| 新增 `api/ops/store/artifacts.py`：`save_artifact` 幂等 upsert / 重试 / `ArtifactStoreError` | `artifacts.py:8` 定义 `ArtifactStoreError`；`artifacts.py:12-40` 实现 `save_artifact`；默认 `max_retries=3`，重试 `max_retries + 1` 次后抛异常 | 一致 |
| `save_artifact_with_failure_event` 失败时记录 `artifact.write_failed` event | `artifacts.py:43-70` 捕获 `ArtifactStoreError` 后调用 `append_event(kind="artifact.write_failed")` 并返回 `None` | 一致 |
| `OpsRunStore.save_artifact` / `list_artifacts` | `store/runs.py:219-236` 实现 `save_artifact`（upsert on_conflict `run_id,kind`）；`store/runs.py:238-249` 实现 `list_artifacts` | 一致 |
| deep 路径写入 artifact | `orchestrator/core.py:362-373` 调用 `save_artifact_with_failure_event(kind="deep.final_answer", ...)` | 一致 |
| ReAct 路径写入 artifact | `react_loop.py:319-329` 调用 `save_artifact_with_failure_event(kind="react.final_answer", ...)` | 一致 |
| artifact 写失败仍返回答案 | `save_artifact_with_failure_event` 吞异常返回 `None`；deep/ReAct 继续执行到返回 `answer` | 一致 |
| `tests/ops/test_artifacts.py` 10 测例覆盖 | 文件存在；pytest 输出 `292 passed` 包含该文件；覆盖 save/list/schema/幂等/失败 event/deep/ReAct/migration | 一致 |
| 失败路径验证命令 `pytest tests/ops/test_artifacts.py -k write_failed -q` | 本轮独立跑通 `3 passed` | 一致 |
| 最终验证命令绿 | 本轮独立跑通 `292 passed, 10 skipped` + ruff 全绿 | 一致 |
| 未扩 scope | 全量 diff 仅 P1-1 artifact 相关文件 + invoke；未涉及 P1-2/3/4、Session 生产图、Agently lab、前端 | 一致 |

**差异项**：无。

---

## 验收项复核表

| 验收项 | 状态 | 证据 | 备注 |
| --- | --- | --- | --- |
| 新建 Supabase 表 `ops_run_artifacts` 与 `ops_run_events` 风格一致 | pass | `supabase/sql/ops_desk_p1_artifacts.sql:4-14`；含 `run_id` uuid FK、`kind` text、`payload` jsonb、`created_at` timestamptz、`UNIQUE (run_id, kind)`、索引 | — |
| migration 可回滚 | pass | `supabase/sql/ops_desk_p1_artifacts_rollback.sql:2` 含 `DROP TABLE IF EXISTS public.ops_run_artifacts` | — |
| `api/ops/store/artifacts.py` 实现 `save_artifact(run_id, kind, payload)` | pass | `artifacts.py:12-40`；未提供 store 时用全局 `supabase_client()` 构造 `OpsRunStore`；重试 `max_retries + 1` 次后抛 `ArtifactStoreError` | — |
| `save_artifact` 幂等写入 | pass | `store/runs.py:225-228` 使用 `upsert(row, on_conflict="run_id,kind")`；`test_save_artifact_idempotent_upsert` 通过 | — |
| `save_artifact_with_failure_event` 失败时记录 `artifact.write_failed` event | pass | `artifacts.py:57-69` 捕获异常后调用 `append_event`；`test_save_artifact_failure_records_write_failed_event` 与 deep/ReAct 失败测例通过 | — |
| `OpsRunStore.save_artifact` / `list_artifacts` | pass | `store/runs.py:219-249` | — |
| deep 路径在最终答案后调用 `save_artifact_with_failure_event` | pass | `orchestrator/core.py:362-373`；`test_run_deep_saves_final_answer_artifact` 通过 | — |
| ReAct 路径在最终答案后调用 `save_artifact_with_failure_event` | pass | `react_loop.py:319-329`；`test_run_react_saves_final_answer_artifact` 通过 | — |
| artifact 写失败仍返回答案 | pass | `save_artifact_with_failure_event` 吞异常；`test_run_deep_artifact_failure_records_write_failed_event` / `test_run_react_artifact_failure_records_write_failed_event` 断言 `result["answer"]` 存在 | — |
| `tests/ops/test_artifacts.py` 覆盖 schema/幂等/失败 event/deep/ReAct/migration | pass | 10 测例全绿 | — |
| task §失败路径验证命令绿 | pass | `pytest tests/ops/test_artifacts.py -k write_failed -q` → `3 passed` | — |
| 最终验证命令绿 | pass | pytest `292 passed, 10 skipped` + ruff `All checks passed!`；退出码均为 `0` | — |
| 未静默扩大 scope | pass | 全量 diff 仅 P1-1 相关文件 + invoke；未涉及 P1-2/3/4、Session 生产图、Agently lab、前端 | — |
| P0-1 ~ P0-4 已有实现未被破坏 | pass | `api/ops/review/rules.py`、`api/ops/events_schema.py` 未改动；deep/ReAct 仍从共享模块导入 `review_result` 并继续通过 `append_event` 写入 handoff/review 事件 | — |

---

## 阻塞项清单

无。

---

## 是否建议合并

**建议合并**。P1-1 Artifacts → Supabase 实现、测试、30 执行、40 自检、50 独立复检均通过，无 scope creep，人工闸 `HG-TASK-DRAFT` / `HG-AUDIT-R1` 已 approved。

---

## 执行路线与 Commit 回溯

| 阶段 | 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|------|----------|----------|-------------|
| P1-1 | 30 execute | `ops_run_artifacts` 表 + `save_artifact` + deep/ReAct 写入 + 测试 | `supabase/sql/ops_desk_p1_artifacts.sql`, `api/ops/store/artifacts.py`, `api/ops/store/runs.py`, `api/ops/orchestrator/core.py`, `api/ops/react_loop.py`, `tests/ops/test_artifacts.py` | api-python@13eb0524 |
| P1-1 | 40 self-check | 复核 P1-1 验收 | task 内 P1-1 30/40 自检结论 | Projects@59e4aae · api-python@197ce5b7 |
| P1-1 | 50 reinspect R1 | 独立复检 + 全局验收 | `ai-ink-brain-api-python/docs/harness/reviews/task_ops_chat_session_sink_p0_p1_v1_audit_R1_20260709_50_P1-1.md` | 待本审查落盘后 commit |

---

## Judgment（50）

- **experience_capture**: `required` — P1-1 artifact 写入与失败事件模式可复用到 P1-2 checkpoint 及其他运行时契约。
- **gate/risk**: 无 — `HG-TASK-DRAFT` / `HG-AUDIT-R1` 均为 `approved`；50 未遇 pending 人工闸。
- **hat_self**: `pass` — 独立复检与 30/40 结论一致，验证命令绿，输出 pass/fail 表、阻塞项清单、合并建议与执行路线回溯。
