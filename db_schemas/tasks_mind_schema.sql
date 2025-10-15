-- =====================================================
-- TASKS_MIND TABLE SCHEMA
-- =====================================================
-- Mind tasks created by users
-- =====================================================

CREATE TABLE IF NOT EXISTS public.tasks_mind (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_id           UUID REFERENCES public.task_templates(id) ON DELETE SET NULL,
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  created_by            TEXT NOT NULL,
  status                TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'cancelled')),
  scheduled_at          TIMESTAMPTZ,
  completed_at          TIMESTAMPTZ,
  params                JSONB DEFAULT '{}'::jsonb,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tasks_mind_user_id ON public.tasks_mind(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_template_id ON public.tasks_mind(template_id);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_status ON public.tasks_mind(status);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_scheduled_at ON public.tasks_mind(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_created_at ON public.tasks_mind(created_at);

-- Comments
COMMENT ON TABLE public.tasks_mind IS 'Mind tasks created by users';
COMMENT ON COLUMN public.tasks_mind.template_id IS 'Reference to task template (optional)';
COMMENT ON COLUMN public.tasks_mind.user_id IS 'User who owns the task';
COMMENT ON COLUMN public.tasks_mind.created_by IS 'Who created the task (user or system)';
COMMENT ON COLUMN public.tasks_mind.status IS 'Task status: pending, completed, cancelled';
COMMENT ON COLUMN public.tasks_mind.scheduled_at IS 'When the task is scheduled';
COMMENT ON COLUMN public.tasks_mind.completed_at IS 'When the task was completed';
COMMENT ON COLUMN public.tasks_mind.params IS 'Task-specific parameters as JSON';