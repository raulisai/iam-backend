# 🚀 QUICK START - Goal Task Recommendations

## ¿Qué hace este endpoint?

**Le envías un goal → La IA analiza → Te devuelve tareas específicas para lograrlo**

## Endpoint

```
GET  /api/goals/{goal_id}/recommendations    (sin contexto)
POST /api/goals/{goal_id}/recommendations    (con contexto)
```

⚠️ **IMPORTANTE - Evita este error común**: 
```
TypeError: Failed to execute 'fetch' on 'Window': 
Request with GET/HEAD method cannot have body.
```

**Reglas simples**:
- **GET** = SIN body (solo query params en la URL)
- **POST** = CON body (para enviar contexto JSON)
- ❌ **NUNCA**: GET + body = ERROR

📚 [Ver guía completa de troubleshooting](./GOAL_RECOMMENDATIONS_TROUBLESHOOTING.md)

## Lo que necesitas enviar

### Opción 1: GET (Simple, sin contexto)
```bash
curl "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true" \
  -H "Authorization: Bearer {token}"
```

### Opción 2: POST (Con contexto personalizado)
```bash
curl -X POST "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Qué dificultades tienes",
      "available_time": "Cuánto tiempo tienes",
      "resources": ["Qué recursos tienes"],
      "preferences": "Cómo prefieres trabajar"
    }
  }'
```

## Lo que recibes

```json
{
  "success": true,
  "goal": {
    "id": "goal-uuid",
    "title": "Tu objetivo",
    "description": "Descripción del objetivo"
  },
  "recommendations": [
    {
      "title": "Primera tarea a hacer",
      "description": "Qué debes hacer exactamente",
      "priority": "high",
      "estimated_duration": "2 horas",
      "order": 1,
      "reason": "Por qué es importante esta tarea"
    },
    {
      "title": "Segunda tarea",
      "description": "...",
      "priority": "medium",
      "order": 2
    }
  ],
  "method": "ai_powered",
  "existing_task_count": 3
}
```

## Ejemplo Completo con Python

```python
import requests

# 1. Tu configuración
API = "http://localhost:5000"
TOKEN = "tu-jwt-token"
GOAL_ID = "tu-goal-id"

# 2. Obtener recomendaciones
response = requests.post(
    f"{API}/api/goals/{GOAL_ID}/recommendations?use_ai=true&count=5",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={
        "context": {
            "current_challenges": "Poco tiempo y sin experiencia",
            "available_time": "1 hora diaria",
            "resources": ["Laptop", "Internet"],
            "preferences": "Tareas prácticas y cortas"
        }
    }
)

data = response.json()

# 3. Ver recomendaciones
for i, rec in enumerate(data['recommendations'], 1):
    print(f"{i}. {rec['title']}")
    print(f"   Prioridad: {rec['priority']}")
    print(f"   {rec['description']}")
    print(f"   Razón: {rec['reason']}\n")

# 4. Crear tareas que te gusten
for rec in data['recommendations'][:3]:  # Las 3 primeras
    requests.post(
        f"{API}/api/goals/{GOAL_ID}/tasks",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={
            "title": rec['title'],
            "description": rec['description'],
            "priority": rec['priority']
        }
    )
```

## Ejemplo con JavaScript

```javascript
const API = 'http://localhost:5000';
const TOKEN = 'tu-jwt-token';
const GOAL_ID = 'tu-goal-id';

// Obtener recomendaciones
const response = await fetch(
  `${API}/api/goals/${GOAL_ID}/recommendations?use_ai=true&count=5`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      context: {
        current_challenges: 'Poco tiempo y recursos limitados',
        available_time: '1-2 horas diarias',
        resources: ['Laptop', 'Internet', 'Curso online'],
        preferences: 'Tareas prácticas entre 30-60 minutos'
      }
    })
  }
);

const data = await response.json();

// Mostrar recomendaciones
data.recommendations.forEach((rec, i) => {
  console.log(`${i + 1}. ${rec.title}`);
  console.log(`   ${rec.description}`);
  console.log(`   Prioridad: ${rec.priority}\n`);
});
```

## Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `use_ai` | boolean | true | Usar IA para recomendaciones inteligentes |
| `count` | integer | 5 | Número de recomendaciones (1-10) |
| `context` | object | null | Información adicional para mejores recomendaciones |

### Context Object (Opcional pero Recomendado)

```json
{
  "context": {
    "current_challenges": "string - Qué te impide lograr el objetivo",
    "available_time": "string - Cuánto tiempo tienes",
    "resources": ["array de strings - Qué tienes disponible"],
    "preferences": "string - Cómo prefieres trabajar"
  }
}
```

## Casos de Uso

### 1. Nuevo Objetivo - ¿Por dónde empiezo?
```bash
# Acabas de crear objetivo "Aprender Python"
# Pides recomendaciones → IA te dice los primeros pasos
curl -X GET ".../recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer {token}"
```

### 2. Objetivo Estancado - Necesito nuevas ideas
```bash
# Ya tienes algunas tareas pero no avanzas
# Pides recomendaciones con contexto → IA sugiere nuevos enfoques
curl -X POST ".../recommendations?use_ai=true" \
  -d '{"context": {"current_challenges": "Las tareas actuales no funcionan"}}'
```

### 3. Planificación Personalizada
```bash
# Quieres tareas adaptadas a tu situación
# Envías tu contexto → IA personaliza recomendaciones
curl -X POST ".../recommendations?count=3" \
  -d '{
    "context": {
      "available_time": "30 minutos diarios",
      "preferences": "Solo tareas cortas"
    }
  }'
```

## Tips para Mejores Recomendaciones

### ✅ HACER
- Enviar contexto detallado
- Ser específico sobre limitaciones
- Mencionar qué ya has intentado
- Indicar tus preferencias de aprendizaje
- Listar recursos disponibles

### ❌ NO HACER
- Enviar goals muy vagos sin descripción
- No dar contexto (la IA trabajará "a ciegas")
- Pedir demasiadas recomendaciones (>5 pierde calidad)
- Ignorar las recomendaciones sin revisarlas

## Flujo Típico

```
1. Crear Goal
   ↓
2. Obtener Recomendaciones (este endpoint)
   ↓
3. Revisar y Seleccionar tareas que te gusten
   ↓
4. Crear Goal Tasks desde recomendaciones
   ↓
5. Trabajar en las tareas
   ↓
6. [Si necesitas más ideas] → Volver al paso 2
```

## Costos

- **Con IA (`use_ai=true`)**: ~$0.01-0.02 USD por solicitud (tokens OpenAI)
- **Sin IA (`use_ai=false`)**: Gratis, lógica simple

## Límites

- Máximo 10 recomendaciones por solicitud
- Requiere autenticación JWT
- El goal debe pertenecer al usuario autenticado
- Rate limit del servidor aplica

## Troubleshooting Rápido

**Error "Goal not found"**
→ Verifica el goal_id y que sea tuyo

**Recomendaciones genéricas**
→ Agrega más contexto en el body

**Error "AI service unavailable"**
→ Verifica OPENAI_API_KEY en .env

**Response vacío**
→ Verifica que el goal tenga título y descripción

## Testing Rápido

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}' \
  | jq -r '.token')

# 2. Crear goal
GOAL_ID=$(curl -s -X POST "http://localhost:5000/api/goals" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Goal","description":"Testing recommendations"}' \
  | jq -r '.id')

# 3. Obtener recomendaciones
curl -X GET "http://localhost:5000/api/goals/$GOAL_ID/recommendations?use_ai=true&count=3" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## Recursos

- **Documentación completa**: `Documentation/GOAL_TASK_RECOMMENDATIONS_API.md`
- **Ejemplos cURL**: `Documentation/GOAL_RECOMMENDATIONS_CURL_EXAMPLES.md`
- **Script de prueba**: `test/test_goal_recommendations.py`
- **Swagger UI**: http://localhost:5000/apidocs

---

**¿Más preguntas?** Revisa la documentación completa en `/Documentation/` 📚
