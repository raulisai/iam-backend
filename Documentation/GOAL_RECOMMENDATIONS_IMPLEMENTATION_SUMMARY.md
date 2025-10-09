# Goal Task Recommendations - Resumen de Implementación

## 📦 Archivos Creados/Modificados

### Nuevos Archivos
1. **`services/goal_task_recommendation_service.py`** - Servicio principal con lógica de IA
2. **`controllers/goal_task_recommendation_controller.py`** - Controlador de endpoints
3. **`routes/goal_task_recommendation_routes.py`** - Definición de rutas
4. **`Documentation/GOAL_TASK_RECOMMENDATIONS_API.md`** - Documentación completa
5. **`test/test_goal_recommendations.py`** - Script de pruebas y ejemplos

### Archivos Modificados
1. **`app.py`** - Registro de nuevas rutas

## 🎯 Funcionalidad Implementada

### Endpoint Principal
```
GET/POST /api/goals/{goal_id}/recommendations
```

### Características
✅ **IA Integrada**: Usa OpenAI GPT-4 para analizar objetivos y generar recomendaciones inteligentes
✅ **Contexto Adicional**: Acepta información adicional del usuario (desafíos, tiempo, recursos, preferencias)
✅ **Fallback Automático**: Si IA falla, usa lógica basada en patrones
✅ **Configurable**: Permite elegir número de recomendaciones (1-10)
✅ **Autenticación**: Protegido con JWT
✅ **Documentación Swagger**: Completamente documentado
✅ **Análisis Contextual**: Analiza el goal y tareas existentes antes de recomendar

## 🔍 Cómo Funciona

### 1. Análisis del Goal
- Lee el título y descripción del objetivo
- Obtiene todas las tareas existentes para ese goal
- Identifica qué falta por hacer

### 2. Análisis de Contexto (opcional)
El usuario puede proporcionar:
- **current_challenges**: Desafíos actuales
- **available_time**: Tiempo disponible
- **resources**: Recursos disponibles
- **preferences**: Preferencias de tipo de tareas

### 3. Generación con IA
- Construye un prompt detallado para GPT-4
- Incluye información del goal, tareas existentes, templates disponibles
- La IA genera tareas específicas, accionables y relevantes
- Cada recomendación incluye:
  - Título
  - Descripción detallada
  - Prioridad (low/medium/high)
  - Duración estimada
  - Template ID (si aplica)
  - Razón de por qué es importante

### 4. Respuesta Estructurada
Devuelve JSON con:
- Goal info
- Lista de recomendaciones
- Método usado (ai_powered o pattern_based)
- Metadata (tokens usados, modelo, etc.)

## 💡 Ejemplos de Uso

### Caso 1: Nuevo Objetivo sin Tareas
```bash
# Usuario crea objetivo: "Aprender Python"
# Sistema analiza y recomienda:
1. Completar tutorial básico de Python (HIGH priority)
2. Instalar Python y configurar entorno (HIGH priority)
3. Crear primer programa: Hello World (MEDIUM priority)
4. Leer documentación oficial de Python (MEDIUM priority)
5. Unirse a comunidad Python local (LOW priority)
```

### Caso 2: Objetivo con Contexto Específico
```bash
# Usuario: "Crear una app web"
# Contexto: "Soy principiante, 2 horas diarias, tengo laptop"
# Sistema recomienda:
1. Aprender HTML/CSS básico (2-3 horas diarias por 1 semana)
2. Tutorial de Flask o FastAPI (sesiones de 1-2 horas)
3. Crear proyecto simple: Lista de tareas
4. Aprender Git y GitHub para versionar código
5. Desplegar app en Heroku o Render (gratis)
```

### Caso 3: Objetivo Estancado
```bash
# Usuario: "Perder peso - 10kg"
# Ya tiene: "Correr 3x semana", "Dieta baja en carbos"
# Contexto: "No veo progreso después de 2 meses"
# Sistema recomienda:
1. Consultar con nutricionista profesional
2. Agregar entrenamiento de fuerza (2x por semana)
3. Llevar registro detallado de calorías diarias
4. Medir progreso con fotos semanales
5. Ajustar macros: aumentar proteína
```

## 🔧 Configuración Requerida

### Variables de Entorno
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
JWT_SECRET_KEY=tu-secret-key-seguro
```

### Dependencias Python
- `openai` - Cliente de OpenAI
- `flask` - Framework web
- Todas las dependencias ya están en `requirements.txt`

## 🚀 Cómo Probar

### 1. Iniciar el servidor
```bash
python app.py
```

### 2. Usar el script de prueba
```bash
python test/test_goal_recommendations.py
```

### 3. Llamada directa con curl
```bash
# Simple
curl -X GET "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer {token}"

# Con contexto
curl -X POST "http://localhost:5000/api/goals/{goal-id}/recommendations?use_ai=true&count=3" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Poco tiempo disponible",
      "available_time": "1 hora diaria",
      "resources": ["Laptop", "Internet"],
      "preferences": "Tareas cortas y prácticas"
    }
  }'
```

### 4. Swagger UI
```
http://localhost:5000/apidocs
```
Busca "Goal Task Recommendations" en la documentación.

## 📊 Ventajas del Sistema

### Con IA (use_ai=true)
✅ Recomendaciones personalizadas y contextuales
✅ Analiza el objetivo en profundidad
✅ Se adapta a recursos y tiempo disponible
✅ Genera pasos específicos y accionables
✅ Explica por qué cada tarea es importante

💰 Costo: ~$0.01-0.02 USD por solicitud

### Sin IA (use_ai=false)
✅ Gratis, sin límites
✅ Recomendaciones genéricas pero útiles
✅ Respuesta inmediata
✅ Basado en patrones comunes

## 🎨 Integración con Frontend

### React Example
```jsx
const GoalRecommendations = ({ goalId }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `/api/goals/${goalId}/recommendations?use_ai=true&count=5`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setRecommendations(data.recommendations);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <button onClick={fetchRecommendations}>
        🤖 Generar Recomendaciones con IA
      </button>
      
      {loading && <p>Generando recomendaciones...</p>}
      
      {recommendations.map((rec, i) => (
        <div key={i} className="recommendation-card">
          <h3>{rec.title}</h3>
          <p>{rec.description}</p>
          <span className={`priority-${rec.priority}`}>
            {rec.priority}
          </span>
          <button onClick={() => createTask(rec)}>
            ➕ Crear Tarea
          </button>
        </div>
      ))}
    </div>
  );
};
```

## 🔐 Seguridad

- ✅ Requiere autenticación JWT
- ✅ Valida que el goal pertenezca al usuario
- ✅ Límite de 10 recomendaciones máximo
- ✅ Validación de parámetros
- ✅ Manejo de errores robusto

## 📈 Métricas y Monitoreo

El servicio registra:
- Tokens de OpenAI usados
- Método utilizado (AI vs simple)
- Tiempo de generación
- Cantidad de tareas existentes
- Éxito/fallo de generación

## 🐛 Troubleshooting

### Error: "AI agent service not available"
- Verifica que `OPENAI_API_KEY` esté configurada
- Verifica que el servicio de agente esté funcionando

### Error: "Goal not found or unauthorized"
- Verifica que el `goal_id` sea correcto
- Verifica que el goal pertenezca al usuario autenticado

### Recomendaciones vacías
- Verifica que el goal tenga título y descripción
- Prueba con `use_ai=false` para ver si es problema de IA
- Revisa logs del servidor para más detalles

## 🎯 Próximos Pasos

1. **Usar el endpoint** para tus goals existentes
2. **Experimentar con contexto** adicional para mejores recomendaciones
3. **Integrar en tu frontend** para UX completa
4. **Crear tareas** desde las recomendaciones que te gusten
5. **Monitorear progreso** y pedir nuevas recomendaciones cuando sea necesario

## 📚 Documentación Adicional

- **API Docs**: `Documentation/GOAL_TASK_RECOMMENDATIONS_API.md`
- **Test Script**: `test/test_goal_recommendations.py`
- **Swagger**: http://localhost:5000/apidocs

---

## ✨ Ejemplo Completo de Flujo

```python
import requests

# 1. Login
login_response = requests.post('http://localhost:5000/api/auth/login', json={
    'email': 'user@example.com',
    'password': 'password123'
})
token = login_response.json()['token']

# 2. Crear Goal
goal_response = requests.post('http://localhost:5000/api/goals', 
    headers={'Authorization': f'Bearer {token}'},
    json={
        'title': 'Aprender Machine Learning',
        'description': 'Dominar conceptos de ML y crear proyectos reales',
        'start_date': '2025-10-08',
        'end_date': '2025-12-31',
        'target_value': 100
    }
)
goal_id = goal_response.json()['id']

# 3. Obtener Recomendaciones
rec_response = requests.post(
    f'http://localhost:5000/api/goals/{goal_id}/recommendations?use_ai=true&count=5',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'context': {
            'current_challenges': 'Sin experiencia previa en ML',
            'available_time': '2 horas diarias',
            'resources': ['Laptop con GPU', 'Curso Coursera'],
            'preferences': 'Aprendizaje práctico con proyectos'
        }
    }
)

recommendations = rec_response.json()['recommendations']

# 4. Crear Tareas desde Recomendaciones
for rec in recommendations[:3]:  # Crear las 3 más prioritarias
    task_response = requests.post(
        f'http://localhost:5000/api/goals/{goal_id}/tasks',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': rec['title'],
            'description': rec['description'],
            'priority': rec['priority']
        }
    )
    print(f"✅ Tarea creada: {rec['title']}")
```

---

**¡Tu endpoint de recomendaciones con IA está listo! 🎉**
