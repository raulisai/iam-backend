# Ejemplos de Uso - Sistema de Puntos

Ejemplos prácticos de cómo usar los endpoints del sistema de puntos.

## Configuración Inicial

```python
import requests

BASE_URL = "http://localhost:5000"
TOKEN = "your-jwt-token-here"

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}
```

---

## Ejemplo 1: Ver Resumen de Puntos

```python
# GET /api/points
response = requests.get(
    f"{BASE_URL}/api/points",
    headers=headers
)

print(response.json())
```

**Respuesta:**
```json
{
  "goal_points_target": 500,
  "goal_points_earned": 250,
  "goal_points_remaining": 250,
  "completion_percentage": 50.0
}
```

---

## Ejemplo 2: Calcular Puntos Disponibles

```python
# POST /api/points/calculate-target
response = requests.post(
    f"{BASE_URL}/api/points/calculate-target",
    headers=headers
)

result = response.json()
print(f"Mind: {result['mind_points']}")
print(f"Body: {result['body_points']}")
print(f"Goal: {result['goal_points']}")
print(f"Total: {result['total_target_points']}")
```

**Respuesta:**
```json
{
  "mind_points": 200,
  "body_points": 150,
  "goal_points": 150,
  "total_target_points": 500
}
```

---

## Ejemplo 3: Completar Tarea Mind y Sumar Puntos

```python
# Usuario completa una tarea de meditación de 50 puntos
response = requests.post(
    f"{BASE_URL}/api/points/add",
    headers=headers,
    json={
        "points": 50,
        "task_type": "mind"
    }
)

print(response.json())
```

**Respuesta:**
```json
{
  "previous_earned": 250,
  "points_added": 50,
  "new_earned": 300,
  "task_type": "mind"
}
```

**Efecto:**
- `goal_points_earned` pasa de 250 → 300
- `mind_score` en snapshot de hoy +50
- `total_score` se actualiza

---

## Ejemplo 4: Completar Tarea Body

```python
# Usuario completa ejercicio de 30 puntos
response = requests.post(
    f"{BASE_URL}/api/points/add",
    headers=headers,
    json={
        "points": 30,
        "task_type": "body"
    }
)

print(response.json())
```

**Respuesta:**
```json
{
  "previous_earned": 300,
  "points_added": 30,
  "new_earned": 330,
  "task_type": "body"
}
```

**Efecto:**
- `goal_points_earned` pasa de 300 → 330
- `body_score` en snapshot +30
- `total_score` se actualiza

---

## Ejemplo 5: Completar Tarea de Goal

```python
# Usuario completa una tarea de objetivo de 40 puntos
response = requests.post(
    f"{BASE_URL}/api/points/add",
    headers=headers,
    json={
        "points": 40,
        "task_type": "goal"
    }
)

print(response.json())
```

**Respuesta:**
```json
{
  "previous_earned": 330,
  "points_added": 40,
  "new_earned": 370,
  "task_type": "goal"
}
```

**Efecto:**
- `goal_points_earned` pasa de 330 → 370
- `goal_score` en snapshot +20 (50% de 40)
- `total_score` se actualiza

---

## Ejemplo 6: Restar Puntos (Corrección)

```python
# Se necesita restar 15 puntos por error
response = requests.post(
    f"{BASE_URL}/api/points/subtract",
    headers=headers,
    json={
        "points": 15,
        "task_type": "mind"
    }
)

print(response.json())
```

**Respuesta:**
```json
{
  "previous_earned": 370,
  "points_subtracted": 15,
  "new_earned": 355,
  "task_type": "mind"
}
```

**Efecto:**
- `goal_points_earned` pasa de 370 → 355
- `mind_score` en snapshot -15
- `total_score` se actualiza

---

## Ejemplo 7: Recalcular Todo

```python
# Recalcular target y obtener resumen completo
response = requests.post(
    f"{BASE_URL}/api/points/recalculate",
    headers=headers
)

result = response.json()
print("=== Target Breakdown ===")
print(result['target_breakdown'])
print("\n=== Points Summary ===")
print(result['points_summary'])
```

**Respuesta:**
```json
{
  "target_breakdown": {
    "mind_points": 200,
    "body_points": 150,
    "goal_points": 150,
    "total_target_points": 500
  },
  "points_summary": {
    "goal_points_target": 500,
    "goal_points_earned": 355,
    "goal_points_remaining": 145,
    "completion_percentage": 71.0
  }
}
```

---

## Ejemplo 8: Flujo Completo de Completar Tarea

```python
def complete_task(task_id, task_type, reward_xp):
    """
    Flujo completo al completar una tarea.
    
    1. Actualizar estado de la tarea
    2. Sumar puntos ganados
    3. Recalcular target (opcional)
    4. Obtener resumen actualizado
    """
    
    # 1. Actualizar estado de tarea (ejemplo con mind task)
    task_update = requests.patch(
        f"{BASE_URL}/api/mind-tasks/{task_id}",
        headers=headers,
        json={"status": "completed"}
    )
    
    # 2. Sumar puntos ganados
    points_response = requests.post(
        f"{BASE_URL}/api/points/add",
        headers=headers,
        json={
            "points": reward_xp,
            "task_type": task_type
        }
    )
    
    # 3. Recalcular target (opcional, los triggers SQL lo hacen automático)
    # recalc_response = requests.post(
    #     f"{BASE_URL}/api/points/calculate-target",
    #     headers=headers
    # )
    
    # 4. Obtener resumen actualizado
    summary_response = requests.get(
        f"{BASE_URL}/api/points",
        headers=headers
    )
    
    return {
        'points_added': points_response.json(),
        'summary': summary_response.json()
    }

# Usar la función
result = complete_task(
    task_id="123e4567-e89b-12d3-a456-426614174000",
    task_type="mind",
    reward_xp=50
)

print(result)
```

---

## Ejemplo 9: Dashboard de Progreso

```python
def get_daily_progress():
    """Obtener progreso diario con scores."""
    
    # Obtener puntos
    points_response = requests.get(
        f"{BASE_URL}/api/points",
        headers=headers
    )
    points = points_response.json()
    
    # Obtener snapshot de hoy (ejemplo asumiendo endpoint de snapshots)
    from datetime import date
    today = date.today().isoformat()
    
    snapshot_response = requests.get(
        f"{BASE_URL}/api/performance-snapshots?date={today}",
        headers=headers
    )
    snapshot = snapshot_response.json()
    
    # Construir dashboard
    dashboard = {
        'date': today,
        'points': {
            'target': points['goal_points_target'],
            'earned': points['goal_points_earned'],
            'remaining': points['goal_points_remaining'],
            'percentage': points['completion_percentage']
        },
        'scores': snapshot.get('metrics', {})
    }
    
    return dashboard

# Mostrar dashboard
dashboard = get_daily_progress()
print(f"Fecha: {dashboard['date']}")
print(f"Progreso: {dashboard['points']['percentage']}%")
print(f"Mind Score: {dashboard['scores'].get('mind_score', 0)}")
print(f"Body Score: {dashboard['scores'].get('body_score', 0)}")
print(f"Goal Score: {dashboard['scores'].get('goal_score', 0)}")
print(f"Total Score: {dashboard['scores'].get('total_score', 0)}")
```

---

## Ejemplo 10: Manejo de Errores

```python
def add_points_safe(points, task_type):
    """Función segura para agregar puntos con manejo de errores."""
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/points/add",
            headers=headers,
            json={
                "points": points,
                "task_type": task_type
            }
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        elif response.status_code == 400:
            return {
                'success': False,
                'error': 'Datos inválidos',
                'details': response.json()
            }
        elif response.status_code == 401:
            return {
                'success': False,
                'error': 'Token inválido o expirado'
            }
        elif response.status_code == 404:
            return {
                'success': False,
                'error': 'Perfil de usuario no encontrado'
            }
        else:
            return {
                'success': False,
                'error': f'Error desconocido: {response.status_code}'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Error de conexión: {str(e)}'
        }

# Usar función
result = add_points_safe(50, 'mind')
if result['success']:
    print(f"Puntos agregados: {result['data']}")
else:
    print(f"Error: {result['error']}")
```

---

## Testing con cURL

### Ver puntos
```bash
curl -X GET "http://localhost:5000/api/points" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Calcular target
```bash
curl -X POST "http://localhost:5000/api/points/calculate-target" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Agregar puntos
```bash
curl -X POST "http://localhost:5000/api/points/add" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"points": 50, "task_type": "mind"}'
```

### Restar puntos
```bash
curl -X POST "http://localhost:5000/api/points/subtract" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"points": 25, "task_type": "body"}'
```

### Recalcular
```bash
curl -X POST "http://localhost:5000/api/points/recalculate" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
