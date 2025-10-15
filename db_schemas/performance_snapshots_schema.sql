-- =====================================================
-- PERFORMANCE_SNAPSHOTS TABLE SCHEMA
-- =====================================================
-- Historical snapshots of user performance metrics
-- =====================================================

CREATE TABLE IF NOT EXISTS public.performance_snapshots (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  snapshot_date         DATE NOT NULL,
  metrics               JSONB NOT NULL DEFAULT '{}'::jsonb,
  notes                 TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, snapshot_date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_snapshots_user_id ON public.performance_snapshots(user_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_date ON public.performance_snapshots(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON public.performance_snapshots(created_at);

-- Comments
COMMENT ON TABLE public.performance_snapshots IS 'Historical snapshots of user performance metrics';
COMMENT ON COLUMN public.performance_snapshots.user_id IS 'User who owns the snapshot';
COMMENT ON COLUMN public.performance_snapshots.snapshot_date IS 'Date of the performance snapshot';
COMMENT ON COLUMN public.performance_snapshots.metrics IS 'Metrics data as JSON object';
COMMENT ON COLUMN public.performance_snapshots.notes IS 'Optional notes about the snapshot';