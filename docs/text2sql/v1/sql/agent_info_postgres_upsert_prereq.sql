-- =============================================================================
-- 文件：agent_info_postgres_upsert_prereq.sql
-- 用途：修复 Postgres 报错 — `there is no unique or exclusion constraint matching
--       the ON CONFLICT specification`（对 `agent_info` 使用 `ON CONFLICT (agent_id)` 前
--       须存在以 `agent_id` 为目标的 **UNIQUE** 或 **PRIMARY KEY**）。
-- 执行位置：Supabase Dashboard → SQL Editor（在 `supabase_init.sql` 已建表之后执行一次即可）
-- 依赖：`public.agent_info` 已存在（见 docs/text2sql/v1/sql/supabase_init.sql）
--
-- 说明：
-- - `docs/text2sql/v1/sql/agentinfo.sql` 为 **MySQL Navicat 导出**，无 `ON CONFLICT` 语法；
--   若在 **Postgres** 上自行编写 `INSERT ... ON CONFLICT (agent_id)`，请先执行本脚本。
-- - 若表中已有重复 `agent_id`，须先清洗后再加 UNIQUE。
-- =============================================================================

begin;

do $$
begin
  if not exists (
    select 1
    from pg_constraint c
    join pg_class t on c.conrelid = t.oid
    join pg_namespace n on t.relnamespace = n.oid
    where n.nspname = 'public'
      and t.relname = 'agent_info'
      and c.conname = 'agent_info_agent_id_key'
  ) then
    alter table public.agent_info
      add constraint agent_info_agent_id_key unique (agent_id);
  end if;
end $$;

commit;

-- ---------------------------------------------------------------------------
-- 示例：幂等 upsert（执行完上面约束后可用；列名须与 supabase_init 一致）
-- ---------------------------------------------------------------------------
-- insert into public.agent_info (
--   agent_id, name, gender, date_of_birth, address, phone_number, email_address,
--   certificate_number, license_issue_date, license_expiration_date, commission_structure
-- ) values (
--   100001, 'AI新增用户01', '男', '1990-01-02', '北京', 13800000002, 'test@example.com',
--   11111111, '2022-01-01', '2033-01-01', '固定佣金'
-- )
-- on conflict (agent_id) do update set
--   name = excluded.name,
--   gender = excluded.gender,
--   date_of_birth = excluded.date_of_birth,
--   address = excluded.address,
--   phone_number = excluded.phone_number,
--   email_address = excluded.email_address,
--   certificate_number = excluded.certificate_number,
--   license_issue_date = excluded.license_issue_date,
--   license_expiration_date = excluded.license_expiration_date,
--   commission_structure = excluded.commission_structure;
