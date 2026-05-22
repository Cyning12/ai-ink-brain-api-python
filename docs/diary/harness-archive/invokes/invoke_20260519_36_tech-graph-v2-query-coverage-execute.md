# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/30-execute-code.md |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_query_coverage_v1.md |
| related_review_or_none | none（继承闸口 C R1 范围 · 无新实验门闸） |
| created_utc_or_local | 2026-05-19 CST |
| git_branch | task/engineering-tech-graph-v2-query-coverage-v1 |
| notes | 闸口 C follow-up · graph_v2 可达性；与 P3 文档分支并行 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽（30）」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
- 子仓 ai-ink-brain-api-python：从 main 新建分支 task/engineering-tech-graph-v2-query-coverage-v1
  （勿基于 task/engineering-tech-graph-gate-c-p3-docs-v1；P3 文档在另一分支并行）
- 工作区根 Projects/：本 task 默认不改；若动 docs/tech_graph/ 须单开 commit 并说明

【并行说明】
- 闸口 C 已关账（done + 结论 accepted）；P3 文档帽在分支 task/engineering-tech-graph-gate-c-p3-docs-v1 执行，本 task 不替代 P3。
- 本 task 目标：提升 graph_v2 + graph_query 对 gold 的可达性（尤其 T002），不推翻闸口 B/C 的「machine 默认 = query 子图」。

【输入】
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_query_coverage_v1.md
- 闸口 C 结论与 follow-up（只读）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- 闸口 B 结论（只读）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md
- 方案2 SPEC：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
- 治理层：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md
- 实现真值：
tools/tech_graph_graph_export.py
tools/tech_graph_graph_query.py
docs/_tech_graph/graph.json
- 闸口 C 物化（可扩展，不重跑 batch）：
fixtures/gate_ctx_c_v1/query_seeds.json
fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
fixtures/gate_ctx_c_v1/protocol_version.yaml
- 题集 gold：
fixtures/gate_ctx_ab_v1/tasks.json
- 子仓根：ai-ink-brain-api-python
- 验证：
pytest tests -m "not intent_eval and not intent_benchmark"
pytest tests/test_tech_graph_graph_export.py tests/test_tech_graph_graph_query.py
python tools/tech_graph_graph_export.py --check
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py

【开帽前硬检查】
0. 落盘已存在则复读：docs/harness/invokes/invoke_20260519_36_tech-graph-v2-query-coverage-execute.md
0b. 复读 task human_gate：blocks 含 30 且 pending → 拒开工并列 gate_id。
1. 通读 task §0～§1、闸口 C §3.3 follow-up；确认本线非重跑 C batch 改结论。
2. 自 main 检出分支 task/engineering-tech-graph-v2-query-coverage-v1（若未建则创建）。

【范围 · 按 task §1.3 分期执行】
PR-1（图真值 · 仍 graph_v2）：
- export：T002 gold 可达（U2、U1、AUTH、EV_TYPES）；新 graph_v2_freeze_id 写入 graph.json
- tech_graph_graph_export.py --check 绿 + 相关 pytest 绿

PR-2（查询与物化）：
- query_seeds：T002 多查询 union（token 上限内）
- materialize_gate_c_payloads.py：子图并集；可选 SSE contract/manifest 小切片 + anchors 索引
- 扩展 test_gate_ctx_c_v1_materialize.py（T002）
- materialize exit 0；T002 D 臂 tokens < protocol 上限

PR-3（可选）：T002 dry-run 或「须新 batch 目录」说明；不覆盖 runs/..._052803

【禁止】
NR-1/2：不重跑闸口 A/B/C 主 batch；不改历史 runs
不改 conclusion_gate_c accepted；不升 CTX_DUAL_MD 为默认
不与 P3 分支混改 改进方向.md 闸口 C 表
schema 仍 graph_v2（breaking → 拒扩 scope）
git add -A

【交付】
1. 回填 task §6 实现备忘 +「### 自检结论（执行者）」30 帽
2. 输出下一棒 40 自检 Prompt
3. HANDOFF_AUTO_COMMIT：仅 add 本轮路径；对话报 short-hash
```
