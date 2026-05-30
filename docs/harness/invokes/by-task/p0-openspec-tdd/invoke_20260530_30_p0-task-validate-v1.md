# Invoke · 30 执行 · R1 · p0-task-validate

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_harness_p0_task_validate_v1.md` |
| **task_slug** | `p0-task-validate` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R1** · **30 执行帽**（上一帽 22 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §4.1

【元信息】
- round: R1
- task: docs/tasks/active/task_harness_p0_task_validate_v1.md
- task_slug: p0-task-validate
- freeze_id: HARNESS-P0-TASK-VALIDATE@2026-05-30
- git_branch: task/harness-p0-openspec-tdd
- 22 review: docs/harness/reviews/by-task/p0-task-validate/task_harness_p0_task_validate_v1_audit_R1_20260530.md

【commit 硬纪律】交付完成后 git add 本轮路径 → commit message 须含 HARNESS-P0-TASK-VALIDATE@2026-05-30 → 再戴 40 帽。

步骤 2 · 30 执行交付清单：
1. 新增 tools/harness_task_validate.py（SPEC §4.1 十条规则 + CLI）
2. 新增 tests/test_harness_task_validate.py（validate-active · fp-validate-api-na · fp-validate-missing-fp · --json · --all-active）
3. 运行 pytest tests/test_harness_task_validate.py 绿
4. 运行 python tools/harness_task_validate.py docs/tasks/active/task_harness_p0_task_validate_v1.md exit 0
5. 回填 task §实现备忘（涉及文件列表）
6. 落盘本 invoke：invoke_20260530_30_p0-task-validate-v1.md（§3 ≥15 行）
7. commit 后下一棒 = **40 自检帽**

硬约束：不改 api/ · 不新增 Required CI workflow · 单 PR task/harness-p0-openspec-tdd
```
