# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（执行帽 P2-3 闸口 B） |
| notes | 上一棒 invoke_20260517_40_tech-graph-v2-p2-2-self-check.md；HG-AUDIT-R2 approved；HG-P2-3-GATE-B pending |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（semi_auto、human_gate）

输入（占位符已替换）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md
- 子仓根（相对 Projects/）：
ai-ink-brain-api-python
- 合并前 VERIFY：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md
- 上一棒 invoke 快照：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-2-self-check.md
- 必读（闸口 B）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md（§8.2～§8.3）
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_ctx_ab_final_zh.md（闸口 A · 勿复做主实验）
docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/protocol_version.yaml（freeze_id 对齐）

你必须完成：
0. Invoke 快照：按 docs/harness/invokes/README.md 将本消息全文落盘后再开工。
0b. 人工闸：HG-AUDIT-R2 已 approved 可开工；HG-P2-3-GATE-B 仍 pending — Agent 不得代填 approved，关账前须人签。
1. 从 task §6 **P2-3** 开工：闸口 B 行为实验（§4.2），**禁止** NR-1（再跑整包 v1 vs Mermaid 作主结论）。
2. 三组对照（§4.2）：
   - **A** 整包 CTX_MERMAID（基线）
   - **B** 整包 v1 CTX_JSON（对照 · 非默认推荐）
   - **C** **CTX_QUERY** = `python tools/tech_graph_graph_query.py` 子图输出 + manifest/contract 切片（**非**整包 graph_v2 文件）
3. 指标：token/墙钟、entry/impact F1（`score_gold_f1`）、P1 Rubric 子集（≥3 题，样本量可参照审查 N-3）；结论对照 §4.3 B-1～B-3。
4. 落盘闸口 B 报告至 task §9 约定路径（`docs/diary/jsonPKmermaid/` 或 `docs/tech_graph/`），文内链回 freeze_id `TECH_GRAPH_S2_FREEZE_20260517_V2_0`。
5. 子仓根跑 VERIFY；结论回填 task「### 自检结论（执行者）」；§4.1 **闸口 B** 仅在有实验证据后勾选；工程 query 项保持 pass。
6. 对话回复：输出下一棒可复制 Prompt（**40 自检帽**复跑闸口 B 证据，或打回修复）。

禁止：默认整包 v1/v2 作 CTX_QUERY；合并 tech_graph_contract_check 与 graph 导出；扩 scope 至 P2-4（graphs[]/ref/kind）或退役 .ai.md；代填 HG-P2-3-GATE-B 为 approved。
```
