-- Ops Desk P2-2 Scan Ingest rollback
-- 顺序：先删关联表，再删快照表

drop table if exists public.ops_sync_run_artifacts cascade;
drop table if exists public.ops_graph_snapshots cascade;
drop table if exists public.ops_scan_snapshots cascade;
