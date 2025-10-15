-- =====================================================
-- CHAT_IA_SESSIONS TABLE SCHEMA
-- =====================================================
-- Chat sessions with AI assistant
-- =====================================================

CREATE TABLE IF NOT EXISTS public.chat_ia_sessions (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  title                 TEXT,
  model                 TEXT DEFAULT 'gpt-5',
  system_prompt         TEXT,
  last_message_at       TIMESTAMPTZ,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON public.chat_ia_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON public.chat_ia_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_last_message_at ON public.chat_ia_sessions(last_message_at);

-- Comments
COMMENT ON TABLE public.chat_ia_sessions IS 'Chat sessions with AI assistant';
COMMENT ON COLUMN public.chat_ia_sessions.user_id IS 'User who owns the session';
COMMENT ON COLUMN public.chat_ia_sessions.title IS 'Session title';
COMMENT ON COLUMN public.chat_ia_sessions.model IS 'AI model used for the session';
COMMENT ON COLUMN public.chat_ia_sessions.system_prompt IS 'System prompt for the AI';
COMMENT ON COLUMN public.chat_ia_sessions.last_message_at IS 'Timestamp of the last message';