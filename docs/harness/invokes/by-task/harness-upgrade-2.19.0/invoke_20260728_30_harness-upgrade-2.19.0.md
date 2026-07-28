# Invoke：30（含 40）· harness-upgrade-2.19.0

---

## 元信息表

| 字段 | 值 |
| --- | --- |
| hat_id | 30（含 40） |
| task_slug | `harness-upgrade-2.19.0` |
| task_paths | `docs/tasks/active/task_harness_upgrade_2.19.0.md` |
| related_review_or_none | `docs/harness/reviews/by-task/harness-upgrade-2.19.0/task_harness_upgrade_2.19.0_audit_R1_20260728.md` |
| git_branch | `task/harness-upgrade-2-19-0` |
| created_utc_or_local | 2026-07-28 |
| notes | 棒 A：2.19.0 upgrade + lint-wiki-delta + overlay；未启用 WikiTrack |

---

## 人工闸扫描（GATE_VERIFY）

| human_gate_id | task表status | 一致？ | 30可开工？ |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | Y | Y |
| HG-AUDIT-R1 | approved | Y | Y |
| HG-GRAPH-MODULES | approved | Y | Y |

结论：可开工

---

## 交付摘要

- **upgrade**：`npx --yes @cyning/harness@2.19.0 upgrade --yes --target .` → exit 0（不带 `--ide`）
- **manifest / pin**：`2.18.0` → `2.19.0`
- **overlay**：已恢复 AGENTS / CLAUDE / FRAGMENT_30* / `06-harness-pointer` / `11-coding-wiki-readorder` / prompts README
- **lint-wiki-delta**：`--scope all` · scanned=197 · missing=0 · PASS（补 10 个遗漏文件）
- **coding_wiki**：本波 **未改**
- **RUNBOOK**：POINTER 拷贝至 `docs/harness/RUNBOOK_wikitrack_enable_obsidian_v1_zh.md`
- **质量门**：ruff pass；pytest 见同会话记录
- **下一棒**：`task close --file docs/tasks/active/task_harness_upgrade_2.19.0.md --yes`

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-07-28 | 2.19.0 upgrade + lint-wiki-delta + overlay |

## CLOSE

- CLOSE → `docs/tasks/done/` · 禁止 `task close --target .`
