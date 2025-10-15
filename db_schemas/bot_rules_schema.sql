-- =====================================================
-- BOT_RULES TABLE SCHEMA
-- =====================================================
-- Automated rules for the AI assistant
-- =====================================================

CREATE TABLE IF NOT EXISTS public.bot_rules (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name                  TEXT NOT NULL,
  condition             JSONB NOT NULL DEFAULT '{}'::jsonb,
  action                JSONB NOT NULL DEFAULT '{}'::jsonb,
  priority              INTEGER NOT NULL DEFAULT 10,
  active                BOOLEAN NOT NULL DEFAULT TRUE,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_bot_rules_active ON public.bot_rules(active);
CREATE INDEX IF NOT EXISTS idx_bot_rules_priority ON public.bot_rules(priority);
CREATE INDEX IF NOT EXISTS idx_bot_rules_created_at ON public.bot_rules(created_at);

-- Comments
COMMENT ON TABLE public.bot_rules IS 'Automated rules for the AI assistant';
COMMENT ON COLUMN public.bot_rules.name IS 'Human-readable name for the rule';
COMMENT ON COLUMN public.bot_rules.condition IS 'Condition that triggers the rule as JSON';
COMMENT ON COLUMN public.bot_rules.action IS 'Action to perform when condition is met as JSON';
COMMENT ON COLUMN public.bot_rules.priority IS 'Rule priority (higher numbers = higher priority)';
COMMENT ON COLUMN public.bot_rules.active IS 'Whether the rule is active';