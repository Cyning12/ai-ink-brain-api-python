# Task：Kimi Code Harness 试点 · RECENT 同步 + done/ 状态卫生（A+B 合并）

> **状态**：`done（2026-06-08 · PR #134 · Kimi Harness 试点 CLOSE）`  
> **关联 Issue/PR**：[#134](https://github.com/Cyning12/ai-ink-brain-api-python/pull/134)  
> **Epic**：Kimi Code 执行器落地实验 · **非** docs-noise 业务续跑  
> **关联 SPEC 导图**：[`docs/spec/governance/docs-noise-inventory/README.md`](../../spec/governance/docs-noise-inventory/README.md) §6（治理线已 CLOSE · 本 task 仅排期卫生）  
> **对照实验**：Cursor P0 [`task_gov_docs_noise_p0_readme_v1.md`](task_gov_docs_noise_p0_readme_v1.md) · CC P1–P3 · Plan Agent 分析 [`docs/diary/2026-06-05-plan-agent-analysis/00_README.md`](../../diary/2026-06-05-plan-agent-analysis/00_README.md)  
> **freeze_id**：`GOV-KIMI-HARNESS-PILOT@2026-06-06`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `kimi_harness_pilot_recentsync_v1` |
| **orchestration** | **Kimi Code** · Lead 主会话 + 串行 `Agent()` · **Git 仅 Lead** |
| **semi_auto** | `false` — Kimi 试点须按 PROMPT 显式 spawn；禁止同会话裸换帽 |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs 排期/元数据；无 `api/` / 契约 / workflow 变更 |
| **audit_profile** | `post_close` |
| **git_branch** | `task/kimi-harness-pilot-recentsync-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **merge_policy** | `stop_before_merge` — CI 全绿后 **停** · 人审 Kimi 执行质量再 merge |
| **close_action** | `merge` — Cursor 复查通过后 Lead/Cursor 执行 `gh pr merge 134 --squash` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **experience_capture** | `required` |
| **experience_capture_note** | 关账已落盘 [`docs/diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md`](../../diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md) |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | 22-R1, 30 | task + PROMPT 人扫；Kimi 开跑前须 `approved` |
| HG-KIMI-PILOT-EXEC | approved | explore, 22, 30, 40, CLOSE | Kimi T1 执行链开干前人签 |

---

## 背景与目标

docs-noise 治理线 **P0–P3 + MANIFEST 已 CLOSE**，但 `RECENT_TASK_SCHEDULE.md` **§1.2** 仍写过期状态（MANIFEST 链 `active/`、P1「脚手架」、P2/P3 pending）。同时 RECENT **§6.3** 指出 `done/` 内部分文首状态日期待核对。

本 task **合并 A+B**：在 **Kimi Code Harness T1 链** 下完成排期同步 + 有限状态回填，验证 Kimi 作为第三执行器（对照 Cursor P0 / CC P1–P3）的可行性与耗时。

**完成态**：§1.2 与 `done/` 真值一致；Kimi 帽链 invoke/review 落盘；单 PR docs-only · CI Required 全绿。

---

## 范围

### A · RECENT §1.2 同步（必做）

| ID | 交付 | 文件 |
| --- | --- | --- |
| **A-1** | MANIFEST 链至 `done/task_governance_docs_noise_line_manifest_v1.md` | `docs/tasks/RECENT_TASK_SCHEDULE.md` §1.2 |
| **A-2** | P0–P3 子批表：状态 **done** + PR #121/#123/#126/#129 | 同上 |
| **A-3** | 执行器行：P0 **Cursor** · P1–P3 **Claude Code** · 注明治理线 **CLOSE** | 同上 |
| **A-4** | 删除「P1 脚手架 / 分支已开 / P2 P3 pending / active MANIFEST」等过期表述 | 同上 |
| **A-5** | §1.2 标题或段首注明：docs-noise **已 CLOSE**（2026-06-06） | 同上 |

### B · done/ 状态卫生（有条件 · 上限 10 文件）

| ID | 交付 | 约束 |
| --- | --- | --- |
| **B-1** | explore 用 `rg` 扫描 `docs/tasks/done/`，列出文首 `**状态**` 缺 PR 或缺日期的候选 | 交付 explore 报告 |
| **B-2** | **优先** 5 个 gov-docs-noise 线 task 统一为 `done（YYYY-MM-DD · PR #xxx @ commit）` 格式 | 见下表 |
| **B-3** | 其余 `done/` 候选 **最多再修 5 个**；若无合格候选则 **跳过** 并在 40 自检说明 | 禁止 glob 改全库 |

**B-2 固定文件清单（必核对）**：

- `docs/tasks/done/task_gov_docs_noise_p0_readme_v1.md`
- `docs/tasks/done/task_gov_docs_noise_p1_archived_v1.md`
- `docs/tasks/done/task_gov_docs_noise_p2_readorder_v1.md`
- `docs/tasks/done/task_gov_docs_noise_p3_index_v1.md`
- `docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md`

## 非范围

- 修改 `api/`、`tests/`、`.github/workflows/`
- 重跑 docs-noise C1–C6 业务或删 invoke/review 审计链
- 改 ChatBI / RAG active task
- Kimi **Plan Agent** 导航复验（独立实验 · 见 [`PROMPT_kimi_plan_agent_nav_revalidation_zh.md`](../../harness/prompts/PROMPT_kimi_plan_agent_nav_revalidation_zh.md) · **零业务 PR**）

---

## 验收标准

- [x] A-1～A-5：`RECENT §1.2` 与 MANIFEST / 子批 `done/` 真值一致
- [x] B-2：5 个 gov-docs-noise done task 状态行格式统一且含 PR 号
- [x] B-3：无额外回填；仅 5 个 B-2 文件 + RECENT，总计 6 文件 ≤10
- [x] Harness：`docs/harness/invokes/by-task/kimi-harness-recentsync/` 帽链齐全（explore + 22 + 30 + 40 共 5 invoke）
- [x] 单 PR · docs-only · CI Required 全绿（`task_validate` 含 failure_paths Scenario ID）· [#134](https://github.com/Cyning12/ai-ink-brain-api-python/pull/134)
- [x] 关账 diary：[`docs/diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md`](../../diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md)

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
| --- | --- | --- | --- |
| F1 | fp-kimi-pilot-scope-drift | Kimi 深读 `docs/spec/v3-agent/**` 或改 `api/` | **禁止**；explore/30 须停并回报 Lead |
| F2 | fp-kimi-pilot-readorder | RECENT 与 MANIFEST 仍指向 `active/` 路径 | 30 帽 **必须** 修正为 `done/` |
| F3 | fp-kimi-pilot-over-edit | B 段修改超过 10 个 `done/` 文件 | **禁止**；仅 explore 清单内文件 |
| F4 | fp-kimi-subagent-git | subagent 尝试 `git commit` | **禁止**；仅 Lead commit（PROMPT §5.2） |

---

## Kimi 试点说明（Round T1）

Harness **Lead**（Kimi 主会话）串行 `Agent()`：`explore` → `22` → `30` → `40` → `CLOSE` → PR → CI → **stop_before_merge**。

Invoke 落盘：`docs/harness/invokes/by-task/kimi-harness-recentsync/`

**Prompt 真值**：

- 通用模板：[`docs/harness/prompts/PROMPT_kimi_task_chain_serial_v1.md`](../../harness/prompts/PROMPT_kimi_task_chain_serial_v1.md)
- T1 实例：[`docs/harness/prompts/PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md`](../../harness/prompts/PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md)

**Kimi 硬约束**（每帽 spawn prompt **须全文内联**，不可假设子 Agent 已读 `AGENTS.md`）：

1. canonical 读序 + forbidden（见 PROMPT 实例 §2–§5）
2. 禁止 `git log` / `git blame`（30 帽）
3. wall-clock **>10 min** 须停并向 Lead 汇报
4. 回报 ≤10 行 · 禁止贴 subagent 全文

---

### 自检结论（执行者）

> **40 帽 + Cursor 终验** · 2026-06-08 · **建议 merge PR #134 + 归档 done/**

| 验收项 | 结果 |
| --- | --- |
| A RECENT §1.2 与 MANIFEST/done 一致 | ✅ |
| B-2 五文件状态行含 PR | ✅（Cursor 终验统一 P2/P3/MANIFEST 反引号格式） |
| B-3 ≤10 文件 | ✅ 跳过 11 候选 |
| Harness invoke + 22 R1 | ✅ 5 invoke + 1 review |
| CI Required 全绿 | ✅ PR #134 |
| diary 关账 | ✅ `2026-06-08-kimi-harness-pilot-recentsync_zh.md` |

**验证命令**：

```text
$ rg -n 'active/task_governance_docs_noise_line_manifest|脚手架|P2/P3.*pending' docs/tasks/RECENT_TASK_SCHEDULE.md
(无命中)
```

---

### KPI（00）

**rubric**: KPI_RUBRIC_v1_2 · **汇总**: **92%** · **状态**: **pass** · **帽**: explore · 22 · 30 · 40 · CLOSE · Cursor 终验  
**评诊日期**: 2026-06-08 · **简报**: [`docs/diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md`](../../diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md)

| hat_code | round | agent_mode | D1 | D2 | D3 | D4 | D5 | judgment_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| explore | T1 | kimi_agent | pass | pass | pass | pass | — | 差分完整；11 候选清单 |
| 22 | T1 | kimi_agent | pass | pass | pass | pass | — | R1 无阻塞；task_validate OK |
| 30 | T1 | kimi_agent | pass | pass | pass-with-notes | pass | — | B-2 格式初版略异；终验已修 |
| 40 | T1 | kimi_agent | pass | pass | pass | pass | — | 验收勾选 + rg 证据 |
| CLOSE | T1 | kimi_lead | pass | pass | pass | pass | pass | PR #134 · CI 全绿 · stop_before_merge 已人审 |
| Cursor | close | main_chat | pass | pass | pass | pass | pass | 终验 merge + git mv done |

**Task 级聚合**：D1 avg=100 · D2 min=100 · D3 avg=95 · D4 min=100 · D5 min=100  
**Task_KPI%** ≈ **92%**（Kimi 执行达标；关账文书 task 元数据由 Cursor 终验补齐）

**关账**：PR [#134](https://github.com/Cyning12/ai-ink-brain-api-python/pull/134) · 本 task 已归档 `done/` · `_views/done.md` 已更新（2026-06-08 Cursor 终验）。

---

## 给 Cursor / Kimi

`task_slug=kimi_harness_pilot_recentsync_v1` · `test_strategy=not_applicable` · `orchestration=Kimi Code` · 开跑前读 PROMPT T1 实例 §1 · `human_gate` 须预批。
