-- =====================================================
-- IAM BACKEND DATABASE SCHEMA - COMPLETE BACKUP
-- =====================================================
-- This script creates all tables for the IAM Backend system
-- Run this to restore or initialize the complete database
-- =====================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. USERS_IAM - User authentication
-- =====================================================

CREATE TABLE IF NOT EXISTS public.users_iam (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email             TEXT NOT NULL UNIQUE,
  name              TEXT NOT NULL,
  hashed_password   TEXT NOT NULL,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_iam_email ON public.users_iam(email);
CREATE INDEX IF NOT EXISTS idx_users_iam_created_at ON public.users_iam(created_at);

-- =====================================================
-- 2. PROFILES - Extended user profiles
-- =====================================================

CREATE TABLE IF NOT EXISTS public.profiles (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL UNIQUE REFERENCES public.users_iam(id) ON DELETE CASCADE,
  timezone              TEXT NOT NULL DEFAULT 'America/Mexico_City',
  birth_date            DATE,
  gender                TEXT CHECK (gender IN ('male', 'female', 'other', 'prefer_not_to_say')),
  weight_kg             NUMERIC CHECK (weight_kg > 0),
  height_cm             NUMERIC CHECK (height_cm > 0),
  preferred_language    TEXT NOT NULL DEFAULT 'es',
  time_dead             NUMERIC NOT NULL DEFAULT 0,
  day_work              TEXT DEFAULT NULL,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON public.profiles(created_at);

-- =====================================================
-- 3. TASK_TEMPLATES - Predefined task templates
-- =====================================================

CREATE TABLE IF NOT EXISTS public.task_templates (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key                   TEXT NOT NULL UNIQUE,
  name                  TEXT NOT NULL,
  category              TEXT NOT NULL CHECK (category IN ('mind', 'body')),
  estimated_minutes     INTEGER NOT NULL CHECK (estimated_minutes > 0),
  difficulty            INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
  reward_xp             INTEGER NOT NULL DEFAULT 0,
  descr                 TEXT,
  default_params        JSONB DEFAULT '{}'::jsonb,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_task_templates_key ON public.task_templates(key);
CREATE INDEX IF NOT EXISTS idx_task_templates_category ON public.task_templates(category);
CREATE INDEX IF NOT EXISTS idx_task_templates_created_at ON public.task_templates(created_at);

-- =====================================================
-- 4. TASKS_MIND - Mind tasks
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

CREATE INDEX IF NOT EXISTS idx_tasks_mind_user_id ON public.tasks_mind(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_template_id ON public.tasks_mind(template_id);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_status ON public.tasks_mind(status);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_scheduled_at ON public.tasks_mind(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_tasks_mind_created_at ON public.tasks_mind(created_at);

-- =====================================================
-- 5. TASKS_BODY - Body tasks
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

CREATE INDEX IF NOT EXISTS idx_tasks_body_user_id ON public.tasks_body(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_body_template_id ON public.tasks_body(template_id);
CREATE INDEX IF NOT EXISTS idx_tasks_body_status ON public.tasks_body(status);
CREATE INDEX IF NOT EXISTS idx_tasks_body_scheduled_at ON public.tasks_body(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_tasks_body_created_at ON public.tasks_body(created_at);

-- =====================================================
-- 6. GOALS - User goals
-- =====================================================

CREATE TABLE IF NOT EXISTS public.goals (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  title                 TEXT NOT NULL,
  description           TEXT,
  metric_key            TEXT,
  target_value          NUMERIC,
  start_date            DATE NOT NULL,
  end_date              DATE NOT NULL,
  is_active             BOOLEAN NOT NULL DEFAULT TRUE,
  progress              TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_goals_user_id ON public.goals(user_id);
CREATE INDEX IF NOT EXISTS idx_goals_is_active ON public.goals(is_active);
CREATE INDEX IF NOT EXISTS idx_goals_start_date ON public.goals(start_date);
CREATE INDEX IF NOT EXISTS idx_goals_end_date ON public.goals(end_date);

-- =====================================================
-- 7. GOAL_TASKS - Tasks derived from goals
-- =====================================================

CREATE TABLE IF NOT EXISTS public.goal_tasks (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  goal_id           UUID NOT NULL REFERENCES public.goals(id) ON DELETE CASCADE,
  user_id           UUID NOT NULL,
  title             TEXT NOT NULL,
  description       TEXT,
  type              TEXT,
  required          BOOLEAN NOT NULL DEFAULT TRUE,
  weight            NUMERIC NOT NULL DEFAULT 1,
  due_at            TIMESTAMPTZ,
  schedule_rrule    TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_goal_tasks_goal ON public.goal_tasks(goal_id);
CREATE INDEX IF NOT EXISTS idx_goal_tasks_user ON public.goal_tasks(user_id);

-- =====================================================
-- 8. TASK_OCCURRENCES - Goal task occurrences
-- =====================================================

CREATE TABLE IF NOT EXISTS public.task_occurrences (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id         UUID NOT NULL REFERENCES public.goal_tasks(id) ON DELETE CASCADE,
  scheduled_at    TIMESTAMPTZ NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(task_id, scheduled_at)
);

CREATE INDEX IF NOT EXISTS idx_occ_task ON public.task_occurrences(task_id);
CREATE INDEX IF NOT EXISTS idx_occ_time ON public.task_occurrences(scheduled_at);

-- =====================================================
-- 9. TASK_LOGS - Task action logs
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

CREATE INDEX IF NOT EXISTS idx_logs_table_id ON public.task_logs(task_table, task_id);
CREATE INDEX IF NOT EXISTS idx_logs_user ON public.task_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_logs_action ON public.task_logs(action);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON public.task_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_logs_metadata ON public.task_logs USING gin(metadata);

-- =====================================================
-- 10. ACHIEVEMENTS - User achievements
-- =====================================================

CREATE TABLE IF NOT EXISTS public.achievements (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  key                   TEXT NOT NULL,
  title                 TEXT NOT NULL,
  description           TEXT,
  awarded_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, key)
);

CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON public.achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_achievements_key ON public.achievements(key);
CREATE INDEX IF NOT EXISTS idx_achievements_awarded_at ON public.achievements(awarded_at);

-- =====================================================
-- 11. FAILURES - Task failure tracking
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

CREATE INDEX IF NOT EXISTS idx_failures_user_id ON public.failures(user_id);
CREATE INDEX IF NOT EXISTS idx_failures_task_table_id ON public.failures(task_table, task_id);
CREATE INDEX IF NOT EXISTS idx_failures_severity ON public.failures(severity);
CREATE INDEX IF NOT EXISTS idx_failures_created_at ON public.failures(created_at);

-- =====================================================
-- 12. BOT_RULES - AI assistant rules
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

CREATE INDEX IF NOT EXISTS idx_bot_rules_active ON public.bot_rules(active);
CREATE INDEX IF NOT EXISTS idx_bot_rules_priority ON public.bot_rules(priority);
CREATE INDEX IF NOT EXISTS idx_bot_rules_created_at ON public.bot_rules(created_at);

-- =====================================================
-- 13. CHAT_IA_SESSIONS - Chat sessions
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

CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON public.chat_ia_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON public.chat_ia_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_last_message_at ON public.chat_ia_sessions(last_message_at);

-- =====================================================
-- 14. CHAT_IA_MESSAGES - Chat messages
-- =====================================================

CREATE TABLE IF NOT EXISTS public.chat_ia_messages (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id            UUID NOT NULL REFERENCES public.chat_ia_sessions(id) ON DELETE CASCADE,
  role                  TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content               TEXT NOT NULL,
  content_json          JSONB,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON public.chat_ia_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_role ON public.chat_ia_messages(role);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON public.chat_ia_messages(created_at);

-- =====================================================
-- 15. METRIC_CATALOG - Available metrics
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

CREATE INDEX IF NOT EXISTS idx_metric_catalog_domain ON public.metric_catalog(domain);
CREATE INDEX IF NOT EXISTS idx_metric_catalog_created_at ON public.metric_catalog(created_at);

-- =====================================================
-- 16. PERFORMANCE_SNAPSHOTS - Performance data
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

CREATE INDEX IF NOT EXISTS idx_snapshots_user_id ON public.performance_snapshots(user_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_date ON public.performance_snapshots(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON public.performance_snapshots(created_at);

-- =====================================================
-- TRIGGERS AND FUNCTIONS (from goal_tasks_schema.sql)
-- =====================================================

-- Function to update goal progress from logs
CREATE OR REPLACE FUNCTION public.trg_update_goal_progress_from_logs()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE v_goal UUID;
BEGIN
  -- Only react to logs of occurrences
  IF NEW.task_table <> 'task_occurrences' THEN
    RETURN NEW;
  END IF;

  SELECT gt.goal_id INTO v_goal
  FROM public.goal_tasks gt
  JOIN public.task_occurrences oc ON oc.task_id = gt.id
  WHERE oc.id = NEW.task_id
  LIMIT 1;

  IF v_goal IS NOT NULL THEN
    UPDATE public.goals g
    SET progress = v.progress_percent::text
    FROM public.goal_progress_view v
    WHERE v.goal_id = g.id AND g.id = v_goal;
  END IF;

  RETURN NEW;
END $$;

-- View for goal progress calculation
CREATE OR REPLACE VIEW public.goal_progress_view AS
WITH occ_logs AS (
  SELECT
    g.id                                  AS goal_id,
    gt.id                                 AS task_id,
    o.id                                  AS occurrence_id,
    (array_agg(l.action ORDER BY l."timestamp" DESC))[1] AS last_action,
    (array_agg( (l.metadata->>'value')::numeric
                ORDER BY l."timestamp" DESC))[1]         AS last_value
  FROM public.goals g
  JOIN public.goal_tasks gt ON gt.goal_id = g.id
  LEFT JOIN public.task_occurrences o ON o.task_id = gt.id
  LEFT JOIN public.task_logs l
    ON l.task_table = 'task_occurrences' AND l.task_id = o.id
  GROUP BY g.id, gt.id, o.id
), agg AS (
  SELECT
    goal_id,
    SUM(
      CASE
        WHEN last_action IN ('completed','skipped') THEN
          COALESCE(last_value, 1)
        ELSE 0
      END
    ) AS contributed,
    AVG(CASE WHEN last_action = 'completed' THEN 1.0 ELSE 0.0 END) AS pct_completed
  FROM occ_logs
  GROUP BY goal_id
)
SELECT
  g.id AS goal_id,
  CASE
    WHEN COALESCE(g.target_value,0) > 0 THEN
      LEAST(100, 100 * COALESCE(a.contributed,0) / NULLIF(g.target_value,0))
    ELSE
      100 * COALESCE(a.pct_completed,0)
  END::numeric AS progress_percent
FROM public.goals g
LEFT JOIN agg a ON a.goal_id = g.id;

-- Trigger for automatic progress updates
DROP TRIGGER IF EXISTS task_logs_progress_trg ON public.task_logs;
CREATE TRIGGER task_logs_progress_trg
AFTER INSERT ON public.task_logs
FOR EACH ROW
EXECUTE FUNCTION public.trg_update_goal_progress_from_logs();

-- =====================================================
-- SCHEMA CREATION COMPLETE
-- =====================================================