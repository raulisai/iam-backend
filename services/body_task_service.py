"""Body task service for body task operations."""
from lib.db import get_supabase
from datetime import datetime
from services.points_service import add_earned_points, subtract_earned_points


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


def complete_body_task(task_id, user_id, reward_xp):
    """Mark a body task as completed and add points.
    
    Args:
        task_id (str): Task ID.
        user_id (str): User ID.
        reward_xp (int): XP to award.
    
    Returns:
        dict: Updated task with points info.
    """
    supabase = get_supabase()
    
    # Update task status
    res = supabase.from_('tasks_body').update({
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat()
    }).eq('id', task_id).execute()
    
    if not res.data:
        return None
    
    task = res.data[0]
    
    # Add points if reward_xp > 0
    points_result = None
    if reward_xp > 0:
        points_result = add_earned_points(user_id, reward_xp, 'body')
    
    return {
        'task': task,
        'points': points_result
    }


def uncomplete_body_task(task_id, user_id, reward_xp):
    """Revert a body task to pending and subtract points.
    
    Args:
        task_id (str): Task ID.
        user_id (str): User ID.
        reward_xp (int): XP to remove.
    
    Returns:
        dict: Updated task with points info.
    """
    supabase = get_supabase()
    
    # Update task status back to pending
    res = supabase.from_('tasks_body').update({
        'status': 'pending',
        'completed_at': None
    }).eq('id', task_id).execute()
    
    if not res.data:
        return None
    
    task = res.data[0]
    
    # Subtract points if reward_xp > 0
    points_result = None
    if reward_xp > 0:
        points_result = subtract_earned_points(user_id, reward_xp, 'body')
    
    return {
        'task': task,
        'points': points_result
    }


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
