"""
EJEMPLO DE INTEGRACIÓN: Cómo agregar IA a un endpoint existente
Este archivo muestra cómo modificar un controlador para usar los agentes IA
"""

# ============================================================================
# ANTES: Controller sin IA
# ============================================================================

def create_task_before(data):
    """Versión original sin IA"""
    title = data.get('title')
    description = data.get('desc', '')
    priority = data.get('priority', 'medium')  # Valor por defecto manual
    category = data.get('categoria', 'personal')  # Valor por defecto manual
    user_id = data.get('user_id')
    
    task_data = {
        'title': title,
        'description': description,
        'priority': priority,
        'categoria': category,
        'user_id': user_id,
        'status': 'pending'
    }
    
    # Guardar en DB
    from lib.db import get_supabase
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    from flask import jsonify
    return jsonify({'task': response.data[0]}), 201


# ============================================================================
# DESPUÉS: Controller con IA (OPCIÓN 1 - Básico)
# ============================================================================

def create_task_with_ai_basic(data):
    """Versión mejorada con IA - básica"""
    from lib.agent_helpers import ai_suggest_priority, ai_suggest_category
    import asyncio
    from flask import jsonify
    from lib.db import get_supabase
    
    title = data.get('title')
    description = data.get('desc', '')
    user_id = data.get('user_id')
    
    # Si el usuario NO especificó prioridad, usar IA
    priority = data.get('priority')
    if not priority:
        priority = asyncio.run(ai_suggest_priority(title, description))
    
    # Si el usuario NO especificó categoría, usar IA
    category = data.get('categoria')
    if not category:
        category = asyncio.run(ai_suggest_category(title, description))
    
    task_data = {
        'title': title,
        'description': description,
        'priority': priority,
        'categoria': category,
        'user_id': user_id,
        'status': 'pending'
    }
    
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    return jsonify({
        'task': response.data[0],
        'ai_suggested_priority': priority,
        'ai_suggested_category': category
    }), 201


# ============================================================================
# DESPUÉS: Controller con IA (OPCIÓN 2 - Robusto con fallbacks)
# ============================================================================

def create_task_with_ai_robust(data):
    """Versión mejorada con IA - robusta con manejo de errores"""
    from lib.agent_helpers import ai_suggest_priority, ai_suggest_category
    import asyncio
    import logging
    from flask import jsonify
    from lib.db import get_supabase
    
    logger = logging.getLogger(__name__)
    
    title = data.get('title')
    description = data.get('desc', '')
    user_id = data.get('user_id')
    use_ai = data.get('use_ai', True)  # Flag para habilitar/deshabilitar IA
    
    ai_metadata = {
        'ai_used': False,
        'ai_suggested_priority': None,
        'ai_suggested_category': None,
        'ai_errors': []
    }
    
    # Prioridad
    priority = data.get('priority')
    if not priority and use_ai:
        try:
            priority = asyncio.run(ai_suggest_priority(title, description))
            ai_metadata['ai_used'] = True
            ai_metadata['ai_suggested_priority'] = priority
            logger.info(f"AI suggested priority: {priority} for task: {title}")
        except Exception as e:
            logger.warning(f"AI priority suggestion failed: {str(e)}")
            priority = 'medium'  # Fallback
            ai_metadata['ai_errors'].append(f"priority: {str(e)}")
    elif not priority:
        priority = 'medium'  # Fallback sin IA
    
    # Categoría
    category = data.get('categoria')
    if not category and use_ai:
        try:
            category = asyncio.run(ai_suggest_category(title, description))
            ai_metadata['ai_used'] = True
            ai_metadata['ai_suggested_category'] = category
            logger.info(f"AI suggested category: {category} for task: {title}")
        except Exception as e:
            logger.warning(f"AI category suggestion failed: {str(e)}")
            category = 'personal'  # Fallback
            ai_metadata['ai_errors'].append(f"category: {str(e)}")
    elif not category:
        category = 'personal'  # Fallback sin IA
    
    # Crear tarea
    task_data = {
        'title': title,
        'description': description,
        'priority': priority,
        'categoria': category,
        'user_id': user_id,
        'status': 'pending'
    }
    
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    # Respuesta con metadata de IA
    return jsonify({
        'task': response.data[0],
        'ai_metadata': ai_metadata
    }), 201


# ============================================================================
# DESPUÉS: Controller con IA (OPCIÓN 3 - Análisis completo)
# ============================================================================

def create_task_with_ai_full_analysis(data):
    """Versión con análisis completo usando el agente directamente"""
    from lib.agent_helpers import get_agent_helper
    import asyncio
    from flask import jsonify
    from lib.db import get_supabase
    
    title = data.get('title')
    description = data.get('desc', '')
    user_id = data.get('user_id')
    
    # Usar el AgentHelper para análisis más completo
    helper = get_agent_helper()
    
    # Análisis en paralelo (más rápido)
    priority, category = asyncio.run(
        asyncio.gather(
            helper.analyze_task_priority(title, description),
            helper.suggest_task_category(title, description)
        )
    )
    
    task_data = {
        'title': title,
        'description': description,
        'priority': priority,
        'categoria': category,
        'user_id': user_id,
        'status': 'pending'
    }
    
    supabase = get_supabase()
    response = supabase.table('task').insert(task_data).execute()
    
    return jsonify({
        'task': response.data[0],
        'ai_analysis': {
            'priority': priority,
            'category': category,
            'analysis_time': 'concurrent'
        }
    }), 201


# ============================================================================
# NUEVO ENDPOINT: Analytics con IA
# ============================================================================

def get_user_productivity_insights(user_id):
    """
    Nuevo endpoint que usa IA para dar insights de productividad
    GET /tasks/insights/<user_id>
    """
    from lib.agent_helpers import ai_analyze_user
    import asyncio
    from flask import jsonify
    
    try:
        # El agente analizará automáticamente las tareas del usuario
        analysis = asyncio.run(ai_analyze_user(user_id))
        
        return jsonify({
            'user_id': user_id,
            'insights': analysis.get('analysis', ''),
            'success': analysis.get('success', False),
            'function_calls': len(analysis.get('function_calls', []))
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'user_id': user_id
        }), 500


# ============================================================================
# NUEVO ENDPOINT: Actualización inteligente con lenguaje natural
# ============================================================================

def smart_update_task(task_id):
    """
    Actualizar tarea con lenguaje natural
    POST /tasks/<task_id>/smart-update
    Body: { "instruction": "mark as done", "user_id": 1 }
    """
    from lib.agent_helpers import get_agent_helper
    from flask import request, jsonify
    import asyncio
    
    data = request.json
    instruction = data.get('instruction')
    user_id = data.get('user_id')
    
    if not instruction or not user_id:
        return jsonify({
            'error': 'instruction and user_id required'
        }), 400
    
    try:
        helper = get_agent_helper()
        result = asyncio.run(
            helper.smart_task_update(task_id, instruction, user_id)
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# EJEMPLO DE RUTAS
# ============================================================================

"""
# En task_routes.py, agregar:

from controllers.task_controller import (
    create_task_with_ai_robust,
    get_user_productivity_insights,
    smart_update_task
)

# Endpoint existente mejorado con IA
task_routes.route('/tasks', methods=['POST'])(create_task_with_ai_robust)

# Nuevos endpoints con IA
task_routes.route('/tasks/insights/<int:user_id>', methods=['GET'])(
    get_user_productivity_insights
)

task_routes.route('/tasks/<int:task_id>/smart-update', methods=['POST'])(
    smart_update_task
)
"""


# ============================================================================
# EJEMPLO DE USO DESDE EL FRONTEND
# ============================================================================

"""
// JavaScript - Crear tarea con IA

// Opción 1: Dejar que la IA sugiera (usuario no especifica nada)
fetch('/tasks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Fix critical bug in production',
    desc: 'Users cannot login',
    user_id: 1,
    use_ai: true  // Habilitar IA
  })
})
.then(res => res.json())
.then(data => {
  console.log('Task created:', data.task);
  console.log('AI suggested priority:', data.ai_metadata.ai_suggested_priority);
  console.log('AI suggested category:', data.ai_metadata.ai_suggested_category);
});

// Opción 2: Usuario especifica, IA NO se usa
fetch('/tasks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Buy milk',
    desc: 'Get milk from store',
    priority: 'low',  // Usuario especifica
    categoria: 'shopping',  // Usuario especifica
    user_id: 1,
    use_ai: false  // Deshabilitar IA
  })
})

// Opción 3: Obtener insights de productividad
fetch('/tasks/insights/1')
  .then(res => res.json())
  .then(data => {
    console.log('Productivity insights:', data.insights);
  });

// Opción 4: Actualización con lenguaje natural
fetch('/tasks/5/smart-update', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    instruction: 'mark this as completed',
    user_id: 1
  })
})
.then(res => res.json())
.then(data => {
  console.log('Task updated:', data);
});
"""


# ============================================================================
# COMPARACIÓN DE OPCIONES
# ============================================================================

"""
OPCIÓN 1 - BÁSICO:
Pros:
  - Simple de implementar
  - Código mínimo
  - Usa IA directamente
Cons:
  - No maneja errores de IA
  - Puede fallar si API está caída

OPCIÓN 2 - ROBUSTO (RECOMENDADO):
Pros:
  - Manejo completo de errores
  - Fallbacks automáticos
  - Flag para habilitar/deshabilitar IA
  - Logs detallados
  - Metadata de IA en respuesta
Cons:
  - Más código
  - Un poco más complejo

OPCIÓN 3 - ANÁLISIS COMPLETO:
Pros:
  - Usa AgentHelper directamente
  - Análisis en paralelo (más rápido)
  - Más control sobre el agente
Cons:
  - Requiere entender AgentHelper
  - Un poco más complejo

RECOMENDACIÓN: Empezar con OPCIÓN 2 (Robusto) para producción
"""


# ============================================================================
# TESTING
# ============================================================================

"""
# Test manual con curl:

# 1. Crear tarea con IA
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "URGENT: Fix critical security issue",
    "desc": "SQL injection vulnerability found",
    "user_id": 1,
    "use_ai": true
  }'

# 2. Crear tarea sin IA
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "desc": "Milk, eggs, bread",
    "priority": "low",
    "categoria": "shopping",
    "user_id": 1,
    "use_ai": false
  }'

# 3. Obtener insights
curl http://localhost:5000/tasks/insights/1

# 4. Actualización inteligente
curl -X POST http://localhost:5000/tasks/5/smart-update \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "mark as completed",
    "user_id": 1
  }'
"""


# ============================================================================
# MEJORES PRÁCTICAS
# ============================================================================

"""
1. SIEMPRE tener fallbacks cuando uses IA
2. LOGGEAR todo lo que hace la IA (para debugging)
3. Hacer la IA OPCIONAL (flag use_ai)
4. VALIDAR inputs antes de pasar a la IA
5. MANEJAR errores de API de OpenAI
6. MONITOREAR uso de tokens (costos)
7. Implementar RATE LIMITING para llamadas de IA
8. No incluir datos SENSIBLES en prompts
9. Usar ASYNC para no bloquear el servidor
10. TESTEAR con y sin IA
"""
