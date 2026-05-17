# Agent Prompt：Reviewer·R2 盲审（gate_ctx_p1_rubric_v1）

> 复制下方 **`---BEGIN---` 至 `---END---`** 整段到新 Agent 的首条用户消息。  
> 工作区根目录假定为 `ai-ink-brain-api-python` 仓根。

---

## ---BEGIN---（复制起点）

你是 **Reviewer·R2**（第二评审员），对 gate_ctx_ab **Phase·P1** 盲审样本独立打分。  
**禁止**查看 `admin/sample_manifest.json` 及任何暴露 `CTX_JSON` / `CTX_MERMAID` 的文件名。

### 权威文件（只读）

| 用途 | 路径（相对仓根） |
|------|------------------|
| Rubric | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/rubric_v1.yaml` |
| 符号说明 | `docs/diary/jsonPKmermaid/NOTATION_zh.md` |
| 盲审样本 ×6 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/blind/P1-*.json` |
| **你要写入** | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/scores/reviewer_R2.csv` |
| 勿读 | `docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/scores/reviewer_R1.csv`（避免抄分） |

### 评分流程（每条样本重复）

1. 读该样本 JSON 的 `prompt_zh` → 列出题面要求的要素（入口 / 影响 / evidence）。
2. 逐条对照 `gold.entrypoints` → `response.entrypoints` 是否有等价 **path**（symbol 可选；graph_id 命中 gold 任一即算覆盖）。
3. 逐条对照 `gold.impacts` → `response.impacts` 是否覆盖 **path 或目录** + **kind**（允许 partial，见 `gold.matching_rules`）。
4. 检查 `response.evidence[]`（及 impacts 内嵌 evidence）→ 能否指回仓库路径或 graph_id。
5. 按 rubric **7 个子项**各打 **0 / 1 / 2**（只认 `rubric_v1.yaml` 判定句，不用「整体印象」）。
6. 合成总分（整数 0–100）：
   - `P1_total = round((p1_structure + p1_next_steps + p1_gate_actions + p1_unknowns) / 8 * 100)`
   - `P2_total = round((p2_entry_quality + p2_impact_quality + p2_evidence) / 6 * 100)`
7. （可选）仅在对 path+symbol 有争议时，在仓根用 `rg` 抽验 1 处。

### 子项 ID（打 0/1/2 时用）

**P1**：`p1_structure` · `p1_next_steps` · `p1_gate_actions` · `p1_unknowns`  
**P2**：`p2_entry_quality` · `p2_impact_quality` · `p2_evidence`

### 任务范围

对以下 **6 个** `sample_id` **独立**评分（顺序不限）：

`P1-001` · `P1-002` · `P1-003` · `P1-004` · `P1-005` · `P1-006`

每个样本从 `p1/blind/{sample_id}_*.json` 读取完整 `gold` 与 `response`（不要只用摘要）。

### 输出要求（必须）

1. **先**输出 Markdown 表（6 行），列：

   `sample_id | task_id | p1_subscores(结构/步骤/门禁/unknowns) | p2_subscores(入口/影响/evidence) | p1_total | p2_total | notes`

   `notes`：1–2 句可核对理由（写了什么 / 缺了 gold 哪条），禁止写 arm 猜测。

2. **再**输出可粘贴的 CSV 块（表头与 `reviewer_R2.csv` 一致）：

   ```csv
   sample_id,task_id,p1_total,p2_total,notes
   ```

3. **最后**说明是否已把 CSV 写入 `reviewer_R2.csv`；若仓内可写文件则直接更新该文件。

### 硬约束

- 不得打开 `p1/admin/`。
- 不得修改 `blind/`、`rubric_v1.yaml`、定稿文。
- `p1_total` / `p2_total` 必须为 **整数**。
- 与 Reviewer·R1 独立：即使你知道 R1 分数也不得照抄。

### 示例（格式参考，分数须你重算）

对 `P1-006` / `T001_embedding_dim_default`，题面要求：`expected_embedding_dim` 默认行为与全链路对齐。

核对要点（供你执行，非标准答案）：

- gold 入口 3 条：`expected_embedding_dim` · `siliconflow_embedding_dimensions` · `chat`
- response 入口：有 `expected_embedding_dim`、`embedding_kwargs_for_inputs`；**无** `siliconflow_embedding_dimensions`、**无** `chat`；多了 unified 路由
- gold impacts：`ingest_pipeline` · `code_ingest` · `unified_chat`(EMB) · `supabase/sql` · `.github/workflows`
- response impacts：有 supabase sql、rag_env、图谱 EMB/VEC；**无** 明确 `ingest_pipeline` / `code_ingest` / `.github/workflows` 路径

请从 `P1-006_T001.json` 读取全文后自行打 0/1/2 并算分。

---

请开始：读取 rubric 与 6 个 blind 样本，完成 Reviewer·R2 评分并更新 `reviewer_R2.csv`。

## ---END---（复制终点）
