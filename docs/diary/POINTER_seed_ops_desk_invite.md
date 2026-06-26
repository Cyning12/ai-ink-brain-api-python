# POINTER · Ops Desk invite 本地 seed 脚本

> **脚本本体不在 Git**（对齐 ChatBI `tmp/diary/local_chatbi_access_token_gen.py`）。  
> **本机路径（api-python 仓根）**：`tmp/diary/seed_ops_desk_invite.py`  
> **目录约定**：见 [`tmp/README.md`](../../tmp/README.md) §`tmp/diary/`

## 用途

- **默认自动生成** `secrets.token_urlsafe(32)` 明文并打印（请自行保存）
- 向 `ops_desk_invites` 写入 **token_hash**（DB **不存明文**）
- 可选 `expires_at`（`--expires-hours` / `--expires-days` · 最小 0.01h）

## 清空旧密钥（Supabase SQL Editor）

执行 [`supabase/sql/ops_desk_p3_auth_reset.sql`](../../supabase/sql/ops_desk_p3_auth_reset.sql)：

```sql
DELETE FROM public.ops_desk_sessions;
DELETE FROM public.ops_desk_invites;
```

## 常用命令（仓库根）

```bash
cd ai-ink-brain-api-python

# 1. 先清空（可选）→ Supabase 跑 reset.sql

# 2. 自动生成 maintainer 明文 + seed
python3 tmp/diary/seed_ops_desk_invite.py --label maintainer --role maintainer

# 7 天 visitor
python3 tmp/diary/seed_ops_desk_invite.py --label guest --role viewer --expires-days 7

# 使用已有明文
python3 tmp/diary/seed_ops_desk_invite.py --label maintainer --role maintainer --token "YOUR_TOKEN"
```

## 关联

| 文档 | 说明 |
| --- | --- |
| [`supabase/sql/ops_desk_p3_auth.sql`](../../supabase/sql/ops_desk_p3_auth.sql) | DDL |
| [`supabase/sql/ops_desk_p3_auth_reset.sql`](../../supabase/sql/ops_desk_p3_auth_reset.sql) | 清空 invite/session |

**勿**将终端输出的明文或 `.env` 提交到 GitHub。
