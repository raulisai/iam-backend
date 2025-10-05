# Ejemplos de CURL para probar el Chat IA con Agente

## Configuración
Primero obtén un token JWT válido:
```bash
# Registrar usuario
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# O iniciar sesión
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

**Guarda el token de la respuesta y úsalo en las siguientes peticiones:**

```bash
export TOKEN="tu_token_jwt_aqui"
```

---

## 1. Crear una sesión de chat

```bash
curl -X POST http://localhost:5000/api/chat/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Conversación sobre productividad"
  }'
```

**Respuesta esperada:**
```json
{
  "id": "uuid-de-la-sesion",
  "user_id": "uuid-del-usuario",
  "title": "Conversación sobre productividad",
  "created_at": "2025-10-04T...",
  "updated_at": "2025-10-04T...",
  "last_message_at": null
}
```

**Guarda el `id` de la sesión:**
```bash
export SESSION_ID="uuid-de-la-sesion"
```

---

## 2. Enviar un mensaje y obtener respuesta del agente

```bash
curl -X POST http://localhost:5000/api/chat/sessions/$SESSION_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "Hola! Necesito ayuda para organizar mis tareas del día. ¿Qué me recomiendas?"
  }'
```

**Respuesta esperada:**
```json
{
  "user_message": {
    "id": "uuid-mensaje-usuario",
    "session_id": "uuid-de-la-sesion",
    "role": "user",
    "content": "Hola! Necesito ayuda para organizar mis tareas del día...",
    "created_at": "2025-10-04T..."
  },
  "assistant_message": {
    "id": "uuid-mensaje-asistente",
    "session_id": "uuid-de-la-sesion",
    "role": "assistant",
    "content": "¡Hola! Me encantaría ayudarte a organizar tu día. Aquí te recomiendo...",
    "created_at": "2025-10-04T..."
  }
}
```

---

## 3. Enviar más mensajes (conversación continua)

```bash
curl -X POST http://localhost:5000/api/chat/sessions/$SESSION_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "¿Y qué técnicas de productividad me recomiendas para empezar?"
  }'
```

```bash
curl -X POST http://localhost:5000/api/chat/sessions/$SESSION_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "¿Puedes explicarme cómo funciona la técnica Pomodoro?"
  }'
```

---

## 4. Obtener todos los mensajes de una sesión

```bash
curl -X GET http://localhost:5000/api/chat/sessions/$SESSION_ID/messages \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada:**
```json
[
  {
    "id": "uuid-1",
    "session_id": "uuid-de-la-sesion",
    "role": "user",
    "content": "Hola! Necesito ayuda...",
    "created_at": "2025-10-04T..."
  },
  {
    "id": "uuid-2",
    "session_id": "uuid-de-la-sesion",
    "role": "assistant",
    "content": "¡Hola! Me encantaría ayudarte...",
    "created_at": "2025-10-04T..."
  },
  ...
]
```

---

## 5. Obtener todas las sesiones del usuario

```bash
curl -X GET http://localhost:5000/api/chat/sessions \
  -H "Authorization: Bearer $TOKEN"
```

---

## 6. Obtener una sesión específica

```bash
curl -X GET http://localhost:5000/api/chat/sessions/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

## 7. Actualizar el título de una sesión

```bash
curl -X PUT http://localhost:5000/api/chat/sessions/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Consejos de productividad y técnicas"
  }'
```

---

## 8. Eliminar una sesión

```bash
curl -X DELETE http://localhost:5000/api/chat/sessions/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

## Script completo de prueba

```bash
#!/bin/bash

# Configuración
BASE_URL="http://localhost:5000/api"

# 1. Login
echo "1. Iniciando sesión..."
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
echo "Token obtenido: ${TOKEN:0:20}..."

# 2. Crear sesión
echo -e "\n2. Creando sesión de chat..."
SESSION_RESPONSE=$(curl -s -X POST $BASE_URL/chat/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test de productividad"}')

SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Sesión creada: $SESSION_ID"

# 3. Enviar mensaje
echo -e "\n3. Enviando mensaje..."
MESSAGE_RESPONSE=$(curl -s -X POST $BASE_URL/chat/sessions/$SESSION_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "Hola! ¿Cómo puedo ser más productivo?"
  }')

echo "Respuesta completa:"
echo $MESSAGE_RESPONSE | jq '.'

# 4. Obtener historial
echo -e "\n4. Obteniendo historial..."
curl -s -X GET $BASE_URL/chat/sessions/$SESSION_ID/messages \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

---

## Notas importantes

1. **El agente responde automáticamente**: Cada vez que envías un mensaje con `role: "user"`, el sistema genera automáticamente una respuesta del asistente.

2. **Contexto conversacional**: El agente tiene acceso a los últimos 10 mensajes para mantener el contexto de la conversación.

3. **Respuesta dual**: La API devuelve tanto tu mensaje como la respuesta del asistente en una sola respuesta.

4. **Manejo de errores**: Si el agente falla, se devuelve un mensaje de error amigable pero no falla la petición.

5. **Timestamps automáticos**: El campo `last_message_at` se actualiza automáticamente después de cada mensaje.
