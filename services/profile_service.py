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
        dict: Created profile data.
    """
    supabase = get_supabase()
    res = supabase.from_('profiles').insert(data).execute()
    return res.data[0] if res.data else None


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
