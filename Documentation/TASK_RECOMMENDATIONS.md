# Sistema de Recomendaciones de Tareas

## Descripción General

El sistema de recomendaciones proporciona sugerencias personalizadas de tareas basadas en el historial del usuario y patrones de uso. Puede funcionar con dos métodos:

1. **Recomendaciones basadas en patrones** (por defecto)
2. **Recomendaciones con IA** (cuando se solicita explícitamente)

## Endpoint

### GET `/api/tasks/recommendations/`

Genera 3 recomendaciones de tareas personalizadas para el usuario autenticado.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Query Parameters
- `use_ai` (boolean, opcional): Si es `true`, usa el agente de IA para generar recomendaciones más inteligentes. Por defecto es `false`.

#### Respuesta Exitosa (200)

```json
{
  "recommendations": [
    {
      "id": "uuid-template-1",
      "key": "meditation_morning",
      "name": "Meditación Matutina",
      "category": "mind",
      "desc": "Sesión de meditación para comenzar el día",
      "default_xp": 10,
      "default_params": {
        "duration": 15
      },
      "suggested_schedule": "2025-10-06T14:00:00Z",
      "reason": "Recomendado para balancear tus tareas de mente"
    },
    {
      "id": "uuid-template-2",
      "key": "workout_cardio",
      "name": "Cardio 30 min",
      "category": "body",
      "desc": "Ejercicio cardiovascular moderado",
      "default_xp": 15,
      "default_params": {
        "duration": 30,
        "intensity": "moderate"
      },
      "suggested_schedule": "2025-10-06T18:00:00Z",
      "reason": "Nuevo desafío para expandir tu rutina"
    },
    {
      "id": "uuid-template-3",
      "key": "reading_session",
      "name": "Lectura Educativa",
      "category": "mind",
      "desc": "20 minutos de lectura",
      "default_xp": 8,
      "default_params": {
        "duration": 20
      },
      "suggested_schedule": "2025-10-06T22:00:00Z",
      "reason": "Tarea de mind para continuar tu progreso"
    }
  ],
  "method": "pattern_based",
  "generated_at": "2025-10-06T10:30:00Z",
  "task_history_count": 12
}
```

## Lógica de Recomendaciones

### Método Basado en Patrones (pattern_based)

Este método analiza el historial reciente del usuario sin usar IA:

1. **Análisis de Balance**: 
   - Cuenta tareas de mente vs cuerpo
   - Si hay desbalance (>1.5x), prioriza la categoría con menos tareas
   
2. **Evita Repetición**:
   - Identifica templates usados recientemente
   - Prioriza templates no usados

3. **Distribución Inteligente**:
   - Si necesita balance de body: recomienda 2 body, 1 mind
   - Si necesita balance de mind: recomienda 2 mind, 1 body
   - Si está balanceado: mezcla equitativa

4. **Horarios Sugeridos**:
   - Distribuye las 3 tareas en las próximas 12-24 horas
   - Espaciadas cada 4 horas aproximadamente

### Método con IA (ai_powered)

Activado con `?use_ai=true`. Solo se usa si el usuario tiene al menos 3 tareas en su historial:

1. **Análisis Contextual**:
   - El agente analiza hasta 15 tareas recientes
   - Considera patrones, frecuencia y completitud
   
2. **Selección Inteligente**:
   - El agente evalúa todos los templates disponibles
   - Considera progresión y dificultad
   - Busca variedad y balance óptimo

3. **Fallback Automático**:
   - Si la IA falla o no puede decidir, usa el método de patrones
   - Garantiza siempre una respuesta

## Casos de Uso

### 1. Usuario nuevo (pocas tareas)
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \
  -H "Authorization: Bearer <token>"
```
- Usa método de patrones
- Mezcla equilibrada de mind y body
- Introduce al usuario a diferentes tipos de tareas

### 2. Usuario con historial desbalanceado
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \
  -H "Authorization: Bearer <token>"
```
- Detecta el desbalance automáticamente
- Recomienda más tareas de la categoría menos usada
- Ayuda a mantener rutina equilibrada

### 3. Usuario avanzado que quiere recomendaciones IA
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/?use_ai=true" \
  -H "Authorization: Bearer <token>"
```
- Usa análisis de IA profundo
- Considera patrones complejos
- Recomendaciones más personalizadas

## Integración con el Frontend

### Ejemplo React/JavaScript

```javascript
// Obtener recomendaciones simples
const getRecommendations = async () => {
  const response = await fetch('http://localhost:5000/api/tasks/recommendations/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  return data.recommendations;
};

// Obtener recomendaciones con IA
const getAIRecommendations = async () => {
  const response = await fetch('http://localhost:5000/api/tasks/recommendations/?use_ai=true', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  return data.recommendations;
};

// Crear tarea desde recomendación
const createTaskFromRecommendation = async (recommendation) => {
  const taskData = {
    template_id: recommendation.id,
    scheduled_at: recommendation.suggested_schedule,
    params: recommendation.default_params || {},
    created_by: 'user',
    status: 'pending'
  };
  
  // Determinar endpoint según categoría
  const endpoint = recommendation.category === 'mind' 
    ? '/api/tasks/mind/'
    : '/api/tasks/body/';
  
  const response = await fetch(`http://localhost:5000${endpoint}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(taskData)
  });
  
  return response.json();
};
```

## Ventajas del Sistema

1. **Siempre Disponible**: Funciona incluso sin historial extenso
2. **Inteligente por Defecto**: El método de patrones ya es bastante efectivo
3. **IA Opcional**: Solo cuando el usuario lo necesita o tiene historial suficiente
4. **Performance**: El método de patrones es rápido y no consume recursos de IA
5. **Balance Automático**: Ayuda al usuario a mantener rutina equilibrada
6. **Variedad**: Evita repetición de las mismas tareas

## Notas de Implementación

- Las recomendaciones son stateless (no se guardan)
- Cada llamada genera nuevas recomendaciones
- El usuario decide si crear las tareas recomendadas
- Los horarios sugeridos son solo guías, el usuario puede modificarlos
- El sistema aprende de forma pasiva observando el historial

## Futuras Mejoras

1. Considerar hora del día para mejores horarios sugeridos
2. Análisis de tasa de completitud por tipo de tarea
3. Recomendaciones basadas en objetivos activos
4. Machine learning para aprender preferencias del usuario
5. Recomendaciones adaptativas según días de la semana
