"""Failure service for failure tracking operations."""
from lib.db import get_supabase


def get_user_failures(user_id, severity=None):
    """Get failures for a user, optionally filtered by severity.
    
    Args:
        user_id (str): User ID.
        severity (str, optional): Filter by severity.
    
    Returns:
        list: List of failures.
    """
    supabase = get_supabase()
    query = supabase.from_('failures').select('*').eq('user_id', user_id)
    
    if severity:
        query = query.eq('severity', severity)
    
    res = query.order('created_at', desc=True).execute()
    return res.data


def get_failure_by_id(failure_id):
    """Get failure by ID.
    
    Args:
        failure_id (str): Failure ID.
    
    Returns:
        dict: Failure data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('failures').select('*').eq('id', failure_id).execute()
    return res.data[0] if res.data else None


def create_failure(data):
    """Create a new failure record.
    
    Args:
        data (dict): Failure data.
    
    Returns:
        dict: Created failure.
    """
    supabase = get_supabase()
    res = supabase.from_('failures').insert(data).execute()
    return res.data[0] if res.data else None


def delete_failure(failure_id):
    """Delete a failure record.
    
    Args:
        failure_id (str): Failure ID.
    
    Returns:
        dict: Deleted failure.
    """
    supabase = get_supabase()
    res = supabase.from_('failures').delete().eq('id', failure_id).execute()
    return res.data[0] if res.data else None
