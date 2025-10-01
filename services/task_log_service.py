"""Task log service for task log operations."""
from lib.db import get_supabase


def get_user_task_logs(user_id, task_table=None):
    """Get task logs for a user, optionally filtered by task_table.
    
    Args:
        user_id (str): User ID.
        task_table (str, optional): Filter by task table ('tasks_mind' or 'tasks_body').
    
    Returns:
        list: List of task logs.
    """
    supabase = get_supabase()
    query = supabase.from_('task_logs').select('*').eq('user_id', user_id)
    
    if task_table:
        query = query.eq('task_table', task_table)
    
    res = query.order('timestamp', desc=True).execute()
    return res.data


def get_task_log_by_id(log_id):
    """Get task log by ID.
    
    Args:
        log_id (str): Log ID.
    
    Returns:
        dict: Log data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('task_logs').select('*').eq('id', log_id).execute()
    return res.data[0] if res.data else None


def create_task_log(data):
    """Create a new task log entry.
    
    Args:
        data (dict): Log data.
    
    Returns:
        dict: Created log.
    """
    supabase = get_supabase()
    res = supabase.from_('task_logs').insert(data).execute()
    return res.data[0] if res.data else None


def delete_task_log(log_id):
    """Delete a task log.
    
    Args:
        log_id (str): Log ID.
    
    Returns:
        dict: Deleted log.
    """
    supabase = get_supabase()
    res = supabase.from_('task_logs').delete().eq('id', log_id).execute()
    return res.data[0] if res.data else None
