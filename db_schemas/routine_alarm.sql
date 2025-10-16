-- =====================================================
-- ROUTINE_ALARMS TABLE SCHEMA
-- =====================================================
-- Alarmas que se disparan a una hora específica
-- =====================================================

CREATE TABLE IF NOT EXISTS public.routine_alarms (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID NOT NULL REFERENCES public.users_iam(id) ON DELETE CASCADE,
  
  -- Información básica
  name                  TEXT NOT NULL,
  description           TEXT,
  
  -- Vinculación con el sistema existente
  source_type           TEXT CHECK (source_type IN ('mind', 'body', 'goal', 'custom')),
  task_id      TEXT,
  
  -- Configuración de horario
  alarm_time            TIME NOT NULL,
  
  -- Días de la semana
  -- Array: 0=Domingo, 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes, 6=Sábado
  days_of_week          INTEGER[] NOT NULL DEFAULT ARRAY[1,2,3,4,5], -- Lunes a Viernes por defecto
  
  -- Contenido de la notificación
  notification_title    TEXT NOT NULL,
  notification_body     TEXT NOT NULL,
  notification_icon     TEXT,
  notification_color    TEXT,
  
  -- Configuración de alarma
  sound_enabled         BOOLEAN NOT NULL DEFAULT TRUE,
  sound_uri             TEXT, -- URI del sonido personalizado
  vibration_enabled     BOOLEAN NOT NULL DEFAULT TRUE,
  vibration_pattern     INTEGER[], -- Patrón de vibración [300, 200, 300]
  
  -- Configuración de snooze
  snooze_enabled        BOOLEAN NOT NULL DEFAULT TRUE,
  snooze_duration_min   INTEGER DEFAULT 10 CHECK (snooze_duration_min > 0),
  max_snoozes           INTEGER DEFAULT 3 CHECK (max_snoozes >= 0),
  
  -- Configuración adicional
  priority              TEXT NOT NULL DEFAULT 'max' CHECK (priority IN ('min', 'low', 'default', 'high', 'max')),
  can_dismiss           BOOLEAN NOT NULL DEFAULT TRUE,
  auto_dismiss_minutes  INTEGER CHECK (auto_dismiss_minutes > 0),
  
  -- Estado
  is_active             BOOLEAN NOT NULL DEFAULT TRUE,
  
  -- Auditoría
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_routine_alarms_user_id ON public.routine_alarms(user_id);
CREATE INDEX IF NOT EXISTS idx_routine_alarms_is_active ON public.routine_alarms(is_active);
CREATE INDEX IF NOT EXISTS idx_routine_alarms_alarm_time ON public.routine_alarms(alarm_time);
CREATE INDEX IF NOT EXISTS idx_routine_alarms_source_type ON public.routine_alarms(source_type);
CREATE INDEX IF NOT EXISTS idx_routine_alarms_created_at ON public.routine_alarms(created_at);

-- Índice compuesto para búsqueda eficiente
CREATE INDEX IF NOT EXISTS idx_routine_alarms_active_time 
ON public.routine_alarms(is_active, alarm_time) WHERE is_active = TRUE;

-- Comentarios
COMMENT ON TABLE public.routine_alarms IS 'Alarmas programadas para una hora específica del día';
COMMENT ON COLUMN public.routine_alarms.alarm_time IS 'Hora exacta en que se dispara la alarma';
COMMENT ON COLUMN public.routine_alarms.days_of_week IS 'Días activos: 0=Dom, 1=Lun, 2=Mar, 3=Mié, 4=Jue, 5=Vie, 6=Sáb';
COMMENT ON COLUMN public.routine_alarms.snooze_enabled IS 'Si permite posponer la alarma';
COMMENT ON COLUMN public.routine_alarms.snooze_duration_min IS 'Duración del snooze en minutos';
COMMENT ON COLUMN public.routine_alarms.max_snoozes IS 'Número máximo de veces que se puede posponer';
COMMENT ON COLUMN public.routine_alarms.vibration_pattern IS 'Patrón de vibración en milisegundos: [vibrar, pausa, vibrar, ...]';
COMMENT ON COLUMN public.routine_alarms.auto_dismiss_minutes IS 'Minutos después de los cuales se descarta automáticamente';
COMMENT ON COLUMN public.routine_alarms.source_type IS 'Tipo de origen: mind (tarea mental), body (tarea física), goal (meta), custom (personalizado)';
COMMENT ON COLUMN public.routine_alarms.task_id IS 'Plantilla de tarea asociada (si aplica)';
