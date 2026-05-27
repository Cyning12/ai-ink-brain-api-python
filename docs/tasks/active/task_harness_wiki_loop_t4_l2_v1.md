# Task：Wiki Loop T4 + L2 工具链 — 单 PR 编排母单（第四轮 · 真实业务）

> **状态**：active  
> **关联 SKILL**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../tasks/skills/SKILL-harness-loop-batch.md)（第四轮 · **T4 桥接 + L2 test manifest**）  
> **治理 SPEC（draft）**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) · [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md)  
> **10 帽 Batch**：见 [`docs/harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_BATCH_10_t4_l2_v1.md`](../harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_BATCH_10_t4_l2_v1.md) · invoke [`invoke_20260527_10_batch_t4_l2_v1.md`](../harness/invokes/by-task/wiki-loop-t4-l2/invoke_20260527_10_batch_t4_l2_v1.md)

> 落盘规则：三轮子 task 均 `done/` 后本单 META 关账；`git mv` → `docs/tasks/done/` 并更新 `_views/done.md`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 交付 docs/治理；母 task 不直接改业务正文。 |
| **freeze_id** | `WIKI-LOOP-T4-L2@2026-05-27` |
| **gates_before_code** | `["human_gate", "failure_paths", "子 task 顺序", "T4 先于 L2"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-spec-t4-l2-v1` |
| **task_slug** | `wiki-loop-t4-l2` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **approved** | 22-R1, 30, 40, 50 | 人批 2026-05-27；子 task 继承后可启动全链 |

---

## 子 task 顺序（硬 · R1→R2→R3→META）

| 序 | round | task 路径 | task_slug | freeze_id | 关账后回填 |
|----|-------|-----------|-----------|-----------|------------|
| 1 | **R1** | [`task_governance_wiki_t4_r1_pilot_v1.md`](task_governance_wiki_t4_r1_pilot_v1.md) | `wiki-t4-r1-pilot` | `GOV-T4-R1-PILOT@2026-05-27` | — |
| 2 | **R2** | [`task_governance_wiki_t4_r2_l0_align_v1.md`](task_governance_wiki_t4_r2_l0_align_v1.md) | `wiki-t4-r2-l0-align` | `GOV-T4-R2-L0-ALIGN@2026-05-27` | — |
| 3 | **R3** | [`task_governance_l2_r3_test_manifest_v1.md`](task_governance_l2_r3_test_manifest_v1.md) | `gov-l2-r3-test-manifest` | `GOV-L2-R3-TEST-MANIFEST@2026-05-27` | — |
| 4 | **META** | 本文件 | `wiki-loop-t4-l2` | `WIKI-LOOP-T4-L2@2026-05-27` | 三轮均 `done/` 后关账 |

**Manifest 真值**：[`docs/harness/invokes/by-task/wiki-loop-t4-l2/LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-t4-l2/LOOP_MANIFEST.md)

**排期职责**：**R1** 负责 `RECENT_TASK_SCHEDULE.md` §6.6 **in_progress** 行；**R3 关账** 负责 RECENT 行 **done** + `_views/done.md` + invoke README 验收说明。

---

## 帽子顺序（母单 · **跳过 10** · Loop 关账）

| 序 | 帽 | 说明 |
|----|-----|------|
| — | **10** | **本 Loop 已 Batch 起草**；子 task **禁止** 再开 10 |
| 1–3 | **R1–R3 各轮** | 每轮 **22 → 30 → 40 → 50 → 关账**；[`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_LOOP_22_to_CLOSE_v1.md) |
| 4 | **母关账** | 三轮子 task 均在 `done/` 后 META；输出 CLOSE_TRACE + `REPORT_completion_*` |

**执行纪律**：

- **单 PR**：合入 **`task/gov-spec-t4-l2-v1`**，最终 **一个 PR** 合 `main`。  
- **顺序**：**先 T4（R1→R2）再 L2（R3）**；R3 可引用 R1 `graph_nodes` 的 node id。  
- **禁止**：改 `api/`、`tests/`（**除** R3 仅新增/改 `_test_manifest.json` 与 docs）、`docs/harness/prompts/` 帽子正文、CI workflow。  
- **主验收**：各 round 交付项 + invoke **C2 全绿**（§3 ≥15 行 · 非 stub）。

---

## 背景与目标

治理 Roadmap **P2 · T4 / L2 工具链** 已有 draft SPEC（`b3a4c06` 起）；本 Loop 为 **harness-loop-batch 第四轮真实业务**，落地 T4 Pilot + L0 指针 + `_test_manifest` 草案，**非** A1–A4 / B-Q3 / C2 烟雾。

**母单完成态**：R1 T4 Pilot（1 页 synthesis + `CODING_WIKI`）；R2 T4 L0 对齐与 VERIFY；R3 L2 `_test_manifest`；META 关账 + `REPORT_completion_*`。

---

## 范围

- [x] `HG-LOOP-BATCH` 由 **人** 改 `approved` 后启动 R1 Loop。  
- [ ] R1→R2→R3 按上表顺序各走完整 22→30→40→50→关账链。  
- [ ] 各 round invoke **C2 全绿**。  
- [ ] 三轮子 task 均 `git mv` 至 `docs/tasks/done/` 并更新索引。  
- [ ] 母 task META 关账 + `REPORT_completion_*` §1～§5 落盘。

## 非范围

- Harness 烟雾（C2 Verify 类 RECENT-only round）。  
- 全站 syntheses 批量补 `graph_nodes`。  
- Phase B `tech_graph_test_manifest_check.py`（可 follow-up，非本 Loop 必须）。  
- 改 Harness 帽子 prompts 正文。

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | 母 `HG-LOOP-BATCH` = `pending` | 22 **拒开工** | 人批后 |
| F2 | R2 开工时 R1 未 `done/` | 22 **阻塞** | R1 关账后 |
| F3 | R3 开工时 R2 未 `done/` | 22 **阻塞** | R2 关账后 |
| F4 | R3 先于 R1/R2 交付 L2 | 50 **fail**（顺序违反） | 按 MANIFEST 重跑 |
| F5 | 子 task 越界改 `api/` / `tests/`（除 manifest 禁止项） | 50 fail · revert | 拆出 Loop |
| F6 | invoke stub（C2 fail） | 50 fail | 重写 invoke §3 |

---

## 验收标准

- [ ] 三轮子 task 路径与 MANIFEST 一致且均在 `done/`。  
- [ ] T4 VERIFY（Bridge SPEC §7）与 L2 VERIFY（L2 SPEC §7）在对应 round 40/50 重跑通过。  
- [ ] `docs/_tech_graph/_test_manifest.json` 存在且 ≥5 entries（R3）。  
- [ ] Pilot：`query-rewrite-observability` 含合法 `graph_nodes`（R1）。

---

## 实现备忘（执行者回填）

| 项 | 内容 |
| --- | --- |
| PR | （META 后填） |
| REPORT | `docs/harness/invokes/by-task/wiki-loop-t4-l2/REPORT_completion_*` |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| | | |

---

## 给 Cursor

`WIKI-LOOP-T4-L2`、`wiki-loop-t4-l2`、`GOV-WIKI-T4-BRIDGE`、`GOV-L2-ANCHOR-TEST-MANIFEST`、`graph_nodes`、`_test_manifest`、`HG-LOOP-BATCH`、`harness-loop-batch`
