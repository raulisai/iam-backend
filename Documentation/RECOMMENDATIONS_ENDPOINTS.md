# Endpoints de Recomendaciones de Tareas

## 📋 Resumen

El sistema ahora cuenta con **3 endpoints** de recomendaciones:

1. **General** - Mezcla de mind y body (3 tareas)
2. **Mind** - Solo tareas mentales (personalizable 1-10)
3. **Body** - Solo tareas físicas (personalizable 1-10)

---

## 🔗 Endpoints

### 1. Recomendaciones Generales (Mixtas)

```
GET /api/tasks/recommendations/
```

Retorna 3 recomendaciones balanceadas entre tareas de mente y cuerpo.

#### Query Parameters
- `use_ai` (boolean, opcional): Usar IA para recomendaciones. Default: `false`

#### Ejemplo
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Respuesta
```json
{
  "recommendations": [
    {
      "id": "uuid-1",
      "name": "Meditación Matutina",
      "category": "mind",
      "default_xp": 10,
      "suggested_schedule": "2025-10-06T14:00:00Z",
      "reason": "Recomendado para balancear..."
    },
    {
      "id": "uuid-2",
      "name": "Cardio 30min",
      "category": "body",
      "default_xp": 15,
      "suggested_schedule": "2025-10-06T18:00:00Z",
      "reason": "Nuevo desafío..."
    },
    {
      "id": "uuid-3",
      "name": "Lectura",
      "category": "mind",
      "default_xp": 8,
      "suggested_schedule": "2025-10-06T22:00:00Z",
      "reason": "Continuar progreso..."
    }
  ],
  "method": "pattern_based",
  "generated_at": "2025-10-06T10:30:00Z",
  "task_history_count": 12
}
```

---

### 2. Recomendaciones de Tareas Mentales

```
GET /api/tasks/recommendations/mind
```

Retorna recomendaciones **solo de tareas de mente** (lectura, meditación, estudio, etc).

#### Query Parameters
- `use_ai` (boolean, opcional): Usar IA. Default: `false`
- `count` (integer, opcional): Cantidad de recomendaciones (1-10). Default: `3`

#### Ejemplos

**Básico (3 tareas)**
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Personalizado (5 tareas)**
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind?count=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Con IA**
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind?use_ai=true&count=3" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Respuesta
```json
{
  "recommendations": [
    {
      "id": "uuid-1",
      "key": "meditation_morning",
      "name": "Meditación Matutina",
      "category": "mind",
      "desc": "Sesión de meditación para comenzar el día",
      "default_xp": 10,
      "default_params": {
        "duration": 15
      },
      "suggested_schedule": "2025-10-06T14:00:00Z",
      "reason": "Nueva actividad para expandir tu rutina"
    },
    {
      "id": "uuid-2",
      "key": "reading_session",
      "name": "Lectura Educativa",
      "category": "mind",
      "desc": "20 minutos de lectura",
      "default_xp": 8,
      "default_params": {
        "duration": 20
      },
      "suggested_schedule": "2025-10-06T18:00:00Z",
      "reason": "Continuar tu progreso mental"
    },
    {
      "id": "uuid-3",
      "key": "journaling",
      "name": "Diario Personal",
      "category": "mind",
      "desc": "Reflexión y escritura",
      "default_xp": 12,
      "default_params": {
        "duration": 25
      },
      "suggested_schedule": "2025-10-06T22:00:00Z",
      "reason": "Recomendado para balance mental"
    }
  ],
  "method": "pattern_based",
  "generated_at": "2025-10-06T10:30:00Z",
  "task_history_count": 12,
  "category": "mind"
}
```

---

### 3. Recomendaciones de Tareas Físicas

```
GET /api/tasks/recommendations/body
```

Retorna recomendaciones **solo de tareas de cuerpo** (ejercicio, yoga, deportes, etc).

#### Query Parameters
- `use_ai` (boolean, opcional): Usar IA. Default: `false`
- `count` (integer, opcional): Cantidad de recomendaciones (1-10). Default: `3`

#### Ejemplos

**Básico (3 tareas)**
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/body" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Personalizado (4 tareas)**
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/body?count=4" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Con IA**
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/body?use_ai=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Respuesta
```json
{
  "recommendations": [
    {
      "id": "uuid-1",
      "key": "cardio_30min",
      "name": "Cardio 30 minutos",
      "category": "body",
      "desc": "Ejercicio cardiovascular moderado",
      "default_xp": 15,
      "default_params": {
        "duration": 30,
        "intensity": "moderate"
      },
      "suggested_schedule": "2025-10-06T14:00:00Z",
      "reason": "Nuevo desafío para expandir tu rutina"
    },
    {
      "id": "uuid-2",
      "key": "yoga_session",
      "name": "Sesión de Yoga",
      "category": "body",
      "desc": "Práctica de yoga para flexibilidad",
      "default_xp": 12,
      "default_params": {
        "duration": 45,
        "level": "beginner"
      },
      "suggested_schedule": "2025-10-06T18:00:00Z",
      "reason": "Recomendado para balance físico"
    },
    {
      "id": "uuid-3",
      "key": "strength_training",
      "name": "Entrenamiento de Fuerza",
      "category": "body",
      "desc": "Ejercicios con pesas",
      "default_xp": 18,
      "default_params": {
        "duration": 40,
        "equipment": "dumbbells"
      },
      "suggested_schedule": "2025-10-06T22:00:00Z",
      "reason": "Continuar tu progreso físico"
    }
  ],
  "method": "pattern_based",
  "generated_at": "2025-10-06T10:30:00Z",
  "task_history_count": 12,
  "category": "body"
}
```

---

## 📊 Comparación de Endpoints

| Endpoint | Retorna | Count | Uso Principal |
|----------|---------|-------|---------------|
| `/api/tasks/recommendations/` | Mezcla mind + body | Fijo: 3 | Vista general balanceada |
| `/api/tasks/recommendations/mind` | Solo mind | 1-10 | Enfoque en tareas mentales |
| `/api/tasks/recommendations/body` | Solo body | 1-10 | Enfoque en tareas físicas |

---

## 💡 Casos de Uso

### Caso 1: Dashboard Principal
```javascript
// Mostrar recomendaciones balanceadas
const recommendations = await fetch('/api/tasks/recommendations/', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Siempre 3 tareas (mezcla de mind y body)
```

### Caso 2: Sección "Mente"
```javascript
// Usuario navega a sección de tareas mentales
const mindRecommendations = await fetch('/api/tasks/recommendations/mind?count=5', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// 5 recomendaciones solo de mente
```

### Caso 3: Sección "Cuerpo"
```javascript
// Usuario navega a sección de tareas físicas
const bodyRecommendations = await fetch('/api/tasks/recommendations/body?count=4', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// 4 recomendaciones solo de cuerpo
```

### Caso 4: Modo Experto con IA
```javascript
// Usuario premium quiere recomendaciones inteligentes
const aiMindRecs = await fetch(
  '/api/tasks/recommendations/mind?use_ai=true&count=3',
  { headers: { 'Authorization': `Bearer ${token}` } }
).then(r => r.json());

// 3 recomendaciones de mente generadas por IA
```

---

## 🎨 Integración Frontend - React

### Componente para Mind
```jsx
const MindRecommendations = ({ token }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [count, setCount] = useState(3);

  const fetchMindRecommendations = async () => {
    const response = await fetch(
      `http://localhost:5000/api/tasks/recommendations/mind?count=${count}`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    const data = await response.json();
    setRecommendations(data.recommendations);
  };

  return (
    <div className="mind-recommendations">
      <h2>🧠 Recomendaciones Mentales</h2>
      <select value={count} onChange={(e) => setCount(e.target.value)}>
        <option value="3">3 tareas</option>
        <option value="5">5 tareas</option>
        <option value="10">10 tareas</option>
      </select>
      <button onClick={fetchMindRecommendations}>Actualizar</button>
      
      {recommendations.map(rec => (
        <div key={rec.id} className="recommendation-card mind">
          <h3>{rec.name}</h3>
          <p>{rec.desc}</p>
          <span>+{rec.default_xp} XP</span>
        </div>
      ))}
    </div>
  );
};
```

### Componente para Body
```jsx
const BodyRecommendations = ({ token }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [count, setCount] = useState(3);

  const fetchBodyRecommendations = async () => {
    const response = await fetch(
      `http://localhost:5000/api/tasks/recommendations/body?count=${count}`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    const data = await response.json();
    setRecommendations(data.recommendations);
  };

  return (
    <div className="body-recommendations">
      <h2>💪 Recomendaciones Físicas</h2>
      <select value={count} onChange={(e) => setCount(e.target.value)}>
        <option value="3">3 tareas</option>
        <option value="5">5 tareas</option>
        <option value="10">10 tareas</option>
      </select>
      <button onClick={fetchBodyRecommendations}>Actualizar</button>
      
      {recommendations.map(rec => (
        <div key={rec.id} className="recommendation-card body">
          <h3>{rec.name}</h3>
          <p>{rec.desc}</p>
          <span>+{rec.default_xp} XP</span>
        </div>
      ))}
    </div>
  );
};
```

### Componente con Tabs
```jsx
const TaskRecommendations = ({ token }) => {
  const [activeTab, setActiveTab] = useState('general');
  
  return (
    <div className="task-recommendations">
      <div className="tabs">
        <button 
          className={activeTab === 'general' ? 'active' : ''}
          onClick={() => setActiveTab('general')}
        >
          🎯 General
        </button>
        <button 
          className={activeTab === 'mind' ? 'active' : ''}
          onClick={() => setActiveTab('mind')}
        >
          🧠 Mente
        </button>
        <button 
          className={activeTab === 'body' ? 'active' : ''}
          onClick={() => setActiveTab('body')}
        >
          💪 Cuerpo
        </button>
      </div>
      
      {activeTab === 'general' && <GeneralRecommendations token={token} />}
      {activeTab === 'mind' && <MindRecommendations token={token} />}
      {activeTab === 'body' && <BodyRecommendations token={token} />}
    </div>
  );
};
```

---

## ✅ Ventajas del Sistema Dividido

1. **Flexibilidad**: El usuario elige cuántas recomendaciones ver (1-10)
2. **Especialización**: Endpoints dedicados para cada categoría
3. **UX Mejorada**: Secciones separadas en la UI
4. **Performance**: Consultas más específicas y rápidas
5. **Escalable**: Fácil agregar más categorías en el futuro

---

## 🔄 Migración desde Endpoint General

Si ya usabas el endpoint general, no hay breaking changes:

```javascript
// ANTES - sigue funcionando
fetch('/api/tasks/recommendations/')

// AHORA - más opciones
fetch('/api/tasks/recommendations/mind?count=5')
fetch('/api/tasks/recommendations/body?count=3')
```

---

## 📖 Referencias

- [Documentación completa](./TASK_RECOMMENDATIONS.md)
- [Guía rápida](./QUICKSTART_RECOMMENDATIONS.md)
- [Ejemplos de código](./RECOMMENDATION_EXAMPLES.py)
