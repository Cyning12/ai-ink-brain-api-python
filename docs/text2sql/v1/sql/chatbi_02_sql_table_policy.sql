-- =============================================================================
-- 文件：chatbi_02_sql_table_policy.sql
-- 用途：ChatBI V3 分级权限 · **T2** 每张业务表在 Text2SQL 上的最低操作等级
-- 执行位置：Supabase Dashboard → SQL Editor → 整段粘贴执行
-- 依赖：建议 **先于或后于** chatbi_01_access_tokens.sql 均可（无 FK）；任务单推荐顺序 **01 → 02**
--
-- 等级编码（与 chatbi_access_tokens.access_level、OpenItems §1.2 一致）：
--   0 = Super，1 = Admin，2 = L2 终端用户（数值越小权限越高）
--
-- L2 附加策略（须在 AST 后闸与代码中 enforce，不单靠本表）：
--   禁止 JOIN / 多表；禁止 INSERT；UPDATE 仅允许 chatbi_user_portrait 且列在白名单内；见 OpenItems §1.4。
--
-- 判定规则（实现 Agent 须在代码中单点实现，与本文注释一致）：
--   主体 `access_level` 数值 **越小** 权限 **越高**。
--   对某操作 op，若 `min_*_level` 为 **NULL** → 表示 **禁止**该操作（任何等级均不可，由应用层拒绝）。
--   若 `min_*_level` 非 NULL → 当且仅当 `主体.access_level <= min_*_level` 时 **允许**该操作。
--   例：min_select_level=2 → Super/Admin/L2 均可 SELECT；min_delete_level=0 → 仅 Super 可物理 DELETE。
--
-- `owner_column`：L2 行级过滤时，应用/AST 将强制 `owner_column = 主体的 subject_user_id`（列名可按表覆盖）。
-- =============================================================================

begin;

-- drop table if exists public.chatbi_sql_table_policy cascade;

create table if not exists public.chatbi_sql_table_policy (
  id uuid primary key default gen_random_uuid(),

  schema_name text not null default 'public',
  table_name text not null,

  -- NULL = 禁止该操作类型
  min_select_level smallint null check (min_select_level is null or min_select_level between 0 and 2),
  min_insert_level smallint null check (min_insert_level is null or min_insert_level between 0 and 2),
  min_update_level smallint null check (min_update_level is null or min_update_level between 0 and 2),
  min_delete_level smallint null check (min_delete_level is null or min_delete_level between 0 and 2),

  owner_column text not null default 'user_id',

  notes text null,
  created_at timestamptz not null default now(),

  constraint chatbi_sql_table_policy_schema_table_unique unique (schema_name, table_name)
);

comment on table public.chatbi_sql_table_policy is 'Text2SQL：表级最低操作等级；NULL 表示该操作类型对全等级关闭';
comment on column public.chatbi_sql_table_policy.min_select_level is '允许 SELECT 的最大数字等级：主体 access_level <= 本值；NULL=禁止';
comment on column public.chatbi_sql_table_policy.owner_column is 'L2 行级：WHERE 子句绑定列名，值来自 chatbi_access_tokens.subject_user_id';

create index if not exists chatbi_sql_table_policy_lookup_idx
  on public.chatbi_sql_table_policy (schema_name, table_name);

commit;
