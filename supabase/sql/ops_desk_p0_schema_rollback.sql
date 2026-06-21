-- Ops Desk P0 四表回滚（按外键依赖倒序删除）
-- 配套：ops_desk_p0_schema.sql

drop table if exists public.ops_sync_runs cascade;
drop table if exists public.ops_pull_requests cascade;
drop table if exists public.ops_issues cascade;
drop table if exists public.ops_repos cascade;
