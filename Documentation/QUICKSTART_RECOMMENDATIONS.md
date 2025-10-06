# Guía Rápida: Integración del Sistema de Recomendaciones

## 🚀 Inicio Rápido

### 1. Ejecutar el Servidor
```bash
python app.py
```

### 2. Probar el Endpoint

#### Opción A: Con cURL
```bash
# Recomendaciones básicas (rápidas)
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Recomendaciones con IA (más personalizadas)
curl -X GET "http://localhost:5000/api/tasks/recommendations/?use_ai=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Opción B: Con Postman
1. Método: `GET`
2. URL: `http://localhost:5000/api/tasks/recommendations/`
3. Headers:
   - `Authorization: Bearer YOUR_JWT_TOKEN`
4. Query Params (opcional):
   - `use_ai: true`

### 3. Respuesta Esperada
```json
{
  "recommendations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
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
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "key": "cardio_30min",
      "name": "Cardio 30 minutos",
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
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "key": "reading_20min",
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

## 📱 Integración Frontend

### React Component Completo
```jsx
import React, { useState, useEffect } from 'react';

const TaskRecommendations = ({ token }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [useAI, setUseAI] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const url = useAI 
        ? 'http://localhost:5000/api/tasks/recommendations/?use_ai=true'
        : 'http://localhost:5000/api/tasks/recommendations/';
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Error al obtener recomendaciones');
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTaskFromRecommendation = async (recommendation) => {
    try {
      const endpoint = recommendation.category === 'mind'
        ? 'http://localhost:5000/api/tasks/mind/'
        : 'http://localhost:5000/api/tasks/body/';
      
      const taskData = {
        template_id: recommendation.id,
        scheduled_at: recommendation.suggested_schedule,
        params: recommendation.default_params || {},
        created_by: 'user',
        status: 'pending'
      };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskData)
      });
      
      if (!response.ok) {
        throw new Error('Error al crear tarea');
      }
      
      const createdTask = await response.json();
      alert(`¡Tarea "${recommendation.name}" creada exitosamente!`);
      return createdTask;
    } catch (err) {
      alert(`Error: ${err.message}`);
      console.error('Error creating task:', err);
    }
  };

  // Auto-cargar al montar
  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <div className="task-recommendations">
      <div className="recommendations-header">
        <h2>Tareas Recomendadas para Ti</h2>
        
        <div className="controls">
          <label className="ai-toggle">
            <input
              type="checkbox"
              checked={useAI}
              onChange={(e) => setUseAI(e.target.checked)}
            />
            <span>Usar IA para recomendaciones más inteligentes</span>
          </label>
          
          <button 
            onClick={fetchRecommendations} 
            disabled={loading}
            className="refresh-btn"
          >
            {loading ? '🔄 Cargando...' : '🔄 Actualizar'}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {recommendations.length > 0 && (
        <div className="recommendations-grid">
          {recommendations.map((rec, index) => (
            <div key={rec.id} className="recommendation-card">
              <div className="card-header">
                <span className={`category-badge ${rec.category}`}>
                  {rec.category === 'mind' ? '🧠' : '💪'} {rec.category}
                </span>
                <span className="xp-badge">+{rec.default_xp} XP</span>
              </div>
              
              <h3>{rec.name}</h3>
              <p className="description">{rec.desc}</p>
              
              <div className="card-details">
                <p className="reason">
                  <strong>Por qué:</strong> {rec.reason}
                </p>
                <p className="schedule">
                  <strong>Sugerido:</strong>{' '}
                  {new Date(rec.suggested_schedule).toLocaleString('es-ES', {
                    weekday: 'short',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
              
              <button 
                onClick={() => createTaskFromRecommendation(rec)}
                className="add-task-btn"
              >
                ➕ Agregar a mis tareas
              </button>
            </div>
          ))}
        </div>
      )}

      {!loading && recommendations.length === 0 && (
        <div className="empty-state">
          <p>No hay recomendaciones disponibles</p>
          <button onClick={fetchRecommendations}>
            Cargar recomendaciones
          </button>
        </div>
      )}
    </div>
  );
};

export default TaskRecommendations;
```

### CSS Sugerido
```css
.task-recommendations {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.recommendations-header {
  margin-bottom: 30px;
}

.recommendations-header h2 {
  margin-bottom: 15px;
  color: #333;
}

.controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.ai-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.refresh-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.recommendation-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.category-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.category-badge.mind {
  background: #e3f2fd;
  color: #1976d2;
}

.category-badge.body {
  background: #fff3e0;
  color: #f57c00;
}

.xp-badge {
  padding: 4px 12px;
  background: #4caf50;
  color: white;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.recommendation-card h3 {
  margin: 10px 0;
  color: #333;
  font-size: 18px;
}

.description {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
}

.card-details {
  margin: 15px 0;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
  font-size: 13px;
}

.reason {
  margin-bottom: 8px;
}

.schedule {
  color: #666;
}

.add-task-btn {
  width: 100%;
  padding: 10px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 15px;
}

.add-task-btn:hover {
  background: #45a049;
}

.error-message {
  padding: 15px;
  background: #ffebee;
  color: #c62828;
  border-radius: 6px;
  margin-bottom: 20px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}
```

## 🧪 Testing

### Probar manualmente
```bash
# 1. Asegúrate de tener el servidor corriendo
python app.py

# 2. En otra terminal, prueba el endpoint
cd test
python test_recommendations.py
```

### Verificar en el navegador
1. Abre Swagger UI: `http://localhost:5000/apidocs/`
2. Busca la sección "Task Recommendations"
3. Prueba el endpoint directamente desde ahí

## 🔑 Notas Importantes

1. **Token JWT**: Necesitas un token válido de autenticación
2. **Templates**: Deben existir templates en la base de datos
3. **Historial**: Funciona mejor con al menos 3-5 tareas previas
4. **IA**: El modo IA requiere `OPENAI_API_KEY` en `.env`

## 📞 Soporte

Para más información, revisa:
- `Documentation/TASK_RECOMMENDATIONS.md` - Documentación completa
- `Documentation/RECOMMENDATION_EXAMPLES.py` - Más ejemplos
- `Documentation/RECOMMENDATIONS_IMPLEMENTATION_SUMMARY.md` - Resumen técnico
