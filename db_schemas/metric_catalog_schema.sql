-- =====================================================
-- METRIC_CATALOG TABLE SCHEMA
-- =====================================================
-- Catalog of available metrics for tracking
-- =====================================================

CREATE TABLE IF NOT EXISTS public.metric_catalog (
  metric_key            TEXT PRIMARY KEY,
  domain                TEXT NOT NULL CHECK (domain IN ('body', 'mind', 'system')),
  display_name          TEXT NOT NULL,
  description           TEXT,
  unit                  TEXT,
  agg_method            TEXT CHECK (agg_method IN ('sum', 'avg', 'min', 'max', 'last')),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_metric_catalog_domain ON public.metric_catalog(domain);
CREATE INDEX IF NOT EXISTS idx_metric_catalog_created_at ON public.metric_catalog(created_at);

-- Comments
COMMENT ON TABLE public.metric_catalog IS 'Catalog of available metrics for tracking';
COMMENT ON COLUMN public.metric_catalog.metric_key IS 'Unique key identifying the metric';
COMMENT ON COLUMN public.metric_catalog.domain IS 'Domain: body, mind, or system';
COMMENT ON COLUMN public.metric_catalog.display_name IS 'Human-readable name';
COMMENT ON COLUMN public.metric_catalog.description IS 'Description of what the metric measures';
COMMENT ON COLUMN public.metric_catalog.unit IS 'Unit of measurement (e.g., minutes, count)';
COMMENT ON COLUMN public.metric_catalog.agg_method IS 'Aggregation method: sum, avg, min, max, last';