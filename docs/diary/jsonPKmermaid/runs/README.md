# jsonPKmermaid — 行为实验 runs

每次 `run_s0_minimal.py`（或后续全协议 runner）在此生成子目录：

```
runs/<run_id>/
  index.json
  README.md
  raw/{arm}_{task_id}_S0.jsonl
```

示例：[`gate_ctx_ab_v1_minimal_s0_20260516_105006/`](./gate_ctx_ab_v1_minimal_s0_20260516_105006/)（首轮为 `CTX_JSON`，墙钟可能偏长）

复跑时建议用 `--arms-order mermaid,json` 或依赖 protocol 默认 `s0_arms_order`，并在 `index.json` 查看 `arms_order` / `call_index`。
