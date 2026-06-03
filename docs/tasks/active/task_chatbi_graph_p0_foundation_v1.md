# Task：ChatBI Graph P0 地基 — 共享层抽取 + State/边表草案 + 骨架路由（单 Loop）

> **状态**：`active`（10 需求帽草案 · SDD 轮 2 待确认清零）  
> **Task-P0**：对齐 [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) **§4A** · **§10 Task-P0**  
> **冻结决策**：[`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) **§4.3**（D-1～D-5）  
> **关联图谱**：`docs/_tech_graph/00_main.ai.md`（增量指针）；待建 `10_flow_agent_graph.ai.md`（30 帽落盘）

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
| **gates_before_code** | `failure_paths` 三节可操作 · 验收 `- [ ]` 与 §4A.3 对齐 · **SPEC 待确认清单 Q-8 已人确认** · 必读列表已读 · `HG-TASK-DRAFT` = `approved` · 若走路径 A：`HG-AUDIT-R1` = `approved` |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **推荐路径** | **A（22 R1）** — `test_strategy: required` + 新路由 + 待确认项未清零 |
| **worktree_root** | （非并行时与 Open Folder 同仓根；并行时 invoke 另填） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | pending | 22-R1, 30 | 10 帽 task 草案 · 待人扫或明示「方向对」 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 书面审查通过后改 `approved` |

---

## 1. 背景与目标

ChatBI V2 `ChatBIAgent.run` 与 Unified Chat 编排堆叠在 `api/agent.py`（约 1342 行），控制流与 SSE/失败路由耦合，难以单测与演进。冻结决策 **D-1～D-5** 已选定 **自研 StateGraph**、**并行 Graph 新路由**、**不改** 现有 `unified_chat.py` 行为。

**本 task 完成态（一句话）**：在旧 Unified/Agent **行为不变** 前提下，抽出 `chatbi_events` / `chatbi_agent_models` / `chatbi_failure`；落地 `ChatBIState` 与 **legacy/graph 分表** 边表草案；注册 Graph **骨架** HTTP 路由（stub 可调用）；`pytest tests -m "not intent_eval and not intent_benchmark"` 全绿；`_manifest` / `tech_graph_contract_check` 仍绿。

**Harness 管控**：本 Loop = **P0 单 Loop**（合并原 Task-A + Task-A′）；**00/10 收口** scope 与 Done；**禁止** 夹带 P1 完整 intent→tool parity（见 §5）。

---

## 2. 范围

对齐计划 SPEC **§4A.2** 五步（30 帽须按序交付，可在同一 PR 内完成）：

| 步 | 交付 | 要点 |
| ---: | --- | --- |
| ① | **agent 抽模块** | `chatbi_events.py` · `chatbi_agent_models.py` · `chatbi_failure.py`；`agent.py` 改 import；`run()` 逻辑 **不删不改语义** |
| ② | **State + 边表草案** | `ChatBIState`；`failure_edges_legacy()` / `failure_edges_graph()`（Graph Intent 超时 **方案 A**，legacy 保留 v1 fallback，D-3） |
| ③ | **最小 runner** | `api/graph/runner.py`（stub 节点，**非** 完整 ReAct） |
| ④ | **骨架路由** | `unified_chat_graph.py`（或等价薄 handler）+ `index` 注册 + `_manifest` 登记 **Q-8 定名** 端点 |
| ⑤ | **单测** | 边表参数化 + runner smoke；必绿 pytest 集全绿 |

**契约 / 图谱（本 Loop 内）**：

- 更新 `docs/_tech_graph/_manifest.json`（或仓内 manifest 真值路径）登记新端点。
- `_CONTRACT_ANCHOR_*` 迁出后须仍可被 `tech_graph_contract_check` 扫描（re-export 或更新扫描路径）。
- **D-5**：P0 **可不** 新增 `graph.*` SSE type；若新增须登记 `_contract_manifest` 且 CI 绿。

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
| D-1～D-5 冻结 | [`docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3 |
| LangChain 背景（低优先模式） | [`docs/spec/research/SPEC-Research-SelfChain-vs-LangChain-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangChain-v1_zh.md) |
| V2 fallback 对照 | [`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`](../spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md) §2.4 |
| 抽模块锚点 | `api/agent.py` |
| 环境 / 目录 | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| SDD 三轮纪律 | [`docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) |
| Harness 字段 | [`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5 |
| 合并前必绿 | `pytest tests -m "not intent_eval and not intent_benchmark"` |

---

## 5. P0 单 Loop 硬约束（30 帽）

1. **一个 PR / 一条 task Loop** 完成 §2 五步；**不得** 拆成两个并行 Loop（除非 00 重开范围）。
2. **禁止夹带 P1**：不得在本 PR 实现完整 intent→tool 环、Graph SSE parity、clarify/plan 上图。
3. **D-2**：`unified_chat.py` 对外行为与默认路由 **零变更**（仅允许与本 task 无关的修复须单独说明）。
4. **旧路径回归**：抽取后 `ChatBIAgent` / Unified Chat 关键路径须与抽取前一致（pytest + 现有 contract 锚点）。
5. **Q-7 defer**：Intent 超时方案 A 的 SSE `ok` 字段语义 **不在本 Loop 冻结** → P1 Task-B（见文末待确认清单）。

---

## 6. 验收标准（§4A.3 Done 清单）

- [ ] `agent.py` 行数明显下降；`FailureTypeHandler` 等已迁出；**旧 Unified 行为无回归**
- [ ] `chatbi_events` / models / failure 可被 Graph 与 Agent **共用**
- [ ] `ChatBIState` + 边表草案；Graph 侧 Intent 超时走 **方案 A**（legacy 边保留 v1 fallback）
- [ ] Graph 路由 **已注册、可调用**（stub 响应即可）；**不要求** 与旧 Agent parity
- [ ] `_manifest` 登记新端点；`_contract_manifest` / `tech_graph_contract_check` **仍绿**
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [ ] **未** 修改 `unified_chat.py` 行为；**未** 做 P1 clarify/plan 上图

---

## 7. failure_paths

### FP-1 · 旧 Agent / Unified 回归失败

| 项 | 内容 |
| --- | --- |
| **触发** | 模块抽取后 import 循环、行为漂移、或既有 Agent/Unified pytest / contract 锚点失败 |
| **系统行为** | CI pytest 或 `tech_graph_contract_check` 失败；PR **不可合并** |
| **可重试** | 是（修复抽取边界或恢复 re-export，**禁止** 在 Unified 路径塞 Graph 逻辑） |
| **用户可见** | 无（本 Loop 前端 **否**）；运维见 CI 红 |

### FP-2 · contract / manifest check 失败

| 项 | 内容 |
| --- | --- |
| **触发** | 新端点未登记 `_manifest`；`_CONTRACT_ANCHOR_*` 迁出后扫描不到；擅自新增 `graph.*` type 未登记 |
| **系统行为** | `tech_graph_contract_check` 或图谱 CI 失败 |
| **可重试** | 是（补 manifest / re-export 锚点 / 登记 contract） |
| **用户可见** | 无 |

### FP-3 · Graph stub 路由 4xx / 5xx

| 项 | 内容 |
| --- | --- |
| **触发** | 错误 path（Q-8 未对齐）、未注册路由、鉴权与 Unified 不一致、handler 未捕获异常 |
| **系统行为** | HTTP 4xx（路由/校验）或 5xx（未处理异常）；stub 宜返回 **结构化错误**（与 V2 错误处理惯例一致），**不得** 拖垮进程 |
| **可重试** | 客户端可重试（5xx）；4xx 须修请求或配置 |
| **用户可见** | 仅 **联调** 直接打 Graph 端点时可见；生产访客默认仍走旧 Unified（D-4） |

### FP-4 · 边表 / State 单测失败

| 项 | 内容 |
| --- | --- |
| **触发** | `error_code` 未覆盖 V2 §2.4 主路径；legacy/graph 边表语义混用 |
| **系统行为** | 单元测试失败；**禁止** 带红测合并 |
| **可重试** | 是（修正边表分函数） |
| **用户可见** | 无 |

---

## 8. 给执行帽（30）的必读列表

开干前须通读（顺序建议与实现顺序一致）：

1. 本 task §2～§6、§5 硬约束、`gates_before_code`。
2. [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) **§4A.2**（五步顺序）、**§4A.3**（Done）、**§4.4**（不做）。
3. [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](../spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) **§4.3**（D-1～D-5）。
4. [`SPEC-ChatBI-V2-Agent-Overview.md`](../spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md) **§2.4**（fallback 对照 · 边表覆盖参考）。
5. `api/agent.py` — 迁出块边界（计划 §4.4.1 表）。
6. `docs/harness/prompts/hats/30-execute-code.md` · **拒开工** 条件。
7. 若存在 22 审查：`docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_*.md`。

**VERIFY（合并前）**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 9. 实现备忘（30 帽回填）

- （待 30 填写：文件列表、manifest 节点、contract 锚点迁移说明）

### 自检结论（执行者）

- （待 40 帽回填）

---

## 10. SPEC 待确认清单（SDD §4 · 轮 2）

> **未确认前**：30 帽 **拒开工**（仅输出缺口）。**Q-8 清零** 或人明示「方向对」后，方可进入 22→30 链。

| # | 决策点 | 建议选项 | 待谁确认 | 备注 |
| --- | --- | --- | --- | --- |
| **Q-8** | Graph 新路由最终 path 命名 | **A**：`POST /api/py/unified/chat/graph` + `POST /api/py/unified/chat/graph/stream`（与计划 §5.5 一致） · **B**：其他前缀（须在 task 修订记录写明） | 人 | **P0 须冻结** · `_manifest` 依赖 |
| **Q-7** | Intent 超时方案 A 的 SSE `ok`：`true` 降级答 vs `false` 硬失败 | （不在 P0 拍板） | 人 · **P1 Task-B** | **defer** 至 P1；P0 边表仅实现 D-3 结构分表 |
| 3 | P0 是否新增 `graph.*` SSE type | **A**：不新增（默认，D-5） · **B**：新增并登记 contract | 人 | 选 B 则 FP-2 必过 contract CI |
| 4 | `ChatBIState` 物理路径 | **A**：`api/graph/state.py` · **B**：`api/chatbi_state.py` | 人 · 30 可据 A 默认实施 | 非阻塞 manifest |
| 5 | stub 响应最小契约 | **A**：HTTP 200 + 最小 JSON/SSE 心跳 · **B**：501 Not Implemented | 人 | 须与 FP-3 一致且可 pytest |

**均已人确认 · YYYY-MM-DD**：（待填写）

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-03 | 10 需求帽：Task-P0 草案 · invoke `invoke_20260603_10_requirements.md` |
