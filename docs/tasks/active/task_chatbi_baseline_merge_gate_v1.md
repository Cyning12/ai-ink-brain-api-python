# Task：ChatBI 基线合并闸 — origin/main 既有 pytest + contract 红项修复

> **状态**：`active`（10 需求帽草案 · 待 22 R1）  
> **维护者决策**：50 复检 `[reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md](../reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md)` **选 B** — 先修 main 基线债，再合 P0 Graph PR  
> **关联图谱**：`docs/_tech_graph/_contract_manifest.json`（Unified SSE 跨端契约）；`api/unified_chat.py` / `api/agent.py`（v3 plan/clarify 路径）  
> **schedule_ref**：P0 Graph 合入前置 · 见 `[RECENT_TASK_SCHEDULE.md](../RECENT_TASK_SCHEDULE.md)`（待维护者补锚）

---

## Harness 元信息（执行 Agent 必读）


| 字段                     | 值                                                                                                                                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **task_slug**          | `chatbi_baseline_merge_gate_v1`                                                                                                                                                                          |
| **semi_auto**          | `true`                                                                                                                                                                                                   |
| **test_strategy**      | `required`                                                                                                                                                                                               |
| **test_strategy_note** | 涉 `api/` Unified Chat v3 plan/clarify 行为回归 + `_contract_manifest.json` 同步；须 red-green 对齐既有 10 测；关账前须 50 落盘                                                                                               |
| **audit_profile**      | `post_close`                                                                                                                                                                                             |
| **freeze_id**          | （无新 L1 SPEC；行为真值以既有 v3 单测断言 + `_contract_manifest.json` 为准）                                                                                                                                              |
| **gates_before_code**  | `harness_task_validate.py` OK · `## 失败路径` + Scenario ID · `## 验收标准` 含 pytest + contract + PR workflow · `## 行为变更（Delta）` 已填 · 必读列表已读 · `HG-TASK-DRAFT` = `approved` · `HG-AUDIT-R1` = `approved`（路径 A 后） |
| **git_branch**         | `task/chatbi-baseline-merge-gate-v1`（从 **最新 `origin/main`** 拉出；开干前 `git fetch && git rebase origin/main`）                                                                                                |
| **Open Folder**        | `ai-ink-brain-api-python`                                                                                                                                                                                |
| **blocked_by**         | （无 — 本 task 为 P0 前置）                                                                                                                                                                                     |
| **blocks**             | `chatbi_graph_p0_foundation_v1` — P0 分支 **须** 本 PR 合入 main 后 **rebase** 再开 PR                                                                                                                            |
| **experience_capture** | `required`                                                                                                                                                                                               |
| **kpi_rubric**         | `KPI_RUBRIC_v1_2`                                                                                                                                                                                        |
| **kpi_aggregator**     | `CLOSE`                                                                                                                                                                                                  |
| **推荐路径**               | **22 R1**（`test_strategy: required` + 涉 `api/` + 契约）                                                                                                                                                     |


### 人工闸 `human_gate`


| human_gate_id | status   | blocks_hats | 说明                                   |
| ------------- | -------- | ----------- | ------------------------------------ |
| HG-TASK-DRAFT | approved | 22-R1, 30   | 初稿 task 人扫                           |
| HG-AUDIT-R1   | approved | 30          | 22 R1 落盘 `docs/harness/reviews/` 后人签 |


---

## 1. 背景与目标

P0 Graph 地基 task（`chatbi_graph_p0_foundation_v1`）增量经 50 复检 **pass-with-notes**，但 **Strict 合并**仍被 `**origin/main` 既有** 两类红项阻塞（与 P0 分支同型，**非 P0 引入**）：

1. **10× pytest fail** — `tests/test_unified_chat_backend_v2_agent.py` 内 ChatBI v3 **plan preview / execution_token / low-confidence clarify** 相关用例（典型：期望 SSE/JSON 含 `agent.plan.preview` 等事件，当前实现未产出）。
2. `**tech_graph_contract_check` fail** — `contract.frontend_anchors.sse_consumer_files` 扫描：前端 TS 读取字段 `**label`**，`_contract_manifest.json` **未声明**（main 已红）。

**本 task 完成态（一句话）**：在 **独立 PR → main** 内修复上述基线债，使 `pytest tests -m "not intent_eval and not intent_benchmark"` 与 `python tools/tech_graph_contract_check.py` **全绿**，PR `**pytest` workflow Required check 全绿**；**不** 夹带 P0 Graph 五步交付物。

**合并策略（硬）**：


| 顺序  | 动作                                                                                  |
| --- | ----------------------------------------------------------------------------------- |
| 1   | 本 task PR **单独** 合入 `main`                                                          |
| 2   | P0 分支 `task/chatbi-graph-p0-foundation-v1` **rebase** 最新 `main`                     |
| 3   | P0 task 元信息补 `**blocked_by: chatbi_baseline_merge_gate_v1`**（若 rebase 前未写入）后开 P0 PR |


---

## 2. 范围


| #   | 交付                        | 要点                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ①   | **v3 plan/clarify 行为对齐**  | 修复 `api/unified_chat.py` / `api/agent.py`（及必要共享模块）使下列 **10 测** 通过（**不** 删测、**不** 放宽断言）： `test_v3_low_confidence_clarify_json_skips_text2sql` `test_v3_plan_preview_json_includes_plan_preview_and_ttl_notice` `test_v3_plan_execution_token_json_bypasses_clarify` `test_v3_plan_execution_token_invalid_json_denies_bypass` `test_v3_plan_preview_fail_json_no_token` `test_v3_plan_preview_sse_parity` `test_v3_rag_plan_preview_json_includes_rewrite_query` `test_v3_rag_plan_execution_token_json_bypasses_clarify` `test_v3_rag_plan_preview_fail_json_no_token` `test_v3_rag_plan_preview_sse_parity` |
| ②   | **contract `label` 漂移修复** | 按 `[RUNBOOK_graph_contract_ci_red_v1.md](../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md)` **路径 A**：同 PR 更新 `_contract_manifest.json`（及触达时的 `.ai.md` / export）；`python tools/tech_graph_contract_check.py` **exit 0**                                                                                                                                                                                                                                                                                                                                                                                  |
| ③   | **全集回归**                  | `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿（AGENTS §8 等价）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ④   | **CI**                    | PR 上 `.github/workflows/pytest.yml`（workflow 名 `**pytest`**）全绿                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |


**实现约束**：

- 优先 **恢复/对齐既有 v3 契约语义**（单测即规格）；禁止为绿而删用例或改 marker 排除。
- contract 修复若将 `label` 列为前端 UI 辅助字段，须与 Runbook **路径 A** 一致并在 Delta 留痕；**禁止** 静默忽略真实跨端契约字段。

---

## 3. 非范围

- **P0 Graph 五步**（`chatbi_events` / `chatbi_agent_models` / `chatbi_failure` 抽取 · `api/graph/`* · Q-8 `/graph` 路由 · P0 专测 `test_chatbi_graph_p0_foundation.py`）— **禁止** 本 PR 夹带。
- **P1** clarify/plan **上图**、Graph SSE parity、ReAct 完整环。
- **前端 / BFF**（`ai-ink-brain`）功能改动（contract 仅同步 manifest 声明；**不** 改 TS 消费逻辑除非 manifest 策略明确要求）。
- **CI workflow / Required check 策略变更**（本 task 以现有 `pytest.yml` 为准）。
- **新 L1 SPEC**；**图谱大改**（无行为变更时不强制改 `.ai.md`）。

---

## 4. 依赖（相对路径 · 只读真值）


| 用途                  | 路径                                                                                                                                      |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 50 复检 · 选 B 依据      | `[reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md](../reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md)` |
| P0 task（被阻塞）        | `[task_chatbi_graph_p0_foundation_v1.md](task_chatbi_graph_p0_foundation_v1.md)`（P0 分支；main 上可能不存在）                                     |
| 失败用例                | `tests/test_unified_chat_backend_v2_agent.py`                                                                                           |
| contract 真值         | `docs/_tech_graph/_contract_manifest.json`                                                                                              |
| contract CI Runbook | `[RUNBOOK_graph_contract_ci_red_v1.md](../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md)`                                          |
| v3 事件语义（参考）         | `[SPEC-ChatBI-V2-Events.md](../spec/v2-agent/SPEC-ChatBI-V2-Events.md)`                                                                 |
| 环境 / 目录             | `[PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md)`                                        |
| Harness 字段          | `[HARNESS_V2_PLAN.md](../harness/HARNESS_V2_PLAN.md)` §5                                                                                |
| 合并前必绿               | `AGENTS.md` §8 · `.github/workflows/pytest.yml`                                                                                         |


---

## 行为变更（Delta）

> 相对 `**origin/main` 基线**（修复漂移 · **非** 新功能）。

### ADDED

- **Requirement**：跨端 contract 允许前端 SSE 消费者读取 UI 辅助字段 `label`（若 Runbook 路径 A 判定为合法 UI 字段）。
  - **Scenario**：`baseline-contract-label-declared` — GIVEN 前端 `UnifiedChatPageClient.tsx` 读取 `label` WHEN `tech_graph_contract_check` THEN manifest 已声明或列入 `frontend_ts_ignore_payload_like_keys`，check **exit 0**。

### MODIFIED

- **Requirement**：Unified Chat v3 plan preview / execution_token / low-confidence clarify 路径恢复单测期望的 SSE/JSON 事件语义（Previously: main 上 10 测红 · `agent.plan.preview` 等未产出或路径断裂）。
  - **Scenario**：`baseline-v3-plan-preview-events` — GIVEN v3 plan/clarify 请求 WHEN 跑 `tests/test_unified_chat_backend_v2_agent.py` 上述 10 用例 THEN 全部 **pass**；全集 pytest marker 排除集 **pass**。

### REMOVED

- （无）

---

## 5. 给执行帽（30）的必读列表

1. 本 task §2～§3、`## 验收标准`、`## 失败路径`、`gates_before_code`、**合并策略**。
2. `[reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md](../reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md)` §阻塞合并项。
3. `tests/test_unified_chat_backend_v2_agent.py` — 10 个失败用例通读断言。
4. `[RUNBOOK_graph_contract_ci_red_v1.md](../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md)` §2 路径 A。
5. `docs/_tech_graph/_contract_manifest.json` — `frontend_anchors` / `frontend_ts_ignore_payload_like_keys`。
6. `api/unified_chat.py` · `api/agent.py` — v3 plan/clarify _emit 路径（**禁止** 引入 P0 graph 模块）。
7. `[docs/harness/prompts/hats/30-execute-code.md](../harness/prompts/hats/30-execute-code.md)` — 拒开工条件。

**VERIFY（合并前）**：

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
python tools/tech_graph_contract_check.py
```

---

## 验收标准

- 上述 **10** 个 v3 plan/clarify 用例 **全部 pass**（`tests/test_unified_chat_backend_v2_agent.py`）
- `pytest tests -m "not intent_eval and not intent_benchmark"` **全绿**（本地 · AGENTS §8 等价）
- `python tools/tech_graph_contract_check.py` **exit 0**（`label` 漂移已修复）
- `python tools/tech_graph_manifest_check.py` **仍绿**（若本 PR 未改 manifest 则对照基线仍 OK）
- PR 上 `**.github/workflows/pytest.yml`**（workflow 名 `**pytest**`）**Required check 全绿**
- **未** 夹带 P0 Graph 交付物（`api/graph/`* · Q-8 路由 · `test_chatbi_graph_p0_foundation.py` · P0 manifest 增量）
- 若触达 `_contract_manifest.json` / `.ai.md`：`## 行为变更（Delta）` 与实现 **一致**
- `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` **OK**

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"` + `python tools/tech_graph_contract_check.py`（见 `AGENTS.md` §8 与 `tech-graph-contract.yml`）。

---

## 失败路径


| #   | Scenario ID                        | 触发条件                                                                           | 系统行为                                   | 可重试 | 用户可见                                                 | 测试（可选）                                      |
| --- | ---------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------- | --- | ---------------------------------------------------- | ------------------------------------------- |
| F1  | `fp-baseline-v3-plan-regression`   | 修复后仍缺 `agent.plan.preview` / clarify 短路语义错误；或引入非范围 P0 模块导致其他 pytest/contract 红 | CI pytest **fail**；PR **不可合并**         | 是   | Unified Chat v3 plan/clarify 路径异常（SSE/JSON 缺事件或错误短路） | 10× v3 用例 + 全集 pytest                       |
| F2  | `fp-baseline-contract-label-drift` | 仅改 api 未同步 manifest；或误将 `label` 标为后端必出键导致扫描反向失败                                | `tech_graph_contract_check` **exit 1** | 是   | 无（CI 阻塞）                                             | `python tools/tech_graph_contract_check.py` |
| F3  | `fp-baseline-scope-creep-p0`       | PR diff 含 P0 Graph 五步（`api/graph/`*、Q-8 路由、P0 专测等）                             | 22/50 **拒签收**；维护者 **revert** 或拆 PR     | 否   | 无                                                    | `git diff origin/main...HEAD` 范围审查          |


---

## 修订记录


| 日期         | 摘要                                                                                              |
| ---------- | ----------------------------------------------------------------------------------------------- |
| 2026-06-04 | 10 需求帽：基线合并闸 task 草案 · invoke `invoke_20260604_10_chatbi-baseline-merge-gate.md` · 维护者 50 复检选 B |


**下一棒**：**22 任务审核 R1**（推荐）或 **30 执行**（跳过 22 · 人承担闸 1）。

---

## KPI（00）

> 关账前由 CLOSE / 00 汇总；开工时留空。


| 指标        | 值     |
| --------- | ----- |
| Task_KPI% | （关账填） |
| blocked   | （关账填） |


