# gate_ctx_ab — 实验日志（防漂移）

> **维护规则**：每完成一步（题集 / 跑数 / 脚本 / 结论文档），在 **[§4 步骤流水](#4-步骤流水)** 追加一行，并视情况更新 **[§3 真值表](#3-真值表)** 与 **[§5 待办](#5-待办与定稿门槛)**。  
> **实验边界**：仅 **Agent 主上下文消耗**（token / 墙钟 / 结构化输出 / gold F1）；**不含**人读 md、双轨维护工时、Cursor rules 第三臂。

---

## 1. 冻结项（变更须记一笔）

| 项 | 真值 |
|----|------|
| 协议 | `fixtures/gate_ctx_ab_v1/protocol_version.yaml` → `v1-minimal-s0` |
| 模型 | `deepseek-ai/DeepSeek-V4-Flash`（SiliconFlow） |
| 策略 | `context_strategy: alpha`（每轮全量主载荷 + manifest/contract） |
| S0 执行 | 3 轮 / 题，`run_s0_batch.py --parallel`；离群剔除见 batch `aggregate.md` |
| 轴 II 静态 | `graph.json` 20224 B；Mermaid 20953 B；启发式 token 5056 / 5026 |
| `freeze_id` | `TECH_GRAPH_S1_FREEZE_20260514_V1_1_3` |
| 计分 | `scripts/score_gold_f1.py`（启发式；非双人 Rubric） |

**对照 arm**

| arm | 主载荷 |
|-----|--------|
| `CTX_JSON` | `payloads/CTX_JSON/main.graph.json` |
| `CTX_MERMAID` | `payloads/CTX_MERMAID/main.mermaid_corpus.txt` |

---

## 2. 题集与 canonical batch（S0 主结论只认下表）

| task_id | topic_id | gold 状态 | **canonical batch**（3×parallel） |
|---------|----------|-----------|-----------------------------------|
| `T001_embedding_dim_default` | `rag_env_embedding` | rg 核验 | [`runs/gate_ctx_ab_v1_batch_20260516_111037/`](./runs/gate_ctx_ab_v1_batch_20260516_111037/) |
| `T002_unified_sse_chain_contract` | `unified_chat_sse` | rg 核验 | [`runs/gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253/`](./runs/gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253/) |
| `T003_ingest_admin_rpc` | `ingest_rpc` | rg 核验 | [`runs/gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300/`](./runs/gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300/) |

> **勿用** `110751` 等与 `111037` 重复 T001 的 batch 写总表（`score_gold_f1.py --runs-root` 会重复计数）。  
> 历史/异常 run 索引：[`runs/README.md`](./runs/README.md)。

---

## 3. 真值表（canonical batch · clean 中位数 + F1 均值）

更新日期：**2026-05-16**（P0-A 收口）

| 题 | arm | wall_s | total_tokens | entrypoints F1 | impacts F1 |
|----|-----|-------:|-------------:|---------------:|-----------:|
| T001 | CTX_JSON | **17.4** | **12159** | 0.822 | **0.396** |
| T001 | CTX_MERMAID | 32.5 | 12609 | 0.794 | 0.325 |
| T002 | CTX_JSON | **39.0** | **12044** | 0.667 | 0.309 |
| T002 | CTX_MERMAID | 47.6 | 12571 | **0.939** | 0.340 |
| T003 | CTX_JSON | **45.3** | **12258** | 0.909 | 0.424 |
| T003 | CTX_MERMAID | 57.8 | 12810 | **1.000** | **0.483** |

性能来源：各 batch `aggregate.md`（剔除后 n=2~3）。  
F1 来源：各 batch `gold_f1.md`（`score_gold_f1.py --batch-dir`）。

**三题草案汇总**：[`reports/conclusion_gate_ctx_ab_three_tasks_draft_zh.md`](./reports/conclusion_gate_ctx_ab_three_tasks_draft_zh.md)

---

## 4. 步骤流水

| 日期 | 步骤 | 产出 / commit | 备注 |
|------|------|---------------|------|
| 2026-05-16 | 轴 II + fixtures Step 0–2 | payloads、`tasks` T001 | materialize |
| 2026-05-16 | T001 S0 多轮；终批 `111037` | `conclusion_gate_ctx_ab_comprehensive_zh.md` | 并行 + 离群剔除 |
| 2026-05-16 | 入仓 T002 + rg 核验 | `50c1e55` | unified SSE |
| 2026-05-16 | T002 S0 批跑 `121253` | `e10aaa1` | `run_s0_batch --task-id` |
| 2026-05-16 | 规则双轨 `10/20-tech-graph.mdc` | `27554a2` | 与实验隔离说明 |
| 2026-05-16 | 入仓 T003 + rg 核验 | `d1ccf00` | ingest_rpc |
| 2026-05-16 | `score_gold_f1.py` + T003 批跑 `144300` | `408409e` | **P0-A 完成** |
| 2026-05-16 | 本日志 + 三题草案 | `c16adc1` | 防漂移 |
| 2026-05-16 | P0-B：`run_s1_s2.py` + `user_scripts.json`；T001 启用 S1/S2 scope | （待 commit） | 未跑 API |

<!-- 后续追加模板：
| YYYY-MM-DD | 简述 | 路径或 commit | 备注 |
-->

---

## 5. 待办与定稿门槛

### 已完成

- [x] P0-A：≥3 题 + gold 核验 + F1 脚本 + 每题 canonical S0 批跑
- [x] 实验日志（本文件）+ 三题性能/F1 草案

### 定稿前仍缺

- [x] **P0-B 脚本**：`user_scripts.json` + `run_s1_s2.py --all-tasks`（三题×两 arm）
- [ ] **P0-B 跑数**：执行 S1/S2 并落盘（6 会话 × 6 轮 API，耗时长）
- [ ] 三题总表 + S1/S2 后的 **修订结论文**（非 draft）
- [ ] 可选：F1 规则收紧或 Rubric 抽样（P1）
- [ ] 书面 **决策规则**（几胜才算倾向 JSON）

### 明确不做（除非改实验 charter）

- [ ] 人读 md / 维护成本对照
- [ ] Cursor rules 作为第三 arm
- [ ] 仅靠增加 S0 轮次代替 S1/S2

---

## 6. 脚本与报告索引

| 用途 | 路径 |
|------|------|
| 跑 S0 批跑 | `fixtures/gate_ctx_ab_v1/scripts/run_s0_batch.py` |
| 跑 S1/S2 | `fixtures/gate_ctx_ab_v1/scripts/run_s1_s2.py --all-tasks` |
| gold F1 | `fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py` |
| 题集 | `fixtures/gate_ctx_ab_v1/tasks.json` |
| 全批 F1（勿用于 T001 定稿表） | `reports/gold_f1_all_batches.md` |
| T001 综合（单题） | `reports/conclusion_gate_ctx_ab_comprehensive_zh.md` |
| T002 综合（单题） | `reports/conclusion_t002_s0_batch_zh.md` |
