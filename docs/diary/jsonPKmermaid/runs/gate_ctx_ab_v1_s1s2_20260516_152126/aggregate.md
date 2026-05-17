# S1/S2 batch aggregate — `gate_ctx_ab_v1_s1s2_20260516_152126`

- **策略**：beta
- **会话数**：6（3 题 × 2 arm）

## 会话一览

| task | arm | S0 wall_s | S0 tokens | 累计 tokens | S2 泄漏合计 |
| --- | --- | ---:| ---:| ---:| ---:|
| `T001_embedding_dim_default` | `CTX_MERMAID` | 7.496 | 12368 | **148257** | 5 |
| `T001_embedding_dim_default` | `CTX_JSON` | 20.106 | 11801 | **141365** | 6 |
| `T002_unified_sse_chain_contract` | `CTX_MERMAID` | 64.259 | 12816 | **154664** | 4 |
| `T002_unified_sse_chain_contract` | `CTX_JSON` | 59.074 | 12456 | **159335** | 4 |
| `T003_ingest_admin_rpc` | `CTX_MERMAID` | 394.115 | 13037 | **155509** | 8 |
| `T003_ingest_admin_rpc` | `CTX_JSON` | 70.276 | 12366 | **154026** | 7 |

## 按 arm 中位数

| arm | 累计 token 中位数 | S0 token 中位数 | S2 泄漏均值 |
| --- | ---:| ---:| ---:|
| `CTX_MERMAID` | 154664.0 | 12816.0 | 5.67 |
| `CTX_JSON` | 154026.0 | 12366.0 | 5.67 |
