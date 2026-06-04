# RUNBOOK — Portfolio 演示站 RAG 同源 sync 与五问验收（v1）


| 项              | 内容                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------ |
| **freeze_id**  | `PORTFOLIO-RAG-DEMO@2026-06-01`                                                                                    |
| **关联 SPEC**    | `[SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md](../../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md)` |
| **投递计划**       | `[投递冲刺_20260609_v1_zh.md](../../spec/governance/投递冲刺_20260609_v1_zh.md)` §2                                        |
| **env 真值**     | `[PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md)` §C.1           |
| **本地执行落盘（默认）** | 仓库根 `**tmp/portfolio-rag-demo/`**（不纳入 Git · 见 `[tmp/README.md](../../../tmp/README.md)`）                           |
| **冻结留证（人签后）**  | `[docs/diary/samples/portfolio-rag-demo/](../../diary/samples/portfolio-rag-demo/)`                                |
| **入库路径**       | **仅** `POST /api/py/admin/sync`（**禁止**本 RUNBOOK 使用 `admin/ingest` 备用）                                              |


### 留证路径约定（本地 vs Git）


| 阶段            | 目录                                       | 说明                                                                                    |
| ------------- | ---------------------------------------- | ------------------------------------------------------------------------------------- |
| **本地执行（默认）**  | `tmp/portfolio-rag-demo/`                | sync 轮询 JSON、五问 curl 响应、sources、汇总表 **一律先落此处**                                        |
| **环境变量**      | `PORTFOLIO_RAG_EVIDENCE_DIR`             | 未设时默认 `<repo>/tmp/portfolio-rag-demo`；可覆盖为其他本机路径                                      |
| **冻结留证（Git）** | `docs/diary/samples/portfolio-rag-demo/` | **HG-W5-SYNC / HG-W5-FIVE-Q 人签前**：从 tmp **脱敏复制** 上表文件；**禁止**把 token/密钥 commit 进 diary |


**每次开跑前（仓库根）**：

```bash
export REPO_ROOT="$(git rev-parse --show-toplevel)"
export PORTFOLIO_RAG_EVIDENCE_DIR="${PORTFOLIO_RAG_EVIDENCE_DIR:-$REPO_ROOT/tmp/portfolio-rag-demo}"
mkdir -p "$PORTFOLIO_RAG_EVIDENCE_DIR"
```

下文 `$PORTFOLIO_RAG_EVIDENCE_DIR` 均指上述目录。

---

## §1 前提与权限

### 1.1 执行环境


| 项                | 要求                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| **五问预跑环境**       | **预发 / Preview 与生产等价**：同 Supabase 项目、同 `EMBEDDING_DIM`、同 `CONTENT_ROOT` 挂载语义（SPEC Q-3）                  |
| **演示 URL**       | portfolio 模式同一 Vercel 项目（如 `https://ai-ink-brain.vercel.app/unified-chat`）；BFF 转发至 Python API           |
| **RAG 入口**       | `**POST /api/py/unified/chat`** 或 `**/stream**`；Bearer **visitor** ChatBI token（**不禁 text2sql** · T-05） |
| **CONTENT_ROOT** | **必须**显式指向前端仓 `ai-ink-brain/content/`；**禁止**生产依赖后端仓 `REPO_ROOT/content` 回退                              |


### 1.2 前置检查（sync 前）

```bash
# 1) 确认 CONTENT_ROOT 为目录且含三类文稿（目标态）
test -d "$CONTENT_ROOT/methodology" && test -d "$CONTENT_ROOT/resume" && test -d "$CONTENT_ROOT/evidence"
find "$CONTENT_ROOT/methodology" "$CONTENT_ROOT/resume" "$CONTENT_ROOT/evidence" -name '*.md' | head

# 2) 确认 Python 服务可读 env（本地示例）
# export CONTENT_ROOT="/Users/cyning/Desktop/Projects/ai-ink-brain/content"
# CONTENT_ROOT="/Users/cyning/Desktop/Projects/ai-ink-brain/content"
```

### 1.3 鉴权（不写明文密钥）

> **废弃说明（2026-06）**：`NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` **已废弃**（前端不再使用）；Python `admin_secret()` 仍作 fallback，**计划后续删除**。portfolio / sync **真值** = **`SYNC_ADMIN_SECRET`**（与前端 BFF 同值 · 见 [`SPEC-portfolio_admin_sync_auth_v1_zh.md`](../../../ai-ink-brain/content/tasks/specs/SPEC-portfolio_admin_sync_auth_v1_zh.md)）。

> **易错（2026-06）**：本地 **三种入口** 鉴权不同，勿混用 token / Cookie。
>
> | 入口 | 你传的凭证 | 服务端行为 |
> | --- | --- | --- |
> | **`GET /api/py/chat/history`**（直连 Python） | Bearer **visitor** ChatBI token（或回退 admin） | Python 校验 |
> | **`POST /api/admin/sync`**（**BFF** · `localhost:3000`） | **无 Bearer 也行**：`chatbi_site_bearer` Cookie（SystemStatus 管理会话）· 或 Bearer `$SYNC_ADMIN_SECRET` | BFF 入站鉴权 → **`forwardToPyAdmin` 注入** `SYNC_ADMIN_SECRET` 再调 Python |
> | **`POST /api/py/admin/sync`**（**直连 Python** · `:8000`） | Bearer **`SYNC_ADMIN_SECRET`**（须写入 **Python `.env`**） | Python `admin_secret()`；**不读** Cookie |
>
> **因此**：浏览器点 sync **202** 只说明 **前端 `.env.local` 的 `SYNC_ADMIN_SECRET` + BFF 转发 OK**；直连 Python 仍 **401** 的常见原因：① shell 里 `$ADMIN_TOKEN` 是 visitor token；② **Python `.env` 未设或未对齐** `SYNC_ADMIN_SECRET`（BFF 有、Python 无）。

**请用两个 shell 变量，勿混用：**

| Shell 变量 | 对应 env / 来源 | 用途 |
| --- | --- | --- |
| **`SYNC_ADMIN_SECRET`** / **`ADMIN_TOKEN`** | **前端** `.env.local` 与 **Python** `.env` **同值** | BFF Bearer curl · 直连 Python sync |
| **`VISITOR_CHATBI_TOKEN`** | §1.4 签发的 ChatBI 明文 token | §4 五问 Unified · **history 探活** |

| 用途 | 入口 | Header / Cookie |
| --- | --- | --- |
| **sync（本地推荐 · 路径 B）** | `POST http://localhost:3000/api/admin/sync` | Bearer `$SYNC_ADMIN_SECRET` **或** 浏览器同款 `Cookie: chatbi_site_bearer=…` |
| **sync（运维 · 路径 A）** | `POST $PY_API_URL/api/py/admin/sync` | Bearer `$SYNC_ADMIN_SECRET`（**Python `.env` 必须有**） |
| **history / 五问** | `$PY_API_URL/...` | Bearer `$VISITOR_CHATBI_TOKEN` |
| ~~废弃~~ | — | ~~`CHAT_API_SECRET` / `NEXT_PUBLIC_ADMIN_SECRET`~~ · 勿新配 |

**对齐 `SYNC_ADMIN_SECRET`（两端须同值 · 示例）：**

```bash
# 前端（BFF 转发用）
grep '^SYNC_ADMIN_SECRET=' ~/Desktop/Projects/ai-ink-brain/.env.local

# 后端（直连 Python 用 · 值须与上一行一致）
grep '^SYNC_ADMIN_SECRET=' ~/Desktop/Projects/ai-ink-brain-api-python/.env

# 写入 Python .env 后重启 uvicorn
export ADMIN_TOKEN="$SYNC_ADMIN_SECRET"
```


### 1.4 运维签发 ChatBI visitor token（五问 curl · W5）

> **与前端 W3 分工**：招聘访客 **默认 UX** 为前端 `POST /api/auth/unlock` + `PORTFOLIO_VISITOR_`*（见配对前端 SPEC §4.3）；**本 RUNBOOK 五问 curl** 直连 Python API 时使用 **ChatBI DB token**。


| 步骤  | 动作                                                                                                                                               |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | 本机（仓库根）：`python3 docs/diary/local_chatbi_access_token_gen.py --level 2 --subject-user-id <user_id> --label portfolio-five-q --expires-in-days 7` |
| 2   | 将脚本 stdout 的 **INSERT SQL** 在 Supabase SQL Editor 执行（**勿**将明文 token 提交 Git）                                                                      |
| 3   | 探活：`curl -sS "$PY_API_URL/api/py/chatbi/access/verify" -H "Authorization: Bearer $VISITOR_CHATBI_TOKEN"` → `ok: true`                                   |
| 4   | 五问 / history：`Authorization: Bearer $VISITOR_CHATBI_TOKEN` 调用 Unified 或 `GET /api/py/chat/history`（**不禁 text2sql** · level 2 `end_user`）                                               |


**禁止**：用 `SYNC_ADMIN_SECRET` / `ADMIN_TOKEN` 冒充五问 visitor Bearer；admin token **仅** §2 sync。**禁止**用 history 探活结果推断 sync 鉴权已通过（见 §1.3）。

---

## §2 Sync 执行

> **本地联调**：`pnpm dev` 已起时，**优先路径 B（BFF）**——与浏览器 SystemStatus 点 sync 同链；见 [`SPEC-portfolio_admin_sync_auth_v1_zh.md`](../../../ai-ink-brain/content/tasks/specs/SPEC-portfolio_admin_sync_auth_v1_zh.md)。

| 路径 | 适用 | POST 目标 |
| --- | --- | --- |
| **B · BFF**（本地推荐） | 前端 `:3000` 已起；Cookie 或 Bearer | `http://localhost:3000/api/admin/sync` |
| **A · 直连 Python** | 生产/脚本；**Python `.env` 已设 `SYNC_ADMIN_SECRET`** | `$PY_API_URL/api/py/admin/sync` |

### 2.1 路径 B — BFF（与浏览器一致）

**B1 · Bearer**（维护者 curl · 读 **前端** `.env.local`）：

```bash
export INK_ROOT="${INK_ROOT:-$HOME/Desktop/Projects/ai-ink-brain}"
set -a && source "$INK_ROOT/.env.local" && set +a
export BFF_URL="${BFF_URL:-http://localhost:3000}"

curl -sS -X POST "$BFF_URL/api/admin/sync" \
  -H "Authorization: Bearer $SYNC_ADMIN_SECRET" \
  -H "Content-Type: application/json" | jq .
```

**B2 · Cookie**（DevTools → Network → 复制 Request Headers 里的 `Cookie`；**勿**提交 Git）：

```bash
# 浏览器成功示例：仅 Cookie、无 Authorization（chatbi_site_bearer = 管理会话）
curl -sS -X POST "$BFF_URL/api/admin/sync" \
  -H "Content-Type: application/json" \
  -H "Cookie: chatbi_site_bearer=<DevTools 原样>; portfolio_visitor_session=<可选>"
```

BFF 校验通过后，由 `forwardToPyAdmin` **服务端**带 `Authorization: Bearer $SYNC_ADMIN_SECRET` 调 Python；**你无需**在 Cookie curl 里手写 Python Bearer。

### 2.2 路径 A — 直连 Python

```bash
export PY_API_URL="${PY_API_URL:-http://127.0.0.1:8000}"
set -a && source .env && set +a
export ADMIN_TOKEN="$SYNC_ADMIN_SECRET"
test -n "$ADMIN_TOKEN" || { echo "Python .env 缺少 SYNC_ADMIN_SECRET（须与前端 .env.local 同值）"; exit 1; }

curl -sS -X POST "$PY_API_URL/api/py/admin/sync" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" | jq .
```

**期望**：HTTP **202**，响应含 `job.id` 与 `statusUrl`（形如 `/api/py/admin/sync?jobId=<uuid>`）。

### 2.3 轮询 job

**与创建 job 同路径**（BFF 创建的 job 用 BFF 轮询；直连 Python 则用 Python URL）：

```bash
export JOB_ID="<上一步 job.id>"
export SYNC_POLL_JSON="$PORTFOLIO_RAG_EVIDENCE_DIR/sync-job-poll.json"

# 路径 B 示例（Bearer · 与 §2.1 B1 相同 env）
while true; do
  curl -sS "$BFF_URL/api/admin/sync?jobId=$JOB_ID" \
    -H "Authorization: Bearer $SYNC_ADMIN_SECRET" | tee "$SYNC_POLL_JSON"
  STATUS=$(python3 -c "import json,sys; print(json.load(open('$SYNC_POLL_JSON'))['job']['status'])")
  echo "status=$STATUS"
  case "$STATUS" in
    succeeded|failed) break ;;
    *) sleep 3 ;;
  esac
done

# 路径 A：将 URL 换为 "$PY_API_URL/api/py/admin/sync?jobId=$JOB_ID" + Bearer $ADMIN_TOKEN
```


| 参数   | 值           |
| ---- | ----------- |
| 轮询间隔 | **2～5s**    |
| 总超时  | **≤60 min** |


### 2.4 成功硬检查（全部满足才进入 §4 五问）


| 检查项                     | 阈值                                                        |
| ----------------------- | --------------------------------------------------------- |
| `job.status`            | `**succeeded`**                                           |
| `result.filesScanned`   | `**> 0**`（`=0` 记 **FAIL** · Q-4）                          |
| `result.chunksUpserted` | `**> 0`**                                                 |
| 目录覆盖                    | `methodology/`、`resume/`、`evidence/` **各 ≥1** 个 `.md` 被扫描 |


**留证**：将终态 JSON 摘要保存至 `**$PORTFOLIO_RAG_EVIDENCE_DIR/sync-job-final.json`**（可删敏感字段）；人签 `**HG-W5-SYNC**` 后脱敏复制至 `docs/diary/samples/portfolio-rag-demo/sync-job-final.json`。

---

## §3 Sync 失败排障


| 错误特征                                     | 含义                                    | 处置                                                                                   | 可重试                |
| ---------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------ | ------------------ |
| **`401 Unauthorized`**（**直连 Python**） | Bearer 非 `SYNC_ADMIN_SECRET`；或 **Python `.env` 未设**（BFF 仍 202） | 把前端 `.env.local` 同值写入 Python `.env` → **重启 uvicorn**；或改走 **§2.1 路径 B** |
| **`403 Forbidden`**（**BFF** `:3000`） | 无有效 Cookie / Bearer | SystemStatus 进 **ADMIN MODE** 或 `-H "Authorization: Bearer $SYNC_ADMIN_SECRET"`（前端 `.env.local`） |
| **`401 Unauthorized`**（直连 · 曾用 visitor token） | `$ADMIN_TOKEN` = 五问 token | 勿混用；sync 只用 `$SYNC_ADMIN_SECRET` |
| `Embedding 维度为 … 与期望 … 不一致`              | `EMBEDDING_DIM` 与 `vector(N)` 不一致     | 对齐 env 与 `supabase/sql/init.sql`；**勿**临时改库维度                                         | 修正后重跑 sync         |
| `CONTENT_ROOT=… 不是目录` / `filesScanned=0` | 路径错或目录空                               | 修正 mount；补三类 content 后再 sync                                                         | 是                  |
| SiliconFlow / Supabase 失败                | 上游或密钥                                 | 查 `SILICONFLOW_API_KEY`、Supabase service role                                        | 指数退避               |
| `**404 Job not found`**                  | redeploy / 单实例 job 丢失                 | **重新 `POST`** 创建 job；sync 窗口 **避免** 并发 redeploy                                      | 是                  |
| ingest `400` + 「维度」                      | 同维度不匹配                                | 同上 Embedding 行                                                                       | 修正后重跑              |
| sync 已成功但五问 **答 Harness.io / 无 sources** | 库无 portfolio 语料或 `RAG_RETRIEVE_EMPTY` | 见 `[GUIDE_rag_user_self_check_v1_zh.md](./GUIDE_rag_user_self_check_v1_zh.md)` §3～§5 | 灌库 / FTS / 阈值对齐后重问 |


---

## §4 五问验收表

**通过口径**：**5/5** 非空切题；sources **≥4/5**；单问 **≤3** 次重试仍不达标则记 **FAIL**。


| #      | 标准问句（chip 可粘贴）                        | 期望 `content/` 路径     | sources 主 `metadata.category` | 合格要点                                      |
| ------ | ------------------------------------- | -------------------- | ----------------------------- | ----------------------------------------- |
| **Q1** | 《AI 编程可闭环协作》**卷三**讲什么？Harness 和签收是什么？ | `methodology/vol3_*` | `**methodology`**             | 任务单 + 书面签收 + 合并前 CI；sources 含 vol3        |
| **Q2** | **RAG 混合检索**怎么做的？                     | `resume/*`           | `**resume`**                  | 向量 + 混合检索 + rerank 至少两项                   |
| **Q3** | **冷/温/热** 和 **架构三层** 区别？              | `evidence/*`         | `**evidence` only**           | 记忆分层 ≠ 架构分层；**methodology vol3 不计 Q3 通过** |
| **Q4** | **11 年经历**里 AI Coding 相关成果？           | `resume/*`           | `**resume`**                  | 百果园 Cursor + Ink + 连载；不虚构                 |
| **Q5** | 按需读图相对整图灌入 **token/效果**？**边界**？       | `evidence/*`         | `**evidence`**                | 约 1/9 或「约十分之一」+ **小样本、非全行业**              |


**Unified 调用示例（JSON）**：

```bash
curl -sS -X POST "$PY_API_URL/api/py/unified/chat" \
  -H "Authorization: Bearer $VISITOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"<上表问句>","session_id":"portfolio-five-q-smoke"}' \
  -D "$PORTFOLIO_RAG_EVIDENCE_DIR/unified-headers.txt" \
  | tee "$PORTFOLIO_RAG_EVIDENCE_DIR/unified-response.json"
# sources：响应 JSON events 内 rag.sources，或响应头 x-sources（若 BFF 透传）
# 五问逐条留证建议：q{N}-response-run{1,2}.json 等同目录命名
```

术语纠偏见 `[GUIDE_冷温热层_对内术语_v1_zh.md](./GUIDE_冷温热层_对内术语_v1_zh.md)`。

### §4.1 Intent Hints 补充问（Step1 · 不纳入 5/5 计数）

> **状态（2026-06-04）**：Step1（#109）五问 **5/5 人验已通过**；本表 **不单独 reinspect 落盘**，仅作 Intent Hints / 人名路由 smoke 参考。U1.5 重试逻辑合 main 后，可与下表一并 spot-check。

| # | 标准问句（chip 可粘贴） | 期望 `content/` 路径 | sources 主 `metadata.category` | 合格要点 |
| --- | --- | --- | --- | --- |
| **Q-INTENT** | 聊聊你对刘新宁的看法，他在 AI coding 岗位有什么优势。 | `resume/*` | **`resume`** | Intent → `rag_search`（非 `direct_answer`）；sources 含 `resume/cv-online.md` 或同类；回答含履历/优势要点（百果园 / Cursor / Ink 等 **至少一项**） |

**负例（仍须 direct_answer）**：「解释一下量子计算，用通俗语言」→ 见 §4 **Q 表外** Step1 负例 smoke。

---

## §5 单问重试规则

1. 同一问 **最多 3 次**（可调 chip 文案或 session，**不得**刷通过率）。
2. 第 3 次仍不达标 → 该问记 **FAIL**，写入留证表 blocker 列。
3. 若多问 FAIL → 阻塞 6/9 全绿；须补 content 或修正 ingest 后 **重新 sync** 再跑。

---

## §6 Sources 留证


| 项              | 要求                                                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **强制**         | **Q1**、**Q5** 保存 sources JSON（或 SSE `rag.sources` 片段）                                                                  |
| **可复现**        | 同 visitor token、**同问句** 预跑 **2 次**；主 `metadata.category` **须一致**（不一致记 FAIL · Q-9:A）                                    |
| **路径字段**       | 每条主 source 须含非空 `**relativePath`**（或 `path` 同值）；验收时核对前缀与 §4 期望目录一致（SPEC §4.5.3）                                        |
| **块序号**        | 建议记录 `**chunk_index`**；同文件多块时用于消歧（当前切片 **512 字 / 50 overlap**，无标题锚点 · SPEC §4.5.1）                                     |
| **落盘（本地默认）**   | `$PORTFOLIO_RAG_EVIDENCE_DIR/q1-sources-run{1,2}.json`、`q5-sources-run{1,2}.json`                                      |
| **五问汇总（本地默认）** | `$PORTFOLIO_RAG_EVIDENCE_DIR/five-questions-results.md`：问句 / pass-fail / 重试次数 / sources category **与 relativePath 摘要** |
| **冻结（人签后）**    | 脱敏复制上列文件 → `docs/diary/samples/portfolio-rag-demo/`（**HG-W5-FIVE-Q**）                                                  |


**人签后复制示例（脱敏后）**：

```bash
DIARY_EVIDENCE="$REPO_ROOT/docs/diary/samples/portfolio-rag-demo"
cp "$PORTFOLIO_RAG_EVIDENCE_DIR/sync-job-final.json" "$DIARY_EVIDENCE/"
cp "$PORTFOLIO_RAG_EVIDENCE_DIR"/q1-sources-run*.json "$DIARY_EVIDENCE/"
cp "$PORTFOLIO_RAG_EVIDENCE_DIR"/q5-sources-run*.json "$DIARY_EVIDENCE/"
cp "$PORTFOLIO_RAG_EVIDENCE_DIR/five-questions-results.md" "$DIARY_EVIDENCE/"
# 复制前确认 JSON/MD 无 Bearer token、密钥、完整 PII
```

**单条 source 最低字段（留证 JSON 自检）**：

```json
{
  "relativePath": "methodology/vol3_xxx.md",
  "path": "methodology/vol3_xxx.md",
  "filename": "vol3_xxx.md",
  "category": "methodology",
  "chunk_index": 0,
  "snippet": "…"
}
```

> **前端跳转**：`url` 多为 `null`；W6 由前端将 `relativePath` 映射至 `/methodology`  `/resume`  `/evidence`（见 SPEC §4.5.3）。RUNBOOK 验收 **只验 API 字段**，不验点击行为。

---

## §7 卷四 / 卷五 release 后再 sync


| 步骤  | 动作                                               |
| --- | ------------------------------------------------ |
| 1   | 公众仓卷四/卷五 release 后，确认 `content/methodology/` 已更新 |
| 2   | **24h 内**对同一 `CONTENT_ROOT` 执行 §2 sync           |
| 3   | sync `succeeded` 后跑 **五问 smoke**（至少 **Q1 + Q5**） |
| 4   | sync `failed` → **不得**对外宣称 RAG 语料已更新             |


---

## §8 附录 · 环境变量

完整表见 `[PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md)` **§C.1 Portfolio 演示站**。


| 变量 | portfolio 要点 |
| --- | --- |
| `CONTENT_ROOT` | 前端 `ai-ink-brain/content` 绝对路径 |
| **`SYNC_ADMIN_SECRET`** | Python + 前端 BFF admin/sync **同值**；shell：`export ADMIN_TOKEN="$SYNC_ADMIN_SECRET"`（**≠** visitor token） |
| **`VISITOR_CHATBI_TOKEN`** | 五问 / history / verify；**勿**用于 sync |
| ~~`CHAT_API_SECRET` / `NEXT_PUBLIC_ADMIN_SECRET`~~ | **已废弃 · 待删**；勿新配 |
| `EMBEDDING_DIM` | 与 Supabase `vector(N)` 一致（默认 1024） |
| `SILICONFLOW_API_KEY` | Embedding 必填 |
| `DEBUG_INGEST` | 生产 **关闭** |


---

## 修订记录


| 日期         | 摘要                                                                                     |
| ---------- | -------------------------------------------------------------------------------------- |
| 2026-06-01 | v1：30 帽落盘 · 对齐 `PORTFOLIO-RAG-DEMO@2026-06-01`                                         |
| 2026-06-02 | §1.3–§1.4：ChatBI visitor token 运维签发 + verify 探活 · 与前端 W3 unlock 分工                     |
| 2026-06-03 | §6：sources **relativePath** 留证 · 块序号说明 · 对齐 SPEC §4.5                                  |
| 2026-06-03 | 留证路径：本地默认 `**tmp/portfolio-rag-demo/`** · `PORTFOLIO_RAG_EVIDENCE_DIR` · diary 为冻结复制目标 |
| 2026-06-03 | §1.3/§8：`SYNC_ADMIN_SECRET` 为 admin 真值；`CHAT_API_*` / `NEXT_PUBLIC_*` 标注废弃待删 |
| 2026-06-03 | §1.3/§2/§3：history 与 sync 鉴权分离；401 排障；`ADMIN_TOKEN` 须来自 `.env` 的 `SYNC_ADMIN_SECRET` |
| 2026-06-04 | §4.1：Intent Hints Q-INTENT 补充问（Step1 五问已验 · 不单独落盘） |


