-- Ops Desk P3-2a · 清空全部 invite / session（运维 · 不可逆）
-- 用法：Supabase SQL Editor 执行 · 执行前确认无生产访客依赖旧 invite

-- 先删 session（使所有已登录 Cookie 失效）
DELETE FROM public.ops_desk_sessions;

-- 再删 invite（所有登录秘钥 hash）
DELETE FROM public.ops_desk_invites;

-- 可选：确认已空
-- SELECT count(*) FROM public.ops_desk_invites;
-- SELECT count(*) FROM public.ops_desk_sessions;
