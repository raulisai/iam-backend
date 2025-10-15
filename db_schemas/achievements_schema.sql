-- =====================================================
-- ACHIEVEMENTS TABLE SCHEMA
-- =====================================================
-- User achievements and badges
-- =====================================================

CREATE TABLE IF NOT EXISTS public.achievements (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  key                   TEXT NOT NULL,
  title                 TEXT NOT NULL,
  description           TEXT,
  awarded_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, key)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON public.achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_achievements_key ON public.achievements(key);
CREATE INDEX IF NOT EXISTS idx_achievements_awarded_at ON public.achievements(awarded_at);

-- Comments
COMMENT ON TABLE public.achievements IS 'User achievements and badges';
COMMENT ON COLUMN public.achievements.user_id IS 'User who earned the achievement';
COMMENT ON COLUMN public.achievements.key IS 'Unique key identifying the achievement type';
COMMENT ON COLUMN public.achievements.title IS 'Display title of the achievement';
COMMENT ON COLUMN public.achievements.description IS 'Description of the achievement';
COMMENT ON COLUMN public.achievements.awarded_at IS 'When the achievement was awarded';