# Invoke · 40 自检 · chatbi_intent_hints_step2_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 40 |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **task_path** | `docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` |
| **git_branch** | `task/chatbi-intent-hints-step2-v1` |

## §3 快照（40 自检）

```text
40 自检帽 · 对照 task 验收表逐条 pass · 回填 ### 自检结论（执行者）
```

## 命令证据

| 命令 | exit | 结果 |
| --- | ---: | --- |
| `pytest tests/test_intent_hints_arbitration.py tests/test_intent_router_backend_v1.py -q` | 0 | 17 passed |
| `pytest tests/test_intent_hints_loader.py -q` | 0 | 9 passed |
| `pytest tests/test_intent_agent_accuracy.py -k portfolio -q` | 0 | 2 passed |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 312 passed · 1 skipped |
| `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` | 0 | OK |

**回填**：task `### 自检结论（执行者）` · 验收标准全勾选。

**下一棒**：50 独立复检 → `docs/tasks/reinspect_results/reinspect_chatbi_intent_hints_step2_v1_20260604_v1.md`
