# Task：治理 — T4 L0 对齐与 VERIFY（R2）

> **状态**：active  
> **母 Loop**：[`task_harness_wiki_loop_t4_l2_v1.md`](task_harness_wiki_loop_t4_l2_v1.md) · round **R2**  
> **SPEC**：[`SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`](../spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；**依赖 R1** 已在 `done/`。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | T4 L0 pointer + VERIFY；纯 docs。 |
| **freeze_id** | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-spec-t4-l2-v1` |
| **task_slug** | `wiki-t4-r2-l0-align` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 继承母闸 |

---

## 帽子顺序（**跳过 10** · Loop R2）

| 序 | 帽 | 启动 |
|----|-----|------|
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_LOOP_22_to_CLOSE_v1.md) · **round=R2** |

---

## 背景与目标

R1 已完成 Pilot 后，本 round 补齐 **L0 指针** 与 **图谱 CI VERIFY**，使 T4 交付可独立验收；可选将 Bridge SPEC `draft`→`active`（**建议人审 commit**，Agent 可准备正文不改 status）。

**完成态**：

- `docs/_tech_graph/99_spec.md` 含「Wiki ↔ 图谱桥接（T4）」小节（≤30 行）链 Bridge SPEC + Pilot 路径。  
- 重跑 Bridge SPEC §7 VERIFY + `manifest_check` 四脚本绿。  
- 确认 R1 Pilot 仍满足 `graph_query neighbors` lint。

---

## 范围

- [ ] `99_spec.md` T4 小节（或 `00_main.md` 等价 pointer，二选一，以 SPEC §5.1 为准）。  
- [ ] 全量 T4 VERIFY（§7）+ 图谱 CI 四脚本。  
- [ ] invoke README 可增「T4 Pilot 路径」一行（可选）。  
- [ ] 22/30/40/50 invoke C2 全绿。

## 非范围

- `_test_manifest.json`（R3）。  
- 改 `graph.json` / `.ai.md` 拓扑（无业务变更时）。  
- api / tests / Harness prompts。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | R1 未 done | 22 阻塞 |
| F2 | 图谱 CI 失败 | 40/50 fail |
| F3 | Agent 代改 SPEC `active` 无人审 | 50 标风险 · 回滚 status |

---

## 验收标准

- [ ] `rg 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md`  
- [ ] `python tools/tech_graph_manifest_check.py` 等四脚本 exit 0  
- [ ] Pilot `graph_nodes` lint 仍 pass  

**VERIFY**：

```bash
rg -n 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
```

---

## 实现备忘（执行者回填）

| 项 | 内容 |
| --- | --- |
| commits | |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| | | |
