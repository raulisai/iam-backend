# Arquitectura del Sistema de Automatización

## 🏗️ Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Actions                            │
│                   (Ejecuta cada hora: 0 * * * *)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   scripts/run_automation.py                      │
│                    (Script Principal)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              automation/scheduler.py                             │
│                  (Orquestador)                                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  run_hourly_tasks()                                      │  │
│  │  ├─ Cada hora: Notificaciones + Métricas                │  │
│  │  ├─ 23:00: Scores + Resúmenes                           │  │
│  │  └─ Domingo 00:00: Limpieza + Reportes                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└───┬─────────────┬─────────────┬──────────────┬─────────────────┘
    │             │             │              │
    ▼             ▼             ▼              ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐
│ Score   │ │Notifica- │ │ Metrics  │ │   Supabase     │
│Calcula- │ │tion      │ │ Updater  │ │   Database     │
│tor      │ │Sender    │ │          │ │                │
└────┬────┘ └────┬─────┘ └────┬─────┘ └────────┬───────┘
     │           │             │                │
     │           │             │                │
     └───────────┴─────────────┴────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │   Firebase Cloud Messaging    │
         │   (Notificaciones Push)       │
         └───────────────┬───────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Usuarios  │
                  │  (Devices)  │
                  └─────────────┘
```

## 🔄 Flujo de Datos

### 1. Flujo Horario (Cada Hora)

```
GitHub Actions (Cron)
    │
    ├─> Instalar Python + Dependencias
    │
    ├─> Cargar Variables de Entorno (Secrets)
    │
    └─> Ejecutar run_automation.py
            │
            └─> AutomationScheduler.run_hourly_tasks()
                    │
                    ├─> NotificationSender.send_scheduled_notifications()
                    │       │
                    │       ├─> Consultar routine_alarms (activas)
                    │       ├─> Consultar routine_reminders (activas)
                    │       ├─> Verificar hora y día actual
                    │       ├─> Obtener device_tokens del usuario
                    │       └─> Enviar via Firebase FCM
                    │
                    └─> MetricsUpdater.update_all_metrics()
                            │
                            ├─> Consultar tasks_body (completadas/pendientes)
                            ├─> Consultar tasks_mind (completadas/pendientes)
                            ├─> Calcular tasas de completación
                            └─> Guardar en performance_snapshots
```

### 2. Flujo de Fin de Día (23:00)

```
AutomationScheduler.run_hourly_tasks()
    │
    ├─> ScoreCalculator.calculate_daily_scores()
    │       │
    │       ├─> Obtener todos los usuarios activos
    │       │
    │       └─> Para cada usuario:
    │               ├─> Contar tareas Body incompletas
    │               ├─> Contar tareas Mind incompletas
    │               ├─> Contar alarmas perdidas
    │               ├─> Calcular penalizaciones
    │               ├─> Actualizar scores (min: 0)
    │               └─> Guardar en performance_snapshots
    │
    └─> NotificationSender.send_daily_summary()
            │
            └─> Para cada usuario:
                    ├─> Obtener snapshot del día
                    ├─> Generar resumen de texto
                    └─> Enviar notificación
```

### 3. Flujo Semanal (Domingo 00:00)

```
AutomationScheduler.run_hourly_tasks()
    │
    ├─> MetricsUpdater.cleanup_old_snapshots()
    │       │
    │       └─> Eliminar snapshots > 90 días
    │
    └─> MetricsUpdater.generate_weekly_report()
            │
            └─> Para cada usuario:
                    ├─> Obtener snapshots de últimos 7 días
                    ├─> Calcular totales y promedios
                    └─> Guardar reporte
```

## 📊 Modelo de Datos

### Tablas Principales

```
┌─────────────────┐
│   users_iam     │
│─────────────────│
│ id (PK)         │
│ email           │
│ created_at      │
└────────┬────────┘
         │
         │ 1:1
         ▼
┌─────────────────┐
│    profiles     │
│─────────────────│
│ id (PK)         │
│ user_id (FK)    │
│ timezone        │
│ birth_date      │
└────────┬────────┘
         │
         │ 1:N
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌─────────────────┐              ┌─────────────────┐
│   tasks_body    │              │   tasks_mind    │
│─────────────────│              │─────────────────│
│ id (PK)         │              │ id (PK)         │
│ user_id (FK)    │              │ user_id (FK)    │
│ status          │              │ status          │
│ scheduled_at    │              │ scheduled_at    │
│ completed_at    │              │ completed_at    │
└─────────────────┘              └─────────────────┘

         │
         │ 1:N
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌─────────────────┐              ┌─────────────────┐
│ routine_alarms  │              │routine_reminders│
│─────────────────│              │─────────────────│
│ id (PK)         │              │ id (PK)         │
│ user_id (FK)    │              │ user_id (FK)    │
│ alarm_time      │              │ times_per_day   │
│ days_of_week    │              │ start_time      │
│ is_active       │              │ end_time        │
└─────────────────┘              │ is_active       │
                                 └─────────────────┘

         │
         │ 1:N
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌─────────────────┐              ┌─────────────────┐
│performance_     │              │ device_tokens   │
│snapshots        │              │─────────────────│
│─────────────────│              │ id (PK)         │
│ id (PK)         │              │ user_id (FK)    │
│ user_id (FK)    │              │ token           │
│ snapshot_date   │              │ platform        │
│ metrics (JSONB) │              │ is_active       │
└─────────────────┘              └─────────────────┘
```

### Estructura de Metrics (JSONB)

```json
{
  "score_body": 85,
  "score_mind": 90,
  "completed_body_tasks": 5,
  "completed_mind_tasks": 3,
  "pending_body_tasks": 2,
  "pending_mind_tasks": 1,
  "incomplete_body_tasks": 2,
  "incomplete_mind_tasks": 1,
  "missed_alarms": 1,
  "total_penalty": 13,
  "body_completion_rate": 71.43,
  "mind_completion_rate": 75.0,
  "active_alarms": 4,
  "active_reminders": 6,
  "last_updated": "2024-10-16T17:00:00Z"
}
```

## 🔧 Componentes Detallados

### ScoreCalculator

```python
class ScoreCalculator:
    """
    Responsabilidades:
    - Calcular penalizaciones por tareas incompletas
    - Actualizar scores diarios (Body y Mind)
    - Mantener score mínimo de 0
    - Guardar resultados en snapshots
    
    Constantes:
    - PENALTY_BODY_TASK = 5
    - PENALTY_MIND_TASK = 5
    - PENALTY_ROUTINE_ALARM = 3
    - MIN_SCORE = 0
    - MAX_SCORE = 100
    
    Métodos principales:
    - calculate_daily_scores()
    - _calculate_user_score(user)
    - _count_incomplete_tasks(table, user_id, start, end)
    - _count_missed_alarms(user_id, start, end)
    """
```

### NotificationSender

```python
class NotificationSender:
    """
    Responsabilidades:
    - Enviar alarmas de rutina en horarios específicos
    - Enviar recordatorios distribuidos durante el día
    - Enviar resúmenes diarios
    - Gestionar tokens FCM inválidos
    
    Métodos principales:
    - send_scheduled_notifications()
    - _process_routine_alarms()
    - _process_routine_reminders()
    - _should_trigger_alarm(alarm)
    - _should_trigger_reminder(reminder)
    - send_daily_summary()
    """
```

### MetricsUpdater

```python
class MetricsUpdater:
    """
    Responsabilidades:
    - Actualizar métricas de rendimiento cada hora
    - Calcular tasas de completación
    - Limpiar snapshots antiguos
    - Generar reportes semanales
    
    Métodos principales:
    - update_all_metrics()
    - _update_user_metrics(user)
    - cleanup_old_snapshots(days_to_keep)
    - generate_weekly_report()
    """
```

### AutomationScheduler

```python
class AutomationScheduler:
    """
    Responsabilidades:
    - Orquestar todas las tareas de automatización
    - Decidir qué tareas ejecutar según la hora
    - Manejar errores y logs
    - Ejecutar tareas específicas manualmente
    
    Métodos principales:
    - run_hourly_tasks()
    - run_specific_task(task_name)
    """
```

## 🕐 Cronograma de Ejecución

```
00:00 ─┬─ Notificaciones
       ├─ Métricas
       └─ [Domingo] Limpieza + Reportes

01:00 ─┬─ Notificaciones
       └─ Métricas

02:00 ─┬─ Notificaciones
       └─ Métricas

...

23:00 ─┬─ Notificaciones
       ├─ Métricas
       ├─ Cálculo de Scores
       └─ Resúmenes Diarios
```

## 🔐 Seguridad

### Variables de Entorno

```
GitHub Secrets (Encriptados)
    │
    ├─> SUPABASE_URL
    ├─> SUPABASE_SERVICE_ROLE_KEY
    ├─> FIREBASE_SERVICE_ACCOUNT
    └─> JWT_SECRET_KEY
         │
         └─> Inyectados en runtime
             (No almacenados en código)
```

### Permisos de Base de Datos

```
Service Role Key
    │
    ├─> Acceso completo a todas las tablas
    ├─> Bypass de Row Level Security (RLS)
    └─> Solo para backend/automatización
        (Nunca expuesto al frontend)
```

## 📈 Escalabilidad

### Optimizaciones Implementadas

1. **Consultas Eficientes**
   - Índices en columnas frecuentemente consultadas
   - Uso de `count='exact'` solo cuando es necesario
   - Límites en consultas de listado

2. **Procesamiento por Lotes**
   - Usuarios procesados en bucle (no en paralelo por simplicidad)
   - Posibilidad de paralelizar en el futuro

3. **Manejo de Errores**
   - Errores individuales no detienen el proceso completo
   - Logs detallados para debugging

4. **Limpieza Automática**
   - Snapshots antiguos eliminados semanalmente
   - Previene crecimiento descontrolado de la BD

### Límites Actuales

- **Usuarios:** Sin límite teórico (depende de Supabase)
- **Ejecución:** ~5-10 minutos para 1000 usuarios
- **Notificaciones:** Limitado por cuota de Firebase FCM
- **Snapshots:** 90 días de retención

### Mejoras Futuras

```
┌─────────────────────────────────────────┐
│  Posibles Optimizaciones                │
├─────────────────────────────────────────┤
│ ✓ Procesamiento paralelo de usuarios   │
│ ✓ Cache de consultas frecuentes        │
│ ✓ Queue system para notificaciones     │
│ ✓ Webhooks para eventos en tiempo real │
│ ✓ Dashboard de monitoreo               │
│ ✓ Alertas automáticas de errores       │
└─────────────────────────────────────────┘
```

## 🧪 Testing

### Niveles de Testing

```
┌─────────────────────────────────────────┐
│  Unit Tests                             │
│  - Funciones individuales               │
│  - Cálculos de scores                   │
│  - Lógica de notificaciones             │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  Integration Tests                      │
│  - Interacción con Supabase             │
│  - Envío de notificaciones FCM          │
│  - Flujos completos                     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  End-to-End Tests                       │
│  - Ejecución completa del scheduler     │
│  - Verificación de datos en BD          │
│  - Notificaciones recibidas             │
└─────────────────────────────────────────┘
```

## 📊 Monitoreo y Observabilidad

### Logs Disponibles

```
GitHub Actions Logs
    │
    ├─> Inicio de ejecución
    ├─> Tareas ejecutadas
    ├─> Resultados por usuario
    ├─> Errores encontrados
    └─> Resumen final
```

### Métricas Rastreadas

```
Sistema:
- Tiempo de ejecución total
- Número de usuarios procesados
- Tareas exitosas vs fallidas

Usuarios:
- Scores diarios
- Tareas completadas
- Tasas de completación
- Notificaciones enviadas
```

## 🔄 Ciclo de Vida de Datos

```
Creación → Uso Activo → Archivo → Eliminación
   │           │           │           │
   │           │           │           └─> 90 días
   │           │           │
   │           │           └─> performance_snapshots
   │           │
   │           └─> Métricas actualizadas cada hora
   │
   └─> Usuario crea alarma/recordatorio
```

---

**Documentación relacionada:**
- `README.md` - Documentación técnica
- `EXAMPLES.md` - Ejemplos de uso
- `../AUTOMATION_SETUP.md` - Guía de configuración
- `../AUTOMATION_SUMMARY.md` - Resumen ejecutivo
