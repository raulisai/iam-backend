# Ejemplos cURL - Time Optimizer API

## 🔐 Primero: Obtener Token

```bash
# Login
curl -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tu_email@ejemplo.com",
    "password": "tu_password"
  }'

# Respuesta:
# {
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "user": { ... }
# }
```

**Guarda el token** para usarlo en los siguientes requests.

---

## 1️⃣ Calcular Tiempo Disponible

### Request
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/available-time" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Respuesta Ejemplo
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "has_profile": true,
  "profile": {
    "work_schedule": "9:00-17:00",
    "work_start": "09:00",
    "work_end": "17:00",
    "hours_per_week": 40,
    "hours_used_this_week": 15.5,
    "remaining_hours_this_week": 24.5
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

### Interpretación
- ✅ Tienes **6 horas libres** por día
- ⏰ Slot matutino: **2 horas** (6am-9am)
- ⏰ Slot vespertino: **5 horas** (5pm-10pm)
- 📊 Esta semana te quedan **24.5 horas** disponibles

---

## 2️⃣ Obtener Horario Optimizado del Día

### Request - Para HOY
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/optimize-day" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Request - Para fecha específica
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/optimize-day?date=2025-10-15" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Respuesta Ejemplo
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "date": "2025-10-09",
  "generated_at": "2025-10-09T06:00:00.000Z",
  "profile_summary": {
    "work_schedule": "9:00-17:00",
    "daily_free_hours": 6,
    "weekly_hours_remaining": 24.5
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
          "id": "occ-123",
          "task_id": "task-456",
          "title": "Completar proyecto final de Machine Learning",
          "description": "Implementar modelo y documentación",
          "type": "goal",
          "goal_title": "Completar Curso de ML",
          "goal_deadline": "2025-10-10T23:59:59Z",
          "days_until_deadline": 1,
          "urgency_multiplier": 3.0,
          "weight": 1,
          "estimated_duration_minutes": 90,
          "start_time": "2025-10-09T06:00:00Z",
          "end_time": "2025-10-09T07:30:00Z",
          "time_slot": "morning",
          "priority_score": 90.0,
          "status": "pending"
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
          "id": "occ-124",
          "title": "Revisar código del sprint",
          "type": "goal",
          "goal_deadline": "2025-10-11T17:00:00Z",
          "days_until_deadline": 2,
          "urgency_multiplier": 2.5,
          "estimated_duration_minutes": 60,
          "start_time": "2025-10-09T17:00:00Z",
          "end_time": "2025-10-09T18:00:00Z",
          "time_slot": "evening",
          "priority_score": 77.0
        },
        {
          "id": "mind-789",
          "title": "Meditar 30 minutos",
          "type": "mind",
          "estimated_duration_minutes": 30,
          "start_time": "2025-10-09T18:15:00Z",
          "end_time": "2025-10-09T18:45:00Z",
          "time_slot": "evening",
          "priority_score": 20.0
        },
        {
          "id": "body-321",
          "title": "Gimnasio - Rutina de fuerza",
          "type": "body",
          "estimated_duration_minutes": 60,
          "start_time": "2025-10-09T19:00:00Z",
          "end_time": "2025-10-09T20:00:00Z",
          "time_slot": "evening",
          "priority_score": 17.0
        }
      ]
    }
  },
  "summary": {
    "total_tasks_available": 15,
    "tasks_by_type_available": {
      "goals": 8,
      "mind": 4,
      "body": 3
    },
    "total_tasks_scheduled": 4,
    "tasks_by_type_scheduled": {
      "goals": 2,
      "mind": 1,
      "body": 1
    },
    "total_minutes_available": 420,
    "total_minutes_scheduled": 240,
    "total_hours_scheduled": 4.0,
    "efficiency_percentage": 57.14,
    "unscheduled_tasks": 11
  },
  "distribution_analysis": {
    "actual_distribution": {
      "goal": 62.5,
      "mind": 12.5,
      "body": 25.0
    },
    "ideal_distribution": {
      "goal": 60.0,
      "mind": 20.0,
      "body": 20.0
    },
    "deviation_from_ideal": {
      "goal": 2.5,
      "mind": -7.5,
      "body": 5.0
    },
    "balance_score": 95.0
  },
  "scores": {
    "efficiency_score": 57.14,
    "balance_score": 95.0,
    "productivity_score": 72.28
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

### Interpretación
- 🌅 **Mañana**: 1 tarea (proyecto urgente que vence mañana)
- 🌆 **Tarde**: 3 tareas (goal, mind, body)
- 📊 **Efficiency**: 57% (puedes agregar más tareas si quieres)
- ⚖️ **Balance**: 95% (excelente distribución)
- 🚀 **Productivity**: 72% (bueno)

---

## 3️⃣ ¿Qué Debo Hacer AHORA?

### Request
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/tasks-now" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Respuesta Ejemplo (a las 6:00 AM)
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_time": "2025-10-09T06:00:00.000Z",
  "time_slot": "morning",
  "remaining_minutes_in_slot": 180,
  "remaining_hours_in_slot": 3.0,
  "recommended_tasks": [
    {
      "id": "occ-123",
      "title": "Completar proyecto final de Machine Learning",
      "type": "goal",
      "goal_deadline": "2025-10-10T23:59:59Z",
      "days_until_deadline": 1,
      "estimated_duration_minutes": 90,
      "start_time": "2025-10-09T06:00:00Z",
      "end_time": "2025-10-09T07:30:00Z",
      "priority_score": 90.0,
      "urgency_multiplier": 3.0
    }
  ],
  "total_available_tasks": 1,
  "quick_wins": [],
  "message": "You have 180 minutes remaining in your morning slot"
}
```

### Respuesta Ejemplo (a las 6:00 PM)
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_time": "2025-10-09T18:00:00.000Z",
  "time_slot": "evening",
  "remaining_minutes_in_slot": 240,
  "remaining_hours_in_slot": 4.0,
  "recommended_tasks": [
    {
      "id": "occ-124",
      "title": "Revisar código del sprint",
      "type": "goal",
      "estimated_duration_minutes": 60,
      "start_time": "2025-10-09T18:00:00Z",
      "priority_score": 77.0
    },
    {
      "id": "mind-789",
      "title": "Meditar 30 minutos",
      "type": "mind",
      "estimated_duration_minutes": 30,
      "start_time": "2025-10-09T18:15:00Z",
      "priority_score": 20.0
    },
    {
      "id": "body-321",
      "title": "Gimnasio - Rutina de fuerza",
      "type": "body",
      "estimated_duration_minutes": 60,
      "start_time": "2025-10-09T19:00:00Z",
      "priority_score": 17.0
    }
  ],
  "total_available_tasks": 3,
  "quick_wins": [
    {
      "id": "mind-789",
      "title": "Meditar 30 minutos",
      "estimated_duration_minutes": 30
    }
  ],
  "message": "You have 240 minutes remaining in your evening slot"
}
```

### Interpretación
- ⏰ Tienes **240 minutos** (4 horas) disponibles
- 🎯 **Primero**: "Revisar código" (1 hora)
- ⚡ **Quick win**: "Meditar" (solo 30 min)
- 💪 **Después**: "Gimnasio" (1 hora)

---

## 4️⃣ ¿Qué Me Falta del Día?

### Request
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/remaining-day" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Respuesta Ejemplo (a las 6:30 PM)
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "current_time": "2025-10-09T18:30:00.000Z",
  "remaining_productive_hours": 3.5,
  "remaining_productive_minutes": 210,
  "remaining_tasks": [
    {
      "id": "mind-789",
      "title": "Meditar 30 minutos",
      "type": "mind",
      "estimated_duration_minutes": 30,
      "start_time": "2025-10-09T18:45:00Z"
    },
    {
      "id": "body-321",
      "title": "Gimnasio - Rutina de fuerza",
      "type": "body",
      "estimated_duration_minutes": 60,
      "start_time": "2025-10-09T19:15:00Z"
    }
  ],
  "total_remaining_tasks": 2,
  "total_remaining_task_minutes": 90,
  "can_complete_all": true,
  "completion_percentage": 50.0,
  "full_day_summary": {
    "total_tasks_scheduled": 4,
    "efficiency_percentage": 57.14
  }
}
```

### Interpretación
- ✅ Ya completaste **50%** de tus tareas
- ⏳ Te quedan **3.5 horas** de tiempo productivo
- 📋 Te faltan **2 tareas** (90 minutos)
- 🎉 **Sí puedes** completar todo hoy (90 min < 210 min)

---

## 🧪 Pruebas Completas

### Script completo de prueba
```bash
#!/bin/bash

# Variables
BASE_URL="http://localhost:5000"
TOKEN="TU_TOKEN_AQUI"

echo "=== 1. Tiempo Disponible ==="
curl -X GET "$BASE_URL/api/time-optimizer/available-time" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n\n=== 2. Horario de Hoy ==="
curl -X GET "$BASE_URL/api/time-optimizer/optimize-day" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n\n=== 3. Tareas para Ahora ==="
curl -X GET "$BASE_URL/api/time-optimizer/tasks-now" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n\n=== 4. Lo que Falta del Día ==="
curl -X GET "$BASE_URL/api/time-optimizer/remaining-day" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

**Nota**: Requiere `jq` instalado para formatear JSON. Si no lo tienes:
```bash
# En Ubuntu/Debian
sudo apt-get install jq

# En macOS
brew install jq

# En Windows (PowerShell)
# Usa: | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 🔧 Troubleshooting

### Error 401 - Unauthorized
```json
{
  "error": "Invalid or missing token"
}
```
**Solución**: Verifica que tu token esté correcto y no haya expirado.

### Error 404 - Profile not found
```json
{
  "error": "Profile not found",
  "message": "Please create a profile first"
}
```
**Solución**: Crea un perfil primero:
```bash
curl -X POST "$BASE_URL/api/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "work_schedules": "9:00-17:00",
    "hours_available_to_week": 40,
    "hours_used_to_week": 0
  }'
```

### No hay tareas en el schedule
**Posibles causas**:
1. No tienes tareas pendientes
2. Todas las tareas están completadas
3. La fecha especificada no tiene tareas

**Solución**: Crea algunas tareas de goals, mind o body.

---

## 📚 Más Información

- [Documentación Completa](./TIME_OPTIMIZER_SYSTEM.md)
- [Guía Rápida](./TIME_OPTIMIZER_QUICKSTART.md)
- [Diagramas](./TIME_OPTIMIZER_DIAGRAMS.md)
