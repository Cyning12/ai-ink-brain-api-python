# 任务审核 R1 · gov_docs_noise_p0_readme_v1

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_path** | `docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md` |
| **task_slug** | `gov_docs_noise_p0_readme_v1` |
| **audit_round** | `R1` |
| **audit_date** | `20260606` |
| **prev_review** | 无（首轮） |
| **invoke_snapshot** | `docs/harness/invokes/by-task/gov-docs-noise-p0/invoke_20260606_22_gov-docs-noise-p0.md` |
| **关联 SPEC** | `docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md` |
| **审查帽** | `22-task-audit` |
| **git_branch** | `task/gov-docs-noise-p0-v1` |
| **explore 差分** | `docs/harness/invokes/by-task/gov-docs-noise-p0/explore_C1-C3_diff_20260606.md` |

---

## 审查结论摘要

**零阻塞，R1 通过，建议 30 帽开工。** 本单为纯 docs 指针修正（C1–C3），范围清晰、非范围禁止删审计链；`test_strategy: not_applicable` 理由充分；explore 差分确认三处冲突均可最小扰动修复。

---

## 理论对齐检查表（P0 · 已核对项）

### §3.1 任务单最小字段

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 头部 Harness 元信息表：`test_strategy` 三选一 | ✅ `not_applicable` |
| 2 | `not_applicable` 时 `test_strategy_note` 非空 | ✅ 纯 docs 指针 |
| 3 | `failure_paths` ≥1 行 | ✅ 误删审计链 / AGENTS 不一致 |
| 4 | **非范围** 独立小节非空 | ✅ 禁止 api/tests/workflows |
| 5 | **验收标准** 含 **合并前必绿** 条 | ✅ CI Required 全绿 |
| 6 | `semi_auto` + `audit_profile` 已填 | ✅ `true` + `post_close` |

### §3.2 合并前 CI 验收条

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 验收含 PR workflow 全绿 | ✅ docs-only · CI Required |
| 2 | 40 自检 / PR 链接可核对 | ⏳ 30→40 阶段 |

### §Blocking · 高敏须人判断

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 触达 api/契约/manifest | N/A — 纯 docs |

### §3.3 独立复检（50）触发

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型匹配 | ✅ `not_applicable` + 纯 docs |
| 2 | `required` 且涉契约 → 50 落盘 | N/A |

**human_gate**：`HG-TASK-DRAFT` = `approved`；`HG-GOV-P0-EXEC` = `approved`。

---

## 阻塞

（无）

---

## 非阻塞

| 项 | 说明 |
| --- | --- |
| AGENTS 读序 | 本 task 不改 AGENTS，留 P2；不得引入新冲突 |
| explore 已核对 | C1/C2/C3 现状 vs 期望已落盘，30 可按清单执行 |
| audit_profile | `post_close` — 关账后人审 |

---

## 需任务帽回填清单

（无）

---

## 是否建议执行帽开工

**是。** 30 帽可按 explore 改动清单执行 C1–C3 + SPEC §3 状态更新。

---

## 签收 / 关闭

R1 **通过**；本 task **可进入 30 执行帽**。终轮签收待 40 自检 + CLOSE。

---

## 下一棒可复制 Prompt

见 `docs/harness/invokes/by-task/gov-docs-noise-p0/invoke_20260606_30_gov-docs-noise-p0.md`（30 帽 invoke 落盘后执行）。
