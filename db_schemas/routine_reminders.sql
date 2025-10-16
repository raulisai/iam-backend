-- =====================================================
-- ROUTINE_REMINDERS TABLE SCHEMA
-- =====================================================
-- Recordatorios que se envían N veces al día
-- =====================================================

CREATE TABLE IF NOT EXISTS public.routine_reminders (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  
  -- Información básica
  name                  TEXT NOT NULL,
  description           TEXT,
  
  -- Vinculación con el sistema existente
  source_type           TEXT CHECK (source_type IN ('mind', 'body', 'goal', 'custom')),
  task_id               TEXT ,
  
  -- Configuración de frecuencia
  times_per_day         INTEGER NOT NULL CHECK (times_per_day > 0 AND times_per_day <= 24),
  
  -- Ventana de tiempo (opcional)
  -- Si no se especifica, usa 8:00 AM - 10:00 PM
  start_time            TIME DEFAULT '08:00',
  end_time              TIME DEFAULT '22:00',
  
  -- Días de la semana
  -- Array: 0=Domingo, 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes, 6=Sábado
  days_of_week          INTEGER[] NOT NULL DEFAULT ARRAY[1,2,3,4,5], -- Lunes a Viernes por defecto
  
  -- Contenido de la notificación
  notification_title    TEXT NOT NULL,
  notification_body     TEXT NOT NULL,
  notification_icon     TEXT,
  notification_color    TEXT,
  
  -- Configuración adicional
  sound_enabled         BOOLEAN NOT NULL DEFAULT TRUE,
  vibration_enabled     BOOLEAN NOT NULL DEFAULT TRUE,
  priority              TEXT NOT NULL DEFAULT 'default' CHECK (priority IN ('min', 'low', 'default', 'high', 'max')),
  
  -- Estado
  is_active             BOOLEAN NOT NULL DEFAULT TRUE,
  
  -- Auditoría
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_routine_reminders_user_id ON public.routine_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_routine_reminders_is_active ON public.routine_reminders(is_active);
CREATE INDEX IF NOT EXISTS idx_routine_reminders_times_per_day ON public.routine_reminders(times_per_day);
CREATE INDEX IF NOT EXISTS idx_routine_reminders_source_type ON public.routine_reminders(source_type);
CREATE INDEX IF NOT EXISTS idx_routine_reminders_created_at ON public.routine_reminders(created_at);

-- Comentarios
COMMENT ON TABLE public.routine_reminders IS 'Recordatorios que se distribuyen N veces durante el día';
COMMENT ON COLUMN public.routine_reminders.times_per_day IS 'Cantidad de veces que se envía el recordatorio por día';
COMMENT ON COLUMN public.routine_reminders.start_time IS 'Hora de inicio de la ventana de recordatorios';
COMMENT ON COLUMN public.routine_reminders.end_time IS 'Hora de fin de la ventana de recordatorios';
COMMENT ON COLUMN public.routine_reminders.days_of_week IS 'Días activos: 0=Dom, 1=Lun, 2=Mar, 3=Mié, 4=Jue, 5=Vie, 6=Sáb';
COMMENT ON COLUMN public.routine_reminders.priority IS 'Prioridad de la notificación: min, low, default, high, max';
COMMENT ON COLUMN public.routine_reminders.source_type IS 'Tipo de origen: mind (tarea mental), body (tarea física), goal (meta), custom (personalizado)';
COMMENT ON COLUMN public.routine_reminders.task_id IS 'Plantilla de tarea asociada (si aplica)';
