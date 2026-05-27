# Task：治理 — L2 Phase C 设计落盘（P2 Loop · R2）

> **状态**：draft  
> **round**：**R2** · 母单 [`task_harness_wiki_loop_p2_followup_v1.md`](task_harness_wiki_loop_p2_followup_v1.md)  
> **SPEC**：[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) · Phase B **done**

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | **设计文档 only**；不新增 pytest 或校验脚本（实现另 task）。 |
| **freeze_id** | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
| **semi_auto** | `true` |
| **git_branch** | `task/wiki-loop-p2-followup-v1` |
| **task_slug** | `gov-l2-phase-c-design` |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **pending** | 22, 30 | 继承母单 · **R1 须在 done/** |

---

## 背景与目标

Phase B manifest CI **done**。Phase C 目标：**task `failure_paths`** ↔ `_test_manifest` **双向口径**（哪些 ERR 须 manifest 条目、哪些 task 字段必填）。

本 round **仅** 在 L2 SPEC 增 **Phase C 设计节** + 验收口径草案 + 可选 `TASK_TEMPLATE` 一行 pointer — **不** 实现自动化校验。

**完成态**：L2 SPEC 含 **§ Phase C（design）** · 明确「实现 task」非范围说明。

---

## 范围

- [x] `SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` 增 Phase C 设计（§4.4 · 示例 3 条）  
- [x] `docs/tasks/templates/TASK_TEMPLATE.md` pointer 链 §4.4  
- [x] P2 SPEC §2 R2 行同步  

## 非范围

- 新 `tools/*` 脚本 · 改 `tests/` · CI Required  
- Wiki ingest  

---

## 验收标准

- [ ] Phase C 设计节可读、可独立立项实现 task  
- [ ] invoke C2 全绿 · task **`done/`**  

---

## 给 Cursor

`gov-l2-phase-c-design`、`GOV-L2-PHASE-C-DESIGN`、Loop R2
