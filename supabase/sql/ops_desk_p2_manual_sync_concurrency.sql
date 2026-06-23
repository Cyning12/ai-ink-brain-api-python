-- Ops Desk P2-3 hotfix：同一 repo 同时只允许一条 pending/running sync run
-- 应用：Supabase SQL Editor 或 migration 流水线执行一次

create unique index if not exists idx_ops_sync_runs_one_active_per_repo
  on public.ops_sync_runs (repo_id)
  where status in ('pending', 'running');
