# Goal Task Recommendations - Ejemplos cURL

## Variables
```bash
# Configura estas variables
export API_URL="http://localhost:5000"
export JWT_TOKEN="tu-token-jwt-aqui"
export GOAL_ID="tu-goal-id-aqui"
```

## 1. Login (Para obtener token)
```bash
curl -X POST "${API_URL}/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

## 2. Crear un Goal de Prueba
```bash
curl -X POST "${API_URL}/api/goals" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender Python Avanzado",
    "description": "Dominar conceptos avanzados de Python en 6 meses",
    "start_date": "2025-10-08",
    "end_date": "2026-04-08",
    "target_value": 100,
    "is_active": true
  }'
```

## 3. Obtener Recomendaciones Simples (GET)
```bash
curl -X GET "${API_URL}/api/goals/${GOAL_ID}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json"
```

## 4. Obtener Recomendaciones con Contexto (POST)
```bash
curl -X POST "${API_URL}/api/goals/${GOAL_ID}/recommendations?use_ai=true&count=3" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Tengo poco tiempo libre, solo 1 hora diaria",
      "available_time": "1 hora por día en las mañanas (6-7 AM)",
      "resources": [
        "Laptop personal",
        "Curso Udemy Python avanzado",
        "Libro Fluent Python",
        "ChatGPT"
      ],
      "preferences": "Prefiero tareas prácticas de 30-60 minutos con proyectos reales"
    }
  }'
```

## 5. Recomendaciones sin IA (Lógica Simple)
```bash
curl -X GET "${API_URL}/api/goals/${GOAL_ID}/recommendations?use_ai=false&count=5" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json"
```

## 6. Pedir Solo 3 Recomendaciones
```bash
curl -X GET "${API_URL}/api/goals/${GOAL_ID}/recommendations?use_ai=true&count=3" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json"
```

## 7. Recomendaciones con Contexto Detallado
```bash
curl -X POST "${API_URL}/api/goals/${GOAL_ID}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Soy principiante total en programación. No sé por dónde empezar y me siento abrumado con tanta información.",
      "available_time": "2-3 horas diarias después del trabajo (7-10 PM)",
      "resources": [
        "Laptop con Windows 11",
        "Internet estable",
        "Cuenta GitHub",
        "VS Code instalado"
      ],
      "preferences": "Me gusta aprender haciendo proyectos prácticos. Prefiero videos cortos a leer documentación larga. Quiero ver resultados rápido para mantenerme motivado."
    }
  }'
```

## 8. Caso: Objetivo de Fitness
```bash
# Primero crear el goal
curl -X POST "${API_URL}/api/goals" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Perder 10kg en 3 meses",
    "description": "Bajar de peso de forma saludable combinando ejercicio y nutrición",
    "start_date": "2025-10-08",
    "end_date": "2026-01-08",
    "target_value": 10,
    "is_active": true
  }'

# Obtener recomendaciones
curl -X POST "${API_URL}/api/goals/[GOAL_ID]/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "He intentado varias dietas sin éxito. Me cuesta mantener la consistencia.",
      "available_time": "1 hora por día para ejercicio (mañanas), 30 min para preparar comidas",
      "resources": [
        "Membresía de gimnasio",
        "App de conteo de calorías",
        "Báscula inteligente"
      ],
      "preferences": "Prefiero ejercicios de cardio moderado. No me gustan las dietas muy restrictivas."
    }
  }'
```

## 9. Caso: Objetivo Profesional
```bash
# Crear goal
curl -X POST "${API_URL}/api/goals" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Conseguir trabajo como Data Scientist",
    "description": "Prepararme y conseguir mi primer trabajo en ciencia de datos",
    "start_date": "2025-10-08",
    "end_date": "2026-06-08",
    "target_value": 100,
    "is_active": true
  }'

# Obtener recomendaciones
curl -X POST "${API_URL}/api/goals/[GOAL_ID]/recommendations?use_ai=true&count=7" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Tengo conocimientos básicos de Python pero no experiencia laboral en DS",
      "available_time": "15-20 horas por semana",
      "resources": [
        "Laptop con GPU",
        "Curso Coursera ML",
        "Kaggle account",
        "LinkedIn premium"
      ],
      "preferences": "Quiero construir un portfolio sólido con proyectos reales. Necesito preparar entrevistas técnicas."
    }
  }'
```

## 10. Verificar Progreso del Goal
```bash
# Ver todas las tareas del goal
curl -X GET "${API_URL}/api/goals/${GOAL_ID}/tasks" \
  -H "Authorization: Bearer ${JWT_TOKEN}"

# Ver progreso
curl -X GET "${API_URL}/api/goals/${GOAL_ID}/progress" \
  -H "Authorization: Bearer ${JWT_TOKEN}"
```

## 11. Crear Tarea desde Recomendación
```bash
# Después de obtener recomendaciones, crear una tarea
curl -X POST "${API_URL}/api/goals/${GOAL_ID}/tasks" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Completar tutorial básico de Python",
    "description": "Seguir tutorial introductorio de Python cubriendo variables, funciones y estructuras de control",
    "priority": "high",
    "due_at": "2025-10-15T18:00:00Z"
  }'
```

## 12. Script Completo de Prueba
```bash
#!/bin/bash

# Configuración
API_URL="http://localhost:5000"
EMAIL="test@example.com"
PASSWORD="test123"

echo "=== 1. LOGIN ==="
LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")

JWT_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')
echo "Token obtenido: ${JWT_TOKEN:0:20}..."

echo -e "\n=== 2. CREAR GOAL ==="
GOAL_RESPONSE=$(curl -s -X POST "${API_URL}/api/goals" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender Machine Learning",
    "description": "Dominar ML y crear proyectos reales",
    "start_date": "2025-10-08",
    "end_date": "2026-04-08",
    "target_value": 100,
    "is_active": true
  }')

GOAL_ID=$(echo $GOAL_RESPONSE | jq -r '.id')
echo "Goal creado: $GOAL_ID"
echo "Título: $(echo $GOAL_RESPONSE | jq -r '.title')"

echo -e "\n=== 3. OBTENER RECOMENDACIONES ==="
RECS_RESPONSE=$(curl -s -X POST "${API_URL}/api/goals/${GOAL_ID}/recommendations?use_ai=true&count=5" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "current_challenges": "Sin experiencia previa en ML",
      "available_time": "2 horas diarias",
      "resources": ["Laptop", "Curso Coursera"],
      "preferences": "Aprendizaje práctico"
    }
  }')

echo "Método: $(echo $RECS_RESPONSE | jq -r '.method')"
echo "Recomendaciones generadas: $(echo $RECS_RESPONSE | jq '.recommendations | length')"
echo -e "\nPrimera recomendación:"
echo $RECS_RESPONSE | jq '.recommendations[0]'

echo -e "\n=== 4. CREAR PRIMERA TAREA ==="
FIRST_REC_TITLE=$(echo $RECS_RESPONSE | jq -r '.recommendations[0].title')
FIRST_REC_DESC=$(echo $RECS_RESPONSE | jq -r '.recommendations[0].description')
FIRST_REC_PRIORITY=$(echo $RECS_RESPONSE | jq -r '.recommendations[0].priority')

TASK_RESPONSE=$(curl -s -X POST "${API_URL}/api/goals/${GOAL_ID}/tasks" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"${FIRST_REC_TITLE}\",
    \"description\": \"${FIRST_REC_DESC}\",
    \"priority\": \"${FIRST_REC_PRIORITY}\"
  }")

echo "Tarea creada: $(echo $TASK_RESPONSE | jq -r '.title')"

echo -e "\n=== 5. VER TODAS LAS TAREAS DEL GOAL ==="
curl -s -X GET "${API_URL}/api/goals/${GOAL_ID}/tasks" \
  -H "Authorization: Bearer ${JWT_TOKEN}" | jq '.[] | {title: .title, priority: .priority}'

echo -e "\n✅ Prueba completada!"
```

## Notas

- Reemplaza `${API_URL}`, `${JWT_TOKEN}` y `${GOAL_ID}` con tus valores reales
- Para formatear JSON responses, instala `jq`: `brew install jq` (Mac) o `apt-get install jq` (Linux)
- Windows PowerShell: Usa comillas dobles y escapa las comillas internas
- Los ejemplos usan `-s` en algunos casos para salida silenciosa (sin progreso)
- Agrega `-v` para modo verbose y ver headers HTTP
