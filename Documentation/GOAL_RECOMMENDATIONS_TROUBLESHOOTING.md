# 🐛 Troubleshooting - Goal Task Recommendations

## Error Común: "Request with GET/HEAD method cannot have body"

### ❌ Problema
```
TypeError: Failed to execute 'fetch' on 'Window': Request with GET/HEAD method cannot have body.
```

### 🔍 Causa
Estás intentando enviar un `body` con una petición `GET`, lo cual está **prohibido por el estándar HTTP**.

### ✅ Solución

#### Opción 1: Usa GET sin body
```javascript
// ✅ CORRECTO
const response = await fetch(
  `http://localhost:5000/api/goals/${goalId}/recommendations?use_ai=true&count=5`,
  {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
    // NO incluir body
  }
);
```

#### Opción 2: Usa POST con body
```javascript
// ✅ CORRECTO
const response = await fetch(
  `http://localhost:5000/api/goals/${goalId}/recommendations?use_ai=true&count=5`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      context: {
        current_challenges: "...",
        available_time: "...",
        resources: [],
        preferences: "..."
      }
    })
  }
);
```

---

## ¿Cuándo usar GET vs POST?

### Usa GET cuando:
✅ Solo necesitas recomendaciones básicas  
✅ No tienes contexto adicional que enviar  
✅ Quieres una petición más simple y rápida  
✅ Solo necesitas pasar parámetros en la URL (`?use_ai=true&count=5`)

### Usa POST cuando:
✅ Quieres personalizar con contexto adicional  
✅ Tienes información sobre desafíos, recursos, tiempo disponible  
✅ Quieres recomendaciones más específicas y de mejor calidad  
✅ Necesitas enviar un objeto JSON complejo

---

## Ejemplos Correctos

### ✅ GET - Recomendaciones Simples

#### JavaScript/Fetch
```javascript
const getRecommendations = async (goalId, token) => {
  const response = await fetch(
    `/api/goals/${goalId}/recommendations?use_ai=true&count=5`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
      // Sin body
    }
  );
  return response.json();
};
```

#### cURL
```bash
curl -X GET "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer {token}"
```

#### Python
```python
response = requests.get(
    f"{API_URL}/goals/{goal_id}/recommendations",
    headers={"Authorization": f"Bearer {token}"},
    params={"use_ai": "true", "count": 5}
    # Sin data/json
)
```

---

### ✅ POST - Recomendaciones con Contexto

#### JavaScript/Fetch
```javascript
const getRecommendationsWithContext = async (goalId, token) => {
  const response = await fetch(
    `/api/goals/${goalId}/recommendations?use_ai=true&count=5`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        context: {
          current_challenges: "Poco tiempo libre",
          available_time: "1 hora diaria",
          resources: ["Laptop", "Internet"],
          preferences: "Tareas cortas y prácticas"
        }
      })
    }
  );
  return response.json();
};
```

#### cURL
```bash
curl -X POST "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Poco tiempo libre",
      "available_time": "1 hora diaria",
      "resources": ["Laptop", "Internet"],
      "preferences": "Tareas cortas"
    }
  }'
```

#### Python
```python
response = requests.post(
    f"{API_URL}/goals/{goal_id}/recommendations",
    headers={"Authorization": f"Bearer {token}"},
    params={"use_ai": "true", "count": 5},
    json={
        "context": {
            "current_challenges": "Poco tiempo libre",
            "available_time": "1 hora diaria",
            "resources": ["Laptop", "Internet"],
            "preferences": "Tareas cortas"
        }
    }
)
```

---

## Otros Errores Comunes

### Error: "Goal not found or unauthorized"
**Causa**: El goal_id no existe o no pertenece al usuario  
**Solución**: Verifica que el goal_id sea correcto y que el token JWT sea del usuario dueño del goal

### Error: "AI service unavailable"
**Causa**: OpenAI API key no configurada o inválida  
**Solución**: Verifica que `OPENAI_API_KEY` esté en el archivo `.env`

### Error: "Invalid or expired token"
**Causa**: Token JWT inválido o expirado  
**Solución**: Haz login nuevamente para obtener un token fresco

### Error: 500 - "Failed to generate recommendations"
**Causa**: Error interno del servidor o de la API de OpenAI  
**Solución**: 
1. Revisa los logs del servidor
2. Intenta con `use_ai=false` para ver si funciona sin IA
3. Verifica que OpenAI API tenga créditos disponibles

---

## Tabla de Referencia Rápida

| Método | Body | Content-Type | Contexto | Uso |
|--------|------|--------------|----------|-----|
| GET | ❌ NO | ❌ No necesario | ❌ No | Recomendaciones simples |
| POST | ✅ SÍ (opcional) | ✅ application/json | ✅ Sí | Recomendaciones personalizadas |

---

## Checklist de Debugging

Si tienes un error, verifica:

- [ ] ¿Estás usando GET con body? → Cambia a POST o quita el body
- [ ] ¿El goal_id es correcto y existe?
- [ ] ¿El token JWT es válido y del usuario correcto?
- [ ] ¿El header `Authorization` está presente?
- [ ] ¿Si usas POST, incluiste `Content-Type: application/json`?
- [ ] ¿La variable `OPENAI_API_KEY` está configurada?
- [ ] ¿El servidor está corriendo?

---

## Necesitas más ayuda?

1. Revisa la [documentación completa](./GOAL_TASK_RECOMMENDATIONS_API.md)
2. Ve ejemplos en [cURL examples](./GOAL_RECOMMENDATIONS_CURL_EXAMPLES.md)
3. Prueba el [script de testing](../test/test_goal_recommendations.py)
4. Revisa los logs del servidor en la terminal
