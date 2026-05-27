# Invoke · 22 任务审核 · R2 · wiki-t4-r2-l0-align

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 母 Loop：`task_harness_wiki_loop_t4_l2_v1.md` · `HG-LOOP-BATCH` = approved。
- R1 已在 `done/`（e833d07）。
- 下一棒：30 执行编码。

## §2 审查结论

**零阻塞。可进入 30。**

- R1 前置：`task_governance_wiki_t4_r1_pilot_v1.md` 在 `done/` ✅。
- 99_spec T4 小节已存在（line 42，R1 f2f7505）。
- manifest_check / contract_check / graph_export 预跑 exit 0。
- drift_check exit 1 为已知历史债务（P2-1a/P1-3 等），非 R2 引入；task §非范围 "不改 .ai.md 拓扑"。

## §3 下一棒可复制 Prompt

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

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_wiki_t4_r2_l0_align_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：review 落盘 + invoke 落盘
├── 下一棒：A=30 执行编码 · B=—
├── 推荐：A
└── 阻塞：无
```
