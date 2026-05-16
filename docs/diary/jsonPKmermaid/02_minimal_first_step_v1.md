# 最小可跑第一步：`CTX_JSON` vs `CTX_MERMAID`（v1）

> **前置**：[`01_experiment_json_vs_mermaid_kpi_v1.md`](./01_experiment_json_vs_mermaid_kpi_v1.md)（完整协议）  
> **静态基线**：[`docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md`](../../tech_graph/gate_a_scheme1_perf_compare_backend_detail.md) §4 / §9  
> **目标**：用 **1 道题 × 2 分支 × 仅 S0**，验证「主载荷形态」可复现、输出 JSON 可解析，**不**要求跑满 S1/S2 与双人 Rubric。

---

## Step 0 — 轴 II 数字对齐（本机复现，约 5 分钟）

在仓根执行（与专文 §3 一致）：

```bash
cd ai-ink-brain-api-python   # 本仓根
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
python tools/tech_graph_token_estimate.py --json
wc -c docs/_tech_graph/graph.json
```

**签收**：`--json` 中 `A.bytes_utf8`、`B.bytes_utf8`、`A.heuristic_tokens`、`B.heuristic_tokens` 与专文 §9 一致（见下文「轴 II 对齐清单」）。不一致则 **先修图/工具，再开 LLM 实验**。

---

## Step 1 — 冻结 `protocol_version`（fixtures 骨架）

创建（路径可按 `01` §6，此处为最小集）：

```
docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/
  protocol_version.yaml   # 模型、temperature、策略 α、commit 短 SHA、freeze_id
  tasks.json              # 仅 1 条 task：题面 + gold.entrypoints/impacts
  user_scripts.yaml       # 本步不用（S1 再用）
```

**`protocol_version.yaml` 最少字段**：

- `protocol_version: v1-minimal-s0`
- `model` / `provider`（与 SiliconFlow 或选定 API 一致）
- `context_strategy: alpha`（每轮重贴全量主载荷；先固定 α）
- `git_commit` / `freeze_id`（与 `TECH_GRAPH_S1_FREEZE_20260514_V1_1_3` 或当前 HEAD 一致）
- `arms: [CTX_JSON, CTX_MERMAID]`

**`tasks.json` 最少 1 题**：例如「改动 `api/rag_env.py` 中某 env 默认值时，入口与影响面？」——`gold` 须事先人工写好 **可核验路径集合**（3～8 条即可）。

---

## Step 2 — 准备两分支主载荷（不调用 LLM）

| 分支 | 主载荷来源 | 附件（Patch 对齐） |
|------|------------|-------------------|
| `CTX_JSON` | 读入 `docs/_tech_graph/graph.json`（全文或协议上限） | `_manifest.json`、`_contract_manifest.json` |
| `CTX_MERMAID` | 与 `tech_graph_token_estimate.py` 相同规则收集的 Mermaid 语料总串 | 同上 |

**禁止**：A 分支夹带 `_tech_graph` 下 Markdown 正文；B 分支夹带 `graph.json` 全文（除非协议 bump 明确允许）。

---

## Step 3 — 跑 S0 × 2 分支（各 1 次）

对 **同一 `task_id`**：

1. System：固定 persona（写进 `protocol_version` 或单独 `system.md`）。  
2. User：主载荷块 + manifest/contract + **题目正文**。  
3. 要求模型输出 §3 schema（`entrypoints` / `impacts` / `evidence` / `unknowns`）。  
4. 落盘：`runs/<run_id>/raw/{arm}_{task_id}_S0.jsonl` + usage（`prompt_tokens` / `completion_tokens` / `wall_total`）。

**本步成功标准**：

- [ ] 两次响应均为 **合法 JSON**（FP-1 未触发或已按协议重试）  
- [ ] `evidence` 可映射到 graph id 或 `path:line`  
- [ ] 记录 token / 墙钟，**不**与轴 II 专文字节混写为同一句「结论」

---

## Step 4 — 粗算 P3/P4（可选，仍不需 Rubric）

对两分支比较：

- **P3**：`prompt_tokens + completion_tokens`（谁更低记相对分）  
- **P4**：`wall_total`  

**P1/P2**：本最小步 **不跑** 双人 Rubric；仅人工扫一眼结构是否可交接、入口是否明显离谱。

---

## Step 5 — 写 1 页小结（再决定是否扩 S1/S2）

`docs/diary/jsonPKmermaid/reports/compare_gate_ctx_json_vs_mermaid_minimal_s0.md`：

- 链 Step 0 复现的轴 II 数字（或写「与专文 §9 一致」）  
- 表：`| arm | task | S0 tokens | wall | JSON ok | 入口粗评 |`  
- **明确写**：本报告 **不含** S1 多轮、S2 换题、双人盲审  

---

## 本步 **不做**

- 不跑 `tools/rubric_review` 的 `examples_builtin`（与 JSON/Mermaid 无关）  
- 不把 `docs/harness/reviews` 下旧演示批当作本实验数据  
- 不宣称 browser / LCP（轴 II 专文 §3.2 **N/A**）

---

## 给 Cursor

`CTX_JSON`、`CTX_MERMAID`、`gate_ctx_ab_v1`、`protocol_version.yaml`、`S0`、`tech_graph_token_estimate`、`freeze_id`
