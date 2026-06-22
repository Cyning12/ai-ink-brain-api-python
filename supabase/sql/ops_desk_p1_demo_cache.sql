-- Ops Desk P1 Demo Cache
-- 支撑面试 Demo 与 LLM 断联兜底：D1-D3 预计算 / D4 首次深析后缓存 24h

CREATE TABLE IF NOT EXISTS public.ops_demo_answers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id uuid NOT NULL REFERENCES public.ops_repos(id) ON DELETE CASCADE,
    demo_id text NOT NULL,
    query_template text NOT NULL,
    params jsonb DEFAULT '{}',
    answer_json jsonb NOT NULL,
    source_sync_run_id uuid REFERENCES public.ops_sync_runs(id) ON DELETE SET NULL,
    expires_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (repo_id, demo_id)
);

CREATE INDEX IF NOT EXISTS idx_ops_demo_answers_repo ON public.ops_demo_answers(repo_id, demo_id);
CREATE INDEX IF NOT EXISTS idx_ops_demo_answers_expires ON public.ops_demo_answers(expires_at);

-- 预置 P1 最小 4 题 D1-D4；实际数值由首次请求或 sync 后预计算覆盖
INSERT INTO public.ops_demo_answers (
    repo_id,
    demo_id,
    query_template,
    params,
    answer_json,
    expires_at
)
SELECT
    id,
    demo.demo_id,
    demo.query_template,
    demo.params,
    demo.answer_json,
    now() + interval '25 hours'
FROM public.ops_repos,
    (VALUES
        ('D1', 'kimi-code 最近 30 天 open issue 有多少？', '{"days": 30}'::jsonb, '{"answer": "最近 30 天 closed issue 共 -- 个，平均每天 -- 个。", "metric": "issue-throughput", "days": 30}'::jsonb),
        ('D2', 'PR cycle time 最近 30 天趋势如何？', '{"days": 30}'::jsonb, '{"answer": "最近 30 天 PR cycle time 平均 -- 小时。", "metric": "cycle-time", "days": 30}'::jsonb),
        ('D3', 'PR review time 中位数是多少？', '{"days": 30}'::jsonb, '{"answer": "最近 30 天 PR review time 中位数 -- 小时。", "metric": "review-time", "days": 30}'::jsonb),
        ('D4', '#545 适合我做吗？', '{"issue_number": 545}'::jsonb, '{"answer": "#545 尚在分析中，首次请求后将写入完整分析结果。", "issue_number": 545}'::jsonb)
    ) AS demo(demo_id, query_template, params, answer_json)
WHERE owner = 'MoonshotAI' AND name = 'kimi-code'
ON CONFLICT (repo_id, demo_id) DO NOTHING;
