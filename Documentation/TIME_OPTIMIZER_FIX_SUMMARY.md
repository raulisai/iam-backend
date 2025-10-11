# ✅ Time Optimizer Fix - COMPLETADO

## Problemas Corregidos

### 1. **Nombres de Columnas Incorrectos**
- ❌ `goals.end_at` → ✅ `goals.end_date`
- ❌ `task_templates.description` → ✅ Eliminado (no existe)
- ❌ `task_occurrences.status` → ✅ Eliminado (no existe)
- ❌ `task_occurrences.completed_at` → ✅ Eliminado (no existe)
- ❌ `goal_tasks.status` → ✅ Eliminado (no existe)

### 2. **Lógica de Inclusión de Tareas**
- ✅ Ahora incluye tareas **sin programación específica** (`scheduled_at = NULL`)
- ✅ Incluye tareas programadas para el día de hoy
- ✅ Incluye goal_tasks sin task_occurrences (tareas no recurrentes pendientes)

### 3. **Estructura de Respuesta Mejorada**
Ahora el endpoint `/api/time-optimizer/tasks-now` devuelve:

```json
{
  "user_id": "6a012777-fdaf-4ee1-b41b-b59f48374f59",
  "current_time": "2025-10-11T06:06:26",
  "time_slot": "morning",
  "remaining_minutes_in_slot": 165,
  "remaining_hours_in_slot": 2.75,
  
  "recommended_tasks": [
    // Top 5 tareas recomendadas de todos los tipos
  ],
  
  "quick_wins": [
    // Tareas que toman 30 min o menos
  ],
  
  "goal_tasks": [
    // Solo las tareas de metas de las RECOMENDADAS (subconjunto de recommended_tasks)
    {
      "id": "...",
      "title": "Establecer rutina diaria",
      "type": "goal",
      "goal_title": "Desarrollar Hábitos Saludables",
      "goal_deadline": "2025-12-31T00:00:00",
      "days_until_deadline": 81,
      "urgency_multiplier": 1.0,
      "priority_score": 30.0,
      "estimated_duration_minutes": 60,
      "start_time": "2025-10-11T06:00:00",
      "end_time": "2025-10-11T07:00:00"
    }
  ],
  
  "mind_tasks": [
    // Solo las tareas mentales de las RECOMENDADAS (subconjunto de recommended_tasks)
  ],
  
  "body_tasks": [
    // Solo las tareas físicas de las RECOMENDADAS (subconjunto de recommended_tasks)
  ],
  
  "total_available_tasks": 46,
  "message": "You have 165 minutes remaining in your morning slot"
}
```

## Resultados de Prueba

```
✓ Total available tasks: 46
✓ Recommended tasks: 10 (top priorities)
✓ Goal tasks: 10 (categorización de recommended)
✓ Mind tasks: 0 (categorización de recommended)
✓ Body tasks: 0 (categorización de recommended)
✓ Arrays son CATEGORIZACIÓN de recommended, no todas las tasks
```

## Archivos Modificados

### `services/time_optimizer_service.py`

#### Cambios en `get_pending_tasks_all_types()`:
1. Agregado parámetro `include_unscheduled: bool = True`
2. Corregidos nombres de columnas en consultas SQL
3. Lógica para incluir tareas sin `scheduled_at`
4. Consulta adicional para `goal_tasks` sin occurrences
5. Prevención de duplicados

#### Cambios en `get_tasks_for_current_moment()`:
1. Agregados arrays separados: `goal_tasks`, `mind_tasks`, `body_tasks`
2. **IMPORTANTE**: Estos arrays son CATEGORIZACIÓN de `recommended_tasks`, no todas las disponibles
3. Se limita a top 10 tareas recomendadas (o menos si hay menos disponibles)
4. Mantiene compatibilidad con `recommended_tasks` y `quick_wins`

## Esquema de Base de Datos Verificado

### `task_occurrences`
```python
{
  'id': str,
  'task_id': str,
  'scheduled_at': str,
  'created_at': str,
  'notes': str (nullable)
}
```

### `goal_tasks`
```python
{
  'id': str,
  'goal_id': str,
  'user_id': str,
  'title': str,
  'description': str,
  'type': str (nullable),
  'required': bool,
  'weight': int,
  'due_at': str (nullable),
  'schedule_rrule': str (nullable),
  'created_at': str
}
```

### `tasks_mind` y `tasks_body`
```python
{
  'id': str,
  'template_id': str,
  'user_id': str,
  'created_by': str,
  'status': str,  # 'pending', 'in_progress', 'completed'
  'scheduled_at': str,
  'completed_at': str,
  'xp_awarded': int,
  'params': dict,
  'created_at': str
}
```

## Cómo Probar

### 1. Reiniciar el Servidor
```bash
cd c:\Users\raul_\Documents\code\iam-backend
python app.py
```

### 2. Ejecutar el Curl
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/tasks-now" \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmEwMTI3NzctZmRhZi00ZWUxLWI0MWItYjU5ZjQ4Mzc0ZjU5IiwiZW1haWwiOiJkakB4eC5jb20iLCJuYW1lIjoiRGpva2VyIE0iLCJleHAiOjE3NjAyNDg3ODcsImlhdCI6MTc2MDE2MjM4N30.HAg8plLJ4KTAwJL-ZUzIT7wKJXIVZSsLR1Lld2hzVmk"
```

### 3. Verificar Respuesta
Deberías ver:
- ✅ `total_available_tasks` > 0 (todas las tareas que caben en el tiempo disponible)
- ✅ `recommended_tasks` con las top 10 tareas por prioridad
- ✅ `goal_tasks` array (solo las recomendadas de tipo goal)
- ✅ `mind_tasks` array (solo las recomendadas de tipo mind)
- ✅ `body_tasks` array (solo las recomendadas de tipo body)
- ✅ **La suma de goal + mind + body = total de recommended**

## Notas Importantes

1. **Tareas Goal**: Se buscan en dos lugares:
   - `task_occurrences` (tareas recurrentes programadas) del usuario
   - `goal_tasks` sin occurrences (tareas únicas o pendientes de programar) **filtradas por user_id**

2. **Tareas Mind/Body**: Se buscan en sus tablas respectivas filtrando por:
   - `status IN ('pending', 'in_progress')`
   - `user_id` del usuario autenticado
   - Opcionalmente `scheduled_at` para el día seleccionado

3. **Priorización**: Las tareas se ordenan por:
   - Tipo (goal > mind/body)
   - Urgencia (deadline cercano)
   - Peso/importancia
   - Duración (tareas cortas = bonus)

4. **Time Slots**: 
   - Morning: 6:00 AM - Work Start
   - Evening: Work End - 10:00 PM
   - Work Hours: No se programan tareas

## Concepto Importante ⚠️

**Los arrays `goal_tasks`, `mind_tasks`, `body_tasks` NO son todas las tareas disponibles.**

Son una **CATEGORIZACIÓN** de las tareas en `recommended_tasks`:
- `recommended_tasks` = Top 10 tareas por prioridad (de todas las disponibles)
- `goal_tasks` = Filtro de `recommended_tasks` donde `type == 'goal'`
- `mind_tasks` = Filtro de `recommended_tasks` donde `type == 'mind'`
- `body_tasks` = Filtro de `recommended_tasks` donde `type == 'body'`

**Verificación**: `len(goal_tasks) + len(mind_tasks) + len(body_tasks) = len(recommended_tasks)`

## Documentación Adicional

- `Documentation/TIME_OPTIMIZER_TASKS_NOW_FIX.md` - Guía detallada
- `Documentation/TIME_OPTIMIZER_CURL_EXAMPLES.md` - Ejemplos de uso
