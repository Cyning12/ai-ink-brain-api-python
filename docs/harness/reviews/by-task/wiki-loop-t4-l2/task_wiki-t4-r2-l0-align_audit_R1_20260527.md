# 任务审核 — T4 L0 对齐与 VERIFY（R2）

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | task | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | round | R2 |
> | audit_profile | post_close |
> | invoke_snapshot | `docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_20260527_22_wiki-t4-r2-l0-align-v1.md` |

---

## 审查结论摘要

**零阻塞。建议执行帽开工。**

- 前置检查：R1 `task_governance_wiki_t4_r1_pilot_v1.md` 已在 `done/` ✅（e833d07）。
- 母闸 `HG-LOOP-BATCH` 状态 `approved`。
- 任务范围明确：VERIFY + 确认 T4 小节存在；纯 docs。
- **已知债务标注**：`drift_check` exit 1（P2-1a health/ready、P1-3 access_tokens 等已有 drift），非 R2 引入；task §非范围明确 "不改 `.ai.md` 拓扑"。

---

## 已核对项

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | R1 在 `done/` | pass | `docs/tasks/done/task_governance_wiki_t4_r1_pilot_v1.md` |
| 2 | `HG-LOOP-BATCH` = approved | pass | 母 task §human_gate |
| 3 | task 含验收标准 + VERIFY | pass | task §验收标准 |
| 4 | 99_spec T4 小节已存在 | pass | `rg` line 42, exit 0（R1 f2f7505 已交付） |
| 5 | manifest_check / contract_check / graph_export 绿 | pass | 预跑 exit 0 |
| 6 | drift_check 已知债务 | 标注 | P2-1a/P1-3 等历史 drift；非 R2 范围 |
| 7 | 不改 api/tests/prompts/CI | pass | task §非范围 |

---

## 阻塞 / 非阻塞

**无阻塞。**

drift_check exit 1 为已有技术债务（非 R2 引入）。R2 执行帽应：
1. 重跑 VERIFY 并记录 drift_check 输出。
2. 在 task 自检结论中标注 drift 为 "已知历史债务，非本 round 引入"。
3. **不**修改 `.ai.md` / `graph.json` 修复 drift（超出范围）。

---

## 签收 / 关闭

本 task **R2 可进入执行帽**。30 帽负责：
1. 重跑全量 VERIFY。
2. 可选：invoke README 增 T4 Pilot 路径一行。
3. task 自检结论回填（含 drift 标注）。
4. 40 → 50 → 关账。

---

## 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop T4+L2 **R2** 的 **30 执行编码帽**。上一帽（22 任务审核）已结束；本帽只按下文执行。

【元信息】
- round: R2
- hat: 30
- task: docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md
- task_slug: wiki-t4-r2-l0-align
- freeze_id: GOV-T4-R2-L0-ALIGN@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 当前状态
- R1 已在 done/（task_governance_wiki_t4_r1_pilot_v1.md · e833d07）
- 99_spec.md 已含 T4 小节（line 42，R1 f2f7505 交付）

### 30 帽交付
1. 重跑 task §VERIFY 全部命令：
   ```bash
   rg -n 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md
   python tools/tech_graph_manifest_check.py
   python tools/tech_graph_drift_check.py
   python tools/tech_graph_contract_check.py
   python tools/tech_graph_graph_export.py --check
   ```
2. 确认 Pilot graph_nodes lint 仍 pass（`graph_query neighbors C1/RAG/RAG_DOC/FTS`）。
3. 可选：invoke README 增 T4 Pilot 路径一行。
4. `git add` 本轮路径 → `git commit`（HANDOFF_AUTO_COMMIT）。
5. 输出 40 自检 invoke。

### drift_check 处理
- drift_check 可能 exit 1（P2-1a health/ready、P1-3 access_tokens 等已有 drift）。
- **不修改 .ai.md / graph.json 修复**（task §非范围）。
- 在 task 自检结论中标注为 "已知历史债务"。

### 硬约束
- 不改 api/、tests/、docs/harness/prompts/、CI workflow。
- 仅 docs；test_strategy = not_applicable。
```
