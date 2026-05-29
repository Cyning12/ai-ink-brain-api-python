# Task：ChatBI V3 P2-1b 高消耗端点限流

> **状态**：in_progress  
> **schedule_ref**：RECENT §1.1 #0b · **V3 业务当前棒**  
> **epic**：ChatBI V3 · P2 韧性  
> **blocked_by**：P2-1a done（PR #52）  
> **blocks**：P2-1c 熔断  
> **排期**：见 [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) · Wiki hub [`task-schedule-ink-backend`](../../coding_wiki/concepts/task-schedule-ink-backend.md)  
> **关联母单**：`docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`（P2-1a 已 **done** · PR #52）  
> **关联 SPEC**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md` §2  
> **并行**：与 `task/gov-wiki-milestone-acceptance-expand-v1` 并行 · 见 RECENT §1.2

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| test_strategy | `required` |
| freeze_id | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| gates_before_code | `["failure_paths","验收标准","必读列表"]` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| git_branch | `task/chatbi-v3-p2-1b-rate-limit` |
| worktree_root | 主仓 `ai-ink-brain-api-python/` |

---

## 背景与目标

为 `/api/py/unified/chat/stream` 与 `/api/py/chat` 增加可配置限流，避免突发并发压垮推理与数据库资源。

## 范围

- 定义限流粒度（IP 或 access token）与优先策略。
- 新增阈值 env（QPS/并发窗口等）并文档化默认值。
- 触发限流时统一返回 `429` 结构化 body（`error_code`、可选 `retry_after`）。

## 非范围

- 不改 `/live` `/ready` 契约（P2-1a）。
- 不实现熔断状态机（P2-1c）。
- 不引入全链路 WAF。

---

## 失败路径

| # | 触发条件 | 系统行为（可观测） | 可重试 | 用户可见类型 |
|---|----------|---------------------|--------|--------------|
| F1 | 流量超阈值 | 返回 `429` + 结构化错误码 | 是 | API 错误 JSON |
| F2 | 阈值 env 缺失或非法 | 启动期报配置错误或回退默认值并告警 | 是 | 日志告警 |
| F3 | 限流只覆盖一个端点导致绕过 | 40/50 复检 fail，不允许关账 | 是 | 验收阻塞 |

---

## 验收标准

- [ ] 使用压测脚本（`hey` 或 pytest 并发桩）可稳定触发 429。
- [ ] 429 响应体含 `error_code`，可选 `retry_after` 字段语义明确。
- [ ] 阈值可通过 env 调整，调整后行为变化可复现。
- [ ] 至少覆盖 `/api/py/unified/chat/stream` 与 `/api/py/chat` 两条路径。

---

## 给执行帽的必读列表

1. 本 task 全文  
2. `docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`  
3. `docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md`  
4. `api/index.py` + `api/unified_chat.py`

