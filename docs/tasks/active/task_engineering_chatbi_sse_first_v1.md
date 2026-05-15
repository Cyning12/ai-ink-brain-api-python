# Task：ChatBI 工程约定 — **新功能以 SSE 优先**（Harness 需求帽落盘）

> **状态**：`todo`（团队纪律；与具体 implementation 可并行）  
> **帽子依据**：工作区 `docs/harness/prompts/10-requirements.md`  
> **test_strategy**：`not_applicable`  
> **test_strategy_note**：流程/优先级约定；验收以 **SPEC/task 勾选 + 代码审查** 为准，无单独 pytest 门禁。

---

## 1. 背景与目标

Unified Chat 的 **观测与产品主路径** 已以 **`POST /api/py/unified/chat/stream`（SSE）** 为迭代重心；非流式 JSON 易成为「后补」路径。本单将纪律写死：**新增 ChatBI 行为（安全闸、可观测、门控）默认先接 SSE**，再对齐 JSON（除非 task 显式豁免）。

---

## 2. 范围 / 非范围

**范围**

- 后端新能力排期：设计评审时 **先问**「SSE 首帧 / `chain` 事件 / `done` 是否与 JSON 语义一致」。  
- 与 **P1-2 Prompt guard** 对齐：`handle_unified_chat_stream` 已与 JSON 共用 `_unified_prompt_guard_short_circuit_events`（见 `api/unified_chat.py`）。  

**非范围**

- 不强制废弃 JSON 端点；**双轨**仍保留。  
- 不修改 Ink 前端布局（另 task）。

---

## 3. 依赖

| 项 | 路径 |
|----|------|
| Prompt guard P1-2 | `docs/tasks/active/task_chatbi_v3_prompt_injection_guard_poc_v1.md` |
| 安全子规 | `docs/spec/v3-agent/SPEC-ChatBI-V3-Security.md` §3.1 |

---

## 4. 验收标准

- [ ] 后续 **含 Unified 行为变更** 的 task 在 **§实现备忘** 或 **非范围** 中显式写明 **「SSE 与 JSON 是否同时交付」**；默认 **同时** 除非豁免理由一行。  
- [x] 总规或子规索引处（可选）链回本文件，避免口头约定漂移。已落锚：本仓 [`docs/tasks/README.md`](../README.md) → **工程纪律索引**。

---

## 5. failure_paths

与 `docs/harness/HARNESS_V2_PLAN.md` §5.3 对齐：**触发条件** → **系统/流程行为** → **是否可重试** → **用户可见文案类型**（不适用列显式 `N/A`）。

| ID | 触发 | 行为 | 是否可重试 | 用户可见文案类型 |
|----|------|------|------------|------------------|
| FP-1 | 仅 JSON 合入、SSE 漏接且 task 未豁免 | **Code Review 打回** 或补 follow-up task | 否（须修订实现或补充/豁免 task 后重新发起 MR） | `N/A`（流程/CR 闸门；无面向终端用户的可见文案类型） |

---

## 6. 给执行帽的必读列表

1. 读本单 **§2**。  
2. 改 `unified_chat` 时同时打开 **`handle_unified_chat`** 与 **`handle_unified_chat_stream`**  diff。

---

## 7. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-15 | **按审查 R1 回填**：[`../../harness/reviews/task_engineering_chatbi_sse_first_v1_audit_R1_20260515.md`](../../harness/reviews/task_engineering_chatbi_sse_first_v1_audit_R1_20260515.md) — §5 `failure_paths` 增补 `HARNESS_V2_PLAN.md` §5.3 建议列（可重试性、用户可见类型；不适用处标 `N/A`）；§4 验收第 2 条在 [`../README.md`](../README.md)「工程纪律索引」回链。 |

---

## 给 Cursor

`SSE 优先`、`unified_chat_stream`、`task_engineering_chatbi_sse_first_v1`、`10-requirements`
