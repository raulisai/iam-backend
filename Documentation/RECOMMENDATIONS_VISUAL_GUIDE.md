# 🎯 Guía Visual: Endpoints de Recomendaciones

## 📍 Los 3 Endpoints

```
┌─────────────────────────────────────────────────────────────┐
│                    RECOMENDACIONES                          │
└─────────────────────────────────────────────────────────────┘
                              │
                 ┌────────────┼────────────┐
                 │            │            │
          ┌──────▼─────┐ ┌───▼────┐ ┌────▼─────┐
          │  GENERAL   │ │  MIND  │ │   BODY   │
          │  (Mixto)   │ │  🧠    │ │   💪     │
          └────────────┘ └────────┘ └──────────┘
               │              │           │
          Fijo: 3        1-10 tareas  1-10 tareas
         Mind + Body      Solo Mind    Solo Body
```

---

## 🔀 Endpoint 1: General (Mixto)

### URL
```
GET /api/tasks/recommendations/
```

### Características
- ✅ Retorna **exactamente 3 tareas**
- ✅ **Mezcla** de mind y body (balanceado)
- ✅ Ideal para **dashboard principal**
- ✅ No personalizable (siempre 3)

### Ejemplo Visual
```
┌─────────────────────────────────────┐
│   RECOMENDACIONES PARA HOY          │
├─────────────────────────────────────┤
│ 🧠 Meditación Matutina    +10 XP   │
│ 💪 Cardio 30min           +15 XP   │
│ 🧠 Lectura                +8 XP    │
└─────────────────────────────────────┘
Total: 3 tareas (2 mind, 1 body)
```

### Código
```bash
curl -X GET "http://localhost:5000/api/tasks/recommendations/" \
  -H "Authorization: Bearer TOKEN"
```

---

## 🧠 Endpoint 2: Mind (Tareas Mentales)

### URL
```
GET /api/tasks/recommendations/mind
```

### Características
- ✅ Retorna **1 a 10 tareas** (personalizable)
- ✅ **Solo tareas de mente**: lectura, meditación, estudio
- ✅ Ideal para **sección "Mente"** en la app
- ✅ Parámetro `count` para controlar cantidad

### Ejemplo Visual
```
┌─────────────────────────────────────┐
│   🧠 RECOMENDACIONES MENTALES       │
├─────────────────────────────────────┤
│ 1. Meditación Matutina    +10 XP   │
│ 2. Lectura Educativa      +8 XP    │
│ 3. Diario Personal        +12 XP   │
│ 4. Curso Online           +15 XP   │
│ 5. Planificación          +10 XP   │
└─────────────────────────────────────┘
Total: 5 tareas MIND
```

### Código
```bash
# 3 tareas (default)
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind" \
  -H "Authorization: Bearer TOKEN"

# 5 tareas (personalizado)
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind?count=5" \
  -H "Authorization: Bearer TOKEN"

# Con IA
curl -X GET "http://localhost:5000/api/tasks/recommendations/mind?use_ai=true" \
  -H "Authorization: Bearer TOKEN"
```

---

## 💪 Endpoint 3: Body (Tareas Físicas)

### URL
```
GET /api/tasks/recommendations/body
```

### Características
- ✅ Retorna **1 a 10 tareas** (personalizable)
- ✅ **Solo tareas de cuerpo**: ejercicio, yoga, deportes
- ✅ Ideal para **sección "Cuerpo"** en la app
- ✅ Parámetro `count` para controlar cantidad

### Ejemplo Visual
```
┌─────────────────────────────────────┐
│   💪 RECOMENDACIONES FÍSICAS        │
├─────────────────────────────────────┤
│ 1. Cardio 30min           +15 XP   │
│ 2. Sesión de Yoga         +12 XP   │
│ 3. Entrenamiento Fuerza   +18 XP   │
│ 4. Caminata                +8 XP   │
└─────────────────────────────────────┘
Total: 4 tareas BODY
```

### Código
```bash
# 3 tareas (default)
curl -X GET "http://localhost:5000/api/tasks/recommendations/body" \
  -H "Authorization: Bearer TOKEN"

# 4 tareas (personalizado)
curl -X GET "http://localhost:5000/api/tasks/recommendations/body?count=4" \
  -H "Authorization: Bearer TOKEN"

# Con IA
curl -X GET "http://localhost:5000/api/tasks/recommendations/body?use_ai=true" \
  -H "Authorization: Bearer TOKEN"
```

---

## 🎨 Diseño de UI Sugerido

### Opción A: Tabs
```
┌──────────────────────────────────────────────┐
│  [🎯 General] [🧠 Mente] [💪 Cuerpo]        │
├──────────────────────────────────────────────┤
│                                              │
│  Contenido según tab seleccionado           │
│                                              │
└──────────────────────────────────────────────┘
```

### Opción B: Secciones Separadas
```
┌──────────────────────────────────────────────┐
│  🎯 TUS RECOMENDACIONES DE HOY              │
│  ├─ 🧠 Meditación Matutina    +10 XP       │
│  ├─ 💪 Cardio 30min           +15 XP       │
│  └─ 🧠 Lectura                +8 XP        │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  🧠 MÁS TAREAS MENTALES                     │
│  [Ver 5 más ▼]                              │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  💪 MÁS TAREAS FÍSICAS                      │
│  [Ver 5 más ▼]                              │
└──────────────────────────────────────────────┘
```

### Opción C: Cards con Filtro
```
┌──────────────────────────────────────────────┐
│  RECOMENDACIONES                             │
│  [Todas ▼] [🧠 Mente] [💪 Cuerpo]           │
│  Cantidad: [3 ▼] [🤖 Usar IA]               │
├──────────────────────────────────────────────┤
│  📋 Lista de recomendaciones                 │
└──────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Usuario

### Escenario 1: Usuario casual
```
1. Abre la app
2. Ve dashboard con 3 recomendaciones (General)
3. Hace click en "Agregar tarea"
4. Tarea agregada ✅
```

### Escenario 2: Usuario enfocado en mente
```
1. Navega a sección "🧠 Mente"
2. Ve 5 recomendaciones mentales
3. Selecciona 2 tareas
4. Agrega ambas ✅
```

### Escenario 3: Usuario enfocado en cuerpo
```
1. Navega a sección "💪 Cuerpo"
2. Cambia count a 7 tareas
3. Ve 7 recomendaciones físicas
4. Selecciona 3 tareas
5. Agrega las 3 ✅
```

### Escenario 4: Usuario premium con IA
```
1. Activa modo IA 🤖
2. Solicita recomendaciones mind
3. IA analiza historial profundamente
4. Ve recomendaciones ultra-personalizadas
5. Agrega tareas ✅
```

---

## 📊 Matriz de Decisión: ¿Qué Endpoint Usar?

| Situación | Endpoint | Parámetros |
|-----------|----------|------------|
| Dashboard principal | `/recommendations/` | ninguno |
| Vista rápida balanceada | `/recommendations/` | ninguno |
| Sección "Mente" | `/recommendations/mind` | `count=5` |
| Sección "Cuerpo" | `/recommendations/body` | `count=5` |
| Lista completa mental | `/recommendations/mind` | `count=10` |
| Lista completa física | `/recommendations/body` | `count=10` |
| Usuario premium | cualquiera | `use_ai=true` |
| Pocas opciones | cualquiera | `count=1 o 2` |
| Muchas opciones | mind o body | `count=8-10` |

---

## 🎯 Casos de Uso por Tipo de Aplicación

### App Móvil
```
Pantalla 1: Home
  → GET /recommendations/ (3 tareas mixtas)

Pantalla 2: Tareas Mentales
  → GET /recommendations/mind?count=5

Pantalla 3: Tareas Físicas
  → GET /recommendations/body?count=5
```

### Web Dashboard
```
Sidebar: Recomendaciones Rápidas
  → GET /recommendations/ (3 tareas)

Modal "Más Tareas Mentales"
  → GET /recommendations/mind?count=10

Modal "Más Tareas Físicas"
  → GET /recommendations/body?count=10
```

### Smartwatch / Widget
```
Pantalla pequeña
  → GET /recommendations/mind?count=1
  → GET /recommendations/body?count=1
  
(Una tarea mental + una física)
```

---

## ✨ Tips de Implementación

### 1. Carga Inicial
```javascript
// Cargar recomendaciones generales al abrir la app
useEffect(() => {
  fetch('/api/tasks/recommendations/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(r => r.json())
  .then(data => setRecommendations(data.recommendations));
}, []);
```

### 2. Navegación entre Secciones
```javascript
const loadSection = (section) => {
  const endpoints = {
    'general': '/api/tasks/recommendations/',
    'mind': '/api/tasks/recommendations/mind?count=5',
    'body': '/api/tasks/recommendations/body?count=5'
  };
  
  fetch(endpoints[section], {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(r => r.json())
  .then(data => setRecommendations(data.recommendations));
};
```

### 3. Selector de Cantidad
```javascript
<select onChange={(e) => {
  fetch(`/api/tasks/recommendations/mind?count=${e.target.value}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(r => r.json())
  .then(data => setRecommendations(data.recommendations));
}}>
  <option value="3">3 tareas</option>
  <option value="5">5 tareas</option>
  <option value="10">10 tareas</option>
</select>
```

---

## 🚀 Resumen Rápido

```
ENDPOINT                              RETORNA              COUNT
────────────────────────────────────────────────────────────────
/recommendations/                     Mind + Body          Fijo: 3
/recommendations/mind                 Solo Mind            1-10
/recommendations/body                 Solo Body            1-10

TODOS soportan: ?use_ai=true
```

¡Ahora tienes 3 endpoints flexibles para diferentes necesidades! 🎉
