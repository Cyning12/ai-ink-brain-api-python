# SPEC — 治理：Portfolio 演示站 RAG 语料同源 ingest 与五问验收（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `PORTFOLIO-RAG-DEMO@2026-06-01`（Prompt 00 轮 3 · 待确认清单清零 · 人可另议改日） |
| **Roadmap** | [`投递冲刺_20260609_v1_zh.md`](./投递冲刺_20260609_v1_zh.md) §2（五问真值 · **已对齐**） |
| **配对前端 SPEC** | `ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md`（并行起草 · **draft**） |
| **Harness 映射** | **10** 需求（本稿）→ 人审冻结 → **22** task 审核 → **30** RUNBOOK / env 文档 → 生产五问预跑 |
| **SDD 过程** | 轮 0 意图卡并入 §1；轮 1 覆盖 §0～§4；[`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) |
| **细化 Prompt 00** | [`PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md`](./PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md)（≤5 轮 · 阅读→提问→改 SPEC） |

---

## 0. 完成态（一句话）

在 **2026-06-09 投递前**，portfolio 演示站生产环境的 RAG 向量库与前端仓 **`ai-ink-brain/content/`** 保持 **同源 ingest**（`CONTENT_ROOT` → `POST /api/py/admin/sync`），并有一份 **人可执行、可复现** 的五问验收 RUNBOOK，使 Q1～Q5 **5/5 可答**、**sources ≥4/5**、单问重试 **≤3 次** 时仍可通过预检。

---

## 1. 背景与立项条件

### 1.1 轮 0 · 意图卡（并入）

| 项 | 结论 |
| --- | --- |
| **业务目标** | portfolio **演示站**（非完全公开博客）需在投递前展示 **RAG 问答能力**，语料与站点展示内容 **同源**，避免「页面有、向量库无」或 category 错位。 |
| **时间门槛** | **2026-06-09** 投递冲刺；本 Epic **6/9 前** 交付 ingest 对齐 + RUNBOOK + 生产五问预跑留证；**不** 将 ChatBI v3 preview 全链或双能力 handoff 纳入 6/9 硬门槛。 |
| **入库方式（已拍板）** | 现有 **`POST /api/py/admin/sync`** 异步 job 机制；**人**在生产/预发触发，本 SPEC 回合 **不执行** sync。 |
| **CONTENT_ROOT（已拍板）** | 指向前端仓 **`ai-ink-brain/content/`**（本地与 deploy 文档化；见 §4.4）。 |
| **visitor 策略（已拍板 · T-05）** | 演示站 visitor **不禁 text2sql**；库内为 **可公开** 样例数据。 |
| **release 节奏（已拍板）** | 卷四 / 卷五每次公众 release 后 **24h 内** → **再 sync 一轮**（运维 SOP，见 §4.3 · Q-8:A） |
| **sync 运维（已拍板 · Q-6:A · Q-7:A · Q-10:B）** | **单实例**接受：sync 时避免并发 redeploy；`404 Job not found` → 重新 `POST` 创建 job。**仅** `admin/sync` 入库路径；**不**在 RUNBOOK 中使用 `admin/ingest` 备用。轮询总超时 **≤60 min**。 |
| **依赖** | 前端 `content/methodology`、`content/resume`、`content/evidence` 目录与 metadata 约定（目标态；见 §4.1）；配对前端 SPEC；Supabase `documents` + SiliconFlow Embedding（维度与 `EMBEDDING_DIM` 一致）。 |
| **非范围（摘要）** | 改 Next 页面、新建向量 schema 大改、GraphRAG 试点、Wiki batch 重复 ingest、本 SPEC 内承诺 ChatBI v3 preview 全链。 |
| **部署边界（已拍板 · Prompt 00 轮 2 · Q-3）** | 演示 URL 沿用现有前端 Vercel 项目（当前 [`https://ai-ink-brain.vercel.app/`](https://ai-ink-brain.vercel.app/)）；`NEXT_PUBLIC_SITE_MODE=portfolio` **隐藏** Blog/Learning 等模块入口，**不删**路由代码。**不**变更后端 API 域名、Supabase 项目名或 Python 服务部署仓；本 Epic 允许 **新增** `documents` 入库相关 SQL/迁移（若尚未执行）。 |
| **五问执行环境（已拍板 · Q-3）** | **预发 / Preview 与生产等价**即可通过五问预检（同 `CONTENT_ROOT` 挂载语义、同 Supabase 项目、同 Embedding 维）；最终投递演示以 portfolio 模式下的 **同一 Vercel 项目 URL** 为准，**不**要求另起后端或 DB 域名。 |

### 1.2 立项条件

- [ ] 人审本 SPEC 并冻结 `freeze_id`
- [ ] 前端 portfolio content 三类目录（或等价路径）与 category 映射 **书面确认**
- [ ] 生产/预发 `CONTENT_ROOT` 与 `NEXT_PUBLIC_ADMIN_SECRET`（或 `CHAT_API_SECRET`）**部署文档**就绪（不含真实密钥）

---

## 2. 现状快照（基于代码扫描 · 2026-06-01）

> 扫描范围：`api/ingest_pipeline.py`、`api/index.py`（admin/sync）、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`、`.env.example`。

### 2.1 内容根与 category 规则

| 项 | 现状 |
| --- | --- |
| **CONTENT_ROOT** | `api/ingest_pipeline.py::get_all_markdown_chunks()` 读取 env `CONTENT_ROOT`；**留空**时回退 `REPO_ROOT/content`（后端仓内，会自动 `mkdir`）；**设置**则 `expanduser().resolve()` 后扫描；路径非目录时返回 **空 chunk 列表**（不抛错，`DEBUG_INGEST=1` 时打印跳过日志）。 |
| **扫描范围** | 递归遍历 `.md` / `.mdx`；跳过 `.` 前缀目录及 `node_modules`、`.next`。 |
| **metadata.category** | **相对路径第一段**：`parts = rel.split("/")` → `category = parts[0]`；缺省为 `uncategorized`。 |
| **其他 metadata** | `slug`（文件名去扩展名）、`relativePath`、`chunk_index`、`lastModified` / `mtime`；可选 `date_norm`（从 slug/filename 抽日期）。 |
| **增强文本** | `build_enhanced_chunk_text` 注入 `[Document Context]` + Title / Date / **Category** + Content，供 embedding 与检索展示。 |

### 2.2 入库路径对比

| 接口 | 行为 | 同步/异步 |
| --- | --- | --- |
| **`POST /api/py/admin/ingest?type=markdown`** | `process_markdown_files()`：按 **relativePath** 删旧行再批量 insert；返回 JSON 统计 | **同步**（请求内完成） |
| **`POST /api/py/admin/sync`** | 创建内存 job → 后台线程执行 `sync_content_to_vector()`：按 **slug** 删旧行再逐 chunk embed + insert | **异步**（`202` + job 轮询） |

`sync_content_to_vector()` 与 `process_markdown_files()` 均会调用 RPC `refresh_documents_fts_tokens_for_paths`（失败时 ingest 侧可跳过并仅在 `DEBUG_INGEST` 打印）。

### 2.3 admin/sync job 机制

| 字段 | 说明 |
| --- | --- |
| **创建** | `POST /api/py/admin/sync` → `create_sync_job()` → `BackgroundTasks` 调用 `run_sync_job_sync(job_id)` |
| **HTTP 202 体** | `{ ok, job, statusUrl: "/api/py/admin/sync?jobId=<uuid>" }` |
| **轮询** | `GET /api/py/admin/sync?jobId=<uuid>` → `{ ok, job }` |
| **job.status** | `queued` → `running` → `succeeded` \| `failed` |
| **job.result**（成功） | `filesScanned`, `chunksTotal`, `chunksUpserted`, `rowsDeleted` |
| **job.error**（失败） | 异常 `str(e)` 字符串（如 Embedding **维度不匹配**：`RuntimeError` 含「维度」文案） |
| **持久性** | **内存** `JOBS` 字典；**单实例**（**已拍板 · Q-6:A**）；serverless redeploy 后 job 丢失 → **重新 POST**；**不**做持久化 job 方案 |
| **鉴权** | `_require_auth`：`Authorization: Bearer <secret>` 或 `x-admin-token` / `x-blog-admin-token`；secret 来自 `NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET`（`api/rag_env.py::admin_secret()`） |

### 2.4 前端 content 目录（目标态 · 扫描 2026-06-01）

本机 `ai-ink-brain/content/` **尚未** 存在 `methodology/`、`resume/`、`evidence/` 顶层目录（仅有 `tasks/`、`harness/`、`diary/` 等）。portfolio 演示语料按 **目标态** 与前端 SPEC 对齐创建；ingest 侧 **无需改代码** 即可在目录就绪后通过 category 第一段映射入库。

### 2.5 Unified Chat 入口（只读 · 与验收相关）

- 演示站 RAG 问答预期走 **`POST /api/py/unified/chat`** 或 **`/stream`**（Bearer ChatBI token；visitor 不禁 text2sql）。
- Legacy `POST /api/py/chat` 仍存在；五问 RUNBOOK **默认**以 Unified 路径为准（具体 BFF 转发以前端 SPEC 为准）。

---

## 3. 范围 / 非范围

| 在范围（6/9 前） | 说明 |
| --- | --- |
| **CONTENT_ROOT 部署文档** | 本地 / 生产 / CI 如何指向前端 `content/` |
| **category 对齐** | `methodology` / `resume` / `evidence` 与 ingest `metadata.category` 一致 |
| **sync RUNBOOK** | 人触发 `POST /api/py/admin/sync`、轮询、失败语义、卷四/五 release 后再 sync |
| **五问验收 RUNBOOK** | Q1～Q5 提问句、期望 category、sources 检查、重试规则 |
| **生产预跑留证** | 录屏 / 日志 / diary 样本（路径由 RUNBOOK 指定，非本回合落盘） |
| **本 SPEC + 索引** | 治理级 SDD；冻结后驱动 task |

| 非范围 | 说明 |
| --- | --- |
| **前端 Next 页面 / UX** | 属 `ai-ink-brain` + 前端 SPEC |
| **新建或大幅变更 `documents` schema** | 沿用现有 `vector(N)` + metadata JSON |
| **GraphRAG 试点** | 不在本 Epic |
| **Wiki batch 重复 ingest** | 见 [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-v1.md)；portfolio 语料 **独立** content 树 |
| **ChatBI v3 preview 全链** | 低置信 RAG preview 等属其他 Epic；本 SPEC **不承诺** |
| **本回合执行生产 sync** | 仅规格与 RUNBOOK |
| **6/9 后 P1-B 双能力 handoff 实现** | 仅 §8 占位 |

---

## 4. 行为与操作需求

### 4.1 content 目录与 metadata.category 映射

| 前端目录（`content/` 下） | ingest `metadata.category` | 五问关联 | 内容类型（目标态） |
| --- | --- | --- | --- |
| **`methodology/`** | `methodology` | **Q1**（卷三 / Harness / 签收） | 方法论、Harness 工程、卷三相关文稿 |
| **`resume/`** | `resume` | **Q2**（RAG 混合检索）、**Q4**（11 年 AI Coding 成果） | 履历、项目段、个人成果叙事 |
| **`evidence/`** | `evidence` | **Q3**（冷温热 vs 架构三层 · sources **仅** `evidence`）、**Q5**（token/效果 + 边界） | 证据、实验、效果与边界说明 |

**规则（与现码一致）**：

1. 文件须为 `.md` 或 `.mdx`，且位于上述目录 **子树** 内；`relativePath` 形如 `methodology/xxx.md`。
2. **禁止**依赖后端仓内默认 `REPO_ROOT/content` 作为 portfolio 真值（生产必须显式 `CONTENT_ROOT`）。
3. 若文稿需跨 category 引用，仍以 **物理路径第一段** 为准；交叉引用通过文内链接，**不**伪造 category。
4. 前端若在 frontmatter 声明 category，须与目录第一段 **一致**（以前端 SPEC 为准；ingest **当前不读** frontmatter）。

### 4.2 sync 触发、job 轮询、失败语义

#### 4.2.1 触发（人执行）

```http
POST /api/py/admin/sync
Authorization: Bearer <ADMIN_SECRET>
```

期望：**HTTP 202**，记录 `job.id` 与 `statusUrl`。

#### 4.2.2 轮询

```http
GET /api/py/admin/sync?jobId=<uuid>
Authorization: Bearer <ADMIN_SECRET>
```

| job.status | 操作 |
| --- | --- |
| `queued` / `running` | 继续轮询（间隔 2～5s；总超时 **≤60 min** · **已拍板 · Q-10:B**） |
| `succeeded` | **硬检查**（**已拍板 · Q-4**）：`result.filesScanned > 0` **且** `chunksUpserted > 0`；`filesScanned=0` **视为 sync FAIL**，不得进入五问 |
| `failed` | 读 `error`；按下列语义处置 **不得** 标记五问通过 |

#### 4.2.3 失败语义（SPEC 级）

| 错误特征 | 含义 | 建议处置 |
| --- | --- | --- |
| `Embedding 维度为 … 与期望 … 不一致` | `EMBEDDING_DIM` / 模型与 Supabase `vector(N)` 不一致 | 修正 env 与 `init.sql` 一致后重跑；**勿**改库维度的临时 hack |
| `CONTENT_ROOT=… 不是目录` / `filesScanned=0` | 路径错误或目录空（**已拍板 · Q-4**：`filesScanned=0` **硬 FAIL**） | 修正 mount / 路径；确认 `methodology/`、`resume/`、`evidence/` **各 ≥1** `.md` 后再 sync |
| SiliconFlow / Supabase 网络或鉴权失败 | 上游或密钥问题 | 查 `SILICONFLOW_API_KEY`、Supabase service role；指数退避后重试 |
| `404 Job not found` | 进程重启或 redeploy（**已拍板 · Q-6:A**） | **重新 `POST`** 创建 job；sync 窗口内 **避免** 并发 redeploy |
| ingest 同步接口 `400` + 「维度」 | 同维度不匹配 | 与上表第一行相同 |

**与 `POST /api/py/admin/ingest` 差异**：ingest 为同步且按 path 删；sync 为异步且按 slug 删。portfolio **仅**用 **`admin/sync`**（**已拍板 · Q-7:A**）；RUNBOOK **不包含** ingest 备用路径。

### 4.3 卷四 / 卷五 release 后再 sync 的运维节奏

| 事件 | 动作 | 负责人 |
| --- | --- | --- |
| 卷四或卷五 **公众 release** 合并/发布 | 确认前端 `content/` 已更新对应文稿 | 内容 + 前端 |
| release 后 **24h 内**（**已拍板 · Q-8:A**） | 对 **同一 CONTENT_ROOT** 执行一轮 `POST /api/py/admin/sync` | 运维 / 后端负责人 |
| sync `succeeded` | 跑 **五问 smoke**（至少 Q1 + Q5） | 验收负责人 |
| sync `failed` | 阻塞标记 release RAG 就绪；不得对外宣称语料已更新 | — |

### 4.4 生产 / 本地 env 文档（须由 30 帽落盘 · 不含真实密钥）

| 变量 | 用途 | 本地示例 | 生产要求 |
| --- | --- | --- | --- |
| **`CONTENT_ROOT`** | Markdown 扫描根 | `/path/to/ai-ink-brain/content`（见 `.env.example`） | 部署 mount 或 CI checkout 路径 **必须**指向前端 content 真值 |
| **`NEXT_PUBLIC_ADMIN_SECRET`** 或 **`CHAT_API_SECRET`** | admin/sync 鉴权 | 本地 `.env` | 平台 Secrets；**禁止**进 Git |
| **`SILICONFLOW_API_KEY`** | Embedding | 本地 | 生产 Secrets |
| **`EMBEDDING_DIM`** / **`SILICONFLOW_EMBEDDING_DIMENSIONS`** | 与 `vector(N)` 一致 | `1024` | 与生产 Supabase 一致 |
| **`NEXT_PUBLIC_SUPABASE_URL`** + **`SUPABASE_SERVICE_ROLE_KEY`** | 写 `documents` | 本地 | 生产 |
| **`DEBUG_INGEST`** | 可选调试 | `1` 仅本地 | 生产 **关闭** |

**文档落点（30 帽）**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §C 增补 portfolio 段落，或独立 `docs/harness/guides/` 运维页（与 RUNBOOK 交叉链接）。

---

## 5. RUNBOOK 规格

本 SPEC **要求**另建可操作 RUNBOOK（30 帽正文），路径：

**`docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md`**

### 5.1 RUNBOOK 必含目录（大纲）

| # | 小节 | 必含内容 |
| --- | --- | --- |
| 1 | **前提与权限** | 生产 URL、Bearer token 获取方式（不写明文）、`CONTENT_ROOT` 确认命令 |
| 2 | **Sync 执行** | `POST /api/py/admin/sync` curl 模板、轮询、`succeeded` 字段检查 |
| 3 | **Sync 失败排障** | §4.2.3 对照表 + 维度 / 空目录 / job 404 |
| 4 | **五问验收表** | Q1～Q5 标准问句、期望 category、通过标准（5/5 可答、sources ≥4/5） |
| 5 | **单问重试规则** | 同一问最多 **3** 次；仍失败则记录 blocker |
| 6 | **Sources 留证** | Q1、Q5 **必须**保存 `x-sources` 或 SSE sources 片段（Unified 路径） |
| 7 | **卷四/五 release 后再 sync** | §4.3 检查清单 |
| 8 | **附录：环境变量表** | 链 PROJECT_CONFIG §C |

### 5.2 附录 A — RUNBOOK 大纲（本回合 · 非正文）

```text
§1 前提
  - 演示站 Unified Chat 入口（BFF：同 Vercel 项目 portfolio 模式，如 https://ai-ink-brain.vercel.app/unified-chat）
  - ChatBI visitor token（不禁 text2sql）；预发/Preview 与生产等价（§6.1）
§2 Sync
  - curl POST/GET admin/sync；轮询间隔 2～5s；总超时 ≤60min
  - 仅 sync（不含 admin/ingest 备用）
§3 失败排障
  - 维度 / CONTENT_ROOT / job 404（404 → 重新 POST；避免 redeploy 窗口）
§4 五问表（见 §6）
§5 重试 ≤3
§6 Sources 留证（Q1/Q5 强制）
§7 Release 后再 sync
§8 Env 指针
```

---

## 6. 验收标准（SPEC 级）

### 6.1 Sync job

- [ ] 人对 **预发 / Preview 或生产等价环境**（**已拍板 · Q-3**）执行 `POST /api/py/admin/sync`，job 终态 **`succeeded`**
- [ ] **硬门槛**（**已拍板 · Q-4**）：`result.filesScanned > 0`；`filesScanned=0` **记 FAIL**
- [ ] `result.filesScanned` 覆盖 `methodology/`、`resume/`、`evidence/` **各 ≥1** 个 `.md`（目标态参考 [`投递冲刺_20260609_v1_zh.md`](./投递冲刺_20260609_v1_zh.md) §3.2：`methodology/vol3_*`、`resume/cv-online.md`、`evidence/methodology-card.md`）
- [ ] `result.chunksUpserted > 0`

### 6.2 五问 RAG 验收

**通过口径（已拍板）**：

| 指标 | 阈值 |
| --- | --- |
| 可答率 | **5/5** 问均得到 **非空、切题** 回答 |
| Sources | **≥4/5** 问有可追溯 sources（Unified JSON `sources` / header `x-sources` / SSE 等价字段） |
| 单问重试 | 同一问 **≤3** 次仍不达标则记 FAIL，不得刷通过率 |

**五问真值表**（问句与 [`投递冲刺_20260609_v1_zh.md`](./投递冲刺_20260609_v1_zh.md) §2 **逐字对齐** · Prompt 00 轮 2 · Q-1:A）：

| # | 标准问句（chip / RUNBOOK 可粘贴） | 期望命中 `content/` 路径 | sources 主 `metadata.category`（硬约束） | 合格回答要点 |
| --- | --- | --- | --- | --- |
| **Q1** | 《AI 编程可闭环协作》**卷三**讲什么？Harness 和签收是什么？ | `methodology/vol3_*` | **`methodology`** | 任务单 + 书面签收 + 合并前 CI；sources 含 vol3 |
| **Q2** | **RAG 混合检索**怎么做的？ | `resume/*` 或项目段 | **`resume`** | 向量 + 混合检索 + rerank 至少两项 |
| **Q3** | **冷/温/热** 和 **架构三层** 区别？ | `evidence/*` | **`evidence` only**（**已拍板 · Q-2:A**；`methodology` 下 vol3 **不计** Q3 通过） | 记忆分层 ≠ 架构分层 |
| **Q4** | **11 年经历**里 AI Coding 相关成果？ | `resume/*` | **`resume`** | 百果园 Cursor + Ink + 连载；不虚构 |
| **Q5** | 按需读图相对整图灌入 **token/效果**？**边界**？ | `evidence/*` | **`evidence`** | 约 1/9 或「约十分之一」+ **小样本、非全行业** |

**强制留证**（**已拍板 · Q-9:A**）：

- [ ] **Q1**、**Q5** 的 sources JSON **可复现**：同 token、同问句预跑 **2 次**，sources 主 `metadata.category` **须一致**（不一致记 FAIL）

### 6.3 文档

- [ ] RUNBOOK 正文落盘（§5 路径）且与 §4、§6 一致
- [ ] `CONTENT_ROOT` 生产配置有 **非密钥** 留证（deploy 文档或 diary 样本）

---

## 7. 工作包拆分（→ 未来 task 建议 · 本回合不创建 task）

| ID | 工作包 | 交付物 | 建议 Harness |
| --- | --- | --- | --- |
| **W1** | SPEC 人审与 `freeze_id` | 本文件状态 → `active`/`done` | 人 |
| **W2** | RUNBOOK 正文 | `RUNBOOK_portfolio_rag_five_questions_v1_zh.md` | 30 |
| **W3** | env / deploy 文档 | PROJECT_CONFIG 或 guides 增补 `CONTENT_ROOT` 生产路径 | 30 |
| **W4** | 前端 content 三类目录 | 前端仓 `methodology|resume|evidence` + 前端 SPEC | 前端 30 |
| **W5** | 生产 sync + 五问预跑 | diary 留证、录屏 | 人 + 40 自检 |
| **W6** | task 创建 | `task_portfolio_rag_demo_v1` | 22 后 |

**建议 task 字段草案**（冻结后填写）：

- `test_strategy`: `recommended`（五问以人工 RUNBOOK 为主；可选 smoke pytest 由 task 择要）
- `failure_paths`: sync 维度失败、空 CONTENT_ROOT、job 404、五问 sources 不足
- Open Folder: `ai-ink-brain-api-python`（W2/W3）；联调时开双仓

---

## 8. 后续 Epic（6/10+ · 非 6/9 门槛）— P1-B 双能力 handoff

> **意图占位 only**；本 SPEC **不**写实现、不纳入 6/9 验收。

| 项 | 占位说明 |
| --- | --- |
| **目标** | Unified Chat SSE 上 **双能力 handoff** 最小闭环：例如 RAG 低置信 → 澄清 / Text2SQL handoff，事件类型 **`agent.handoff`**（名称 **待确认**，以 `_contract_manifest.json` 冻结为准） |
| **接口面** | `POST /api/py/unified/chat/stream` · Bearer ChatBI principal · 事件链见 `api/unified_chat.py`、`api/agent.py` |
| **与 portfolio 关系** | 演示站 visitor 已不禁 text2sql；handoff 为 **体验增强**，**不**替代本 Epic 的 ingest + 五问 |
| **依赖 SPEC** | ChatBI v3 系列 L1（如 LowConfidence / Events）；**禁止**在本治理 SPEC 内展开实现细节 |

---

## 9. 关联引用

| 用途 | 路径 |
| --- | --- |
| 项目真值表 | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| ingest 实现 | [`api/ingest_pipeline.py`](../../../api/ingest_pipeline.py) |
| admin/sync 路由 | [`api/index.py`](../../../api/index.py)（`py_admin_sync_post` / `py_admin_sync_get`） |
| 投递计划（五问 §2） | [`投递冲刺_20260609_v1_zh.md`](./投递冲刺_20260609_v1_zh.md) |
| 配对前端 SPEC | `ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md` |
| SDD 起草 | [`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) |
| Wiki ingest（勿重复） | [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-v1.md) |
| 冷温热术语 | [`docs/harness/guides/GUIDE_冷温热层_对内术语_v1_zh.md`](../../harness/guides/GUIDE_冷温热层_对内术语_v1_zh.md) |
| Unified 契约 | [`docs/_tech_graph/_contract_manifest.json`](../../_tech_graph/_contract_manifest.json) |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-01 | v1 **draft**：Harness 10 帽轮 1；§0～§9 + RUNBOOK 大纲；候选 `PORTFOLIO-RAG-DEMO@2026-06-0?` |
| 2026-06-01 | Prompt 00 **轮 2**：消化 Q-1～Q-5（五问 §2 写入 §6.2；Q3 strict evidence；预发等价；sync 空库 FAIL；freeze_id 冻结当日策略） |
| 2026-06-01 | Prompt 00 **轮 3**：消化 Q-6～Q-10；待确认清单清零 → **`active`** · `PORTFOLIO-RAG-DEMO@2026-06-01` |

---

## SPEC 待确认清单

| # | 决策点 | 状态 |
| --- | --- | --- |
| 1～10 | Prompt 00 轮 1～3 全部决策点 | **resolved**（见 §1.1、§4.2、§4.3、§6.2 已拍板条文） |

> **冻结说明**：本 Epic 6/9 范围内 **无 pending**；§8 P1-B handoff 事件名仍随 ChatBI 契约演进，**不阻塞**本 SPEC 冻结。

---

## 给 Cursor

`portfolio`、`CONTENT_ROOT`、`admin/sync`、`五问验收`、`methodology`、`resume`、`evidence`、`PORTFOLIO-RAG-DEMO`、`RUNBOOK_portfolio_rag_five_questions`
