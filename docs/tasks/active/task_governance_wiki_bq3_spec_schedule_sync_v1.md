# Task：治理同步 — SPEC / RECENT B-Q3 Recheck（R3 · 合并）

> **状态**：draft  
> **母 Loop**：[`task_harness_wiki_loop_bq3_recheck_v1.md`](task_harness_wiki_loop_bq3_recheck_v1.md) · round **R3**  
> **说明**：合并 Loop A1–A4 的 A3+A4 职责为一 round（SPEC + 排期）

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；**本 round 负责** `RECENT_TASK_SCHEDULE.md` §6.6。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 治理文档与排期表；纯 docs。 |
| **freeze_id** | `GOV-WIKI-BQ3-SYNC@2026-05-26` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-bq3-recheck-v1` |
| **task_slug** | `wiki-bq3-r3-gov-sync` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 继承 [`HG-LOOP-BATCH`](task_harness_wiki_loop_bq3_recheck_v1.md) |

---

## 帽子顺序（**跳过 10** · Loop R3）

| 序 | 帽 | 启动 |
|----|-----|------|
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-bq3-recheck/PROMPT_LOOP_22_to_CLOSE_v1.md) · **round=R3** |

---

## 背景与目标

R1/R2 已更新实验证据与对比表。本 round **合并** 治理收口：SPEC 路线图下一步表、RECENT §6.6 Wiki 推广表、可选 SKILL 修订记录（**不**改 SKILL status）。

**完成态**：

- [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.1 增 **B-Q3 Recheck** 行或 §2 脚注 + 修订记录。  
- [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §6.6 增 **Wiki Loop B-Q3 Recheck** 行（关账时标 done）。  
- 可选：[`SKILL-harness-loop-batch.md`](../tasks/skills/SKILL-harness-loop-batch.md) 修订记录「第二 Loop 试点 @2026-05-26」；**禁止** Agent 将 status 改为 `accepted`。

---

## 范围

- [ ] 建议 R1–R2 已在 `done/`（非硬阻塞，但 22 应读 R2 交付）。  
- [ ] 更新 SPEC §5.1 + 修订记录。  
- [ ] 更新 RECENT §6.6 + §8 修订记录（若惯例需要）。  
- [ ] 关账时更新 `_views/done.md` 与本 Loop 三子 task 索引。  
- [ ] 22/40/50 落盘。

## 非范围

- Harness prompts / CI / api / tests。  
- 代改 SKILL `accepted`。  
- 重跑实验（R1 职责）。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | SPEC 与 R2 #46 矛盾 | 50 fail |
| F2 | RECENT 行写 done 但子 task 未全 done | 关账步骤阻塞 |
| F3 | Agent 改 SKILL → accepted | **禁止** · revert |

---

## 验收标准

- [ ] SPEC §5.1 链至本 Loop 母 task / done 路径。  
- [ ] RECENT §6.6 有 B-Q3 Recheck 行且状态正确。  
- [ ] SKILL status 仍为 `draft`（除非人另 commit）。

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | |
| RECENT 行文案 | |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| SPEC §5.1 | | |
| RECENT §6.6 | | |

---

## 给 Cursor

`SPEC-Governance`、`RECENT_TASK_SCHEDULE` §6.6、Loop R3、合并治理、SKILL draft
