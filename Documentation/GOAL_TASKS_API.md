# Goal Tasks API Documentation

Este documento describe los nuevos endpoints para gestionar **tareas derivadas de goals** (`goal_tasks`) y sus **ocurrencias** (`task_occurrences`).

## 📋 Tabla de Contenidos

- [Conceptos Clave](#conceptos-clave)
- [Endpoints de Goal Tasks](#endpoints-de-goal-tasks)
- [Endpoints de Occurrences](#endpoints-de-occurrences)
- [Endpoint de Progreso](#endpoint-de-progreso)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🎯 Conceptos Clave

### Goal Tasks
Son tareas específicas ligadas a un goal. Pueden ser:
- **One-time tasks**: Tareas puntuales con fecha de vencimiento (`due_at`)
- **Recurring tasks**: Tareas recurrentes con regla RRULE (`schedule_rrule`)

### Task Occurrences
Son instancias concretas de ejecución de una tarea. Para tareas recurrentes, se genera una ocurrencia por cada fecha programada.

### Task Logs
Registran acciones sobre las ocurrencias (`completed`, `skipped`, `started`). El sistema calcula el progreso del goal basándose en estos logs.

### Cálculo de Progreso
- Si el goal tiene `target_value > 0`: suma de valores numéricos en metadata de logs completados
- Si no hay `target_value`: porcentaje de ocurrencias completadas vs totales

---

## 🎯 Endpoints de Goal Tasks

### 1. Obtener todas las tareas de un goal

```http
GET /api/goals/{goal_id}/tasks
Authorization: Bearer {token}
```

**Response 200:**
```json
[
  {
    "id": "uuid",
    "goal_id": "uuid",
    "user_id": "uuid",
    "title": "Meditar 10 minutos",
    "description": "Sesión de meditación matutina",
    "type": "mind",
    "required": true,
    "weight": 1,
    "due_at": null,
    "schedule_rrule": "FREQ=DAILY;BYHOUR=8",
    "created_at": "2025-10-07T10:00:00Z"
  }
]
```

---

### 2. Crear una tarea para un goal

```http
POST /api/goals/{goal_id}/tasks
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (Tarea Recurrente):**
```json
{
  "title": "Meditar 10 minutos",
  "description": "Sesión de meditación matutina",
  "type": "mind",
  "required": true,
  "weight": 1,
  "schedule_rrule": "FREQ=DAILY;BYHOUR=8;BYMINUTE=0"
}
```

**Body (Tarea Puntual):**
```json
{
  "title": "Comprar libro de meditación",
  "description": "Libro recomendado",
  "type": "one_off",
  "required": false,
  "weight": 0.5,
  "due_at": "2025-10-15T12:00:00Z"
}
```

**Campos:**
- `title` (requerido): Título de la tarea
- `description`: Descripción detallada
- `type`: Tipo de tarea (`mind`, `body`, `habit`, `one_off`)
- `required` (default: true): Si cuenta para el progreso del goal
- `weight` (default: 1): Ponderación en el cálculo de progreso
- `due_at`: Fecha de vencimiento (para tareas puntuales)
- `schedule_rrule`: Regla de recurrencia RFC 5545 (para tareas recurrentes)

**Response 201:** Tarea creada

---

### 3. Obtener una tarea específica

```http
GET /api/goals/tasks/{task_id}
Authorization: Bearer {token}
```

---

### 4. Actualizar una tarea

```http
PUT /api/goals/tasks/{task_id}
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "title": "Meditar 15 minutos",
  "weight": 1.5
}
```

---

### 5. Eliminar una tarea

```http
DELETE /api/goals/tasks/{task_id}
Authorization: Bearer {token}
```

**Nota:** Esto eliminará en cascada todas las ocurrencias asociadas.

---

## 📅 Endpoints de Occurrences

### 1. Obtener ocurrencias de una tarea

```http
GET /api/goals/tasks/{task_id}/occurrences?start_date=2025-10-01&end_date=2025-10-31&include_status=true
Authorization: Bearer {token}
```

**Query Parameters:**
- `start_date` (opcional): Filtrar desde esta fecha (ISO 8601)
- `end_date` (opcional): Filtrar hasta esta fecha (ISO 8601)
- `include_status` (default: true): Incluir status actual desde logs

**Response 200:**
```json
[
  {
    "id": "uuid",
    "task_id": "uuid",
    "scheduled_at": "2025-10-08T08:00:00Z",
    "created_at": "2025-10-07T10:00:00Z",
    "status": "completed",
    "last_action": "completed",
    "last_value": 10
  },
  {
    "id": "uuid",
    "task_id": "uuid",
    "scheduled_at": "2025-10-09T08:00:00Z",
    "created_at": "2025-10-07T10:00:00Z",
    "status": "pending",
    "last_action": null,
    "last_value": null
  }
]
```

---

### 2. Crear una ocurrencia manualmente

```http
POST /api/goals/tasks/{task_id}/occurrences
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "scheduled_at": "2025-10-08T08:00:00Z"
}
```

**Response 201:** Ocurrencia creada
**Response 409:** Ya existe una ocurrencia para esa fecha/hora

---

### 3. Generar ocurrencias automáticamente

```http
POST /api/goals/tasks/{task_id}/occurrences/generate
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (opcional):**
```json
{
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z"
}
```

Si no se especifican fechas, genera ocurrencias para el mes actual.

**Response 201:**
```json
{
  "generated": 31,
  "occurrences": [...]
}
```

---

### 4. Obtener una ocurrencia específica

```http
GET /api/goals/occurrences/{occurrence_id}
Authorization: Bearer {token}
```

**Response 200:**
```json
{
  "id": "uuid",
  "task_id": "uuid",
  "scheduled_at": "2025-10-08T08:00:00Z",
  "created_at": "2025-10-07T10:00:00Z",
  "status": "completed",
  "last_action": "completed",
  "last_value": 10
}
```

---

### 5. Eliminar una ocurrencia

```http
DELETE /api/goals/occurrences/{occurrence_id}
Authorization: Bearer {token}
```

---

### 6. Registrar acción sobre una ocurrencia (IMPORTANTE)

```http
POST /api/goals/occurrences/{occurrence_id}/log
Authorization: Bearer {token}
Content-Type: application/json
```

**Body (Completar):**
```json
{
  "action": "completed",
  "metadata": {
    "value": 10,
    "notes": "Excelente sesión"
  }
}
```

**Body (Saltar):**
```json
{
  "action": "skipped",
  "metadata": {
    "reason": "Falta de tiempo"
  }
}
```

**Body (Iniciar):**
```json
{
  "action": "started",
  "metadata": {}
}
```

**Acciones comunes:**
- `completed`: Tarea completada
- `skipped`: Tarea saltada/omitida
- `started`: Tarea iniciada
- `paused`: Tarea pausada
- `cancelled`: Tarea cancelada

**Response 201:** Log creado (automáticamente actualiza el progreso del goal)

---

### 7. Obtener todos los logs de una ocurrencia

```http
GET /api/goals/occurrences/{occurrence_id}/logs
Authorization: Bearer {token}
```

**Response 200:**
```json
[
  {
    "id": "uuid",
    "task_table": "task_occurrences",
    "task_id": "uuid",
    "user_id": "uuid",
    "action": "completed",
    "timestamp": "2025-10-08T09:30:00Z",
    "metadata": {
      "value": 10,
      "notes": "Excelente sesión"
    }
  }
]
```

---

## 📊 Endpoint de Progreso

### Obtener progreso de un goal

```http
GET /api/goals/{goal_id}/progress
Authorization: Bearer {token}
```

**Response 200:**
```json
{
  "goal_id": "uuid",
  "progress_percent": 75.5
}
```

Este endpoint usa la vista `goal_progress_view` que calcula automáticamente el progreso basándose en:
- Logs de tipo `completed` en las ocurrencias
- Valores numéricos en `metadata.value` (si existen)
- Target value del goal (si está definido)

---

## 🔍 Ejemplos de Uso

### Ejemplo 1: Goal de Meditación (30 días)

#### Paso 1: Crear el Goal
```http
POST /api/goals
{
  "title": "Meditar 30 días seguidos",
  "target_value": 30,
  "metric_key": "meditation_days",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31"
}
```

#### Paso 2: Crear tarea recurrente diaria
```http
POST /api/goals/{goal_id}/tasks
{
  "title": "Meditación matutina",
  "type": "mind",
  "schedule_rrule": "FREQ=DAILY;BYHOUR=8"
}
```

#### Paso 3: Generar ocurrencias para el mes
```http
POST /api/goals/tasks/{task_id}/occurrences/generate
{
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z"
}
```

#### Paso 4: Marcar ocurrencia como completada
```http
POST /api/goals/occurrences/{occurrence_id}/log
{
  "action": "completed",
  "metadata": {
    "value": 1
  }
}
```

#### Paso 5: Ver progreso
```http
GET /api/goals/{goal_id}/progress
# Response: { "goal_id": "uuid", "progress_percent": 3.33 }
```

---

### Ejemplo 2: Goal de Ejercicio (Correr 100km)

#### Paso 1: Crear el Goal
```http
POST /api/goals
{
  "title": "Correr 100km en octubre",
  "target_value": 100,
  "metric_key": "running_km",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31"
}
```

#### Paso 2: Crear tarea recurrente (3 veces por semana)
```http
POST /api/goals/{goal_id}/tasks
{
  "title": "Correr",
  "type": "body",
  "schedule_rrule": "FREQ=WEEKLY;BYDAY=MO,WE,FR;BYHOUR=7"
}
```

#### Paso 3: Generar ocurrencias
```http
POST /api/goals/tasks/{task_id}/occurrences/generate
```

#### Paso 4: Registrar carrera completada con distancia
```http
POST /api/goals/occurrences/{occurrence_id}/log
{
  "action": "completed",
  "metadata": {
    "value": 8.5,
    "notes": "8.5 km en 45 minutos"
  }
}
```

#### Paso 5: Ver progreso
```http
GET /api/goals/{goal_id}/progress
# Response: { "goal_id": "uuid", "progress_percent": 8.5 }
# (8.5km / 100km = 8.5%)
```

---

## 🔐 Reglas de RRULE (RFC 5545)

Las reglas de recurrencia siguen el estándar RFC 5545. Ejemplos:

### Diaria
```
FREQ=DAILY;BYHOUR=8;BYMINUTE=0
```

### Semanal (Lunes, Miércoles, Viernes)
```
FREQ=WEEKLY;BYDAY=MO,WE,FR;BYHOUR=7;BYMINUTE=30
```

### Mensual (Primer día del mes)
```
FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9
```

### Cada 2 días
```
FREQ=DAILY;INTERVAL=2;BYHOUR=10
```

### Días de semana solamente
```
FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=8
```

---

## ⚡ Características Importantes

### 1. Cálculo Automático de Progreso
El trigger `task_logs_progress_trg` actualiza automáticamente `goals.progress` cada vez que se registra un log.

### 2. Validación de Ownership
Todos los endpoints verifican que el usuario autenticado sea el dueño del goal/task/occurrence.

### 3. Cascade Delete
Al eliminar un goal, se eliminan automáticamente todas sus tasks y occurrences (gracias a `ON DELETE CASCADE`).

### 4. Prevención de Duplicados
No se pueden crear dos ocurrencias con la misma `task_id` y `scheduled_at`.

### 5. Metadata Flexible
El campo `metadata` en logs es un JSONB que permite almacenar cualquier información adicional (valores numéricos, notas, duración, etc).

---

## 📝 Notas Finales

- Los endpoints están documentados en Swagger: `/apidocs`
- Todas las fechas deben estar en formato ISO 8601
- El progreso se calcula en base a la vista `goal_progress_view`
- Las ocurrencias se pueden generar automáticamente o crear manualmente
- El sistema soporta tanto tareas puntuales como recurrentes
