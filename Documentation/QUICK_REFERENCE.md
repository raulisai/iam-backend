# 📋 Quick Reference - Recomendaciones API

## 🚀 Los 3 Endpoints

```bash
# 1. GENERAL (3 tareas mixtas)
GET /api/tasks/recommendations/

# 2. MIND (1-10 tareas mentales)
GET /api/tasks/recommendations/mind

# 3. BODY (1-10 tareas físicas)
GET /api/tasks/recommendations/body
```

---

## 📝 Parámetros

| Parámetro | Tipo | Default | Descripción | Disponible en |
|-----------|------|---------|-------------|---------------|
| `use_ai` | boolean | false | Usar IA para recomendaciones | Todos |
| `count` | integer | 3 | Cantidad de recomendaciones (1-10) | Mind, Body |

---

## 💻 Ejemplos Rápidos

### cURL

```bash
# General
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Mind (5 tareas)
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind?count=5" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Body (4 tareas)
curl -X GET "http://localhost:5000/api/tasks/recommendations/body?count=4" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Con IA
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind?use_ai=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### JavaScript

```javascript
// General
const general = await fetch('/api/tasks/recommendations/', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Mind
const mind = await fetch('/api/tasks/recommendations/mind?count=5', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Body
const body = await fetch('/api/tasks/recommendations/body?count=4', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Con IA
const aiMind = await fetch('/api/tasks/recommendations/mind?use_ai=true&count=3', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());
```

### Python

```python
import requests

# General
response = requests.get(
    'http://localhost:5000/api/tasks/recommendations/',
    headers={'Authorization': f'Bearer {token}'}
)

# Mind
response = requests.get(
    'http://localhost:5000/api/tasks/recommendations/mind?count=5',
    headers={'Authorization': f'Bearer {token}'}
)

# Body
response = requests.get(
    'http://localhost:5000/api/tasks/recommendations/body?count=4',
    headers={'Authorization': f'Bearer {token}'}
)
```

---

## 📦 Respuesta

```json
{
  "recommendations": [
    {
      "id": "uuid",
      "key": "template_key",
      "name": "Nombre",
      "category": "mind|body",
      "desc": "Descripción",
      "default_xp": 10,
      "default_params": {},
      "suggested_schedule": "2025-10-06T14:00:00Z",
      "reason": "Por qué se recomienda"
    }
  ],
  "method": "pattern_based|ai_powered",
  "generated_at": "2025-10-06T10:30:00Z",
  "task_history_count": 12,
  "category": "mind|body|null"
}
```

---

## 🎯 Casos de Uso

| Necesidad | Endpoint | Params |
|-----------|----------|--------|
| Dashboard principal | `/recommendations/` | ninguno |
| Sección Mente | `/recommendations/mind` | `count=5` |
| Sección Cuerpo | `/recommendations/body` | `count=5` |
| Lista completa mental | `/recommendations/mind` | `count=10` |
| Lista completa física | `/recommendations/body` | `count=10` |
| Usuario premium | cualquiera | `use_ai=true` |

---

## ⚡ React Hook

```javascript
const useRecommendations = (category = null, count = 3) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const fetch = async (useAI = false) => {
    setLoading(true);
    const base = '/api/tasks/recommendations/';
    const url = category 
      ? `${base}${category}?count=${count}&use_ai=${useAI}`
      : `${base}?use_ai=${useAI}`;
    
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    setData(await response.json());
    setLoading(false);
  };
  
  return { data, loading, fetch };
};

// Uso
const { data, loading, fetch } = useRecommendations('mind', 5);
```

---

## 🔑 Headers Requeridos

```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📚 Documentación Completa

- [RECOMMENDATIONS_ENDPOINTS.md](./RECOMMENDATIONS_ENDPOINTS.md)
- [RECOMMENDATIONS_VISUAL_GUIDE.md](./RECOMMENDATIONS_VISUAL_GUIDE.md)
- [RECOMMENDATIONS_FINAL_SUMMARY.md](./RECOMMENDATIONS_FINAL_SUMMARY.md)

---

## 🧪 Testing

```bash
# En Swagger UI
http://localhost:5000/apidocs/

# Script de prueba
python test/test_recommendations.py
```

---

**Última actualización**: 6 de Octubre, 2025
