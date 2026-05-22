# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md · P3 文档 |
| task_paths | ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md |
| created_utc_or_local | 2026-05-18 CST |
| git_branch | `task/engineering-tech-graph-gate-c-p3-docs-v1` |
| notes | 闸口 C PR-3 文档帽；上一棒 50 invoke_20260518_34；**非**重跑 batch |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽（30）」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
- 子仓 ai-ink-brain-api-python：自 `main` 拉分支 `task/engineering-tech-graph-gate-c-p3-docs-v1`（PR #32 已合并）
- 工作区根 Projects：同步改 `docs/tech_graph/改进方向.md` 与 `docs/tech_graph/tasks/ai-ink-brain-api-python/README.md`（**分仓 commit**）。

输入：
- 主 task（done · P3 未勾选）：
  ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
- P2 结论（只读引用，勿改 accepted）：
  ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- 规划真值：
  Projects/docs/tech_graph/改进方向.md（v1.1.3 · §对比实验门闸、§2.7）
- 专题索引：
  Projects/docs/tech_graph/tasks/ai-ink-brain-api-python/README.md
- 子仓根：ai-ink-brain-api-python
- 验证命令（合并前必绿 · 文档帽仍须回归）：
  pytest tests -m "not intent_eval and not intent_benchmark"
- 关联审查：ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_v2_dual_track_v1_audit_R1_20260518.md
- 关联 SPEC：无（纯文档对齐）

【范围 · task §1.1 P3】
1. `改进方向.md`：
   - 「对比实验门闸（摘要）」表增 **闸口 C** 行：对比组 **D `CTX_V2_QUERY` vs E `CTX_DUAL_MD`**；链结论 `conclusion_gate_c_v2_dual_track_v1_zh.md`、canonical run `gate_ctx_c_v1_batch_20260518_052803`、`freeze_id` `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0`。
   - 写明 **不推翻闸口 B** 已采纳的 CTX_QUERY / graph_query 默认；E 为人读/按需双轨，非 machine 默认。
   - 方案2 **§2.7** 增已勾选 **闸口 C** 验收项（与闸口 B 条目同型）。
   - 若路线图/三者关系表需一句「方案2 + 闸口 C」前置说明，仅最小增补，禁止扩 scope 改方案3 时序（R2 仍依赖 B）。
2. `docs/tech_graph/tasks/ai-ink-brain-api-python/README.md`：
   - 闸口 C task 指针改为 **done/** 路径；可选增一行链结论 md。
3. 子仓 task 正文：
   - §1.1 P3 两项勾选 `[x]`；§6 增 **P3 自检** 小节（改了哪些文件、未改代码）。
   - **禁止**改 P0～P2 实验结论数字、**禁止**重跑 `run_gate_c_batch.py`。

【非范围】
- NR-1/2：不重跑闸口 A/B/C batch；不改 `gate_ctx_*` fixture/run。
- 不实现 §2.7 的 Cursor/MCP 冒烟（F-2.7-local/agent）。
- 不改 `graph_v2` schema / 业务代码。

【test_strategy】
- 本切片：`not_applicable`（仅 md）；仍跑主链 pytest 证明无回归。

开帽前硬检查：
0. 落盘 invoke（若尚未）：`invoke_20260518_35_tech-graph-gate-c-p3-docs.md`。
0b. human_gate：HG-* 无 blocks 含 `30` 且 pending → 可开工。
1. 通读 task §1.1 P3、结论 §3.2；对照 B 的 `改进方向` / README 写法保持一致。
2. 完成上述文档编辑；Projects 与子仓 **分别** `git add` 本轮路径。
3. 跑 pytest；回填 task「### 自检结论」**P3** 小节。
4. 输出下一棒 **40 自检帽** Prompt（或 `semi_auto` 链式落盘 invoke_36 + commit 后自戴 40）。
5. HANDOFF_AUTO_COMMIT：禁止 `git add -A`；对话报各仓 short-hash。

禁止：代填 human_gate；修改结论 `accepted`；重跑 gate_ctx_c LLM batch。
```
