# 50 独立复检 · Ops Chat ← Session 能力下沉 · P1-2 Checkpoint

| 字段 | 值 |
| --- | --- |
| **task** | `ops-chat-session-sink-p0-p1` |
| **phase** | P1-2 Checkpoint |
| **subproject** | `ai-ink-brain-api-python` |
| **audit_round** | R1 |
| **date** | 2026-07-09 |
| **hat** | 50-reinspect |
| **30 commit** | `api-python@35279435` |
| **40 commit** | `api-python@3ee3c0ee` · `Projects@c8f1410` |

---

## 复核方法

1. 独立阅读 task 正文「### 自检结论（执行者）· P1-2」与「### 自检结论（40 复核）· P1-2」小节。
2. 独立阅读本轮 P1-2 改动代码：
   - `api/ops/store/checkpoints.py`
   - `api/ops/store/runs.py`
   - `api/ops/react_loop.py`
   - `tests/ops/test_checkpoint.py`
3. 在 `ai-ink-brain-api-python/` 内完整执行 30 声明的验证命令：
   ```bash
   pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q && ruff check api/ops
   ```
4. 额外执行 task §失败路径所列的 `pytest tests/ops/test_checkpoint.py -k corrupted -q`。
5. 执行 `git diff origin/main...HEAD --stat`（在 `ai-ink-brain-api-python` 内）核对全量变更路径，确认未扩 scope 到 P1-3/4、Session 生产图、Agently lab、前端。
6. 与 30 commit `api-python@35279435`、40 commit `api-python@3ee3c0ee` / `Projects@c8f1410`、R2 任务审核书面结论逐条核对。

---

## 命令输出

### 主验证命令

```text
pytest tests/ops tests/ops_desk -m "not intent_eval and not intent_benchmark" -q
.................................s...................................... [ 23%]
........................................................................ [ 46%]
........................................................................ [ 69%]
........................ss......................sssssss................. [ 93%]
.....................                                                    [100%]
=============================== warnings summary ================================
../../../miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1
  /Users/cyning/miniconda3/lib/python3.13/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/howto/capture-warnings.html
=========================== short test summary info ============================
SKIPPED [1] tests/ops/test_events_schema.py:181: 需要真实 Supabase 连接；本地/CI 环境缺失时跳过
SKIPPED [2] tests/ops_desk/test_run_schema_p1.py:102: public 中表已存在，跳过写测试以避免破坏数据
SKIPPED [7] tests/ops_desk/test_schema_p0.py:102: public 中表已存在，跳过写测试以避免破坏数据
299 passed, 10 skipped, 1 warning in 50.93s

ruff check api/ops
All checks passed!
```

- pytest 退出码：`0`
- ruff 退出码：`0`
- 10 skipped 中：1 个为 `tests/ops/test_events_schema.py::test_append_event_integration_with_real_store`（显式 skip，需真实 Supabase 连接）；其余 9 个为 `tests/ops_desk/test_run_schema_p1.py` / `tests/ops_desk/test_schema_p0.py` 中环境感知跳过（表已存在），与 P1-2 改动无关。

### 失败路径额外验证

```text
pytest tests/ops/test_checkpoint.py -k corrupted -q
...                                                                      [100%]
3 passed, 4 deselected in 0.50s
```

- pytest 退出码：`0`

---

## 与 30 / 40 结论差异核对

| 30 / 40 声称项 | 50 独立复核 | 结果 |
| --- | --- | --- |
| 复用已有 `ops_run_checkpoints` 表 | `api/ops/store/runs.py` 已存在 `save_checkpoint`；新增 `load_checkpoint` / `find_latest_checkpoint_for_session`；未改表结构 | 一致 |
| 新增 `api/ops/store/checkpoints.py` | 文件存在；`save_checkpoint` / `load_checkpoint` / `find_latest_checkpoint_for_session` / `CheckpointStoreError` 均实现 | 一致 |
| ReAct 路径每步后保存 checkpoint | `react_loop.py` 在每次非最终 step 后调用 `_try_save_checkpoint`（`react_loop.py:353-367`） | 一致 |
| 同 session 续问隐式恢复并续跑 | `run_react_fallback` 启动时若 `session_id` 存在则调用 `find_latest_checkpoint_for_session`；有效 checkpoint 通过 `_resume_react_state` 恢复并 emit `checkpoint.resume`；单测 `test_same_session_resumes_from_checkpoint` 通过 | 一致 |
| checkpoint 损坏时冷启动且不 500 | `_resume_react_state` 捕获 `CheckpointStoreError`，emit `checkpoint.corrupted` 并返回 None，走冷启动分支；3 个 corrupted 测例均通过 | 一致 |
| `checkpoint.corrupted` event 被记录 | 事件 `event_type=checkpoint.corrupted`，payload 含 `error` / `session_id` / `from_run_id` | 一致 |
| deep 路径未支持 checkpoint | `origin/main...HEAD` diff 未包含 `api/ops/orchestrator/core.py` | 一致 |
| P1-1 artifact 行为未被破坏 | `save_artifact_with_failure_event` 与 `artifact.write_failed` 保留；artifact 测例全绿 | 一致 |
| P0-3/P0-4 行为未被破坏 | transcript / tracing 相关测例全绿 | 一致 |
| 新增单测覆盖 | `tests/ops/test_checkpoint.py` 7 测例全绿 | 一致 |
| 验证命令绿 | 本轮独立跑通 `299 passed, 10 skipped` + ruff 全绿 | 一致 |
| 未扩 scope | 全量 diff 仅 P1-2 checkpoint 相关文件 + invoke；未涉及 P1-3/4、Session 生产图、Agently lab、前端 | 一致 |

**差异项**：无。

**非阻塞观察**：
- `api/ops/store/checkpoints.py` 中定义的 `_validate_react_state` 当前未被引用，实际校验由 `api/ops/react_loop.py` 内 `_validate_react_checkpoint` 完成；属轻微代码冗余，不影响功能与测试。
- `checkpoints.py` 文件末尾缺少换行符；不影响 ruff / pytest。

---

## 验收项复核表

| 验收项 | 状态 | 证据 | 备注 |
| --- | --- | --- | --- |
| `api/ops/store/checkpoints.py` 存在且实现 `save_checkpoint` / `load_checkpoint` / `find_latest_checkpoint_for_session` | pass | `checkpoints.py:45-97` | `CheckpointStoreError` 同文件定义 |
| `api/ops/store/runs.py` 为 `OpsRunStore` 新增 `load_checkpoint` / `find_latest_checkpoint_for_session` | pass | `runs.py:219-253` | 按 `checkpoint_id=session_id` 跨 run 取最新一条 |
| ReAct 路径每步后保存 checkpoint | pass | `react_loop.py:353-367` | 仅非最终 step、且 `session_id` 存在时保存 |
| 同 session 续问隐式恢复并续跑 | pass | `react_loop.py:231-262` | 查找并恢复 checkpoint；`test_same_session_resumes_from_checkpoint` 断言续跑完成 |
| checkpoint 损坏时冷启动且不 500 | pass | `_resume_react_state` 捕获 `CheckpointStoreError` 并返回 None；3 个 corrupted 测例通过 | — |
| `checkpoint.corrupted` event 被记录 | pass | `react_loop.py:112-123` emit `checkpoint.corrupted`，payload 含 `error` / `session_id` / `from_run_id` | — |
| deep 路径未支持 checkpoint（符合范围） | pass | diff 未含 `api/ops/orchestrator/core.py` | — |
| P1-1 artifact 行为未被破坏 | pass | `react_loop.py:495-506` 仍调用 `save_artifact_with_failure_event`；artifact 测例全绿 | — |
| P0-3/P0-4 行为未被破坏 | pass | transcript / tracing 相关测例全绿；`load_chat_transcript` / `trace_span` 调用路径保留 | — |
| `tests/ops/test_checkpoint.py` 覆盖完整 | pass | 7 测例全绿：save/load、按 session 查找、损坏冷启动、无效 schema、同 session 续跑、失败路径验证 | — |
| 最终验证命令绿 | pass | pytest `299 passed, 10 skipped` + ruff `All checks passed!` | 退出码均为 `0` |
| 失败路径验证命令绿 | pass | `pytest tests/ops/test_checkpoint.py -k corrupted -q` → `3 passed, 4 deselected` | — |
| 未静默扩大 scope | pass | 全量 diff 仅 `api/ops/react_loop.py`、`api/ops/store/checkpoints.py`、`api/ops/store/runs.py`、`tests/ops/test_checkpoint.py` + invoke 文档；未涉及 P1-3/4、Session 生产图、Agently lab、前端 | — |

---

## 阻塞项清单

无。

---

## 合并建议

**建议合并**。P1-2 Checkpoint 续跑实现、测试、30 执行、40 自检、50 独立复检均通过，无 scope creep，人工闸 `HG-TASK-DRAFT` / `HG-AUDIT-R1` 已 approved。

---

## 执行路线与 Commit 回溯

| 阶段 | 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|------|----------|----------|-------------|
| P1-2 | 30 execute | ReAct checkpoint save/load/resume + corrupted 处理 + 测试 | `api/ops/store/checkpoints.py`, `api/ops/store/runs.py`, `api/ops/react_loop.py`, `tests/ops/test_checkpoint.py` | `api-python@35279435` |
| P1-2 | 40 self-check | 复核 P1-2 验收 | task 内 P1-2 30/40 自检结论 | `api-python@3ee3c0ee` · `Projects@c8f1410` |
| P1-2 | 50 reinspect R1 | 独立复检 + 全局验收 | 本文件 | 待本审查落盘后 commit |

---

## Judgment（50）

- **experience_capture**: `required` — P1-2 checkpoint save/resume/corrupted 事件模式与状态序列化经验可复用到后续 P1-3/P1-4 及 Session 相关能力。
- **gate/risk**: 无 — `HG-TASK-DRAFT` / `HG-AUDIT-R1` 均为 `approved`；50 未遇 pending 人工闸。
- **hat_self**: `pass` — 独立复检与 30/40 结论一致，验证命令绿，输出 pass/fail 表、阻塞项清单、合并建议与执行路线回溯。
