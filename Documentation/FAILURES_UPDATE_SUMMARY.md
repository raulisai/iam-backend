# Actualización de la Estructura de Failures

## 📋 Resumen de Cambios

Se ha actualizado la estructura de la tabla `failures` para incluir nuevas columnas que permiten un análisis más profundo de los fallos y su prevención.

## 🆕 Nueva Estructura de la Tabla

| Nombre | Formato | Tipo | Descripción |
|--------|---------|------|-------------|
| `id` | uuid | string | Identificador único del registro |
| `user_id` | uuid | string | ID del usuario |
| `task_table` | text | string | Tabla de la tarea: "tasks_mind" o "tasks_body" |
| `task_id` | uuid | string | ID de la tarea que falló |
| `reason` | text | string | Razón del fallo |
| `severity` | text | string | Severidad: "minor", "major", "critical" |
| `created_at` | timestamp with time zone | string | Fecha de creación (antes: occurred_at) |
| `notes` | text | string | Notas adicionales (opcional) |
| **`title`** | text | string | **NUEVO: Título o resumen del fallo** |
| **`rootCause`** | text | string | **NUEVO: Análisis de causa raíz** |
| **`prevention`** | text | string | **NUEVO: Estrategia de prevención** |

## 🔄 Cambios Realizados

### 1. Routes (`routes/failure_routes.py`)
- ✅ Actualizado el schema de respuesta GET para incluir `title`, `rootCause`, `prevention`
- ✅ Actualizado el schema de request POST para incluir las nuevas columnas
- ✅ Actualizado el schema de respuesta POST
- ✅ Cambiado `occurred_at` por `created_at` en toda la documentación Swagger

### 2. Documentación API (`Documentation/API_Tasks.md`)
- ✅ Actualizado el ejemplo de respuesta GET para incluir las nuevas columnas
- ✅ Actualizado el request body de POST con las nuevas columnas opcionales
- ✅ Agregadas descripciones claras de cada nueva columna

### 3. Ejemplos cURL (`Documentation/CURL_EXAMPLES.md`)
- ✅ Actualizado el ejemplo de POST con las nuevas columnas
- ✅ Incluidos ejemplos prácticos de uso

### 4. Documentación General (`Documentation/API_General.md`)
- ✅ Actualizada la descripción de la tabla `failures` con los nuevos campos

## 📝 Ejemplos de Uso

### GET - Obtener Failures
```bash
curl -X GET http://localhost:5000/api/failures \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "task_table": "tasks_mind",
    "task_id": "uuid",
    "reason": "Olvidé hacer la tarea",
    "severity": "minor",
    "notes": "Reprogramar para mañana",
    "title": "Falta de gestión del tiempo",
    "rootCause": "Sobrecarga de trabajo sin planificación adecuada",
    "prevention": "Implementar técnica Pomodoro y planificación semanal",
    "created_at": "2025-10-05T00:00:00Z"
  }
]
```

### POST - Crear Failure
```bash
curl -X POST http://localhost:5000/api/failures \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_table": "tasks_mind",
    "task_id": "task-uuid",
    "reason": "Olvidé hacer la tarea",
    "severity": "minor",
    "notes": "Reprogramar para mañana",
    "title": "Falta de gestión del tiempo",
    "rootCause": "Sobrecarga de trabajo sin planificación adecuada",
    "prevention": "Implementar técnica Pomodoro y planificación semanal"
  }'
```

## 🎯 Campos Obligatorios vs Opcionales

### Obligatorios
- `task_table` (string: "tasks_mind" | "tasks_body")
- `task_id` (uuid)
- `reason` (string)

### Opcionales
- `severity` (string: "minor" | "major" | "critical") - Default: "minor"
- `notes` (string)
- `title` (string) - 🆕 NUEVO
- `rootCause` (string) - 🆕 NUEVO
- `prevention` (string) - 🆕 NUEVO

## 📚 Beneficios de los Nuevos Campos

### `title`
- Resumen rápido del tipo de fallo
- Facilita la categorización y búsqueda
- Mejora la visualización en dashboards

### `rootCause`
- Análisis profundo de la causa del fallo
- Permite identificar patrones subyacentes
- Facilita la toma de decisiones informadas

### `prevention`
- Estrategias concretas para evitar futuros fallos
- Base de conocimiento de mejores prácticas
- Apoyo para el crecimiento personal y profesional

## ⚠️ Notas Importantes

1. **Retrocompatibilidad**: Los campos nuevos son opcionales, por lo que las integraciones existentes seguirán funcionando sin cambios.

2. **Migración de Datos**: Si tienes datos existentes en la tabla `failures`, los nuevos campos serán `NULL` por defecto.

3. **Renombrado de columna**: `occurred_at` ahora es `created_at` (más consistente con otras tablas).

4. **Servicios y Controladores**: No requieren cambios, ya que manejan dinámicamente todos los campos que se envíen.

## 🚀 Próximos Pasos

1. ✅ Actualizar la base de datos con las nuevas columnas
2. ✅ Actualizar la documentación Swagger
3. ✅ Actualizar ejemplos en la documentación
4. 🔲 Actualizar frontend para incluir los nuevos campos
5. 🔲 Agregar validaciones adicionales si es necesario
6. 🔲 Implementar análisis de patrones basado en rootCause

## 📞 Soporte

Si tienes preguntas sobre estos cambios, consulta:
- `Documentation/API_Tasks.md` - Documentación completa de endpoints
- `Documentation/CURL_EXAMPLES.md` - Ejemplos prácticos
- Swagger UI: `http://localhost:5000/apidocs/` - Documentación interactiva
