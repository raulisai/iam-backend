# Endpoints de Completar/Revertir Tareas

Endpoints unificados para completar y revertir tareas con gestión automática de puntos.

## Descripción General

Se han creado endpoints especializados para completar y revertir tareas que gestionan automáticamente:
- ✅ Cambio de estado de la tarea (completed ↔ pending)
- ✅ Suma/resta de puntos en `goal_points_earned`
- ✅ Actualización de scores en `performance_snapshots`
- ✅ Actualización de `goal_points_target` (vía triggers SQL)

## Endpoints Disponibles

### 1. Mind Tasks

#### **POST /api/tasks/mind/{task_id}/complete**
Completa una tarea mind y suma puntos automáticamente.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "task": {
    "id": "task-uuid",
    "status": "completed",
    "completed_at": "2025-10-18T18:00:00Z",
    ...
  },
  "points": {
    "previous_earned": 100,
    "points_added": 50,
    "new_earned": 150,
    "task_type": "mind"
  }
}
```

**Proceso:**
1. Verifica que la tarea existe y pertenece al usuario
2. Verifica que no esté ya completada
3. Obtiene `reward_xp` del template
4. Actualiza status a 'completed' y completa `completed_at`
5. Suma puntos a `goal_points_earned`
6. Actualiza `mind_score` en snapshot de hoy

---

#### **POST /api/tasks/mind/{task_id}/uncomplete**
Revierte una tarea mind completada y resta puntos.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "task": {
    "id": "task-uuid",
    "status": "pending",
    "completed_at": null,
    ...
  },
  "points": {
    "previous_earned": 150,
    "points_subtracted": 50,
    "new_earned": 100,
    "task_type": "mind"
  }
}
```

**Proceso:**
1. Verifica que la tarea existe y pertenece al usuario
2. Verifica que esté completada
3. Obtiene `reward_xp` del template
4. Actualiza status a 'pending' y limpia `completed_at`
5. Resta puntos de `goal_points_earned`
6. Resta de `mind_score` en snapshot de hoy

---

### 2. Body Tasks

#### **POST /api/tasks/body/{task_id}/complete**
Completa una tarea body y suma puntos automáticamente.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "task": {
    "id": "task-uuid",
    "status": "completed",
    "completed_at": "2025-10-18T18:00:00Z",
    ...
  },
  "points": {
    "previous_earned": 150,
    "points_added": 30,
    "new_earned": 180,
    "task_type": "body"
  }
}
```

**Proceso:**
Idéntico al de mind tasks pero actualiza `body_score` en el snapshot.

---

#### **POST /api/tasks/body/{task_id}/uncomplete**
Revierte una tarea body completada y resta puntos.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "task": {
    "id": "task-uuid",
    "status": "pending",
    "completed_at": null,
    ...
  },
  "points": {
    "previous_earned": 180,
    "points_subtracted": 30,
    "new_earned": 150,
    "task_type": "body"
  }
}
```

---

### 3. Goal Task Occurrences

Las goal tasks funcionan con **occurrences** (instancias de ejecución).

#### **POST /api/goals/occurrences/{occurrence_id}/complete**
Completa una occurrence de goal task y suma puntos.

**Headers:**
```
Authorization: Bearer <token>
```

**Body (opcional):**
```json
{
  "value": 5.5
}
```
*`value` es opcional y se usa para goals basados en métricas*

**Respuesta:**
```json
{
  "occurrence": {
    "id": "occurrence-uuid",
    "task_id": "task-uuid",
    "scheduled_at": "2025-10-18T08:00:00Z",
    "status": "completed",
    "last_action": "completed",
    "last_value": 5.5
  },
  "log": {
    "id": "log-uuid",
    "action": "completed",
    "timestamp": "2025-10-18T18:00:00Z",
    "metadata": {
      "value": 5.5
    }
  },
  "points": {
    "previous_earned": 180,
    "points_added": 10,
    "new_earned": 190,
    "task_type": "goal"
  }
}
```

**Proceso:**
1. Verifica que el occurrence existe
2. Verifica que la tarea pertenece al usuario
3. Verifica que no esté ya completado
4. Registra un log con action='completed'
5. Usa el `weight` de la tarea como puntos
6. Suma puntos × 0.5 a `goal_score` (contribuye 50%)

---

#### **POST /api/goals/occurrences/{occurrence_id}/uncomplete**
Revierte una occurrence completada y resta puntos.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "occurrence": {
    "id": "occurrence-uuid",
    "task_id": "task-uuid",
    "scheduled_at": "2025-10-18T08:00:00Z",
    "status": "uncompleted",
    "last_action": "uncompleted",
    "last_value": null
  },
  "log": {
    "id": "log-uuid",
    "action": "uncompleted",
    "timestamp": "2025-10-18T18:05:00Z",
    "metadata": {}
  },
  "points": {
    "previous_earned": 190,
    "points_subtracted": 10,
    "new_earned": 180,
    "task_type": "goal"
  }
}
```

---

## Ejemplos de Uso

### Completar Tarea Mind

```bash
curl -X POST "http://localhost:5000/api/tasks/mind/123-uuid/complete" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Revertir Tarea Body

```bash
curl -X POST "http://localhost:5000/api/tasks/body/456-uuid/uncomplete" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Completar Goal Occurrence con Valor

```bash
curl -X POST "http://localhost:5000/api/goals/occurrences/789-uuid/complete" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": 5.5}'
```

---

## Flujo Completo: Mind Task

```python
import requests

BASE_URL = "http://localhost:5000"
TOKEN = "your-jwt-token"

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

# 1. Crear una tarea mind
task_response = requests.post(
    f"{BASE_URL}/api/tasks/mind",
    headers=headers,
    json={
        "template_id": "template-uuid",
        "created_by": "user",
        "scheduled_at": "2025-10-18T08:00:00Z"
    }
)
task = task_response.json()
task_id = task['id']

# 2. Completar la tarea (automáticamente suma puntos)
complete_response = requests.post(
    f"{BASE_URL}/api/tasks/mind/{task_id}/complete",
    headers=headers
)
result = complete_response.json()

print(f"Tarea completada: {result['task']['status']}")
print(f"Puntos ganados: {result['points']['points_added']}")
print(f"Total puntos: {result['points']['new_earned']}")

# 3. Si fue un error, revertir
uncomplete_response = requests.post(
    f"{BASE_URL}/api/tasks/mind/{task_id}/uncomplete",
    headers=headers
)
revert_result = uncomplete_response.json()

print(f"Tarea revertida: {revert_result['task']['status']}")
print(f"Puntos restados: {revert_result['points']['points_subtracted']}")
```

---

## Flujo Completo: Goal Task

```python
# 1. Crear goal task
goal_task_response = requests.post(
    f"{BASE_URL}/api/goals/goal-uuid/tasks",
    headers=headers,
    json={
        "title": "Meditar 10 minutos",
        "type": "mind",
        "weight": 10,
        "schedule_rrule": "FREQ=DAILY;BYHOUR=8"
    }
)
goal_task = goal_task_response.json()

# 2. Generar occurrences para el mes
generate_response = requests.post(
    f"{BASE_URL}/api/goals/tasks/{goal_task['id']}/occurrences/generate",
    headers=headers,
    json={
        "start_date": "2025-10-01T00:00:00Z",
        "end_date": "2025-10-31T23:59:59Z"
    }
)

# 3. Obtener occurrences
occurrences_response = requests.get(
    f"{BASE_URL}/api/goals/tasks/{goal_task['id']}/occurrences",
    headers=headers
)
occurrences = occurrences_response.json()

# 4. Completar la primera occurrence
first_occurrence = occurrences[0]
complete_occ_response = requests.post(
    f"{BASE_URL}/api/goals/occurrences/{first_occurrence['id']}/complete",
    headers=headers,
    json={"value": 10}  # Opcional
)

result = complete_occ_response.json()
print(f"Occurrence completada: {result['occurrence']['status']}")
print(f"Puntos: {result['points']['points_added']}")

# 5. Revertir si es necesario
uncomplete_occ_response = requests.post(
    f"{BASE_URL}/api/goals/occurrences/{first_occurrence['id']}/uncomplete",
    headers=headers
)
```

---

## Validaciones y Errores

### **400 - Bad Request**
- "Task already completed" - Intentaste completar una tarea ya completada
- "Task is not completed" - Intentaste revertir una tarea que no está completada
- "Occurrence already completed" - El occurrence ya fue completado
- "Occurrence is not completed" - El occurrence no está completado

### **401 - Unauthorized**
- Token JWT inválido o expirado

### **403 - Forbidden**
- La tarea no pertenece al usuario autenticado

### **404 - Not Found**
- Tarea u occurrence no encontrado

### **500 - Internal Server Error**
- Error al procesar la solicitud

---

## Resumen de Multiplicadores de Puntos

| Tipo de Tarea | Puntos Base | Multiplicador Score | Score Actualizado |
|---------------|-------------|---------------------|-------------------|
| **Mind**      | `reward_xp` | 1.0x                | `mind_score`      |
| **Body**      | `reward_xp` | 1.0x                | `body_score`      |
| **Goal**      | `weight`    | 0.5x                | `goal_score`      |

---

## Beneficios de Estos Endpoints

✅ **Simplicidad**: Un solo endpoint completa la tarea Y suma puntos  
✅ **Atomicidad**: Todo sucede en una transacción  
✅ **Consistencia**: Los puntos siempre están sincronizados con el estado de la tarea  
✅ **Reversibilidad**: Fácil de revertir errores sin cálculos manuales  
✅ **Trazabilidad**: Todas las acciones quedan registradas en logs (goal tasks)  

---

## Ver También

- **Sistema de Puntos**: `Documentation/POINTS_SYSTEM.md`
- **Ejemplos de Puntos**: `Documentation/POINTS_SYSTEM_EXAMPLES.md`
- **Setup de Puntos**: `POINTS_SETUP.md`
