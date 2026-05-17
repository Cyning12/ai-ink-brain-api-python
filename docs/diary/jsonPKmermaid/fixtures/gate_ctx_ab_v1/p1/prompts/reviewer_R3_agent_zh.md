# Agent Prompt：Reviewer·R3 仲裁（gate_ctx_p1 · 4 条分歧样本）

> 复制 **`---BEGIN---`～`---END---`** 到 **Cursor 外** 的模型（需能读本地文件）。  
> 仓根（绝对路径）：`/Users/cyning/Desktop/Projects/ai-ink-brain-api-python`

---

## ---BEGIN---（复制起点）

你是 **Reviewer·R3（仲裁员）**。Reviewer·R1 与 Reviewer·R2 已对 6 条盲审样本打分，其中 **4 条** 在 KPI·P1 或 KPI·P2 上分歧 ≥15 分，需要你给出 **终裁分数**。

**符号**：Reviewer·R3 ≠ 定稿文里的 Rule·R1–R6（签收规则）。见符号表。

---

### 本地文件路径（必读 / 可写）

| 用途 | 绝对路径 |
|------|----------|
| Rubric（0/1/2 判定句） | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/rubric_v1.yaml` |
| 符号说明 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/NOTATION_zh.md` |
| R1 分数 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/scores/reviewer_R1.csv` |
| R2 分数 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/scores/reviewer_R2.csv` |
| 分歧汇总表 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/scores/aggregate_p1.md` |
| **arm 映射（仲裁时可读）** | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/admin/sample_manifest.json` |
| 盲审样本 P1-001 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/blind/P1-001_T002.json` |
| 盲审样本 P1-002 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/blind/P1-002_T003.json` |
| 盲审样本 P1-003 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/blind/P1-003_T001.json` |
| 盲审样本 P1-006 | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/blind/P1-006_T001.json` |
| **你要写入** | `/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/p1/scores/reviewer_R3_arbitration.csv` |
| 无需仲裁（勿改分） | P1-004、P1-005：见 `aggregate_p1.md` |

可选：在仓根用 `rg` 抽验争议 path+symbol（例如 `api/unified_chat.py` 是否存在 `handle_unified_chat_stream`）。

---

### 待仲裁一览（来自 aggregate_p1.md）

| sample_id | task_id | R1 P1 | R1 P2 | R2 P1 | R2 P2 | ΔP1 | ΔP2 |
|-----------|---------|------:|------:|------:|------:|----:|----:|
| P1-001 | T002_unified_sse_chain_contract | 62 | 68 | 50 | 50 | 12 | **18** |
| P1-002 | T003_ingest_admin_rpc | 58 | 80 | 38 | 50 | **20** | **30** |
| P1-003 | T001_embedding_dim_default | 50 | 52 | 38 | 33 | 12 | 19 |
| P1-006 | T001_embedding_dim_default | 62 | 82 | 38 | 67 | **24** | 15 |

---

### 仲裁流程（每条争议样本）

1. 读该样本 blind JSON：`prompt_zh`、`gold`、`response`（全文，勿只用摘要）。
2. 读 R1/R2 的 `notes`（在各自 CSV 中）理解分歧点。
3. 按 `rubric_v1.yaml` **7 个子项**自评 0/1/2（可写在输出 notes 里），**不得**简单取 R1/R2 平均数作为终裁，除非子项证据支持。
4. 给出 **final_p1_total**、**final_p2_total**（0–100 整数）及 **arb_notes**（引用 gold 条目 / response 字段 / 是否采纳 R1 或 R2 的哪一侧）。
5. 从 `sample_manifest.json` 记录该样本的 **arm**（`CTX_JSON` 或 `CTX_MERMAID`），写入 CSV。

**合成公式（与子项一致时）**：

- `final_p1 = round((p1_structure + p1_next_steps + p1_gate_actions + p1_unknowns) / 8 * 100)`
- `final_p2 = round((p2_entry_quality + p2_impact_quality + p2_evidence) / 6 * 100)`

---

### 输出格式（必须）

#### 1）Markdown 仲裁表（4 行）

列：`sample_id | arm | R1(P1/P2) | R2(P1/P2) | final_p1 | final_p2 | 采纳倾向 | arb_notes`

`采纳倾向`：如「偏 R1」「偏 R2」「折中」「重算」。

#### 2）CSV 文件（写入上述路径）

```csv
sample_id,task_id,arm,r1_p1,r1_p2,r2_p1,r2_p2,final_p1,final_p2,arb_notes
P1-001,T002_unified_sse_chain_contract,CTX_JSON,62,68,50,50,,,
...
```

（`arm` 从 manifest 读取；`final_*` 填你的终裁整数。）

#### 3）按 arm 终裁均值（4 条终裁 + P1-004/005 用 R1≈R2 均值）

| arm | 样本 | final P1 均值 | final P2 均值 |
|-----|------|--------------:|--------------:|
| CTX_JSON | P1-001,002,003 | ? | ? |
| CTX_MERMAID | P1-006 + 004,005 | ? | ? |

说明：P1-004/005 无仲裁，终裁可取 `(R1+R2)/2`：`P1-004` → P1=76, P2=98；`P1-005` → P1=64, P2=86。

#### 4）一句结论

人审终裁后，**CTX_JSON vs CTX_MERMAID** 在 P1/P2 上谁更高？是否改变定稿文「不签收一律 JSON」？（**不修改** Rule·R1–R6，仅建议。）

---

### 硬约束

- 必须读取列出的 **绝对路径** 文件；路径不存在则报告，勿编造分数。
- 只仲裁上表 **4 条**；勿改 P1-004/005。
- `final_p1` / `final_p2` 必须为整数。
- 仲裁后可读 `sample_manifest.json`；R1/R2 盲审时不能读，**你可以读**。

---

请开始：读取所有路径文件，完成 4 条仲裁并写入 `reviewer_R3_arbitration.csv`。

## ---END---（复制终点）
