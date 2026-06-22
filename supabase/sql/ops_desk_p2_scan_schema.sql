-- Ops Desk P2-2 Scan Ingest 数据层
-- 范围：ops_scan_snapshots / ops_graph_snapshots / ops_sync_run_artifacts
-- 参考：ROUND_06_R5_track_c_deps.md §3.3

create extension if not exists "pgcrypto";

create table if not exists public.ops_graph_snapshots (
  id uuid primary key default gen_random_uuid(),
  repo_id uuid not null references public.ops_repos(id) on delete cascade,
  source_branch text not null,
  source_commit text,
  manifest_version text,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_ops_graph_snapshots_repo_created on public.ops_graph_snapshots(repo_id, created_at desc);

create table if not exists public.ops_scan_snapshots (
  id uuid primary key default gen_random_uuid(),
  repo_id uuid not null references public.ops_repos(id) on delete cascade,
  scan_version text not null,
  total_open int,
  p0_items jsonb default '[]'::jsonb,
  p1_items jsonb default '[]'::jsonb,
  p2_items jsonb default '[]'::jsonb,
  deferred_items jsonb default '[]'::jsonb,
  raw_markdown_url text,
  parsed_summary jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_ops_scan_snapshots_repo_created on public.ops_scan_snapshots(repo_id, created_at desc);

create table if not exists public.ops_sync_run_artifacts (
  id uuid primary key default gen_random_uuid(),
  sync_run_id uuid not null references public.ops_sync_runs(id) on delete cascade,
  graph_snapshot_id uuid references public.ops_graph_snapshots(id) on delete set null,
  scan_snapshot_id uuid references public.ops_scan_snapshots(id) on delete set null,
  created_at timestamptz not null default now()
);

create index if not exists idx_ops_sync_run_artifacts_run on public.ops_sync_run_artifacts(sync_run_id);
