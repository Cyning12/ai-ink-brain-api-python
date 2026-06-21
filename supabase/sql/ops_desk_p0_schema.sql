-- Ops Desk P0 数据层：监控仓、Issue、Pull Request、Sync Run
-- 参考：ROUND_03_R2_gha_sync_schema.md §3.3 DDL 草案
-- 范围：ops_repos / ops_issues / ops_pull_requests / ops_sync_runs

create extension if not exists "pgcrypto";

create table if not exists public.ops_repos (
  id uuid primary key default gen_random_uuid(),
  owner text not null,
  name text not null,
  full_name text generated always as (owner || '/' || name) stored,
  default_branch text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (owner, name)
);

create table if not exists public.ops_issues (
  id uuid primary key default gen_random_uuid(),
  repo_id uuid not null references public.ops_repos(id) on delete cascade,
  number int not null,
  title text not null,
  body text,
  state text not null check (state in ('open','closed')),
  labels text[] default '{}',
  assignees text[] default '{}',
  milestone text,
  created_at timestamptz not null,
  updated_at timestamptz not null,
  closed_at timestamptz,
  author text,
  html_url text,
  scan_tags text[] default '{}',
  unique (repo_id, number)
);

create table if not exists public.ops_pull_requests (
  id uuid primary key default gen_random_uuid(),
  repo_id uuid not null references public.ops_repos(id) on delete cascade,
  number int not null,
  title text not null,
  body text,
  state text not null check (state in ('open','closed','merged')),
  draft bool default false,
  labels text[] default '{}',
  created_at timestamptz not null,
  updated_at timestamptz not null,
  closed_at timestamptz,
  merged_at timestamptz,
  author text,
  html_url text,
  head_ref text,
  base_ref text,
  checks_conclusion text,
  review_decision text,
  first_review_at timestamptz,
  additions int,
  deletions int,
  changed_files int,
  unique (repo_id, number)
);

create table if not exists public.ops_sync_runs (
  id uuid primary key default gen_random_uuid(),
  repo_id uuid not null references public.ops_repos(id) on delete cascade,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  status text not null check (status in ('pending','running','success','failed','partial')),
  cursor timestamptz,
  records_issue int default 0,
  records_pr int default 0,
  error_message text,
  trigger text not null check (trigger in ('cron','manual','initial'))
);

create index if not exists idx_ops_issues_repo_state on public.ops_issues(repo_id, state);
create index if not exists idx_ops_issues_updated on public.ops_issues(repo_id, updated_at desc);
create index if not exists idx_ops_issues_created on public.ops_issues(created_at desc);
create index if not exists idx_ops_pulls_repo_state on public.ops_pull_requests(repo_id, state);
create index if not exists idx_ops_pulls_updated on public.ops_pull_requests(repo_id, updated_at desc);
create index if not exists idx_ops_sync_runs_repo_started on public.ops_sync_runs(repo_id, started_at desc);
