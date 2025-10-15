-- =====================================================
-- TASK_TEMPLATES TABLE SCHEMA
-- =====================================================
-- Predefined task templates for mind and body activities
-- =====================================================

CREATE TABLE IF NOT EXISTS public.task_templates (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key                   TEXT NOT NULL UNIQUE,
  name                  TEXT NOT NULL,
  category              TEXT NOT NULL CHECK (category IN ('mind', 'body')),
  estimated_minutes     INTEGER NOT NULL CHECK (estimated_minutes > 0),
  difficulty            INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
  reward_xp             INTEGER NOT NULL DEFAULT 0,
  descr                 TEXT,
  default_params        JSONB DEFAULT '{}'::jsonb,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_task_templates_key ON public.task_templates(key);
CREATE INDEX IF NOT EXISTS idx_task_templates_category ON public.task_templates(category);
CREATE INDEX IF NOT EXISTS idx_task_templates_created_at ON public.task_templates(created_at);

-- Comments
COMMENT ON TABLE public.task_templates IS 'Predefined task templates for mind and body activities';
COMMENT ON COLUMN public.task_templates.key IS 'Unique identifier key for the template';
COMMENT ON COLUMN public.task_templates.name IS 'Display name of the task template';
COMMENT ON COLUMN public.task_templates.category IS 'Category: mind or body';
COMMENT ON COLUMN public.task_templates.estimated_minutes IS 'Estimated duration in minutes';
COMMENT ON COLUMN public.task_templates.difficulty IS 'Difficulty level (1-5)';
COMMENT ON COLUMN public.task_templates.reward_xp IS 'XP reward for completing the task';
COMMENT ON COLUMN public.task_templates.descr IS 'Description of the task template';
COMMENT ON COLUMN public.task_templates.default_params IS 'Default parameters as JSON object';