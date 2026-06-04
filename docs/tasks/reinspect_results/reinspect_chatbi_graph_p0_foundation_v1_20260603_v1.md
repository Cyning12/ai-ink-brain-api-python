# 独立复检 · ChatBI Graph P0 地基 · v1

| 字段 | 值 |
| --- | --- |
| **task** | `docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |
| **task_slug** | `chatbi_graph_p0_foundation_v1` |
| **模式** | 独立复检 |
| **分支** | `task/chatbi-graph-p0-foundation-v1` |
| **实现 commit** | `b43ae3e`（`feat(chatbi): P0 Graph 地基`） |
| **40 自检 commit** | `e3a0d60` |
| **审查** | R2 [`task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md`](../harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md) |
| **invoke_snapshot** | [`invoke_20260603_50_reinspect.md`](../harness/invokes/by-task/chatbi_graph_p0_foundation_v1/invoke_20260603_50_reinspect.md) |
| **复检日期** | 2026-06-03 |
| **复检者** | Agent（50 帽 · Fresh Context） |

---

## 复检结论摘要

| 维度 | 判定 |
|------|------|
| **P0 五步交付** | **pass** — 共享层 / state+边表 / runner / Q-8 路由 / P0 单测 |
| **P0 单测** | **pass** — `tests/test_chatbi_graph_p0_foundation.py` **10/10** |
| **D-2 unified_chat** | **pass** — `git diff origin/main...HEAD -- api/unified_chat.py` 空 |
| **manifest** | **pass** — `tech_graph_manifest_check` OK；Q-8 两路由已登记 |
| **全集 pytest（AGENTS §8）** | **fail** — 277 passed · **10 failed**（与 `origin/main` 同 10 项 · **非** `b43ae3e` 引入） |
| **contract_check（task 字面）** | **fail** — `contract.frontend_anchors` · `label`（`origin/main` 同红 · 非 P0 新增） |
| **PR workflow** | **证据不足** — 本机未跑 Actions |

**50 总评（P0 增量）**：**pass-with-notes** — 实现与 R2/Delta 一致，**无 P0 范围回归**；**Strict 合并**仍被全集 pytest + contract 字面验收阻塞（分支基线既有红项）。

**是否建议合并（维护者）**：**条件性建议** — 若接受「P0 PR 不修复 v3 plan + contract label 基线债」，可合；若 Required check 须字面全绿 → **不建议合并** 直至基线修复或 CI 策略书面豁免。

---

## human_gate 追溯（commit-level）

| gate_id | 最终 status | 变更 commit | author | 结论 |
|---------|-------------|-------------|--------|------|
| HG-TASK-DRAFT | approved | `ab4ca03` | cyning | 人签单独 commit · 非 Agent 静默代填 |
| HG-AUDIT-R1 | approved | `ab4ca03` | cyning | 同上 |

`git log -p origin/main...HEAD -- docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` 中 `pending→approved` **仅**出现在 `ab4ca03`；与 task 修订记录一致。

---

## 独立验证命令（50 复跑）

| 命令 | exit | 要点 |
|------|-----:|------|
| `pytest tests/test_chatbi_graph_p0_foundation.py -q` | 0 | 10 passed |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 1 | 277 passed · 10 failed · 1 skipped |
| `python tools/tech_graph_manifest_check.py` | 0 | OK |
| `python tools/tech_graph_contract_check.py` | 1 | `contract 未声明字段: label` |
| `wc -l api/agent.py` | — | **1078**（抽取前 ~1342） |
| `origin/main` 对照 pytest 全集 | 1 | **267** passed · **10 failed**（同失败集） |
| `origin/main` 对照 contract_check | 1 | 同 `label` 红项 |

**10 failed 测试名（分支 = main 基线）**：`tests/test_unified_chat_backend_v2_agent.py` 内 `test_v3_*plan*`（含 clarify / preview / execution_token / sse_parity / rag 变体）。`git diff b43ae3e^..b43ae3e` **未**修改 `api/unified_chat.py`。

---

## 验收表（对照 task `## 验收标准`）

| 验收项 | pass/fail | 证据 | 备注 |
|--------|:---------:|------|------|
| `agent.py` 瘦身 + failure 迁出 | **pass** | `wc -l` 1078；`api/chatbi_failure.py:54` `FailureTypeHandler` | 289 行迁出至共享模块 |
| 共享模块 Graph/Agent 共用 | **pass** | `test_chatbi_shared_modules_importable`；`agent.py` import 共享层 | `b43ae3e` |
| `ChatBIState` + 边表 D-3 | **pass** | `api/graph/state.py:23-61`；`test_graph_intent_timeout_scheme_a` · `test_legacy_intent_timeout_v1_fallback` | graph=`direct_answer` · legacy=`intent_v1_fallback` |
| Q-8 Graph 路由 stub | **pass** | `api/index.py:649,657`；`test_graph_json_route_stub` · `test_graph_stream_route_stub` | HTTP 200 + stub JSON/SSE |
| `_manifest` + manifest check | **pass** | `_manifest.json` L138/L147；manifest_check OK | Q-8 两 path |
| `tech_graph_contract_check` 仍绿 | **fail** | exit 1 · `label` | **origin/main 同 fail**；P0 仅增扫描源 `chatbi_events.py` |
| 边表单测 + runner smoke | **pass** | `tests/test_chatbi_graph_p0_foundation.py` 10/10；`api/graph/runner.py:run_graph_stub` | required red-green 口径满足 P0 专测 |
| 必绿 pytest 全集（本地） | **fail** | 277/287 pass；10× v3 plan | 见上 · **非 P0 回归** |
| PR pytest workflow | **fail** | 未执行 `gh`/Actions | 本地全集未绿 → **不可假设** CI 绿 |
| `unified_chat.py` 无行为变更 | **pass** | `git diff origin/main...HEAD -- api/unified_chat.py` 0 行 | D-2 |
| 未做 P1 clarify/plan 上图 | **pass** | 无 `graph.*` SSE；runner stub 非 ReAct 环 | 非范围一致 |

---

## failure_paths 抽检（F1～F4）

| Scenario ID | 50 判定 | 证据 |
|-------------|:-------:|------|
| `fp-chatbi-p0-agent-regression` | **pass-with-notes** | 全集 10 fail 为 v3 · 非 agent 抽取；P0 专测 + 267 基线用例仍过 |
| `fp-chatbi-p0-contract-manifest` | **pass** | manifest OK；contract `label` 为 **frontend 锚点** 非 manifest 登记缺失 |
| `fp-chatbi-p0-graph-stub-http` | **pass** | 路由 smoke 200；鉴权与 Unified 同 override 模式 |
| `fp-chatbi-p0-edge-table-unit` | **pass** | 参数化边表 3 codes + scheme A 断言 |

---

## test_strategy: required（50 专节）

| 检查 | 结果 | 说明 |
|------|:----:|------|
| P0 先测后实现 | **pass** | 专测文件覆盖 Delta Scenario |
| 测试与实现同 PR | **pass** | `b43ae3e` 含 `tests/test_chatbi_graph_p0_foundation.py` |
| 全集回归 | **fail** | 分支/main 同 10 红 · 超出 P0 范围 |

---

## 阻塞合并项（Strict · task + AGENTS §8）

1. **全集 pytest 未绿** — 复现：`pytest tests -m "not intent_eval and not intent_benchmark"` → 10× `test_v3_*plan*` fail（main 已存在）。
2. **task 验收「contract_check 仍绿」字面 fail** — 复现：`python tools/tech_graph_contract_check.py` → `label`（main 已存在）。
3. **PR Required check 未在本复检验证** — 须 CI 或维护者签核。

**非阻塞（P0 范围）**：无。

---

## 给需求帽回填

**无**（P0 合同已闭合；基线债不属于本 task 范围，若修须 **新 task**）。

---

## Judgment（50）

- **experience_capture**: **维持 required** — P0 专测 red-green 有效；全集红项为仓内基线，不应降为 n/a。
- **gate/risk**: **须人审: merge-policy** — 是否接受 main 既有 10 fail + contract `label` 下合入 P0 PR。
- **hat_self**: **pass-with-notes** — P0 增量 independently verified；Strict 合并叙事须维护者决策。

---

## 下一棒可复制 Prompt（打回 / 人决策 · 非 30 返工 P0）

```text
【维护者决策 · 非 Harness 帽】

背景：50 复检 `reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md` — P0 增量 pass；全集 pytest 10× v3 plan + contract `label` 与 origin/main 同红。

请二选一并在 PR 说明中留证：
A) 接受基线债：P0 PR 合 main（Required check 策略须与仓库现状一致）
B) 先修基线：新开 task 修 v3 plan 十测 +/或 contract `label`，再合 P0

若选 B 且需 Agent 修 v3：新开 task，勿在 P0 task 扩 scope。
```
