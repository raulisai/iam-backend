# Setup del Sistema de Puntos - Guía Rápida

## 1. Aplicar Cambios en la Base de Datos

Ejecuta el siguiente SQL en tu base de datos:

```bash
# Si usas psql
psql -h YOUR_HOST -U YOUR_USER -d YOUR_DATABASE -f db_schemas/points_calculation_functions.sql

# O copia y pega el contenido del archivo en tu cliente SQL
```

Este archivo crea:
- ✅ Función `calculate_pending_points()` para calcular puntos de tareas pendientes
- ✅ Función `trg_update_goal_points_target()` para recalcular automáticamente
- ✅ Triggers en `tasks_mind`, `tasks_body` y `goal_tasks` para actualización automática

## 2. Verificar Columnas en Profiles

Asegúrate de que la tabla `profiles` tiene estas columnas (ya deberían existir):

```sql
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'profiles' 
  AND column_name IN ('goal_points_target', 'goal_points_earned');
```

## 3. Reiniciar el Servidor

```bash
# Instalar dependencias (si es necesario)
pip install -r requirements.txt

# Reiniciar
python app.py
```

## 4. Probar los Endpoints

```bash
# Login primero para obtener token
curl -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'

# Usar el token en los endpoints de puntos
TOKEN="your-token-here"

# Ver puntos actuales
curl -X GET "http://localhost:5000/api/points" \
  -H "Authorization: Bearer $TOKEN"

# Calcular target
curl -X POST "http://localhost:5000/api/points/calculate-target" \
  -H "Authorization: Bearer $TOKEN"
```

## 5. Endpoints Disponibles

### Gestión de Puntos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/points` | Obtener resumen de puntos |
| POST | `/api/points/calculate-target` | Calcular puntos disponibles |
| POST | `/api/points/add` | Sumar puntos ganados |
| POST | `/api/points/subtract` | Restar puntos ganados |
| POST | `/api/points/recalculate` | Recalcular todo |

### Completar Tareas (Gestión Automática de Puntos)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/tasks/mind/{task_id}/complete` | Completar tarea mind + sumar puntos |
| POST | `/api/tasks/mind/{task_id}/uncomplete` | Revertir tarea mind + restar puntos |
| POST | `/api/tasks/body/{task_id}/complete` | Completar tarea body + sumar puntos |
| POST | `/api/tasks/body/{task_id}/uncomplete` | Revertir tarea body + restar puntos |
| POST | `/api/goals/occurrences/{id}/complete` | Completar occurrence + sumar puntos |
| POST | `/api/goals/occurrences/{id}/uncomplete` | Revertir occurrence + restar puntos |

## 6. Documentación Completa

- **Sistema de Puntos**: `Documentation/POINTS_SYSTEM.md`
- **Ejemplos de Puntos**: `Documentation/POINTS_SYSTEM_EXAMPLES.md`
- **Endpoints de Completar Tareas**: `Documentation/TASK_COMPLETION_ENDPOINTS.md`

## Archivos Creados/Modificados

### Nuevos Archivos

```
services/points_service.py                          # Lógica de negocio de puntos
controllers/points_controller.py                    # Controladores de puntos
routes/points_routes.py                             # Rutas de puntos
db_schemas/points_calculation_functions.sql         # SQL functions y triggers
Documentation/POINTS_SYSTEM.md                      # Documentación del sistema
Documentation/POINTS_SYSTEM_EXAMPLES.md             # Ejemplos de uso
Documentation/TASK_COMPLETION_ENDPOINTS.md          # Endpoints de completar tareas
```

### Archivos Modificados

```
app.py                                               # Blueprint de points registrado
services/mind_task_service.py                       # complete/uncomplete functions
controllers/mind_task_controller.py                 # complete/uncomplete endpoints
routes/mind_task_routes.py                          # Rutas complete/uncomplete
services/body_task_service.py                       # complete/uncomplete functions
controllers/body_task_controller.py                 # complete/uncomplete endpoints
routes/body_task_routes.py                          # Rutas complete/uncomplete
services/goal_task_service.py                       # complete/uncomplete occurrences
controllers/goal_task_controller.py                 # complete/uncomplete endpoints
routes/goal_task_routes.py                          # Rutas complete/uncomplete
```

## Notas Importantes

⚠️ **Triggers Automáticos**: Al crear/actualizar/eliminar tareas, el `goal_points_target` se actualiza automáticamente.

⚠️ **Task Templates**: Las tareas deben tener un `template_id` válido con `reward_xp` > 0.

⚠️ **Snapshots**: Los scores se guardan diariamente en `performance_snapshots`.

⚠️ **Multiplicadores**: 
- Mind/Body: 1.0x
- Goal: 0.5x
