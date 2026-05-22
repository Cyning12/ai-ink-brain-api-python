# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3 |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（执行帽 P2-2） |
| notes | 上一棒 invoke_20260517_40_tech-graph-v2-p2-1-self-check.md |

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
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_40_tech-graph-v2-p2-1-self-check.md

你必须完成：
0. Invoke 快照：按 docs/harness/invokes/README.md 将本消息全文落盘后再开工。
1. 从 task §6 **P2-2** 开工：实现 `tools/tech_graph_graph_query.py`（加载 **v2** `graph.json`；v1 仅文档化降级，**禁止**静默整包 v1 进 prompt，见 FP-5）。
2. 最小查询 API：`downstream(id, depth)`、`upstream(id, depth)`、`neighbors(id)`；返回可序列化子图 + anchors；CLI 示例见 task §2.1 B。
3. `test_strategy: required`：先写 query golden + ≥1 失败路径（未知节点 FP-4、无 v2 FP-5），再实现；专项 pytest 与 VERIFY 一并绿。
4. 更新 `.cursor/rules/10-tech-graph.mdc`：**query 优先**；禁止默认整包 v1（与 G-END-5/6 一致）。
5. 子仓根跑 VERIFY + query 专项 pytest；结论回填 task「### 自检结论（执行者）」；§4.1 中 **闸口 B** 仍标 **未测**（P2-3）。
6. 对话回复：输出下一棒可复制 Prompt（自检帽复跑 §4.1 query 项，或打回修复）。

禁止：静默整包 v1 作 query 默认；合并 tech_graph_contract_check 与 graph 导出；扩 scope 至闸口 B（P2-3）或 P2-4（graphs[]/ref/kind）；用 v1 等价检查冒充 v2 签收。
```
