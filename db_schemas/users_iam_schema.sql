-- =====================================================
-- USERS_IAM TABLE SCHEMA
-- =====================================================
-- User authentication and basic information table
-- =====================================================

CREATE TABLE IF NOT EXISTS public.users_iam (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email             TEXT NOT NULL UNIQUE,
  name              TEXT NOT NULL,
  hashed_password   TEXT NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_iam_email ON public.users_iam(email);
CREATE INDEX IF NOT EXISTS idx_users_iam_created_at ON public.users_iam(created_at);

-- Comments
COMMENT ON TABLE public.users_iam IS 'User authentication and basic profile information';
COMMENT ON COLUMN public.users_iam.id IS 'Unique user identifier (UUID)';
COMMENT ON COLUMN public.users_iam.email IS 'User email address (unique)';
COMMENT ON COLUMN public.users_iam.name IS 'User display name';
COMMENT ON COLUMN public.users_iam.hashed_password IS 'Hashed password for authentication';
COMMENT ON COLUMN public.users_iam.created_at IS 'Account creation timestamp';
COMMENT ON COLUMN public.users_iam.updated_at IS 'Last update timestamp';