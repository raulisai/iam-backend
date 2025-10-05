# Guía de Uso Interno de Agentes IA

## Overview
Los agentes IA están diseñados para ser utilizados **internamente** dentro de los controladores y servicios existentes, NO como endpoints públicos.

## Arquitectura

```
Endpoint Público → Controller → Agent Helper → AI Agent → OpenAI API
                       ↓                ↓
                   Supabase      Function Execution
```

## Archivos Principales

- **`lib/agent.py`** - Core del agente (AIAgent, FunctionRegistry, etc.)
- **`services/agent_service.py`** - Funciones registradas y lógica de negocio
- **`lib/agent_helpers.py`** - Funciones de ayuda para usar en controladores
- **`controllers/*_controller.py`** - Uso interno en endpoints existentes

## Casos de Uso

### 1. Auto-sugerir Prioridad de Tareas

Cuando un usuario crea una tarea, el agente analiza el título y descripción para sugerir la prioridad automáticamente.

**Implementación en `task_controller.py`:**

```python
from lib.agent_helpers import ai_suggest_priority
import asyncio

def create_new_task(data):
    """Create a new task with AI-suggested priority"""
    title = data.get('title')
    description = data.get('desc', '')
    priority = data.get('priority')
    
    # Si no se proporciona prioridad, usar IA
    if not priority:
        priority = asyncio.run(ai_suggest_priority(title, description))
    
    task_data = {
        'title': title,
        'description': description,
        'priority': priority,
        'status': 'pending'
    }
    
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    return jsonify({
        'task': response.data[0],
        'ai_suggested_priority': priority
    }), 201
```

### 2. Análisis de Productividad

Endpoint para obtener insights de productividad usando IA.

**Nuevo endpoint en `task_controller.py`:**

```python
from lib.agent_helpers import ai_analyze_user
import asyncio

def get_user_productivity_insights(user_id):
    """
    Get AI-powered productivity insights
    ---
    tags:
      - Tasks
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Productivity insights
    """
    try:
        analysis = asyncio.run(ai_analyze_user(user_id))
        
        return jsonify({
            'user_id': user_id,
            'insights': analysis.get('analysis', ''),
            'statistics': analysis.get('function_calls', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 3. Generación de Tareas desde Goals

Cuando se crea un goal, sugerir tareas automáticamente.

**En `goal_controller.py`:**

```python
from lib.agent_helpers import ai_generate_tasks_for_goal
import asyncio

def create_goal_with_tasks(data):
    """Create a goal and generate suggested tasks"""
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description', '')
    
    # Crear el goal
    supabase = get_supabase()
    goal_data = {
        'user_id': user_id,
        'title': title,
        'description': description,
        'status': 'active'
    }
    goal_response = supabase.table('goal').insert(goal_data).execute()
    goal = goal_response.data[0]
    
    # Generar tareas sugeridas con IA
    suggestions = asyncio.run(ai_generate_tasks_for_goal(user_id, title))
    
    return jsonify({
        'goal': goal,
        'suggested_tasks': suggestions.get('suggestions', ''),
        'message': 'Goal created! Here are some suggested tasks to get started.'
    }), 201
```

### 4. Actualización Inteligente de Tareas

Permitir actualizar tareas con lenguaje natural.

**En `task_controller.py`:**

```python
from lib.agent_helpers import get_agent_helper
import asyncio

def smart_update_task(task_id, data):
    """
    Update task using natural language
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            instruction:
              type: string
              example: "mark this as done"
            user_id:
              type: integer
    """
    instruction = data.get('instruction')
    user_id = data.get('user_id')
    
    if not instruction:
        return jsonify({'error': 'instruction is required'}), 400
    
    helper = get_agent_helper()
    result = asyncio.run(
        helper.smart_task_update(task_id, instruction, user_id)
    )
    
    return jsonify(result), 200
```

### 5. Validación Mejorada de Perfil

Validar y sugerir mejoras en perfiles de usuario.

**En `profile_controller.py`:**

```python
from lib.agent_helpers import get_agent_helper
import asyncio

def update_profile_with_validation(user_id, data):
    """Update profile with AI validation"""
    
    # Primero validar con IA
    helper = get_agent_helper()
    validation = asyncio.run(
        helper.validate_and_enhance_profile(data)
    )
    
    # Actualizar el perfil
    supabase = get_supabase()
    response = supabase.table('profile')\
        .update(data)\
        .eq('user_id', user_id)\
        .execute()
    
    return jsonify({
        'profile': response.data[0],
        'ai_suggestions': validation.get('suggestions', ''),
        'validation': validation
    }), 200
```

### 6. Categorización Automática

Auto-categorizar tareas basándose en su contenido.

**En `task_controller.py`:**

```python
from lib.agent_helpers import ai_suggest_category
import asyncio

def create_task_with_auto_category(data):
    """Create task with automatic categorization"""
    title = data.get('title')
    description = data.get('desc', '')
    category = data.get('categoria')
    
    # Si no hay categoría, usar IA
    if not category:
        category = asyncio.run(ai_suggest_category(title, description))
    
    task_data = {
        'title': title,
        'description': description,
        'categoria': category,
        'status': 'pending'
    }
    
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    return jsonify({
        'task': response.data[0],
        'ai_categorized': True,
        'category': category
    }), 201
```

## Funciones Disponibles

### En `lib/agent_helpers.py`:

| Función | Descripción | Uso |
|---------|-------------|-----|
| `ai_suggest_priority(title, desc)` | Sugerir prioridad de tarea | Creación de tareas |
| `ai_suggest_category(title, desc)` | Sugerir categoría | Organización |
| `ai_analyze_user(user_id)` | Analizar patrones del usuario | Analytics |
| `ai_generate_tasks_for_goal(user_id, goal)` | Generar tareas para un objetivo | Planificación |

### En `AgentHelper` class:

| Método | Descripción |
|--------|-------------|
| `analyze_task_priority()` | Análisis detallado de prioridad |
| `suggest_task_category()` | Sugerencia de categoría |
| `generate_task_suggestions()` | Generar lista de tareas |
| `analyze_task_completion_patterns()` | Análisis de patrones |
| `smart_task_update()` | Actualización con lenguaje natural |
| `generate_achievement_description()` | Descripción motivacional |
| `validate_and_enhance_profile()` | Validación de perfil |

## Ejemplo Completo: Endpoint Mejorado

```python
# controllers/task_controller.py

from flask import jsonify, request
from lib.db import get_supabase
from lib.agent_helpers import ai_suggest_priority, ai_suggest_category
import asyncio

def create_smart_task():
    """
    Create a task with AI enhancements
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        schema:
          properties:
            title:
              type: string
            description:
              type: string
            user_id:
              type: integer
            use_ai:
              type: boolean
              default: true
    responses:
      201:
        description: Task created with AI suggestions
    """
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    user_id = data.get('user_id')
    use_ai = data.get('use_ai', True)
    
    if not title or not user_id:
        return jsonify({'error': 'title and user_id required'}), 400
    
    # Construir datos de la tarea
    task_data = {
        'title': title,
        'description': description,
        'user_id': user_id,
        'status': 'pending'
    }
    
    ai_enhancements = {}
    
    # Usar IA si está habilitado
    if use_ai:
        try:
            # Sugerir prioridad y categoría en paralelo
            priority = asyncio.run(ai_suggest_priority(title, description))
            category = asyncio.run(ai_suggest_category(title, description))
            
            task_data['priority'] = priority
            task_data['categoria'] = category
            
            ai_enhancements = {
                'ai_suggested_priority': priority,
                'ai_suggested_category': category,
                'ai_used': True
            }
        except Exception as e:
            # Si falla la IA, continuar sin ella
            ai_enhancements = {
                'ai_used': False,
                'ai_error': str(e)
            }
    
    # Crear en la base de datos
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    return jsonify({
        'task': response.data[0],
        **ai_enhancements
    }), 201
```

## Consideraciones Importantes

### 1. Manejo de Async
Como Flask no es nativo async, usamos `asyncio.run()`:

```python
import asyncio

result = asyncio.run(ai_suggest_priority(title, desc))
```

### 2. Error Handling
Siempre manejar errores de IA con fallback:

```python
try:
    priority = asyncio.run(ai_suggest_priority(title, desc))
except Exception as e:
    logger.error(f"AI failed: {e}")
    priority = "medium"  # Fallback
```

### 3. Performance
- La IA agrega latencia (~1-3 segundos)
- Hacer opcional con flags `use_ai`
- Considerar hacer async en background para requests largos

### 4. Costos
- Cada llamada consume tokens
- Monitorear uso con `agent.get_stats()`
- Implementar rate limiting si es necesario

## Testing

```python
# test_agent_helpers.py

import asyncio
from lib.agent_helpers import ai_suggest_priority, ai_suggest_category

def test_priority_suggestion():
    result = asyncio.run(
        ai_suggest_priority(
            "URGENT: Fix critical bug in production",
            "System is down, users can't login"
        )
    )
    assert result in ["low", "medium", "high"]
    print(f"Suggested priority: {result}")

def test_category_suggestion():
    result = asyncio.run(
        ai_suggest_category(
            "Buy groceries",
            "Milk, eggs, bread"
        )
    )
    print(f"Suggested category: {result}")

if __name__ == "__main__":
    test_priority_suggestion()
    test_category_suggestion()
```

## Roadmap de Integración

1. ✅ **Fase 1**: Core agent library creada
2. ✅ **Fase 2**: Agent helpers y funciones de utilidad
3. 🔄 **Fase 3**: Integrar en endpoints de tasks (próximo)
4. 📋 **Fase 4**: Integrar en goals y achievements
5. 📋 **Fase 5**: Analytics avanzados con IA
6. 📋 **Fase 6**: MCP integration

## Recursos

- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- Async in Flask: https://flask.palletsprojects.com/en/2.3.x/async-await/
- Agent Documentation: `Documentation/AI_AGENT_SYSTEM.md`
