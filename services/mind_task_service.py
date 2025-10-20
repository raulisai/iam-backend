"""Mind task service for mind task operations."""
from lib.db import get_supabase
from datetime import datetime
from services.points_service import add_earned_points, subtract_earned_points


def get_user_mind_tasks(user_id, status=None):
    """Get mind tasks for a user, optionally filtered by status.
    
    Args:
        user_id (str): User ID.
        status (str, optional): Filter by status.
    
    Returns:
        list: List of mind tasks.
    """
    supabase = get_supabase()
    query = supabase.from_('tasks_mind').select('*, task_templates(*)').eq('user_id', user_id)
    
    if status:
        query = query.eq('status', status)
    
    res = query.order('created_at', desc=True).execute()
    return res.data


def get_mind_task_by_id(task_id):
    """Get mind task by ID.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Task data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('tasks_mind').select('*, task_templates(*)').eq('id', task_id).execute()
    return res.data[0] if res.data else None


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


def complete_mind_task(task_id, user_id, reward_xp):
    """Mark a mind task as completed and add points.
    
    Args:
        task_id (str): Task ID.
        user_id (str): User ID.
        reward_xp (int): XP to award.
    
    Returns:
        dict: Updated task with points info.
    """
    supabase = get_supabase()
    
    # Update task status
    res = supabase.from_('tasks_mind').update({
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat()
    }).eq('id', task_id).execute()
    
    if not res.data:
        return None
    
    task = res.data[0]
    
    # Add points if reward_xp > 0
    points_result = None
    if reward_xp > 0:
        points_result = add_earned_points(user_id, reward_xp, 'mind')
    
    return {
        'task': task,
        'points': points_result
    }


def uncomplete_mind_task(task_id, user_id, reward_xp):
    """Revert a mind task to pending and subtract points.
    
    Args:
        task_id (str): Task ID.
        user_id (str): User ID.
        reward_xp (int): XP to remove.
    
    Returns:
        dict: Updated task with points info.
    """
    supabase = get_supabase()
    
    # Update task status back to pending
    res = supabase.from_('tasks_mind').update({
        'status': 'pending',
        'completed_at': None
    }).eq('id', task_id).execute()
    
    if not res.data:
        return None
    
    task = res.data[0]
    
    # Subtract points if reward_xp > 0
    points_result = None
    if reward_xp > 0:
        points_result = subtract_earned_points(user_id, reward_xp, 'mind')
    
    return {
        'task': task,
        'points': points_result
    }


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
