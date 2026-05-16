# JSON vs Mermaid — minimal S0 对照（T001）

> **run_id**：`gate_ctx_ab_v1_minimal_s0_20260516_105006`  
> **题**：`T001_embedding_dim_default`（`expected_embedding_dim()` 默认维度）  
> **模型**：`deepseek-ai/DeepSeek-V4-Flash`（SiliconFlow）  
> **轴 II 静态基线**：见 [`../fixtures/gate_ctx_ab_v1/payloads/materialize_report.json`](../fixtures/gate_ctx_ab_v1/payloads/materialize_report.json)（**不与下表混写为同一句结论**）

## S0 行为向（LLM usage）

| arm | status | prompt_tokens | completion_tokens | total | wall_s |
|-----|--------|---------------|-------------------|------:|-------:|
| `CTX_JSON` | ok | 11039 | 842 | 11881 | 39.6 |
| `CTX_MERMAID` | ok | 11425 | 937 | 12362 | 6.1 |

- **P3（省钱，粗）**：本 run 下 **JSON 分支 total 略低**（11881 vs 12362）。  
- **P4（省时，粗）**：**Mermaid 分支墙钟明显更短**（6.1s vs 39.6s）；仅单次、未重复 R 次，不作签收。  

原始记录：[`../runs/gate_ctx_ab_v1_minimal_s0_20260516_105006/`](../runs/gate_ctx_ab_v1_minimal_s0_20260516_105006/)

## 结构粗评（未跑 Rubric）

两分支均输出合法 JSON（含 `entrypoints` / `impacts` / `evidence` / `unknowns`）。  
`CTX_JSON` 命中 `api/rag_env.py::expected_embedding_dim`；`CTX_MERMAID` 以图谱节点 `EMB`/`VEC`/`FUSE` 为主（与 gold 部分对齐，**未**做 F1 计分）。

## 本报告未覆盖

- S1 多轮、S2 换题、双人盲审  
- 入口/影响 F1 对 gold 的定量对比  

## 复现

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_minimal.py
```
