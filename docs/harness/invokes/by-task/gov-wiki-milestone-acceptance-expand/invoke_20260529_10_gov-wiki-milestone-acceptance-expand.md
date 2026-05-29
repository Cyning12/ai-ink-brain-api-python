---
hat_id: 10
round: 1
task: gov-wiki-milestone-acceptance-expand
git_branch: task/gov-wiki-milestone-acceptance-expand-v1
freeze_id: GOV-WIKI-MILESTONE-ACCEPT@2026-05-29
author: Agent
---

# Invoke 快照：10 需求与任务分析帽 · R1

| 字段 | 值 |
|------|-----|
| hat_id | 10 |
| round | R1 |
| task_slug | gov-wiki-milestone-acceptance-expand |
| task_path | docs/tasks/active/task_governance_wiki_milestone_acceptance_expand_v1.md |
| git_branch | task/gov-wiki-milestone-acceptance-expand-v1 |
| freeze_id | GOV-WIKI-MILESTONE-ACCEPT@2026-05-29 |
| audit_profile | post_close |
| test_strategy | not_applicable |
| semi_auto | true |
| human_gate | HG-TASK-DRAFT approved · HG-REINSPECT approved |
| 范围锁 | 仅 `docs/diary/2026-05-29-wiki-milestone-acceptance.md` |
| 下一棒 | B（30）推荐 |

---

## §3 可复制 Prompt 正文（快照）

```text
你正在扮演本仓 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/harness/prompts/templates/TEMPLATE-requirements-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5

【目标与上下文】
扩充 Wiki 治理线对内验收文稿（diary 里程碑签字稿），使 §1 可签字、§3 VERIFY 留证清晰、§6 smoke / §7 边界 / §8.2 公众稿扩充清单可推进。
硬约束：整个 10→30 链 仅允许编辑 docs/diary/2026-05-29-wiki-milestone-acceptance.md；其它路径 只读（含 RECENT · coding_wiki · task 正文 · 图谱 · api）。关账归档 不在本链范围。

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
0. Invoke 快照：在 Wiki worktree 落盘 docs/harness/invokes/by-task/gov-wiki-milestone-acceptance-expand/invoke_YYYYMMDD_10_gov-wiki-milestone-acceptance-expand.md。
1. 扫描 task human_gate（HG-TASK-DRAFT approved · HG-REINSPECT pending）。
2. 通读 diary 全文：输出 扩充计划表（章节 · 现状 · 拟增内容 · 只读依据路径）；不得 在 10 帽写入 diary 以外文件。
3. 验收 operacionalize：§1 四项 pass 边界 · §8.2 至少 5/8 项如何勾选或 defer（对话表，非 L0 真值复述）。
4. 禁止：改 api/ · 图谱 · CODING_WIKI · RECENT · task 归档；把 diary 叙述升格为 L0/L1 真值。
5. 下一棒双 Prompt：
   - 推荐：B（30） — 纯 docs · test_strategy not_applicable · HG-TASK-DRAFT approved · 范围锁清晰；30 Prompt 须 复述范围锁（仅 diary 一文件）。
   - 路径 A：TEMPLATE-task-audit-invoke §3 全文（可选，若人要先 22）。
   - 路径 B：TEMPLATE-execute-invoke §3 全文；30 交付 = diary diff 摘要 + §8.2 进度表；禁止 touch 白名单外路径。
6. Harness 状态栏（版本 B）。
7. commit：仅 invoke（+ 用户显式授权时 diary）；分支 task/gov-wiki-milestone-acceptance-expand-v1。

```

---

## §3.1 占位符替换确认

| 占位符 | 替换值 | 状态 |
|--------|--------|------|
| `{{GOAL_AND_CONTEXT}}` | 扩充 Wiki 治理线对内验收文稿… | 已替换 |
| `{{SPEC_OR_TASK_PATHS_OR_PASTE_NOTE}}` | 6 条只读路径 | 已替换 |
| `{{AUDIT_REVIEW_PATH_OR_NONE}}` | 无 | 已替换 |
| `{{SDD_INTENT_ROUNDS_STATUS}}` | 不涉及新 SPEC（§3 省略） | 已替换 |
| `{{NEW_OR_MAJOR_SPEC}}` | 否 | 已替换 |

---

## 扩充计划表（10 帽产出 · 供 30 执行）

| 章节 | 现状 | 拟增内容 | 只读依据 |
|------|------|----------|----------|
| §1 验收结论 | 四项 pass + 签字行 | 强化「可签字」小结句（确认 §1–§7 属实） | diary 全文 |
| §3 机器门禁 | 日期/环境一行 + 六命令 + 摘要 | 确认无需大改；可加「留证完整」结语 | diary §3 |
| §6 smoke | 4/4 pass + freeze_id | 补「可签字」小结句 | `conclusion_smoke_zh.md` |
| §7 边界 | 可外推/不可外推表 | 补「可签字」小结句 | diary §7 |
| §8.2 扩充清单 | 8 项全未勾 | 勾 6 项、defer 2 项（附理由） | `public-narrative-zh` Skill |
| §9 修订记录 | 4 行 | 补「本扩充」一行 | — |

---

## §8.2 勾选建议（30 帽执行口径）

| # | 项 | 建议 | 理由 |
|---|-----|------|------|
| 1 | 术语 | 勾选 | §8.1/8.3 已按 public-narrative-zh 原则编排；正文未用 slug/freeze_id 作主语 |
| 2 | 通俗名对照 | 勾选 | §8.3 三轨分工表已提供完整对照 |
| 3 | 数字边界 | 勾选 | §2/§4 已附「字符降幅≠API token」限定语；题集规模/单仓/场景均已注明 |
| 4 | 失败样本 | 勾选 | §4.2 已列 harness-wiki-loop-t4-l2 3/4 作诚实边界 |
| 5 | 脱敏 | defer | 属公众稿起草阶段执行项；本对内稿保留 PR#/freeze 锚点为留证需要 |
| 6 | 与卷二划界 | defer | 属 OUTLINE 标注时执行；§8.1 已列「勿主放卷二 §8.5」 |
| 7 | OUTLINE 链 | 勾选 | §8.1/8.4 已提及公众仓同级 PR |
| 8 | 核心句保留 | 勾选 | §2/§8.3 已多次强调「Wiki 不替代技术图谱」 |

---

## 10 帽交付摘要

- **human_gate**：HG-TASK-DRAFT approved（不阻塞 30）；HG-REINSPECT approved（阻塞 done，不阻塞 30）
- **范围锁**：仅 `docs/diary/2026-05-29-wiki-milestone-acceptance.md`，禁止 touch 白名单外路径
- **test_strategy**：not_applicable（纯 docs 扩充）
- **推荐下一棒**：B（30）— 范围清晰、人已承担闸 1、无 API/表变更
