-- Ops Chat P1-3 · clarify 路由扩展
-- 用途：ops_runs.route CHECK 增加 clarify（FALLBACK 澄清短路）
-- 依赖：ops_desk_s2_session_00_route.sql 已应用

ALTER TABLE public.ops_runs DROP CONSTRAINT IF EXISTS ops_runs_route_check;
ALTER TABLE public.ops_runs ADD CONSTRAINT ops_runs_route_check
  CHECK (route IN ('fast', 'deep', 'react', 'session_00', 'clarify'));
