# Smart Task Scheduling - Optimización Inteligente

## Problema Resuelto

El endpoint estaba devolviendo **TODAS** las tareas disponibles sin considerar:
- ✅ El tiempo real restante en el día
- ✅ La prioridad de las tareas (goals > mind/body)
- ✅ Límite razonable de tareas por tipo

## Solución Implementada

### 1. Cálculo de Tiempo Restante HOY

```python
# Calcula cuánto tiempo queda desde AHORA hasta las 22:00 (10 PM)
end_of_day = current_time.replace(hour=22, minute=0, second=0, microsecond=0)
remaining_minutes_today = int((end_of_day - current_time).total_seconds() / 60)
```

**Ejemplo:**
- Hora actual: 21:00 (9 PM)
- Fin del día: 22:00 (10 PM)
- Tiempo restante: **60 minutos = 1 hora**
- Si son las 21:00, solo quedan **3 horas** hasta medianoche, pero el sistema usa 22:00 como límite productivo

### 2. Sistema de Prioridades

El algoritmo ahora programa tareas en este orden:

#### **Prioridad 1: GOAL TASKS** 🎯
- Se programan PRIMERO todas las que quepan
- Son las más importantes para alcanzar objetivos
- Se llenan hasta agotar el tiempo disponible

#### **Prioridad 2: MIND TASKS** 🧠
- Máximo **1-2 tareas** solamente
- Solo si queda tiempo después de goals
- Limita a las 2 más prioritarias

#### **Prioridad 3: BODY TASKS** 💪
- Máximo **1-2 tareas** solamente
- Solo si queda tiempo después de goals y mind
- Limita a las 2 más prioritarias

### 3. Control de Capacidad

```python
# Sistema inteligente que verifica si cabe cada tarea
duration_with_buffer = duration + 15  # Incluye 15 min de descanso

if duration_with_buffer <= available_time_buffer:
    # ✅ Cabe - programar la tarea
    scheduled_tasks.append(task)
    available_time_buffer -= duration_with_buffer
else:
    # ❌ No cabe - detener programación
    break
```

## Ejemplo Real: 9 PM con 3 horas restantes

### Situación
- **Hora actual:** 21:00 (9 PM)
- **Tiempo disponible:** 180 minutos (3 horas hasta 22:00... pero espera, ¿cómo 3 horas?)
- **Nota:** Si el usuario dice "son las 9 y me quedan 3 horas", el sistema debe ajustarse

### Ajuste del Horario de Fin
Si necesitas que el día termine a las 00:00 (medianoche) en lugar de 22:00:

```python
# Cambiar línea 807 en time_optimizer_service.py
end_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
# Si ya pasó medianoche, sumar un día
if current_time.hour < 12:
    end_of_day = end_of_day  # Ya es del día siguiente
else:
    end_of_day = end_of_day + timedelta(days=1)
```

O mejor, usar 24:00 = 00:00 del día siguiente:

```python
# Opción más simple: hasta medianoche
if current_time.hour >= 22:
    # Después de las 10 PM, calcular hasta medianoche
    end_of_day = (current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
else:
    # Antes de las 10 PM, usar 22:00 como límite
    end_of_day = current_time.replace(hour=22, minute=0, second=0, microsecond=0)
```

### Programación Resultante (180 minutos disponibles)

#### ✅ Goal Tasks (Prioridad 1)
```
1. Goal Task 1 - 60 min (09:00 PM - 10:00 PM)
   Buffer: 15 min
2. Goal Task 2 - 60 min (10:15 PM - 11:15 PM)
   Buffer: 15 min
Total: 150 minutos usados
Restante: 30 minutos
```

#### ✅ Mind Tasks (Prioridad 2) - Máximo 2
```
3. Mind Task 1 - 30 min (11:30 PM - 12:00 AM)
   ❌ No cabe (necesita 45 min con buffer)
Total: 0 mind tasks programadas
```

#### ❌ Body Tasks (Prioridad 3)
```
No hay tiempo restante
```

### Resultado Final
- **Goal tasks programadas:** 2
- **Mind tasks programadas:** 0 (no cabían)
- **Body tasks programadas:** 0 (no había tiempo)
- **Total tareas:** 2 (en lugar de 10+)

## Respuesta JSON Mejorada

```json
{
  "body_tasks": [],
  "goal_tasks": [
    {
      "id": "uuid-1",
      "title": "Pararme y bañarme con agua fría",
      "type": "goal",
      "estimated_duration_minutes": 60,
      "priority_score": 3000002,
      "start_time": "2025-10-12T21:00:00",
      "end_time": "2025-10-12T22:00:00",
      "time_slot": "evening"
    },
    {
      "id": "uuid-2",
      "title": "Planificación del proyecto IAM",
      "type": "goal",
      "estimated_duration_minutes": 60,
      "priority_score": 62,
      "start_time": "2025-10-12T22:15:00",
      "end_time": "2025-10-12T23:15:00",
      "time_slot": "evening"
    }
  ],
  "mind_tasks": [],
  "current_time": "2025-10-12T21:00:00-06:00",
  "message": "You have 180 minutes remaining today. 150 minutes scheduled.",
  "remaining_minutes_today": 180,
  "remaining_hours_today": 3.0,
  "total_body_tasks": 0,
  "total_goal_tasks": 2,
  "total_mind_tasks": 0,
  "total_time_used_for_tasks": 150,
  "remaining_after_scheduling": 30,
  "total_available_tasks": 15,
  "total_scheduled_tasks": 2,
  "user_id": "6a012777-fdaf-4ee1-b41b-b59f48374f59"
}
```

## Campos Nuevos en la Respuesta

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `remaining_minutes_today` | Minutos restantes desde AHORA hasta fin del día | 180 |
| `remaining_hours_today` | Horas restantes hoy (versión decimal) | 3.0 |
| `remaining_after_scheduling` | Tiempo libre después de programar todas las tareas | 30 |
| `total_scheduled_tasks` | Total de tareas programadas (que caben en el tiempo) | 2 |
| `total_available_tasks` | Total de tareas disponibles en BD | 15 |

## Comparación: Antes vs Después

### ❌ Antes
- Devolvía **todas** las tareas (10-15+)
- No consideraba tiempo disponible
- No limitaba mind/body tasks
- Respuesta poco práctica

### ✅ Después
- Devuelve **solo** las que caben en el tiempo restante (2-5)
- Calcula tiempo real desde hora actual
- Limita mind/body a máximo 2 cada uno
- Prioriza goals (lo más importante)
- Respuesta práctica y realista

## Límites Configurables

Si necesitas ajustar los límites:

```python
# En time_optimizer_service.py, líneas ~880-900

# Cambiar límite de mind tasks (actualmente 2)
mind_task_limit = 2  # Cambiar a 1, 3, etc.

# Cambiar límite de body tasks (actualmente 2)
body_task_limit = 2  # Cambiar a 1, 3, etc.

# Cambiar hora de fin del día (actualmente 22:00)
end_of_day = current_time.replace(hour=22, minute=0, second=0, microsecond=0)
# Cambiar a 23:00, 00:00, etc.
```

## Próximos Ajustes Recomendados

1. **Configurar hora de fin**: Permitir que el usuario configure hasta qué hora trabaja (en lugar de hardcodear 22:00)

2. **Pausas inteligentes**: Detectar si hay tiempo para descansos entre tareas

3. **Alertas de sobrecarga**: Avisar si hay más tareas de las que caben en el tiempo disponible

4. **Reprogramación automática**: Mover tareas que no caben a mañana

## Testing

```bash
# Test con hora actual simulada (9 PM)
curl -X GET "http://localhost:5000/api/time-optimizer/tasks-now" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Validar que:**
- ✅ Solo devuelve 2-5 tareas (no 10+)
- ✅ Goals están primero
- ✅ Mind/Body máximo 2 cada uno
- ✅ `remaining_minutes_today` refleja tiempo real restante
- ✅ `total_time_used_for_tasks` <= `remaining_minutes_today`
