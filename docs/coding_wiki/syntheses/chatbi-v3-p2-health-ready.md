---
title: ChatBI V3 P2-1a 健康探针（/live · /ready）
slug: chatbi-v3-p2-health-ready
layer: L2
source_task: docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md
freeze_id: SPEC-ChatBI-V3-Resilience-Ops@2026-05-11
closed_date: 2026-05-25
status: compiled
test_strategy: required
---

# P2-1a 健康探针

## 摘要

将轻量 `/api/py/health` 扩展为分层契约：**`/live`** 进程存活、**`/ready`** 依赖就绪（含 Supabase 配置等）；未就绪时 **503** + `components[]` 摘要。P2-1 母单拆单之首项 · PR #52。

## 决策要点

- 非范围：限流（1b）· 熔断（1c）· 前端 BFF 探活。  
- 与 Resilience SPEC §4 对齐。  
- 后续 V3 排队项见 `RECENT` P2-1b/c。

## §测试变更

| 动作 | 说明 |
|------|------|
| L1 | `test_strategy: required` — 须可失败单测再合并 |
| 范围 | `tests/` 覆盖 live/ready 契约与 503 分支 |

## 指针（L1）

→ `docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md`  
→ 母单 `docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`  
→ `docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md` §4
