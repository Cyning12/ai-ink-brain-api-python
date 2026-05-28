# 单元 B · 单 task 22→关账（cc · PR-B）

> **task**：`docs/tasks/active/task_governance_l2_phase_c_impl_v1.md`  
> **分支**：`task/wiki-unit-ab-plan-v1` · **前置**：`origin/main` 已含 PR-A [#79](https://github.com/Cyning12/ai-ink-brain-api-python/pull/79)

---

## 执行前（人 + 机）

```bash
git checkout task/wiki-unit-ab-plan-v1
git pull origin main

# 闸口（须文件内 approved，非口头）
grep -E 'HG-TASK-DRAFT.*approved' docs/tasks/active/task_governance_l2_phase_c_impl_v1.md \
  || { echo 'BLOCK: HG-TASK-DRAFT'; exit 1; }

python tools/harness_human_gate_check.py --task docs/tasks/active/task_governance_l2_phase_c_impl_v1.md
```

---

## §3 可复制 Prompt（22→关账）

```text
【步骤 0 · Gate】打开 task_governance_l2_phase_c_impl_v1.md，扫描 human_gate。
HG-TASK-DRAFT / HG-AUDIT-R1 未 approved 且阻塞当前帽 → 硬停（HANDOFF_SEMI_AUTO §2.3）。
HG-REINSPECT 在 50 前须 approved（可 22 后再请人批）。

执行单元 B · PR-B · test_strategy: required · 22→30→40→50→关账。
分支 task/wiki-unit-ab-plan-v1；禁止改 docs/coding_wiki/ 批量 ingest。

必读 @：
- docs/tasks/skills/SKILL-harness-task.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md §4.4
- docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md §3
- docs/harness/prompts/hats/22-task-audit.md … 50-independent-reinspect.md
- HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/invokes/by-task/gov-l2-phase-c-impl/PROMPT_TASK_22_to_CLOSE_v1.md（本文件）

【30 实现要点】
1. tools/tech_graph_test_manifest_check.py 增 --check-failure-paths（与默认 Phase B 检查向后兼容）
2. task→manifest：failure_path_ref 指向的 task 须含对应 F# 或 manifest_exempt
3. manifest→task：entries[].failure_path_ref 文件存在且可解析 F#
4. error_codes 集合与 task 表一致（实现期，见 SPEC §4.4.2）
5. tests/ 新增可失败用例覆盖双向模式
6. docs/_tech_graph/99_spec.md VERIFY 增一行

【C2 抽样 ≥3 Epic】（写入 22 review 或 30 invoke）
- task_05_query_rewrite_observability ↔ FP-RAG-DB-DISCONNECT / FP-QUERY-REWRITE-ANCHOR-LOST
- task_chatbi_v3_sql_ast_text2sql_gate_v1 ↔ FP-SQL-GATE-DENIED
- task_chatbi_v3_p2_resilience_health_ready_v1 ↔ FP-HEALTH-PROBE-FAIL

VERIFY（40 须粘贴输出）：
python tools/tech_graph_test_manifest_check.py
python tools/tech_graph_test_manifest_check.py --check-failure-paths
pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short

关账：reinspect_gov-l2-phase-c-impl_* · git mv done/ · _views · RECENT §6.6 Unit B done。
```
