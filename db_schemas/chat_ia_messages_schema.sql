-- =====================================================
-- CHAT_IA_MESSAGES TABLE SCHEMA
-- =====================================================
-- Individual messages in chat sessions
-- =====================================================

CREATE TABLE IF NOT EXISTS public.chat_ia_messages (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id            UUID NOT NULL REFERENCES public.chat_ia_sessions(id) ON DELETE CASCADE,
  role                  TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content               TEXT NOT NULL,
  content_json          JSONB,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON public.chat_ia_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_role ON public.chat_ia_messages(role);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON public.chat_ia_messages(created_at);

-- Comments
COMMENT ON TABLE public.chat_ia_messages IS 'Individual messages in chat sessions';
COMMENT ON COLUMN public.chat_ia_messages.session_id IS 'Reference to the chat session';
COMMENT ON COLUMN public.chat_ia_messages.role IS 'Message role: user, assistant, or system';
COMMENT ON COLUMN public.chat_ia_messages.content IS 'Message content as text';
COMMENT ON COLUMN public.chat_ia_messages.content_json IS 'Message content as JSON (optional)';