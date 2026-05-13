-- =============================================================================
-- 文件：chatbi_01_access_tokens.sql
-- 用途：ChatBI V3 分级权限 · **T1** 访问令牌表（Bearer 鉴权用，仅存哈希）
-- 执行位置：Supabase Dashboard → SQL Editor → 整段粘贴执行
-- 依赖：无（建议在业务库 `public` schema）
-- 执行顺序：与任务单一致 **01 → 02 →（可选）03 → 04**（`chatbi_04_user_portrait.sql`）
--
-- 说明：
-- - 请求头 `Authorization: Bearer <明文 token>` 仅在 HTTPS 下传输；库内 **只存 key_hash**。
-- - `access_level`（与 OpenItems §1.2 对齐）：**0 = Super**，**1 = Admin**，**2 = L2 终端用户**。
--   Super：目标态仅管理台签发；Admin = 合并原 temp_admin 与 admin 同档；L2 须配合肖像表与闸门策略。
-- - `subject_user_id`：**L2 必填**（与 `chatbi_user_portrait.user_id` 等对齐）；Super/Admin 可留空。
-- - 插入/轮换 token 的 **明文** 不落库；手工造哈希见任务单 `docs/tasks/done/task_chatbi_level_gate_v1.md` §「RUNBOOK：生成 key_hash」。
-- =============================================================================

begin;

-- 若需幂等重跑，可先取消下一行注释（会删表，谨慎）
-- drop table if exists public.chatbi_access_tokens cascade;

create table if not exists public.chatbi_access_tokens (
  id uuid primary key default gen_random_uuid(),

  -- SHA-256 等十六进制小写哈希（实现须与 FastAPI 侧 `hmac.compare_digest` 比对逻辑一致）
  key_hash text not null,

  -- 0=Super 1=Admin 2=L2（终端用户）
  access_level smallint not null check (access_level between 0 and 2),

  -- L2 必填：与 chatbi_user_portrait.user_id 等一致；Super/Admin 可 null
  subject_user_id text null,

  label text null,
  expires_at timestamptz null,
  revoked_at timestamptz null,
  created_at timestamptz not null default now(),
  metadata jsonb not null default '{}'::jsonb,

  constraint chatbi_access_tokens_key_hash_unique unique (key_hash)
);

comment on table public.chatbi_access_tokens is 'ChatBI：Bearer API key 哈希 + 访问等级；明文 token 仅运维本地生成后写入哈希';
comment on column public.chatbi_access_tokens.key_hash is '明文 token 经哈希后的十六进制字符串；禁止存明文';
comment on column public.chatbi_access_tokens.access_level is '0=Super 1=Admin（合并原 temp+admin）2=L2 终端用户';
comment on column public.chatbi_access_tokens.subject_user_id is 'L2 主体归属键，与 chatbi_sql_table_policy.owner_column 指向列对齐';

create index if not exists chatbi_access_tokens_key_hash_active_idx
  on public.chatbi_access_tokens (key_hash)
  where revoked_at is null;

create index if not exists chatbi_access_tokens_level_idx
  on public.chatbi_access_tokens (access_level)
  where revoked_at is null;

commit;
