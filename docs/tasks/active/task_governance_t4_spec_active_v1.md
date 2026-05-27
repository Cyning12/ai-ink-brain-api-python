# Task：治理 — T4 Bridge SPEC draft→active（P2 Loop · R1）

> **状态**：draft  
> **round**：**R1** · 母单 [`task_harness_wiki_loop_p2_followup_v1.md`](task_harness_wiki_loop_p2_followup_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md) · [`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](../spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md)

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | SPEC 状态升格 + docs hygiene；不改 graph 导出逻辑。 |
| **freeze_id** | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
| **semi_auto** | `true` |
| **git_branch** | `task/wiki-loop-p2-followup-v1` |
| **task_slug** | `gov-t4-spec-active` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **pending** | 22, 30 | 继承母单 |

---

## 背景与目标

T4 Pilot + 扩面 **done**；bridge SPEC 仍为 **draft**。本 round 将 SPEC **升格 active**，同步 RECENT §6.6 T4 行、Pilot/扩面 synthesis pointer，并确认与 `graph_query` 消费口径一致（只读对照，不改 tools）。

**完成态**：T4 SPEC 头表 `状态: active` · RECENT 更新 · Roadmap §5.1 T4 行 **active**。

---

## 范围

- [ ] `SPEC-Governance-Wiki-TechGraph-Bridge-v1.md` draft→active + 修订记录  
- [ ] `docs/spec/governance/README.md` T4 行状态  
- [ ] RECENT §6.6 T4 行：`draft` → **active**  
- [ ] 链出 3+ 扩面 synthesis（已有 `graph_nodes`）  

## 非范围

- 新增 synthesis / graph_nodes（→ 非本 round）  
- 改 `api/`、`tests/`、CI  

---

## 验收标准

- [ ] T4 SPEC **active** 且 freeze_id 与扩面 task 一致 pointer  
- [ ] invoke C2 全绿 · task **`done/`**  

---

## 给 Cursor

`gov-t4-spec-active`、`GOV-T4-SPEC-ACTIVE`、Loop R1
