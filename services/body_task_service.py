"""Body task service for body task operations."""
from lib.db import get_supabase
from datetime import datetime


def get_user_body_tasks(user_id, status=None):
    """Get body tasks for a user, optionally filtered by status.
    
    Args:
        user_id (str): User ID.
        status (str, optional): Filter by status.
    
    Returns:
        list: List of body tasks.
    """
    supabase = get_supabase()
    query = supabase.from_('tasks_body').select('*, task_templates(*)').eq('user_id', user_id)
    
    if status:
        query = query.eq('status', status)
    
    res = query.order('created_at', desc=True).execute()
    return res.data


def get_body_task_by_id(task_id):
    """Get body task by ID.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Task data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_body').select('*, task_templates(*)').eq('id', task_id).execute()
    return res.data[0] if res.data else None


def create_body_task(data):
    """Create a new body task.
    
    Args:
        data (dict): Task data.
    
    Returns:
        dict: Created task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_body').insert(data).execute()
    return res.data[0] if res.data else None


def update_body_task(task_id, data):
    """Update a body task.
    
    Args:
        task_id (str): Task ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_body').update(data).eq('id', task_id).execute()
    return res.data[0] if res.data else None


def complete_body_task(task_id, xp_awarded):
    """Mark a body task as completed.
    
    Args:
        task_id (str): Task ID.
        xp_awarded (int): XP to award.
    
    Returns:
        dict: Updated task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_body').update({
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat(),
        'xp_awarded': xp_awarded
    }).eq('id', task_id).execute()
    return res.data[0] if res.data else None


def delete_body_task(task_id):
    """Delete a body task.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Deleted task.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_body').delete().eq('id', task_id).execute()
    return res.data[0] if res.data else None
