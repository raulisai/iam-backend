-- =====================================================
-- FAILURES TABLE SCHEMA
-- =====================================================
-- Task failure tracking and analysis
-- =====================================================

CREATE TABLE IF NOT EXISTS public.failures (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  task_table            TEXT CHECK (task_table IN ('tasks_mind', 'tasks_body', 'task_occurrences')),
  task_id               UUID,
  reason                TEXT NOT NULL,
  severity              TEXT NOT NULL DEFAULT 'minor' CHECK (severity IN ('minor', 'major', 'critical')),
  notes                 TEXT,
  title                 TEXT,
  root_cause            TEXT,
  prevention            TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_failures_user_id ON public.failures(user_id);
CREATE INDEX IF NOT EXISTS idx_failures_task_table_id ON public.failures(task_table, task_id);
CREATE INDEX IF NOT EXISTS idx_failures_severity ON public.failures(severity);
CREATE INDEX IF NOT EXISTS idx_failures_created_at ON public.failures(created_at);

-- Comments
COMMENT ON TABLE public.failures IS 'Task failure tracking and analysis';
COMMENT ON COLUMN public.failures.user_id IS 'User who experienced the failure';
COMMENT ON COLUMN public.failures.task_table IS 'Table where the failed task is stored';
COMMENT ON COLUMN public.failures.task_id IS 'ID of the failed task';
COMMENT ON COLUMN public.failures.reason IS 'Reason for the failure';
COMMENT ON COLUMN public.failures.severity IS 'Severity level: minor, major, critical';
COMMENT ON COLUMN public.failures.notes IS 'Additional notes about the failure';
COMMENT ON COLUMN public.failures.title IS 'Title or summary of the failure';
COMMENT ON COLUMN public.failures.root_cause IS 'Root cause analysis';
COMMENT ON COLUMN public.failures.prevention IS 'Prevention strategies';