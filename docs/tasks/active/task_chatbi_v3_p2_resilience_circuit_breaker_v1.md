# Task：ChatBI V3 P2-1c 外呼熔断与降级

> **状态**：todo  
> **schedule_ref**：RECENT §1.1 #L1-R2 · **P2 Loop R2**  
> **epic**：ChatBI V3 · P2 韧性  
> **blocked_by**：Loop **R1** 关账（#0b/#W1 已 `done/`）  
> **Loop 母单**：[`task_chatbi_v3_p2_resilience_loop_v1.md`](task_chatbi_v3_p2_resilience_loop_v1.md) · round **R2**  
> **关联母单（拆单）**：`docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`  
> **关联 SPEC**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md` §3  
> **排期**：[`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) · 单 PR `task/chatbi-v3-p2-loop-v1`

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| test_strategy | `required` |
| freeze_id | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| gates_before_code | `["failure_paths","验收标准","必读列表"]` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| git_branch | `task/chatbi-v3-p2-loop-v1`（与 Loop 母单 **同 PR**） |
| worktree_root | 主仓 `ai-ink-brain-api-python/` |
| task_slug | `chatbi-v3-p2-loop-r2-circuit-breaker` |
| human_gate | **继承母单** `HG-LOOP-BATCH` |

**帽子顺序**：跳过 10 · 链 `docs/harness/invokes/by-task/chatbi-v3-p2-loop/PROMPT_LOOP_22_to_CLOSE_v1.md` · round=**R2**

---

## 背景与目标

对 LLM 与 Supabase 等外呼链路增加熔断保护，避免下游持续失败放大级联故障，并提供可观测状态迁移。

## 范围

- 定义 `closed/open/half-open` 状态语义与切换条件。
- 失败累计达到阈值时快速失败并返回结构化错误。
- 恢复窗口后允许 half-open 探测并自动回到 closed。
- 记录状态迁移日志字段（便于后续 metrics 接入）。

## 非范围

- 不实现分布式熔断集群一致性。
- 不替代上游鉴权或限流。
- 不引入新的外部可观测平台 SDK。

---

## 失败路径

| # | 触发条件 | 系统行为（可观测） | 可重试 | 用户可见类型 |
|---|----------|---------------------|--------|--------------|
| F1 | 下游连续失败达到阈值 | 熔断器进入 open，快速失败返回结构化错误 | 是（等待恢复窗口） | API 错误 JSON |
| F2 | 恢复窗口后探测仍失败 | 保持 open 并记录状态迁移日志 | 是 | 日志告警 |
| F3 | 熔断吞错导致调用方误判成功 | 视为严重缺陷，禁止合并 | 否 | 复检阻塞 |

---

## 验收标准

- [ ] 注入下游错误后，日志可观测到 `closed -> open` 迁移。
- [ ] open 状态下请求快速失败，响应含结构化 `error_code`。
- [ ] 恢复窗口后可触发 half-open 探测，成功后回到 closed。
- [ ] pytest 覆盖最小状态机转移路径（失败、恢复、再次失败）。

---

## 给执行帽的必读列表

1. 本 task 全文  
2. `docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`  
3. `docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md`  
4. `api/index.py` + `api/unified_chat.py` + 外呼相关模块

