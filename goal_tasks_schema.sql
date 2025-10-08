-- =====================================================
-- GOAL TASKS SYSTEM - Database Schema
-- =====================================================
-- Este script crea las tablas necesarias para el sistema
-- de tareas derivadas de goals con cálculo automático
-- de progreso.
-- =====================================================

-- === BASE MÍNIMA ===

-- 1) Tareas ligadas a un goal
CREATE TABLE IF NOT EXISTS public.goal_tasks (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  goal_id           UUID NOT NULL REFERENCES public.goals(id) ON DELETE CASCADE,
  user_id           UUID NOT NULL,                 -- dueño
  title             TEXT NOT NULL,
  description       TEXT,
  type              TEXT,                          -- 'mind' | 'body' | 'habit' | 'one_off'...
  required          BOOLEAN NOT NULL DEFAULT TRUE, -- cuenta para el progreso
  weight            NUMERIC NOT NULL DEFAULT 1,    -- ponderación
  due_at            TIMESTAMPTZ,                   -- para tareas puntuales
  schedule_rrule    TEXT,                          -- para recurrentes (opcional)
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_goal_tasks_goal ON public.goal_tasks(goal_id);
CREATE INDEX IF NOT EXISTS idx_goal_tasks_user ON public.goal_tasks(user_id);

-- 2) Ocurrencias (instancias concretas de ejecución)
CREATE TABLE IF NOT EXISTS public.task_occurrences (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id         UUID NOT NULL REFERENCES public.goal_tasks(id) ON DELETE CASCADE,
  scheduled_at    TIMESTAMPTZ NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(task_id, scheduled_at)
);

CREATE INDEX IF NOT EXISTS idx_occ_task ON public.task_occurrences(task_id);
CREATE INDEX IF NOT EXISTS idx_occ_time ON public.task_occurrences(scheduled_at);

-- 3) (Opcional pero útil) Asegura columnas/índices mínimos en tu task_logs
--    ESTRUCTURA dada por ti:
--    task_logs(id uuid, task_table text, task_id uuid, user_id uuid,
--              action text, "timestamp" timestamptz, metadata jsonb)
ALTER TABLE public.task_logs
  ALTER COLUMN id SET DEFAULT gen_random_uuid(),
  ALTER COLUMN metadata SET DEFAULT '{}'::jsonb;

CREATE INDEX IF NOT EXISTS idx_logs_table_id   ON public.task_logs(task_table, task_id);
CREATE INDEX IF NOT EXISTS idx_logs_user       ON public.task_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_logs_action     ON public.task_logs(action);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp  ON public.task_logs("timestamp");
CREATE INDEX IF NOT EXISTS idx_logs_metadata   ON public.task_logs USING gin(metadata);

-- === PROGRESO SIMPLE ===
-- Regla: si goals.target_value > 0 => suma de metadata.value en logs
--        (o 1 por 'completed' si no hay value) / target_value * 100
--        si no hay target_value => % de ocurrencias completed.

CREATE OR REPLACE VIEW public.goal_progress_view AS
WITH occ_logs AS (
  SELECT
    g.id                                  AS goal_id,
    gt.id                                 AS task_id,
    o.id                                  AS occurrence_id,
    -- último estado por ocurrencia
    (array_agg(l.action ORDER BY l."timestamp" DESC))[1] AS last_action,
    -- último valor numérico registrado
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
          COALESCE(last_value, 1)                    -- usa value si hay, si no vale 1
        ELSE 0
      END
    ) AS contributed,                                -- aporte total
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

-- Escribe el progreso en goals.progress cuando haya nuevos logs
CREATE OR REPLACE FUNCTION public.trg_update_goal_progress_from_logs()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE v_goal UUID;
BEGIN
  -- Sólo reaccionamos a logs de ocurrencias
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

DROP TRIGGER IF EXISTS task_logs_progress_trg ON public.task_logs;
CREATE TRIGGER task_logs_progress_trg
AFTER INSERT ON public.task_logs
FOR EACH ROW
EXECUTE FUNCTION public.trg_update_goal_progress_from_logs();

-- =====================================================
-- COMENTARIOS Y NOTAS
-- =====================================================

COMMENT ON TABLE public.goal_tasks IS 
'Tareas específicas derivadas de goals. Pueden ser puntuales (due_at) o recurrentes (schedule_rrule)';

COMMENT ON COLUMN public.goal_tasks.required IS 
'Si TRUE, esta tarea cuenta para el cálculo de progreso del goal';

COMMENT ON COLUMN public.goal_tasks.weight IS 
'Ponderación de la tarea en el cálculo de progreso (default: 1)';

COMMENT ON COLUMN public.goal_tasks.schedule_rrule IS 
'Regla de recurrencia RFC 5545 (ej: FREQ=DAILY;BYHOUR=8) para tareas recurrentes';

COMMENT ON TABLE public.task_occurrences IS 
'Instancias concretas de ejecución de una goal_task. Para tareas recurrentes, se genera una ocurrencia por fecha';

COMMENT ON VIEW public.goal_progress_view IS 
'Vista que calcula el progreso de cada goal basándose en logs de sus ocurrencias';

COMMENT ON FUNCTION public.trg_update_goal_progress_from_logs() IS 
'Trigger que actualiza automáticamente goals.progress cuando se registra un log en task_occurrences';
