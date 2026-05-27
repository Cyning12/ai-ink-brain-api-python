# 任务审核 R1 · Wiki-CTX-AB 代表性扩面（6 slug · v1）

## 元信息

| 字段 | 值 |
|------|-----|
| **audit_round** | R1 |
| **task_path** | `docs/tasks/active/task_governance_wiki_ctx_ab_representative_v1.md` |
| **task_slug** | `wiki-ctx-ab-representative` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **git_branch** | `task/wiki-ctx-ab-representative-v1` |
| **invoke_snapshot** | `docs/harness/invokes/by-task/wiki-ctx-ab-representative/invoke_20260527_22_wiki-ctx-ab-representative-v1.md` |
| **关联 SPEC** | `docs/spec/governance/SPEC-Governance-Wiki-CTX-AB-Representative-v1.md` |
| **日期** | 2026-05-27 |

---

## 审查结论摘要

**零硬阻塞 · 准许 30 执行帽开工。**

四枚人工闸（`HG-TASK-DRAFT`、`HG-AUDIT-R1`、`HG-AB-REP-SLUGS`、`HG-AB-REP-RUN`）均为 **approved**；锁定 **6** slug 与 synthesis / done task 齐备；题集、阈值 T7/T8 与 P2/Multi 先例一致；实验目录骨架已就绪（`questions.md` · `scorecard.md` · `README.md`）。

---

## 已核对项

| # | 项 | 结果 |
|---|-----|------|
| 1 | task `test_strategy: not_applicable` + note | ✅ |
| 2 | `failure_paths` F1–F4 可操作 | ✅ |
| 3 | 非范围：不改 `api/` · 前端仓 · 新 ingest | ✅ |
| 4 | 6 slug synthesis `test -f` | ✅ 六页均存在 |
| 5 | 6 slug done task `test -f` | ✅ 见下表 |
| 6 | P2 基线只读 | ✅ `conclusion_p2_zh.md` accepted |
| 7 | Multi 2 slug 先例只读 | ✅ `conclusion_multi_slug_zh.md` |
| 8 | SPEC §3 T7/T8 聚合阈值 | ✅ ≥5/6 · 每 slug ≥30% / ≥3/4 |
| 9 | `questions.md` 每 slug Q1–Q4 + Q4 变体 | ✅ |
| 10 | W 物化脚本 | ✅ `python tools/wiki_ctx_ab_materialize_w.py --slug <slug>` 可执行 |
| 11 | H-lean 模板与 Multi 先例 | ✅ `wiki_ctx_ab_v1/payloads/TEMPLATE-H-lean.md` + Multi 物化实例可对齐 |
| 12 | `payloads/` 目录待 30 创建 | ✅ 非阻塞 |
| 13 | 对比表 #46 待 30 更新 | ✅ 非阻塞 |
| 14 | semi_auto 长链 + 人闸已批 | ✅ |

### done task 对照（SPEC §2.1）

| slug | done task |
|------|-----------|
| `harness-p1-docs-consolidation` | `task_harness_p1_docs_consolidation_v1.md` |
| `tech-graph-gate-d-v2-tasks` | `task_engineering_tech_graph_gate_d_v2_tasks_v1.md` |
| `chatbi-v3-p2-health-ready` | `task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| `governance-l2-manifest-ci` | `task_governance_l2_manifest_ci_v1.md` |
| `wiki-ctx-ab-v1` | `task_wiki_ctx_ab_v1.md` |
| `harness-wiki-loop-t4-l2` | `task_harness_wiki_loop_t4_l2_v1.md` |

---

## 题集 spot-check（非阻塞备注）

| slug | Q | 核对 | 备注 |
|------|---|------|------|
| harness-p1 | Q4 | ✅ | synthesis：P1-1 工作区 reviews **非**本 Epic |
| tech-graph-gate-d | Q4 | ✅ | 禁止手改 `graph.json`；synthesis / done 一致 |
| chatbi-v3-p2 | Q2/Q4 | ⚠️ | `test_strategy: required`；Q4 前端 UI **非**范围 — 30 以 synthesis + done 为准 |
| governance-l2-manifest | Q4 | ✅ | Wiki **不能**替代 `_test_manifest` CI |
| wiki-ctx-ab-v1 | Q4 | ✅ | P2 **不可**外推 ChatBI 实现 |
| harness-wiki-loop-t4-l2 | Q4 | ✅ | 子 round **不可**跳过 invoke 落盘 |

**通用**：Q3 `freeze_id` / 关账日须与 synthesis frontmatter 或 done 头一致；W 臂 **禁止** 读 done/invoke 全文（F2）。

---

## 阻塞 / 非阻塞

**阻塞**：无。

**非阻塞**：

- `chatbi-v3-p2-health-ready` W 臂 Q2 依赖 synthesis 是否蒸馏 `test_strategy`（ingest 后通常有 frontmatter `required`）。
- `harness-wiki-loop-t4-l2` 为 **多 round** Epic，H-lean 字符量可能偏大；不影响 T7 相对比较。
- 30 物化 W 时须 **复制**至 `wiki_ctx_ab_representative_v1/payloads/`，**禁止覆盖** `wiki_ctx_ab_v1/payloads/` 冻结文件；`freeze_id` 头改为 `WIKI-CTX-AB-REP@2026-05-27`。

---

## 需任务帽回填清单

无。

---

## 是否建议执行帽开工

**是** — 准许 **30** 物化 12 payload、跑题、填 `scorecard.md`、撰写 `conclusion_representative_zh.md`、更新 `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` #46。

---

## 签收 / 关闭

本 R1 为 **执行前合同审查**；task **尚未** 关账。终轮签收待 **50 + 关账帽** 完成后与 task `done` 对齐。

---

## 下一棒可复制 Prompt

见 [`docs/harness/invokes/by-task/wiki-ctx-ab-representative/PROMPT_30_startup_wiki-ctx-ab-representative-v1.md`](../../../invokes/by-task/wiki-ctx-ab-representative/PROMPT_30_startup_wiki-ctx-ab-representative-v1.md) 内 `text` 代码块全文。
