-- Ops Desk P1 Demo Cache Rollback

DROP INDEX IF EXISTS public.idx_ops_demo_answers_expires;
DROP INDEX IF EXISTS public.idx_ops_demo_answers_repo;
DROP TABLE IF EXISTS public.ops_demo_answers CASCADE;
