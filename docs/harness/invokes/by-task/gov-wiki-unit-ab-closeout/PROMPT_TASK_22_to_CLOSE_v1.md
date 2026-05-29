# P0 · Wiki 单元 A/B 收口 · 22→关账

> **task**：`docs/tasks/active/task_governance_wiki_unit_ab_closeout_v1.md`  
> **分支**：`task/gov-wiki-unit-ab-closeout-v1`（从最新 `origin/main` 拉出）  
> **前置**：`main` 已含 #79、#80、#81

---

## 执行前（人 + 机）

```bash
git checkout main && git pull origin main
git checkout -b task/gov-wiki-unit-ab-closeout-v1

# 闸口（须文件内 approved，非口头）
python tools/harness_human_gate_check.py \
  --task docs/tasks/active/task_governance_wiki_unit_ab_closeout_v1.md
```

---

## §3 可复制 Prompt（22→关账）

```text
【步骤 0 · Gate】打开 task_governance_wiki_unit_ab_closeout_v1.md，扫描 human_gate。
HG-TASK-DRAFT / HG-AUDIT-R1 未 approved 且阻塞当前帽 → 硬停（HANDOFF_SEMI_AUTO §2.3）。
HG-REINSPECT 在 50 前须 approved（可 22 后再请人批）。

执行 P0 · gov-wiki-unit-ab-closeout · test_strategy: not_applicable · 22→30→40→50→关账。
分支 task/gov-wiki-unit-ab-closeout-v1；禁止 api/tests/tools/workflows；禁止 syntheses 批量 ingest。

必读 @：
- docs/tasks/active/task_governance_wiki_unit_ab_closeout_v1.md（范围 + VERIFY）
- docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md
- docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md §5.2
- docs/tasks/RECENT_TASK_SCHEDULE.md §0、§6.6、§8
- docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md
- docs/harness/experiments/skill_cross_platform_v1/README.md · rubric_v1.md
- cases/wiki-loop-unit-a_claude-code_20260528/（A 臂参照）
- docs/tasks/skills/SKILL-harness-task.md · SKILL-docs-governance.md
- docs/harness/prompts/hats/22-task-audit.md … 50-independent-reinspect.md
- HANDOFF_SEMI_AUTO.md · HANDOFF_AUTO_COMMIT.md · HANDOFF_CLOSE_TRACE.md
- 本文件 PROMPT_TASK_22_to_CLOSE_v1.md

【30 要点】
1. Unit AB Plan §4 步骤 1–6 与 PR #79/#80/#81 对齐（done）
2. Roadmap §5.2 A/B 收口 → done；§0 下一棒勿写「B 待执行」
3. RECENT §0 + §8 + 关账时 §6.6 增本 task done 行
4. WIKI_REQUIREMENTS_COMPARISON 补 Unit A/B · Phase C · CI 行
5. skill_cross_platform：新建 gov-l2-phase-c-impl_claude-code_20260528（scorecard + conclusion_zh + README 索引）
6. 每帽落盘 invoke/review/reinspect；commit 按 HANDOFF_AUTO_COMMIT

【40 须粘贴】task §VERIFY 全部命令输出要点。

【50】独立复检 diff 白名单；reinspect_gov-wiki-unit-ab-closeout_<date>_v1.md。

关账：git mv done/ · _views · RECENT §6.6 · CLOSE_TRACE。
```

---

## C2 / invoke 落盘

| 帽 | 路径模式 |
|----|----------|
| 22 | `docs/harness/reviews/by-task/gov-wiki-unit-ab-closeout/review_*_22_*` |
| 30 | `docs/harness/invokes/by-task/gov-wiki-unit-ab-closeout/invoke_*_30_*` |
| 40 | `docs/harness/invokes/by-task/gov-wiki-unit-ab-closeout/invoke_*_40_*` |
| 50 | `docs/tasks/reinspect_results/reinspect_gov-wiki-unit-ab-closeout_*` |

§3 正文 **≥15 行**；元信息含 `task_slug` · `freeze_id` · `git_branch`。
