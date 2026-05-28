# Wiki Loop 单元 A · 单 round 22→关账（cc）

> 每 round 复制 §3 到 invoke `docs/harness/invokes/invoke_<task_slug>_<hat>_<date>.md`（或 `by-task/wiki-loop-unit-a/` 下按 round 命名）。

---

## §3 模板（替换 `<ROUND>` / `<TASK_PATH>` / `<SLUG>` / `<FREEZE>`）

```text
执行 Wiki Loop 单元 A · <ROUND> · 22→关账。分支 task/wiki-unit-ab-plan-v1。
task: <TASK_PATH>
task_slug: <SLUG>
freeze_id: <FREEZE>
semi_auto: true · PR-A docs-only · 禁止 api/tests/tools。

帽子：22→30→40→50；落盘 invoke + commit；关账 HANDOFF_CLOSE_TRACE。
R3 额外：Batch-3 五 slug 见 SPEC-Governance-Wiki-Ingest-Batch-3-v1.md §1。

**执行步骤（hard rules · 每帽换前须落盘 + commit）**

1. **Gate 验证**：打开 `<TASK_PATH>`，扫描 `human_gate` 表。若有 `pending` 阻塞当前帽 → **硬停**，输出 `📋 Harness 状态栏（版本 B）`（阻塞版），不写 review / 不改代码 / 不落盘 invoke。真值：`HANDOFF_SEMI_AUTO.md` §2.3。
2. **22 审核**：读 task + 关联 SPEC / 前置 task，产出 `docs/harness/reviews/by-task/<SLUG>/task_*_audit_R<ROUND>_*.md`。post_close 轻闸；无阻塞则写「零阻塞·可执行」+ 下一棒 30 Prompt。
3. **30 执行**：按 task 范围改文档；遵守「范围 / 非范围」；每文件改动后自核链接、状态、freeze_id 一致性。
4. **40 自检**：逐条对照 task 验收标准，运行 VERIFY 命令，粘贴输出要点；回填 task 内 `### 自检结论（执行者）`。
5. **50 复检**：独立 diff 审查（非复读 40），产出 `docs/tasks/reinspect_results/reinspect_<SLUG>_*.md`；含 human_gate diff 审查与 author 追溯。
6. **关账**：`git mv` task → `docs/tasks/done/`；更新 `_views/done.md`；输出 `HANDOFF_CLOSE_TRACE`（执行路线 + commit 回溯）。
7. **invoke 质量（C2）**：每帽落盘 `docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_*`，§3 ≥15 行，元信息表完整（round/hat/task/task_slug/freeze_id/git_branch）。按 `HANDOFF_AUTO_COMMIT` 仅 add 本轮路径后 commit。
```

### R1 填表

| 占位 | 值 |
|------|-----|
| ROUND | R1 |
| TASK_PATH | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| SLUG | `gov-wiki-docs-hygiene` |
| FREEZE | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |

### R2 填表

| ROUND | R2 |
| TASK_PATH | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| SLUG | `gov-wiki-t4-rollout` |
| FREEZE | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |

### R3 填表

| ROUND | R3 |
| TASK_PATH | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| SLUG | `gov-wiki-ingest-batch-3` |
| FREEZE | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |

---

## 单元 B（PR-B · 非本 Prompt）

`docs/tasks/active/task_governance_l2_phase_c_impl_v1.md` · `test_strategy: required` · PR-A 合并后继续同分支。
