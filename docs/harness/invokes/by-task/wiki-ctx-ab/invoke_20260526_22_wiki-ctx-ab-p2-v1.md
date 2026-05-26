# Invoke Snapshot · 22 R1 · Wiki-CTX-AB P2

| 字段 | 值 |
| --- | --- |
| hat_id | `22` |
| task_slug | `wiki-ctx-ab` |
| phase | `P2` |
| freeze_id | `WIKI-CTX-AB@2026-05-25` |
| task_path | `docs/tasks/active/task_wiki_ctx_ab_v1.md` |
| git_branch | `task/wiki-ctx-ab-p2-v1` |
| worktree_root | `.` |
| created_at | `2026-05-26` |

---

## 用户消息全文快照

```text
你正在扮演 Harness「任务审核帽（22 · R1）」（本 Epic：Wiki-CTX-AB **P2** · H-lean vs W · 后端子仓），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/templates/TEMPLATE-task-audit-invoke.md §3
- docs/harness/reviews/README.md（落盘 by-task/wiki-ctx-ab/）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc
- **说明**：本 task 的 P1 已 accepted（见 conclusion_p1）；本轮 R1 审 **P2 开工条件**，非重审 P1。

【开帽 · Invoke 快照】在输出审查正文之前，将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_22_wiki-ctx-ab-p2-v1.md
（元信息：hat_id=22、task_slug=wiki-ctx-ab、phase=P2、freeze_id=WIKI-CTX-AB@2026-05-25）

输入（相对子仓根）：
- 待审 task：docs/tasks/active/task_wiki_ctx_ab_v1.md
- 关联 SPEC：docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md（§3 · T2 / P2）
- 实验目录：docs/harness/experiments/wiki_ctx_ab_v1/
- P1 证据（只读）：docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md
- T1b 关账（只读）：docs/tasks/done/task_coding_wiki_pilot_v1.md
- 同 slug Wiki 页（须存在 · test -f）：
  docs/coding_wiki/syntheses/harness-p1-docs-consolidation.md
  docs/coding_wiki/index.md
- P2 预备工件（审查存在性，勿在本帽跑题答题）：
  docs/harness/experiments/wiki_ctx_ab_v1/payloads/TEMPLATE-W.md
  docs/harness/experiments/wiki_ctx_ab_v1/payloads/W_harness-p1-docs-consolidation.md
  docs/harness/experiments/wiki_ctx_ab_v1/payloads/H-lean_harness-p1-docs-consolidation.md（P1 基线臂 · 复用）
  tools/wiki_ctx_ab_materialize_w.py
- 上一轮审查：无（本 task 首份 22）
- worktree_root / git cwd：.（分支 task/wiki-ctx-ab-p2-v1）
- freeze_id：WIKI-CTX-AB@2026-05-25
- gold slug：harness-p1-docs-consolidation

0b. 人工闸：HG-AB-SLUG、HG-AB-P1-DONE 须 **approved**；否则拒准 P2 开工。

你必须完成（R1 · P2 就绪审 · 按序）：

1. 通读 task §范围/§非范围/§验收标准（P2 节）；确认 T1b **已关账** 且 Wiki 同 slug 页可 `test -f`。

2. 对照 SPEC §3.1 P2 签收条件：H-lean vs W、题集仍用 questions.md（四题）、不得改 harness prompts/api。

3. 检查 P2 工件完整性（阻塞/非阻塞分项）：
   · TEMPLATE-W + W 物化实例 char_count 已填
   · H-lean 实例仍与 P1 一致（勿删改 P1 行）
   · PROMPT_third_party P2 或 30 帽内跑题说明就绪（见实验目录 README）
   · scorecard.md 留 §P2 空表待 30 填

4. **落盘审查 md**（零阻塞亦须写）：
   docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md

   文内结构（硬）：
   - 元信息（task_path、invoke_snapshot、freeze_id、audit_round=R1、phase=P2）
   - 审查结论摘要
   - P2 开工焦点：Wiki 仅载荷 vs H-lean 边界；题集 gold 要点仍覆盖 Q1–Q4
   - 阻塞 / 非阻塞
   - 是否建议 **30 帽开工**（须无阻塞）
   - 签收 / 关闭（R1：是否准许进入 P2 执行）
   - **下一棒可复制 Prompt**：若准许，**全文嵌入**：
     docs/harness/invokes/by-task/wiki-ctx-ab/PROMPT_30_startup_wiki-ctx-ab-p2-v1.md
     并注明帽链：**30 → 40 → 50 → CLOSE**

5. **禁止**：执行 P2 答题/填 scorecard（属 30）；改 docs/harness/prompts/、api/、CI。

6. **Commit**（仅路径）：
   git add docs/harness/reviews/by-task/wiki-ctx-ab/ docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_22_*.md
   message 含 WIKI-CTX-AB@2026-05-25 · P2 R1

7. 对话末尾：**📋 Harness 状态栏（版本 B）**；**勿执行 30**；提示人 **新开对话** 粘贴 PROMPT_30。

硬约束：
- Open Folder = **ai-ink-brain-api-python/**
- 有阻塞时 **禁止** 指示 30 开工

关键词：22、R1、Wiki-CTX-AB、P2、H-lean、W、coding_wiki、T2、wiki-ctx-ab
```
