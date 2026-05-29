# Task：治理 — Wiki 单元 A/B 推广收口（P0 · docs-only）

> **状态**：done（2026-05-28）  
> **前置**：PR-A [#79](https://github.com/Cyning12/ai-ink-brain-api-python/pull/79)、PR-B [#80](https://github.com/Cyning12/ai-ink-brain-api-python/pull/80)、Phase C CI [#81](https://github.com/Cyning12/ai-ink-brain-api-python/pull/81) **已合 `main`**  
> **规划 SPEC**：[`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md)  
> **执行入口**：[`PROMPT_TASK_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/gov-wiki-unit-ab-closeout/PROMPT_TASK_22_to_CLOSE_v1.md)

> 落盘：**done** · `docs/tasks/_views/done.md` · `RECENT_TASK_SCHEDULE.md` §6.6 · `reinspect_gov-wiki-unit-ab-closeout_20260528_v1.md`

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 仅同步治理 SPEC / 排期 / 对比表与 SKILL 测评落盘；不改 `api/`、`tools/`、`.github/workflows/`。 |
| **freeze_id** | `GOV-WIKI-UNIT-AB-CLOSEOUT@2026-05-28` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读路径", "验收命令"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-wiki-unit-ab-closeout-v1` |
| **task_slug** | `gov-wiki-unit-ab-closeout` |
| **executor** | `claude-code`（建议 · 与 Unit A/B 同平台） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1, 30 | 人扫本 task + §范围 文件清单 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 落盘后人签 |
| HG-REINSPECT | approved | done | 50 落盘后人签 · 合并 PR 前 |

---

## 背景与目标

单元 A/B 与 L2 Phase C（含 CI）已在 `main` 落地，但 **Roadmap / Unit AB Plan / RECENT / 对比表** 仍残留 **in_progress、待执行、pending** 等表述，易导致后续 Agent **误开单元 B 或重复 PR**。

**完成态**：

1. 治理叙事与 **Git 真值**（#79–#81）一致：**Unit A/B done** · Phase C **implemented + CI Required**  
2. [`skill_cross_platform_v1`](../../harness/experiments/skill_cross_platform_v1/README.md) 补 **B 臂** case：`gov-l2-phase-c-impl_claude-code_<date>/`  
3. 22→30→40→**50**→关账 · invoke C2 全绿 · 单 PR **docs-only**

---

## 范围

### 必须改（勾选验收）

- [x] [`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md) §4 步骤 3–7 → **done**；§3 `task_governance_l2_phase_c_impl` 链至 `docs/tasks/done/`；修订记录 v1.2（#79–#81）  
- [x] [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.2「后端 P2 收口（A/B 双 PR）」→ **done**（PR #79/#80/#81）；RECENT §0「下一棒」→ **T4 / Batch-4 可选**  
- [x] [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §0 · §6.6 · §8 **Unit AB closeout**  
- [x] [`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) v1.5 · §7 Unit A/B + Phase C  
- [x] [`docs/harness/experiments/skill_cross_platform_v1/`](../../harness/experiments/skill_cross_platform_v1/) · `gov-l2-phase-c-impl_claude-code_20260528/`  
- [x] Harness：22 review · 30/40 invoke · `reinspect_gov-wiki-unit-ab-closeout_20260528_v1.md`

### 建议核对（无矛盾即可）

- [x] `SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.3 与 #81 一致（未改 design-only）  
- [x] `task_governance_l2_phase_c_impl_v1.md` 头部 PR #80/#81 链

## 非范围

- 改 `docs/coding_wiki/syntheses/` 正文（属 **Batch-4** 另单）  
- 改 `api/`、`tests/`、`tools/`、`.github/workflows/`  
- 改 `docs/harness/prompts/` 帽子正文  
- `coding_wiki_lint.py` CI Required（**P3**）  
- 全仓 `failure_path_ref` 真值化（**L2 manifest 提质** 另单）

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| Unit AB 规划 | `docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md` |
| Roadmap | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` |
| 已关 task | `docs/tasks/done/task_harness_wiki_loop_unit_a_v1.md` · `task_governance_l2_phase_c_impl_v1.md` |
| SKILL 测评 | `docs/harness/experiments/skill_cross_platform_v1/rubric_v1.md` |
| A 臂 case 参照 | `cases/wiki-loop-unit-a_claude-code_20260528/` |
| Harness | `docs/tasks/skills/SKILL-harness-task.md` · `SKILL-docs-governance.md` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | 范围文件仍写「单元 B 待执行 / in_progress」且与 `main` 矛盾 | 22 **阻塞**；列冲突表 | 是 | 审查阻塞 |
| F2 | diff 含 `api/`、`tools/`、`.github/workflows/` | 30 **拒开工** / 50 **fail** | 是 | PR 范围违规 |
| F3 | 未建 `gov-l2-phase-c-impl` SKILL case 即宣称关账 | 40/50 **fail** | 是 | 验收未过 |
| F4 | invoke §3 不足 15 行或无 commit 回溯 | C2 **fail** | 是 | Harness 阻塞 |

---

## 验收标准

- [x] §范围「必须改」全部勾选  
- [x] **零阻塞**：`rg` 在下列路径无「单元 B 待执行」「PR-B 待」「步骤 5 待」等残留（允许历史修订记录 **叙述** 过去态）  
  - `docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`  
  - `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.2  
  - `docs/tasks/RECENT_TASK_SCHEDULE.md` §0（非 §8 历史表）  
- [x] SKILL case 目录存在且 README 已索引  
- [x] 22→50 落盘完整 · `semi_auto` 链式执行  
- [x] 合并前：`pytest` 绿（242 passed）

**VERIFY**：

```bash
# 1) 残留措辞扫描（应无命中或仅 §8 历史行 — 若有命中须在 40 自检表说明）
rg -n "单元 B 待|PR-B 待|步骤 5.*待执行|A/B 双 PR.*in_progress" \
  docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md \
  docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md \
  docs/tasks/RECENT_TASK_SCHEDULE.md || true

# 2) main 已含 Phase C CI（只读核对）
rg -n "check-failure-paths" .github/workflows/tech-graph.yml

# 3) 合并前必绿
pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short

# 4) L2 manifest（回归 · 应有 failure-paths 步）
python tools/tech_graph_test_manifest_check.py
python tools/tech_graph_test_manifest_check.py --check-failure-paths

# 5) 关账前人闸（task 路径在 active/ 时）
python tools/harness_human_gate_check.py --task docs/tasks/done/task_governance_wiki_unit_ab_closeout_v1.md
```

---

## PR diff 白名单（硬）

| 允许 | 禁止 |
|------|------|
| `docs/spec/governance/` | `api/`、`tools/`、`tests/` |
| `docs/tasks/`、`docs/harness/`（invokes/reviews/reinspect + experiments） | `docs/coding_wiki/syntheses/` 批量 |
| `docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` | `.github/workflows/` |
| `docs/harness/experiments/skill_cross_platform_v1/` | `docs/harness/prompts/` 帽子正文 |

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | 见 `invoke_20260528_30_*` §2 |
| PR | 待开（本 task docs-only）· 前置 #79/#80/#81 已合 `main` |
| SKILL case | `cases/gov-l2-phase-c-impl_claude-code_20260528/` |
| reinspect | `reinspect_gov-wiki-unit-ab-closeout_20260528_v1.md` |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| VERIFY §1 `rg` 残留扫描 | **pass**（无命中） |
| VERIFY §2–§4 | **pass**（CI L31 · pytest 242 · manifest×2） |
| 结论 | **pass** |

---

## 给 Cursor / Claude Code

`gov-wiki-unit-ab-closeout`、`GOV-WIKI-UNIT-AB-CLOSEOUT`、P0、docs-only、`semi_auto`、`22→关账`、`skill_cross_platform`、`#79` `#80` `#81`
