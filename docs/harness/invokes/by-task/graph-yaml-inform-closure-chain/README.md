# Invoke · graph-yaml-inform-closure-chain（P0→P1 串行）

| 项 | 值 |
| --- | --- |
| **chain_slug** | `graph-yaml-inform-closure-chain` |
| **Round** | T1 |
| **Open Folder** | **`ai-ink-brain-api-python/`** |
| **merge_policy** | **`ci_green_merge`（强制）**：P0 PR **CI 全绿 + merge 入 `main`** 后，方可开 P1 30 |
| **链 PROMPT 真值** | [`PROMPT_cursor_task_chain_serial_v1_T1_graph-yaml-inform-closure_zh.md`](../../../prompts/PROMPT_cursor_task_chain_serial_v1_T1_graph-yaml-inform-closure_zh.md) |

## 串行 task

| # | slug | task | 分支 | HG-TASK-DRAFT |
| --- | --- | --- | --- | --- |
| 1 | `graph-yaml-doc-hygiene-p0` | [`task_engineering_graph_yaml_doc_hygiene_p0_v1.md`](../../../tasks/active/task_engineering_graph_yaml_doc_hygiene_p0_v1.md) | `task/graph-yaml-doc-hygiene-p0` | **approved** |
| 2 | `graph-yaml-export-yaml-p1` | … | `task/graph-yaml-export-yaml-p1` | **approved** · 30 blocked_by **P0 CI 绿 + merge** |

## P1 开 30 硬闸门

1. P0 task → `docs/tasks/done/` · HG-REINSPECT signed  
2. P0 PR **CI 全绿**  
3. P0 PR **已 merge 入 `main`**  
4. `git checkout main && git pull` 含 P0 merge commit  

## 启动（复制即用）

| 模式 | 文件 |
| --- | --- |
| **会话 1 · 仅 P0** | [`PROMPT_START_SERIAL_v1.md`](./PROMPT_START_SERIAL_v1.md)（PHASE A → STOP at merge） |
| **会话 2 · P1**（P0 已 merge） | [`../graph-yaml-export-yaml-p1/PROMPT_START_30_v1.md`](../graph-yaml-export-yaml-p1/PROMPT_START_30_v1.md) |
| 仅 P0（分步） | [`../graph-yaml-doc-hygiene-p0/PROMPT_START_30_v1.md`](../graph-yaml-doc-hygiene-p0/PROMPT_START_30_v1.md) |
