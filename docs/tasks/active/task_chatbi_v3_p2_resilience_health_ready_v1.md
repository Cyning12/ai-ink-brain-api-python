# Task：ChatBI V3 P2-1a 健康探针契约（/live + /ready）

> **状态**：todo  
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

