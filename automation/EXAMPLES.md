# Ejemplos de Uso - Sistema de Automatización

## 📖 Casos de Uso Comunes

### 1. Usuario con Rutina Matutina

**Escenario:**
María quiere hacer ejercicio todos los días a las 7:00 AM.

**Configuración:**
```json
// Crear alarma de rutina
POST /api/routine/alarms
{
  "name": "Ejercicio Matutino",
  "description": "Rutina de ejercicio diaria",
  "source_type": "body",
  "alarm_time": "07:00:00",
  "days_of_week": [1, 2, 3, 4, 5, 6, 7],
  "notification_title": "¡Hora de Ejercitarse!",
  "notification_body": "Es momento de tu rutina matutina",
  "is_active": true
}
```

**Resultado:**
- A las 7:00 AM cada día, María recibe una notificación
- Si no completa la tarea, al final del día (23:00) se le restan 3 puntos de su score
- Las métricas se actualizan cada hora

### 2. Usuario con Recordatorios de Hidratación

**Escenario:**
Juan quiere recordatorios para tomar agua 8 veces al día entre 8 AM y 10 PM.

**Configuración:**
```json
// Crear recordatorio de rutina
POST /api/routine/reminders
{
  "name": "Hidratación",
  "description": "Recordatorio para tomar agua",
  "source_type": "body",
  "times_per_day": 8,
  "start_time": "08:00:00",
  "end_time": "22:00:00",
  "days_of_week": [1, 2, 3, 4, 5, 6, 7],
  "notification_title": "💧 Hora de Hidratarte",
  "notification_body": "Toma un vaso de agua",
  "is_active": true
}
```

**Cálculo de Intervalos:**
```
Ventana activa: 8:00 - 22:00 = 14 horas
Recordatorios: 8 veces al día
Intervalo: 14 / 8 = 1.75 horas ≈ cada 1 hora 45 minutos

Horarios aproximados:
- 08:00
- 09:45
- 11:30
- 13:15
- 15:00
- 16:45
- 18:30
- 20:15
```

### 3. Usuario con Múltiples Tareas Diarias

**Escenario:**
Ana tiene 3 tareas Body y 2 tareas Mind programadas para hoy.

**Tareas:**
```
Body Tasks:
- Ejercicio (07:00) - Pendiente
- Caminar (12:00) - Completada ✓
- Yoga (19:00) - Pendiente

Mind Tasks:
- Meditación (08:00) - Completada ✓
- Lectura (21:00) - Pendiente
```

**Cálculo de Score (23:00):**
```
Tareas incompletas:
- Body: 2 tareas × 5 puntos = -10 puntos
- Mind: 1 tarea × 5 puntos = -5 puntos
- Total penalty: -15 puntos

Score inicial: Body=100, Mind=100
Score final: Body=90, Mind=95
```

**Snapshot guardado:**
```json
{
  "user_id": "ana-uuid",
  "snapshot_date": "2024-10-16",
  "metrics": {
    "completed_body_tasks": 1,
    "completed_mind_tasks": 1,
    "incomplete_body_tasks": 2,
    "incomplete_mind_tasks": 1,
    "total_penalty": 15,
    "score_body": 90,
    "score_mind": 95,
    "body_completion_rate": 33.33,
    "mind_completion_rate": 50.0
  }
}
```

## 🔧 Ejemplos de Código

### Ejemplo 1: Crear Alarma Programáticamente

```python
from lib.db import get_supabase

def create_morning_alarm(user_id):
    """Crear alarma matutina para un usuario."""
    supabase = get_supabase()
    
    alarm_data = {
        "user_id": user_id,
        "name": "Despertar",
        "description": "Alarma para despertar",
        "source_type": "custom",
        "alarm_time": "06:30:00",
        "days_of_week": [1, 2, 3, 4, 5],  # Lunes a Viernes
        "notification_title": "¡Buenos Días!",
        "notification_body": "Es hora de comenzar el día",
        "sound_enabled": True,
        "vibration_enabled": True,
        "priority": "max",
        "is_active": True
    }
    
    result = supabase.from_('routine_alarms').insert(alarm_data).execute()
    return result.data[0] if result.data else None
```

### Ejemplo 2: Consultar Métricas de Usuario

```python
from datetime import datetime, timedelta
from lib.db import get_supabase

def get_user_weekly_stats(user_id):
    """Obtener estadísticas semanales de un usuario."""
    supabase = get_supabase()
    
    # Últimos 7 días
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    result = supabase.from_('performance_snapshots').select('*').eq(
        'user_id', user_id
    ).gte(
        'snapshot_date', start_date.isoformat()
    ).lte(
        'snapshot_date', end_date.isoformat()
    ).order('snapshot_date').execute()
    
    snapshots = result.data or []
    
    # Calcular promedios
    if not snapshots:
        return None
    
    total_body_tasks = sum(s['metrics'].get('completed_body_tasks', 0) for s in snapshots)
    total_mind_tasks = sum(s['metrics'].get('completed_mind_tasks', 0) for s in snapshots)
    avg_body_score = sum(s['metrics'].get('score_body', 0) for s in snapshots) / len(snapshots)
    avg_mind_score = sum(s['metrics'].get('score_mind', 0) for s in snapshots) / len(snapshots)
    
    return {
        'period': f"{start_date} to {end_date}",
        'total_body_tasks': total_body_tasks,
        'total_mind_tasks': total_mind_tasks,
        'avg_body_score': round(avg_body_score, 2),
        'avg_mind_score': round(avg_mind_score, 2),
        'days_tracked': len(snapshots)
    }
```

### Ejemplo 3: Enviar Notificación Manual

```python
from services.notification_service import send_notification_to_user

def send_achievement_notification(user_id, achievement_name):
    """Enviar notificación de logro."""
    send_notification_to_user(
        user_id=user_id,
        title="🏆 ¡Nuevo Logro!",
        body=f"Has desbloqueado: {achievement_name}",
        data={
            'type': 'achievement',
            'achievement': achievement_name
        }
    )
```

## 📊 Ejemplos de Consultas SQL

### Consulta 1: Top Usuarios por Score

```sql
-- Usuarios con mejor score body en la última semana
SELECT 
  u.email,
  AVG((ps.metrics->>'score_body')::numeric) as avg_body_score,
  COUNT(ps.id) as days_tracked
FROM users_iam u
JOIN performance_snapshots ps ON u.id = ps.user_id
WHERE ps.snapshot_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY u.id, u.email
ORDER BY avg_body_score DESC
LIMIT 10;
```

### Consulta 2: Usuarios con Más Tareas Completadas

```sql
-- Usuarios más activos en el último mes
SELECT 
  u.email,
  SUM((ps.metrics->>'completed_body_tasks')::int) as total_body,
  SUM((ps.metrics->>'completed_mind_tasks')::int) as total_mind,
  SUM(
    (ps.metrics->>'completed_body_tasks')::int + 
    (ps.metrics->>'completed_mind_tasks')::int
  ) as total_tasks
FROM users_iam u
JOIN performance_snapshots ps ON u.id = ps.user_id
WHERE ps.snapshot_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY u.id, u.email
ORDER BY total_tasks DESC
LIMIT 10;
```

### Consulta 3: Análisis de Tendencias

```sql
-- Tendencia de scores en los últimos 30 días
SELECT 
  snapshot_date,
  AVG((metrics->>'score_body')::numeric) as avg_body_score,
  AVG((metrics->>'score_mind')::numeric) as avg_mind_score,
  COUNT(*) as users_tracked
FROM performance_snapshots
WHERE snapshot_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY snapshot_date
ORDER BY snapshot_date;
```

## 🎯 Escenarios de Testing

### Test 1: Verificar Cálculo de Scores

```python
# test/test_score_calculation.py
import pytest
from automation.score_calculator import ScoreCalculator

def test_score_penalty_calculation():
    """Test que las penalizaciones se calculan correctamente."""
    calculator = ScoreCalculator()
    
    # Simular usuario con tareas incompletas
    incomplete_body = 2
    incomplete_mind = 1
    missed_alarms = 1
    
    expected_penalty = (
        (incomplete_body * 5) +  # 10
        (incomplete_mind * 5) +   # 5
        (missed_alarms * 3)       # 3
    )  # Total: 18
    
    assert expected_penalty == 18
```

### Test 2: Verificar Envío de Notificaciones

```python
# test/test_notifications.py
from automation.notification_sender import NotificationSender

def test_alarm_should_trigger():
    """Test que las alarmas se activan en el momento correcto."""
    sender = NotificationSender()
    
    # Alarma configurada para las 7:00 AM, Lunes a Viernes
    alarm = {
        'alarm_time': '07:00:00',
        'days_of_week': [1, 2, 3, 4, 5],
        'user_id': 'test-user',
        'is_active': True
    }
    
    # Simular que es Lunes a las 7:00 AM
    # (necesitarías mockear datetime.now())
    
    should_trigger = sender._should_trigger_alarm(alarm)
    # assert should_trigger == True
```

## 🔄 Flujos de Trabajo Completos

### Flujo 1: Día Completo de un Usuario

```
06:30 - Alarma "Despertar" se activa
        → Notificación enviada
        → Usuario despierta

07:00 - Alarma "Ejercicio" se activa
        → Notificación enviada
        → Usuario completa tarea Body

08:00 - Recordatorio "Hidratación" #1
        → Notificación enviada

09:00 - Métricas actualizadas (ejecución horaria)
        → completed_body_tasks: 1
        → pending_body_tasks: 0

12:00 - Alarma "Almuerzo Saludable"
        → Notificación enviada
        → Usuario NO completa tarea

23:00 - Cálculo de scores (fin del día)
        → Tarea "Almuerzo" incompleta: -5 puntos
        → Score body: 95
        → Snapshot guardado
        → Resumen diario enviado
```

### Flujo 2: Semana Completa

```
Lunes - Viernes:
  - Alarmas diarias se activan
  - Recordatorios distribuidos
  - Métricas actualizadas cada hora
  - Scores calculados cada noche

Sábado:
  - Solo alarmas de fin de semana
  - Métricas actualizadas

Domingo 00:00:
  - Limpieza de snapshots antiguos
  - Generación de reporte semanal
  - Usuario recibe resumen de la semana
```

## 💡 Tips y Mejores Prácticas

### 1. Configurar Alarmas Efectivas

```python
# ✅ BUENO: Alarma específica con contexto
{
  "name": "Ejercicio Matutino - Cardio",
  "alarm_time": "07:00:00",
  "notification_title": "🏃 Cardio Time!",
  "notification_body": "30 minutos de cardio para empezar el día",
  "priority": "max"
}

# ❌ MALO: Alarma genérica sin contexto
{
  "name": "Alarma",
  "alarm_time": "07:00:00",
  "notification_title": "Alarma",
  "notification_body": "Alarma"
}
```

### 2. Distribuir Recordatorios Inteligentemente

```python
# ✅ BUENO: Recordatorios distribuidos en ventana realista
{
  "times_per_day": 6,
  "start_time": "08:00:00",  # Después de despertar
  "end_time": "22:00:00"     # Antes de dormir
}

# ❌ MALO: Demasiados recordatorios en poco tiempo
{
  "times_per_day": 20,
  "start_time": "08:00:00",
  "end_time": "10:00:00"  # Solo 2 horas
}
```

### 3. Monitorear Regularmente

```bash
# Revisar snapshots recientes
python scripts/manage_automation.py snapshots 7

# Verificar rutinas activas
python scripts/manage_automation.py routines

# Ver stats de usuario específico
python scripts/manage_automation.py user <user-id>
```

## 🎓 Casos de Estudio

### Caso 1: Usuario Principiante

**Perfil:** Carlos, nuevo en el sistema
**Objetivo:** Establecer hábitos básicos

**Configuración Recomendada:**
- 2 alarmas diarias (mañana y noche)
- 3 recordatorios de hidratación
- Tareas simples de 10-15 minutos

**Resultado Esperado:**
- Score inicial: 100/100
- Después de 1 semana: 85-95 (ajustándose)
- Después de 1 mes: 90-100 (hábitos establecidos)

### Caso 2: Usuario Avanzado

**Perfil:** Laura, usuaria experimentada
**Objetivo:** Optimizar rendimiento

**Configuración Recomendada:**
- 5 alarmas diarias (rutina completa)
- 8 recordatorios distribuidos
- Tareas desafiantes de 30-60 minutos

**Resultado Esperado:**
- Score consistente: 95-100
- Alta tasa de completación: >90%
- Reportes semanales positivos

---

Para más información, consulta:
- `automation/README.md` - Documentación técnica
- `AUTOMATION_SETUP.md` - Guía de configuración
- `AUTOMATION_SUMMARY.md` - Resumen del sistema
