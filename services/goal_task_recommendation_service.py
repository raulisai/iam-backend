"""Goal Task Recommendation Service - AI-powered task recommendations for goals."""
import logging
import asyncio
import json
import re
from datetime import datetime
from services.goal_service import get_goal_by_id
from services.goal_task_service import get_goal_tasks
from services.task_template_service import get_all_task_templates

# Configure logging
logger = logging.getLogger(__name__)


def get_goal_context(goal_id, user_id):
    """Get comprehensive goal context for AI analysis.
    
    Args:
        goal_id (str): Goal ID.
        user_id (str): User ID.
    
    Returns:
        dict: Goal context including goal data and existing tasks.
    """
    # Get goal details
    goal = get_goal_by_id(goal_id)
    if not goal or goal.get('user_id') != user_id:
        return None
    
    # Get existing tasks for this goal
    existing_tasks = get_goal_tasks(goal_id, user_id)
    
    return {
        'goal': goal,
        'existing_tasks': existing_tasks,
        'task_count': len(existing_tasks)
    }


def format_goal_for_ai(goal_context):
    """Format goal context for AI prompt.
    
    Args:
        goal_context (dict): Goal context data.
    
    Returns:
        str: Formatted goal information.
    """
    goal = goal_context['goal']
    existing_tasks = goal_context['existing_tasks']
    
    formatted = f"""
OBJETIVO DEL USUARIO:
- Título: {goal.get('title', 'Sin título')}
- Descripción: {goal.get('description', 'Sin descripción')}
- Fecha objetivo: {goal.get('target_date', 'No definida')}
- Estado: {'Activo' if goal.get('is_active') else 'Inactivo'}
- Categoría: {goal.get('category', 'General')}

TAREAS EXISTENTES ({len(existing_tasks)}):
"""
    
    if existing_tasks:
        for i, task in enumerate(existing_tasks[:10], 1):
            status = '✓' if task.get('is_completed') else '○'
            formatted += f"{i}. {status} {task.get('title', 'Sin título')} - {task.get('description', '')[:50]}\n"
    else:
        formatted += "No hay tareas aún para este objetivo.\n"
    
    return formatted


def format_templates_for_goal(templates):
    """Format available templates for AI context.
    
    Args:
        templates (list): Available task templates.
    
    Returns:
        str: Formatted template information.
    """
    if not templates:
        return "No hay templates disponibles."
    
    formatted = "TEMPLATES DISPONIBLES:\n"
    for template in templates:
        formatted += f"- [{template['id']}] {template['name']} ({template.get('category', 'general')})\n"
        formatted += f"  Descripción: {template.get('desc', 'Sin descripción')[:80]}\n"
    
    return formatted


def parse_ai_task_recommendations(response):
    """Parse AI response to extract task recommendations.
    
    Args:
        response (str): AI response text.
    
    Returns:
        list: List of task recommendation objects.
    """
    recommendations = []
    
    try:
        # Try to find JSON array in response
        json_match = re.search(r'\[[\s\S]*?\]', response, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            
            # Validate structure
            for item in parsed:
                if isinstance(item, dict) and 'title' in item:
                    recommendations.append({
                        'title': item.get('title', ''),
                        'description': item.get('description', ''),
                        'priority': item.get('priority', 'medium'),
                        'estimated_duration': item.get('estimated_duration'),
                        'template_id': item.get('template_id'),
                        'order': item.get('order', len(recommendations) + 1),
                        'reason': item.get('reason', '')
                    })
            
            if recommendations:
                return recommendations
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning("Failed to parse JSON recommendations: %s", str(e))
    
    # Fallback: Try to extract structured information from text
    lines = response.split('\n')
    current_task = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Look for task titles (numbered or bulleted lists)
        title_match = re.match(r'^[\d]+[\.\)]\s*(.+)$|^[-*]\s*(.+)$', line)
        if title_match:
            # Save previous task
            if current_task and current_task.get('title'):
                recommendations.append(current_task)
            
            # Start new task
            title = title_match.group(1) or title_match.group(2)
            current_task = {
                'title': title.strip(),
                'description': '',
                'priority': 'medium',
                'estimated_duration': None,
                'template_id': None,
                'order': len(recommendations) + 1,
                'reason': ''
            }
        elif current_task:
            # Add to description
            if line.lower().startswith('descripción:') or line.lower().startswith('description:'):
                current_task['description'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('prioridad:') or line.lower().startswith('priority:'):
                priority = line.split(':', 1)[1].strip().lower()
                if priority in ['low', 'medium', 'high', 'baja', 'media', 'alta']:
                    current_task['priority'] = priority
            elif line.lower().startswith('duración:') or line.lower().startswith('duration:'):
                duration_text = line.split(':', 1)[1].strip()
                current_task['estimated_duration'] = duration_text
            else:
                # Add to description if not empty
                if current_task['description']:
                    current_task['description'] += ' ' + line
                else:
                    current_task['description'] = line
    
    # Add last task
    if current_task and current_task.get('title'):
        recommendations.append(current_task)
    
    return recommendations


async def generate_goal_task_recommendations_with_ai(goal_id, user_id, count=5, additional_context=None):
    """Generate task recommendations for a goal using AI.
    
    Args:
        goal_id (str): Goal ID.
        user_id (str): User ID.
        count (int): Number of recommendations to generate (default 5).
        additional_context (dict, optional): Additional context from user.
    
    Returns:
        dict: Recommendations with metadata.
    """
    try:
        from services.agent_service import get_agent_service
        
        # Get goal context
        goal_context = get_goal_context(goal_id, user_id)
        if not goal_context:
            return {
                'success': False,
                'error': 'Goal not found or unauthorized'
            }
        
        # Get available templates
        templates = get_all_task_templates()
        
        # Build AI prompt
        prompt = f"""
Eres un asistente experto en planificación y logro de objetivos. Tu tarea es analizar el objetivo del usuario y recomendar tareas específicas y accionables que le ayuden a lograrlo.

{format_goal_for_ai(goal_context)}

{format_templates_for_goal(templates) if templates else ''}

CONTEXTO ADICIONAL:
{json.dumps(additional_context, indent=2) if additional_context else 'Ninguno proporcionado'}

INSTRUCCIONES:
1. Analiza el objetivo y las tareas existentes
2. Identifica qué pasos faltan o qué tareas complementarias serían útiles
3. Recomienda {count} tareas específicas, accionables y relevantes
4. Para cada tarea incluye:
   - Título claro y específico
   - Descripción detallada
   - Prioridad (low, medium, high)
   - Duración estimada (si aplica)
   - Template ID si existe uno apropiado
   - Razón por la que esta tarea es importante

IMPORTANTE: Devuelve tu respuesta como un JSON array con esta estructura:
[
  {{
    "title": "Título de la tarea",
    "description": "Descripción detallada de lo que debe hacerse",
    "priority": "high|medium|low",
    "estimated_duration": "30 minutos" o null,
    "template_id": "uuid del template" o null,
    "order": 1,
    "reason": "Por qué esta tarea es importante para el objetivo"
  }}
]

Enfócate en tareas prácticas, específicas y que realmente impulsen el progreso hacia el objetivo.
"""
        
        # Get agent service
        agent_service = get_agent_service()
        
        # Generate recommendations
        result = await agent_service.agent.ask(
            prompt,
            conversation_id=f"goal_recommendations_{goal_id}_{user_id}",
            user_context={
                "user_id": user_id,
                "goal_id": goal_id,
                "type": "goal_task_recommendations"
            }
        )
        
        if not result.get("success"):
            return {
                'success': False,
                'error': 'AI generation failed',
                'details': result.get('error')
            }
        
        # Parse AI response
        ai_response = result.get('response', '')
        recommendations = parse_ai_task_recommendations(ai_response)
        
        if not recommendations:
            return {
                'success': False,
                'error': 'Failed to parse AI recommendations',
                'raw_response': ai_response
            }
        
        # Ensure we have the requested count (or less if AI provided fewer)
        recommendations = recommendations[:count]
        
        return {
            'success': True,
            'goal': {
                'id': goal_context['goal']['id'],
                'title': goal_context['goal'].get('title'),
                'description': goal_context['goal'].get('description')
            },
            'recommendations': recommendations,
            'method': 'ai_powered',
            'generated_at': datetime.utcnow().isoformat(),
            'existing_task_count': goal_context['task_count'],
            'ai_metadata': {
                'tokens_used': result.get('metadata', {}).get('tokens_used', 0),
                'model': result.get('metadata', {}).get('model', 'unknown')
            }
        }
        
    except ImportError:
        return {
            'success': False,
            'error': 'AI agent service not available'
        }
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Error generating AI goal recommendations: %s", str(e))
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def generate_goal_task_recommendations_simple(goal_id, user_id, count=5):
    """Generate simple task recommendations without AI.
    
    Args:
        goal_id (str): Goal ID.
        user_id (str): User ID.
        count (int): Number of recommendations to generate.
    
    Returns:
        dict: Basic recommendations.
    """
    goal_context = get_goal_context(goal_id, user_id)
    if not goal_context:
        return {
            'success': False,
            'error': 'Goal not found or unauthorized'
        }
    
    goal = goal_context['goal']
    existing_tasks = goal_context['existing_tasks']
    
    # Generate basic recommendations based on common patterns
    recommendations = []
    
    # Default task suggestions
    if len(existing_tasks) == 0:
        recommendations.append({
            'title': 'Definir plan de acción inicial',
            'description': f'Crear un plan detallado de pasos necesarios para lograr: {goal.get("title")}',
            'priority': 'high',
            'estimated_duration': '30 minutos',
            'template_id': None,
            'order': 1,
            'reason': 'Primera tarea esencial para estructurar el camino hacia el objetivo'
        })
        
        recommendations.append({
            'title': 'Investigar recursos necesarios',
            'description': 'Identificar y listar todos los recursos, herramientas o conocimientos necesarios',
            'priority': 'high',
            'estimated_duration': '45 minutos',
            'template_id': None,
            'order': 2,
            'reason': 'Conocer qué necesitas antes de empezar acelera el progreso'
        })
    
    recommendations.append({
        'title': 'Revisión de progreso semanal',
        'description': f'Evaluar avances hacia: {goal.get("title")} y ajustar plan si es necesario',
        'priority': 'medium',
        'estimated_duration': '20 minutos',
        'template_id': None,
        'order': len(recommendations) + 1,
        'reason': 'Mantener seguimiento regular asegura que vas por buen camino'
    })
    
    recommendations.append({
        'title': 'Siguiente paso concreto',
        'description': 'Identificar y completar la siguiente acción específica hacia el objetivo',
        'priority': 'high',
        'estimated_duration': None,
        'template_id': None,
        'order': len(recommendations) + 1,
        'reason': 'Mantener momentum con acciones constantes'
    })
    
    recommendations.append({
        'title': 'Celebrar hitos alcanzados',
        'description': 'Reconocer y celebrar los logros parciales conseguidos hasta ahora',
        'priority': 'low',
        'estimated_duration': '10 minutos',
        'template_id': None,
        'order': len(recommendations) + 1,
        'reason': 'La motivación es clave para mantener el esfuerzo a largo plazo'
    })
    
    return {
        'success': True,
        'goal': {
            'id': goal['id'],
            'title': goal.get('title'),
            'description': goal.get('description')
        },
        'recommendations': recommendations[:count],
        'method': 'pattern_based',
        'generated_at': datetime.utcnow().isoformat(),
        'existing_task_count': len(existing_tasks)
    }


def generate_goal_task_recommendations(goal_id, user_id, count=5, use_ai=True, additional_context=None):
    """Generate task recommendations for a goal.
    
    Args:
        goal_id (str): Goal ID.
        user_id (str): User ID.
        count (int): Number of recommendations (1-10, default 5).
        use_ai (bool): Whether to use AI for recommendations (default True).
        additional_context (dict, optional): Additional context for AI.
    
    Returns:
        dict: Task recommendations with metadata.
    """
    # Validate count
    count = max(1, min(count, 10))
    
    if use_ai:
        # Use asyncio to run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                generate_goal_task_recommendations_with_ai(goal_id, user_id, count, additional_context)
            )
            return result
        finally:
            loop.close()
    else:
        return generate_goal_task_recommendations_simple(goal_id, user_id, count)
