# Invoke · explore · api-env-rag-env-consolidation

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-env-rag-env-consolidation` |
| **round** | T1-W1 |
| **hat** | explore |
| **git_branch** | `task/api-env-rag-env-w1` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

## §1 摘要

W1 explore 完成：`index.py` 11 处 `os.getenv` 待迁入 `rag_env` helper；无契约变更。

## §2 交付

- `explore_api_env_rag_env_consolidation_gap.md`

## §3 下一棒（30 帽）

```text
【角色】Harness 30 · 实现 · W1

【读序】task_api_env_rag_env_consolidation_w1.md · R1 audit · explore gap · L2 P-03

【必须】
1. 先写 tests/test_rag_env_helpers_w1.py
2. rag_env 新增 helper；index 零 os.getenv
3. ruff + pytest 绿

【forbidden】MANIFEST 外 api/*.py · HTTP 契约变更 · git commit

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```
