# Invoke · 22 帽 · Wiki Loop A1 · ingest test_strategy（v1）

| 字段 | 值 |
|------|-----|
| **hat_id** | 22 · 任务审核 R1 |
| **task_slug** | `wiki-a1-ingest-test-strategy` |
| **task_path** | `docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md` |
| **freeze_id** | `CODING-WIKI-A1-TEST-STRATEGY@2026-05-26` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **round** | A1 |
| **semi_auto** | true |
| **date** | 2026-05-26 |
| **invoke_snapshot** | 本文件 |

---

## §3 调用体快照（user 消息全文）

```text
你正在执行 Wiki Loop **A1** 帽链：**22 → 30 → 40 → 50 → 关账**（本 Epic **无 10**），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md、50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5
- semi_auto: true（无 pending 闸时可同会话连跑至本 round 关账）

【元信息】
- round: A1
- task: docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md
- task_slug: wiki-a1-ingest-test-strategy
- freeze_id: CODING-WIKI-A1-TEST-STRATEGY@2026-05-26
- git_branch: task/wiki-loop-a1-a4-v1

### 步骤 0 · 占位回填
A1 实际：本 task 无 PLACEHOLDER → **直接跳过步骤 0**。

### 步骤 1 · 22 R1
【开帽】落盘 invoke：docs/harness/invokes/by-task/wiki-loop-a1-a4/invoke_20260526_22_wiki-a1-ingest-test-strategy-v1.md
- 审 task §范围/§非范围/§failure_paths
- 子 task：确认「继承 HG-LOOP-BATCH」；母 task 已 approved
- 落盘 R1：docs/harness/reviews/by-task/wiki-loop-a1-a4/task_coding_wiki_ingest_test_strategy_v1_audit_R1_20260526.md
- 无阻塞 → 准许 30
- commit review + invoke
```

---

## 下一棒

- **帽**：30 · 执行
- **invoke**：`invoke_20260526_30_wiki-a1-ingest-test-strategy-v1.md`
