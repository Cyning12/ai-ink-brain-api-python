## Prompt A V3（禁用图谱）— KPI：易交接 > 可靠性 > 省钱 > 省时

你是一个新的后端理解与交接文档 Agent。任务：**在不读取 `docs/_tech_graph/` 的前提下**，完成对 `ai-ink-brain-api-python` 的「可交接」级别梳理，并把结果写入指定文件。

### 0. 强制约束

- **禁止读取**：`docs/_tech_graph/**` 下的图谱正文（全部 `.md`/`.ai.md` 及其他用于阅读的图谱文件）。
- **例外（门禁真值，最小范围）**：为交接「CI/manifest 闸门」允许 **仅** 打开 **`docs/_tech_graph/_manifest.json`**；若输出涉及 Unified SSE 契约变更说明，允许 **仅** 打开 **`docs/_tech_graph/_contract_manifest.json`**。除此二文件外，**仍禁止**读取 `docs/_tech_graph/` 下任何其他路径。
- **禁止**从别处复述图谱全文；若其他文档引用图谱路径，跳过细节。
- **事实来源**：仅真实代码、`supabase/sql/*.sql`、`docs/meta/`、`tests/`、`.env.example`、`requirements.txt` 等；禁止编造 endpoint、RPC、表名、env。
- **KPI 顺序**：产出结构与评分优先级为 **易交接（P1）> 可靠性（P2）> token（P3）> 时间（P4）**。不要在篇幅上堆砌 token，而把篇幅用在锚点与可执行清单。

### 1. Token / 时间估算（统一口径，便于与 B 对照）

- **代码/SQL**：约 **12 tokens/行**。
- **Markdown 文档**：约 **10 tokens/行**。
- **命令/grep 输出**：约 **8 tokens/行**。
- **输出**：中文为主的正文按 **约 4 字符 ≈ 1 token**（注明公式）。
- **时间**：分项给出 `t_scan` / `t_read` / `t_synthesis` / `t_total`（可为估算，注明依据）。

### 2. 输出文件（必须落盘）

**落盘规则（已定稿，勿在旧文件文末拼接）**：

1. **`docs/diary/test/result_A_no_tech_graph_v3.md`**：保留为 **首轮 V3 基线**（历史对照用）；**禁止**在本文件末尾追加「补丁运行」段落或覆盖写入，除非任务明确要求「重置基线」。
2. **当前 Prompt（含 manifest/门禁补丁）的执行结果**：写入 **新文件** **`docs/diary/test/result_A_no_tech_graph_v3_patch.md`**。若同一 Prompt 多次复跑需保留历次产出，改用 **`result_A_no_tech_graph_v3_patch2.md`** 递增序号。
3. 文首一行元信息（必填）：`Prompt 文件`、`执行日期（YYYY-MM-DD）`；可选：`git rev-parse --short HEAD`（若环境允许）。

说明：**不在原文档下面追加补丁输出**，便于 diff、对照实验与版本回溯。

### 3. 结果文件固定标题顺序（必须完全一致）

#### P1 易交接（权重最高）

1. **冷启动接手清单**（10～15 步；每步一句可执行动作；足够让另一名 Agent 从零跟上）
2. **锚点索引表**（路径/RPC/表/env → `文件路径` + `函数名或行区间` + 一句职责）
3. **新人 FAQ**（6～10 条；每条含证据锚点）
4. **改动配方卡**（三卡固定：
   - 新增 HTTP 端点（**强制**：写明同步 **`docs/_tech_graph/_manifest.json`**；合并前本地执行 **`python tools/tech_graph_manifest_check.py`**；若涉及 SSE 契约键集变更则一并写明 **`_contract_manifest.json`** 与 **`python tools/tech_graph_contract_check.py`** 的适用条件，均以仓库内 `tools/`、`.github/workflows/` 为准）
   - 调整检索策略（向量/keyword/融合/threshold）
   - 调整 ingest（markdown/code）
   每张卡：**必读文件**、**慎碰点**、**推荐验证**：本地命令或请求维度描述）

#### P2 可靠性

5. **摘要**（≤200 字）
6. **模块地图与主链路**（按链路小节：Legacy RAG / Unified / Text2SQL / Ingest / Code RAG）
7. **事实断言清单**（表格：`断言 | 证据 | 核验方式 | 置信度`）
8. **不确定性与验证步骤**

#### P3/P4

9. **消耗明细**（时间 + token，分项累计 + 估算公式）
10. **覆盖率**（读过哪些文件；若抽样请注明读到 approximately 哪些行段）

---

### 4. 质量门槛（自检后再提交）

- 任意 endpoint/RPC/env/表出现在「断言」或「锚点表」中，必须有证据列或可核验路径。
- 「不确定」宁可多写，不可用臆测补足。
- **「新增 HTTP 端点」配方卡** 必须包含 **`_manifest.json` 同步 + `tech_graph_manifest_check.py`**；不得仅写「在 `api/index.py` 注册路由」而略过门禁。
- **不要为了压低 token 删掉锚点表与接手清单**：这两部分是 P1 核心交付。
