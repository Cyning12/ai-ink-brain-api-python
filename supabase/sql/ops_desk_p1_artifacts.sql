-- Ops Desk P1-1: Run Artifacts（deep / ReAct 结果落库）
-- 与 ops_run_events 风格保持一致：run_id 外键、jsonb payload、默认 now()

CREATE TABLE IF NOT EXISTS public.ops_run_artifacts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id uuid NOT NULL REFERENCES public.ops_runs(id) ON DELETE CASCADE,
    kind text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (run_id, kind)
);

CREATE INDEX IF NOT EXISTS idx_ops_run_artifacts_run_kind ON public.ops_run_artifacts(run_id, kind);
CREATE INDEX IF NOT EXISTS idx_ops_run_artifacts_created ON public.ops_run_artifacts(created_at);
