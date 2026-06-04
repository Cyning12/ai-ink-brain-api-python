# NOTE — 技术图谱 · import 绑定类回归与 AST backlog 边界（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` — **留证与方案占位**；**当前不立项、不扩 CI** |
| **freeze_id** | `GOV-NOTE-TG-IMPORT-BINDING@2026-06-04` |
| **关联 SPEC** | [`SPEC-Governance-TechGraph-Anchor-SQLGate-Backlog-v1_zh.md`](./SPEC-Governance-TechGraph-Anchor-SQLGate-Backlog-v1_zh.md)（TG-AST-03 / 06 / 07 / **09**） |
| **关联 task** | [`task_chatbi_intent_hints_step1_v1.md`](../../tasks/done/task_chatbi_intent_hints_step1_v1.md) · 失败路径 **F6** `FP-AGENT-LATENCY-V1-FALLBACK` |
| **触发事件** | 2026-06-04 RUNBOOK Q4 人验：`decide_intent_v1 is not defined`（`f53327a` Graph P0 重构删 import 留调用） |

---

## 1. 问题摘要

| 项 | 内容 |
| --- | --- |
| **表象** | Unified Agent 在 intent 慢于 `AGENT_MAX_LATENCY_MS` 时进入软超时降级，调用 `decide_intent_v1` → `NameError` |
| **根因** | `api/agent.py` 调用点保留，`from .intent_router import decide_intent as decide_intent_v1` 在 refactor 中被删 |
| **为何 CI 未拦** | 主路径 intent 快，不触发超时分支；298 pytest 全绿仍可能漏 |
| **即时修复** | 恢复 import + 分支单测 + `_test_manifest` 条目 F6 |

---

## 2. 图谱（当前 L0）能否避免？

**不能单独避免。** 现有 `_tech_graph` 建模的是 **运行时流程与锚点**，不是 Python **模块 import 绑定**。

| 图谱能力 | 对本 bug |
| --- | --- |
| Mermaid 流程 / `graph_query` | 可表达「超时 → V1 路由」，**不验** `agent.py` 是否 import |
| TG-AST-03（锚点符号存在） | 可证 `intent_router.decide_intent` **存在**，**不证** 调用方已绑定 |
| TG-AST-06/07（Agent/Intent 节点） | 降低 refactor 遗漏概率，**非硬闸** |
| 全仓 import AST（`graph.auto.json`） | **能**，但 backlog **已拒**（见 Anchor-SQLGate SPEC §1） |

---

## 3. 与 AST backlog 的关联（后续再议）

| backlog ID | 与本事件关系 | **当前决策** |
| --- | --- | --- |
| **TG-AST-06** | 应在 Agent 子图显式画出「软超时 → V1 fallback」 | 待抽空；**不阻塞** Intent Hints Step1 |
| **TG-AST-07** | Intent V2 与 V1 降级并存，避免图谱仍只写 V1 router | 同上 |
| **TG-AST-09** | **唯一可能接近「import 绑定校验」的图谱向方案**：P0 白名单 + 文件内「调用点 ↔ import」轻量交叉；**禁止全仓 AST** | **占位**；实现前须单独立项 task，规则范围另审 |
| Ruff F821 / Pyright | **非图谱**；对 `NameError` 类最直接 | **不在本 NOTE 范围扩 CI**（后续 governance task 可选） |

**TG-AST-09 若立项时的设计草图（非承诺）**：

1. P0 节点：`AgentSoftTimeout` → `api/agent.py#L602` · `intent_router::decide_intent`
2. 规则：锚点文件内出现 `decide_intent_v1(` ⇒ 同文件须有对应 `import`
3. 与 `_test_manifest` 交叉：`FP-AGENT-LATENCY-V1-FALLBACK` 缺测则 CI 红

---

## 4. 当前已落地的 Verify（不等待 AST）

| 层 | 交付 |
| --- | --- |
| 代码 | `api/agent.py` 恢复 `decide_intent_v1` import |
| pytest | `test_agent_decide_intent_v1_import_bound` · `test_v2_agent_latency_exceeded_v1_fallback_rag` |
| L2 manifest | `FP-AGENT-LATENCY-V1-FALLBACK` · task F6 |

---

## 5. 非范围（本 NOTE）

- 立即实现 TG-AST-09 或全仓 AST
- 修改 Intent Hints Step1 产品行为
- 替代 Harness 50 / RUNBOOK 人验

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 初稿：Q4 回归留证 · 与 AST backlog 边界 · 当前仅测试/manifest 收口 |
