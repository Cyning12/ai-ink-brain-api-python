# jsonPKmermaid — 行为实验 runs

每次 `run_s0_minimal.py`（或后续全协议 runner）在此生成子目录：

```
runs/<run_id>/
  index.json
  README.md
  raw/{arm}_{task_id}_S0.jsonl
```

| run_id | arms_order | 备注 |
|--------|------------|------|
| [`…_110007`](./gate_ctx_ab_v1_minimal_s0_20260516_110007/) | Mermaid → JSON | **推荐对照**（2026-05-16 复跑） |
| [`…_105006`](./gate_ctx_ab_v1_minimal_s0_20260516_105006/) | JSON → Mermaid | 首轮 JSON 39.6s |
| [`…_104123`](./gate_ctx_ab_v1_minimal_s0_20260516_104123/) | JSON → Mermaid | 异常墙钟，勿作主结论 |

| [`…_batch_20260516_111037`](./gate_ctx_ab_v1_batch_20260516_111037/) | 3×parallel | **T001 终批**（见 `../reports/conclusion_gate_ctx_ab_comprehensive_zh.md`） |
| [`…_batch_t2_…_121253`](./gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253/) | 3×parallel | **T002** Unified SSE（见 `../reports/conclusion_t002_s0_batch_zh.md`） |
| [`…_batch_T003_…_144300`](./gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300/) | 3×parallel | **T003** Admin Ingest（[`gold_f1.md`](./gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300/gold_f1.md)） |
| [`…_batch_20260516_110751`](./gate_ctx_ab_v1_batch_20260516_110751/) | 3×parallel | T001 前一批对照 |

| [`…_s1s2_…_152126`](./gate_ctx_ab_v1_s1s2_20260516_152126/) | 3 题 × 2 arm × (S0+S1×3+S2×2) | **P0-B 全量**（β；36/36 ok；见 `aggregate.md`） |
| [`…_s1s2_…_150452`](./gate_ctx_ab_v1_s1s2_20260516_150452/) | T002 × CTX_JSON | P0-B smoke |

汇总：[`../reports/compare_gate_ctx_json_vs_mermaid_minimal_s0.md`](../reports/compare_gate_ctx_json_vs_mermaid_minimal_s0.md)  
gold F1 全批：[`../reports/gold_f1_all_batches.md`](../reports/gold_f1_all_batches.md)  
S1/S2 结论：[`../reports/conclusion_s1s2_batch_20260516_152126_zh.md`](../reports/conclusion_s1s2_batch_20260516_152126_zh.md)
