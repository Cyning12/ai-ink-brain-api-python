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

| [`…_batch_20260516_111037`](./gate_ctx_ab_v1_batch_20260516_111037/) | 3×parallel | **终批综合结论依据**（见 `../reports/conclusion_gate_ctx_ab_comprehensive_zh.md`） |
| [`…_batch_20260516_110751`](./gate_ctx_ab_v1_batch_20260516_110751/) | 3×parallel | 前一批对照 |

汇总：[`../reports/compare_gate_ctx_json_vs_mermaid_minimal_s0.md`](../reports/compare_gate_ctx_json_vs_mermaid_minimal_s0.md)
