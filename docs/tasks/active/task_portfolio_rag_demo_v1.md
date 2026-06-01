# Task：Portfolio 演示站 RAG — RUNBOOK · env 文档 · 五问预跑留证（后端）

> **状态**：`in_progress`（30 W2/W3 done · W5 待人 · 40 文档 tranche 自检完成）  
> **schedule_ref**：投递冲刺 [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) · P0-C  
> **硬 deadline**：**2026-06-09 上午**（投递前 ingest 对齐 + 五问 RUNBOOK + 预发/生产等价环境 sync 与五问预跑留证）  
> **治理 SPEC（L1 · 已冻结）**：[`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) · `PORTFOLIO-RAG-DEMO@2026-06-01`  
> **配对前端 SPEC（只读）**：`ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md`  
> **关联图谱**：[`docs/_tech_graph/10_flow_ingest.ai.md`](../_tech_graph/10_flow_ingest.ai.md)（ingest/sync 只读对照）

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **task_slug** | `portfolio-rag-demo` |
| **test_strategy** | `recommended` |
| **test_strategy_note** | 验收以 **人工 RUNBOOK**（sync 轮询 + 五问预跑 + sources 留证）为主；可选补 smoke pytest（如 ingest env 解析）由 30 择要，**非** red-green 硬门槛 |
| **freeze_id** | `PORTFOLIO-RAG-DEMO@2026-06-01` |
| **gates_before_code** | `failure_paths`、必读列表、验收命令、W4 前端 content 就绪确认 |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **experience_capture** | `recommended` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **git_branch** | `task/portfolio-rag-demo-v1` |
| **Open Folder** | `ai-ink-brain-api-python`（W2/W3 落盘）；W5 预跑须开双仓读前端 content / Unified Chat |
| **推荐路径** | **A（22 R1）** — 与前端 portfolio task 审查节奏对齐 |

### 工作包映射（SPEC §7 → 本 task）

| SPEC ID | 工作包 | 本 task 范围 | 执行帽 |
|---------|--------|--------------|--------|
| W2 | RUNBOOK 正文 | **在范围** | 30 |
| W3 | env / deploy 文档 | **在范围** | 30 |
| W5 | 生产 sync + 五问预跑留证 | **在范围**（人触发 sync；40 回填留证） | 人 + 40 |
| W4 | 前端 content 三类目录 | **依赖 · 非本仓 commit** | 前端 30 |
| W1 | SPEC 冻结 | **已完成** | — |

### 跨仓依赖

| 项 | 说明 |
|----|------|
| **blocked_by** | 前端 W4：`ai-ink-brain/content/{methodology,resume,evidence}/` 目标态文稿就绪（见 [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) §3.2） |
| **blocks** | 投递 P0-C / P0-D 录屏；前端 portfolio 演示站五问 chip 联调 |
| **配对 task** | `ai-ink-brain` · `task_portfolio_demo_site_v1`（并行 Harness · 22 R1 节奏对齐） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | semi_auto 链式执行人授权 · 2026-06-01 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 零阻塞 · `reviews/.../audit_R1_20260601.md` |
| HG-W5-SYNC | pending | — | **人**在预发/生产等价环境 sync `succeeded` 后改 approved |
| HG-W5-FIVE-Q | pending | done | 五问预跑 + diary 留证人签 |
| HG-REINSPECT | approved | done | 50 复检后人签、合并 PR 前 |

---

## 1. 背景与目标

Portfolio 演示站需在 **2026-06-09 投递前** 展示与前端 `content/` **同源** 的 RAG 问答能力：语料经 **`POST /api/py/admin/sync`** 入库（`CONTENT_ROOT` → 前端仓 `ai-ink-brain/content/`），并通过 **可复现的五问 RUNBOOK** 验收 Q1～Q5。

**本 task 完成态（后端仓）**：

1. **W2**：可操作 RUNBOOK 落盘 [`docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md)，与 SPEC §4～§6 一致。  
2. **W3**：`CONTENT_ROOT` 及 admin/sync 相关 env 的 **生产/本地部署说明** 落盘（`PROJECT_CONFIG` §C 增补 portfolio 段落，与 RUNBOOK §8 交叉链接）。  
3. **W5**：在 **预发 / Preview 与生产等价环境**（同 Supabase、同 Embedding 维、同 `CONTENT_ROOT` 挂载语义）由 **人** 执行 sync + 五问预跑，留证于 `docs/diary/samples/portfolio-rag-demo/`（路径由 RUNBOOK 指定）；40 帽回填 task **`### 自检结论（执行者）`**。

**现网 ingest 行为无需改码**（SPEC §2 扫描结论）：category = 相对路径第一段；portfolio 仅 **`admin/sync`** 路径。

---

## 2. 范围

### 2.1 W2 · RUNBOOK（30 帽交付）

- [x] **G-W2-1** 新建 RUNBOOK，必含 SPEC §5.1 八节：前提与权限 / Sync 执行 / 失败排障 / 五问验收表 / 单问重试 ≤3 / Sources 留证（Q1、Q5 强制）/ 卷四·五 release 后再 sync / Env 指针  
- [x] **G-W2-2** 五问问句与 [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) §2 **逐字对齐**（SPEC §6.2 真值表）  
- [x] **G-W2-3** Q3 sources 硬约束：**仅** `metadata.category == evidence`（不含 methodology vol3）  
- [x] **G-W2-4** Sync 硬检查：`succeeded` 且 `filesScanned > 0` 且 `chunksUpserted > 0`；三目录各 ≥1 `.md`  
- [x] **G-W2-5** 仅 `admin/sync`；**不含** `admin/ingest` 备用路径  
- [x] **G-W2-6** 轮询间隔 2～5s，总超时 ≤60 min；`404 Job not found` → 重新 POST  

### 2.2 W3 · env / deploy 文档（30 帽交付）

- [x] **G-W3-1** 在 [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) **§C** 增补 **portfolio 演示站** 段落：`CONTENT_ROOT`、`NEXT_PUBLIC_ADMIN_SECRET`/`CHAT_API_SECRET`、`EMBEDDING_DIM`、`SILICONFLOW_*`、Supabase 写库变量（**不含真实密钥**）  
- [x] **G-W3-2** 说明本地 `CONTENT_ROOT` 指向前端仓 `content/` 的示例；生产 mount / CI checkout 语义与 Vercel 部署边界（SPEC §1.1 Q-3）  
- [x] **G-W3-3** 明确 **禁止** 生产依赖后端仓默认 `REPO_ROOT/content` 回退作为 portfolio 真值  
- [x] **G-W3-4** RUNBOOK §8 与 PROJECT_CONFIG 双向链接  

### 2.3 W5 · 预跑留证（人 + 40 帽 · 本 task 验收项）

> **Agent 禁止** 在本 task 内对生产/预发执行 `POST /api/py/admin/sync`；仅 RUNBOOK 与留证目录规范。

- [ ] **G-W5-1** 前置：HG-W5-SYNC 人签 — 预发/生产等价环境 sync job **`succeeded`**，且 `filesScanned` 覆盖 `methodology/`、`resume/`、`evidence/` **各 ≥1**  
- [ ] **G-W5-2** 五问预跑：**5/5** 非空切题；sources **≥4/5**；单问重试 **≤3** 次  
- [ ] **G-W5-3** Q1、Q5 sources JSON **可复现**：同 token、同问句预跑 **2 次**，主 `metadata.category` **一致**  
- [ ] **G-W5-4** 留证落盘 `docs/diary/samples/portfolio-rag-demo/`：sync job 终态 JSON 摘要、Q1/Q5 sources 片段、五问结果表（pass/fail + 重试次数）；可选录屏路径索引链 [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) P0-D  
- [ ] **G-W5-5** Unified Chat 路径（`/api/py/unified/chat` 或 `/stream` + visitor token）；visitor **不禁 text2sql**（T-05）  

---

## 3. 非范围

- 改 `api/`、`tests/` **业务实现**（ingest 现码已满足 SPEC §2）  
- 前端 Next 页面 / portfolio UX / 访客秘钥实现（前端 SPEC + task）  
- 本 task 回合 **执行** 生产或预发 `admin/sync`（仅 RUNBOOK 与留证规范）  
- 新建或大幅变更 `documents` schema、GraphRAG、Wiki batch ingest  
- ChatBI v3 preview 全链、§8 P1-B 双能力 handoff（6/9 后 Epic）  
- 卷四/卷五 **内容创作** 与公众 release（属 docs / 公众仓；release 后再 sync 见 RUNBOOK §7）  

---

## 行为变更（Delta）

**无** — 本 task 为 **文档 + 运维 RUNBOOK + 人工验收留证**；不修改对外 API 契约。关账时可把 RUNBOOK 路径写入 SPEC §9 关联表（可选 patch，非本 task 硬门槛）。

---

## 5. 依赖与引用

| 依赖项 | 路径 / 说明 |
|--------|-------------|
| 治理 SPEC | [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) |
| 投递计划 | [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) §2 五问 · §3.2 content 树 |
| PROJECT_CONFIG | [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| ingest 实现（只读） | `api/ingest_pipeline.py`、`api/index.py`（admin/sync） |
| 冷温热术语 | [`GUIDE_冷温热层_对内术语_v1_zh.md`](../harness/guides/GUIDE_冷温热层_对内术语_v1_zh.md) |
| Unified 契约 | [`docs/_tech_graph/_contract_manifest.json`](../_tech_graph/_contract_manifest.json) |
| `.env.example` | 仓库根 · `CONTENT_ROOT` 注释 |

---

## 验收标准

### 6.1 文档（30 完成后）

- [x] RUNBOOK 路径存在且 §5.1 八节齐全  
- [x] PROJECT_CONFIG §C portfolio 段落存在且无真实密钥  
- [x] RUNBOOK 与 SPEC §4.2.3 失败语义表 **一致**  

### 6.2 预跑（W5 · 40 + 人签）

- [ ] sync job 终态 `succeeded` + 硬检查通过（§2.3 G-W5-1）  
- [ ] 五问指标达标（§2.3 G-W5-2～G-W5-3）  
- [ ] `docs/diary/samples/portfolio-rag-demo/` 留证可读（§2.3 G-W5-4）  
- [ ] HG-W5-SYNC、HG-W5-FIVE-Q → `approved`  

### 6.3 CI

- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（本 task **不应** 引入 api 变更；若仅 docs 则作回归确认）  

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 / RUNBOOK 处置 |
|---|-------------|----------|----------|--------|-------------------------|
| F1 | `fp-portfolio-embed-dim` | Embedding 维度与 `vector(N)` 不一致 | sync job `failed`；`error` 含「维度」 | 修正 env 后 **重跑 sync** | RUNBOOK §3 对照表第一行 |
| F2 | `fp-portfolio-files-scanned-zero` | `CONTENT_ROOT` 非目录或空树；`filesScanned=0` | job 可能 `succeeded` 但 **硬 FAIL**（Q-4） | 修正 mount / 补 content 后重跑 | **不得**进入五问 |
| F3 | `fp-portfolio-job-404` | `404 Job not found`（redeploy） | GET 轮询 404 | **重新 POST** 创建 job | sync 窗口避免并发 redeploy |
| F4 | `fp-portfolio-upstream-auth` | SiliconFlow / Supabase 鉴权或网络失败 | job `failed` 或超时 | 指数退避；查 Secrets | RUNBOOK §3 |
| F5 | `fp-portfolio-five-q-retry` | 五问单问 3 次仍不达标 | 记该问 **FAIL** | 可调 query/chip 或补 content 后再 sync | 不得刷通过率；阻塞 6/9 全绿 |
| F6 | `fp-portfolio-sources-drift` | Q1/Q5 两次预跑 sources category 不一致 | 记 **FAIL**（Q-9:A） | 查 ingest category / 文稿路径 | diary 留证须标注 blocker |
| F7 | `fp-portfolio-q3-evidence` | Q3 sources 命中 `methodology` | Q3 **FAIL**（strict evidence） | 调整 evidence 文稿或检索参数 | RUNBOOK 五问表须写明 |
| F8 | `fp-portfolio-w4-blocked` | 前端 W4 未就绪即 sync | `filesScanned` 不足三目录 | 等待前端 content 后再 sync | task `blocked_by` |

---

## 8. 给执行帽的必读列表（30 · 按序）

1. 本 task 全文 + **`failure_paths`** + **`human_gate`**  
2. [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) §4～§6  
3. [`投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) §2 五问表  
4. [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) §C（改前读现表）  
5. `api/ingest_pipeline.py` · `get_all_markdown_chunks()`（只读 · category 规则）  
6. `api/index.py` · admin/sync 路由（只读 · job 字段）  
7. 22 R1 审查 [`docs/harness/reviews/task_portfolio_rag_demo_v1_audit_R1_*.md`](../harness/reviews/)（**30 开工前须存在且零阻塞**）  

**验证命令（合并前）**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 9. 文档矛盾（须以 freeze_id 为准）

| 矛盾 | 出处 A | 出处 B | task 口径 |
|------|--------|--------|-----------|
| Q3 期望路径 | 投递冲刺 §2：「`evidence/*` **或 vol3**」 | SPEC §6.2（Q-2:A）：sources **仅** `evidence` | **以 SPEC / freeze_id 为准**；RUNBOOK 写 strict evidence |

---

### 6.3 CI

- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿（本 task **不应** 引入 api 变更；若仅 docs 则作回归确认）  

---

## 10. 实现备忘（30 回填）

| 文件 | 动作 | 状态 |
|------|------|------|
| `docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md` | **新建** | done · 30 |
| `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | §C.1 增补 portfolio | done · 30 |
| `docs/diary/samples/portfolio-rag-demo/README.md` | W5 留证索引 | done · 30（正文待人） |
| `api/`、`tests/` | **不改** | — |

---

### 自检结论（执行者）

> **40 帽 · 2026-06-01 · 分支 `task/portfolio-rag-demo-v1`**

#### 命令与退出码

| 命令 | cwd | 退出码 | 摘要 |
|------|-----|--------|------|
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 仓库根 | **0** | **277 passed**, 1 skipped, 2 deselected |

#### 验收表（文档 tranche）

| 验收项 | 结果 | 证据 |
|--------|------|------|
| §6.1 RUNBOOK 八节 | pass | `docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md` |
| §6.1 PROJECT_CONFIG §C.1 | pass | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` |
| §6.1 失败语义一致 | pass | RUNBOOK §3 ↔ SPEC §4.2.3 |
| §6.3 pytest 回归 | pass | 见上表 |
| §6.2 W5 sync + 五问 | **未测** | `HG-W5-SYNC` / `HG-W5-FIVE-Q` pending；待人按 RUNBOOK 执行 |
| §2.3 G-W5-1～5 | **未测** | 留证目录仅 README 索引 |

#### OpenSpec × TDD 三维（docs task）

| 维度 | 结果 |
|------|------|
| Completeness | pass（W2/W3 交付物齐；W5 显式 defer） |
| Correctness | pass（五问/Q3 strict 与 freeze_id 一致） |
| Coherence | pass（RUNBOOK ↔ PROJECT_CONFIG ↔ SPEC） |

#### 已知未测项

- 生产/预发 `admin/sync` 与五问预跑（**禁止 Agent 执行**）  
- 前端 W4 content 三类目录就绪性（跨仓 · 人确认）

---

## 11. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-01 | 10 帽草案：自 SPEC §7 W2/W3/W5 拆 task；`PORTFOLIO-RAG-DEMO@2026-06-01` |
| 2026-06-01 | 22 R1 零阻塞 · 30 W2/W3 落盘 · 40 文档 tranche 自检（W5 defer） |

---

## 给 Cursor

`portfolio-rag-demo`、`CONTENT_ROOT`、`admin/sync`、`五问验收`、`RUNBOOK_portfolio_rag_five_questions`、`freeze_id`、`failure_paths`、`HG-W5-SYNC`
