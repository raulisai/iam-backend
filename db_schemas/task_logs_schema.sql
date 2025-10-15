-- =====================================================
-- TASK_LOGS TABLE SCHEMA
-- =====================================================
-- Audit log for task actions and events
-- =====================================================

CREATE TABLE IF NOT EXISTS public.task_logs (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_table            TEXT NOT NULL CHECK (task_table IN ('tasks_mind', 'tasks_body', 'task_occurrences')),
  task_id               UUID NOT NULL,
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  action                TEXT NOT NULL,
  timestamp             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata              JSONB DEFAULT '{}'::jsonb
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_logs_table_id ON public.task_logs(task_table, task_id);
CREATE INDEX IF NOT EXISTS idx_logs_user ON public.task_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_logs_action ON public.task_logs(action);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON public.task_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_logs_metadata ON public.task_logs USING gin(metadata);

-- Comments
COMMENT ON TABLE public.task_logs IS 'Audit log for task actions and events';
COMMENT ON COLUMN public.task_logs.task_table IS 'Table name where the task is stored';
COMMENT ON COLUMN public.task_logs.task_id IS 'ID of the task in the referenced table';
COMMENT ON COLUMN public.task_logs.user_id IS 'User who performed the action';
COMMENT ON COLUMN public.task_logs.action IS 'Action performed (e.g., completed, started, skipped)';
COMMENT ON COLUMN public.task_logs.timestamp IS 'When the action occurred';
COMMENT ON COLUMN public.task_logs.metadata IS 'Additional metadata as JSON';