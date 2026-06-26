-- Ops Desk P3-1 ReAct fallback route 扩展
-- 用途：将 ops_runs.route 的 CHECK 约束从 ('fast','deep') 扩展为 ('fast','deep','react')
-- freeze_id: OPS-DESK-KIMI-CODE-P3-REACT-FALLBACK

ALTER TABLE public.ops_runs DROP CONSTRAINT IF EXISTS ops_runs_route_check;
ALTER TABLE public.ops_runs ADD CONSTRAINT ops_runs_route_check
  CHECK (route IN ('fast','deep','react'));
