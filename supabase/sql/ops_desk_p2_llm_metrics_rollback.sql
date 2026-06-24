-- Ops Desk P2-5a-ext rollback
-- 用法：Supabase Dashboard → SQL Editor 粘贴执行，按逆序回滚

-- 1. 先删依赖 view（按创建逆序）
DROP VIEW IF EXISTS public.ops_v_run_metrics_daily_by_route;
DROP VIEW IF EXISTS public.ops_v_run_metrics_daily;

-- 2. 删 GIN 索引
DROP INDEX IF EXISTS idx_ops_runs_metrics_json;

-- 3. 最后删列
ALTER TABLE public.ops_runs DROP COLUMN IF EXISTS metrics_json;
