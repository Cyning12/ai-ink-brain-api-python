# gate_ctx_c_v1_batch_20260518_052803

- **arms**：`CTX_V2_QUERY,CTX_DUAL_MD`
- **dry_run**：`False`

## 复现

```bash
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
RUBRIC_REVIEW_BACKEND=siliconflow python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py --arms CTX_V2_QUERY,CTX_DUAL_MD
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803 --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json
```

模型/温度见 gate_ctx_c_v1/protocol_version.yaml（DeepSeek-V4-Flash · 0.2）
