# Task：治理 — Coding Wiki 批量 Ingest（10 slug · v1）

> **状态**：done（2026-05-27 · GOV-WIKI-INGEST-BATCH@2026-05-27）  
> **前置**：T1b/T1c **done** · T4 扩面 **done** · L2 Phase B **done**  
> **SPEC**：[`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](../spec/governance/SPEC-Governance-Wiki-Ingest-Batch-v1.md)  
> **SKILL**：[`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../skills/SKILL-docs-governance.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6/§8。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 Wiki ingest；lint 用 SPEC §4 脚本；不改 pytest。 |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-wiki-ingest-batch-v1` |
| **task_slug** | `gov-wiki-ingest-batch` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22, 30 | SPEC + 10 slug 名单 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 |
| HG-INGEST-BATCH-SCOPE | approved | 30 | **锁定** SPEC §2 表 · 禁止擅自增删 slug |

---

## 长任务执行（单 task 全链 · 非 Loop Batch）

> **模式**：`SKILL-harness-task` · 30 帽可 **连续** 写完 10 页再 commit，或 **每 2～3 页** 一 commit；**同会话** 跑完 22→关账。  
> **人授权**：`human_gate` 已 **approved** → 无新 `pending` 前 **禁止** 每帽向人索要确认。

| 规则 | 内容 |
| --- | --- |
| **【授权】cross-hat** | 22→关账 同会话；10 页 ingest 属 **单次 30 帽** 交付 |
| **【禁止跳帽】** | invoke + commit 后方可 40 |
| **【停】** | F5 名单变更 · `graph_query` 对 graph_nodes 失败且无法修 · 拟改 api/tests |
| **关账前** | ST1–ST6 · 确认 syntheses 文件数 **≥15** |
| **入口** | [`PROMPT_START_full_chain_v1.md`](../../harness/invokes/by-task/gov-wiki-ingest-batch/PROMPT_START_full_chain_v1.md) |

---

## 帽子顺序

| 序 | 帽 | 启动 |
|----|-----|------|
| 0 | **10** | **跳过** |
| 1–5 | **22→关账** | `PROMPT_START` · `PROMPT_TASK_22_to_CLOSE_v1.md` §3 |

---

## 背景与目标

当前仅 **5** 篇 synthesis，不足以支撑推广体感。本 task 按 SPEC **锁定 10 slug** 批量 ingest，使 syntheses **≥15**（含既有 5）。

**完成态**：见 SPEC §0；`index.md` / `log.md` 同步；lint 通过。

---

## 范围（10 slug · 与 SPEC §2 一致）

- [x] `governance-l2-manifest-ci` ← `task_governance_l2_manifest_ci_v1.md`
- [x] `governance-wiki-t4-expand` ← `task_governance_wiki_t4_expand_v2.md`
- [x] `governance-l2-r3-test-manifest` ← `task_governance_l2_r3_test_manifest_v1.md`
- [x] `harness-wiki-loop-t4-l2` ← `task_harness_wiki_loop_t4_l2_v1.md`
- [x] `wiki-ctx-ab-v1` ← `task_wiki_ctx_ab_v1.md`
- [x] `coding-wiki-pilot` ← `task_coding_wiki_pilot_v1.md`
- [x] `chatbi-v3-p2-health-ready` ← `task_chatbi_v3_p2_resilience_health_ready_v1.md`
- [x] `harness-wiki-loop-c2-verify` ← `task_harness_wiki_loop_c2_verify_v1.md`
- [x] `governance-wiki-t4-r1-pilot` ← `task_governance_wiki_t4_r1_pilot_v1.md`
- [x] `wiki-ctx-ab-multi-slug` ← `task_wiki_ctx_ab_multi_slug_v1.md`
- [x] 更新 `index.md` · `log.md`（10 行）
- [x] 22/30/40/50 + reinspect + 关账

## 非范围

- 已有 5 篇 synthesis **正文重做**（仅允许补 frontmatter/§测试变更）  
- Agent 必读链（→ [`task_governance_wiki_agent_readorder_v1.md`](../done/task_governance_wiki_agent_readorder_v1.md) · 可并行 PR）  
- `api/` · `tests/` · workflow  

---

## 失败路径

| # | 触发 | 行为 |
|---|------|------|
| F1 | `source_task` 404 | 修路径 |
| F2 | 复制 review 全文 | 50 fail |
| F3 | `graph_nodes` 非法 | graph_query fail → 修 |
| F4 | index 未登记 | 50 fail |
| F5 | 擅自改 10 slug 名单 | **停** · 人改 SPEC |

---

## 验收标准

- [x] SPEC §4 VERIFY 全过  
- [x] `ls docs/coding_wiki/syntheses/*.md \| wc -l` **≥15**  
- [x] 10 个锁定 slug 均在 `index.md`  
- [x] 关账 + reinspect + RECENT

**VERIFY（40 帽）**：

```bash
ls docs/coding_wiki/syntheses/*.md | wc -l
python -c "
import pathlib
idx = pathlib.Path('docs/coding_wiki/index.md').read_text()
slugs='governance-l2-manifest-ci governance-wiki-t4-expand governance-l2-r3-test-manifest harness-wiki-loop-t4-l2 wiki-ctx-ab-v1 coding-wiki-pilot chatbi-v3-p2-health-ready harness-wiki-loop-c2-verify governance-wiki-t4-r1-pilot wiki-ctx-ab-multi-slug'.split()
assert all(s in idx for s in slugs)
"
python tools/tech_graph_manifest_check.py
```

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/coding_wiki/syntheses/` ×10 新增 · `index.md` · `log.md` |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | wc -l=15 · index assert · manifest_check |
| 结论 | **pass** |

---

## 给 Cursor

`gov-wiki-ingest-batch`、ingest、10 slug、syntheses、长链 semi_auto
