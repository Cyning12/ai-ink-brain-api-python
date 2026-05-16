# fixtures：`gate_ctx_ab_v1`（JSON vs Mermaid 行为实验）

> **协议**：[`../../01_experiment_json_vs_mermaid_kpi_v1.md`](../../01_experiment_json_vs_mermaid_kpi_v1.md)  
> **最小步骤**：[`../../02_minimal_first_step_v1.md`](../../02_minimal_first_step_v1.md)

| 文件 | 用途 |
|------|------|
| [`protocol_version.yaml`](./protocol_version.yaml) | 冻结模型、策略 α、commit、`freeze_id`、轴 II 基线 |
| [`tasks.json`](./tasks.json) | 题集 + `gold`（Step 1 仅 **T001**） |
| [`user_scripts.yaml`](./user_scripts.yaml) | S1 固定追问（Step 3 后再用） |
| [`system.md`](./system.md) | S0 共用 system persona（Step 3） |

**Step 1 完成标准**：本目录四文件齐全；`tasks.json` 中 `gold` 路径可在仓内 `rg` 核验。
