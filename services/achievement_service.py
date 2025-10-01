"""Achievement service for achievement operations."""
from lib.db import get_supabase


def get_user_achievements(user_id):
    """Get all achievements for a user.
    
    Args:
        user_id (str): User ID.
    
    Returns:
        list: List of achievements.
    """
    supabase = get_supabase()
    res = supabase.from_('achievements').select('*').eq('user_id', user_id).order('awarded_at', desc=True).execute()
    return res.data


def get_achievement_by_id(achievement_id):
    """Get achievement by ID.
    
    Args:
        achievement_id (str): Achievement ID.
    
    Returns:
        dict: Achievement data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('achievements').select('*').eq('id', achievement_id).execute()
    return res.data[0] if res.data else None


def create_achievement(data):
    """Award a new achievement to a user.
    
    Args:
        data (dict): Achievement data.
    
    Returns:
        dict: Created achievement.
    """
    supabase = get_supabase()
    res = supabase.from_('achievements').insert(data).execute()
    return res.data[0] if res.data else None


def delete_achievement(achievement_id):
    """Delete an achievement.
    
    Args:
        achievement_id (str): Achievement ID.
    
    Returns:
        dict: Deleted achievement.
    """
    supabase = get_supabase()
    res = supabase.from_('achievements').delete().eq('id', achievement_id).execute()
    return res.data[0] if res.data else None
