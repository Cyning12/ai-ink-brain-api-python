# Task：治理 — L2 Phase C 双向校验实现（单元 B · 单 task 全链）

> **状态**：pending  
> **单元**：**B** · [`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md) §3  
> **设计真值**：[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) §4.4  
> **执行备注**：**PR-B** · 分支仍为 **`task/wiki-unit-ab-plan-v1`**（**PR-A 已合 main** 后 `git pull` 续跑）· **Claude Code**

> 落盘：验收后 `git mv` → `docs/tasks/done/`；**50 复检必落盘**（`test_strategy: required`）。

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **freeze_id** | `GOV-L2-PHASE-C-IMPL@2026-05-28` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **task_slug** | `gov-l2-phase-c-impl` |
| **executor** | `claude-code` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1, 30 | SPEC §4.4 + 本 task 人扫 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 后人签 |
| HG-REINSPECT | pending | done | 50 后人签 · **PR-B 合并前** |

---

## 背景与目标

P2 Loop R2 仅落盘 **Phase C design**（§4.4）。本 task 实现 **C1–C3**（§4.4.4），不扩大 Wiki coverage 真值边界。

**完成态**：

- `tools/tech_graph_test_manifest_check.py` 支持 **双向** 模式（如 `--check-failure-paths` 或子命令，与 Phase B 向后兼容）  
- `tests/` 覆盖新模式 **可失败** 路径  
- `docs/_tech_graph/99_spec.md` VERIFY 表增一行  
- （可选）`_test_manifest.json` 增 **≤3** 条与 done task `failure_paths` 对齐的条目  
- **禁止** 改 `docs/coding_wiki/` 批量 ingest（属单元 A）

---

## 范围

- [ ] 脚本双向校验（task F# ↔ manifest `id` / `error_codes`）  
- [ ] pytest 绿：`pytest tests -m "not intent_eval and not intent_benchmark"`  
- [ ] 22→30→40→**50**→关账 · `docs/tasks/reinspect_results/reinspect_gov-l2-phase-c-impl_<date>_v1.md`  
- [ ] **PR-B** 仅含 `tools/`、`tests/`、`docs/_tech_graph/`（manifest/99_spec）

## 非范围

- 全仓历史 task 一次性扫完（**抽样 ≥3 Epic** 即可，见 SPEC C2）  
- Wiki lint CI Required  
- 改 Harness 帽子正文  
- 与单元 A **同一 PR**

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | manifest 有 id 无对应 failure_path | check exit 1 | 修 manifest 或 task |
| F2 | task F# 无 manifest 且无 exempt | check exit 1 | 补条目或文档 exempt |
| F3 | pytest 未绿 | **禁止** 标 done / 合并 PR-B | 修测 |

---

## 验收标准（对齐 SPEC §4.4.4）

- [ ] **C1**：双向模式 exit 0（本地 + CI 既有 job 若已接 test manifest check）  
- [ ] **C2**：≥3 Epic task 与 manifest 行人工对照表在 invoke/review  
- [ ] **C3**：§4.2 Wiki≠coverage 审查通过  
- [ ] **PR-A 已合 main** 后再推 PR-B  
- [ ] （建议）`skill_cross_platform_v1` case `gov-l2-phase-c-impl_claude-code_<date>`

---

## VERIFY

```bash
python tools/tech_graph_test_manifest_check.py
python tools/tech_graph_test_manifest_check.py --check-failure-paths   # 实现后真命令以代码为准
pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short
```

---

## 给 Cursor / Claude Code

`gov-l2-phase-c-impl`、`GOV-L2-PHASE-C-IMPL`、PR-B、required、cc
