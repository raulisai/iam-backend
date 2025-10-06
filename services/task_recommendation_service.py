"""Task recommendation service for generating task recommendations."""
import logging
import random
from datetime import datetime, timedelta
from services.mind_task_service import get_user_mind_tasks
from services.body_task_service import get_user_body_tasks
from services.task_template_service import get_templates_by_category

# Configure logging
logger = logging.getLogger(__name__)


def get_recent_tasks(user_id, limit=10):
    """Get recent tasks from both mind and body categories.
    
    Args:
        user_id (str): User ID.
        limit (int): Number of recent tasks to fetch.
    
    Returns:
        dict: Recent tasks grouped by category.
    """
    mind_tasks = get_user_mind_tasks(user_id)[:limit]
    body_tasks = get_user_body_tasks(user_id)[:limit]
    
    return {
        'mind': mind_tasks,
        'body': body_tasks,
        'total_count': len(mind_tasks) + len(body_tasks)
    }


def analyze_task_patterns(recent_tasks):
    """Analyze patterns in recent tasks.
    
    Args:
        recent_tasks (dict): Recent tasks data.
    
    Returns:
        dict: Analysis of task patterns.
    """
    analysis = {
        'mind_count': len(recent_tasks['mind']),
        'body_count': len(recent_tasks['body']),
        'completed_mind': len([t for t in recent_tasks['mind'] if t.get('status') == 'completed']),
        'completed_body': len([t for t in recent_tasks['body'] if t.get('status') == 'completed']),
        'recent_template_ids': []
    }
    
    # Get recently used template IDs
    for task in recent_tasks['mind'] + recent_tasks['body']:
        template_id = task.get('template_id')
        if template_id and template_id not in analysis['recent_template_ids']:
            analysis['recent_template_ids'].append(template_id)
    
    # Determine which category needs more attention
    if analysis['mind_count'] > analysis['body_count'] * 1.5:
        analysis['needs_balance'] = 'body'
    elif analysis['body_count'] > analysis['mind_count'] * 1.5:
        analysis['needs_balance'] = 'mind'
    else:
        analysis['needs_balance'] = None
    
    return analysis


def select_templates_by_pattern(templates, analysis, count=3):
    """Select templates based on usage patterns.
    
    Args:
        templates (list): Available templates.
        analysis (dict): Task pattern analysis.
        count (int): Number of templates to select.
    
    Returns:
        list: Selected templates.
    """
    # Filter out recently used templates
    available = [t for t in templates if t['id'] not in analysis['recent_template_ids']]
    
    # If not enough unique templates, include some recent ones
    if len(available) < count:
        available = templates
    
    # Randomly select from available templates
    selected = random.sample(available, min(count, len(available)))
    
    return selected


def generate_recommendations_simple(user_id):
    """Generate task recommendations using simple logic (no AI).
    
    Args:
        user_id (str): User ID.
    
    Returns:
        list: List of 3 recommended task templates with scheduling.
    """
    # Get recent tasks
    recent_tasks = get_recent_tasks(user_id)
    
    # Analyze patterns
    analysis = analyze_task_patterns(recent_tasks)
    
    recommendations = []
    
    # Decide distribution based on balance needs
    if analysis['needs_balance'] == 'body':
        # Recommend 2 body, 1 mind
        mind_templates = get_templates_by_category('mind')
        body_templates = get_templates_by_category('body')
        
        mind_selected = select_templates_by_pattern(mind_templates, analysis, 1)
        body_selected = select_templates_by_pattern(body_templates, analysis, 2)
        
        recommendations.extend(mind_selected)
        recommendations.extend(body_selected)
    elif analysis['needs_balance'] == 'mind':
        # Recommend 2 mind, 1 body
        mind_templates = get_templates_by_category('mind')
        body_templates = get_templates_by_category('body')
        
        mind_selected = select_templates_by_pattern(mind_templates, analysis, 2)
        body_selected = select_templates_by_pattern(body_templates, analysis, 1)
        
        recommendations.extend(mind_selected)
        recommendations.extend(body_selected)
    else:
        # Balanced approach - mix of both
        mind_templates = get_templates_by_category('mind')
        body_templates = get_templates_by_category('body')
        
        # Alternate or mix
        all_templates = mind_templates + body_templates
        selected = select_templates_by_pattern(all_templates, analysis, 3)
        recommendations.extend(selected)
    
    # Add suggested scheduling times (next 24 hours)
    base_time = datetime.utcnow()
    for i, template in enumerate(recommendations):
        template['suggested_schedule'] = (base_time + timedelta(hours=4 * (i + 1))).isoformat()
        template['reason'] = _get_recommendation_reason(template, analysis)
    
    return recommendations[:3]  # Ensure we return exactly 3


def _get_recommendation_reason(template, analysis):
    """Generate a reason for the recommendation.
    
    Args:
        template (dict): Template data.
        analysis (dict): Task pattern analysis.
    
    Returns:
        str: Reason for recommendation.
    """
    category = template.get('category', '')
    
    if analysis['needs_balance'] == category:
        return f"Recomendado para balancear tus tareas de {category}"
    elif template['id'] not in analysis['recent_template_ids']:
        return "Nuevo desafío para expandir tu rutina"
    else:
        return f"Tarea de {category} para continuar tu progreso"


def generate_recommendations_with_ai(user_id):
    """Generate task recommendations using AI agent.
    
    Args:
        user_id (str): User ID.
    
    Returns:
        list: List of 3 recommended task templates with AI-generated insights.
    """
    try:
        import asyncio
        from services.agent_service import get_agent_service
        
        # Get recent tasks and templates
        recent_tasks = get_recent_tasks(user_id, limit=15)
        mind_templates = get_templates_by_category('mind')
        body_templates = get_templates_by_category('body')
        all_templates = mind_templates + body_templates
        
        # Prepare context for AI
        context = f"""
Analiza el historial de tareas del usuario y recomienda 3 tareas específicas.

Tareas recientes de mente ({len(recent_tasks['mind'])}):
{_format_tasks_for_ai(recent_tasks['mind'][:5])}

Tareas recientes de cuerpo ({len(recent_tasks['body'])}):
{_format_tasks_for_ai(recent_tasks['body'][:5])}

Templates disponibles:
{_format_templates_for_ai(all_templates)}

Considera:
1. Balance entre tareas de mente y cuerpo
2. Variedad (evita repetir las mismas tareas)
3. Progresión gradual en dificultad

Devuelve SOLO un JSON array con 3 template_ids en orden de prioridad.
Ejemplo: ["uuid1", "uuid2", "uuid3"]
        """
        
        # Get agent service and generate response
        agent_service = get_agent_service()
        result = asyncio.run(
            agent_service.agent.ask(
                context,
                conversation_id=f"recommendation_{user_id}",
                user_context={"user_id": user_id}
            )
        )
        
        if result.get("success"):
            response = result.get('response', '')
        else:
            logger.warning("AI request failed, falling back to simple logic")
            return generate_recommendations_simple(user_id)
        
        # Parse AI response
        recommended_ids = _parse_ai_recommendations(response, all_templates)
        
        # Build recommendations with selected templates
        recommendations = []
        base_time = datetime.utcnow()
        
        for i, template_id in enumerate(recommended_ids[:3]):
            template = next((t for t in all_templates if t['id'] == template_id), None)
            if template:
                template['suggested_schedule'] = (base_time + timedelta(hours=4 * (i + 1))).isoformat()
                template['reason'] = "Recomendado por IA basado en tu historial y balance"
                recommendations.append(template)
        
        # If AI didn't provide enough, fall back to simple logic
        if len(recommendations) < 3:
            logger.warning("AI recommendations insufficient, using simple logic")
            return generate_recommendations_simple(user_id)
        
        return recommendations
        
    except (ValueError, KeyError, TypeError, ImportError) as e:
        logger.error("Error generating AI recommendations: %s", str(e))
        # Fall back to simple recommendations
        return generate_recommendations_simple(user_id)


def _format_tasks_for_ai(tasks):
    """Format tasks for AI context.
    
    Args:
        tasks (list): List of tasks.
    
    Returns:
        str: Formatted task summary.
    """
    if not tasks:
        return "Ninguna"
    
    formatted = []
    for task in tasks:
        template = task.get('task_templates', {})
        status = task.get('status', 'unknown')
        formatted.append(f"- {template.get('name', 'Unknown')} ({status})")
    
    return "\n".join(formatted)


def _format_templates_for_ai(templates):
    """Format templates for AI context.
    
    Args:
        templates (list): List of templates.
    
    Returns:
        str: Formatted template summary.
    """
    formatted = []
    for template in templates:
        formatted.append(
            f"- [{template['id']}] {template['name']} ({template['category']}) - {template.get('desc', '')}"
        )
    
    return "\n".join(formatted)


def _parse_ai_recommendations(response, all_templates):
    """Parse AI response to extract template IDs.
    
    Args:
        response (str): AI response text.
        all_templates (list): All available templates.
    
    Returns:
        list: List of template IDs.
    """
    import json
    import re
    
    try:
        # Try to find JSON array in response
        json_match = re.search(r'\[[\s\S]*?\]', response)
        if json_match:
            template_ids = json.loads(json_match.group())
            # Validate IDs exist
            valid_ids = [tid for tid in template_ids if any(t['id'] == tid for t in all_templates)]
            return valid_ids
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Fallback: try to find UUIDs in text
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    found_ids = re.findall(uuid_pattern, response, re.IGNORECASE)
    valid_ids = [tid for tid in found_ids if any(t['id'] == tid for t in all_templates)]
    
    return valid_ids


def generate_task_recommendations(user_id, use_ai=False):
    """Generate task recommendations for a user.
    
    Args:
        user_id (str): User ID.
        use_ai (bool): Whether to use AI for recommendations.
    
    Returns:
        dict: Recommendations with metadata.
    """
    recent_tasks = get_recent_tasks(user_id)
    
    # Decide if AI is needed
    # Use simple logic if user has few tasks or AI is not requested
    if not use_ai or recent_tasks['total_count'] < 3:
        recommendations = generate_recommendations_simple(user_id)
        method = 'pattern_based'
    else:
        recommendations = generate_recommendations_with_ai(user_id)
        method = 'ai_powered'
    
    return {
        'recommendations': recommendations,
        'method': method,
        'generated_at': datetime.utcnow().isoformat(),
        'task_history_count': recent_tasks['total_count']
    }


def generate_mind_task_recommendations(user_id, use_ai=False, count=3):
    """Generate mind task recommendations for a user.
    
    Args:
        user_id (str): User ID.
        use_ai (bool): Whether to use AI for recommendations.
        count (int): Number of recommendations to generate.
    
    Returns:
        dict: Mind task recommendations with metadata.
    """
    recent_tasks = get_recent_tasks(user_id)
    mind_templates = get_templates_by_category('mind')
    
    if not mind_templates:
        return {
            'recommendations': [],
            'method': 'no_templates',
            'generated_at': datetime.utcnow().isoformat(),
            'task_history_count': recent_tasks['total_count'],
            'category': 'mind'
        }
    
    # Analyze patterns
    analysis = analyze_task_patterns(recent_tasks)
    
    # Select templates
    selected = select_templates_by_pattern(mind_templates, analysis, count)
    
    # Add scheduling and reasons
    recommendations = []
    base_time = datetime.utcnow()
    
    for i, template in enumerate(selected):
        template['suggested_schedule'] = (base_time + timedelta(hours=4 * (i + 1))).isoformat()
        template['reason'] = _get_recommendation_reason(template, analysis)
        recommendations.append(template)
    
    return {
        'recommendations': recommendations,
        'method': 'pattern_based' if not use_ai else 'ai_powered',
        'generated_at': datetime.utcnow().isoformat(),
        'task_history_count': recent_tasks['total_count'],
        'category': 'mind'
    }


def generate_body_task_recommendations(user_id, use_ai=False, count=3):
    """Generate body task recommendations for a user.
    
    Args:
        user_id (str): User ID.
        use_ai (bool): Whether to use AI for recommendations.
        count (int): Number of recommendations to generate.
    
    Returns:
        dict: Body task recommendations with metadata.
    """
    recent_tasks = get_recent_tasks(user_id)
    body_templates = get_templates_by_category('body')
    
    if not body_templates:
        return {
            'recommendations': [],
            'method': 'no_templates',
            'generated_at': datetime.utcnow().isoformat(),
            'task_history_count': recent_tasks['total_count'],
            'category': 'body'
        }
    
    # Analyze patterns
    analysis = analyze_task_patterns(recent_tasks)
    
    # Select templates
    selected = select_templates_by_pattern(body_templates, analysis, count)
    
    # Add scheduling and reasons
    recommendations = []
    base_time = datetime.utcnow()
    
    for i, template in enumerate(selected):
        template['suggested_schedule'] = (base_time + timedelta(hours=4 * (i + 1))).isoformat()
        template['reason'] = _get_recommendation_reason(template, analysis)
        recommendations.append(template)
    
    return {
        'recommendations': recommendations,
        'method': 'pattern_based' if not use_ai else 'ai_powered',
        'generated_at': datetime.utcnow().isoformat(),
        'task_history_count': recent_tasks['total_count'],
        'category': 'body'
    }
