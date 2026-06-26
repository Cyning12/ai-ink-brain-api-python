-- Ops Desk P3-2a · DB session / invite 鉴权

CREATE TABLE IF NOT EXISTS public.ops_desk_invites (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    label text NOT NULL,
    token_hash text NOT NULL UNIQUE,
    role text NOT NULL CHECK (role IN ('viewer', 'maintainer')),
    expires_at timestamptz,
    revoked_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ops_desk_invites_hash ON public.ops_desk_invites(token_hash);

CREATE TABLE IF NOT EXISTS public.ops_desk_sessions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    role text NOT NULL CHECK (role IN ('viewer', 'maintainer')),
    expires_at timestamptz NOT NULL,
    revoked_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ops_desk_sessions_active ON public.ops_desk_sessions(expires_at)
    WHERE revoked_at IS NULL;
