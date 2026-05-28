# Scorecard · `wiki-loop-unit-a` · `claude-code`

| 字段 | 值 |
| --- | --- |
| **freeze_id** | `SKILL-XPLATFORM-WIKI-LOOP-UNIT-A@2026-05-28` |
| **task_slug** | `wiki-loop-unit-a`（母单 · Loop 第六轮） |
| **platform** | `claude-code` |
| **model** | Claude Opus（cc 会话 · 未单独记录 model 版本） |
| **date** | 2026-05-28 |
| **SKILL** | `SKILL-harness-loop-batch` · `SKILL-docs-governance` · `HANDOFF_SEMI_AUTO` / `HANDOFF_AUTO_COMMIT` |
| **PROMPT 入口** | [`PROMPT_START_loop_unit_a_full_chain_v1.md`](../../../../invokes/by-task/wiki-loop-unit-a/PROMPT_START_loop_unit_a_full_chain_v1.md) |
| **业务 PR** | 待开 **PR-A**（分支 `task/wiki-unit-ab-plan-v1` · `bf15688`…`e746781`） |
| **hygiene PR** | 无（本 case 关账 hygiene 一次到位） |

---

## 三维总评

```text
业务实现     ███████████████████░  96%
Harness 落盘  ██████████████████░░  90%
开 PR 就绪度   ███████████████████░  94%
```

| 维度 | 分 | 依据（1–3 句） |
| --- | --- | --- |
| 业务实现 | 96 | R1 对比表/SPEC/RECENT 同步；R2 **20/20** synthesis 全量 `graph_nodes`；R3 **5** slug · syntheses **25** · 无 api/tests 越界 |
| Harness 落盘 | 90 | R1→R3 各 **22→50→CLOSE** + META；R1·22 含 `cross_round_semi_auto`；R2/R3·22 的 §3 为**摘要版**（仍 ≥15 行 / ≥800B）· review 落 `by-task/<slug>/` 非 `wiki-loop-unit-a/` 子目录 |
| 开 PR 就绪度 | 94 | 母单 + 三子 task **`done/`** · `_views` · `REPORT_completion_*` · 母闸 `f30f8dd` approved；可直接开 PR-A |

---

## ST0–ST6

| # | 结果 | 备注 |
| --- | --- | --- |
| **ST0** | **pass**（过程债已记录） | 执行前曾出现 **未人批即开工**（用户复盘）；**`f30f8dd`** 人批后 R1 链启动 · 已反哺 §执行铁律 + `harness_human_gate_check.py` |
| ST1 | pass | 3× review + 15 invoke；R1·22 §3 **7 步全文**；R2/R3·22 §3 缩短 |
| ST2 | pass | 每 round 30 有独立业务 commit（`9a58509` / `a500b96` / `965d834`） |
| ST3 | pass | 3× 40 + task §自检结论回填 |
| ST4 | pass | `reinspect_gov-wiki-*_20260528_v1.md` ×3 + invoke_50 |
| ST5 | pass | 子 task + 母单均 `done（2026-05-28）` · `git mv` · `_views` 4 行 |
| ST6 | pass | RECENT §6.6 Unit A **done**；META 同步 |

**Loop C1–C7（母单 REPORT §5 抽样）**：C1–C7 均 **pass**（见 [`REPORT_completion_wiki_loop_unit_a_v1.md`](../../../../invokes/by-task/wiki-loop-unit-a/REPORT_completion_wiki_loop_unit_a_v1.md)）。

---

## 平台偏差

| 项 | 观测 |
| --- | --- |
| rules 加载 | **无** `.mdc` · 依赖 `PROMPT_START` + 显式 Read/`@` SKILL |
| semi_auto | **同会话** R1→R2→R3→META 续跑 · 无「每 round 新对话」 |
| **ST0 Gate** | 首日误跑暴露 **Prompt≠闸**；人批 + 机器门禁后合规 |
| invoke §3 | R1 达标；R2/R3 的 22/50 略薄但未 stub 一行式 |
| 关账顺序 | task 头部 `done` 与 `git mv` 同链 · 无 Part A hygiene 补债 |
| 改进已落盘 | `7b5bdbf`/`eb32c4b` 铁律 · `64889bf` 门禁 · `8a1d6d4` 继承闸 |

---

## 证据链

| 类型 | 路径 / URL |
| --- | --- |
| invoke | `docs/harness/invokes/by-task/wiki-loop-unit-a/invoke_*_20260528.md`（15 + META CLOSE） |
| review | `docs/harness/reviews/by-task/gov-wiki-docs-hygiene/` · `gov-wiki-t4-rollout/` · `gov-wiki-ingest-batch-3/` |
| reinspect | `docs/tasks/reinspect_results/reinspect_gov-wiki-*_20260528_v1.md` |
| REPORT | [`REPORT_completion_wiki_loop_unit_a_v1.md`](../../../../invokes/by-task/wiki-loop-unit-a/REPORT_completion_wiki_loop_unit_a_v1.md) |
| commit | `bf15688`（R1·22）…`e746781`（META）；闸 `f30f8dd` |
| 母 task | `docs/tasks/done/task_harness_wiki_loop_unit_a_v1.md` |
