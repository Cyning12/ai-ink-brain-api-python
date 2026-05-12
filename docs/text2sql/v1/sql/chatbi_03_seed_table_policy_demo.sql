-- =============================================================================
-- 文件：chatbi_03_seed_table_policy_demo.sql
-- 用途：**演示用**种子数据：为 Text2SQL v1 已有样例表写入几条 `chatbi_sql_table_policy` 行
-- 执行位置：Supabase Dashboard → SQL Editor
-- 依赖：**必须先**已存在 `public.chatbi_sql_table_policy`（见 chatbi_02_sql_table_policy.sql）
--        且目标业务表已存在（如 `public.agent_info` 来自 supabase_init.sql）
--
-- 注意：
-- - 下列策略仅为 **示例**，上线前按真实业务改 `min_*_level` / `owner_column`。
-- - `public.agent_info`（supabase_init）**无** `user_id`，仅有 `agent_id`；本演示将 `owner_column` 设为 `agent_id`，
--   表示「L2 时 subject_user_id 与 agent_id::text 对齐」——**仅演示**，真实业务请改为 `user_id` 等统一归属列。
-- - 使用 `ON CONFLICT DO UPDATE` 便于重复执行幂等。
-- =============================================================================

begin;

-- 示例：agent_info 仅允许 L0/L1 SELECT；INSERT/UPDATE 仅 L0；DELETE 全员关闭（NULL）
insert into public.chatbi_sql_table_policy (
  schema_name, table_name,
  min_select_level, min_insert_level, min_update_level, min_delete_level,
  owner_column, notes
) values (
  'public', 'agent_info',
  1, 0, 0, null,
  'agent_id',
  'demo：L1 可读；写仅 L0；DELETE 关闭；owner 列用 agent_id（样例表无 user_id）'
)
on conflict (schema_name, table_name) do update set
  min_select_level = excluded.min_select_level,
  min_insert_level = excluded.min_insert_level,
  min_update_level = excluded.min_update_level,
  min_delete_level = excluded.min_delete_level,
  owner_column = excluded.owner_column,
  notes = excluded.notes;

commit;
