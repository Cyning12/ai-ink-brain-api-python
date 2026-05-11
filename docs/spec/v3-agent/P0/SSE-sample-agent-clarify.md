# SSE 样例：`agent.clarify`（澄清短路路径）

> 供前端 mock / 手工重放；须与 `docs/_tech_graph/_contract_manifest.json` 中 **`agent.clarify`** 最小 payload 键一致。  
> 后端触发：见 `SPEC-ChatBI-V2-Events.md` §3.2.1（`CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` 等条件）。

以下为 **NDJSON 风格** 片段（每行一条 `data:` JSON，省略 `event: chain` 重复时可自行补全标准 SSE 信封）。

```text
{"type":"meta","ts":1,"step_id":"m1","payload":{"run_id":"run-demo-clarify","mode":"text2sql","session_id":"sess-1"}}
{"type":"agent.step.start","ts":2,"step_id":"a1","payload":{"step_number":1,"max_steps":5}}
{"type":"agent.intent","ts":100,"step_id":"intent_1","payload":{"tool":"text2sql_query","mode":"text2sql","reasoning":"候选表意不够确定","confidence":0.35,"fallback":"rag_search","cache":"miss","cache_key_hash":"","latency_ms":12}}
{"type":"agent.clarify","ts":200,"step_id":"a1_clarify","payload":{"step_number":1,"message":"待您澄清（低置信度）","prompt_for_user":"请补充指标与时间范围。"}}
{"type":"agent.final","ts":300,"step_id":"a_final","payload":{"total_steps":0,"tools_used":[],"modes":["text2sql"],"fallback_used":false}}
{"type":"assistant.message","ts":310,"step_id":"s_answer","payload":{"role":"assistant","content":"系统在继续查数前需要先与您对齐语义…"}}
```

`done` 帧略（与现网 `done.data_keys` 一致即可）。
