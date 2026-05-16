# gate_ctx_ab_v1 题集扩展说明

> 与 [`reports/conclusion_gate_ctx_ab_comprehensive_zh.md`](../../reports/conclusion_gate_ctx_ab_comprehensive_zh.md) §8.1 一致。  
> 当前 [`tasks.json`](./tasks.json) 仅 **T001**（AI 初稿 gold，已用于 minimal S0）。

## 人工是否必须？

- **题面**：AI 可写。  
- **gold**：**必须人工核验**（`rg` + `docs/_tech_graph/00_main.ai.md` + `_manifest.json`）。  
- 未核验 gold 不得用于 P1 F1 或「JSON vs Mermaid 定稿」。

## 推荐新增题（覆盖不同 `topic_id`）

| task_id 建议 | topic_id | 聚焦 |
|--------------|----------|------|
| `T002_unified_sse_chain_contract` | `unified_chat_sse` | **已写入 tasks.json**；rg 已核验符号（见 gold.verified_by） |
| `T003_ingest_rpc` | `ingest_rpc` | admin ingest / RPC / 向量入库 |
| `T003_text2sql_route` | `text2sql_branch` | Text2SQL 路由与子流程 |
| `T004_auth_chatbi` | `auth_chatbi` | 鉴权与 ChatBI verify |

每题 `segment_scope` 建议：`["S0","S1","S2"]`（脚本就绪后）。

## gold 核验清单（每题勾选）

- [ ] 每个 `entrypoints[].path` 在仓内存在  
- [ ] `graph_id`（若有）在 `graph.json` 节点或边上可对应  
- [ ] `impacts[].kind` 与 `contract|data|control|ci|other` 一致  
- [ ] 无「编造 workflow 名 / CI 绿没绿」类不可核验句

## AI 起草 Prompt 片段（复制给 Cursor）

```text
请为 ai-ink-brain-api-python 生成一道 gate_ctx_ab 评测题，topic_id={TOPIC_ID}。
要求：prompt_zh 一句话说清改动假设；gold 含 3–6 条 entrypoints、4–8 条 impacts；
每条附 path 或 graph_id；禁止虚构 CI 结果。输出 JSON 片段可并入 tasks.json。
参考图谱：docs/_tech_graph/00_main.ai.md、_manifest.json（勿读 *.md 正文作 A 载荷）。
```
