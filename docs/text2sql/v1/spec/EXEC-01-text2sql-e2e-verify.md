# EXEC-01：Text2SQL v1 端到端验收（本地 + 远程 Supabase）

## 目标

验证 `POST /api/py/text2sql/chat` 的最小闭环可用：

- 意图识别 → 检索（DDL + 示例）→ LLM 生成 SQL → 只读校验 → 连接 Supabase Postgres 执行 → 返回 `rows` + `answer`

## 前置条件

- Supabase 已执行 `docs/text2sql/v1/sql/supabase_init.sql`（至少表已创建；是否有样例数据按实际为准）
- `.env`（项目根目录 `ai-ink-brain-api-python/.env`）已配置：
  - `SILICONFLOW_API_KEY`
  - `API_KEY`（后端接口鉴权用，不是 SiliconFlow key）
  - `TEXT2SQL_DATABASE_URL`（推荐使用 **Transaction pooler** 的连接串）

## 关键配置说明（容易踩坑）

- **Pooler 用户名格式**：通常需要携带 tenant/project-ref，例如 `text2sql_ro_user.<project_ref>`
- **避免误加载其它项目 .env**：建议启动服务前显式 `source .env`，确保进程环境变量来自本项目

## 操作步骤

### 1) 启动本地服务（显式加载本项目 .env）

在 `ai-ink-brain-api-python` 项目根目录执行：

```bash
set -a && source .env && set +a
python -m uvicorn api.index:app --host 127.0.0.1 --port 8000
```

预期输出包含：

- `Uvicorn running on http://127.0.0.1:8000`

### 2) 直连数据库可用性（可选但建议）

用 `TEXT2SQL_DATABASE_URL` 直接跑一个只读查询，验证网络/用户名/密码都正确：

```sql
select count(*) as cnt from public.agent_info;
```

预期：

- 连接成功
- 返回 1 行 `cnt`（可能为 0，取决于是否导入了样例数据）

### 3) 调用 Text2SQL 接口（端到端）

请求：

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/py/text2sql/chat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"local-test","query":"统计 agent_info 表里有多少条数据"}'
```

预期响应（字段示例）：

- `ok: true`
- `mode: "text2sql"`
- `sql`：形如 `select count(*) from agent_info`
- `rows`：形如 `[{"count": 0}]` 或 `[{"count": 10}]`
- `answer`：当结果是聚合 `count/cnt` 时，应该是确定性文本，例如 `共有 0 条。`

## 常见错误与定位

- **401 Unauthorized**
  - 说明接口鉴权未通过：检查请求头里的 `Authorization: Bearer ...` 是否使用了本项目 `.env` 的 `API_KEY`
- **DB 连接失败 / Tenant or user not found**
  - 检查 `TEXT2SQL_DATABASE_URL`：
    - host/port 是否来自 Transaction pooler
    - user 是否包含 `<project_ref>`（例如 `text2sql_ro_user.<project_ref>`）
- **LLM 401 Api key is invalid**
  - 检查 `SILICONFLOW_API_KEY` 是否为 SiliconFlow 控制台生成的 key，且本项目启动时确实加载到了该值

