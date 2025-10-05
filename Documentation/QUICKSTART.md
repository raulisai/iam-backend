# 🎯 Quick Start Guide - Sistema de Agentes IA

## ⚡ En 5 Minutos

### 1️⃣ Lo que tienes
```
✅ Sistema de agentes IA completo
✅ 12+ funciones registradas
✅ Helpers listos para usar
✅ Documentación completa
⚠️ Necesita saldo en OpenAI API
```

### 2️⃣ Para usar en un endpoint existente

```python
# En controllers/task_controller.py

from lib.agent_helpers import ai_suggest_priority
import asyncio

def create_new_task(data):
    title = data.get('title')
    desc = data.get('desc', '')
    
    # ✨ Magia de IA aquí
    priority = asyncio.run(ai_suggest_priority(title, desc))
    
    # Resto del código normal...
```

### 3️⃣ Funciones disponibles

```python
from lib.agent_helpers import (
    ai_suggest_priority,      # Sugerir prioridad
    ai_suggest_category,      # Sugerir categoría  
    ai_analyze_user,          # Análisis de productividad
    ai_generate_tasks_for_goal # Generar tareas
)
```

### 4️⃣ Ejemplo completo

```python
from lib.agent_helpers import ai_suggest_priority, ai_suggest_category
import asyncio
from flask import jsonify
from lib.db import get_supabase

def create_smart_task(data):
    """Crear tarea con IA"""
    title = data.get('title')
    desc = data.get('desc', '')
    user_id = data.get('user_id')
    
    # IA sugiere prioridad y categoría
    try:
        priority = asyncio.run(ai_suggest_priority(title, desc))
        category = asyncio.run(ai_suggest_category(title, desc))
    except:
        # Fallback si IA falla
        priority = "medium"
        category = "personal"
    
    # Crear tarea normalmente
    task_data = {
        'title': title,
        'description': desc,
        'priority': priority,
        'categoria': category,
        'user_id': user_id,
        'status': 'pending'
    }
    
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    return jsonify({
        'task': response.data[0],
        'ai_priority': priority,
        'ai_category': category
    }), 201
```

### 5️⃣ Agregar saldo a OpenAI (IMPORTANTE)

```
1. Ve a: https://platform.openai.com/account/billing
2. Agrega $5-$10 de crédito
3. Ya puedes usar el sistema
```

---

## 📁 Archivos Importantes

| Archivo | Qué hace |
|---------|----------|
| `lib/agent.py` | Core del agente (no tocar) |
| `lib/agent_helpers.py` | Funciones para usar en controllers |
| `services/agent_service.py` | Funciones registradas del agente |
| `README_AGENTES.md` | Esta guía completa |
| `EXAMPLE_INTEGRATION.py` | Ejemplos de código |

---

## 🚀 Casos de Uso

### Auto-sugerir prioridad
```python
priority = asyncio.run(ai_suggest_priority(
    "URGENT: Fix bug", 
    "System is down"
))
# → "high"
```

### Auto-categorizar
```python
category = asyncio.run(ai_suggest_category(
    "Buy milk",
    "Get groceries"
))
# → "shopping"
```

### Análisis de productividad
```python
analysis = asyncio.run(ai_analyze_user(user_id=1))
# → {"analysis": "You complete most tasks in the morning..."}
```

---

## ⚠️ Importante

1. **NO** expongas los agentes como endpoints públicos
2. **SÍ** úsalos internamente en controllers
3. **SIEMPRE** ten fallbacks si IA falla
4. **LOGGEA** todo para debugging
5. **MONITOREA** costos de OpenAI

---

## 💰 Costos

- Request simple: ~$0.015
- 100 requests/día: ~$1.50/día
- **~$45/mes** uso moderado

---

## 📚 Más Info

- Documentación completa: `Documentation/AI_AGENT_SYSTEM.md`
- Guía de integración: `Documentation/AGENT_INTERNAL_USAGE.md`
- Ejemplos de código: `EXAMPLE_INTEGRATION.py`
- Resumen: `AGENT_IMPLEMENTATION_SUMMARY.md`

---

## ✅ Checklist

- [x] Sistema implementado
- [x] Documentación creada
- [x] Tests creados
- [x] Ejemplos listos
- [ ] Agregar saldo a OpenAI ⬅️ **TÚ DEBES HACER ESTO**
- [ ] Integrar en controllers ⬅️ **PRÓXIMO PASO**

---

## 🎉 ¡Listo!

El sistema está completamente implementado y listo para usar.

**Solo necesitas:**
1. Agregar saldo a OpenAI
2. Empezar a usar en tus controllers

**Archivo para empezar:** `controllers/task_controller.py`

**Función para usar:** `ai_suggest_priority()` o `ai_suggest_category()`

---

_Sistema creado: Octubre 4, 2025_  
_Estado: ✅ Completado - Listo para integración_
