-- Ops Session S2 · session_orchestrator_v1 route 扩展
-- 用途：ops_runs.route CHECK 增加 session_00（00 层 LangGraph 编排）
-- freeze_id: OPS-SESSION-ORCH-SPEC-V1 · S2

ALTER TABLE public.ops_runs DROP CONSTRAINT IF EXISTS ops_runs_route_check;
ALTER TABLE public.ops_runs ADD CONSTRAINT ops_runs_route_check
  CHECK (route IN ('fast', 'deep', 'react', 'session_00'));
