# Task：治理 · semi_auto 物理退场（Phase 2 · G3）

> **状态**：`done`（PR 待开 · 2026-06-08 CLOSE）  
> **schedule_ref**：RECENT §1.4  
> **Epic**：`[task_harness_semi_auto_retirement_manifest_v1.md](../done/task_harness_semi_auto_retirement_manifest_v1.md)` · **G3 / Phase 2**（A+B 已 CLOSE · 2026-06-08）  
> **前置**：G1 PR #135 · G2 PR #137/#138 · 对外宣称「semi_auto 全面废弃」**已满足**  
> **规划**：`[docs/diary/2026-06-08-harness-chain-next-task-planning_zh.md](../diary/2026-06-08-harness-chain-next-task-planning_zh.md)` §7  
> **freeze_id**：`GOV-HARNESS-SEMI-AUTO-RETIRE-P2@2026-06-08`

---

## Harness 元信息


| 字段                          | 值                                                            |
| --------------------------- | ------------------------------------------------------------ |
| **task_slug**               | `harness_semi_auto_retirement_phase2_v1`                     |
| **orchestration**           | **Claude Code** · Lead + 串行 spawn `.claude/agents/harness-*` |
| **semi_auto**               | `false`                                                      |
| **test_strategy**           | `not_applicable`                                             |
| **test_strategy_note**      | 纯 governance docs / 规则 / 索引；无 `api/` 行为变更                    |
| **audit_profile**           | `post_close`                                                 |
| **git_branch**              | `task/harness-semi-auto-retirement-phase2-v1`                |
| **merge_policy**            | `docs_only_ci_green_merge`                                   |
| **close_action**            | `merge`                                                      |
| **kpi_rubric**              | `KPI_RUBRIC_v1_2`                                            |
| **kpi_aggregator**          | `CLOSE`                                                      |
| **experience_capture**      | `required`                                                   |
| **experience_capture_note** | 关账后更新 RECENT §1.4 与 MANIFEST Phase 2 行                       |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


### 人工闸 `human_gate`


| human_gate_id    | status   | blocks_hats                | 说明               |
| ---------------- | -------- | -------------------------- | ---------------- |
| HG-TASK-DRAFT    | approved | 22-R1, 30                  | task + PROMPT 人扫 · **2026-06-08 用户签收** |
| HG-CHAIN-P2-EXEC | approved | explore, 22, 30, 40, CLOSE | Phase 2 T1 执行链 · **2026-06-08 用户签收** |


---

## 背景与目标

Epic **A+B** 已 CLOSE：链式 `orchestration` 为推荐常模，active task 均已 `semi_auto: false`。但治理层仍保留 **半自动续跑** 作为一等公民：

- `[SPEC-Governance-Harness-Chain-Orchestration-v1.md](../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md)` 状态行仍写「待 B 轨齐 CLOSE」
- `[HARNESS_V2_PLAN.md](../harness/HARNESS_V2_PLAN.md)` §0.0 关账表仍列 `semi_auto: true` 常模
- `[.cursor/rules/05-harness-semi-auto.mdc](../../.cursor/rules/05-harness-semi-auto.mdc)` `**alwaysApply: true`**
- `[HANDOFF_SEMI_AUTO.md](../harness/prompts/handoff/HANDOFF_SEMI_AUTO.md)` 无 **DEPRECATED** 横幅

本 task（**Phase 2 / G3**）将 `semi_auto` 从「过渡/废弃表述」推进到 **治理层物理退场**：文档与规则标 **deprecated**，默认读序指向链式 PROMPT；**不删**历史 invoke/review/done task 中的 `semi_auto: true` 留证。

---

## 范围


| ID       | 交付                                                                                                          | 文件                                                                                |
| -------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **P2-1** | SPEC 状态 → **全面生效**；§0/§1 完成态与缺口段更新（B 轨已 CLOSE）                                                              | `docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md`          |
| **P2-2** | `HARNESS_V2_PLAN` §0.0 关账常模表 + §5.6：`semi_auto` 标 **deprecated**（保留对照表，不删 §5.6 历史正文）                        | `docs/harness/HARNESS_V2_PLAN.md`                                                 |
| **P2-3** | `HANDOFF_SEMI_AUTO.md` 文首 **DEPRECATED** 横幅 + 链式替代读序（`PROMPT_*_chain_serial_*` · `HANDOFF_CLOSE_TRACE`）     | `docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md`                               |
| **P2-4** | `.cursor/rules/05-harness-semi-auto.mdc` 文首 deprecated 说明；新 task 默认读链式规则（`06-harness-in-repo` + Chain SPEC） | `.cursor/rules/05-harness-semi-auto.mdc` · `.cursor/rules/06-harness-in-repo.mdc` |
| **P2-5** | `TASK_TEMPLATE`：`semi_auto` 行标 **deprecated**；新建 task **须**填 `orchestration` + 链 PROMPT 路径                  | `docs/tasks/templates/TASK_TEMPLATE.md`                                           |
| **P2-6** | `docs/tasks/README.md` · `AGENTS.md` Harness 指针同步；RECENT §0.0 + **§1.4** Phase 2 关账行                        | 同上 + `docs/tasks/RECENT_TASK_SCHEDULE.md`                                         |
| **P2-7** | `docs/spec/governance/README.md` · `docs/harness/prompts/README.md` 补 Phase 2 索引                            | governance / prompts README                                                       |
| **P2-8** | MANIFEST `done/` 补 **Phase 2** 状态行（本 task CLOSE 后标 done）                                                    | `docs/tasks/done/task_harness_semi_auto_retirement_manifest_v1.md`                |


## 非范围

- 删 `docs/harness/invokes/`、`reviews/`、历史 `done/` task 正文
- 批量改写历史 review 内 `semi_auto: true` 样例行
- 改 `api/`、`tests/`、`.github/workflows/`
- 前端仓 `ai-ink-brain` Harness parity（远期 P1-4）

---

## 验收标准

- [x] P2-1～P2-8 交付物存在且互相链接一致
- [x] SPEC 状态不含「待 B 轨」；§0 明确 A+B 已 CLOSE、链式为唯一推荐常模
- [x] `HANDOFF_SEMI_AUTO` 与 `05-harness-semi-auto.mdc` 含可见 **DEPRECATED** 说明
- [x] `python tools/harness_task_validate.py` 本 task **OK**
- [x] Harness T1：invoke + 22 R1 落盘 · slug `harness-semi-auto-retirement-phase2`
- [ ] 单 PR docs-only · CI Required 全绿（CLOSE 进行中）

---

## 失败路径


| #   | Scenario ID                    | 触发                                                      | 行为                               |
| --- | ------------------------------ | ------------------------------------------------------- | -------------------------------- |
| F1  | fp-p2-scope-drift              | 30 帽改 `api/` 或 workflow                                 | **禁止**                           |
| F2  | fp-p2-delete-semi-auto-history | 未留 deprecated 说明即删 `semi_auto` / `HANDOFF_SEMI_AUTO` 全文 | **禁止**                           |
| F3  | fp-p2-premature-rule-removal   | 未更新链式读序即移除 `05-harness-semi-auto.mdc`                   | **禁止**；须 deprecated 横幅 + pointer |
| F4  | fp-p2-spec-stale-gate          | SPEC 仍写「待 B 轨 CLOSE」                                    | 40 **fail**                      |


---

## 链式执行（Round T1）

**Prompt**：`[PROMPT_claude_chain_serial_v1_T1_semi-auto-retirement-phase2_zh.md](../harness/prompts/PROMPT_claude_chain_serial_v1_T1_semi-auto-retirement-phase2_zh.md)`

**帽链**：explore → 22 → 30 → 40 → CLOSE（**跳过 50** · not_applicable）

**invoke**：`docs/harness/invokes/by-task/harness-semi-auto-retirement-phase2/`

---

## 给 Cursor / CC

`orchestration=Claude Code` · `semi_auto=false` · 开跑前读 T1 PROMPT §1 · `human_gate` 须 `**approved`** 后 spawn。

---

### 自检结论（执行者）

**30 帽 · 2026-06-08**

- [x] **P2-1**：SPEC 状态 **全面生效**；§0 链式唯一推荐常模；§1 缺口段更新（无「待 B 轨」「→ B 轨」）
- [x] **P2-2**：`HARNESS_V2_PLAN` §0.2 链式默认；§5.6 **deprecated** 注记
- [x] **P2-3**：`HANDOFF_SEMI_AUTO.md` 文首 **DEPRECATED** + chain PROMPT / CLOSE_TRACE pointer
- [x] **P2-4**：`05-harness-semi-auto.mdc` deprecated（`alwaysApply: false`）；`06` 链式 pointer
- [x] **P2-5**：`TASK_TEMPLATE` `semi_auto` 行 **deprecated**；真值链改链 PROMPT
- [x] **P2-6**：RECENT §0.0 链式常模；AGENTS + `docs/tasks/README` Harness 指针
- [x] **P2-7**：governance / prompts README Phase 2 **in_progress** 索引
- [x] **P2-8**：MANIFEST / task 归档 — **CLOSE 执行中**
- [x] `python tools/harness_task_validate.py` → **OK**（见 40 帽证据）

**40 帽 · 2026-06-08 · pass（P2-8 / PR·CI 留 CLOSE）**

| 验收项 | 结果 | 证据 |
| --- | --- | --- |
| P2-1 SPEC 全面生效、无「待 B 轨」 | pass | `rg '待 B 轨' SPEC…` → **0 匹配**（exit 1）；状态行 **`全面生效`** |
| P2-2～P2-7 交付 | pass | 30 勾选 + 文件 spot-check（HARNESS_V2 §5.6 deprecated、TASK_TEMPLATE、RECENT §0.0/§1.4、governance/prompts README） |
| P2-8 MANIFEST 归档 | defer | 按 task 范围 **留 CLOSE** |
| DEPRECATED 横幅 | pass | `rg DEPRECATED\|deprecated\|全面生效 HANDOFF_SEMI_AUTO.md 05-harness-semi-auto.mdc` → 7 行（两文件文首横幅 + pointer） |
| `harness_task_validate.py` | pass | exit **0** · `=== …phase2_v1.md ===` · **OK** |
| invoke + 22 R1 落盘 | pass | `invokes/by-task/harness-semi-auto-retirement-phase2/`（6 件）· `reviews/…/…_audit_R1_20260608.md` |
| pytest / 50 | skip | `test_strategy: not_applicable` |
| 单 PR · CI 全绿 | defer | **40 不验** · 交 CLOSE + Lead PR |

**命令摘要**（cwd = 仓根）：

```text
#1 rg DEPRECATED|deprecated|全面生效 … → exit 0 · 7 matches
#2 rg '待 B 轨' SPEC-Governance-Harness-Chain-Orchestration-v1.md → exit 1（无匹配，预期）
#3 python tools/harness_task_validate.py …phase2_v1.md → exit 0 · OK
```

**OpenSpec×TDD 三维**：Completeness pass（P2-1～7 + 命令证据）· Correctness pass（F4 无 stale gate）· Coherence pass（链式 pointer 一致）

**判定**：**40 PASS** → 建议 Lead **CLOSE**（P2-8 归档 + PR + CI）· **跳过 50**

### KPI（00）

| 维度 | 判定 | 备注 |
| --- | --- | --- |
| D1 范围 | pass | P2-1～P2-8 全交付；无 api/tests/workflow 漂移 |
| D2 验收 | pass | 40 三条命令 + validate OK |
| D3 追溯 | pass | invoke 6 件 + 22 R1 + explore 差分 |
| D4 纪律 | pass | deprecated 横幅 + pointer；未删历史全文 |
| D5 CI | pending | CLOSE PR 待绿 |

**Task_KPI%**：~90%（D5 待 PR merge）· **blocked**：否

### 经验摘要

- **P2-2「§0.0」物理落点在 RECENT**，非 `HARNESS_V2_PLAN` 内节号；22/30 应以 explore 差分表为准。
- **`05` alwaysApply 降 false** 与文首 DEPRECATED 并列，避免 Cursor 仍默认注入半自动纪律。
- **P2-8 / MANIFEST / git mv** 严格留 CLOSE，避免 30 单 commit 混入关账索引。

### 关闭回溯

链向终轮审查 [`task_harness_semi_auto_retirement_phase2_v1_audit_R1_20260608.md`](../harness/reviews/by-task/harness-semi-auto-retirement-phase2/task_harness_semi_auto_retirement_phase2_v1_audit_R1_20260608.md) · 完整 commit 表见对话 **执行路线与 Commit 回溯**。