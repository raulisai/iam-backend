# Sistema de Optimización de Tiempo - Documentación Completa

## 📋 Descripción General

El **Sistema de Optimización de Tiempo** es un algoritmo sofisticado diseñado para maximizar la productividad del usuario mediante el cálculo inteligente del tiempo disponible y la distribución óptima de tareas a lo largo del día.

## 🎯 Objetivos del Sistema

1. **Calcular tiempo real disponible**: Después de restar horas fijas (trabajo, sueño, aseo)
2. **Priorizar metas críticas**: Especialmente aquellas con fechas límite cercanas
3. **Balance óptimo**: Mantener equilibrio entre tareas de goals, mind y body
4. **Maximizar productividad**: Aprovechar al máximo las horas libres reales

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO + TOKEN                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              ENDPOINTS DE OPTIMIZACIÓN                  │
│  1. /available-time    - Cálculo de tiempo disponible  │
│  2. /optimize-day      - Horario optimizado del día    │
│  3. /tasks-now         - Tareas para este momento      │
│  4. /remaining-day     - Tareas restantes del día      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│            TIME OPTIMIZER SERVICE                       │
│  - Análisis de perfil y disponibilidad                 │
│  - Obtención de tareas pendientes                      │
│  - Algoritmo de priorización                           │
│  - Distribución temporal óptima                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  BASE DE DATOS                          │
│  - profiles (horarios, horas semanales)                │
│  - goals (con deadlines)                               │
│  - task_occurrences (goal tasks programadas)           │
│  - tasks_mind (tareas mentales)                        │
│  - tasks_body (tareas físicas)                         │
└─────────────────────────────────────────────────────────┘
```

## 🧮 Fórmulas y Algoritmo

### 1. Cálculo de Tiempo Disponible Diario

```python
# Constantes
HORAS_TOTALES_DIA = 24
HORAS_SUEÑO = 8
HORAS_TRABAJO = parse_from_work_schedule(profile.work_schedules)
HORAS_CUIDADO_PERSONAL = 2  # Aseo, comida, transporte

# Fórmula
HORAS_LIBRES = HORAS_TOTALES_DIA - HORAS_SUEÑO - HORAS_TRABAJO - HORAS_CUIDADO_PERSONAL
```

### 2. Slots de Tiempo

El día se divide en dos slots productivos:

- **Slot Matutino**: Desde despertar (6:00) hasta inicio de trabajo
  - Ideal para: Tareas de goals (alta concentración)
  - Duración típica: 2-3 horas

- **Slot Vespertino**: Desde fin de trabajo hasta hora de dormir (22:00)
  - Ideal para: Mix de goals, mind y body tasks
  - Duración típica: 4-5 horas

### 3. Sistema de Priorización

#### Pesos Base por Tipo de Tarea
```python
PRIORITY_WEIGHTS = {
    'goal': 3.0,    # Máxima prioridad (metas personales)
    'mind': 1.5,    # Media prioridad (desarrollo mental)
    'body': 1.5     # Media prioridad (salud física)
}
```

#### Cálculo de Score de Prioridad

```python
def calculate_priority_score(task):
    # 1. Score base por tipo y peso
    base_score = PRIORITY_WEIGHTS[task.type] * task.weight * 10
    
    # 2. Multiplicador de urgencia (deadline)
    if days_until_deadline <= 1:
        urgency_multiplier = 3.0    # ¡Urgente! Vence hoy/mañana
    elif days_until_deadline <= 3:
        urgency_multiplier = 2.5    # Muy importante
    elif days_until_deadline <= 7:
        urgency_multiplier = 2.0    # Importante
    elif days_until_deadline <= 14:
        urgency_multiplier = 1.5    # Moderado
    else:
        urgency_multiplier = 1.0    # Normal
    
    # 3. Bonus por duración corta (más fácil de encajar)
    if duration_minutes <= 30:
        duration_bonus = 5
    elif duration_minutes <= 60:
        duration_bonus = 2
    else:
        duration_bonus = 0
    
    # Score final
    final_score = (base_score * urgency_multiplier) + duration_bonus
    
    return final_score
```

### 4. Algoritmo de Distribución

```
PARA CADA TAREA (ordenadas por priority_score descendente):
    
    1. Calcular duración con buffer
       duration_with_buffer = task.duration + 15 minutos
    
    2. Determinar preferencia de slot:
       SI task.type EN ['goal', 'mind']:
           preferir_slot = 'morning'  # Mejor concentración
       SI task.type == 'body':
           preferir_slot = 'evening'  # Después del trabajo
    
    3. Intentar asignar a slot preferido:
       SI hay espacio suficiente EN slot_preferido:
           asignar_tarea(slot_preferido)
           restar_tiempo(slot_preferido, duration_with_buffer)
       SINO SI hay espacio EN slot_alternativo:
           asignar_tarea(slot_alternativo)
           restar_tiempo(slot_alternativo, duration_with_buffer)
       SINO:
           dejar_sin_programar()
    
    4. Continuar hasta:
       - No quedan tareas
       - No queda tiempo disponible en ningún slot
```

### 5. Distribución Ideal

El sistema busca mantener esta distribución de tiempo:

```
60% → Tareas de Goals (metas personales)
20% → Tareas de Mind (desarrollo mental)
20% → Tareas de Body (actividad física)
```

### 6. Métricas de Calidad

#### Efficiency Score (0-100)
```python
efficiency = (tiempo_programado / tiempo_disponible) * 100
```

#### Balance Score (0-100)
```python
# Calcula desviación de la distribución ideal
balance = 100 - (suma_absoluta_desviaciones / 3)
```

#### Productivity Score (0-100)
```python
productivity = (efficiency * 0.6) + (balance * 0.4)
```

## 🔌 Endpoints Disponibles

### 1. `/api/time-optimizer/available-time` [GET]

**Descripción**: Calcula el tiempo disponible del usuario.

**Headers**:
```
Authorization: Bearer {token}
```

**Respuesta**:
```json
{
  "user_id": "uuid",
  "has_profile": true,
  "profile": {
    "work_schedule": "9:00-17:00",
    "work_start": "09:00",
    "work_end": "17:00",
    "hours_per_week": 40,
    "hours_used_this_week": 12.5,
    "remaining_hours_this_week": 27.5
  },
  "daily_breakdown": {
    "total_hours": 24,
    "sleep_hours": 8,
    "work_hours": 8,
    "personal_care_hours": 2,
    "fixed_hours_total": 18,
    "free_hours_available": 6,
    "avg_study_hours_per_day": 5.71
  },
  "time_slots": {
    "morning": {
      "start": "06:00",
      "end": "09:00",
      "duration_hours": 2
    },
    "evening": {
      "start": "17:00",
      "end": "22:00",
      "duration_hours": 5
    }
  }
}
```

### 2. `/api/time-optimizer/optimize-day` [GET]

**Descripción**: Genera el horario optimizado para un día específico.

**Headers**:
```
Authorization: Bearer {token}
```

**Query Parameters**:
- `date` (opcional): Fecha en formato ISO (YYYY-MM-DD). Por defecto: hoy.

**Ejemplo Request**:
```
GET /api/time-optimizer/optimize-day?date=2025-10-09
```

**Respuesta**:
```json
{
  "user_id": "uuid",
  "date": "2025-10-09",
  "generated_at": "2025-10-09T14:30:00Z",
  "profile_summary": {
    "work_schedule": "9:00-17:00",
    "daily_free_hours": 6,
    "weekly_hours_remaining": 27.5
  },
  "schedule": {
    "morning": {
      "time_range": "06:00 - 09:00",
      "available_hours": 2,
      "available_minutes": 120,
      "scheduled_minutes": 105,
      "remaining_minutes": 15,
      "tasks": [
        {
          "id": "task-1",
          "title": "Estudiar capítulo 5 de Machine Learning",
          "type": "goal",
          "goal_title": "Completar curso de ML",
          "goal_deadline": "2025-10-15T00:00:00Z",
          "days_until_deadline": 6,
          "urgency_multiplier": 2.0,
          "estimated_duration_minutes": 60,
          "start_time": "2025-10-09T06:00:00Z",
          "end_time": "2025-10-09T07:00:00Z",
          "time_slot": "morning",
          "priority_score": 60.0,
          "status": "pending"
        },
        {
          "id": "task-2",
          "title": "Meditar 30 minutos",
          "type": "mind",
          "estimated_duration_minutes": 30,
          "start_time": "2025-10-09T07:15:00Z",
          "end_time": "2025-10-09T07:45:00Z",
          "time_slot": "morning",
          "priority_score": 20.0
        }
      ]
    },
    "evening": {
      "time_range": "17:00 - 22:00",
      "available_hours": 5,
      "available_minutes": 300,
      "scheduled_minutes": 255,
      "remaining_minutes": 45,
      "tasks": [
        {
          "id": "task-3",
          "title": "Proyecto final - Presentación",
          "type": "goal",
          "goal_deadline": "2025-10-10T23:59:59Z",
          "days_until_deadline": 1,
          "urgency_multiplier": 3.0,
          "estimated_duration_minutes": 90,
          "start_time": "2025-10-09T17:00:00Z",
          "end_time": "2025-10-09T18:30:00Z",
          "time_slot": "evening",
          "priority_score": 90.0
        },
        {
          "id": "task-4",
          "title": "Ejercicio en el gimnasio",
          "type": "body",
          "estimated_duration_minutes": 60,
          "start_time": "2025-10-09T18:45:00Z",
          "end_time": "2025-10-09T19:45:00Z",
          "time_slot": "evening",
          "priority_score": 15.0
        }
      ]
    }
  },
  "summary": {
    "total_tasks_available": 12,
    "tasks_by_type_available": {
      "goals": 5,
      "mind": 4,
      "body": 3
    },
    "total_tasks_scheduled": 8,
    "tasks_by_type_scheduled": {
      "goals": 4,
      "mind": 2,
      "body": 2
    },
    "total_minutes_available": 420,
    "total_minutes_scheduled": 360,
    "total_hours_scheduled": 6.0,
    "efficiency_percentage": 85.71,
    "unscheduled_tasks": 4
  },
  "distribution_analysis": {
    "actual_distribution": {
      "goal": 63.3,
      "mind": 18.3,
      "body": 18.3
    },
    "ideal_distribution": {
      "goal": 60.0,
      "mind": 20.0,
      "body": 20.0
    },
    "deviation_from_ideal": {
      "goal": 3.3,
      "mind": -1.7,
      "body": -1.7
    },
    "balance_score": 97.8
  },
  "scores": {
    "efficiency_score": 85.71,
    "balance_score": 97.8,
    "productivity_score": 90.55
  },
  "algorithm_info": {
    "version": "2.0",
    "priority_weights": {
      "goal": 3.0,
      "mind": 1.5,
      "body": 1.5
    },
    "buffer_between_tasks_minutes": 15,
    "considers_deadlines": true,
    "considers_time_of_day": true
  }
}
```

### 3. `/api/time-optimizer/tasks-now` [GET]

**Descripción**: Obtiene las tareas recomendadas para ESTE MOMENTO.

**Headers**:
```
Authorization: Bearer {token}
```

**Respuesta**:
```json
{
  "user_id": "uuid",
  "current_time": "2025-10-09T18:30:00Z",
  "time_slot": "evening",
  "remaining_minutes_in_slot": 210,
  "remaining_hours_in_slot": 3.5,
  "recommended_tasks": [
    {
      "id": "task-5",
      "title": "Revisar código del proyecto",
      "type": "goal",
      "estimated_duration_minutes": 45,
      "start_time": "2025-10-09T18:30:00Z",
      "priority_score": 75.0,
      "urgency_multiplier": 2.5
    },
    {
      "id": "task-6",
      "title": "Leer artículo técnico",
      "type": "mind",
      "estimated_duration_minutes": 30,
      "start_time": "2025-10-09T19:30:00Z",
      "priority_score": 22.0
    }
  ],
  "total_available_tasks": 5,
  "quick_wins": [
    {
      "id": "task-6",
      "title": "Leer artículo técnico",
      "estimated_duration_minutes": 30
    }
  ],
  "message": "You have 210 minutes remaining in your evening slot"
}
```

### 4. `/api/time-optimizer/remaining-day` [GET]

**Descripción**: Obtiene el horario optimizado para lo que resta del día.

**Headers**:
```
Authorization: Bearer {token}
```

**Respuesta**:
```json
{
  "user_id": "uuid",
  "current_time": "2025-10-09T18:30:00Z",
  "remaining_productive_hours": 3.5,
  "remaining_productive_minutes": 210,
  "remaining_tasks": [
    {
      "id": "task-7",
      "title": "Completar ejercicios de Python",
      "type": "goal",
      "estimated_duration_minutes": 60,
      "start_time": "2025-10-09T19:00:00Z"
    },
    {
      "id": "task-8",
      "title": "Yoga sesión nocturna",
      "type": "body",
      "estimated_duration_minutes": 45,
      "start_time": "2025-10-09T20:15:00Z"
    }
  ],
  "total_remaining_tasks": 3,
  "total_remaining_task_minutes": 150,
  "can_complete_all": true,
  "completion_percentage": 62.5,
  "full_day_summary": {
    "total_tasks_scheduled": 8,
    "efficiency_percentage": 85.71
  }
}
```

## 📊 Casos de Uso

### Caso 1: Planificación Matutina
**Escenario**: Usuario se despierta y quiere saber qué hacer hoy.

**Flujo**:
1. Llamar a `/optimize-day` para ver el plan completo del día
2. Revisar las tareas del slot "morning"
3. Comenzar con la tarea de mayor `priority_score`

### Caso 2: ¿Qué hago ahora?
**Escenario**: Usuario termina una tarea y quiere saber qué sigue.

**Flujo**:
1. Llamar a `/tasks-now`
2. Ver `recommended_tasks` ordenadas por prioridad
3. Si hay poco tiempo, elegir de `quick_wins`

### Caso 3: Revisión de Progreso
**Escenario**: Usuario quiere ver qué le falta del día.

**Flujo**:
1. Llamar a `/remaining-day`
2. Ver `remaining_tasks` y `completion_percentage`
3. Verificar si `can_complete_all` es true

### Caso 4: Deadline Urgente
**Escenario**: Una meta vence mañana.

**Flujo**:
- El algoritmo automáticamente:
  1. Detecta `days_until_deadline = 1`
  2. Aplica `urgency_multiplier = 3.0`
  3. Coloca la tarea al inicio del schedule
  4. Prioriza sobre tareas menos urgentes

## ⚙️ Configuración

### Variables del Algoritmo (en `time_optimizer_service.py`)

```python
# Ajustables según necesidad
SLEEP_HOURS = 8                    # Horas de sueño
PERSONAL_CARE_HOURS = 2            # Aseo, comida, transporte
BUFFER_MINUTES = 15                # Descanso entre tareas
DEFAULT_WAKE_UP = 6                # Hora de despertar
DEFAULT_SLEEP_TIME = 22            # Hora de dormir

# Pesos de prioridad
PRIORITY_WEIGHTS = {
    'goal': 3.0,
    'mind': 1.5,
    'body': 1.5
}

# Distribución ideal
IDEAL_DISTRIBUTION = {
    'goal': 0.60,   # 60%
    'mind': 0.20,   # 20%
    'body': 0.20    # 20%
}
```

## 🔍 Interpretación de Scores

### Efficiency Score (85.71%)
- **90-100%**: Excelente - Tiempo casi completamente utilizado
- **70-89%**: Bueno - Buen aprovechamiento del tiempo
- **50-69%**: Regular - Hay espacio para más tareas
- **<50%**: Bajo - Mucho tiempo sin usar

### Balance Score (97.8%)
- **95-100%**: Perfecto - Distribución muy cercana al ideal
- **80-94%**: Bueno - Distribución aceptable
- **60-79%**: Regular - Desbalance moderado
- **<60%**: Malo - Muy desbalanceado

### Productivity Score (90.55%)
- **85-100%**: Excelente productividad
- **70-84%**: Buena productividad
- **50-69%**: Productividad mejorable
- **<50%**: Baja productividad

## 🚀 Próximas Mejoras

1. **Machine Learning**: Aprender patrones de productividad del usuario
2. **Energía Personal**: Considerar niveles de energía por hora del día
3. **Contexto**: Integrar ubicación (casa, oficina, gimnasio)
4. **Interrupciones**: Predecir y ajustar por interrupciones comunes
5. **Gamificación**: Puntos por completar tareas en tiempo

## 📝 Notas Importantes

- Los deadlines de goals se toman del campo `end_at` de la tabla `goals`
- Las tareas completadas (`status = 'completed'`) se excluyen automáticamente
- El sistema respeta el límite de `hours_available_to_week` del perfil
- Los buffers de 15 minutos entre tareas previenen agotamiento
- Las tareas de goals con deadlines cercanos pueden "saltar" el balance ideal

---

**Versión del Algoritmo**: 2.0  
**Última Actualización**: 2025-10-09  
**Autor**: IAM Backend Team
