-- =====================================================
-- GOALS TABLE SCHEMA
-- =====================================================
-- User goals and objectives
-- =====================================================

CREATE TABLE IF NOT EXISTS public.goals (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  title                 TEXT NOT NULL,
  description           TEXT,
  metric_key            TEXT,
  target_value          NUMERIC,
  start_date            DATE NOT NULL,
  end_date              DATE NOT NULL,
  is_active             BOOLEAN NOT NULL DEFAULT TRUE,
  progress              TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_goals_user_id ON public.goals(user_id);
CREATE INDEX IF NOT EXISTS idx_goals_is_active ON public.goals(is_active);
CREATE INDEX IF NOT EXISTS idx_goals_start_date ON public.goals(start_date);
CREATE INDEX IF NOT EXISTS idx_goals_end_date ON public.goals(end_date);

-- Comments
COMMENT ON TABLE public.goals IS 'User goals and objectives';
COMMENT ON COLUMN public.goals.user_id IS 'User who owns the goal';
COMMENT ON COLUMN public.goals.title IS 'Goal title';
COMMENT ON COLUMN public.goals.description IS 'Goal description';
COMMENT ON COLUMN public.goals.metric_key IS 'Key for the metric being tracked';
COMMENT ON COLUMN public.goals.target_value IS 'Target value to achieve';
COMMENT ON COLUMN public.goals.start_date IS 'Goal start date';
COMMENT ON COLUMN public.goals.end_date IS 'Goal end date';
COMMENT ON COLUMN public.goals.is_active IS 'Whether the goal is currently active';
COMMENT ON COLUMN public.goals.progress IS 'Current progress as text/percentage';