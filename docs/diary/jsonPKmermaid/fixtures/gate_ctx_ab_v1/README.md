# fixtures：`gate_ctx_ab_v1`（JSON vs Mermaid 行为实验）

> **协议**：[`../../01_experiment_json_vs_mermaid_kpi_v1.md`](../../01_experiment_json_vs_mermaid_kpi_v1.md)  
> **最小步骤**：[`../../02_minimal_first_step_v1.md`](../../02_minimal_first_step_v1.md)

| 文件 | 用途 |
|------|------|
| [`protocol_version.yaml`](./protocol_version.yaml) | 冻结模型、策略 α、commit、`freeze_id`、轴 II 基线 |
| [`tasks.json`](./tasks.json) | 题集 + `gold`（**T001–T002** 已跑 S0；**T003** draft 待核验） |
| [`TASKS_EXPANSION.md`](./TASKS_EXPANSION.md) | 扩题：人工核验 gold + 推荐方向 |
| [`scripts/score_gold_f1.py`](./scripts/score_gold_f1.py) | 对 raw jsonl 按 gold 计 entrypoints/impacts F1 |
| [`user_scripts.yaml`](./user_scripts.yaml) | S1 固定追问（Step 3 后再用） |
| [`system.md`](./system.md) | S0 共用 system persona（Step 3） |
| [`payloads/`](./payloads/) | Step 2 物化主载荷（`CTX_JSON` / `CTX_MERMAID` + 共享附件） |
| [`scripts/materialize_payloads.py`](./scripts/materialize_payloads.py) | 重新生成 payloads |
| [`scripts/run_s0_minimal.py`](./scripts/run_s0_minimal.py) | Step 3：S0 双分支（`model` 读 `protocol_version.yaml`；`--arms-order mermaid,json`） |

```bash
# 默认：先 Mermaid 再 JSON（见 protocol s0_arms_order）
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_minimal.py

# 与旧 run 相同顺序（先 JSON）
python …/run_s0_minimal.py --arms-order json,mermaid

# 并行（削弱顺序偏差；推荐做 A/B 墙钟对比）
python …/run_s0_minimal.py --parallel

# 多轮批跑（默认 3 轮并行 + 剔除离群后汇总）
python …/run_s0_batch.py --rounds 3
```

**Step 1 完成标准**：本目录四文件齐全；`tasks.json` 中 `gold` 路径可在仓内 `rg` 核验。

**Step 2 完成标准**：`payloads/materialize_report.json` 中 A/B 字节与轴 II 专文一致；`forbidden_checks` 均为预期。
