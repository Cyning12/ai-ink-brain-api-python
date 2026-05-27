# Task：治理 — 后端 Agent Coding Wiki 默认读序常模化（v1）

> **状态**：done（2026-05-27 · GOV-WIKI-AGENT-READORDER@2026-05-27）  
> **前置**：Wiki-CTX-AB P2 **accepted** · L2 Phase B **done** · [`task_governance_l2_manifest_ci_v1.md`](../done/task_governance_l2_manifest_ci_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-Agent-Readorder-v1.md`](../spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md)  
> **SKILL**：[`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../skills/SKILL-docs-governance.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6/§8。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs/rules；关账跑 `tech_graph_manifest_check.py` 作 hygiene，非本 task 业务 pytest。 |
| **freeze_id** | `GOV-WIKI-AGENT-READORDER@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-wiki-agent-readorder-v1` |
| **task_slug** | `gov-wiki-agent-readorder` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22, 30 | SPEC + AGENTS 改稿人扫 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 |
| HG-READORDER-WORDING | approved | 30 | AGENTS/rules 措辞 · 人授权长链一次性执行 |

---

## 长任务执行（单 task 全链 · 非 Loop Batch）

> **模式**：`SKILL-harness-task` · **禁止** 使用 `LOOP_MANIFEST` / `HG-LOOP-BATCH`。  
> **人授权**：上表 `human_gate` 已 **approved** → Agent **同会话** 连续 **22 → 30 → 40 → 50 → 关账**，无需每帽等人重贴模板。

| 规则 | 内容 |
| --- | --- |
| **【授权】cross-hat** | 无新增 `pending` 闸前，禁止因「换帽」停；每帽仍须 invoke §3 ≥15 行 + **commit** |
| **【禁止跳帽】** | 未落盘当前帽 invoke + commit → 不得下一帽 |
| **【停】** | 仅：F* 失败路径 · `tech_graph_manifest_check` fail · 拟改 `api/tests/workflow` · 需求越 scope |
| **关账前** | 勾选 `SKILL-harness-task` **ST1–ST6** |
| **入口** | [`PROMPT_START_full_chain_v1.md`](../../harness/invokes/by-task/gov-wiki-agent-readorder/PROMPT_START_full_chain_v1.md) |

---

## 帽子顺序

| 序 | 帽 | 启动 |
|----|-----|------|
| 0 | **10** | **跳过**（SPEC+task 已冻结） |
| 1–5 | **22→关账** | `PROMPT_START` · `PROMPT_TASK_22_to_CLOSE_v1.md` §3 |

---

## 背景与目标

P2 实验已签收 **推荐默认读序**（`coding_wiki/index` + `syntheses`），但 `AGENTS.md` 仍未列入必读。本 task 将读序 **常模化**，并 pointer L2 `_test_manifest`（Phase B 已关账）。

**完成态**：

- `AGENTS.md` 必读链含 Coding Wiki 条（顺序、禁止项、L0 优先）。  
- 可选 `.cursor/rules/11-coding-wiki-readorder.mdc`；若改 `.mdc` 则跑 `python tools/gen_agents_md.py`。  
- `CODING_WIKI.md` §7 与读序一致（一句）。  
- Harness 22→50 + reinspect + 关账 hygiene。

---

## 范围

- [x] 按 SPEC §2.3 更新 `AGENTS.md`  
- [x] （推荐）新增 `.cursor/rules/11-coding-wiki-readorder.mdc`  
- [x] `docs/coding_wiki/CODING_WIKI.md` §7 同步一句「Agent 默认读序见 SPEC」  
- [x] 22/30/40/50 invoke + review + reinspect + CLOSE  
- [x] RECENT §6.6 增 **Agent 读序** 行 + §8

## 非范围

- 批量 ingest（→ [`task_governance_wiki_ingest_batch_v1.md`](task_governance_wiki_ingest_batch_v1.md)）  
- 前端仓 `AGENTS.md` / P1-4 parity  
- `api/` · `tests/` · workflow  
- Harness prompts 正文  

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| 读序 SPEC | `docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md` |
| P2 结论 | `docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md` |
| L2 done | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | 删除或弱化 L0 图谱必读 | 50 **fail** | 恢复 AGENTS |
| F2 | 读序写 Wiki 替代 graph_query | 50 **fail** | 按 SPEC §2.2 改 |
| F3 | 未跑 manifest_check（hygiene） | 40 标 fail | 补跑 |

---

## 验收标准

- [x] SPEC §4 VERIFY 全过  
- [x] `rg 'coding_wiki|Coding Wiki' AGENTS.md` 有命中  
- [x] 22 review + 50 reinspect 落盘  
- [x] 关账：`done/` + `_views` + ST1–ST6

**VERIFY（40 帽）**：

```bash
rg -n 'coding_wiki|Coding Wiki' AGENTS.md
test -f docs/spec/governance/SPEC-Governance-Wiki-Agent-Readorder-v1.md
python tools/tech_graph_manifest_check.py
```

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `AGENTS.md` · `.cursor/rules/11-coding-wiki-readorder.mdc` · `docs/coding_wiki/CODING_WIKI.md` · Harness invoke/review/reinspect |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `rg` AGENTS · `tech_graph_manifest_check.py` · rules 存在性 |
| 结论 | **pass**（见 `invoke_20260527_40_*` · `reinspect_*_20260527_v1.md`） |

---

## 给 Cursor

`gov-wiki-agent-readorder`、AGENTS、coding_wiki、默认读序、长链 semi_auto
