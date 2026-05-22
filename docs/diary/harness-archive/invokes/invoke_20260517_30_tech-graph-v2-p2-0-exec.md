# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| template | docs/harness/prompts/TEMPLATE-execute-invoke.md §3（审查 R2 下一棒正文） |
| task_paths | ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_graph_query_v1.md |
| related_review_or_none | ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_v2_graph_query_v1_audit_R2_20260517.md |
| created_utc_or_local | 2026-05-17（执行帽 P2-0 开节） |
| notes | R2 零硬阻塞；从 §6 P2-0 开工 |

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

你必须完成：
0. Invoke 快照：按 docs/harness/invokes/README.md 将本消息全文落盘后再开工。
1. 通读 task v0.2：从 §6 **P2-0** 开工——最小 graph_v2 schema 文档 + 等价检查草案；**禁止** P2-0 实现 graphs[]、edges[].ref（见 §2.1、§8）。
2. 必读：治理层应用文 §8.2～§8.3（路径 ai-ink-brain-api-python/docs/diary/jsonPKmermaid/治理层三相塌缩_Ink技术图谱应用.md）；task §7 禁止外推 SBM ARI=1。
3. test_strategy: required——先失败测试/门禁再扩实现；P2-0 阶段以 schema + equivalence 脚本/测试为主，勿扩到 graph_query 或闸口 B。
4. 默认落盘：同路径 docs/_tech_graph/graph.json，schema_version: graph_v2（勿默认并列 graph_v2.json）。
5. 子仓根执行 pytest（上列 VERIFY）；结论回填 task「### 自检结论（执行者）」。
6. 对话回复：输出下一棒可复制 Prompt（自检帽或任务审核，视阻塞而定）。

禁止：静默整包 v1 作 query 默认；合并 tech_graph_contract_check 与 graph 导出；扩 scope 至方案3/退役 .ai.md/长期记忆产品。
```
