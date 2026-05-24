# Task：ChatBI V3 P2-1 高可用拆单（限流 / 熔断 / health）

> **状态**：draft  
> **关联图谱**：`docs/_tech_graph/00_main.md`（顶层 HTTP 入口）、`docs/_tech_graph/99_spec.md`（Env / 工程规约）  
> **关联 Issue/PR**：待补  
> **前端依赖**：无（P2-1 后端 middleware / 端点；BFF 探活对齐另开 task）

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/` 并更新 `docs/tasks/_views/done.md`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../../harness/HARNESS_V2_PLAN.md) **§5**；半自动：[`docs/harness/prompts/HANDOFF_SEMI_AUTO.md`](../../harness/prompts/HANDOFF_SEMI_AUTO.md)。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 本 task **仅拆单与规格/task 落盘**，不写 `api/` 实现；实现子 task 须另设 `test_strategy: required`。 |
| **freeze_id** | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` + `main@7bb8a0b` |
| **gates_before_code** | `["human_gate", "failure_paths", "验收标准", "必读列表"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/chatbi-v3-p2-resilience-spec` |
| **执行模式** | **单闸关账试验**：kickoff 人签 `HG-TASK-DRAFT` + 预批 `HG-AUDIT-R1`；链式 20→22?→30→40→50；**仅** `HG-REINSPECT` 关账前人签 |
| **推荐路径（10 帽）** | **B（30）** — 本 task 已起草；22 可选零阻塞落盘，不挡 30 |

### 人工闸 `human_gate`

> **仅人** 可将 `pending` → `approved`；Agent **禁止**代填（`HG-AUDIT-R1` 由人在 kickoff **预批**）。

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1, 30 | **人扫本 task 初稿**后改 `approved` 再开 30 |
| HG-AUDIT-R1 | approved | 30 | 全自动试验：允许跳过 22 或 22 仅零阻塞 record |
| HG-REINSPECT | pending | done | 50 复检 + PR 前人签 |

---

## 背景与目标

`RECENT_TASK_SCHEDULE` §2 当前棒为 **P2-1**；V3 总规 [`SPEC-ChatBI-V3-Overview.md`](../../spec/v3-agent/SPEC-ChatBI-V3-Overview.md) **§2.1 P2-1** 要求：**限流熔断 + `/health` 契约**。子规 [`SPEC-ChatBI-V3-Resilience-Ops.md`](../../spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md) 已 draft。

**本 task 完成态**（拆单 PR，非实现 PR）：

1. 审计现网：`/api/py/health`（`api/index.py`）与 Unified Chat 高消耗路径。  
2. 产出 **可执行 implementation 拆单**（建议 2～3 个子 task 或分 PR 里程碑）。  
3. 每个子项含：范围 / 非范围 / failure_paths / 验收 / env / `test_strategy`。  
4. 更新 `SPEC-ChatBI-V3-Overview.md` **§3 任务归拢** 一行索引（若尚无 P2-1 行）。  
5. 本 task 验收通过后归档；**实现**在 follow-up task（如 `task_chatbi_v3_p2_resilience_health_ready_v1` 等）中 `test_strategy: required`。

---

## 范围

- [ ] 阅读并对齐 `SPEC-ChatBI-V3-Resilience-Ops.md` §2–§4 与 `PROJECT_CONFIG` 现有 env 习惯。  
- [ ] 现状差距表：`/api/py/health` vs 子规建议的 `/health|/live` + `/ready` + 429/熔断。  
- [ ] 拆单方案（写入本节 **§实现拆单（10/30 回填）**）：  
  - **建议 P2-1a**：health / ready 契约与 JSON 字段  
  - **建议 P2-1b**：限流（IP 或 API Key；优先 unified chat / chat）  
  - **建议 P2-1c**：外呼熔断（LLM、Supabase）与可观测钩子  
- [ ] 为每个子项起草 **`docs/tasks/active/task_chatbi_v3_p2_resilience_*_v1.md` 草案**（或单文件 §附录子 task 全文，二选一须在拆单结论中说明）。  
- [ ] 更新 Overview **§3** 任务表：P2-1 母单 + 子 task 链接。  
- [ ] 本 task：`failure_paths`、验收标准、Harness 字段齐全。

## 非范围

- **本 PR 不写** `api/` 业务实现、middleware 代码、新 pytest（实现 task 负责）。  
- 不修改 CI workflow（实现 task 可能改）。  
- 不做 Ink 前端 BFF 探活（另开跨仓 task）。  
- 不合并 P2-2 评估烟测集（P2-2 独立）。  
- 不启动 P2 延伸低置信 §5.1 backlog。

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| 排期 | [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §2、§5 |
| V3 总规 P2-1 | [`SPEC-ChatBI-V3-Overview.md`](../../spec/v3-agent/SPEC-ChatBI-V3-Overview.md) §2.1、§3 |
| 韧性子规 | [`SPEC-ChatBI-V3-Resilience-Ops.md`](../../spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md) |
| 项目配置 | [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| 现网 health | `api/index.py` `/api/py/health` |
| Unified Chat | `api/unified_chat.py`（高消耗路径参考） |
| Harness skills | [`skills/README.md`](../skills/README.md) · `docs-governance` / 实现子单用 `api-endpoint` |
| 规划入口 | [`task_chatbi_v3_planning_after_resume_v1.md`](task_chatbi_v3_planning_after_resume_v1.md) |

---

## 失败路径

| # | 触发条件 | 系统行为（可观测） | 可重试 | 用户可见类型 |
|---|----------|---------------------|--------|--------------|
| F1 | 执行帽未阅读 `SPEC-ChatBI-V3-Resilience-Ops.md` / `Overview §2.1` 即开工 | 30 帽按拒开工规则停止，仅输出阻塞清单（缺失必读项 + 路径） | 是（补读后重启） | Agent 阻塞说明 |
| F2 | 本 task PR 出现 `api/` 业务实现或 CI workflow 代码 diff | 视为越界；剔除越界文件后重跑验证，未清理前不得进入 40/50 | 是 | PR review 阻塞 |
| F3 | 任一子 task 缺少 `test_strategy: required`、可执行验收命令或 `failure_paths` | 40/50 标记 fail；`HG-REINSPECT` 保持 pending | 是（补齐文档后复检） | `reinspect_results` 失败项 |
| F4 | `SPEC-ChatBI-V3-Overview.md` §3 未同步新增 P2-1 母单/子单索引，或路径失配 | 视为验收未通过；不得归档 `done/` | 是（修正文档后重检） | 验收清单 fail |
| F5 | 子 task 验收只写“应支持”但无法用命令断言（无 curl/pytest 断言点） | 22/40 退回需求帽补强验收可执行性 | 是 | 审查结论 non-pass |

---

## 验收标准

- [ ] **§实现拆单** 含 3 个可独立 PR 子项（P2-1a/b/c），且各自具备可执行验收（命令 + 期望断言）。  
- [ ] 每个子项明确 **env / 端点 / 非范围 / test_strategy(required) / failure_paths**。  
- [ ] 现状差距表引用真实代码路径（如 `api/index.py` health）。  
- [ ] `SPEC-ChatBI-V3-Overview.md` §3 已增 P2-1 母单/子单索引行，并与本 task 子单命名一致。  
- [ ] 本 task 无 `api/` 代码 diff（或仅注释级若 task 允许 — **默认不允许**）。  
- [ ] `docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_resilience_*` 50 帽落盘（semi_auto 关账）。  

**合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"`（纯 docs 亦须绿）。

---

## 实现拆单（10/30 回填）

> 10 帽先给可执行版草案，30 帽据现网与审查结论定稿。

| 子 ID | 建议 task 文件 | 范围摘要 | 必须落盘字段 | 可执行验收（最小） | test_strategy | PR 顺序 |
|-------|----------------|----------|--------------|--------------------|---------------|---------|
| P2-1a | `task_chatbi_v3_p2_resilience_health_ready_v1.md` | `/live` + `/ready` 契约；ready 失败返回 503 + 组件名 | 端点契约、env、failure_paths、非范围 | `curl -sS /api/py/health`（现状对照）+ `curl -sS /api/py/live` 返回 200；`curl -sS /api/py/ready` 在依赖缺失场景返回 503 且 JSON 含 `components[]` | `required` | 1 |
| P2-1b | `task_chatbi_v3_p2_resilience_rate_limit_v1.md` | `/api/py/unified/chat/stream`、`/api/py/chat` 限流；429 结构化 | 限流粒度、阈值 env、429 body、failure_paths | `hey`/并发压测触发 429；响应 JSON 至少含 `error_code`，可选 `retry_after`；阈值可通过 env 调整并复测 | `required` | 2 |
| P2-1c | `task_chatbi_v3_p2_resilience_circuit_breaker_v1.md` | LLM/Supabase 外呼熔断（open/half-open/closed 可观测） | 熔断状态机语义、降级策略、日志字段、failure_paths | 人工注入外呼失败后返回结构化错误（不吞错）；日志含熔断状态迁移；恢复窗口后可半开探测成功 | `required` | 3 |

### 子 task 验收清单（P2-1a/b/c 可执行化）

- [ ] **P2-1a**：task 正文包含至少 2 条命令级断言（`/live` 200、`/ready` 503 场景）与 JSON 字段断言示例。
- [ ] **P2-1b**：task 正文包含 429 触发脚本（或 pytest 压测桩）与阈值 env 配置示例，明确默认值与边界值。
- [ ] **P2-1c**：task 正文包含“依赖故障注入 -> 熔断打开 -> 恢复半开”的三段验证步骤和日志断言键名。
- [ ] 三个子 task 均声明 `test_strategy: required`，并给出“先失败后通过”的最小测试策略说明。
- [ ] 三个子 task 均声明各自非范围，避免跨单耦合（例如 P2-1a 不实现限流，P2-1b 不改熔断状态机）。

### Overview §3 变更点（执行帽需完成）

- [ ] 在 `docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` §3 新增或更新 P2-1 索引行，至少包含：
  - 母单：`docs/tasks/active/task_chatbi_v3_p2_resilience_v1.md`
  - 子单：`task_chatbi_v3_p2_resilience_health_ready_v1.md` / `task_chatbi_v3_p2_resilience_rate_limit_v1.md` / `task_chatbi_v3_p2_resilience_circuit_breaker_v1.md`
- [ ] Overview §3 的“元状态”与子 task 文首状态一致（`todo`/`backlog` 等），并在职责摘要写清 1a/1b/1c 边界。
- [ ] 若子 task 命名调整，需同步回填本 task 与 Overview §3，确保两处路径一致。

---

## 给执行帽的必读列表

1. 本文件全文  
2. `docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md`  
3. `docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` §2.1、§3  
4. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（env 表）  
5. `api/index.py`（health 现状）  
6. `docs/tasks/RECENT_TASK_SCHEDULE.md`  
7. `docs/harness/prompts/HANDOFF_SEMI_AUTO.md`（semi_auto + 单闸关账）  

---

## 给执行帽的执行顺序（硬）

1. 差距表 + 拆单定稿（§实现拆单 + 子 task 草案文件）。  
2. 更新 Overview §3 索引。  
3. 40 自检 → 50 复检 → 待人签 `HG-REINSPECT` → done 归档。  

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | （待 30 帽回填） |
| 子 task 路径 | （待 30 帽回填） |
| 图谱变更点 | 实现阶段再动 `_tech_graph/` |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | |
| 结论 | |
| 要点 | |

---

## 给 Cursor

`task_chatbi_v3_p2_resilience_v1`、`P2-1`、`Resilience`、`拆单`、`semi_auto`、`HG-REINSPECT`、`RECENT_TASK_SCHEDULE`
