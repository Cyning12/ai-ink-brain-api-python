# Invoke · 22 任务审核 · R3 · gov-wiki-ingest-batch-2

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md` |
> | task_slug | `gov-wiki-ingest-batch-2` |
> | freeze_id | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- **前置**：R1/R2 子 task 均在 `done/`。
- **人工闸**：`HG-INGEST-BATCH-2-SCOPE` = **approved**（只读母单 `task_harness_wiki_loop_p2_followup_v1.md` 表，子单勿漂移）。

## §2 审查结论

**零阻塞。** 5 slug 表与 P2 SPEC §3 一致；不与 Batch-1 重复。

| slug | 状态 |
| --- | --- |
| `wiki-ctx-ab-representative` | 待 ingest |
| `governance-wiki-agent-readorder` | 待 ingest |
| `governance-wiki-ingest-batch` | 待 ingest |
| `harness-wiki-loop-t4-l2` | **已有** synthesis · 计 coverage |
| `coding-wiki-t1c-test-archive` | 待 ingest |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R3** 的 **30 执行编码帽**。上一帽（22）已结束。

【元信息】
- round: R3
- hat: 30
- task: docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md
- task_slug: gov-wiki-ingest-batch-2
- freeze_id: GOV-WIKI-INGEST-BATCH-2@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 30 帽交付
1. 新增 synthesis（`docs/coding_wiki/syntheses/`）：上表 4 篇 + `harness-wiki-loop-p2-followup` 骨架（达 **≥20** 文件）。
2. 更新 `docs/coding_wiki/index.md` · `log.md`（batch-ingest-2 行）。
3. lint：frontmatter 符合 `CODING_WIKI.md` §3；无 review 全文粘贴。
4. `python tools/tech_graph_manifest_check.py` hygiene（不改 api）。
5. commit · 落盘 **40** invoke（C2 ≥15 行 §3）。

### 硬约束
- **禁止** 重复 Batch-1 已 ingest slug（见 `SPEC-Governance-Wiki-Ingest-Batch-v1.md` §2）。
- 不改 api/tests/prompts/CI。

### VERIFY（40）
```bash
ls docs/coding_wiki/syntheses/*.md | wc -l    # ≥20
rg -n 'wiki-ctx-ab-representative' docs/coding_wiki/index.md
python tools/tech_graph_manifest_check.py
```
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · R3
├── HG-INGEST-BATCH-2-SCOPE：approved（母单）
└── 下一棒：30
```
