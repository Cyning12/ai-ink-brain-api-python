# Task：ChatBI Graph P0 地基 — 共享层抽取 + State/边表草案 + 骨架路由（单 Loop）

> **状态**：`done（2026-06-04 · PR #107 merged · 50 pass-with-notes）`  
> **Task-P0**：对齐 [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) **§4A** · **§10 Task-P0**  
> **冻结决策**：[`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) **§4.3**（D-1～D-5）  
> **关联图谱**：`docs/_tech_graph/00_main.ai.md`（Q-8 路由已登记 `_manifest`）；`10_flow_agent_graph.ai.md` **defer P1 Task-B**  
> **审查**：R1 [`task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md`](../harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md) · R2 [`task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md`](../harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md)  
> **50 复检**：[`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`](../reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md)  
> **合并**：PR [#106](https://github.com/Cyning12/ai-ink-brain-api-python/pull/106) 基线闸 · PR [#107](https://github.com/Cyning12/ai-ink-brain-api-python/pull/107) P0 实现 · `main@f53327a`

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
| --- | --- |
| **task_slug** | `chatbi_graph_p0_foundation_v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **test_strategy_note** | 涉 `api/` 模块抽取与新 HTTP 路由；须 red-green / 边表单测 + runner smoke；**关账前须 50 帽**（`reinspect_results/`） |
| **audit_profile** | `post_close` |
| **freeze_id** | （本 Loop **无** 新 L1 SPEC；行为真值引用 research/plan SPEC 与 V2 总规） |
| **gates_before_code** | `harness_task_validate.py` OK · `## 失败路径` + Scenario ID · `## 验收标准` 含 pytest/PR workflow · **SDD §10 已冻结（Q-8 等）** · `## 行为变更（Delta）` 已填 · 必读列表已读 · `HG-TASK-DRAFT` = `approved` · `HG-AUDIT-R1` = `approved`（路径 A 后） |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **推荐路径** | **50 独立复检** — `test_strategy: required` + 关账前 `reinspect_results/` |
| **worktree_root** | （非并行时与 Open Folder 同仓根；并行时 invoke 另填） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | — | 人签 **2026-06-03**（R1 B-1 · 本 commit） |
| HG-AUDIT-R1 | approved | — | 22 R2 零阻塞 · 人签 **2026-06-03**（本 commit） |

---

## 1. 背景与目标

ChatBI V2 `ChatBIAgent.run` 与 Unified Chat 编排堆叠在 `api/agent.py`（约 1342 行），控制流与 SSE/失败路由耦合，难以单测与演进。冻结决策 **D-1～D-5** 已选定 **自研 StateGraph**、**并行 Graph 新路由**、**不改** 现有 `unified_chat.py` 行为。

**本 task 完成态（一句话）**：在旧 Unified/Agent **行为不变** 前提下，抽出 `chatbi_events` / `chatbi_agent_models` / `chatbi_failure`；落地 `ChatBIState` 与 **legacy/graph 分表** 边表草案；注册 Graph **骨架** HTTP 路由（stub 可调用）；`pytest tests -m "not intent_eval and not intent_benchmark"` 全绿；`_manifest` / `tech_graph_contract_check` 仍绿。

**Harness 管控**：本 Loop = **P0 单 Loop**（合并原 Task-A + Task-A′）；**00/10 收口** scope 与 Done；**禁止** 夹带 P1 完整 intent→tool parity（见 §5）。

**Graph 路由（Q-8 已冻结）**：`POST /api/py/unified/chat/graph` · `POST /api/py/unified/chat/graph/stream`（与 Plan SPEC §5.5 一致）。

---

## 2. 范围

对齐计划 SPEC **§4A.2** 五步（30 帽须按序交付，可在同一 PR 内完成）：

| 步 | 交付 | 要点 |
| ---: | --- | --- |
| ① | **agent 抽模块** | `chatbi_events.py` · `chatbi_agent_models.py` · `chatbi_failure.py`；`agent.py` 改 import；`run()` 逻辑 **不删不改语义** |
| ② | **State + 边表草案** | `api/graph/state.py`（`ChatBIState`）；`failure_edges_legacy()` / `failure_edges_graph()`（Graph Intent 超时 **方案 A**，legacy 保留 v1 fallback，D-3） |
| ③ | **最小 runner** | `api/graph/runner.py`（stub 节点，**非** 完整 ReAct） |
| ④ | **骨架路由** | `unified_chat_graph.py`（或等价薄 handler）+ `index` 注册 Q-8 端点 + `_manifest` 登记 |
| ⑤ | **单测** | 边表参数化 + runner smoke；必绿 pytest 集全绿 |

**契约 / 图谱（本 Loop 内）**：

- 更新 `docs/_tech_graph/_manifest.json`（或仓内 manifest 真值路径）登记 **Q-8** 两路由。
- `_CONTRACT_ANCHOR_*` 迁出后须仍可被 `tech_graph_contract_check` 扫描（re-export 或更新扫描路径）。
- **D-5 / 项 3**：P0 **不** 新增 `graph.*` SSE type。

---

## 3. 非范围（§4A.4 · 留给 P1 Task-B 及以后）

- 完整 **intent → tool → fallback** ReAct 环与旧 Agent **parity** 测。
- Graph SSE 与旧路径 **帧级 parity**；大规模 `unified_chat.py` import 改造。
- **P1**：clarify / plan preview 上图 · Structured Output 回灌 · Tool schema 自动生成。
- **前端 / BFF**（`ai-ink-brain`）任何改动（D-4：**否**）。
- **HITL interrupt / checkpointer**（P2）。
- 引入 `langgraph` / `langchain`（D-1）。
- 修改 `unified_chat.py` **行为**（D-2）。
- Legacy `/api/py/chat` 链 LCEL 化；Graph 路径接入 V1 规则路由。

---

## 4. 依赖（相对路径 · 只读真值）

| 用途 | 路径 |
| --- | --- |
| P0 单 Loop · Done · 五步 | [`docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) §4A · §10 |
| D-1～D-5 冻结 | [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3 |
| LangChain 背景（低优先模式） | [`SPEC-Research-SelfChain-vs-LangChain-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangChain-v1_zh.md) |
| V2 fallback 对照 | [`SPEC-ChatBI-V2-Agent-Overview.md`](../spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md) §2.4 |
| 抽模块锚点 | `api/agent.py` |
| 环境 / 目录 | [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| SDD 三轮纪律 | [`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) |
| Harness 字段 | [`HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5 |
| 22 R1 审查 | [`task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md`](../harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md) |
| 合并前必绿 | `pytest tests -m "not intent_eval and not intent_benchmark"` |

---

## 行为变更（Delta）

> 相对现网 `api/agent.py` 单体编排 + 无 Graph 路由的增量（P0 · **无** Unified 行为变更）。

### ADDED

- **Requirement**：共享层模块可被 Agent 与 Graph 共用。
  - **Scenario**：`chatbi-events-extract` — GIVEN P0 PR WHEN 迁出 `_agent_chain` 等 THEN `api/chatbi_events.py` 存在且 Graph/Agent 可 import。
- **Requirement**：Graph 骨架路由可调用（stub）。
  - **Scenario**：`graph-route-stub` — GIVEN 合法 Unified 鉴权 WHEN `POST /api/py/unified/chat/graph`（及 `/graph/stream`）THEN HTTP 200 + 最小 JSON/SSE 心跳（项 5 选项 A）；**不要求** Agent parity。
- **Requirement**：`ChatBIState` 与边表草案可单测。
  - **Scenario**：`graph-edge-table-smoke` — GIVEN mock state WHEN 边表驱动 fallback THEN Graph 侧 Intent 超时走方案 A；legacy 保留 v1 fallback（D-3）。
- **Requirement**：新端点登记图谱 manifest。
  - **Scenario**：`manifest-graph-endpoints` — GIVEN Q-8 路径 WHEN 更新 `_manifest` THEN `tech_graph_contract_check` 仍绿。

### MODIFIED

- **Requirement**：`api/agent.py` 仅改 import 边界（Previously: events/models/failure 内联于 `agent.py`）。
  - **Scenario**：`agent-import-only` — GIVEN 抽取 PR WHEN 跑必绿 pytest THEN 旧 Unified/Agent 路径 **无** 行为回归（FP-1）。

### REMOVED

- （无 — P0 不删 `ChatBIAgent.run` 逻辑。）

---

## 5. P0 单 Loop 硬约束（30 帽）

1. **一个 PR / 一条 task Loop** 完成 §2 五步；**不得** 拆成两个并行 Loop（除非 00 重开范围）。
2. **禁止夹带 P1**：不得在本 PR 实现完整 intent→tool 环、Graph SSE parity、clarify/plan 上图。
3. **D-2**：`unified_chat.py` 对外行为与默认路由 **零变更**（仅允许与本 task 无关的修复须单独说明）。
4. **旧路径回归**：抽取后 `ChatBIAgent` / Unified Chat 关键路径须与抽取前一致（pytest + 现有 contract 锚点）。
5. **Q-7 defer**：Intent 超时方案 A 的 SSE `ok` 字段语义 **不在本 Loop 冻结** → P1 Task-B（§10 已注明 defer）。

---

## 验收标准

> 对齐 Plan SPEC **§4A.3** Done 清单 + R1 建议（边表单测 + runner smoke）。

- [x] `agent.py` 行数明显下降；`FailureTypeHandler` 等已迁出；**旧 Unified 行为无回归**
- [x] `chatbi_events` / models / failure 可被 Graph 与 Agent **共用**
- [x] `ChatBIState` + 边表草案；Graph 侧 Intent 超时走 **方案 A**（legacy 边保留 v1 fallback）
- [x] Graph 路由 **已注册、可调用**（Q-8：`/api/py/unified/chat/graph` · `.../graph/stream`；stub 响应即可）；**不要求** 与旧 Agent parity
- [x] `_manifest` 登记新端点；`_contract_manifest` / `tech_graph_contract_check` **仍绿**（#106 修 `label` 后 main 绿）
- [x] 边表单测 + `api/graph/runner` smoke（`test_strategy: required` · 先测后实现 red-green）
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿（main · 2026-06-04 · 323 passed）
- [x] PR 上 **`pytest` workflow 全绿**（#106+#107 CI）
- [x] **未** 修改 `unified_chat.py` 行为；**未** 做 P1 clarify/plan 上图

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（见 `AGENTS.md`）。

---

## 失败路径

> 与 R1 审查 FP-1～4 对齐；**Scenario ID** 供 pytest / 后续 `_test_manifest` 互链。

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 | 测试（可选） |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | `fp-chatbi-p0-agent-regression` | 模块抽取后 import 循环、行为漂移、或既有 Agent/Unified pytest / contract 锚点失败 | CI pytest 或 `tech_graph_contract_check` 失败；PR **不可合并** | 是 | 无（本 Loop 前端 **否**） | 既有 Agent/Unified pytest |
| F2 | `fp-chatbi-p0-contract-manifest` | 新端点未登记 `_manifest`；锚点迁出后扫描不到；擅自新增 `graph.*` type 未登记 | `tech_graph_contract_check` 或图谱 CI 失败 | 是 | 无 | `tools/tech_graph_contract_check.py` |
| F3 | `fp-chatbi-p0-graph-stub-http` | 错误 path、未注册路由、鉴权与 Unified 不一致、handler 未捕获异常 | HTTP 4xx/5xx；stub 须 **结构化错误**（V2 惯例），**不得** 拖垮进程 | 5xx 可重试 | 仅联调打 Graph 端点时可见 | Graph 路由 smoke pytest |
| F4 | `fp-chatbi-p0-edge-table-unit` | `error_code` 未覆盖 V2 §2.4 主路径；legacy/graph 边表语义混用 | 单元测试失败；**禁止** 带红测合并 | 是 | 无 | 边表参数化 pytest |

---

## 8. 给执行帽（30）的必读列表

开干前须通读（顺序建议与实现顺序一致）：

1. 本 task §2～§5、`## 验收标准`、`## 失败路径`、`gates_before_code`。
2. [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) **§4A.2**（五步）、**§4A.3**（Done）、**§4A.4**（不做）。
3. [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) **§4.3**（D-1～D-5）。
4. [`SPEC-ChatBI-V2-Agent-Overview.md`](../spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md) **§2.4**（fallback · 边表覆盖）。
5. `api/agent.py` — 迁出块边界（计划 §4.4.1）。
6. `docs/harness/prompts/hats/30-execute-code.md` · **拒开工** 条件。
7. 22 审查：R1 [`task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md`](../harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md) · R2 [`task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md`](../harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md)。

**VERIFY（合并前）**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 9. 实现备忘（30 帽回填）

| 类别 | 路径 |
| --- | --- |
| 共享层 | `api/chatbi_events.py` · `api/chatbi_agent_models.py` · `api/chatbi_failure.py` |
| agent 瘦身 | `api/agent.py`（1078 行 · import 共享模块；契约锚点保留） |
| Graph | `api/graph/state.py` · `api/graph/runner.py` · `api/unified_chat_graph.py` |
| 路由 | `api/index.py`（Q-8 两路由） |
| manifest | `docs/_tech_graph/_manifest.json` |
| 契约扫描 | `tools/tech_graph_contract_check.py` 增 `chatbi_events.py` 源 |
| 测试 | `tests/test_chatbi_graph_p0_foundation.py` |

**30 验证摘要**：`pytest tests -m "not intent_eval and not intent_benchmark"` → **267 passed**；`tech_graph_manifest_check` OK；`tech_graph_contract_check` 仅剩 **frontend `label`**（分支基线既有，与 P0 无关）。`test_unified_chat_backend_v2_agent` 中 **v3 plan preview** 子集在本分支提交树上 **已红**（stash 对照同红，非本 PR 回归）。

### 自检结论（执行者）

**执行时间**：2026-06-03 · **分支**：`task/chatbi-graph-p0-foundation-v1` · **HEAD**：`b43ae3e` · **cwd**：仓根 `ai-ink-brain-api-python`

#### 命令与退出码

| 命令 | cwd | exit |
| --- | --- | ---: |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 仓根 | **1**（277 passed · **10 failed** · 1 skipped） |
| `pytest tests/test_chatbi_graph_p0_foundation.py -q` | 仓根 | **0**（10 passed） |
| `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` | 仓根 | **0**（OK） |
| `python tools/tech_graph_manifest_check.py` | 仓根 | **0**（OK） |
| `python tools/tech_graph_contract_check.py` | 仓根 | **1**（`contract.frontend_anchors` · 字段 `label` · 分支基线既有） |
| `wc -l api/agent.py` | — | **1078**（原 ~1342） |
| `git diff origin/main...HEAD -- api/unified_chat.py` | — | **0 行**（D-2 零变更） |

**pytest 失败摘要（10 · 均 `test_v3_*plan*`）**：`AssertionError: 'agent.plan.preview' not in events` 等；**非** `b43ae3e` 引入（`git diff b43ae3e^..b43ae3e` 未触 `unified_chat.py`）；本分支相对 `origin/main` 在 feat 前提交树上 **已红**（30 对照 stash 同结论）。**合并阻塞**：Required check 须全绿 → 须另 task/修复或确认 CI 策略后再 PR。

#### 验收表（40 · 对照 `## 验收标准`）

| 验收项 | 结果 | 证据 |
| --- | :---: | --- |
| `agent.py` 瘦身 + FailureTypeHandler 迁出 | **pass** | `wc -l` 1078；`api/chatbi_failure.py` 存在 |
| 共享模块 Graph/Agent 共用 | **pass** | `test_chatbi_shared_modules_importable` |
| `ChatBIState` + 边表 D-3 分表 | **pass** | `test_graph_intent_timeout_scheme_a` · `test_legacy_intent_timeout_v1_fallback` |
| Q-8 Graph 路由 stub 可调用 | **pass** | `test_graph_json_route_stub` · `test_graph_stream_route_stub` |
| `_manifest` + manifest check | **pass** | `tech_graph_manifest_check` OK；manifest 含 `/graph` 两路由 |
| `tech_graph_contract_check` 仍绿 | **fail** | exit 1 · `label`（基线 · 非 P0 新增） |
| 边表单测 + runner smoke | **pass** | `tests/test_chatbi_graph_p0_foundation.py` 10/10 |
| 必绿 pytest 全集（本地） | **fail** | 277/287 通过；10× v3 plan（见上） |
| PR pytest workflow | **未测** | 须 CI；本地全集未绿则 **不建议** 依赖 automerge |
| `unified_chat.py` 无行为变更 | **pass** | `git diff origin/main...HEAD -- api/unified_chat.py` 空 |
| 未做 P1 clarify/plan 上图 | **pass** | 无 `graph.*` SSE；runner 为 stub |

#### OpenSpec × TDD 三维（40 摘要）

| 维度 | 结果 | 备注 |
| --- | :---: | --- |
| Completeness | **pass** | P0 Scenario / F1～F4 有 `test_chatbi_graph_p0_foundation` 或全集子集证据 |
| Correctness | **pass-with-notes** | 边表 LLM_API_TIMEOUT：graph=`direct_answer` · legacy=`intent_v1_fallback` |
| Coherence | **pass-with-notes** | 与 Delta / §10 一致；contract `label` 为仓内已知红项 |

#### 已知未测 / 阻塞

- **50 帽**：`docs/tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_*.md`（关账前 **必须**）。
- **v3 plan preview 十测**：本分支 CI 合并风险；非 P0 diff 引入，但阻塞 `AGENTS.md` 必绿全集。
- **PR 线上 workflow**：未在本机执行 `gh`/Actions。

**40 结论**：P0 范围自检 **通过**；**全集 pytest 未绿** → 合并前须人决策（修 v3 / 拆 PR / 确认 CI 豁免策略）。

#### 关账补记（2026-06-04 · main 已合 #107）

| 项 | 结果 |
| --- | --- |
| 50 复检 | **pass-with-notes** · [`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`](../reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md) |
| 基线闸 | PR **#106** `task_chatbi_baseline_merge_gate_v1` · v3 plan 十测 + contract `label` |
| 合并 | PR **#107** `f53327a` |
| main pytest | **323 passed**（2026-06-04 本地复跑） |

**Harness 关账**：无新增 diary/RUNBOOK（P0 无生产运维步骤 · D-4 前端 **否**）。

---

## 10. SPEC 待确认清单（SDD §4 · 已冻结）

| # | 决策点 | 选定 | 备注 |
| --- | --- | --- | --- |
| **Q-8** | Graph 新路由 path | **A** · `POST /api/py/unified/chat/graph` + `POST /api/py/unified/chat/graph/stream` | P0 须冻结 · `_manifest` |
| **Q-7** | Intent 超时方案 A 的 SSE `ok` | **defer P1 Task-B** | P0 边表仅结构分表 |
| 3 | P0 是否新增 `graph.*` SSE | **A** · 不新增（D-5） | — |
| 4 | `ChatBIState` 物理路径 | **A** · `api/graph/state.py` | R1 NB-2 默认 |
| 5 | stub 响应最小契约 | **A** · HTTP 200 + 最小 JSON/SSE 心跳 | 与 FP-3 一致 |

**均已人确认 · 2026-06-03**（10 帽按 R1 建议选项 **A** 回填冻结；**Q-7** 除外 defer P1。`HG-TASK-DRAFT` / `HG-AUDIT-R1` 已于 **2026-06-03** 人签 `approved`。）

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-03 | 10 需求帽：Task-P0 草案 · invoke `invoke_20260603_10_requirements.md` |
| 2026-06-03 | **按审查 R1 回填**（`task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md`）：B-2 §10 冻结 · B-3 `## 验收标准`/`## 失败路径` · B-4 Delta · validate 对齐；B-1 待人签闸 |
| 2026-06-03 | 人签 `HG-TASK-DRAFT` · `HG-AUDIT-R1` → `approved`（R2 后 · 单独 commit） |
| 2026-06-03 | 30 实现 `b43ae3e` · 40 自检回填 `### 自检结论（执行者）` |
| 2026-06-03 | 50 复检 · [`reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md`](../reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md) |
| 2026-06-04 | PR #106+#107 合 main · Harness 关账 · `git mv` → `done/` |

**下一棒**：**P1 Task-B**（Graph MVP · intent→tool 环）— 见 [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) §10.2。
