# Task：治理 — L2 Phase C 双向校验实现（单元 B · 单 task 全链）

> **状态**：done（2026-05-28 · 单元 B 关账 · PR-B [#80](https://github.com/Cyning12/ai-ink-brain-api-python/pull/80) · CI [#81](https://github.com/Cyning12/ai-ink-brain-api-python/pull/81)）  
> **单元**：**B** · [`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md) §3  
> **设计真值**：[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) §4.4  
> **执行入口**：[`PROMPT_START_full_chain_v1.md`](../../harness/invokes/by-task/gov-l2-phase-c-impl/PROMPT_START_full_chain_v1.md) · [`PROMPT_TASK_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/gov-l2-phase-c-impl/PROMPT_TASK_22_to_CLOSE_v1.md)  
> **执行备注**：**PR-B** · 分支 **`task/wiki-unit-ab-plan-v1`** · `git pull origin main` 后开工 · **Claude Code**

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
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1, 30 | SPEC §4.4 + 本 task 人扫 · **开工前须 approved** |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 |
| HG-REINSPECT | approved | done | 50 后人签 · **PR-B 合并前** |

---

## 背景与目标

P2 Loop R2 仅落盘 **Phase C design**（§4.4）。本 task 在 **Phase B** `tech_graph_test_manifest_check.py` 之上实现 **双向** 校验（§4.4.4 **C1–C3**），不扩大 Wiki coverage 真值边界。

**完成态**：

- `tools/tech_graph_test_manifest_check.py`：`--check-failure-paths`（或等价子命令）· 默认模式行为不变  
- `tests/`：双向模式 **可失败** 用例  
- `docs/_tech_graph/99_spec.md`：VERIFY 表增 Phase C 行  
- （可选）`_test_manifest.json` 增 ≤3 条 · 与下表 C2 抽样一致  
- **禁止** 改 `docs/coding_wiki/`（属单元 A · 已在 PR-A）

---

## 范围

- [x] `--check-failure-paths` 实现 + 默认检查仍绿  
- [x] pytest 绿（AGENTS.md 合并前命令）  
- [x] 22→30→40→**50**→关账 · `reinspect_gov-l2-phase-c-impl_20260528_v1.md`  
- [x] **PR-B** diff 仅 `tools/`、`tests/`、`docs/_tech_graph/`（manifest / 99_spec）

## 非范围

- 全仓历史 task 一次性扫完（C2 **抽样 ≥3** 即可）  
- Wiki lint CI · Harness 帽子正文 · 与单元 A 同 PR

---

## C2 抽样对照表（硬 · 30/22 落盘）

| manifest `id` | `failure_path_ref` | Epic |
| --- | --- | --- |
| `FP-RAG-DB-DISCONNECT` | `docs/tasks/done/task_05_query_rewrite_observability.md` | RAG / task_05 |
| `FP-SQL-GATE-DENIED` | `docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md` | ChatBI SQL gate |
| `FP-HEALTH-PROBE-FAIL` | `docs/tasks/done/task_chatbi_v3_p2_resilience_health_ready_v1.md` | P2-1a health |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | manifest 有 id 无对应 failure_path | check exit 1 | 修 manifest 或 task |
| F2 | task F# 无 manifest 且无 exempt | check exit 1 | 补条目 |
| F3 | pytest 未绿 | 禁止 done / 合并 PR-B | 修测 |
| F4 | PR-B 含 `docs/coding_wiki/` 批量变更 | 50 fail · 拆 PR | revert |

---

## 验收标准（SPEC §4.4.4）

- [x] **C1**：`--check-failure-paths` exit 0 · CI `tech-graph.yml` 仍绿  
- [x] **C2**：上表 3 Epic 对照表在 review/invoke  
- [x] **C3**：§4.2 Wiki≠coverage 审查通过  
- [x] **PR-A 已合 main**（#79）  
- [ ] （建议）`skill_cross_platform_v1` case `gov-l2-phase-c-impl_claude-code_<date>`

---

## VERIFY

```bash
python tools/tech_graph_test_manifest_check.py
python tools/tech_graph_test_manifest_check.py --check-failure-paths
pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short
python tools/harness_human_gate_check.py --task docs/tasks/active/task_governance_l2_phase_c_impl_v1.md
```

---

## 给 Cursor / Claude Code

`gov-l2-phase-c-impl`、`GOV-L2-PHASE-C-IMPL`、PR-B、required、cc
