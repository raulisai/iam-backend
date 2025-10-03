# API Documentation - IAM Backend

## Descripción General
Backend Flask con JWT authentication para sistema de gestión de tareas (mind/body), perfiles de usuario, logros, metas, chat IA y más.

## Autenticación
Todas las rutas (excepto login) requieren JWT token en el header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints Disponibles

### 🔐 Autenticación
- `POST /login` - Login y obtención de JWT token
- `GET /getusers` - Obtener todos los usuarios (testing)

### 👤 Perfil de Usuario
**Base: `/api/profile`**
- `GET /` - Obtener perfil del usuario autenticado
- `POST /` - Crear perfil del usuario
- `PUT /` - Actualizar perfil del usuario
- `DELETE /` - Eliminar perfil del usuario

**Ejemplo de perfil:**
```json
{
  "timezone": "America/Mexico_City",
  "birth_date": "1990-01-15",
  "gender": "male",
  "weight_kg": 75.5,
  "height_cm": 175,
  "preferred_language": "es"
}
```

### 📋 Plantillas de Tareas (Task Templates)
**Base: `/api/task-templates`**
- `GET /` - Obtener todas las plantillas
- `GET /<template_id>` - Obtener plantilla por ID
- `GET /key/<key>` - Obtener plantilla por key (ej: 'meditation_10')
- `GET /category/<category>` - Obtener plantillas por categoría ('mind' o 'body')
- `POST /` - Crear nueva plantilla
- `PUT /<template_id>` - Actualizar plantilla
- `DELETE /<template_id>` - Eliminar plantilla

**Ejemplo de plantilla:**
```json
{
  "key": "meditation_10",
  "name": "Meditación 10 minutos",
  "category": "mind",
  "estimated_minutes": 10,
  "difficulty": 2,
  "reward_xp": 50,
  "descr": "Sesión de meditación guiada de 10 minutos",
  "default_params": {"type": "guided", "music": true}
}
```

### 🧠 Tareas de Mente (Mind Tasks)
**Base: `/api/tasks/mind`**
- `GET /` - Obtener tareas de mente (query: `?status=pending`)
- `GET /<task_id>` - Obtener tarea específica
- `POST /` - Crear nueva tarea de mente
- `PUT /<task_id>` - Actualizar tarea
- `POST /<task_id>/complete` - Marcar tarea como completada
- `DELETE /<task_id>` - Eliminar tarea

**Ejemplo de tarea:**
```json
{
  "template_id": "uuid-of-template",
  "created_by": "user",
  "status": "pending",
  "scheduled_at": "2025-10-01T10:00:00Z",
  "params": {"duration": 10}
}
```

### 💪 Tareas de Cuerpo (Body Tasks)
**Base: `/api/tasks/body`**
- Mismos endpoints que Mind Tasks pero para tareas físicas

### 🏆 Logros (Achievements)
**Base: `/api/achievements`**
- `GET /` - Obtener logros del usuario
- `POST /` - Otorgar nuevo logro
- `DELETE /<achievement_id>` - Eliminar logro

**Ejemplo de logro:**
```json
{
  "key": "first_meditation",
  "title": "Primera Meditación",
  "description": "Completaste tu primera sesión de meditación"
}
```

### 🎯 Metas (Goals)
**Base: `/api/goals`**
- `GET /` - Obtener metas (query: `?is_active=true`)
- `GET /<goal_id>` - Obtener meta específica
- `POST /` - Crear nueva meta
- `PUT /<goal_id>` - Actualizar meta
- `DELETE /<goal_id>` - Eliminar meta

**Ejemplo de meta:**
```json
{
  "title": "Meditar 30 días seguidos",
  "description": "Completar una sesión de meditación cada día durante 30 días",
  "metric_key": "meditation_streak",
  "target_value": 30,
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "is_active": true
}
```

### 📝 Registro de Tareas (Task Logs)
**Base: `/api/task-logs`**
- `GET /` - Obtener logs (query: `?task_table=tasks_mind`)
- `POST /` - Crear entrada de log

**Ejemplo de log:**
```json
{
  "task_table": "tasks_mind",
  "task_id": "uuid-of-task",
  "action": "completed",
  "metadata": {"duration": 600, "notes": "Great session"}
}
```

### ❌ Fallos (Failures)
**Base: `/api/failures`**
- `GET /` - Obtener fallos (query: `?severity=major`)
- `POST /` - Registrar nuevo fallo
- `DELETE /<failure_id>` - Eliminar fallo

**Ejemplo de fallo:**
```json
{
  "task_table": "tasks_mind",
  "task_id": "uuid-of-task",
  "reason": "Olvidé hacer la tarea",
  "severity": "minor"
}
```

### 🤖 Reglas del Bot (Bot Rules)
**Base: `/api/bot-rules`**
- `GET /` - Obtener reglas (query: `?active_only=true`)
- `GET /<rule_id>` - Obtener regla específica
- `POST /` - Crear nueva regla
- `PUT /<rule_id>` - Actualizar regla
- `DELETE /<rule_id>` - Eliminar regla

**Ejemplo de regla:**
```json
{
  "name": "Auto-crear meditación matutina",
  "condition": {
    "time": "08:00",
    "days": ["monday", "wednesday", "friday"]
  },
  "action": {
    "type": "create_task",
    "template_key": "meditation_10",
    "category": "mind"
  },
  "priority": 10,
  "active": true
}
```

### 💬 Chat IA
**Base: `/api/chat`**

**Sesiones:**
- `GET /sessions` - Obtener sesiones de chat
- `GET /sessions/<session_id>` - Obtener sesión específica
- `POST /sessions` - Crear nueva sesión
- `PUT /sessions/<session_id>` - Actualizar sesión
- `DELETE /sessions/<session_id>` - Eliminar sesión

**Mensajes:**
- `GET /sessions/<session_id>/messages` - Obtener mensajes de una sesión
- `POST /sessions/<session_id>/messages` - Enviar mensaje
- `DELETE /messages/<message_id>` - Eliminar mensaje

**Ejemplo de sesión:**
```json
{
  "title": "Consulta sobre meditación",
  "model": "gpt-5",
  "system_prompt": "Eres un asistente experto en mindfulness"
}
```

**Ejemplo de mensaje:**
```json
{
  "role": "user",
  "content": "¿Cómo puedo mejorar mi práctica de meditación?",
  "content_json": null
}
```

## Códigos de Estado HTTP

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (token inválido o faltante)
- `403` - Forbidden (no tienes acceso a este recurso)
- `404` - Not Found
- `500` - Internal Server Error

## Flujo de Trabajo Típico

### 1. Autenticación
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Crear/Actualizar Perfil
```bash
curl -X POST http://localhost:5000/api/profile \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"timezone": "America/Mexico_City", "preferred_language": "es"}'
```

### 3. Obtener Plantillas de Tareas
```bash
curl -X GET http://localhost:5000/api/task-templates/category/mind \
  -H "Authorization: Bearer <token>"
```

### 4. Crear Tarea
```bash
curl -X POST http://localhost:5000/api/tasks/mind \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "<template-uuid>",
    "created_by": "user",
    "scheduled_at": "2025-10-01T10:00:00Z"
  }'
```

### 5. Completar Tarea
```bash
curl -X POST http://localhost:5000/api/tasks/mind/<task-id>/complete \
  -H "Authorization: Bearer <token>"
```

### 6. Ver Logros
```bash
curl -X GET http://localhost:5000/api/achievements \
  -H "Authorization: Bearer <token>"
```

## Estructura de la Base de Datos

### Tablas Principales:
- `users_iam` - Usuarios
- `profiles` - Perfiles de usuario
- `task_templates` - Plantillas de tareas
- `tasks_mind` - Tareas de mente
- `tasks_body` - Tareas de cuerpo
- `task_logs` - Registro de tareas
- `achievements` - Logros
- `failures` - Fallos
- `goals` - Metas
- `bot_rules` - Reglas del bot
- `chat_ia_sessions` - Sesiones de chat
- `chat_ia_messages` - Mensajes de chat

## Notas Importantes

1. **Seguridad**: Todas las rutas (excepto login) requieren JWT válido
2. **Autorización**: Los usuarios solo pueden acceder a sus propios recursos
3. **Validación**: Los campos requeridos están validados en los controladores
4. **JSONB**: Los campos `params`, `condition`, `action`, `metadata`, `content_json` son JSONB para flexibilidad
5. **Timestamps**: Todos los timestamps están en formato ISO 8601 UTC
6. **UUIDs**: La mayoría de IDs son UUIDs (excepto users_iam que puede usar otro formato)

## Testing con Swagger
Accede a `http://localhost:5000/apidocs/` para ver la documentación interactiva Swagger.

## Variables de Entorno

```bash
JWT_SECRET_KEY=your-secret-key-here
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```
