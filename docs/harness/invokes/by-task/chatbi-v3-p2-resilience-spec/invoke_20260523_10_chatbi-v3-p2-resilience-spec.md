# Invoke Snapshot · 10-requirements

| 字段 | 值 |
|------|-----|
| hat | `10-requirements` |
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_v1.md` |
| git_branch | `task/chatbi-v3-p2-resilience-spec` |
| audit_review_path | `无` |
| created_at | `2026-05-24` |
| operator_note | `按用户指令执行 10 帽：P2-1a/b/c 验收可执行化 + 对齐 Resilience/Overview` |

## 用户消息快照（开帽起点）

```text
你正在扮演本仓 Harness「需求与任务分析帽」，遵循 docs/harness/prompts/hats/10-requirements.md 与 TEMPLATE-requirements-invoke §3。

【目标】润色 active/task_chatbi_v3_p2_resilience_v1.md：拆单 P2-1a/b/c 验收可执行化；对齐 SPEC-ChatBI-V3-Resilience-Ops.md

【材料】
docs/tasks/active/task_chatbi_v3_p2_resilience_v1.md
docs/spec/v3-agent/SPEC-ChatBI-V3-Resilience-Ops.md
docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md §2.1
docs/tasks/RECENT_TASK_SCHEDULE.md
api/index.py（/api/py/health）

【审核回填】无

0. Invoke → invoke_20260523_10_chatbi-v3-p2-resilience-spec.md
1. 补强 failure_paths、子 task 验收、Overview §3 变更点
2. 下一棒：推荐 B（30 全自动链）全文 Prompt + A（22）全文
3. 状态栏版本 B；commit task + invoke

人签 HG-TASK-DRAFT 后再执行 Prompt A。
```
