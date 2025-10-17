# Sistema de Automatización IAM Backend

Sistema de automatización para tareas programadas que se ejecuta cada hora mediante GitHub Actions.

## 📁 Estructura

```
automation/
├── __init__.py
├── scheduler.py              # Orquestador principal
├── score_calculator.py       # Cálculo de scores diarios
├── notification_sender.py    # Envío de notificaciones
├── metrics_updater.py        # Actualización de métricas
└── README.md

scripts/
└── run_automation.py         # Script ejecutable

.github/workflows/
└── hourly_automation.yml     # GitHub Action workflow
```

## 🚀 Funcionalidades

### 1. Score Calculator (`score_calculator.py`)

Calcula y actualiza los scores de usuarios al final del día (23:00).

**Características:**
- Penaliza tareas incompletas de Body y Mind
- Penaliza alarmas de rutina perdidas
- Mantiene un score mínimo de 0
- Actualiza `performance_snapshots` con los nuevos scores

**Penalizaciones:**
- Tarea Body incompleta: -5 puntos
- Tarea Mind incompleta: -5 puntos
- Alarma de rutina perdida: -3 puntos

### 2. Notification Sender (`notification_sender.py`)

Envía notificaciones programadas basadas en alarmas y recordatorios de rutina.

**Características:**
- Procesa alarmas de rutina (`routine_alarms`)
- Procesa recordatorios de rutina (`routine_reminders`)
- Respeta la zona horaria del usuario
- Verifica días de la semana activos
- Envía resúmenes diarios al final del día

**Tipos de notificaciones:**
- Alarmas de rutina (horario específico)
- Recordatorios distribuidos durante el día
- Resúmenes diarios de rendimiento

### 3. Metrics Updater (`metrics_updater.py`)

Actualiza métricas de rendimiento de usuarios cada hora.

**Métricas rastreadas:**
- Tareas completadas (Body y Mind)
- Tareas pendientes (Body y Mind)
- Tasas de completación
- Rutinas activas (alarmas y recordatorios)
- Reportes semanales

**Funciones adicionales:**
- Limpieza de snapshots antiguos (>90 días)
- Generación de reportes semanales

### 4. Scheduler (`scheduler.py`)

Orquestador principal que coordina todas las tareas de automatización.

**Ejecución cada hora:**
- ✅ Envío de notificaciones programadas
- ✅ Actualización de métricas de usuarios

**Ejecución a las 23:00 (fin de día):**
- ✅ Cálculo de scores diarios
- ✅ Envío de resúmenes diarios

**Ejecución semanal (Domingo 00:00):**
- ✅ Limpieza de snapshots antiguos
- ✅ Generación de reportes semanales

## 🔧 Uso

### Ejecución Local

```bash
# Ejecutar todas las tareas por hora
python scripts/run_automation.py

# Ejecutar tarea específica
python scripts/run_automation.py notifications
python scripts/run_automation.py metrics
python scripts/run_automation.py scores
python scripts/run_automation.py daily_summary
python scripts/run_automation.py cleanup
python scripts/run_automation.py weekly_report
```

### Ejecución con GitHub Actions

El workflow se ejecuta automáticamente cada hora. También puedes ejecutarlo manualmente:

1. Ve a la pestaña "Actions" en GitHub
2. Selecciona "Hourly Automation Tasks"
3. Click en "Run workflow"
4. Opcionalmente selecciona una tarea específica

## 🔐 Variables de Entorno Requeridas

Configura estos secrets en GitHub:

```
SUPABASE_URL              # URL de tu proyecto Supabase
SUPABASE_SERVICE_ROLE_KEY # Service role key de Supabase
FIREBASE_SERVICE_ACCOUNT  # Credenciales de Firebase (JSON)
JWT_SECRET_KEY            # Secret key para JWT
```

## 📊 Tablas de Base de Datos Utilizadas

- `users_iam` - Usuarios del sistema
- `profiles` - Perfiles con timezone y preferencias
- `tasks_body` - Tareas físicas
- `tasks_mind` - Tareas mentales
- `routine_alarms` - Alarmas de rutina
- `routine_reminders` - Recordatorios de rutina
- `performance_snapshots` - Snapshots de rendimiento diario
- `device_tokens` - Tokens FCM para notificaciones

## 🎯 Lógica de Scores

### Cálculo Diario (23:00)

1. **Obtener tareas del día:**
   - Tareas Body pendientes programadas para hoy
   - Tareas Mind pendientes programadas para hoy
   - Alarmas de rutina que debieron sonar hoy

2. **Calcular penalizaciones:**
   ```
   penalty_body = incomplete_body_tasks * 5
   penalty_mind = incomplete_mind_tasks * 5
   penalty_alarms = missed_alarms * 3
   total_penalty = penalty_body + penalty_mind + penalty_alarms
   ```

3. **Actualizar scores:**
   ```
   new_body_score = max(0, current_body_score - penalty_body)
   new_mind_score = max(0, current_mind_score - penalty_mind)
   ```

4. **Guardar en snapshot:**
   - Scores actualizados
   - Contadores de tareas incompletas
   - Penalizaciones aplicadas

## 🔔 Lógica de Notificaciones

### Alarmas de Rutina

- Verifican la hora actual vs `alarm_time`
- Verifican si el día actual está en `days_of_week`
- Se envían como notificaciones de tipo "alarma" (data-only)

### Recordatorios de Rutina

- Calculan intervalos basados en `times_per_day`
- Distribuyen notificaciones entre `start_time` y `end_time`
- Verifican ventana activa y día de la semana

### Resúmenes Diarios

- Se envían a las 23:00
- Incluyen tareas completadas del día
- Muestran scores actuales

## 📈 Métricas Actualizadas

Cada hora se actualizan:

```json
{
  "completed_body_tasks": 5,
  "completed_mind_tasks": 3,
  "pending_body_tasks": 2,
  "pending_mind_tasks": 1,
  "body_completion_rate": 71.43,
  "mind_completion_rate": 75.0,
  "active_alarms": 4,
  "active_reminders": 6,
  "last_updated": "2024-10-16T17:00:00Z"
}
```

## 🧹 Mantenimiento

### Limpieza Automática

- **Frecuencia:** Domingos a las 00:00
- **Acción:** Elimina snapshots > 90 días
- **Propósito:** Mantener la base de datos optimizada

### Reportes Semanales

- **Frecuencia:** Domingos a las 00:00
- **Contenido:**
  - Total de tareas completadas en la semana
  - Promedios de scores
  - Días rastreados

## 🐛 Debugging

### Ver logs en GitHub Actions

1. Ve a la pestaña "Actions"
2. Selecciona la ejecución que quieres revisar
3. Click en "run-automation" para ver los logs

### Logs locales

El script imprime información detallada en la consola:

```
==============================
HOURLY AUTOMATION RUN
==============================

[TASK] Sending scheduled notifications...
Sent 15 alarms and 23 reminders

[TASK] Updating user metrics...
Updating metrics for 42 users
Completed metrics update for 42 users

==============================
HOURLY AUTOMATION COMPLETED
Tasks executed: 2
==============================
```

## ⚠️ Consideraciones

1. **Zonas Horarias:** El sistema respeta la timezone de cada usuario configurada en `profiles.timezone`

2. **Tokens FCM:** Los tokens inválidos se desactivan automáticamente

3. **Errores:** Los errores se registran pero no detienen la ejecución de otras tareas

4. **Idempotencia:** Las tareas están diseñadas para ser seguras si se ejecutan múltiples veces

5. **Performance:** Las consultas están optimizadas con índices en las tablas principales

## 🔄 Próximas Mejoras

- [ ] Sistema de logs persistente
- [ ] Dashboard de monitoreo de automatización
- [ ] Notificaciones de errores críticos
- [ ] Métricas de rendimiento del sistema
- [ ] Tests automatizados
- [ ] Retry logic para tareas fallidas
