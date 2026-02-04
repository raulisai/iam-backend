"""Mind task service for mind task operations."""
from lib.db import get_supabase
from datetime import datetime


def get_user_mind_tasks(user_id, status=None):
    """Get mind tasks for a user, optionally filtered by status.
    
    Args:
        user_id (str): User ID.
        status (str, optional): Filter by status.
    
    Returns:
        list: List of mind tasks.
    """
    supabase = get_supabase()
    supabase = get_supabase()
    query = supabase.from_('tasks_mind').select('*').eq('user_id', user_id)
    
    if status:
        query = query.eq('status', status)
    
    res = query.order('created_at', desc=True).execute()
    tasks = res.data or []
    
    # Manually join task_templates
    if tasks:
        template_ids = [t['template_id'] for t in tasks if t.get('template_id')]
        if template_ids:
            templates_res = supabase.from_('task_templates').select('*').in_('id', template_ids).execute()
            templates = {t['id']: t for t in templates_res.data}
            
            for task in tasks:
                if task.get('template_id') in templates:
                    task['task_templates'] = templates[task['template_id']]
                else:
                    task['task_templates'] = {}
    
    return tasks


def get_mind_task_by_id(task_id):
    """Get mind task by ID.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Task data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_mind').select('*').eq('id', task_id).execute()
    task = res.data[0] if res.data else None
    
    if task and task.get('template_id'):
        template_res = supabase.from_('task_templates').select('*').eq('id', task['template_id']).execute()
        if template_res.data:
            task['task_templates'] = template_res.data[0]
    
    return task


def create_mind_task(data):
    """Create a new mind task.
    
    Args:
        data (dict): Task data.
    
    Returns:
        dict: Created task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_mind').insert(data).execute()
    return res.data[0] if res.data else None


def update_mind_task(task_id, data):
    """Update a mind task.
    
    Args:
        task_id (str): Task ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_mind').update(data).eq('id', task_id).execute()
    return res.data[0] if res.data else None


def complete_mind_task(task_id, xp_awarded):
    """Mark a mind task as completed.
    
    Args:
        task_id (str): Task ID.
        xp_awarded (int): XP to award.
    
    Returns:
        dict: Updated task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_mind').update({
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat(),
        'xp_awarded': xp_awarded
    }).eq('id', task_id).execute()
    return res.data[0] if res.data else None


def delete_mind_task(task_id):
    """Delete a mind task.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Deleted task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_mind').delete().eq('id', task_id).execute()
    return res.data[0] if res.data else None
