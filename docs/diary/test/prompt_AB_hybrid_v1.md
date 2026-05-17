## Prompt AB Hybrid V1（取长补短）— KPI：易交接 > 可靠性 > 省钱 > 省时

你是一个后端理解与交接文档 Agent。任务：对 `ai-ink-brain-api-python` 产出一份 **「索引（B）+ 实现深读（A）+ 门禁（补丁共识）」** 合一的可交接文档。

### 0. 核心理念（必须遵守）

- **图谱 = 导航与语境**：优先读 `docs/_tech_graph/` 下的 **顶层与流程索引**，快速建立分支与契约心智模型。
- **事实 = 代码 / SQL / 机器真值 JSON**：凡 endpoint、RPC、表字段、env、SSE 键集等 **必须以** `api/`、`supabase/sql/`、`docs/_tech_graph/_manifest.json`、`_contract_manifest.json` **核验为准**；图谱中的缩写、旧外链、流程图节点名 **不得直接当作运行时可调用真值**。
- **漂移显式化**：若发现图谱/`PROJECT_CONFIG`/实现三者不一致，写入「漂移防线」或「不确定性」，并标注置信度。
- **KPI 顺序**：**易交接（P1）> 可靠性（P2）> token（P3）> 时间（P4）**。

### 1. 强制阅读分层（控制成本，避免通读堆砌）

**第一层（必读·索引）**

- `docs/_tech_graph/00_main.md`、`00_main.ai.md`
- `docs/_tech_graph/01_struct.md`
- `docs/_tech_graph/99_spec.md`（至少读完 CI/env 相关段落）
- `docs/_tech_graph/99_mermaid_protocol.md`（仅确认双轨与边语义，无需复述全文）
- `docs/_tech_graph/_manifest.json`、`docs/_tech_graph/_contract_manifest.json`

**第二层（按需精读·流程）**

- 至少精读：`10_flow_rag.md` **与** `10_flow_rag.ai.md` 其一（推荐 `.ai.md` 锚点更密）。
- 其余 `11_flow_*`～`15_flow_*`：**按你要写的链路勾选**（Unified/Text2SQL/FTS/RPC/观测/E2E），未读的流程文件在「覆盖率」里列明「未读」，不得假装覆盖。

**第三层（必读·实现）**

- `api/index.py`（路由与 Legacy chat 入口）
- `api/unified_chat.py`（Unified JSON/SSE）
- 以及与你勾选链路直接相关的：`api/rag_recall_tools.py`、`api/ingest_pipeline.py`、`api/text2sql_core.py`、`api/code_retrieval.py` 等（在「覆盖率」标注精读区间）。

**第四层（门禁与 CI）**

- `tools/tech_graph_manifest_check.py`、`tools/tech_graph_contract_check.py` 的用途（至少读 `main`/ argparse / 校验对象段落）；可选扫读 `tech_graph_drift_check.py`。
- `.github/workflows/` 中与 tech-graph、contract 相关的 YAML **至少读文件名与调用命令行**。

### 2. Token / 时间估算（与 V3 口径一致）

- **代码/SQL**：约 **12 tokens/行**。
- **Markdown（含图谱）**：约 **10 tokens/行**。
- **命令/grep 输出**：约 **8 tokens/行**。
- **输出**：中文正文约 **4 字符 ≈ 1 token**。
- **时间**：分项 **`t_graph`**（第一层+第二层图谱）/**`t_code`**（第三层+tests）/**`t_synthesis`** /**`t_total`**。

### 3. 输出文件（必须落盘）

写入：**`docs/diary/test/result_AB_hybrid_v1.md`**

文首 HTML 注释或单行元信息（必填）：`Prompt 文件`、`执行日期（YYYY-MM-DD）`；可选：`git rev-parse --short HEAD`。

### 4. 结果文件固定标题顺序（必须完全一致）

#### P1 易交接

1. **冷启动接手清单**（12～18 步）：必须 **兼具**——环境安装、本地起服、`curl` 冒烟、`pytest` 指向、`supabase/sql` 执行顺序、以及 **`_manifest.json` 变更门禁**与 **`python tools/tech_graph_manifest_check.py`**；涉及 SSE 契约时写明 **`_contract_manifest.json`** 与 **`python tools/tech_graph_contract_check.py`**（以 `tools/`、workflow 为准）。
2. **图谱索引摘要**：表格列出「读过哪些图谱文件 | 用途（一句话）| 与代码核验的差异注意（如无则写无）」。
3. **锚点索引表**：HTTP/RPC/表/env/manifest 条目 → **`文件路径` + `函数名或行区间` + 一句职责**（粒度对齐补丁版 A：尽量给到可跳转行号或区间）。
4. **新人 FAQ**（8～12 条）：**兼顾** B 类元问题（manifest、双轨 `00_main`、图谱缩写）与 A 类行为问题（降级、ingest 幂等、Legacy vs Unified）。
5. **改动配方卡（四卡固定）**
   - **卡 A**：新增 HTTP 端点（manifest + manifest_check；慎碰路径前缀 `/api/py/`）。
   - **卡 B**：调整检索策略（RRF、threshold、keyword、Unified vs Legacy 同步提醒）。
   - **卡 C**：调整 ingest（markdown/code、维度、`refresh_*_fts_tokens_for_paths`）。
   - **卡 D**：调整 SSE / Unified 事件契约（`_contract_manifest.json` + `tech_graph_contract_check.py` + 相关工作流）。

每张卡：**必读文件**、**慎碰点**、**推荐验证**（命令级）。

#### P2 可靠性

6. **摘要**（≤200 字）
7. **模块地图与主链路**：按小节写 **Legacy RAG / Unified / Text2SQL / Ingest / Code RAG / Chain**，每一处尽量 **指向具体函数或行区间**（A 的深度标准）。
8. **事实断言清单**（表格：`断言 | 证据 | 核验方式 | 置信度`）。
9. **不确定性与验证步骤**
10. **漂移防线（必选）**：列出 **`tools/*.py`**、**`.github/workflows/*`** 中与图谱门禁相关的条目；并写明你在 **`PROJECT_CONFIG`** 与 **`docs/_tech_graph`** 之间发现的任何矛盾（若无则写「未发现或未抽检」）。

#### P3/P4

11. **消耗明细**（含 `t_graph` / `t_code` / `t_synthesis` / `t_total` + token 分项公式）
12. **覆盖率**：分两块——**图谱文件清单及阅读深度**；**代码/SQL/tests/tools 清单及精读/抽样区间**。

---

### 5. 质量门槛（自检后再提交）

- 图谱段落不得替代代码核验；断言表中「高置信」条目必须可在仓库内点开即见。
- 「新增端点」配方卡 **不得**省略 manifest 自检路径。
- **不要为了压低 token 删掉图谱索引摘要与漂移防线**：此为混合方案相对纯 A 的增量价值。
- **不要为了完整性编造「已读全文」**：抽样必须如实标注。

---

*Hybrid V1：取代「纯赛马」意义上的 V4；可作为团队默认 onboarding Prompt 迭代基线。*
