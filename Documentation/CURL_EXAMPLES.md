# Ejemplos de Uso de la API con cURL

Este archivo contiene ejemplos prácticos de cómo usar cada endpoint de la API.

## Variables de Entorno
```bash
# Guardar el token después del login
export TOKEN="tu-jwt-token-aqui"
export BASE_URL="http://localhost:5000"
```

## 🔐 Autenticación

### Login
```bash
curl -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Obtener usuarios (testing)
```bash
curl -X GET $BASE_URL/getusers
```

## 👤 Perfil

### Obtener perfil del usuario
```bash
curl -X GET $BASE_URL/api/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Crear perfil
```bash
curl -X POST $BASE_URL/api/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "timezone": "America/Mexico_City",
    "birth_date": "1990-01-15",
    "gender": "male",
    "weight_kg": 75.5,
    "height_cm": 175,
    "preferred_language": "es"
  }'
```

### Actualizar perfil
```bash
curl -X PUT $BASE_URL/api/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "weight_kg": 76.0,
    "height_cm": 176
  }'
```

### Eliminar perfil
```bash
curl -X DELETE $BASE_URL/api/profile \
  -H "Authorization: Bearer $TOKEN"
```

## 📋 Plantillas de Tareas

### Obtener todas las plantillas
```bash
curl -X GET $BASE_URL/api/task-templates \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener plantilla por ID
```bash
curl -X GET $BASE_URL/api/task-templates/<template-id> \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener plantilla por key
```bash
curl -X GET $BASE_URL/api/task-templates/key/meditation_10 \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener plantillas por categoría
```bash
# Mind templates
curl -X GET $BASE_URL/api/task-templates/category/mind \
  -H "Authorization: Bearer $TOKEN"

# Body templates
curl -X GET $BASE_URL/api/task-templates/category/body \
  -H "Authorization: Bearer $TOKEN"
```

### Crear plantilla
```bash
curl -X POST $BASE_URL/api/task-templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "meditation_15",
    "name": "Meditación 15 minutos",
    "category": "mind",
    "estimated_minutes": 15,
    "difficulty": 3,
    "reward_xp": 75,
    "descr": "Sesión de meditación guiada de 15 minutos",
    "default_params": {"type": "guided", "music": true}
  }'
```

### Actualizar plantilla
```bash
curl -X PUT $BASE_URL/api/task-templates/<template-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reward_xp": 100
  }'
```

### Eliminar plantilla
```bash
curl -X DELETE $BASE_URL/api/task-templates/<template-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 🧠 Tareas de Mente

### Obtener todas las tareas de mente
```bash
curl -X GET $BASE_URL/api/tasks/mind \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener tareas pendientes
```bash
curl -X GET "$BASE_URL/api/tasks/mind?status=pending" \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener tarea específica
```bash
curl -X GET $BASE_URL/api/tasks/mind/<task-id> \
  -H "Authorization: Bearer $TOKEN"
```

### Crear tarea de mente
```bash
curl -X POST $BASE_URL/api/tasks/mind \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "<template-uuid>",
    "created_by": "user",
    "scheduled_at": "2025-10-01T10:00:00Z",
    "params": {"duration": 10, "type": "guided"}
  }'
```

### Actualizar tarea
```bash
curl -X PUT $BASE_URL/api/tasks/mind/<task-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

### Completar tarea
```bash
curl -X POST $BASE_URL/api/tasks/mind/<task-id>/complete \
  -H "Authorization: Bearer $TOKEN"
```

### Eliminar tarea
```bash
curl -X DELETE $BASE_URL/api/tasks/mind/<task-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 💪 Tareas de Cuerpo

Los endpoints son idénticos a las tareas de mente, solo cambia la URL base:

```bash
# Obtener tareas de cuerpo
curl -X GET $BASE_URL/api/tasks/body \
  -H "Authorization: Bearer $TOKEN"

# Crear tarea de cuerpo
curl -X POST $BASE_URL/api/tasks/body \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "<template-uuid>",
    "created_by": "user",
    "scheduled_at": "2025-10-01T18:00:00Z"
  }'

# Completar tarea de cuerpo
curl -X POST $BASE_URL/api/tasks/body/<task-id>/complete \
  -H "Authorization: Bearer $TOKEN"
```

## 🏆 Logros

### Obtener logros
```bash
curl -X GET $BASE_URL/api/achievements \
  -H "Authorization: Bearer $TOKEN"
```

### Otorgar logro
```bash
curl -X POST $BASE_URL/api/achievements \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "first_meditation",
    "title": "Primera Meditación",
    "description": "Completaste tu primera sesión de meditación"
  }'
```

### Eliminar logro
```bash
curl -X DELETE $BASE_URL/api/achievements/<achievement-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 🎯 Metas

### Obtener todas las metas
```bash
curl -X GET $BASE_URL/api/goals \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener metas activas
```bash
curl -X GET "$BASE_URL/api/goals?is_active=true" \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener meta específica
```bash
curl -X GET $BASE_URL/api/goals/<goal-id> \
  -H "Authorization: Bearer $TOKEN"
```

### Crear meta
```bash
curl -X POST $BASE_URL/api/goals \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meditar 30 días seguidos",
    "description": "Completar una sesión de meditación cada día durante 30 días",
    "metric_key": "meditation_streak",
    "target_value": 30,
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "is_active": true
  }'
```

### Actualizar meta
```bash
curl -X PUT $BASE_URL/api/goals/<goal-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

### Eliminar meta
```bash
curl -X DELETE $BASE_URL/api/goals/<goal-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 📝 Logs de Tareas

### Obtener logs
```bash
curl -X GET $BASE_URL/api/task-logs \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrar logs por tabla
```bash
curl -X GET "$BASE_URL/api/task-logs?task_table=tasks_mind" \
  -H "Authorization: Bearer $TOKEN"
```

### Crear log
```bash
curl -X POST $BASE_URL/api/task-logs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_table": "tasks_mind",
    "task_id": "<task-uuid>",
    "action": "completed",
    "metadata": {"duration": 600, "notes": "Excelente sesión"}
  }'
```

## ❌ Fallos

### Obtener fallos
```bash
curl -X GET $BASE_URL/api/failures \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrar por severidad
```bash
curl -X GET "$BASE_URL/api/failures?severity=major" \
  -H "Authorization: Bearer $TOKEN"
```

### Registrar fallo
```bash
curl -X POST $BASE_URL/api/failures \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_table": "tasks_mind",
    "task_id": "<task-uuid>",
    "reason": "Olvidé hacer la tarea",
    "severity": "minor"
  }'
```

### Eliminar fallo
```bash
curl -X DELETE $BASE_URL/api/failures/<failure-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 🤖 Reglas del Bot

### Obtener todas las reglas
```bash
curl -X GET $BASE_URL/api/bot-rules \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener solo reglas activas
```bash
curl -X GET "$BASE_URL/api/bot-rules?active_only=true" \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener regla específica
```bash
curl -X GET $BASE_URL/api/bot-rules/<rule-id> \
  -H "Authorization: Bearer $TOKEN"
```

### Crear regla
```bash
curl -X POST $BASE_URL/api/bot-rules \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Actualizar regla
```bash
curl -X PUT $BASE_URL/api/bot-rules/<rule-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "active": false
  }'
```

### Eliminar regla
```bash
curl -X DELETE $BASE_URL/api/bot-rules/<rule-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 💬 Chat IA

### Obtener sesiones de chat
```bash
curl -X GET $BASE_URL/api/chat/sessions \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener sesión específica
```bash
curl -X GET $BASE_URL/api/chat/sessions/<session-id> \
  -H "Authorization: Bearer $TOKEN"
```

### Crear sesión
```bash
curl -X POST $BASE_URL/api/chat/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Consulta sobre meditación",
    "model": "gpt-5",
    "system_prompt": "Eres un asistente experto en mindfulness y meditación."
  }'
```

### Actualizar sesión
```bash
curl -X PUT $BASE_URL/api/chat/sessions/<session-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nueva consulta actualizada"
  }'
```

### Eliminar sesión
```bash
curl -X DELETE $BASE_URL/api/chat/sessions/<session-id> \
  -H "Authorization: Bearer $TOKEN"
```

### Obtener mensajes de una sesión
```bash
curl -X GET $BASE_URL/api/chat/sessions/<session-id>/messages \
  -H "Authorization: Bearer $TOKEN"
```

### Enviar mensaje
```bash
curl -X POST $BASE_URL/api/chat/sessions/<session-id>/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "¿Cómo puedo mejorar mi práctica de meditación?",
    "tokens_used": 15
  }'
```

### Eliminar mensaje
```bash
curl -X DELETE $BASE_URL/api/chat/messages/<message-id> \
  -H "Authorization: Bearer $TOKEN"
```

## 🔄 Flujo Completo de Ejemplo

```bash
# 1. Login
TOKEN=$(curl -s -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass123"}' \
  | jq -r '.token')

# 2. Crear perfil
curl -X POST $BASE_URL/api/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"timezone": "America/Mexico_City", "preferred_language": "es"}'

# 3. Obtener plantillas de meditación
TEMPLATES=$(curl -s -X GET $BASE_URL/api/task-templates/category/mind \
  -H "Authorization: Bearer $TOKEN")

# 4. Crear tarea de meditación
TEMPLATE_ID=$(echo $TEMPLATES | jq -r '.[0].id')
curl -X POST $BASE_URL/api/tasks/mind \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"template_id\": \"$TEMPLATE_ID\", \"created_by\": \"user\"}"

# 5. Ver mis tareas
curl -X GET $BASE_URL/api/tasks/mind \
  -H "Authorization: Bearer $TOKEN"
```

## 💡 Tips

- Usa `jq` para parsear JSON: `curl ... | jq .`
- Guarda el token en variable: `export TOKEN="..."`
- Usa `-v` para debug: `curl -v ...`
- Pretty print: `curl ... | python -m json.tool`
