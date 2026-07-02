-- Rollback · ops_desk_s2_session_00_route.sql
-- 注意：若已有 session_00 行，回滚前须清理或改 route

ALTER TABLE public.ops_runs DROP CONSTRAINT IF EXISTS ops_runs_route_check;
ALTER TABLE public.ops_runs ADD CONSTRAINT ops_runs_route_check
  CHECK (route IN ('fast', 'deep', 'react'));
