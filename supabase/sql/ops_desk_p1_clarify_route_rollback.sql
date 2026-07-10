-- Ops Chat P1-3 · clarify 路由扩展回滚

ALTER TABLE public.ops_runs DROP CONSTRAINT IF EXISTS ops_runs_route_check;
ALTER TABLE public.ops_runs ADD CONSTRAINT ops_runs_route_check
  CHECK (route IN ('fast', 'deep', 'react', 'session_00'));
