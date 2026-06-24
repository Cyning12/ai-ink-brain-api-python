-- Ops Desk P2-5a-ext · LLM 用量 · 缓存指标
-- 应用：Supabase Dashboard → SQL Editor 粘贴执行 / 或 migration 流水线执行一次
-- ALTER ops_runs ADD metrics_json jsonb
-- 可选 view：日 token 汇总 / cache 命中率

-- 1. 新增 metrics_json 列
ALTER TABLE public.ops_runs
ADD COLUMN IF NOT EXISTS metrics_json jsonb;

-- 2. 可选：GIN 索引加速 JSON 查询
CREATE INDEX IF NOT EXISTS idx_ops_runs_metrics_json
ON public.ops_runs USING gin (metrics_json);

-- 3. 可选 view：日 token 汇总
CREATE OR REPLACE VIEW public.ops_v_run_metrics_daily AS
SELECT
    DATE(created_at) AS day,
    COUNT(*) FILTER (WHERE metrics_json IS NOT NULL) AS runs_with_metrics,
    SUM(COALESCE((metrics_json->'llm'->>'total_tokens')::int, 0)) AS total_tokens,
    SUM(COALESCE((metrics_json->'llm'->>'prompt_tokens')::int, 0)) AS prompt_tokens,
    SUM(COALESCE((metrics_json->'llm'->>'completion_tokens')::int, 0)) AS completion_tokens,
    SUM(COALESCE((metrics_json->'llm'->>'latency_ms')::int, 0)) AS total_latency_ms,
    COUNT(*) FILTER (WHERE metrics_json->'cache'->>'hit' = 'true') AS cache_hits,
    COUNT(*) FILTER (WHERE metrics_json->'cache'->>'hit' IS NULL OR metrics_json->'cache'->>'hit' != 'true') AS cache_misses
FROM public.ops_runs
GROUP BY DATE(created_at);

-- 4. 可选 view：按 route 日汇总
CREATE OR REPLACE VIEW public.ops_v_run_metrics_daily_by_route AS
SELECT
    DATE(created_at) AS day,
    route,
    COUNT(*) AS runs,
    SUM(COALESCE((metrics_json->'llm'->>'total_tokens')::int, 0)) AS total_tokens,
    SUM(COALESCE((metrics_json->'llm'->>'latency_ms')::int, 0)) AS total_latency_ms,
    COUNT(*) FILTER (WHERE metrics_json->'cache'->>'hit' = 'true') AS cache_hits
FROM public.ops_runs
GROUP BY DATE(created_at), route;
