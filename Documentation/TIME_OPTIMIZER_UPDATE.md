# Time Optimizer Update - Mejoras de Cálculo de Tiempo

## Resumen de Cambios

Se ha actualizado el endpoint de optimización de tiempo (`/api/time-optimizer/tasks-now`) para calcular correctamente el tiempo disponible considerando:

1. **Timezone del usuario** (America/Mexico_City por defecto)
2. **Días de trabajo** (campo `day_work` del perfil)
3. **Tiempo muerto** (campo `time_dead` del perfil)
4. **Cálculo correcto**: `Tiempo disponible = 24 - horas_trabajo - time_dead`

## Cambios Técnicos

### 1. Nueva Dependencia: pytz

Se agregó `pytz==2024.1` a `requirements.txt` para manejo de timezones.

```bash
pip install pytz==2024.1
```

### 2. Nuevas Funciones Auxiliares

#### `get_day_name_abbreviation(weekday: int) -> str`
Convierte el número del día de la semana a abreviatura española:
- 0 = L (Lunes)
- 1 = M (Martes)
- 2 = M (Miércoles)
- 3 = J (Jueves)
- 4 = V (Viernes)
- 5 = S (Sábado)
- 6 = D (Domingo)

#### `is_working_day(current_date: datetime, day_work: str) -> bool`
Verifica si la fecha actual es un día de trabajo basado en el campo `day_work` del perfil.

Ejemplo:
- Si `day_work = "L,M,M,J,V"` (Lunes a Viernes)
- Y hoy es sábado (S)
- Retorna `False` → No es día de trabajo → `work_hours = 0`

### 3. Actualización de `get_tasks_for_current_moment()`

La función principal ahora:

1. **Obtiene el perfil del usuario** con todos los campos necesarios:
   - `timezone` (ej: "America/Mexico_City")
   - `day_work` (ej: "L,M,M,J,V")
   - `time_dead` (ej: 9)
   - `work_schedules` (ej: "9:00-17:00")
   - `hours_available_to_week` (ej: 40)
   - `hours_used_to_week` (ej: 12.5)

2. **Calcula la hora actual** en el timezone del usuario:
   ```python
   current_time_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
   current_time = current_time_utc.astimezone(tz)
   ```

3. **Determina si es día de trabajo**:
   ```python
   is_work_day = is_working_day(current_time, day_work)
   ```

4. **Calcula horas de trabajo**:
   ```python
   if is_work_day:
       work_hours = calculate_duration_hours(work_start, work_end)
   else:
       work_hours = 0  # Fin de semana o día no laborable
   ```

5. **Calcula tiempo disponible**:
   ```python
   available_hours_today = 24 - work_hours - time_dead
   ```

   **Ejemplo para sábado (hoy)**:
   - `day_work = "L,M,M,J,V"` → No trabaja sábado
   - `work_hours = 0`
   - `time_dead = 9`
   - `available_hours_today = 24 - 0 - 9 = 15 horas`

6. **Organiza las tareas** por tipo y las programa con horarios:
   - `goal_tasks[]`
   - `mind_tasks[]`
   - `body_tasks[]`

## Formato de Respuesta JSON

El endpoint ahora retorna el siguiente formato:

```json
{
  "body_tasks": [
    {
      "id": "uuid",
      "task_id": "uuid",
      "title": "Yoga Matutino",
      "description": "",
      "type": "body",
      "estimated_duration_minutes": 30,
      "priority_score": 20,
      "urgency_multiplier": 1,
      "scheduled_at": "2025-10-09T21:03:02.852594+00:00",
      "status": "pending",
      "start_time": "2025-10-14T20:30:00",
      "end_time": "2025-10-14T21:00:00",
      "time_slot": "morning"
    }
  ],
  "goal_tasks": [
    {
      "id": "uuid",
      "task_id": "uuid",
      "title": "Pararme y bañarme con agua fria",
      "description": "Levantarme no estar de gay y bañarme con agua fria..",
      "type": "goal",
      "goal_title": "Construir un hábito",
      "goal_deadline": "2025-10-29",
      "days_until_deadline": 17,
      "urgency_multiplier": 1,
      "weight": 100000,
      "estimated_duration_minutes": 60,
      "priority_score": 3000002,
      "scheduled_at": null,
      "status": "pending",
      "start_time": "2025-10-12T06:00:00",
      "end_time": "2025-10-12T07:00:00",
      "time_slot": "morning"
    }
  ],
  "mind_tasks": [
    {
      "id": "uuid",
      "task_id": "uuid",
      "title": "Networking Profesional",
      "description": "",
      "type": "mind",
      "estimated_duration_minutes": 30,
      "priority_score": 20,
      "urgency_multiplier": 1,
      "scheduled_at": "2025-10-10T05:00:09.846444+00:00",
      "status": "pending",
      "start_time": "2025-10-14T16:45:00",
      "end_time": "2025-10-14T17:15:00",
      "time_slot": "morning"
    }
  ],
  "current_time": "2025-10-12T02:51:39.452336",
  "message": "You have 3000 minutes remaining in your morning slot",
  "remaining_hours_in_slot_week": 50,
  "total_body_tasks": 2,
  "total_goal_tasks": 3,
  "total_mind_tasks": 1,
  "total_time_used_for_tasks": 255,
  "remaining_minutes_in_slot_week": 3000,
  "total_available_tasks": 6,
  "user_id": "6a012777-fdaf-4ee1-b41b-b59f48374f59",
  "is_working_day": false,
  "available_hours_today": 15,
  "work_hours_today": 0,
  "time_dead": 9
}
```

## Campos Adicionales en la Respuesta

- `is_working_day`: Boolean que indica si hoy es día de trabajo
- `available_hours_today`: Horas disponibles hoy (24 - work_hours - time_dead)
- `work_hours_today`: Horas de trabajo hoy (0 si no es día laborable)
- `time_dead`: Tiempo muerto del perfil

## Uso del Endpoint

### Request

```bash
GET /api/time-optimizer/tasks-now
Authorization: Bearer <jwt_token>
```

### Ejemplo de Uso

Para un usuario en CDMX (timezone: America/Mexico_City) en sábado:

**Perfil del usuario:**
```json
{
  "timezone": "America/Mexico_City",
  "day_work": "L,M,M,J,V",
  "time_dead": 9,
  "work_schedules": "9:00-17:00",
  "hours_available_to_week": 40,
  "hours_used_to_week": 12.5
}
```

**Cálculo:**
- Hoy es sábado (S)
- `day_work = "L,M,M,J,V"` → No incluye S
- Por lo tanto: `work_hours = 0`
- `available_hours_today = 24 - 0 - 9 = 15 horas`

**Respuesta:**
- `is_working_day: false`
- `work_hours_today: 0`
- `available_hours_today: 15`
- Tareas organizadas y programadas desde la hora actual

## Notas Importantes

1. **Timezone**: El sistema usa el timezone del perfil del usuario. Si no está configurado, usa `America/Mexico_City` por defecto.

2. **Días de Trabajo**: Si el campo `day_work` no existe o está vacío, el sistema asume Lunes a Viernes (L,M,M,J,V) por defecto.

3. **Time Dead**: Si no está configurado, usa 9 horas por defecto.

4. **Fin de Semana**: Los fines de semana o días no laborables tienen más tiempo disponible ya que no hay horas de trabajo.

5. **Fallback**: Si pytz no está disponible o el timezone es inválido, el sistema usa UTC como fallback.

## Testing

Para probar el endpoint:

```bash
# Asegúrate de tener el token JWT
curl -X GET "http://localhost:5000/api/time-optimizer/tasks-now" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Campos del Perfil Requeridos

Para que el endpoint funcione correctamente, el perfil debe tener:

| Campo | Tipo | Descripción | Ejemplo | Default |
|-------|------|-------------|---------|---------|
| `timezone` | string | Timezone del usuario | "America/Mexico_City" | "America/Mexico_City" |
| `day_work` | string | Días de trabajo separados por comas | "L,M,M,J,V" | "L,M,M,J,V" |
| `time_dead` | numeric | Horas de tiempo muerto (sueño, etc.) | 9 | 9 |
| `work_schedules` | string | Horario de trabajo | "9:00-17:00" | "9:00-17:00" |
| `hours_available_to_week` | numeric | Horas disponibles por semana | 40 | 40 |
| `hours_used_to_week` | numeric | Horas usadas esta semana | 12.5 | 0 |

## Próximos Pasos

1. Actualizar la documentación de la API
2. Agregar tests unitarios para las nuevas funciones
3. Considerar agregar soporte para múltiples work_schedules (mañana/tarde)
4. Agregar validación de timezone en la creación/actualización de perfil
