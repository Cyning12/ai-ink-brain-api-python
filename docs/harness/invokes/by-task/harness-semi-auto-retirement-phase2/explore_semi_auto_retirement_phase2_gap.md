# Explore · semi_auto 物理退场 Phase 2（G3）· 只读差分

> **帽**：explore（Harness explore-l0）  
> **task**：[`task_harness_semi_auto_retirement_phase2_v1.md`](../../../../tasks/active/task_harness_semi_auto_retirement_phase2_v1.md)  
> **freeze_id**：`GOV-HARNESS-SEMI-AUTO-RETIRE-P2@2026-06-08`  
> **日期**：2026-06-08  
> **范围**：canonical 读序 1～9 · **禁止** `api/` · `tests/` · `.github/`

---

## 执行摘要

A+B 双轨已 CLOSE（MANIFEST · RECENT §1.3），但治理层仍将 `semi_auto` 作为一等公民：`SPEC` 状态行含「待 B 轨」、`RECENT` §0.0 关账表仍以 `semi_auto: true` 为常模、`HANDOFF_SEMI_AUTO` 与 `05-harness-semi-auto.mdc` 无 **DEPRECATED** 横幅且后者 `alwaysApply: true`。P2-1～P2-8 **均未交付**；`prompts/README` 与 MANIFEST 已有 Phase 2 索引骨架（G1 遗留）。

---

## P2-1～P2-8 逐项缺口表

| ID | 交付目标 | 当前状态 | 缺口 / 证据 |
| --- | --- | --- | --- |
| **P2-1** | SPEC 状态 → **全面生效**；§0/§1 完成态与缺口段更新（B 轨已 CLOSE） | **未改** | 状态行 L5：`accepted`（A 轨 30 帽定稿 · **待 B 轨齐 CLOSE 后全面生效**）。§0 L15：仍写「全面废弃须 **A+B 齐 CLOSE**」未标已完成。§1 L28：缺口仍列「无 api + required + 50 链式关账（→ **B 轨**）」— B 轨已 done（#137/#138）。 |
| **P2-2** | `HARNESS_V2_PLAN` §5.6 + 关账常模：`semi_auto` 标 **deprecated**（保留对照表） | **部分** | §5.6 L135–147：标题为「semi_auto **过渡/废弃**」，对照表保留，**无** `deprecated` 关键字或 DEPRECATED 横幅。§0.2 L20 仍链 `HANDOFF_SEMI_AUTO` 为常模之一。注：本文件无 `§0.0` 关账表（该表在 RECENT，见 P2-6）。 |
| **P2-3** | `HANDOFF_SEMI_AUTO.md` 文首 **DEPRECATED** + 链式替代读序 | **未改** | 文首 L1–5 仍为正常「用途」说明，**无** DEPRECATED。L5 链 `HARNESS_V2_PLAN` §5.5–§5.6，未 pointer `PROMPT_*_chain_serial_*` / `HANDOFF_CLOSE_TRACE` 为默认。 |
| **P2-4** | `05-harness-semi-auto.mdc` deprecated；`06` 指向链式规则 | **未改** | `05` L1–3：`alwaysApply: true`，description「半自动续跑」，**无** deprecated。`06` L8–9、L15：仍写「`semi_auto` 续跑」并链 `05-harness-semi-auto.mdc` 为细则，未升链式 SPEC 为默认。 |
| **P2-5** | `TASK_TEMPLATE`：`semi_auto` 行标 deprecated；新建 task 须 `orchestration` + 链 PROMPT | **部分（G1）** | L22：`semi_auto` 已注「过渡/废弃」+ 链 SPEC pointer，**未**标 **deprecated**。L23：`orchestration` 字段已存在。L9 真值链仍优先 `HANDOFF_SEMI_AUTO`。 |
| **P2-6** | `docs/tasks/README` · `AGENTS.md` · RECENT §0.0 + §1.4 同步 | **部分** | RECENT §1.4 L158–169：Phase 2 行 **in_progress**（结构 OK，关账后待更新）。§0.0 L20–30：关账表列名仍「`semi_auto: true` 时」— **常模残留**。`AGENTS.md` L14：Harness 必读仍含「**半自动**」。`docs/tasks/README.md` L32–34：「**半自动通则**」+ `HANDOFF_SEMI_AUTO`。 |
| **P2-7** | `governance/README` · `prompts/README` 补 Phase 2 索引 | **部分** | `governance/README` L9、L33：Chain SPEC 为 `accepted` · Epic **A 轨**，**无** Phase 2 G3 物理退场完成态。`prompts/README` L29、L47：已有 Phase 2 G3 PROMPT 与 v11 修订记录 — **索引骨架有，关账态缺**。 |
| **P2-8** | MANIFEST `done/` 补 Phase 2 状态行（CLOSE 后标 done） | **部分** | `task_harness_semi_auto_retirement_manifest_v1.md` L33–39：Phase 2 G3 **`in_progress`**，证明列待填 DEPRECATED/SPEC 全面生效 — **关账前预期态，非完成态**。 |

---

## SPEC「待 B 轨」核查

| 位置 | 片段 | 判定 |
| --- | --- | --- |
| `SPEC-Governance-Harness-Chain-Orchestration-v1.md` L5 | `待 B 轨齐 CLOSE 后全面生效` | **仍写「待 B 轨」** — 与 §1.3 A+B done 矛盾 |
| 同文件 L15 | `全面废弃须 A（本文）+ B（api 链式试点）齐 CLOSE` | 未更新为「A+B 已 CLOSE · Phase 2 治理层退场进行中」 |
| 同文件 L28 | 缺口「无 api + required + 50」（→ B 轨） | B 轨已关账，缺口段 **过时** |

**结论**：SPEC **仍写「待 B 轨」**；40 帽须按 task F4（`fp-p2-spec-stale-gate`）在 CLOSE 前清零。

---

## §0.0 `semi_auto` 常模残留

| 文件 | 行号 | 现状 |
| --- | --- | --- |
| `docs/tasks/RECENT_TASK_SCHEDULE.md` | L20–30 §0.0 | 表头「关账链（**`semi_auto: true` 时**）」— 默认常模仍锚定半自动 |
| 同文件 | L124 | 「Harness 关账 · **常模**：`required` → 50」未区分链式 `orchestration` |
| `docs/harness/HARNESS_V2_PLAN.md` | L20 §0.2 | 仍列 `semi_auto` 链式戴帽与 `HANDOFF_SEMI_AUTO` |
| `docs/harness/HARNESS_V2_PLAN.md` | L135–147 §5.6 | 对照表保留 `semi_auto: true` 列，未标 deprecated |

**目标（task P2-2/P2-6）**：§0.0 改链式 `orchestration` 为默认关账常模；`semi_auto` 仅作历史对照 + deprecated 注记。

---

## HANDOFF_SEMI_AUTO / `05-harness-semi-auto.mdc` DEPRECATED 核查

| 工件 | DEPRECATED 横幅 | 链式替代 pointer | 备注 |
| --- | --- | --- | --- |
| `HANDOFF_SEMI_AUTO.md` | **无** | **无**（文首） | 全文 290 行仍作活跃 Guides |
| `.cursor/rules/05-harness-semi-auto.mdc` | **无** | **无** | `alwaysApply: **true**` — Cursor 仍默认注入半自动纪律 |
| `.cursor/rules/06-harness-in-repo.mdc` | — | **无** | L15 仍「半自动续跑细则见 05」 |

全仓 `rg DEPRECATED`（`*.md` / `*.mdc`）：**零命中**。

---

## 30 帽执行建议（优先级）

| 优先级 | 动作 | 文件 | 理由 |
| --- | --- | --- | --- |
| **P0** | 更新 SPEC 状态 + §0/§1 完成态 | `SPEC-Governance-Harness-Chain-Orchestration-v1.md` | 消除「待 B 轨」；40 F4 硬门禁；其余文档引用此 SPEC |
| **P0** | RECENT §0.0 关账常模改链式 | `RECENT_TASK_SCHEDULE.md` | 排期真值；Agent 默认读 RECENT |
| **P1** | `HANDOFF_SEMI_AUTO` + `05` deprecated 横幅 + pointer | handoff + `.cursor/rules/05` | 物理退场核心；`05` 可保留文件但须降 alwaysApply 或文首声明只读考古 |
| **P1** | `06-harness-in-repo` 默认读序改链式 | `.cursor/rules/06-harness-in-repo.mdc` | 与 P2-4 联动；新 task 不再默认 semi_auto |
| **P1** | `HARNESS_V2_PLAN` §5.6 deprecated 注记 | `HARNESS_V2_PLAN.md` | 字段真值；TASK_TEMPLATE 已链本节 |
| **P2** | `TASK_TEMPLATE` semi_auto 行标 deprecated | `TASK_TEMPLATE.md` | G1 已部分完成，增量小 |
| **P2** | `AGENTS.md` + `docs/tasks/README` Harness 指针 | 两文件 | 入口导航；依赖 P0–P1 文案冻结 |
| **P2** | governance / prompts README Phase 2 关账行 | 两 README | 索引闭环 |
| **P3（CLOSE）** | MANIFEST Phase 2 → done + RECENT §1.4 关账 + task `git mv` | MANIFEST · RECENT · active task | P2-8；须 40 通过后 |

**30 帽纪律**：单 PR docs-only；禁止删 `HANDOFF_SEMI_AUTO` / `05` 全文；改后跑 `python tools/harness_task_validate.py docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md`。

---

## 已就绪（无需 30 重复建设）

- task `human_gate`：`HG-TASK-DRAFT` · `HG-CHAIN-P2-EXEC` 均为 **approved**（2026-06-08）
- T1 PROMPT · invoke 目录 · slug `harness-semi-auto-retirement-phase2` 已存在
- MANIFEST §1.3 A+B done；`TASK_TEMPLATE` 已有 `orchestration` 字段（G1）
- `prompts/README` 已索引 Phase 2 PROMPT（v11）

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | explore 帽只读差分 · P2-1～P2-8 全未交付/部分 · 供 22-R1 与 30 帽 |
