# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（执行帽 P2-1） |
| notes | 上一棒 invoke_20260517_40_tech-graph-v2-p2-0-self-check.md；P2-0 已签收 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5

输入（占位符已替换）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md
- 子仓根（相对 Projects/）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md
- 关联 SPEC / 总规：
docs/tech_graph/spec/ai-ink-brain-api-python/machine_track_architecture_draft_zh.md
docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md
docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
- 上一棒 invoke 快照：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-0-self-check.md

你必须完成：
0. Invoke 快照：按 docs/harness/invokes/README.md 将本消息全文落盘后再开工。
1. 从 task §6 **P2-1** 开工：升级 `tools/tech_graph_graph_export.py`（或 v2 导出路径），使 `docs/_tech_graph/graph.json` 输出 `schema_version: graph_v2`（P2-0 最小字段集，见 §2.1）；**禁止** P2-1 引入 `graphs[]`、`edges[].ref`、`nodes[].kind`。
2. `freeze_id` 与 `fixtures/gate_ctx_ab_v1/protocol_version.yaml` 对齐 bump（task N-2）；导出含 `generated_at` / `freeze_id`。
3. 接入 CI（`tech-graph.yml` 或等价）：`export --check` 对 v2 通过；等价检查阈值 §2.1（95%/90%）；manifest_check、contract_check **仍独立**，禁止与 graph 导出合并。
4. pytest：`export v2` golden + 等价 PASS 路径 + ≥1 失败路径（漂移/阈值）；**勿**把「v1 仓内图仍绿」当作 v2 签收。
5. 子仓根跑 VERIFY；结论回填 task「### 自检结论（执行者）」；**勿**扩至 `graph_query`（P2-2）或闸口 B（P2-3）。
6. 对话回复：输出下一棒可复制 Prompt（自检帽复跑 §4.1 导出/等价项，或打回修复）。

禁止：静默整包 v1 作 query 默认；合并 tech_graph_contract_check 与 graph 导出；P2-1 实现 `graphs[]`/`ref`；用 graph_v1 等价检查冒充 graph_v2 CI 签收。
```
