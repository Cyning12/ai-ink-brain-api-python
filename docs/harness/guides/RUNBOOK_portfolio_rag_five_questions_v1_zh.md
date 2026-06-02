# RUNBOOK — Portfolio 演示站 RAG 同源 sync 与五问验收（v1）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `PORTFOLIO-RAG-DEMO@2026-06-01` |
| **关联 SPEC** | [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md) |
| **投递计划** | [`投递冲刺_20260609_v1_zh.md`](../../spec/governance/投递冲刺_20260609_v1_zh.md) §2 |
| **env 真值** | [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) §C.1 |
| **留证目录** | [`docs/diary/samples/portfolio-rag-demo/`](../../diary/samples/portfolio-rag-demo/) |
| **入库路径** | **仅** `POST /api/py/admin/sync`（**禁止**本 RUNBOOK 使用 `admin/ingest` 备用） |

---

## §1 前提与权限

### 1.1 执行环境

| 项 | 要求 |
| --- | --- |
| **五问预跑环境** | **预发 / Preview 与生产等价**：同 Supabase 项目、同 `EMBEDDING_DIM`、同 `CONTENT_ROOT` 挂载语义（SPEC Q-3） |
| **演示 URL** | portfolio 模式同一 Vercel 项目（如 `https://ai-ink-brain.vercel.app/unified-chat`）；BFF 转发至 Python API |
| **RAG 入口** | **`POST /api/py/unified/chat`** 或 **`/stream`**；Bearer **visitor** ChatBI token（**不禁 text2sql** · T-05） |
| **CONTENT_ROOT** | **必须**显式指向前端仓 `ai-ink-brain/content/`；**禁止**生产依赖后端仓 `REPO_ROOT/content` 回退 |

### 1.2 前置检查（sync 前）

```bash
# 1) 确认 CONTENT_ROOT 为目录且含三类文稿（目标态）
test -d "$CONTENT_ROOT/methodology" && test -d "$CONTENT_ROOT/resume" && test -d "$CONTENT_ROOT/evidence"
find "$CONTENT_ROOT/methodology" "$CONTENT_ROOT/resume" "$CONTENT_ROOT/evidence" -name '*.md' | head

# 2) 确认 Python 服务可读 env（本地示例）
# CONTENT_ROOT=/path/to/ai-ink-brain/content
```

### 1.3 鉴权（不写明文密钥）

| 用途 | Header | Secret 来源 |
| --- | --- | --- |
| **admin/sync** | `Authorization: Bearer <ADMIN_TOKEN>`（推荐） | 前端 **`SYNC_ADMIN_SECRET`** 或 Python `CHAT_API_SECRET` / 服务端 admin 同值；**禁止** Portfolio 文档写 `NEXT_PUBLIC_ADMIN_SECRET` |
| **admin/sync（BFF 本地）** | `Authorization: Bearer $SYNC_ADMIN_SECRET` | 本仓 `.env.local` · **服务端 only** |
| **Unified Chat 五问** | `Authorization: Bearer <VISITOR_CHATBI_TOKEN>` | Supabase `chatbi_access_tokens`（`api/chatbi_principal.py`）；**非** admin/sync secret |
| **admin/sync（BFF 本地）** | `Authorization: Bearer $SYNC_ADMIN_SECRET` | 本仓 `.env.local` · **服务端 only** |

### 1.4 运维签发 ChatBI visitor token（五问 curl · W5）

> **与前端 W3 分工**：招聘访客 **默认 UX** 为前端 `POST /api/auth/unlock` + `PORTFOLIO_VISITOR_*`（见配对前端 SPEC §4.3）；**本 RUNBOOK 五问 curl** 直连 Python API 时使用 **ChatBI DB token**。

| 步骤 | 动作 |
| --- | --- |
| 1 | 本机（仓库根）：`python3 docs/diary/local_chatbi_access_token_gen.py --level 2 --subject-user-id <user_id> --label portfolio-five-q --expires-in-days 7` |
| 2 | 将脚本 stdout 的 **INSERT SQL** 在 Supabase SQL Editor 执行（**勿**将明文 token 提交 Git） |
| 3 | 探活：`curl -sS "$PY_API_URL/api/py/chatbi/access/verify" -H "Authorization: Bearer $VISITOR_TOKEN"` → `ok: true` |
| 4 | 五问：`Authorization: Bearer $VISITOR_TOKEN` 调用 §4 Unified Chat（**不禁 text2sql** · level 2 `end_user`） |

**禁止**：用 `SYNC_ADMIN_SECRET` / `CHAT_API_SECRET` 冒充五问 visitor Bearer；admin token 仅 §2 sync。

---

## §2 Sync 执行

### 2.1 创建 job

```bash
export PY_API_URL="https://<python-api-host>"   # 或本地 http://127.0.0.1:8000
export ADMIN_TOKEN="<从 Secrets 读取，勿写入 Git>"

curl -sS -X POST "$PY_API_URL/api/py/admin/sync" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

**期望**：HTTP **202**，响应含 `job.id` 与 `statusUrl`（形如 `/api/py/admin/sync?jobId=<uuid>`）。

### 2.2 轮询

```bash
export JOB_ID="<上一步 job.id>"

while true; do
  curl -sS "$PY_API_URL/api/py/admin/sync?jobId=$JOB_ID" \
    -H "Authorization: Bearer $ADMIN_TOKEN" | tee /tmp/sync-job.json
  STATUS=$(python3 -c "import json,sys; print(json.load(open('/tmp/sync-job.json'))['job']['status'])")
  echo "status=$STATUS"
  case "$STATUS" in
    succeeded|failed) break ;;
    *) sleep 3 ;;
  esac
done
```

| 参数 | 值 |
| --- | --- |
| 轮询间隔 | **2～5s** |
| 总超时 | **≤60 min** |

### 2.3 成功硬检查（全部满足才进入 §4 五问）

| 检查项 | 阈值 |
| --- | --- |
| `job.status` | **`succeeded`** |
| `result.filesScanned` | **`> 0`**（`=0` 记 **FAIL** · Q-4） |
| `result.chunksUpserted` | **`> 0`** |
| 目录覆盖 | `methodology/`、`resume/`、`evidence/` **各 ≥1** 个 `.md` 被扫描 |

**留证**：将终态 JSON 摘要保存至 `docs/diary/samples/portfolio-rag-demo/sync-job-final.json`（可删敏感字段）。

---

## §3 Sync 失败排障

| 错误特征 | 含义 | 处置 | 可重试 |
| --- | --- | --- | --- |
| `Embedding 维度为 … 与期望 … 不一致` | `EMBEDDING_DIM` 与 `vector(N)` 不一致 | 对齐 env 与 `supabase/sql/init.sql`；**勿**临时改库维度 | 修正后重跑 sync |
| `CONTENT_ROOT=… 不是目录` / `filesScanned=0` | 路径错或目录空 | 修正 mount；补三类 content 后再 sync | 是 |
| SiliconFlow / Supabase 失败 | 上游或密钥 | 查 `SILICONFLOW_API_KEY`、Supabase service role | 指数退避 |
| **`404 Job not found`** | redeploy / 单实例 job 丢失 | **重新 `POST`** 创建 job；sync 窗口 **避免** 并发 redeploy | 是 |
| ingest `400` + 「维度」 | 同维度不匹配 | 同上 Embedding 行 | 修正后重跑 |

---

## §4 五问验收表

**通过口径**：**5/5** 非空切题；sources **≥4/5**；单问 **≤3** 次重试仍不达标则记 **FAIL**。

| # | 标准问句（chip 可粘贴） | 期望 `content/` 路径 | sources 主 `metadata.category` | 合格要点 |
| --- | --- | --- | --- | --- |
| **Q1** | 《AI 编程可闭环协作》**卷三**讲什么？Harness 和签收是什么？ | `methodology/vol3_*` | **`methodology`** | 任务单 + 书面签收 + 合并前 CI；sources 含 vol3 |
| **Q2** | **RAG 混合检索**怎么做的？ | `resume/*` | **`resume`** | 向量 + 混合检索 + rerank 至少两项 |
| **Q3** | **冷/温/热** 和 **架构三层** 区别？ | `evidence/*` | **`evidence` only** | 记忆分层 ≠ 架构分层；**methodology vol3 不计 Q3 通过** |
| **Q4** | **11 年经历**里 AI Coding 相关成果？ | `resume/*` | **`resume`** | 百果园 Cursor + Ink + 连载；不虚构 |
| **Q5** | 按需读图相对整图灌入 **token/效果**？**边界**？ | `evidence/*` | **`evidence`** | 约 1/9 或「约十分之一」+ **小样本、非全行业** |

**Unified 调用示例（JSON）**：

```bash
curl -sS -X POST "$PY_API_URL/api/py/unified/chat" \
  -H "Authorization: Bearer $VISITOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"<上表问句>","session_id":"portfolio-five-q-smoke"}' \
  -D /tmp/unified-headers.txt | tee /tmp/unified-response.json
# sources：响应 JSON events 内 rag.sources，或响应头 x-sources（若 BFF 透传）
```

术语纠偏见 [`GUIDE_冷温热层_对内术语_v1_zh.md`](./GUIDE_冷温热层_对内术语_v1_zh.md)。

---

## §5 单问重试规则

1. 同一问 **最多 3 次**（可调 chip 文案或 session，**不得**刷通过率）。  
2. 第 3 次仍不达标 → 该问记 **FAIL**，写入留证表 blocker 列。  
3. 若多问 FAIL → 阻塞 6/9 全绿；须补 content 或修正 ingest 后 **重新 sync** 再跑。

---

## §6 Sources 留证

| 项 | 要求 |
| --- | --- |
| **强制** | **Q1**、**Q5** 保存 sources JSON（或 SSE `rag.sources` 片段） |
| **可复现** | 同 visitor token、**同问句** 预跑 **2 次**；主 `metadata.category` **须一致**（不一致记 FAIL · Q-9:A） |
| **落盘** | `docs/diary/samples/portfolio-rag-demo/q1-sources-run{1,2}.json`、`q5-sources-run{1,2}.json` |
| **五问汇总** | `five-questions-results.md`：问句 / pass-fail / 重试次数 / sources category 摘要 |

---

## §7 卷四 / 卷五 release 后再 sync

| 步骤 | 动作 |
| --- | --- |
| 1 | 公众仓卷四/卷五 release 后，确认 `content/methodology/` 已更新 |
| 2 | **24h 内**对同一 `CONTENT_ROOT` 执行 §2 sync |
| 3 | sync `succeeded` 后跑 **五问 smoke**（至少 **Q1 + Q5**） |
| 4 | sync `failed` → **不得**对外宣称 RAG 语料已更新 |

---

## §8 附录 · 环境变量

完整表见 [`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) **§C.1 Portfolio 演示站**。

| 变量 | portfolio 要点 |
| --- | --- |
| `CONTENT_ROOT` | 前端 `ai-ink-brain/content` 绝对路径 |
| Python `CHAT_API_SECRET` / `NEXT_PUBLIC_ADMIN_SECRET` | Python 进程 admin/sync 鉴权（**服务端** `.env`） |
| 前端 `SYNC_ADMIN_SECRET` | BFF 入站 + 转发 Bearer（**与 Python 同值** · shell 别名 `ADMIN_TOKEN`） |
| `EMBEDDING_DIM` | 与 Supabase `vector(N)` 一致（默认 1024） |
| `SILICONFLOW_API_KEY` | Embedding 必填 |
| `DEBUG_INGEST` | 生产 **关闭** |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-01 | v1：30 帽落盘 · 对齐 `PORTFOLIO-RAG-DEMO@2026-06-01` |
| 2026-06-02 | §1.3–§1.4：ChatBI visitor token 运维签发 + verify 探活 · 与前端 W3 unlock 分工 |
