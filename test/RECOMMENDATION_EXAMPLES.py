"""
Ejemplos de uso del endpoint de recomendaciones de tareas
"""

# Ejemplo 1: Obtener recomendaciones básicas
curl_example_1 = """
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
"""

# Ejemplo 2: Obtener recomendaciones con IA
curl_example_2 = """
curl -X GET "http://localhost:5000/api/tasks/recommendations/?use_ai=true" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
"""

# Ejemplo 3: Crear una tarea desde una recomendación (Python)
python_example = """
import requests

# 1. Obtener recomendaciones
response = requests.get(
    'http://localhost:5000/api/tasks/recommendations/',
    headers={'Authorization': f'Bearer {token}'}
)

recommendations = response.json()

# 2. Seleccionar una recomendación
first_recommendation = recommendations['recommendations'][0]

# 3. Crear la tarea
task_data = {
    'template_id': first_recommendation['id'],
    'scheduled_at': first_recommendation['suggested_schedule'],
    'params': first_recommendation.get('default_params', {}),
    'created_by': 'user',
    'status': 'pending'
}

# Determinar endpoint según categoría
endpoint = (
    '/api/tasks/mind/' if first_recommendation['category'] == 'mind'
    else '/api/tasks/body/'
)

response = requests.post(
    f'http://localhost:5000{endpoint}',
    json=task_data,
    headers={'Authorization': f'Bearer {token}'}
)

created_task = response.json()
print(f"Tarea creada: {created_task}")
"""

# Ejemplo 4: Interfaz JavaScript/React
javascript_example = """
// Component para mostrar recomendaciones
const TaskRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [useAI, setUseAI] = useState(false);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const url = useAI 
        ? '/api/tasks/recommendations/?use_ai=true'
        : '/api/tasks/recommendations/';
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const createTaskFromRecommendation = async (recommendation) => {
    const endpoint = recommendation.category === 'mind'
      ? '/api/tasks/mind/'
      : '/api/tasks/body/';
    
    const taskData = {
      template_id: recommendation.id,
      scheduled_at: recommendation.suggested_schedule,
      params: recommendation.default_params || {},
      created_by: 'user',
      status: 'pending'
    };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskData)
      });
      
      const createdTask = await response.json();
      console.log('Task created:', createdTask);
      // Actualizar UI
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  return (
    <div className="recommendations">
      <div className="controls">
        <label>
          <input
            type="checkbox"
            checked={useAI}
            onChange={(e) => setUseAI(e.target.checked)}
          />
          Usar IA para recomendaciones
        </label>
        <button onClick={fetchRecommendations} disabled={loading}>
          {loading ? 'Cargando...' : 'Obtener Recomendaciones'}
        </button>
      </div>

      {recommendations.length > 0 && (
        <div className="recommendations-list">
          <h3>Tareas Recomendadas</h3>
          {recommendations.map((rec, index) => (
            <div key={rec.id} className="recommendation-card">
              <span className="badge">{rec.category}</span>
              <h4>{rec.name}</h4>
              <p>{rec.desc}</p>
              <p className="reason">{rec.reason}</p>
              <p className="schedule">
                Sugerido: {new Date(rec.suggested_schedule).toLocaleString()}
              </p>
              <p className="xp">+{rec.default_xp} XP</p>
              <button onClick={() => createTaskFromRecommendation(rec)}>
                Agregar a mis tareas
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
"""

print("=" * 80)
print("EJEMPLOS DE USO - Sistema de Recomendaciones de Tareas")
print("=" * 80)

print("\n### Ejemplo 1: cURL - Recomendaciones Básicas")
print(curl_example_1)

print("\n### Ejemplo 2: cURL - Recomendaciones con IA")
print(curl_example_2)

print("\n### Ejemplo 3: Python - Crear tarea desde recomendación")
print(python_example)

print("\n### Ejemplo 4: JavaScript/React - Componente completo")
print(javascript_example)
