# Payload · H-lean（Representative 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `harness-wiki-loop-t4-l2` |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **generated** | 2026-05-27 · `python tools/wiki_ctx_ab_materialize_h_lean.py` |

## Agent 约束

只能依据下文作答。禁止 invoke/review 全文。禁止 `docs/coding_wiki/*`。

---

## 载荷正文

--- FILE: docs/harness/README.md ---
## 1. 日常读什么

| 场景 | 路径 |
|------|------|
| 写 task / **下一棒双 Prompt** | `TEMPLATE-requirements`（**A:22** + **B:30**，人择一） |
| 任务审核 22 | [`reviews/README.md`](reviews/README.md) → `TEMPLATE-task-audit` |
| 执行 + 自检 | `TEMPLATE-execute` → `TEMPLATE-self-check` |
| **三方复检** | `TEMPLATE-independent-reinspect` → [`../tasks/reinspect_results/`](../tasks/reinspect_results/README.md) |
| 半自动 / 人工闸 | `HANDOFF_SEMI_AUTO` |
| commit / 关账 | `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE` |
| task 字段 | `HARNESS_V2_PLAN.md` §5 |
| 流程 | `SDD_HAT_FLOW.md` |
| 新 invoke | `invokes/` |
| **Harness 裁决共识（已接受）** | [`../diary/2026-05-22-harness-evaluation-improvement-response.md`](../diary/2026-05-22-harness-evaluation-improvement-response.md) **§九** |

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc`、`.cursor/rules/06-harness-in-repo.mdc`。

**Agent 禁止（日常）**：

- **禁止** 默认读取工作区 `Projects/docs/harness/`（跨子仓 Harness 任务除外，见 `docs/tasks/README.md`）。
- **禁止** 将子仓 `prompts/` 软链到工作区；真值以 **本仓** `docs/harness/prompts/` 为准。
- **禁止** 在任务执行中运行下文 **§4 `rsync`**（仅维护者偶发同步）。

---

### 2.1 落盘 taxonomy（**已迁移** · 2026-05-25）

**原则**：**按 task 绑定**落盘（`invokes` / `reviews` / `reinspect_results` 已按 task 语义）；**不按业务域分顶层目录**。域知识进 **LLM Wiki**（`task_coding_wiki_pilot_v1`），不进 `prompts/domains/`。

| 树 | 目标路径 | 内容 |
|----|----------|------|
| **prompts** | `prompts/hats/` | `10-requirements` … `50-independent-reinspect` |
| | `prompts/templates/` | `TEMPLATE-*-invoke.md` |
| | `prompts/handoff/` | `HANDOFF_*.md` |
| **invokes** | `invokes/by-task/<task_slug>/` | `invoke_YYYYMMDD_<帽号>_<slug>.md`（见 [`invokes/README.md`](invokes/README.md)） |
| **reviews** | `reviews/by-task/<task_slug>/` | `task_<slug>_audit_R<轮次>_YYYYMMDD.md`（见 [`reviews/README.md`](reviews/README.md)） |
| **50（不变）** | `docs/tasks/reinspect_results/` | 关账复检；文件名可含 task slug |

**为何不建 `prompts/domains/chatbi` 或 `domains/tech-graph`？**

- Harness 文件描述的是**帽序与 HANDOFF 协议**，与「ChatBI / 图谱」等业务域 **正交**；同一 task 常跨多域。
- 按域拆目录会导致：同一 `invoke` 难归类、Agent 误把域片段当关账真值。
- **若将来**需要跨 task 复用的 Prompt **片段**，再用 `prompts/snippets/<domain>/`（可选），与 Wiki 词条分工，**仍不**替代 `by-task/` 落盘。

**新落盘**：invoke / review **必须**进 `by-task/<task_slug>/`；prompts 从 `hats/`、`templates/`、`handoff/` 读取（勿在 `prompts/` 根新增帽文件）。

**落地 task**：[`docs/tasks/active/task_coding_wiki_pilot_v1.md`](../tasks/active/task_coding_wiki_pilot_v1.md) · [`task_wiki_ctx_ab_v1.md`](../tasks/active/task_wiki_ctx_ab_v1.md)（Wiki-CTX-AB）。

**实验（P1 题集 / payload 模板）**：[`experiments/wiki_ctx_ab_v1/`](experiments/wiki_ctx_ab_v1/README.md) · SPEC [`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)。

---

--- FILE: docs/harness/invokes/README.md ---
## 命名

`invoke_YYYYMMDD_<帽号>_<slug>.md`（例：`invoke_20260525_30_chatbi-v3-p2-1a-health.md`）

## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。
## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状（2026-05-25）** | 已迁至 `invokes/by-task/<task_slug>/` |
| **新文件** | 仅落 `invokes/by-task/<task_slug>/invoke_*.md`（例 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。

## 规则（摘要）

1. **同一帽**多轮追问 **不** 重复落盘；换帽才新建文件。

--- FILE: docs/tasks/done/task_harness_wiki_loop_t4_l2_v1.md ---
# Task：Wiki Loop T4 + L2 工具链 — 单 PR 编排母单（第四轮 · 真实业务）

> **状态**：done  
> **META 关账日期**：2026-05-27  
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
- [x] R1→R2→R3 按上表顺序各走完整 22→30→40→50→关账链。  
- [x] 各 round invoke **C2 全绿**。  
- [x] 三轮子 task 均 `git mv` 至 `docs/tasks/done/` 并更新索引。  
- [x] 母 task META 关账 + `REPORT_completion_*` §1～§5 落盘。

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

--- FILE: docs/tasks/RECENT_TASK_SCHEDULE.md ---
| **active/**           | **9** 个任务相关文件（见 §1.1；Wiki Loop A1–A4 已归档）                                                               |
> **SPEC 真值**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)（T0～T4）  
| **Wiki Loop A1–A4** | **`task_harness_wiki_loop_a1_a4_v1`** + 四子 task | **done** | 2026-05-26 · [`done/task_harness_wiki_loop_a1_a4_v1.md`](done/task_harness_wiki_loop_a1_a4_v1.md) · test_strategy ingest + SPEC/排期同步 · 单 PR `task/wiki-loop-a1-a4-v1` |
| **Wiki Loop B-Q3 Recheck** | **`task_harness_wiki_loop_bq3_recheck_v1`** + 三子 task | **done** | 2026-05-26 · [`done/task_harness_wiki_loop_bq3_recheck_v1.md`](done/task_harness_wiki_loop_bq3_recheck_v1.md)（关账后）· B-Q3 Recheck · 单 PR `task/wiki-loop-bq3-recheck-v1` · 第二 Loop 试点 |
| **Wiki Loop C2 Verify** | **`task_harness_wiki_loop_c2_verify_v1`** + 两子 task | **done** | 2026-05-26 · [`done/task_harness_wiki_loop_c2_verify_v1.md`](done/task_harness_wiki_loop_c2_verify_v1.md)（META 关账后）· invoke C2 全绿 · 单 PR `task/wiki-loop-c2-verify-v1` · 第三 Loop |
| T4 | 图谱桥接 / `graph_nodes` | **draft**（Pilot done → 3 slug 扩面） | 链 `SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` · Pilot `query-rewrite-observability` + `chatbi-v3-text2sql-tool-latency-obs` + `tech-graph-gate-d-v2-tasks` · `gov-wiki-t4-expand` |
| **T4+L2** | **Wiki Loop T4+L2** | **done** | `task_harness_wiki_loop_t4_l2_v1` · R1→R2→R3 全关账 · freeze `WIKI-LOOP-T4-L2@2026-05-27` |
| **T4 expand** | **`task_governance_wiki_t4_expand_v2`** | **done** | Post-Pilot · 3 篇 synthesis `graph_nodes` · 单 task · 分支 `task/gov-t4-l2-followup-v1` · `GOV-T4-EXPAND@2026-05-27` |
| **L2 Phase B** | **`task_governance_l2_manifest_ci_v1`** | **done** | manifest ≥12 + `tech_graph_test_manifest_check` + CI · 单 task · 分支 `task/gov-l2-manifest-ci-v1` · `GOV-L2-MANIFEST-CI@2026-05-27` |
| 2026-05-26 | **Wiki Loop A1–A4 done**：四子 task + 母单关账 · §1/§6.6 同步 · `WIKI-LOOP-A1-A4@2026-05-26` |
| 2026-05-26 | **Wiki Loop B-Q3 Recheck done**：R1–R3 子 task + 母单关账 · §6.6 同步 · `WIKI-LOOP-BQ3-RECHECK@2026-05-26` · 第二 harness-loop-batch Loop |
| 2026-05-26 | **Wiki Loop C2 Verify in_progress**：R1 RECENT §6.6 draft 行 · `WIKI-C2-R1-SCHEDULE@2026-05-26` · 第三 Loop invoke C2 试点 |
| 2026-05-26 | **Wiki Loop C2 Verify done**：R2 RECENT §6.6 done + invoke README · `WIKI-C2-R2-INDEX@2026-05-26` · R1/R2 invoke C2 全绿 |
| 2026-05-27 | **Wiki Loop T4+L2 done**：R1→R3 子 task + 母单关账 · §6.6 T4+L2 行 · `WIKI-LOOP-T4-L2@2026-05-27` · 第四 harness-loop-batch 真实业务 Loop |
| 2026-05-27 | **T4 扩面 + L2 Phase B 拆单**：`task_governance_wiki_t4_expand_v2` · `task_governance_l2_manifest_ci_v1` · 两单 task 并行（非 Loop） |
| 2026-05-27 | **gov-wiki-t4-expand done**：T4 扩面 3 synthesis graph_nodes · reinspect pass · Harness 帽链追溯补全 |
| 2026-05-27 | **gov-l2-manifest-ci 30 编码**：manifest 12 entries + `tech_graph_test_manifest_check.py` + pytest + workflow + 99_spec VERIFY |
| 2026-05-27 | **gov-l2-manifest-ci done**：PR #70 merge · L2 Phase B CI · Harness hygiene Part A（task done 正文 · invoke §3 · H5 引用） |

---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | 11977 |
| `file_count` | 4 |
| `notes` | H-lean：README §1+§2.1 + invokes README 摘录 + done task 全文 + RECENT 关键词行 |
