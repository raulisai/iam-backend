-- =====================================================
-- PROFILES TABLE SCHEMA
-- =====================================================
-- Extended user profile information
-- =====================================================

CREATE TABLE IF NOT EXISTS public.profiles (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL UNIQUE REFERENCES public.users_iam(id) ON DELETE CASCADE,
  timezone              TEXT NOT NULL DEFAULT 'America/Mexico_City',
  birth_date            DATE,
  gender                TEXT CHECK (gender IN ('male', 'female', 'other', 'prefer_not_to_say')),
  weight_kg             NUMERIC CHECK (weight_kg > 0),
  height_cm             NUMERIC CHECK (height_cm > 0),
  preferred_language    TEXT NOT NULL DEFAULT 'es',
  time_dead             NUMERIC NOT NULL DEFAULT 0,
  day_work              TEXT DEFAULT NULL,
  goal_points_target    NUMERIC NOT NULL DEFAULT 0 CHECK (goal_points_target >= 0),
  goal_points_earned    NUMERIC NOT NULL DEFAULT 0 CHECK (goal_points_earned >= 0),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON public.profiles(created_at);

-- Comments
COMMENT ON TABLE public.profiles IS 'Extended user profile information and preferences';
COMMENT ON COLUMN public.profiles.user_id IS 'Reference to users_iam table (unique per user)';
COMMENT ON COLUMN public.profiles.timezone IS 'User timezone (IANA format)';
COMMENT ON COLUMN public.profiles.birth_date IS 'User birth date';
COMMENT ON COLUMN public.profiles.gender IS 'User gender preference';
COMMENT ON COLUMN public.profiles.weight_kg IS 'User weight in kilograms';
COMMENT ON COLUMN public.profiles.height_cm IS 'User height in centimeters';
COMMENT ON COLUMN public.profiles.preferred_language IS 'User preferred language code';
COMMENT ON COLUMN public.profiles.time_dead IS 'Time dead or unproductive time tracked';
COMMENT ON COLUMN public.profiles.day_work IS 'Work days in the week (D,L,M,M,J,V,S format)';
COMMENT ON COLUMN public.profiles.goal_points_target IS 'Total points available from all active goals and tasks';
COMMENT ON COLUMN public.profiles.goal_points_earned IS 'Points earned from completed tasks';
