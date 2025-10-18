"""Profile service for user profile operations."""
from lib.db import get_supabase


def get_profile_by_user_id(user_id):
    """Get user profile by user_id.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        dict: Profile data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('profiles').select('*').eq('user_id', user_id).execute()
    return res.data[0] if res.data else None


def create_profile(data):
    """Create a new user profile.
    
    Args:
        data (dict): Profile data.
    
    Returns:
        dict: Created profile data or None if duplicate.
        
    Raises:
        ValueError: If profile already exists for this user.
    """
    # Validar campos numéricos: si vienen null o tienen error, asignar 0
    numeric_fields = [
        'weight_kg', 'height_cm', 'hours_available_to_week',
        'hours_used_to_week', 'goal_points_target',
        'goal_points_earned'
    ]
    
    for field in numeric_fields:
        if field in data:
            value = data.get(field)
            if value is None or value == '':
                data[field] = 0
            else:
                try:
                    data[field] = float(value)
                except (ValueError, TypeError):
                    data[field] = 0
    
    # time_dead se queda por defecto en 9 minutos
    data.setdefault('time_dead', 9)
    
    supabase = get_supabase()
    try:
        res = supabase.from_('profiles').insert(data).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        # Check if it's a duplicate key error (code 23505)
        error_str = str(e)
        if '23505' in error_str or 'duplicate key' in error_str.lower():
            raise ValueError('Profile already exists for this user') from e
        raise


def update_profile(user_id, data):
    """Update user profile.
    
    Args:
        user_id (str): The user's ID.
        data (dict): Updated profile data.
    
    Returns:
        dict: Updated profile data.
    """
    supabase = get_supabase()
    res = supabase.from_('profiles').update(data).eq('user_id', user_id).execute()
    return res.data[0] if res.data else None


def delete_profile(user_id):
    """Delete user profile.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        dict: Deleted profile data.
    """
    supabase = get_supabase()
    res = supabase.from_('profiles').delete().eq('user_id', user_id).execute()
    return res.data[0] if res.data else None


def add_goal_points(user_id, task_occurrence_id):
    """Add points to user profile from a completed goal task.
    
    Args:
        user_id (str): The user's ID.
        task_occurrence_id (str): The task occurrence ID that was completed.
    
    Returns:
        dict: Updated profile with points calculation details or None if error.
    """
    supabase = get_supabase()
    
    # Get task occurrence details with task and goal info
    task_occ_res = supabase.from_('task_occurrences').select(
        'id, task_id, goal_tasks(id, weight, goal_id, goals(id, target_value))'
    ).eq('id', task_occurrence_id).execute()
    
    if not task_occ_res.data:
        return None
    
    task_occ = task_occ_res.data[0]
    task_weight = task_occ.get('goal_tasks', {}).get('weight', 1)
    
    # Get the last log entry for this occurrence to check if completed
    log_res = supabase.from_('task_logs').select('action, metadata').eq(
        'task_table', 'task_occurrences'
    ).eq('task_id', task_occurrence_id).order('timestamp', desc=True).limit(1).execute()
    
    if not log_res.data or log_res.data[0].get('action') != 'completed':
        return {'error': 'Task is not marked as completed'}
    
    # Calculate points (use metadata value if present, otherwise use weight)
    metadata = log_res.data[0].get('metadata', {})
    points_to_add = metadata.get('value', task_weight) if isinstance(metadata, dict) else task_weight
    
    # Get current profile
    profile_res = supabase.from_('profiles').select('*').eq('user_id', user_id).execute()
    
    if not profile_res.data:
        return None
    
    current_profile = profile_res.data[0]
    current_earned = current_profile.get('goal_points_earned', 0)
    new_earned = current_earned + points_to_add
    
    # Update profile with new points
    update_res = supabase.from_('profiles').update({
        'goal_points_earned': new_earned
    }).eq('user_id', user_id).execute()
    
    if not update_res.data:
        return None
    
    result = update_res.data[0]
    result['points_added'] = points_to_add
    result['previous_earned'] = current_earned
    
    return result
