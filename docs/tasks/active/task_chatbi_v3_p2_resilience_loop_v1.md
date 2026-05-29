# Task：ChatBI V3 P2 韧性 Loop — 关账 + 熔断（单 PR 编排母单）

> **状态**：in_progress  
> **schedule_ref**：RECENT §1.1 #L1 · **V3 当前棒（整合 Loop）**  
> **epic**：ChatBI V3 · P2 韧性  
> **关联 SKILL**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../skills/SKILL-harness-loop-batch.md)（**混合 Loop**：R1 docs · R2 `api/`）  
> **关联母单（拆单）**：[`docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`](done/task_chatbi_v3_p2_resilience_v1.md)  
> **10 帽 Batch**：[`docs/harness/invokes/by-task/chatbi-v3-p2-loop/PROMPT_BATCH_10_chatbi_v3_p2_loop_v1.md`](../harness/invokes/by-task/chatbi-v3-p2-loop/PROMPT_BATCH_10_chatbi_v3_p2_loop_v1.md)

> 落盘规则：R1、R2 子 task 均 `done/` 后本单 **META** 关账；`git mv` → `docs/tasks/done/` 并更新 `_views/done.md` · `REPORT_completion_*`。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；**R2** 子 task 为 `required` 实现；母单不直接改 `api/`。 |
| **freeze_id** | `CHATBI-P2-LOOP@2026-05-29` |
| **gates_before_code** | `["human_gate", "failure_paths", "子 task 顺序", "R1 已合 PR 留证"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |
| **worktree_root** | 主仓 `ai-ink-brain-api-python/`（**取消** 双轨 worktree） |
| **task_slug** | `chatbi-v3-p2-loop` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **approved** | 22-R1, 30, 40, 50 | **人** 批后启动 R1；子 task **继承母闸** |

> **子 task 继承**：R1/R2 仅继承 `HG-LOOP-BATCH`。**改 status 以母单为准**。

---

## 整合说明（为何本 Loop）

| 原轨 | PR | 本 Loop 承接 |
|------|-----|----------------|
| P2-1b 限流 | **#86** `29e88ba` | **R1** 归档 + RECENT 同步 |
| Wiki 验收扩充 W1 | **#87** `e6abdf6` | **R1** 同上（docs-only） |
| P2-1c 熔断 | — | **R2** 实现（`test_strategy: required`） |

**禁止**再开 `task/chatbi-v3-p2-1b-rate-limit` 或 `task/gov-wiki-milestone-acceptance-expand-v1` 独立 PR。

---

## 子 task 顺序（硬 · R1→R2→META）

| 序 | round | task 路径 | task_slug | freeze_id |
|----|-------|-----------|-----------|-----------|
| 1 | **R1** | [`task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md`](task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md) | `chatbi-v3-p2-loop-r1-closeout` | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` |
| 2 | **R2** | [`task_chatbi_v3_p2_resilience_circuit_breaker_v1.md`](task_chatbi_v3_p2_resilience_circuit_breaker_v1.md) | `chatbi-v3-p2-loop-r2-circuit-breaker` | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| 3 | **META** | 本文件 | `chatbi-v3-p2-loop` | `CHATBI-P2-LOOP@2026-05-29` |

**Manifest 真值**：[`docs/harness/invokes/by-task/chatbi-v3-p2-loop/LOOP_MANIFEST.md`](../harness/invokes/by-task/chatbi-v3-p2-loop/LOOP_MANIFEST.md)

**排期职责**：**R1 关账** 更新 RECENT §1.1（#0b/#W1 → done）；**META** 负责 §0 当前棒、§5 P2-1b/c 行、`task-schedule-ink-backend.md`、`REPORT_completion_*`。

---

## 帽子顺序（母单 · Batch 已起草 · 子单 **跳过 10**）

| 序 | 帽 | 说明 |
|----|-----|------|
| — | **10** | **本 Loop 已 Batch**；子 task **禁止** 再开 10 |
| 1 | **R1** | docs · **22 → 30 → 40**；50 **可选**（建议落盘 meta 摘要） |
| 2 | **R2** | `api/` · **22 → 30 → 40 → 50 必落盘** |
| 3 | **META** | R1+R2 均在 `done/` 后；因 R2 含 `api/`，META **须** 22→50 + `REPORT_completion_*` |

**执行纪律**：

- **单 PR**：`task/chatbi-v3-p2-loop-v1` → **一个 PR** 合 `main`。  
- **顺序**：**R1 → R2 → META**（R2 **须** R1 已将 #0b/#W1 迁入 `done/`）。  
- **禁止**（除非 R2 task 明示）：改 `docs/harness/prompts/` 帽子正文、无关 CI workflow。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | `HG-LOOP-BATCH` 仍为 `pending` | 硬停 · 输出 gate_id + 路径 |
| F2 | R2 在 R1 关账前改 `api/` | 50 fail · revert 或拆 PR |
| F3 | 双轨 worktree 与 Loop 分支混改 | 硬停 · 仅 `task/chatbi-v3-p2-loop-v1` |
| F4 | R2 无 50 即标 done | 验收 fail · 补 reinspect |

---

## 验收标准

- [ ] `HG-LOOP-BATCH` = **approved** 后启动 R1  
- [ ] R1：#0b/#W1 已 `git mv` → `done/` · `_views/done.md` · P2-1 母单子表同步  
- [ ] R2：熔断实现 + pytest + **50 落盘**  
- [ ] META：`REPORT_completion_chatbi_v3_p2_loop_v1.md` · RECENT §0/§1/§5 与 Wiki hub 一致  

---

## 给 Cursor

`chatbi-v3-p2-loop`、`CHATBI-P2-LOOP`、`harness-loop-batch`、P2-1b 关账、P2-1c 熔断、单 PR
