-- =====================================================
-- BOT_RULES TABLE MIGRATION
-- =====================================================
-- Add id_task column to bot_rules table
-- =====================================================

-- Add the new column
ALTER TABLE public.bot_rules ADD COLUMN IF NOT EXISTS id_task UUID;

-- Add index for performance when filtering/joining by id_task
CREATE INDEX IF NOT EXISTS idx_bot_rules_id_task ON public.bot_rules(id_task);

-- Add comment
COMMENT ON COLUMN public.bot_rules.id_task IS 'Reference to the task template or task ID associated with this rule';
