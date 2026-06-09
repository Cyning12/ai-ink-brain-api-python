> **epic**: `standards-engineering/api-modularization`
> **manifest_ref**: W6 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**: `required`
> **非范围**: MANIFEST 表内未列出的 `api/*.py` 文件

---

# W6 · Agent 循环子模块拆分

> **状态**: done（PR [#153](https://github.com/Cyning12/ai-ink-brain-api-python/pull/153) · 2026-06-09）
> **slug**: `api-agent-loop-split`
> **git_branch**: `task/api-agent-w6`
> **风险**: High
> **freeze_id**: `CODING_BACKEND_L2@2026-06-09`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-agent-loop-split` |
| **git_branch** | `task/api-agent-w6` |
| **orchestration** | Claude Code Harness 链 |
| **chain_prompt** | `PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md` |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `api/agent.py` 中 `ChatBIAgent` 类的 tool 调度与 persist 逻辑抽至子模块；`agent.py` 保留薄编排层。

### 下沉范围

| 模块 | 说明 |
|------|------|
| `api/agent_tool_runner.py` | Tool 执行调度（`_select_tool`, `_tool_to_mode`, `_next_tool_after_success`） |
| `api/agent_persist.py` | Agent 日志持久化（`_sync_persist_chatbi_v2_agent_log` 等） |

### 策略

- **留在 `agent.py`**：`ChatBIAgent` 类骨架、`run()` 主循环、`_step()` 编排
- **下沉**：tool 调度逻辑、persist 辅助函数
- `agent.py` 从子模块 import 下沉的函数/类

---

## 行为变更（Delta）

### ADDED
- `api/agent_tool_runner.py`
- `api/agent_persist.py`

### MODIFIED
- `api/agent.py` — 移除下沉逻辑

### 不变
- `ChatBIAgent.run()` 对外接口不变

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-mega-refactor | 单 PR 触及 >8 个 `api/*.py` | **拒合并** |
| F2 | fp-agent-break | 拆分破坏 Agent 循环 | **40 阻塞** |

---

## 验收标准

- [x] `api/agent_tool_runner.py` 存在且 ruff 绿
- [x] `api/agent_persist.py` 存在且 ruff 绿
- [ ] `agent.py` 行数从 ~1096 降至 ~<600（**defer**：主循环 `run()` 仍留本文件 · 1060 行；子模块拆分已达成 tool/persist 下沉）
- [x] Agent 相关测试通过
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [x] `ruff check api tests` 全绿
- [x] 单 PR 触及 `api/*.py` 数量 ≤8（本 PR：**4** 个）

## 实现备忘

| 项 | 内容 |
| --- | --- |
| 子模块 | `agent_tool_runner.py`（调度）· `agent_persist.py`（落库 + trace 脱敏） |
| 接线 | `unified_chat.py` re-export persist/trace；handlers 仍从 `unified_chat` import |
| agent.py | 1096 → **1060** 行（tool 调度下沉 ~36 行） |

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W6 task 初稿 — agent 循环子模块拆分 |
| 2026-06-09 | v1.1：实现完成 · PR [#153](https://github.com/Cyning12/ai-ink-brain-api-python/pull/153) merge · 关账 |
