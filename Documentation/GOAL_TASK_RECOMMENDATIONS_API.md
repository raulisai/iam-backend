# Goal Task Recommendations API - Guía de Uso

## 📋 Descripción General

Este endpoint utiliza IA (OpenAI GPT) para analizar un objetivo específico y generar recomendaciones inteligentes de tareas que te ayudarán a lograrlo. El sistema analiza:

- El título y descripción del objetivo
- Las tareas existentes para ese objetivo
- Templates disponibles en el sistema
- Contexto adicional que proporciones (opcional)

## 🔗 Endpoint

```
GET/POST /api/goals/{goal_id}/recommendations
```

⚠️ **IMPORTANTE**: 
- **GET**: Para recomendaciones simples sin contexto adicional
- **POST**: Para recomendaciones con contexto personalizado (desafíos, recursos, preferencias)
- ❌ **NO uses body con GET** - causará error "Request with GET/HEAD method cannot have body"

### Autenticación
Requiere token JWT en el header:
```
Authorization: Bearer <tu-token-jwt>
```

## 📥 Parámetros

### Path Parameters
- **goal_id** (string, required): UUID del objetivo

### Query Parameters
- **use_ai** (boolean, optional, default: true): Usar IA para recomendaciones inteligentes
- **count** (integer, optional, default: 5, range: 1-10): Número de recomendaciones

### Body (POST only - opcional)
⚠️ **Solo para método POST**. Si usas GET, omite el body completamente.

```json
{
  "context": {
    "current_challenges": "Descripción de desafíos actuales",
    "available_time": "Tiempo disponible para trabajar",
    "resources": ["Recurso 1", "Recurso 2"],
    "preferences": "Preferencias de tipo de tareas"
  }
}
```

## 📤 Respuestas

### Éxito (200)
```json
{
  "success": true,
  "goal": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Aprender Python",
    "description": "Dominar programación en Python en 6 meses"
  },
  "recommendations": [
    {
      "title": "Completar tutorial básico de Python",
      "description": "Seguir un tutorial introductorio completo de Python que cubra variables, funciones y estructuras de control",
      "priority": "high",
      "estimated_duration": "2 horas",
      "template_id": null,
      "order": 1,
      "reason": "Fundamental para construir una base sólida antes de proyectos avanzados"
    },
    {
      "title": "Crear primer proyecto: Calculadora",
      "description": "Desarrollar una calculadora simple que realice operaciones básicas para aplicar conceptos aprendidos",
      "priority": "medium",
      "estimated_duration": "1.5 horas",
      "template_id": null,
      "order": 2,
      "reason": "Práctica inmediata consolida el aprendizaje teórico"
    }
  ],
  "method": "ai_powered",
  "generated_at": "2025-10-08T10:30:00Z",
  "existing_task_count": 3,
  "ai_metadata": {
    "tokens_used": 1250,
    "model": "gpt-4-turbo-preview"
  }
}
```

### Error (400)
```json
{
  "success": false,
  "error": "Goal not found or unauthorized"
}
```

### Error (401)
```json
{
  "error": "Token missing or invalid"
}
```

## 💡 Ejemplos de Uso

### 🔍 GET vs POST - ¿Cuándo usar cada uno?

**Usa GET cuando**:
- ✅ Solo quieres recomendaciones básicas
- ✅ No necesitas proporcionar contexto adicional
- ✅ Más rápido y simple

**Usa POST cuando**:
- ✅ Quieres personalizar con contexto (desafíos, tiempo, recursos)
- ✅ Necesitas recomendaciones más específicas a tu situación
- ✅ Mejor calidad de recomendaciones

### Ejemplo 1: Recomendaciones Básicas con IA (GET)
```bash
curl -X GET "http://localhost:5000/api/goals/550e8400-e29b-41d4-a716-446655440000/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer tu-token-jwt"
```

### Ejemplo 2: Con Contexto Adicional (POST)
```bash
curl -X POST "http://localhost:5000/api/goals/550e8400-e29b-41d4-a716-446655440000/recommendations?use_ai=true&count=3" \
  -H "Authorization: Bearer tu-token-jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Tengo poco tiempo libre entre semana",
      "available_time": "1 hora diaria en las mañanas",
      "resources": ["Laptop", "Internet", "Curso online ya adquirido"],
      "preferences": "Prefiero tareas prácticas de 30-60 minutos"
    }
  }'
```

### Ejemplo 3: JavaScript/Fetch
```javascript
// ✅ CORRECTO: GET request SIN body
const getRecommendationsSimple = async (goalId, token) => {
  const response = await fetch(
    `http://localhost:5000/api/goals/${goalId}/recommendations?use_ai=true&count=5`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
        // ⚠️ NO incluir Content-Type ni body en GET
      }
    }
  );
  
  const data = await response.json();
  return data;
};

// ✅ CORRECTO: POST request CON body
const getRecommendationsWithContext = async (goalId, token, context) => {
  const response = await fetch(
    `http://localhost:5000/api/goals/${goalId}/recommendations?use_ai=true&count=3`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ context })  // ✅ Body solo en POST
    }
  );
  
  const data = await response.json();
  return data;
};

// ❌ INCORRECTO: GET con body - CAUSA ERROR
// const WRONG = async (goalId, token) => {
//   const response = await fetch(url, {
//     method: 'GET',
//     body: JSON.stringify({ context })  // ❌ ERROR: GET no puede tener body
//   });
// };

// Uso
const token = 'tu-token-jwt';
const goalId = '550e8400-e29b-41d4-a716-446655440000';

// Simple
const recommendations = await getRecommendations(goalId, token);
console.log(recommendations);

// Con contexto
const context = {
  current_challenges: 'Falta de experiencia previa en programación',
  available_time: '2 horas por día',
  resources: ['Computadora', 'Internet'],
  preferences: 'Aprendizaje práctico con proyectos'
};
const detailedRecommendations = await getRecommendationsWithContext(goalId, token, context);
console.log(detailedRecommendations);
```

### Ejemplo 4: Python/Requests
```python
import requests
import json

def get_goal_recommendations(goal_id, token, use_ai=True, count=5, context=None):
    """Obtener recomendaciones de tareas para un objetivo."""
    url = f"http://localhost:5000/api/goals/{goal_id}/recommendations"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'use_ai': str(use_ai).lower(),
        'count': count
    }
    
    if context:
        # POST con contexto
        response = requests.post(
            url,
            headers=headers,
            params=params,
            json={'context': context}
        )
    else:
        # GET sin contexto
        response = requests.get(
            url,
            headers=headers,
            params=params
        )
    
    return response.json()

# Ejemplo de uso
token = "tu-token-jwt"
goal_id = "550e8400-e29b-41d4-a716-446655440000"

# Recomendaciones simples
result = get_goal_recommendations(goal_id, token, use_ai=True, count=5)
print(json.dumps(result, indent=2))

# Con contexto adicional
context = {
    "current_challenges": "Tiempo limitado y sin experiencia",
    "available_time": "1-2 horas diarias",
    "resources": ["Laptop", "Curso Udemy", "Libro Python Crash Course"],
    "preferences": "Tareas prácticas y cortas, enfoque en proyectos"
}

result_with_context = get_goal_recommendations(
    goal_id, 
    token, 
    use_ai=True, 
    count=3,
    context=context
)
print(json.dumps(result_with_context, indent=2))

# Mostrar recomendaciones
for i, rec in enumerate(result_with_context['recommendations'], 1):
    print(f"\n{i}. {rec['title']}")
    print(f"   Prioridad: {rec['priority']}")
    print(f"   Duración: {rec['estimated_duration']}")
    print(f"   Descripción: {rec['description']}")
    print(f"   Razón: {rec['reason']}")
```

## 🎯 Casos de Uso

### 1. Planificar Nuevo Objetivo
Cuando creas un objetivo nuevo y quieres saber qué tareas deberías empezar:
```bash
curl -X GET "http://localhost:5000/api/goals/{nuevo-goal-id}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer {token}"
```

### 2. Replanificar Objetivo Estancado
Si un objetivo no avanza, pide nuevas ideas:
```bash
curl -X POST "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true&count=3" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Las tareas actuales no están funcionando, necesito un enfoque diferente"
    }
  }'
```

### 3. Ajustar según Recursos
Pedir tareas adaptadas a tus recursos actuales:
```bash
curl -X POST "http://localhost:5000/api/goals/{goal-id}/recommendations?count=5" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "available_time": "Solo 30 minutos al día",
      "resources": ["Teléfono móvil"],
      "preferences": "Tareas muy cortas y que pueda hacer en el transporte"
    }
  }'
```

## 🔄 Flujo de Trabajo Recomendado

1. **Crear Goal**: Primero crea tu objetivo usando `/api/goals`
2. **Obtener Recomendaciones**: Usa este endpoint para obtener tareas sugeridas
3. **Revisar y Seleccionar**: Revisa las recomendaciones y selecciona las que te parezcan más relevantes
4. **Crear Goal Tasks**: Crea las tareas para el goal usando `/api/goals/{goal_id}/tasks`
5. **Monitorear Progreso**: Usa `/api/goals/{goal_id}/progress` para ver avance
6. **Re-evaluar**: Si necesitas más ideas, vuelve a llamar este endpoint

## ⚙️ Configuración

### Variables de Entorno Necesarias
```bash
OPENAI_API_KEY=tu-api-key-de-openai
JWT_SECRET_KEY=tu-secret-key
```

### Sin AI (Fallback)
Si `use_ai=false` o si el servicio de IA no está disponible, el sistema usará lógica basada en patrones para generar recomendaciones básicas pero funcionales.

## 📊 Mejores Prácticas

1. **Proporciona Contexto**: Mientras más contexto des, mejores serán las recomendaciones
2. **Usa AI para Objetivos Complejos**: Para objetivos simples, `use_ai=false` puede ser suficiente
3. **Pide Cantidad Apropiada**: Para empezar, 3-5 recomendaciones son ideales
4. **Itera**: Si las primeras recomendaciones no son perfectas, vuelve a pedir con más contexto
5. **Combina con Templates**: Si hay template_id en las recomendaciones, úsalos para crear tareas más rápido

## 🚀 Próximos Pasos

Después de obtener recomendaciones:

1. **Crear Tareas**: 
   ```
   POST /api/goals/{goal_id}/tasks
   ```

2. **Ver Todas las Tareas del Goal**:
   ```
   GET /api/goals/{goal_id}/tasks
   ```

3. **Ver Progreso**:
   ```
   GET /api/goals/{goal_id}/progress
   ```

## ❓ Preguntas Frecuentes

**P: ¿Cuánto cuesta cada recomendación?**
R: Depende del uso de tokens de OpenAI. En promedio, 1000-2000 tokens por solicitud (~$0.01-0.02 USD)

**P: ¿Puedo pedir recomendaciones sin IA?**
R: Sí, usa `use_ai=false` para obtener recomendaciones basadas en patrones básicos.

**P: ¿Qué pasa si el goal no existe?**
R: Recibirás un error 400 con mensaje "Goal not found or unauthorized"

**P: ¿Puedo pedir más de 10 recomendaciones?**
R: No, el máximo es 10 para mantener calidad y relevancia.

**P: ¿Las recomendaciones se guardan automáticamente?**
R: No, solo son sugerencias. Tú decides cuáles crear como tareas reales.
