# Wiki 里程碑验收文档扩充 · 10 帽启动

> **task**：`docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md`  
> **task_slug**：`gov-wiki-milestone-acceptance-expand`  
> **分支**：`task/gov-wiki-milestone-acceptance-expand-v1`  
> **worktree**：`../ai-ink-brain-api-python-wt-wiki-accept`（**Open Folder 须指向 worktree**）

---

## 执行前（分支 / worktree）

```bash
# 在 Wiki worktree 开帽（勿在主仓混切本分支）
cd ../ai-ink-brain-api-python-wt-wiki-accept
git branch --show-current   # 期望 task/gov-wiki-milestone-acceptance-expand-v1

python tools/harness_human_gate_check.py \
  --task docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md
```

主仓当前应停留 **task/chatbi-v3-p2-1b-rate-limit**（P2-1b 业务轨）。

---

## 范围锁（硬 · 贯穿 10→30→40）

| 允许修改 | 禁止修改（本 task 全程） |
|----------|--------------------------|
| **`docs/diary/2026-05-29-wiki-milestone-acceptance.md`** 唯一写文件 | `api/` · `tests/` · `docs/_tech_graph/` · `graph.json` |
| 只读引用 AB/smoke 结论 | `docs/coding_wiki/**`（含 syntheses · index · log.md） |
| — | `docs/tasks/RECENT_TASK_SCHEDULE.md` · task 正文 · `_views/done.md` |
| — | `docs/harness/**`（除本 invoke 落盘由 Agent 按模板写入） |
| — | 公众仓 `ai-coding-closed-loop-articles` 正文 |

关账（git mv · RECENT · log）**另会话 / 人显式授权**后再做；本启动 **只做验收 diary 扩充**。

---

## §3 可复制 Prompt 正文（10-requirements · 开帽）

```text
你正在扮演本仓 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/harness/prompts/templates/TEMPLATE-requirements-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5

【目标与上下文】
扩充 **Wiki 治理线对内验收文稿**（diary 里程碑签字稿），使 §1 可签字、§3 VERIFY 留证清晰、§6 smoke / §7 边界 / §8.2 公众稿扩充清单可推进。
**硬约束**：整个 10→30 链 **仅允许编辑** `docs/diary/2026-05-29-wiki-milestone-acceptance.md`；其它路径 **只读**（含 RECENT · coding_wiki · task 正文 · 图谱 · api）。关账归档 **不在本链范围**。

【已有材料路径 · 只读】
docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md
docs/diary/2026-05-29-wiki-milestone-acceptance.md
docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p*.md（按需）
docs/harness/experiments/wiki_ctx_ab_representative_v1/（按需）
docs/harness/experiments/task_schedule_read_smoke_v1/conclusion_smoke_zh.md
docs/tasks/done/task_governance_wiki_t4_ops_v1.md（#83 背景）

【是否按任务审核文档回填】
无

【SDD 三轮状态】
不涉及新 SPEC（§3 省略）

【是否新建或重大修订 SPEC】
否

你必须完成：
0. **Invoke 快照**：在 **Wiki worktree** 落盘 docs/harness/invokes/by-task/gov-wiki-milestone-acceptance-expand/invoke_YYYYMMDD_10_gov-wiki-milestone-acceptance-expand.md。
1. 扫描 task human_gate（HG-TASK-DRAFT approved · HG-REINSPECT pending）。
2. 通读 diary 全文：输出 **扩充计划表**（章节 · 现状 · 拟增内容 · 只读依据路径）；**不得**在 10 帽写入 diary 以外文件。
3. 验收 operacionalize：§1 四项 pass 边界 · §8.2 至少 5/8 项如何勾选或 defer（对话表，非 L0 真值复述）。
4. **禁止**：改 api/ · 图谱 · CODING_WIKI · RECENT · task 归档；把 diary 叙述升格为 L0/L1 真值。
5. **下一棒双 Prompt**：
   - 推荐：**B（30）** — 纯 docs · test_strategy not_applicable · HG-TASK-DRAFT approved · 范围锁清晰；30 Prompt 须 **复述范围锁**（仅 diary 一文件）。
   - 路径 A：TEMPLATE-task-audit-invoke §3 全文（可选，若人要先 22）。
   - 路径 B：TEMPLATE-execute-invoke §3 全文；30 交付 = diary diff 摘要 + §8.2 进度表；**禁止** touch 白名单外路径。
6. **📋 Harness 状态栏（版本 B）**。
7. commit：仅 invoke（+ 用户显式授权时 diary）；分支 task/gov-wiki-milestone-acceptance-expand-v1。

diary 扩充优先级（建议顺序）：
1. §1 验收结论 — 每项 pass 依据 pointer（不复制长 VERIFY 日志）
2. §3 — 留证日期 / 环境一行对齐
3. §6 / §7 — 已有 smoke · 边界，补「可签字」表述
4. §8.2 — 逐项勾选或「defer + 理由」；术语按 public-narrative-zh 对内备注（不写公众稿正文）
5. §9 修订记录 — 本扩充一行
```

---

## 落盘约定

| 帽 | 路径模式 |
|----|----------|
| 10 | `docs/harness/invokes/by-task/gov-wiki-milestone-acceptance-expand/invoke_*_10_*` |
| 22 | `docs/harness/reviews/by-task/gov-wiki-milestone-acceptance-expand/review_*_22_*`（若人选 A） |
| 30 | `docs/harness/invokes/by-task/gov-wiki-milestone-acceptance-expand/invoke_*_30_*` |
| 40 | `docs/harness/invokes/by-task/gov-wiki-milestone-acceptance-expand/invoke_*_40_*` |

**30 写文件白名单**：`docs/diary/2026-05-29-wiki-milestone-acceptance.md` **仅此一个**。
