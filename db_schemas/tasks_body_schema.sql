-- =====================================================
-- TASKS_BODY TABLE SCHEMA
-- =====================================================
-- Body tasks created by users
-- =====================================================

CREATE TABLE IF NOT EXISTS public.tasks_body (
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
CREATE INDEX IF NOT EXISTS idx_tasks_body_user_id ON public.tasks_body(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_body_template_id ON public.tasks_body(template_id);
CREATE INDEX IF NOT EXISTS idx_tasks_body_status ON public.tasks_body(status);
CREATE INDEX IF NOT EXISTS idx_tasks_body_scheduled_at ON public.tasks_body(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_tasks_body_created_at ON public.tasks_body(created_at);

-- Comments
COMMENT ON TABLE public.tasks_body IS 'Body tasks created by users';
COMMENT ON COLUMN public.tasks_body.template_id IS 'Reference to task template (optional)';
COMMENT ON COLUMN public.tasks_body.user_id IS 'User who owns the task';
COMMENT ON COLUMN public.tasks_body.created_by IS 'Who created the task (user or system)';
COMMENT ON COLUMN public.tasks_body.status IS 'Task status: pending, completed, cancelled';
COMMENT ON COLUMN public.tasks_body.scheduled_at IS 'When the task is scheduled';
COMMENT ON COLUMN public.tasks_body.completed_at IS 'When the task was completed';
COMMENT ON COLUMN public.tasks_body.params IS 'Task-specific parameters as JSON';