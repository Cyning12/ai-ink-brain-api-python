# LOOP_MANIFEST · Wiki Loop 单元 A（第六轮）

| 项 | 值 |
| --- | --- |
| **母 task** | `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **freeze_id** | `WIKI-LOOP-UNIT-A@2026-05-28` |
| **PR** | **PR-A only**（docs） |
| **executor** | Claude Code · 显式 `@` SKILL |

---

## Round 顺序（硬）

| 序 | round | task_slug | active task 路径 | 关账后 |
|----|-------|-----------|------------------|--------|
| 1 | R1 | `gov-wiki-docs-hygiene` | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` | `docs/tasks/done/` |
| 2 | R2 | `gov-wiki-t4-rollout` | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` | `done/` |
| 3 | R3 | `gov-wiki-ingest-batch-3` | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` | `done/` |
| 4 | META | `wiki-loop-unit-a` | `docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md` | `done/` + `REPORT_completion_wiki_loop_unit_a_v1.md` |

---

## 人工闸（真值在母 task）

| gate | 阻塞 |
|------|------|
| `HG-LOOP-BATCH` | R1 启动 |
| `HG-INGEST-BATCH-3-SCOPE` | R3 启动 |

---

## 入口 Prompt

- 全链：[`PROMPT_START_loop_unit_a_full_chain_v1.md`](./PROMPT_START_loop_unit_a_full_chain_v1.md)
- 22→关账：[`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md)

---

## 单元 B（本 Manifest 外）

PR-A 合并后同分支执行：[`task_governance_l2_phase_c_impl_v1.md`](../../../../tasks/active/task_governance_l2_phase_c_impl_v1.md) → **PR-B**
