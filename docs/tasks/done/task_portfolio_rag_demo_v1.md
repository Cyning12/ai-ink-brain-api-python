# Task：Portfolio 演示站 RAG — RUNBOOK · env 文档 · 五问预跑留证（后端）

> **状态**：`done`（W2/W3/W5 关账 · 2026-06-03 · `HG-W5-FIVE-Q` · `HG-REINSPECT` approved）  
> **schedule_ref**：投递冲刺 `[投递冲刺_20260609_v1_zh.md](../spec/governance/投递冲刺_20260609_v1_zh.md)` · P0-C  
> **硬 deadline**：**2026-06-09 上午**（投递前 ingest 对齐 + 五问 RUNBOOK + 预发/生产等价环境 sync 与五问预跑留证）  
> **治理 SPEC（L1 · 已冻结）**：`[SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md)` · `PORTFOLIO-RAG-DEMO@2026-06-01`  
> **配对前端 SPEC（只读）**：`ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md`  
> **关联图谱**：`[docs/_tech_graph/10_flow_ingest.ai.md](../_tech_graph/10_flow_ingest.ai.md)`（ingest/sync 只读对照）

---

## Harness 元信息（执行 Agent 必读）


| 字段                     | 值                                                                                                              |
| ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| **task_slug**          | `portfolio-rag-demo`                                                                                           |
| **test_strategy**      | `recommended`                                                                                                  |
| **test_strategy_note** | 验收以 **人工 RUNBOOK**（sync 轮询 + 五问预跑 + sources 留证）为主；可选补 smoke pytest（如 ingest env 解析）由 30 择要，**非** red-green 硬门槛 |
| **freeze_id**          | `PORTFOLIO-RAG-DEMO@2026-06-01`                                                                                |
| **gates_before_code**  | `failure_paths`、必读列表、验收命令、W4 前端 content 就绪确认                                                                   |
| **semi_auto**          | `true`                                                                                                         |
| **audit_profile**      | `post_close`                                                                                                   |
| **experience_capture** | `recommended`                                                                                                  |
| **kpi_rubric**         | `KPI_RUBRIC_v1_2`                                                                                              |
| **kpi_aggregator**     | `CLOSE`                                                                                                        |
| **git_branch**         | `task/portfolio-rag-w5-v1`（W5 关账 Loop · 自 `task/portfolio-rag-demo-v1` 续跑）                                     |
| **Open Folder**        | `ai-ink-brain-api-python`（W2/W3 落盘）；W5 预跑须开双仓读前端 content / Unified Chat                                        |
| **推荐路径**               | **A（22 R1）** — 与前端 portfolio task 审查节奏对齐                                                                       |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


### 工作包映射（SPEC §7 → 本 task）


| SPEC ID | 工作包              | 本 task 范围                 | 执行帽    |
| ------- | ---------------- | ------------------------- | ------ |
| W2      | RUNBOOK 正文       | **在范围**                   | 30     |
| W3      | env / deploy 文档  | **在范围**                   | 30     |
| W5      | 生产 sync + 五问预跑留证 | **在范围**（人触发 sync；40 回填留证） | 人 + 40 |
| W4      | 前端 content 三类目录  | **依赖 · 非本仓 commit**       | 前端 30  |
| W1      | SPEC 冻结          | **已完成**                   | —      |


### 跨仓依赖


| 项              | 说明                                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **blocked_by** | 前端 W4：`ai-ink-brain/content/{methodology,resume,evidence}/` 目标态文稿就绪（见 `[投递冲刺_20260609_v1_zh.md](../spec/governance/投递冲刺_20260609_v1_zh.md)` §3.2） |
| **blocks**     | 投递 P0-C / P0-D 录屏；前端 portfolio 演示站五问 chip 联调                                                                                                      |
| **配对 task**    | `ai-ink-brain` · `task_portfolio_demo_site_v1`（并行 Harness · 22 R1 节奏对齐）                                                                           |


### 人工闸 `human_gate`


| human_gate_id | status   | blocks_hats | 说明                                                                                                          |
| ------------- | -------- | ----------- | ----------------------------------------------------------------------------------------------------------- |
| HG-TASK-DRAFT | approved | 22-R1,30    | semi_auto 链式执行人授权 · 2026-06-01                                                                              |
| HG-AUDIT-R1   | approved | 30          | 22 R1 零阻塞 · `reviews/.../audit_R1_20260601.md`                                                              |
| HG-W5-SYNC    | approved | —           | sync `succeeded` · job `c44158a5-…` · 人签 2026-06-03 · 留证 `docs/diary/samples/portfolio-rag-demo/sync-job-*` |
| HG-W5-FIVE-Q  | approved | —           | 五问 UI 5/5 · diary 留证 · 人签 2026-06-03                                                                 |
| HG-REINSPECT  | approved | —           | 关账复检 · 人签 2026-06-03 · 合并 PR 前仍须 pytest 绿                                                      |


---

## 1. 背景与目标

Portfolio 演示站需在 **2026-06-09 投递前** 展示与前端 `content/` **同源** 的 RAG 问答能力：语料经 `**POST /api/py/admin/sync`** 入库（`CONTENT_ROOT` → 前端仓 `ai-ink-brain/content/`），并通过 **可复现的五问 RUNBOOK** 验收 Q1～Q5。

**本 task 完成态（后端仓）**：

1. **W2**：可操作 RUNBOOK 落盘 `[docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md)`，与 SPEC §4～§6 一致。
2. **W3**：`CONTENT_ROOT` 及 admin/sync 相关 env 的 **生产/本地部署说明** 落盘（`PROJECT_CONFIG` §C 增补 portfolio 段落，与 RUNBOOK §8 交叉链接）。
3. **W5**：在 **预发 / Preview 与生产等价环境**（同 Supabase、同 Embedding 维、同 `CONTENT_ROOT` 挂载语义）由 **人** 执行 sync + 五问预跑；**本地执行产物默认落** `tmp/portfolio-rag-demo/`（`PORTFOLIO_RAG_EVIDENCE_DIR`）；**人签后**脱敏复制至 `docs/diary/samples/portfolio-rag-demo/`；40 帽回填 task `**### 自检结论（执行者）`**。

**现网 ingest 行为无需改码**（SPEC §2 扫描结论）：category = 相对路径第一段；portfolio 仅 `**admin/sync`** 路径。

---

## 2. 范围

### 2.1 W2 · RUNBOOK（30 帽交付）

- **G-W2-1** 新建 RUNBOOK，必含 SPEC §5.1 八节：前提与权限 / Sync 执行 / 失败排障 / 五问验收表 / 单问重试 ≤3 / Sources 留证（Q1、Q5 强制）/ 卷四·五 release 后再 sync / Env 指针  
- **G-W2-2** 五问问句与 `[投递冲刺_20260609_v1_zh.md](../spec/governance/投递冲刺_20260609_v1_zh.md)` §2 **逐字对齐**（SPEC §6.2 真值表）  
- **G-W2-3** Q3 sources 硬约束：**仅** `metadata.category == evidence`（不含 methodology vol3）  
- **G-W2-4** Sync 硬检查：`succeeded` 且 `filesScanned > 0` 且 `chunksUpserted > 0`；三目录各 ≥1 `.md`  
- **G-W2-5** 仅 `admin/sync`；**不含** `admin/ingest` 备用路径  
- **G-W2-6** 轮询间隔 2～5s，总超时 ≤60 min；`404 Job not found` → 重新 POST

### 2.2 W3 · env / deploy 文档（30 帽交付）

- **G-W3-1** 在 `[PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md)` **§C** 增补 **portfolio 演示站** 段落：`CONTENT_ROOT`、`**SYNC_ADMIN_SECRET`**（admin/sync 真值）、`EMBEDDING_DIM`、`SILICONFLOW_*`、Supabase 写库变量（**不含真实密钥**）  
- **G-W3-2** 说明本地 `CONTENT_ROOT` 指向前端仓 `content/` 的示例；生产 mount / CI checkout 语义与 Vercel 部署边界（SPEC §1.1 Q-3）  
- **G-W3-3** 明确 **禁止** 生产依赖后端仓默认 `REPO_ROOT/content` 回退作为 portfolio 真值  
- **G-W3-4** RUNBOOK §8 与 PROJECT_CONFIG 双向链接

### 2.3 W5 · 预跑留证（人 + 40 帽 · 本 task 验收项）

> **Agent 禁止** 在本 task 内对生产/预发执行 `POST /api/py/admin/sync`；仅 RUNBOOK 与留证目录规范。


| ID         | 验收项         | 硬标准                                                                                                                                                                          | 留证 / 闸                                                |
| ---------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **G-W5-1** | sync job 终态 | `job.status=succeeded`；`filesScanned>0`；`chunksUpserted>0`；`methodology/`、`resume/`、`evidence/` **各 ≥1** `.md` 被扫描                                                           | `sync-job-final.json` · **HG-W5-SYNC** 人签             |
| **G-W5-2** | 五问预跑        | 问句与 `[投递冲刺_20260609_v1_zh.md](../spec/governance/投递冲刺_20260609_v1_zh.md)` §2 **逐字**；**5/5** 非空切题；sources **≥4/5**；Q3 sources **仅** `metadata.category==evidence`；单问重试 **≤3** | `five-questions-results.md`                           |
| **G-W5-3** | Q1/Q5 可复现   | 同 **ChatBI visitor Bearer**、同问句预跑 **2 次**；主 `metadata.category` **一致**（不一致 → F6 **FAIL**）                                                                                    | `q1-sources-run{1,2}.json`、`q5-sources-run{1,2}.json` |
| **G-W5-4** | 留证目录        | 本地：`tmp/portfolio-rag-demo/`（默认）；冻结：`docs/diary/samples/portfolio-rag-demo/` 上表文件可读（脱敏、无密钥）                                                                                  | **HG-W5-FIVE-Q** 人签                                   |
| **G-W5-5** | Unified 路径  | `POST /api/py/unified/chat` 或 `/stream`；visitor **不禁 text2sql**（T-05）；**非** `SYNC_ADMIN_SECRET` / admin Bearer                                                               | RUNBOOK §4                                            |


**鉴权分工（W5 不得混用）**


| 用途                            | Header / Secret                                                                 | 说明                                                                |
| ----------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **admin/sync**                | `Authorization: Bearer $ADMIN_TOKEN`（`export ADMIN_TOKEN="$SYNC_ADMIN_SECRET"`） | 仅 sync job；**禁止**用于五问；**≠** visitor token                         |
| **history / 五问 Unified Chat** | `Authorization: Bearer $VISITOR_CHATBI_TOKEN`                                   | Supabase `chatbi_access_tokens` 行；运维签发见 RUNBOOK §1.4              |
| **前端 W3 unlock**              | `POST /api/auth/unlock` + `PORTFOLIO_VISITOR_*`                                 | **前端仓** BFF Cookie；本 task **不实现**；curl 直连 Python 时用 ChatBI Bearer |


**与前端 W3 分工（只读 · `[SPEC-portfolio_demo_site_v1_zh.md](../../../ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md)` §4.3）**


| 层                 | 职责                                                                         | 本 task                    |
| ----------------- | -------------------------------------------------------------------------- | ------------------------- |
| **前端 W3**         | `tools/gen-portfolio-secrets.sh` · portfolio unlock Cookie · Unified 页内 UX | **非范围** · defer           |
| **后端 W5 RUNBOOK** | 运维 **ChatBI visitor token** 签发指针 · curl 五问 · sync 留证规范                     | **在范围** · 30 帽            |
| **BFF 转发**        | 访客 session → Python Unified 时带 Bearer                                      | 联调时人确认；本仓只文档化 Python 侧校验链 |


**failure_paths 覆盖（W5 执行）**：**F5**（单问 3 次仍不达标 → 记 FAIL · 不得刷通过率）· **F6**（Q1/Q5 双跑 category 漂移 → FAIL · diary 标注 blocker）· **F7**（Q3 命中 methodology → FAIL）· **F8**（W4 未就绪即 sync → 硬 FAIL · 不得进五问）。

### 2.4 W6 增量需求（SPEC §4.5 · **文档已入 SPEC · 待实现 · 不阻塞 W5 文档关账**）

> **2026-06-03**：W6 前端 E2E 验收期间追加；**本 task 回合不改 `api/`**。


| ID     | 需求                                        | 现状（代码扫描）                                                    | 落点                                  | 状态                           |
| ------ | ----------------------------------------- | ----------------------------------------------------------- | ----------------------------------- | ---------------------------- |
| **R1** | RAG 回答须带出具体来源（侧栏 `rag.sources`）           | Unified 已发 `rag.sources`；正文不强制 inline 引用                    | SPEC §4.5.2                         | **文档化** · W6 验收 sources ≥4/5 |
| **R2** | sources 含 `**relativePath`/`path`** 供前端跳转 | `build_sources_payload` **已输出**；前端 `SourceCitations` 未做站内路由 | SPEC §4.5.3 · 配对前端 W6               | **后端字段 OK** · 跳转归前端          |
| **R3** | LLM 意图识别超时 **3 次重试**                      | `decide_intent_v2` **单次** LLM → timeout 即 V1 降级             | SPEC §4.5.4 · `api/intent_agent.py` | **待实现** · 不阻塞 W5/W6 E2E      |


**切片精度摘要**（验收预期管理）：`512` 字字符窗 + `50` overlap → **文件 + chunk_index** 级；**无**章节标题 / 行号（SPEC §4.5.1）。

---

## 3. 非范围

- 改 `api/`、`tests/` **业务实现**（ingest 现码已满足 SPEC §2 · **§4.5 R1～R3 待后续 task**）  
- 前端 Next 页面 / portfolio UX / 访客秘钥实现（前端 SPEC + task）  
- 本 task 回合 **执行** 生产或预发 `admin/sync`（仅 RUNBOOK 与留证规范）  
- 新建或大幅变更 `documents` schema、GraphRAG、Wiki batch ingest  
- ChatBI v3 preview 全链、§8 P1-B 双能力 handoff（6/9 后 Epic）  
- 卷四/卷五 **内容创作** 与公众 release（属 docs / 公众仓；release 后再 sync 见 RUNBOOK §7）

---

## 行为变更（Delta）

**无（W5 文档 tranche）** — 本 task 为 **文档 + 运维 RUNBOOK + 人工验收留证**；不修改对外 API 契约。

**W6 增量（2026-06-03 · SPEC §4.5）**：R2 sources 路径字段 **现网已有**；R3 意图 3 次重试 **待后续实现**；R1 侧栏 sources **现网已有**、正文 inline 引用为可选增强。详见 §2.4。

---

## 5. 依赖与引用


| 依赖项            | 路径 / 说明                                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| 治理 SPEC        | `[SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md)` |
| 投递计划           | `[投递冲刺_20260609_v1_zh.md](../spec/governance/投递冲刺_20260609_v1_zh.md)` §2 五问 · §3.2 content 树                    |
| PROJECT_CONFIG | `[PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md)`                |
| ingest 实现（只读）  | `api/ingest_pipeline.py`、`api/index.py`（admin/sync）                                                             |
| 冷温热术语          | `[GUIDE_冷温热层_对内术语_v1_zh.md](../harness/guides/GUIDE_冷温热层_对内术语_v1_zh.md)`                                        |
| Unified 契约     | `[docs/_tech_graph/_contract_manifest.json](../_tech_graph/_contract_manifest.json)`                            |
| `.env.example` | 仓库根 · `CONTENT_ROOT` 注释                                                                                         |


---

## 验收标准

### 6.1 文档（30 完成后）

- RUNBOOK 路径存在且 §5.1 八节齐全  
- PROJECT_CONFIG §C portfolio 段落存在且无真实密钥  
- RUNBOOK 与 SPEC §4.2.3 失败语义表 **一致**

### 6.2 预跑（W5 · 40 + 人签）


| 项                        | 标准                                              | 状态                                                                                 |
| ------------------------ | ----------------------------------------------- | ---------------------------------------------------------------------------------- |
| sync 终态 + 硬检查            | §2.4 G-W5-1                                     | **pass** · `HG-W5-SYNC` approved · job `c44158a5-…`                                |
| 五问指标 + Q3 strict         | §2.3 G-W5-2                                     | **pass** · UI 5/5 · `five-questions-results.md` · `w5-retest-backlog.md`              |
| Q1/Q5 双跑一致               | §2.3 G-W5-3                                     | **pass** · `q1/q5-sources-run{1,2}.json`                                                |
| 留证目录可读                   | §2.3 G-W5-4                                     | **pass** · diary 冻结 · P1 defer 已人签                                                  |
| Unified + visitor Bearer | §2.3 G-W5-5                                     | **pass** · RUNBOOK §1.3                                                                 |
| 人工闸                      | `HG-W5-SYNC` · `HG-W5-FIVE-Q` · `HG-REINSPECT` approved | 2026-06-03 维护者签收                                                                      |


### 6.3 CI

- `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（本 task **不应** 引入 api 变更；若仅 docs 则作回归确认）

---

## 失败路径


| #   | Scenario ID                       | 触发条件                                   | 系统行为                                 | 可重试                              | 用户可见 / RUNBOOK 处置    |
| --- | --------------------------------- | -------------------------------------- | ------------------------------------ | -------------------------------- | -------------------- |
| F1  | `fp-portfolio-embed-dim`          | Embedding 维度与 `vector(N)` 不一致          | sync job `failed`；`error` 含「维度」      | 修正 env 后 **重跑 sync**             | RUNBOOK §3 对照表第一行    |
| F2  | `fp-portfolio-files-scanned-zero` | `CONTENT_ROOT` 非目录或空树；`filesScanned=0` | job 可能 `succeeded` 但 **硬 FAIL**（Q-4） | 修正 mount / 补 content 后重跑         | **不得**进入五问           |
| F3  | `fp-portfolio-job-404`            | `404 Job not found`（redeploy）          | GET 轮询 404                           | **重新 POST** 创建 job               | sync 窗口避免并发 redeploy |
| F4  | `fp-portfolio-upstream-auth`      | SiliconFlow / Supabase 鉴权或网络失败         | job `failed` 或超时                     | 指数退避；查 Secrets                   | RUNBOOK §3           |
| F5  | `fp-portfolio-five-q-retry`       | 五问单问 3 次仍不达标                           | 记该问 **FAIL**                         | 可调 query/chip 或补 content 后再 sync | 不得刷通过率；阻塞 6/9 全绿     |
| F6  | `fp-portfolio-sources-drift`      | Q1/Q5 两次预跑 sources category 不一致        | 记 **FAIL**（Q-9:A）                    | 查 ingest category / 文稿路径         | diary 留证须标注 blocker  |
| F7  | `fp-portfolio-q3-evidence`        | Q3 sources 命中 `methodology`            | Q3 **FAIL**（strict evidence）         | 调整 evidence 文稿或检索参数              | RUNBOOK 五问表须写明       |
| F8  | `fp-portfolio-w4-blocked`         | 前端 W4 未就绪即 sync                        | `filesScanned` 不足三目录                 | 等待前端 content 后再 sync             | task `blocked_by`    |


---

## 8. 给执行帽的必读列表（30 · 按序）

1. 本 task 全文 + `**failure_paths`** + `**human_gate**`
2. `[SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md)` §4～§6
3. `[投递冲刺_20260609_v1_zh.md](../spec/governance/投递冲刺_20260609_v1_zh.md)` §2 五问表
4. `[PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md)` §C（改前读现表）
5. `api/ingest_pipeline.py` · `get_all_markdown_chunks()`（只读 · category 规则）
6. `api/index.py` · admin/sync 路由（只读 · job 字段）
7. 22 R1 审查 `[docs/harness/reviews/task_portfolio_rag_demo_v1_audit_R1_*.md](../harness/reviews/)`（**30 开工前须存在且零阻塞**）

**验证命令（合并前）**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 9. 文档矛盾（须以 freeze_id 为准）


| 矛盾      | 出处 A                              | 出处 B                                      | task 口径                                             |
| ------- | --------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| Q3 期望路径 | 投递冲刺 §2：「`evidence/`* **或 vol3**」 | SPEC §6.2（Q-2:A）：sources **仅** `evidence` | **以 SPEC / freeze_id 为准**；RUNBOOK 写 strict evidence |


---

### 6.3 CI

- `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（本 task **不应** 引入 api 变更；若仅 docs 则作回归确认）

---

## 10. 实现备忘（30 回填）


| 文件                                                                  | 动作                           | 状态              |
| ------------------------------------------------------------------- | ---------------------------- | --------------- |
| `docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md` | **新建**                       | done · 30       |
| `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`               | §C.1 增补 portfolio            | done · 30       |
| `docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md` | §1.3 ChatBI visitor token 指针 | W5 tranche · 30 |
| `docs/diary/samples/portfolio-rag-demo/README.md`                   | W5 留证 + blocked 说明           | W5 tranche · 30 |
| `docs/diary/samples/portfolio-rag-demo/NOTES-w5-pending_*.md`       | 待人 sync/五问占位                 | W5 tranche · 30 |
| `api/`、`tests/`                                                     | **不改**                       | —               |


---

### 自检结论（执行者）

> **40 帽 · 2026-06-02 · 分支 `task/portfolio-rag-w5-v1` · W5 文档 tranche**

#### 命令与退出码


| 命令                                                              | cwd | 退出码   | 摘要                                      |
| --------------------------------------------------------------- | --- | ----- | --------------------------------------- |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 仓库根 | **0** | **277 passed**, 1 skipped, 2 deselected |


#### 验收表


| 验收项                             | 结果       | 证据                                                             |
| ------------------------------- | -------- | -------------------------------------------------------------- |
| §6.1 RUNBOOK 八节 + §1.4 token 指针 | pass     | `RUNBOOK_portfolio_rag_five_questions_v1_zh.md`                |
| §6.1 PROJECT_CONFIG §C.1        | pass     | 无 env 缺口 · 未改                                                  |
| §6.1 失败语义一致                     | pass     | RUNBOOK §3 ↔ SPEC §4.2.3                                       |
| §6.3 pytest 回归                  | pass     | 见上表                                                            |
| W5 RUNBOOK §1.4 ChatBI visitor  | pass     | 运维签发 + verify 探活                                               |
| W5 diary README + NOTES         | pass     | `NOTES-w5-pending_20260602.md` · blocked 占位                    |
| §6.2 W5 sync                    | **pass** | `HG-W5-SYNC` approved · diary `sync-job-`*                     |
| §6.2 W5 五问                      | **pass** | diary `five-questions-results.md` 5/5 · `HG-W5-FIVE-Q` approved |
| §2.3 G-W5-2～5 执行                | **pass** | `q1–q5-sources-run*.json` · P1 见 `w5-retest-backlog.md`        |


#### 人工闸状态


| gate_id      | status      | 说明                                          |
| ------------ | ----------- | ------------------------------------------- |
| HG-W5-SYNC   | approved    | 2026-06-03 · job `c44158a5-…` · G-W5-1 pass |
| HG-W5-FIVE-Q | **approved** | 2026-06-03 · UI 5/5 · diary 留证 · 维护者签收 |
| HG-REINSPECT | **approved** | 2026-06-03 · 关账 CLOSE · 维护者预批签收      |


**W5 关账**：sync + 五问 UI 5/5 留证齐 · P1 均 defer/已结束（见 `w5-retest-backlog.md`）。

#### OpenSpec × TDD 三维（docs task）


| 维度           | 结果                                       |
| ------------ | ---------------------------------------- |
| Completeness | pass（W5 文档 tranche 齐；执行显式 defer）         |
| Correctness  | pass（鉴权分工 · Q3 strict · freeze_id 一致）    |
| Coherence    | pass（RUNBOOK ↔ task §2.3 ↔ diary README） |


#### 已知未测项

- 生产/预发 `admin/sync` 与五问预跑（**禁止 Agent 执行**）  
- 前端 W3 unlock · W4 content 就绪（跨仓 · defer 非 fail）

---

## 11. 修订记录


| 日期         | 摘要                                                                                                   |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| 2026-06-01 | 10 帽草案：自 SPEC §7 W2/W3/W5 拆 task；`PORTFOLIO-RAG-DEMO@2026-06-01`                                     |
| 2026-06-01 | 22 R1 零阻塞 · 30 W2/W3 落盘 · 40 文档 tranche 自检（W5 defer）                                                 |
| 2026-06-02 | 10 帽 W5 关账 Loop：§2.3 验收表 + 前端 W3 分工 · 帽链续跑 `task/portfolio-rag-w5-v1`                                |
| 2026-06-03 | §2.4 W6 增量（SPEC §4.5）：sources 路径 · 切片精度 · 意图 3 次重试（文档 · 待实现）                                         |
| 2026-06-03 | **CLOSE**：`HG-W5-FIVE-Q` · `HG-REINSPECT` approved · `git mv` → done · KPI 100%                          |


### P1 可选项（维护者 2026-06-03 · 不阻塞 HG-W5-FIVE-Q）


| ID   | 项                               | 决策                                         |
| ---- | ------------------------------- | ------------------------------------------ |
| P1-1 | R7 stream curl 交叉验证             | **已结束**                                    |
| P1-2 | `resume/cv-online.md` 真简历       | **defer**（此前亦无真稿 · 后续 sync）                |
| P1-3 | Supabase `diary/` chunk 噪音      | **保留**                                     |
| P1-4 | 跨仓 `evidence-card.md` + sync 脚本 | **前端 Agent** · `ai-ink-brain` W6 关账 Prompt |


留证：`docs/diary/samples/portfolio-rag-demo/w5-retest-backlog.md` · `five-questions-results.md`（Q5 行已对齐）

---

### KPI（00）

> **rubric**：`KPI_RUBRIC_v1_2` · **aggregator**：CLOSE · **关账** 2026-06-03


| hat_code | round | agent_mode    | D1   | D2   | D3   | D4   | D5   | 返工  | judgment_notes                    |
| -------- | ----- | ------------- | ---- | ---- | ---- | ---- | ---- | --- | --------------------------------- |
| 00       | close | main_chat     | pass | pass | pass | pass | pass | 0   | 关账编排 · 人闸全 approved             |
| 10       | W5    | main_chat     | pass | pass | pass | pass | pass | 0   | §2.3 细化 + 前端 W3 分工                |
| 22       | R1′   | main_chat     | pass | pass | pass | pass | pass | 0   | W5 增量零阻塞                          |
| 30       | W5    | main_chat     | pass | pass | pass | pass | pass | 0   | RUNBOOK §1.4 · diary · pytest 277 |
| 40       | W5    | main_chat     | pass | pass | pass | pass | pass | 0   | 五问 UI 5/5 留证                      |
| 22       | R2    | main_chat     | pass | pass | pass | pass | pass | 0   | 派 50                              |
| 50       | W5    | task_subagent | pass | pass | pass | pass | pass | 0   | pass-with-notes → 关账 pass          |
| CLOSE    | —     | main_chat     | pass | pass | pass | pass | pass | 0   | **Task_KPI% 100%** · git mv done  |


**Task_KPI%**：**100%**（pass · W5 文档 + sync + 五问留证关账）  
**blocked 说明**：无 · P1-2/P1-3 defer · P1-4 归前端 W6

---

## 给 Cursor

`portfolio-rag-demo`、`CONTENT_ROOT`、`admin/sync`、`五问验收`、`RUNBOOK_portfolio_rag_five_questions`、`freeze_id`、`failure_paths`、`HG-W5-SYNC`