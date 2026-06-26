-- Ops Desk P3-1 ReAct fallback route Rollback
-- 还原 ops_runs.route CHECK 为原始 ('fast','deep')

ALTER TABLE public.ops_runs DROP CONSTRAINT IF EXISTS ops_runs_route_check;
ALTER TABLE public.ops_runs ADD CONSTRAINT ops_runs_route_check
  CHECK (route IN ('fast','deep'));
