# Invoke · 30 执行 · R3 · p0-status-cursor

| 字段 | 值 |
|------|-----|
| **round** | R3 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_harness_p0_status_cursor_v1.md` |
| **task_slug** | `p0-status-cursor` |
| **freeze_id** | `HARNESS-P0-STATUS-CURSOR@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R3** · **30 执行帽**，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §5

【元信息】
- round: R3
- task_slug: p0-status-cursor
- freeze_id: HARNESS-P0-STATUS-CURSOR@2026-05-30
- git_branch: task/harness-p0-openspec-tdd

步骤 2 · 30 交付：
1. tools/harness_change_status.py（--task --json · 复用 validate/gate 解析）
2. tests/test_harness_change_status.py（status-json Scenario）
3. .cursor/commands/harness-validate.md · harness-status.md
4. python tools/harness_change_status.py --task docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md --json
5. pytest tests/test_harness_change_status.py
6. commit → 40 自检

禁止：改 api/ 业务
```
