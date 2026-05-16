# JSON vs Mermaid 上下文形态 — 综合结论（gate_ctx_ab_v1 · minimal S0）

> **执行批次（终）**：[`gate_ctx_ab_v1_batch_20260516_111037`](../runs/gate_ctx_ab_v1_batch_20260516_111037/)  
> **题**：`T001_embedding_dim_default`（`expected_embedding_dim()` 默认维度与全链路对齐）  
> **模型**：`deepseek-ai/DeepSeek-V4-Flash`（SiliconFlow）  
> **日期**：2026-05-16

---

## 1. 实验要回答什么

在 **同一题、同一 Rubric 输出 schema** 下，仅改变 LLM **主上下文载荷**：

| 分支 | 主载荷 |
|------|--------|
| **CTX_JSON** | `graph.json` 全文 |
| **CTX_MERMAID** | 与闸口 A 一致的 Mermaid 语料总串（`*.ai.md` fence 拼接） |

比较 **行为向**（墙钟、token、结构化 JSON 是否可解析），并与 **轴 II 静态**（字节/启发式 token，不进模型）分开叙述。

---

## 2. 方法与干扰控制

| 环节 | 做法 |
|------|------|
| 轴 II | 本机复现 `graph.json` **20224 B**；Mermaid **20953 B**；启发式 token **5056 vs 5026**（见 `payloads/materialize_report.json`） |
| S0 | 单题冷启动；输出 `entrypoints` / `impacts` / `evidence` / `unknowns` |
| 顺序偏差 | 每轮 **`parallel`** 同时发两请求，避免「串行第二条占便宜」 |
| 离群 | **3 轮**批跑；剔除 `wall>120s` 或 `>2.5×` 该 arm 三轮中位数；`status!=ok` 剔除 |
| 模型名 | 与官网一致 `deepseek-ai/DeepSeek-V4-Flash`；响应 `model_returned` 一致 |

---

## 3. 终批全量数据（`111037`）

| round | CTX_JSON wall_s | CTX_MERMAID wall_s | 计入 clean |
|------:|----------------:|-------------------:|:----------:|
| 1 | 60.58 | 23.82 | JSON 剔除（>2.5×中位数） |
| 2 | 22.91 | **333.32** | Mermaid 剔除（>120s） |
| 3 | 11.94 | 41.25 | 均保留 |

三轮 **parse_ok 均为 true**（6/6 次调用成功产出合法 schema）。

---

## 4. 剔除离群后的对比（主结论依据）

| 指标 | CTX_JSON | CTX_MERMAID | 相对 |
|------|--------:|------------:|------|
| **wall_median_s** | **17.4** | **32.5** | JSON 墙钟中位数更低（n=2） |
| **total_tokens_median** | **12159** | **12609** | JSON 略省约 **3.6%** token |
| 有效样本 n | 2 | 2 | 各剔除 1 个离群 |

**说明**：n=2 仍偏少；结论方向与前一批 `110751`（JSON 14.1s / Mermaid 22.3s）一致，但数值会有批次间抖动。

---

## 5. 对历史干扰的归因（为何曾以为「JSON 很慢」）

| 现象 | 解释 |
|------|------|
| 串行首轮 JSON **39–72s**、次轮 Mermaid **6–23s** | **首轮冷启动/排队**落在先执行的一支，**非**载荷形态固有 |
| `104123` JSON **612s**、`111037` R2 Mermaid **333s** | **网关/超时边界类离群**；剔除后不应进入主结论 |
| 调换 `arms-order` 或 `parallel` 后 JSON 亦可 **~7–22s** | 与「JSON 必然慢」不符 |

---

## 6. 轴 II vs 行为向（勿混写）

| 维度 | CTX_JSON | CTX_MERMAID | 含义 |
|------|--------:|------------:|------|
| 静态字节 | 20224 | 20953 | 塞进上下文前体积接近（B 约 **+3.6%**） |
| 启发式 token | 5056 | 5026 | 粗估亦接近 |
| LLM prompt（本实验） | ~11039 | ~11425 | 行为向输入略不同（含 manifest/contract） |
| 墙钟（clean 中位数） | **17.4s** | **32.5s** | **本次**终批：JSON 更快，但受 API 抖动影响大 |

**不能**用轴 II「体积相当」直接推出墙钟相当；**也不能**用单次串行 run 断言孰快孰慢。

---

## 7. 质量与验收（本阶段）

- **输出**：6/6 次合法 JSON；均命中 `api/rag_env.py` / 图谱节点类 evidence（未做 gold F1）。  
- **未做**：S1 多轮追问、S2 换题、P1/P2 双人 Rubric、入口/影响 F1。  
- **演示工件**：早期 `examples_builtin` Rubric 批跑已迁至 `_staging/`，**与**本实验无关。

---

## 8. 定稿前的下一步（优先级 — 勿颠倒）

> **未完成 P0 前，不得用「多跑几轮 S0」代替定稿。** 当前 minimal 仅完成 **单题 S0**；定稿须先扩协议段覆盖面。

| 优先级 | 事项 | 说明 |
|--------|------|------|
| **P0** | **扩 `tasks.json`**（建议 **≥3 题**，`topic_id` 互异） | 每题附 **人工核验过的 gold**（见 §8.1） |
| **P0** | 跑 **S1**（同题 K=3 追问，`user_scripts.yaml`） | 测收敛、证据是否收紧、token 累计 |
| **P0** | 跑 **S2**（M=2 换题，不同 `topic_id`） | 测串题泄漏、上下文膨胀 |
| **P1** | **P1/P2**：gold F1 或双人 Rubric | 不只「能吐 JSON」，还要可交接 / 可靠 |
| **P2** | `run_s0_batch.py --rounds 5`（并行 + 剔除离群） | **仅**压低 S0 的 API 抖动，**不替代** S1/S2 |
| **P2** | 可选 **warmup**（不计入统计） | 进一步削弱冷启动，仍不能替代扩题 |
| **定稿** | 更新 `01_experiment` 正式报告 + 选型结论 | **P0 + P1 完成后** |

---

## 8.1 扩题集：是否必须人工？推荐方向

### 是否必须人工？

| 环节 | 谁来做 | 要求 |
|------|--------|------|
| **题面 `prompt_zh`** | AI 起草即可 | 清晰、可判、对应真实子系统 |
| **gold（entrypoints / impacts）** | **必须人工核验** | 每条能在仓库或 `graph.json` / `*.ai.md` 锚点 **指到真值**；AI 起草仅作初稿 |
| **`topic_id` 划分** | 人工定 | S2 禁止相邻同 tag，避免泄漏误判困难 |
| **匹配规则** | 可沿用 T001 | path / graph_id 命中规则写死在 `matching_rules` |

原因：T001 的 gold 也是 AI 初稿 + 图谱命名；若 **不经过人工对照** `rg` / `00_main.ai.md` / manifest，P1 的 F1 与「谁更好」会 **双重幻觉**。

**推荐人机流程（每题约 30–60 分钟）**

1. AI 根据下面「方向模板」生成题面 + 候选 gold。  
2. 维护者用 `rg`、图谱锚点、manifest 端点表 **删假入口、补漏路径**。  
3. 冻结到 `tasks.json` 的 commit（与 `freeze_id` 同批图谱）。  
4. 再跑 S0→S1→S2（先单题打通脚本，再一次跑全题集）。

### 推荐题目方向（至少覆盖 3 类，与 T001 错开 `topic_id`）

选题原则：**图谱里真有边/锚点**、**改动后果可核验**、**不要纯运维口号**。

| 方向 | `topic_id` 示例 | 题面意图（示例） | gold 宜含 |
|------|-------------------|------------------|-----------|
| **A. 统一对话 / SSE 契约** | `unified_chat_sse` | 改 `POST /api/py/unified/chat/stream` 的 chain 事件 时，入口与 contract 敏感点？ | `api/unified_chat.py`、`api/index.py` 路由、`SSE`/`EV_TYPES` 节点、`_contract_manifest.json` |
| **B. Supabase RPC / ingest** | `ingest_rpc` | 调整 `ingest` / `match_documents` 链路时的入口与数据影响？ | `api/ingest_pipeline.py`、`ingest` 管理端点、`RPC`/`A1`/`A2`、相关 `supabase/sql` |
| **C. Text2SQL 分支** | `text2sql_branch` | 用户走 Text2SQL 而非 RAG 时，从路由到 SQL 生成的入口？ | `api/text2sql_api.py`、`T2S`/`T2S_DOC`、manifest 中 text2sql 端点 |
| **D. 鉴权 / ChatBI** | `auth_chatbi` | 变更 admin secret 或 ChatBI token 校验时的控制面入口？ | `api/chatbi_principal.py`、`AUTH`/`ERR_AUTH`、相关 GET 校验路由 |
| **E. 图谱门禁（meta）** | `tech_graph_gate` | 仅改 `graph.json` 导出/contract check 失败时，应跑哪些命令？ | **仅** `tools/tech_graph_*`、CI workflow 名；**不宜**扯业务 RAG（与 A–D 错开） |

**不建议**作为 early 题：过大而空的「重构整个 RAG」；无 manifest 端点的纯文档 typo；需要 **未在图谱出现** 的文件路径（除非标 `unknowns` 并降权）。

### 与当前 T001 的关系

- T001（`rag_env_embedding`）保留，作为 **env/向量维度** 基线。  
- 新增 **2–4 题** 覆盖 A–E 中 **至少 3 个不同 `topic_id`**，再跑 S2 才有「换题」意义。  
- 题集 v2 建议文件：`fixtures/gate_ctx_ab_v1/tasks.json`（同文件追加）+ 在 commit message 标明 `tasks_v2`。

---

## 9. 一句话综合结论

**在静态载荷体积几乎相同的前提下，JSON 与 Mermaid 作为 LLM 主上下文均可完成 T001 结构化分析；剔除离群与并行顺序偏差后，本终批 S0 显示 JSON 在墙钟与 token 中位数上略优，但仅单题 S0、样本极少——定稿前必须先完成扩题集（人工核验 gold）、S1、S2 与质量计分，不可仅凭加跑 S0 轮次签收选型。**

---

## 附录：复现命令

```bash
cd ai-ink-brain-api-python
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/materialize_payloads.py
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/run_s0_batch.py --rounds 3
```

主表：[`runs/.../111037/aggregate.md`](../runs/gate_ctx_ab_v1_batch_20260516_111037/aggregate.md)
