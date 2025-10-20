# Sistema de Puntos

Sistema completo de gestión de puntos para tareas y objetivos.

## Descripción General

El sistema gestiona dos tipos de puntos en la tabla `profiles`:

- **`goal_points_target`**: Puntos totales disponibles de todas las tareas pendientes (mind, body, goal)
- **`goal_points_earned`**: Puntos ganados al completar tareas

## Campos en la Base de Datos

### Tabla `profiles`

```sql
goal_points_target    NUMERIC NOT NULL DEFAULT 0  -- Total de puntos disponibles
goal_points_earned    NUMERIC NOT NULL DEFAULT 0  -- Puntos ganados
```

### Tabla `performance_snapshots`

```json
metrics: {
  "mind_score": 0,      // Score de tareas mind
  "body_score": 0,      // Score de tareas body
  "goal_score": 0,      // Score de tareas goal (50% del valor)
  "total_score": 0      // Suma total de scores
}
```

## Endpoints Disponibles

### 1. **GET /api/points**
Obtiene el resumen de puntos del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "goal_points_target": 500,
  "goal_points_earned": 250,
  "goal_points_remaining": 250,
  "completion_percentage": 50.0
}
```

---

### 2. **POST /api/points/calculate-target**
Calcula y actualiza `goal_points_target` sumando todos los puntos de tareas pendientes.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "mind_points": 200,
  "body_points": 150,
  "goal_points": 150,
  "total_target_points": 500
}
```

**Algoritmo:**
- Suma `reward_xp` de todas las tareas `tasks_mind` con status='pending'
- Suma `reward_xp` de todas las tareas `tasks_body` con status='pending'
- Suma `weight` de todas las `goal_tasks` activas y sus ocurrencias pendientes
- Actualiza `profiles.goal_points_target` con el total

---

### 3. **POST /api/points/add**
Suma puntos a `goal_points_earned` y actualiza scores en `performance_snapshots`.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "points": 50,
  "task_type": "mind"  // "mind" | "body" | "goal"
}
```

**Respuesta:**
```json
{
  "previous_earned": 200,
  "points_added": 50,
  "new_earned": 250,
  "task_type": "mind"
}
```

**Lógica de Scores:**
- **task_type = "mind"**: Suma puntos × 1.0 a `mind_score`
- **task_type = "body"**: Suma puntos × 1.0 a `body_score`
- **task_type = "goal"**: Suma puntos × 0.5 a `goal_score` (contribuye menos)
- Actualiza `total_score` como suma de los tres scores

---

### 4. **POST /api/points/subtract**
Resta puntos de `goal_points_earned` y actualiza scores en `performance_snapshots`.

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "points": 25,
  "task_type": "body"  // "mind" | "body" | "goal"
}
```

**Respuesta:**
```json
{
  "previous_earned": 250,
  "points_subtracted": 25,
  "new_earned": 225,
  "task_type": "body"
}
```

**Nota:** Los puntos ganados nunca pueden ser negativos (mínimo 0).

---

### 5. **POST /api/points/recalculate**
Recalcula todos los puntos (target y earned) del usuario.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "target_breakdown": {
    "mind_points": 200,
    "body_points": 150,
    "goal_points": 150,
    "total_target_points": 500
  },
  "points_summary": {
    "goal_points_target": 500,
    "goal_points_earned": 225,
    "goal_points_remaining": 275,
    "completion_percentage": 45.0
  }
}
```

---

## Flujo de Trabajo Típico

### Al Completar una Tarea Mind:

1. La tarea obtiene su `reward_xp` de `task_templates`
2. Llamar a `POST /api/points/add` con:
   ```json
   {
     "points": 50,
     "task_type": "mind"
   }
   ```
3. Esto suma 50 puntos a `goal_points_earned`
4. Suma 50 a `mind_score` en el snapshot de hoy
5. Recalcula `total_score`

### Al Crear/Eliminar Tareas:

1. Los triggers SQL automáticamente actualizan `goal_points_target`
2. O llamar manualmente a `POST /api/points/calculate-target`

---

## Configuración Requerida

### 1. Aplicar Función SQL

Ejecutar el archivo `db_schemas/points_calculation_functions.sql` en la base de datos:

```bash
psql -h <host> -U <user> -d <database> -f db_schemas/points_calculation_functions.sql
```

Este archivo crea:
- Función `calculate_pending_points()` para calcular puntos de tareas pendientes
- Triggers automáticos que actualizan `goal_points_target` cuando cambian las tareas

### 2. Verificar Columnas

Asegurarse de que la tabla `profiles` tiene las columnas:
```sql
goal_points_target NUMERIC NOT NULL DEFAULT 0
goal_points_earned NUMERIC NOT NULL DEFAULT 0
```

### 3. Verificar Templates

Las tareas deben tener su `template_id` configurado correctamente y el template debe tener un `reward_xp` > 0.

---

## Multiplicadores de Score

| Tipo de Tarea | Multiplicador | Descripción |
|---------------|---------------|-------------|
| `mind`        | 1.0           | Puntos completos al `mind_score` |
| `body`        | 1.0           | Puntos completos al `body_score` |
| `goal`        | 0.5           | 50% de puntos al `goal_score` |

---

## Ejemplo de Integración

```python
# Al completar una tarea mind con reward_xp = 50
import requests

headers = {
    'Authorization': f'Bearer {token}'
}

# 1. Sumar puntos ganados
response = requests.post(
    'http://localhost:5000/api/points/add',
    headers=headers,
    json={
        'points': 50,
        'task_type': 'mind'
    }
)

# 2. Obtener resumen actualizado
response = requests.get(
    'http://localhost:5000/api/points',
    headers=headers
)

print(response.json())
# {
#   "goal_points_target": 500,
#   "goal_points_earned": 275,
#   "goal_points_remaining": 225,
#   "completion_percentage": 55.0
# }
```

---

## Notas Importantes

1. **Triggers Automáticos**: Los cambios en `tasks_mind`, `tasks_body` y `goal_tasks` actualizan automáticamente `goal_points_target`

2. **Snapshots Diarios**: Los scores se guardan en `performance_snapshots` por día. Si no existe un snapshot para hoy, se crea uno nuevo.

3. **Validaciones**: Todos los endpoints validan que los puntos sean números positivos y que el `task_type` sea válido.

4. **Seguridad**: Todos los endpoints requieren autenticación JWT. El token debe incluirse en el header `Authorization: Bearer <token>`.

5. **Task Templates**: Es crucial que todas las tareas tengan un `template_id` válido con `reward_xp` configurado para que el cálculo de puntos funcione correctamente.
