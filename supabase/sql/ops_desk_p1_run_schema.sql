-- Ops Desk P1 Run / Event / Checkpoint 数据层
-- 取代 R3 ops_analysis_jobs 对外命名；主实体 ops_runs + 追加式 ops_run_events

-- ops_runs：一次 Chat 问答 / 深析 Run
CREATE TABLE IF NOT EXISTS public.ops_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id uuid NOT NULL REFERENCES public.ops_repos(id) ON DELETE CASCADE,
    session_id text,
    query text NOT NULL,
    route text NOT NULL CHECK (route IN ('fast','deep')),
    status text NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','running','done','failed','partial')),
    final_answer jsonb,
    retry_token uuid DEFAULT gen_random_uuid(),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ops_runs_repo_created ON public.ops_runs(repo_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ops_runs_session ON public.ops_runs(session_id);
CREATE INDEX IF NOT EXISTS idx_ops_runs_status ON public.ops_runs(status);

-- ops_run_events：可观测时间线，同一 run 内 seq 严格递增
CREATE TABLE IF NOT EXISTS public.ops_run_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id uuid NOT NULL REFERENCES public.ops_runs(id) ON DELETE CASCADE,
    seq int NOT NULL,
    ts_ms bigint NOT NULL,
    node_id text,
    agent_role text NOT NULL,
    event_type text NOT NULL,
    payload jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (run_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_ops_run_events_run_seq ON public.ops_run_events(run_id, seq);
CREATE INDEX IF NOT EXISTS idx_ops_run_events_run_created ON public.ops_run_events(run_id, created_at);

-- ops_run_checkpoints：P1-b LangGraph checkpointer 预留
CREATE TABLE IF NOT EXISTS public.ops_run_checkpoints (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id uuid NOT NULL REFERENCES public.ops_runs(id) ON DELETE CASCADE,
    checkpoint_id text NOT NULL,
    state_json jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (run_id, checkpoint_id)
);

CREATE INDEX IF NOT EXISTS idx_ops_run_checkpoints_run ON public.ops_run_checkpoints(run_id, checkpoint_id);
