# Invoke · 22 任务审核 · gov-wiki-agent-readorder

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_agent_readorder_v1.md` |
> | task_slug | gov-wiki-agent-readorder |
> | freeze_id | GOV-WIKI-AGENT-READORDER@2026-05-27 |
> | git_branch | task/gov-wiki-agent-readorder-v1 |
> | note | 单 task · 无 round |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 单 task（非 Loop）· 人闸 HG-TASK-DRAFT / HG-AUDIT-R1 / HG-READORDER-WORDING 均已 **approved**。

## §2 审核结论

**无阻塞 · 可进入 30。**

### 2.1 已核对项（12/12）

| # | 项 | 结果 |
|---|----|------|
| 1 | 三人工闸 approved | pass |
| 2 | SPEC §2.3 AGENTS 落盘位置明确 | pass |
| 3 | P2 实验结论 §3 推荐默认读序 | pass |
| 4 | 非范围（ingest/api/tests） | pass |
| 5 | test_strategy not_applicable + manifest hygiene | pass |
| 6 | failure_paths F1–F3 可 50 检 | pass |
| 7 | semi_auto 长链授权 | pass |
| 8 | L2 Phase B 前置 done | pass |
| 9 | 验收 VERIFY 可执行 | pass |
| 10 | 禁止项须在 AGENTS/rules 体现 | pass（30 交付） |
| 11 | L2 `_test_manifest` pointer | pass（SPEC R3） |
| 12 | invoke/review 路径 by-task | pass |

### 2.2 阻塞项

无。

## §3 审核落盘

审查文档：`docs/harness/reviews/by-task/gov-wiki-agent-readorder/task_governance_wiki_agent_readorder_audit_R1_20260527.md`

## §4 执行路线（计划）

| 序号 | 帽 | 关键动作 |
|------|-----|----------|
| 1 | 22 | review + invoke（本 commit） |
| 2 | 30 | AGENTS + rules + CODING_WIKI §7 + gen_agents_md |
| 3 | 40 | VERIFY + task §自检 |
| 4 | 50 | reinspect |
| 5 | 关账 | git mv · _views · RECENT · CLOSE |

## §5 下一棒 Prompt

见 review 文末 §下一棒可复制 Prompt。

## §6 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_wiki_agent_readorder_v1.md
├── 分支：task/gov-wiki-agent-readorder-v1
├── human_gate：均已 approved
├── 本棒交付：R1 review + invoke_22
├── 下一棒：30 执行编码
└── 阻塞：无
```
