"""Goal service for goal operations."""
from lib.db import get_supabase


def get_user_goals(user_id, is_active=None):
    """Get goals for a user, optionally filtered by active status.
    
    Args:
        user_id (str): User ID.
        is_active (bool, optional): Filter by active status.
    
    Returns:
        list: List of goals.
    """
    supabase = get_supabase()
    query = supabase.from_('goals').select('*').eq('user_id', user_id)
    
    if is_active is not None:
        query = query.eq('is_active', is_active)
    
    res = query.order('created_at', desc=True).execute()
    return res.data


def get_goal_by_id(goal_id):
    """Get goal by ID.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        dict: Goal data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('goals').select('*').eq('id', goal_id).execute()
    return res.data[0] if res.data else None


def create_goal(data):
    """Create a new goal.
    
    Args:
        data (dict): Goal data.
    
    Returns:
        dict: Created goal.
    """
    supabase = get_supabase()
    res = supabase.from_('goals').insert(data).execute()
    return res.data[0] if res.data else None


def update_goal(goal_id, data):
    """Update a goal.
    
    Args:
        goal_id (str): Goal ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated goal.
    """
    supabase = get_supabase()
    res = supabase.from_('goals').update(data).eq('id', goal_id).execute()
    return res.data[0] if res.data else None


def delete_goal(goal_id):
    """Delete a goal.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        dict: Deleted goal.
    """
    supabase = get_supabase()
    res = supabase.from_('goals').delete().eq('id', goal_id).execute()
    return res.data[0] if res.data else None
