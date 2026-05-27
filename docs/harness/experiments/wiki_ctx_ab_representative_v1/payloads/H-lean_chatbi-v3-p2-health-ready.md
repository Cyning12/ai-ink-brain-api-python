# Payload · H-lean（Representative 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `chatbi-v3-p2-health-ready` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **generated** | 2026-05-27 · `python tools/wiki_ctx_ab_materialize_h_lean.py` |

## Agent 约束

只能依据下文作答。禁止 invoke/review 全文。禁止 `docs/coding_wiki/*`。

---

## 载荷正文

--- FILE: docs/harness/README.md ---
## 1. 日常读什么

| 场景 | 路径 |
|------|------|
| 写 task / **下一棒双 Prompt** | `TEMPLATE-requirements`（**A:22** + **B:30**，人择一） |
| 任务审核 22 | [`reviews/README.md`](reviews/README.md) → `TEMPLATE-task-audit` |
| 执行 + 自检 | `TEMPLATE-execute` → `TEMPLATE-self-check` |
| **三方复检** | `TEMPLATE-independent-reinspect` → [`../tasks/reinspect_results/`](../tasks/reinspect_results/README.md) |
| 半自动 / 人工闸 | `HANDOFF_SEMI_AUTO` |
| commit / 关账 | `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE` |
| task 字段 | `HARNESS_V2_PLAN.md` §5 |
| 流程 | `SDD_HAT_FLOW.md` |
| 新 invoke | `invokes/` |
| **Harness 裁决共识（已接受）** | [`../diary/2026-05-22-harness-evaluation-improvement-response.md`](../diary/2026-05-22-harness-evaluation-improvement-response.md) **§九** |

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc`、`.cursor/rules/06-harness-in-repo.mdc`。

**Agent 禁止（日常）**：

- **禁止** 默认读取工作区 `Projects/docs/harness/`（跨子仓 Harness 任务除外，见 `docs/tasks/README.md`）。
- **禁止** 将子仓 `prompts/` 软链到工作区；真值以 **本仓** `docs/harness/prompts/` 为准。
- **禁止** 在任务执行中运行下文 **§4 `rsync`**（仅维护者偶发同步）。

---

### 2.1 落盘 taxonomy（**已迁移** · 2026-05-25）

**原则**：**按 task 绑定**落盘（`invokes` / `reviews` / `reinspect_results` 已按 task 语义）；**不按业务域分顶层目录**。域知识进 **LLM Wiki**（`task_coding_wiki_pilot_v1`），不进 `prompts/domains/`。

| 树 | 目标路径 | 内容 |
|----|----------|------|
| **prompts** | `prompts/hats/` | `10-requirements` … `50-independent-reinspect` |
| | `prompts/templates/` | `TEMPLATE-*-invoke.md` |
| | `prompts/handoff/` | `HANDOFF_*.md` |
| **invokes** | `invokes/by-task/<task_slug>/` | `invoke_YYYYMMDD_<帽号>_<slug>.md`（见 [`invokes/README.md`](invokes/README.md)） |
| **reviews** | `reviews/by-task/<task_slug>/` | `task_<slug>_audit_R<轮次>_YYYYMMDD.md`（见 [`reviews/README.md`](reviews/README.md)） |
| **50（不变）** | `docs/tasks/reinspect_results/` | 关账复检；文件名可含 task slug |

**为何不建 `prompts/domains/chatbi` 或 `domains/tech-graph`？**

- Harness 文件描述的是**帽序与 HANDOFF 协议**，与「ChatBI / 图谱」等业务域 **正交**；同一 task 常跨多域。
- 按域拆目录会导致：同一 `invoke` 难归类、Agent 误把域片段当关账真值。
- **若将来**需要跨 task 复用的 Prompt **片段**，再用 `prompts/snippets/<domain>/`（可选），与 Wiki 词条分工，**仍不**替代 `by-task/` 落盘。

**新落盘**：invoke / review **必须**进 `by-task/<task_slug>/`；prompts 从 `hats/`、`templates/`、`handoff/` 读取（勿在 `prompts/` 根新增帽文件）。

**落地 task**：[`docs/tasks/active/task_coding_wiki_pilot_v1.md`](../tasks/active/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../tasks/active/task_wiki_ctx_ab_v1.md)（Wiki-CTX-AB）。

**实验（P1 题集 / payload 模板）**：[`experiments/wiki_ctx_ab_v1/`](experiments/wiki_ctx_ab_v1/README.md) · SPEC [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)。

---

--- FILE: docs/harness/invokes/README.md ---
## 命名

`invoke_YYYYMMDD_<帽号>_<slug>.md`（例：`invoke_20260525_30_chatbi-v3-p2-1a-health.md`）

## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。
## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。

## 规则（摘要）

1. **同一帽**多轮追问 **不** 重复落盘；换帽才新建文件。

--- FILE: docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md ---
# Task：ChatBI V3 P2-1a 健康探针契约（/live + /ready）

> **状态**：done（2026-05-25 验收通过 · 人签合并前关账）  
> **关联母单**：`docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`  
> **关联 SPEC**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md` §4

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| test_strategy | `required` |
| freeze_id | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| gates_before_code | `["failure_paths","验收标准","必读列表"]` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| git_branch | `task/chatbi-v3-p2-1a-health` |

---

## 背景与目标

将现有轻量 `/api/py/health` 探针扩展为分层契约：`/live` 仅反映进程存活，`/ready` 反映依赖就绪，确保平台编排能区分“活着但暂不可服务”。

## 范围

- 新增或明确 `/api/py/live` 与 `/api/py/ready` 契约（状态码 + JSON 字段）。
- `ready` 检测关键依赖（至少 Supabase 配置与外部依赖初始化状态）。
- 失败时返回 `503`，JSON 含 `components[]` 和失败原因摘要。

## 非范围

- 不改限流算法（P2-1b）。
- 不改熔断状态机（P2-1c）。
- 不引入前端 BFF 探活改造。

---

## 失败路径

| # | 触发条件 | 系统行为（可观测） | 可重试 | 用户可见类型 |
|---|----------|---------------------|--------|--------------|
| F1 | 依赖未就绪（如 Supabase 配置缺失） | `/ready` 返回 `503`，`components` 标记 failed | 是 | JSON 错误响应 |
| F2 | 探针端点实现与文档不一致 | 40/50 自检 fail，不允许关账 | 是 | 复检阻塞 |
| F3 | `/live` 包含重依赖外呼导致抖动 | 视为契约违背，回退为轻量探活 | 是 | 审查阻塞 |

---

## 验收标准

- [x] `curl -sS http://127.0.0.1:8000/api/py/live` 返回 `200` 且 JSON 含 `ok=true`（或等价布尔）。
- [x] 依赖故障注入场景下，`curl -i -sS http://127.0.0.1:8000/api/py/ready` 返回 `503`，body 含 `components` 数组。
- [x] 文档与实现保持一致：`PROJECT_CONFIG` 或 task 中记录端点字段说明。
- [x] pytest 覆盖最小 happy path + dependency-down path。

---

## 给执行帽的必读列表

1. 本 task 全文  
2. `docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`  
3. `docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md`  
4. `api/index.py`（现有 `/api/py/health`）

---

## 自检结论（执行者）

| 项 | 结果 |
|----|------|
| 命令 1 | `pytest tests/test_health_probe_routes.py` |
| 结论 1 | `exit_code=0`；`2 passed`（覆盖 `/api/py/live` 200 与 `/api/py/ready` 503 注入场景） |
| 命令 2 | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| 结论 2 | `exit_code=0`；`210 passed, 1 skipped, 2 deselected` |
| 证据归因 | 通过 pytest 的接口断言等价覆盖验收中两条 curl 场景（状态码 + JSON 字段） |

---

## 复检结论（50 · 独立复检）

| 项 | 结果 |
|----|------|
| 复检报告 | [`docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_1a_health_ready_20260525_v1.md`](../reinspect_results/reinspect_chatbi_v3_p2_1a_health_ready_20260525_v1.md) |
| 结论 | **pass（建议合并）** |
| 复检基线 | `4dae83c`（实现）+ `d06fe8b`（50 invoke） |
| 独立重跑 | `pytest tests/test_health_probe_routes.py` → `2 passed`；全量门禁 → `210 passed, 1 skipped, 2 deselected` |
| 关账状态 | 已归档 `docs/tasks/done/`；待 **PR 合并 `main` + CI 绿** |

---

## 实现备忘（30/50 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/index.py`；`tests/test_health_probe_routes.py`；`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`；`docs/_tech_graph/_manifest.json` |
| 端点 | `GET /api/py/live`、`GET /api/py/ready`；`GET /api/py/health` 与 live 语义对齐 |
| 图谱 | `_manifest.json` 已登记 live/ready handler |

--- FILE: docs/tasks/RECENT_TASK_SCHEDULE.md ---
> **范围**：`ai-ink-brain-api-python` · `docs/tasks/` · `docs/harness/` · `docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` §2.1 · **治理线** [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)  
> **V3 韧性**：P2-1a **done**（PR #52）；P2-1b/c **排队** — 属 ChatBI 实现子单，**与 Harness 改进无关**，**非**本表默认「当前棒」。
| **done/**             | **55+** 个 `.md`（含 P2-1a，[PR #52](https://github.com/Cyning12/ai-ink-brain-api-python/pull/52)） |
| **_views/done.md**    | 已含 P2-1a 索引行                                                                                   |
| **V3 P2-1 韧性** | P2-1a **done**（PR #52）；P2-1b/c **排队**（非 Harness、非默认当前棒） |
| 0b    | `task_chatbi_v3_p2_resilience_rate_limit_v1.md` | `todo` | P2-1b 限流 | **V3 排队** · 非 Harness 近期 |
| 0c    | `task_chatbi_v3_p2_resilience_circuit_breaker_v1.md` | `todo` | P2-1c 熔断 | V3 排队 · 1b 后 |
| 3     | `task_chatbi_v3_planning_after_resume_v1.md`                            | `planning` | V3 统筹索引           | P4                                   |
| 4     | `task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`              | `backlog`  | 低置信 §5.1          | P2                                   |
| 5     | `task_chatbi_v3_debt_from_v2_multiturn_v1.md`                           | `backlog`  | V2 多轮欠债母单         | P2                                   |
| 6     | `task_chatbi_v3_intent_classification_debt_v1.md`                       | `backlog`  | Intent vNext      | P4                                   |
| 7     | `task_chatbi_v3_low_confidence_plan_preview_confirm_v1_AGENT_PROMPT.md` | 附属         | Agent Prompt      | —                                    |
| ~~**当前**~~  | ~~**P2-1** Resilience 拆单~~                         | ~~**P2**~~ | **done**（PR #51 · 2026-05-24）                   |
| ~~**当前**~~  | ~~**P2-1a** health/ready~~ | ~~**P2**~~ | **done**（PR #52 · `8f56d4a` · 2026-05-25） |
    P21D[P2-1 拆单 done] --> P21A[P2-1a health done]
② V3 排队：P2-1b → P2-1c（P2-1a 已 PR #52）
② V3 韧性排队：P2-1b → P2-1c（母单 done/；P2-1a 见 done/）
  P21D[P2-1 拆单 done PR51] --> P21A[P2-1a done PR52]
| **P1-4**  | 低置信澄清 §4.3       | 后端 `done`；前端 **done**（2026-05-23 · Ink 烟测；`ai-ink-brain/content/tasks/done/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`） |
| **P2-1**  | 拆单母单             | **done**（`docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md` · PR #51）                                                                    |
| **P2-1a** | health / ready   | **done**（`docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md` · PR #52）                                                       |
| **P2-1b** | 限流 | **todo** · V3 排队 · `task_chatbi_v3_p2_resilience_rate_limit_v1.md` |
| **P2-1c** | 熔断               | `**todo`** · `task_chatbi_v3_p2_resilience_circuit_breaker_v1.md`                                                                          |
### 6.4 本仓 Harness 查漏补缺（P2-1a 后 · 前端 parity 前）
| 1   | `RECENT_TASK_SCHEDULE` 与 P2-1a    | **done** | 本节已同步 PR #52                                                           |
| 6   | 母单 §子单状态 P2-1a | **done** | `task_chatbi_v3_p2_resilience_v1.md` + PR #52 |
| T4 | 图谱桥接 / `graph_nodes` | **draft**（Pilot done → 3 slug 扩面） | 链 `SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` · Pilot `query-rewrite-observability` + `chatbi-v3-text2sql-tool-latency-obs` + `tech-graph-gate-d-v2-tasks` · `gov-wiki-t4-expand` |
| V3 总规            | `docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` §2.1                                                                               |
| Ink P1-4 前端关账    | `ai-ink-brain/content/tasks/done/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`                                    |
| 2026-05-24 | **P2-1 拆单 done**（PR #51）；**当前棒 P2-1a**；子单母单路径指向 `done/`；分支 `task/chatbi-v3-p2-1a-health`          |
| 2026-05-25 | P2-1a done（PR #52）；taxonomy §2.1；近期当前=治理+Wiki；P2-1b/c **V3 排队**（非 Harness 当前棒） |

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 10457 |
| `file_count` | 4 |
| `notes` | H-lean：README §1+§2.1 + invokes README 摘录 + done task 全文 + RECENT 关键词行 |
