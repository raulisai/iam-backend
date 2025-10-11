# ⚡ Quick Start - Time Optimizer API

## Endpoints Disponibles

### 1. Calcular Tiempo Disponible
```bash
GET /api/time-optimizer/available-time
Authorization: Bearer {token}
```

**¿Cuándo usarlo?** Cuando quieras saber cuántas horas libres tienes disponibles.

**Respuesta**: Desglose de tu tiempo (trabajo, sueño, tiempo libre)

---

### 2. Obtener Horario Optimizado del Día
```bash
GET /api/time-optimizer/optimize-day?date=2025-10-09
Authorization: Bearer {token}
```

**¿Cuándo usarlo?** Para planificar tu día completo.

**Respuesta**: 
- ✅ Tareas del día organizadas por prioridad
- ⏰ Horarios específicos (start_time, end_time)
- 📊 Métricas de productividad
- 🎯 Tasks priorizadas por deadline

---

### 3. ¿Qué Debo Hacer AHORA?
```bash
GET /api/time-optimizer/tasks-now
Authorization: Bearer {token}
```

**¿Cuándo usarlo?** Cuando termines una tarea y quieras saber qué sigue.

**Respuesta**:
- 🔥 Top 3-5 tareas más urgentes AHORA
- ⚡ "Quick wins" (tareas de 30min o menos)
- ⏳ Tiempo restante en el slot actual

---

### 4. ¿Qué Me Falta Hoy?
```bash
GET /api/time-optimizer/remaining-day
Authorization: Bearer {token}
```

**¿Cuándo usarlo?** Para revisar tu progreso durante el día.

**Respuesta**:
- 📋 Tareas que aún no has hecho
- ✓ Porcentaje de completitud del día
- ⏰ Tiempo restante disponible
- ✅ ¿Puedes completar todo hoy?

---

## 🚀 Ejemplo de Uso

### Flujo típico de un día:

```bash
# 1. Por la mañana: Ver plan del día
curl -X GET "http://localhost:5000/api/time-optimizer/optimize-day" \
  -H "Authorization: Bearer tu_token_jwt"

# Respuesta: "Tienes 8 tareas hoy, empieza con 'Proyecto Final' a las 6:00 AM"


# 2. Durante el día: ¿Qué hago ahora?
curl -X GET "http://localhost:5000/api/time-optimizer/tasks-now" \
  -H "Authorization: Bearer tu_token_jwt"

# Respuesta: "Ahora es 2:00 PM, haz 'Revisar código' (45 min)"


# 3. Por la tarde: ¿Qué me falta?
curl -X GET "http://localhost:5000/api/time-optimizer/remaining-day" \
  -H "Authorization: Bearer tu_token_jwt"

# Respuesta: "Te quedan 3 tareas, 2.5 horas. ¡Puedes terminar todo!"
```

---

## 📊 El Algoritmo en Simple

1. **Resta las horas fijas**: Trabajo (8h) + Sueño (8h) + Aseo/Comida (2h) = 18h ocupadas
2. **Te quedan**: 6 horas libres para TUS tareas
3. **Prioriza**: 
   - Goals con deadline cercano → Máxima prioridad
   - Goals sin deadline → Alta prioridad
   - Mind/Body tasks → Media prioridad
4. **Distribuye**:
   - Mañana (6am-9am): Tareas de alta concentración
   - Tarde (5pm-10pm): Mix de tareas + ejercicio

---

## 🎯 Cómo Funciona la Priorización

```
Tarea con deadline MAÑANA:        Score = 90 puntos ⚠️⚠️⚠️
Tarea con deadline esta semana:   Score = 60 puntos ⚠️⚠️
Tarea de goal sin deadline:       Score = 30 puntos ⚠️
Tarea de mind/body:               Score = 15 puntos
```

**El sistema SIEMPRE pone primero las tareas con deadline cercano.**

---

## ✅ Métricas Importantes

### Efficiency Score (Eficiencia)
- **85-100%**: Excelente - Aprovechas casi todo tu tiempo
- **70-84%**: Bien - Buen uso del tiempo
- **<70%**: Puedes agregar más tareas

### Balance Score (Balance)
- **95-100%**: Perfecto balance entre goals/mind/body
- **80-94%**: Buen balance
- **<80%**: Desbalanceado (pero puede ser OK si hay deadlines urgentes)

### Productivity Score (Productividad)
- **Combina** Efficiency + Balance
- **85-100%**: ¡Día súper productivo! 🚀
- **70-84%**: Día productivo ✓
- **<70%**: Puedes mejorar

---

## 🔧 Configuración en tu Profile

Asegúrate de tener esto en tu perfil:

```json
{
  "work_schedules": "9:00-17:00",
  "hours_available_to_week": 40,
  "hours_used_to_week": 15.5
}
```

**Importante**: El campo `end_at` en tus `goals` se usa para calcular deadlines.

---

## 💡 Tips Pro

1. **Consulta `/tasks-now` frecuentemente** durante el día para mantenerte enfocado
2. **Los "quick wins"** son perfectos cuando tienes poco tiempo
3. **Si una tarea vence mañana**, el sistema la pondrá PRIMERO automáticamente
4. **El buffer de 15 minutos** entre tareas te da tiempo para descansar
5. **Marca tareas completadas** para mejorar las predicciones futuras

---

## 📚 Documentación Completa

- [Documentación Técnica Completa](./TIME_OPTIMIZER_SYSTEM.md)
- [Diagramas Visuales](./TIME_OPTIMIZER_DIAGRAMS.md)

---

**¿Preguntas?** Revisa la documentación completa o el código en:
- `services/time_optimizer_service.py`
- `controllers/time_optimizer_controller.py`
- `routes/time_optimizer_routes.py`
