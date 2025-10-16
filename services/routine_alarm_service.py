"""Routine alarm service for alarm operations."""
from datetime import datetime

from lib.db import get_supabase


def get_user_routine_alarms(user_id, source_type=None, is_active=None):
    """Get routine alarms for a user, optionally filtered by source_type and is_active.

    Args:
        user_id (str): User ID.
        source_type (str, optional): Filter by source_type (mind, body, goal, custom).
        is_active (bool, optional): Filter by active status.

    Returns:
        list: List of routine alarms.
    """
    supabase = get_supabase()
    query = supabase.from_('routine_alarms').select('*').eq('user_id', user_id)

    if source_type:
        query = query.eq('source_type', source_type)

    if is_active is not None:
        query = query.eq('is_active', is_active)

    res = query.order('created_at', desc=True).execute()
    return res.data


def get_routine_alarm_by_id(alarm_id):
    """Get routine alarm by ID.

    Args:
        alarm_id (str): Alarm ID.

    Returns:
        dict: Alarm data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_alarms').select('*').eq('id', alarm_id).execute()
    return res.data[0] if res.data else None


def create_routine_alarm(data):
    """Create a new routine alarm.

    Args:
        data (dict): Alarm data.

    Returns:
        dict: Created alarm.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_alarms').insert(data).execute()
    return res.data[0] if res.data else None


def update_routine_alarm(alarm_id, data):
    """Update a routine alarm.

    Args:
        alarm_id (str): Alarm ID.
        data (dict): Updated data.

    Returns:
        dict: Updated alarm.
    """
    supabase = get_supabase()
    data['updated_at'] = datetime.utcnow().isoformat()
    res = supabase.from_('routine_alarms').update(data).eq('id', alarm_id).execute()
    return res.data[0] if res.data else None


def update_alarm_status(alarm_id, is_active):
    """Update only the is_active status of an alarm.

    Args:
        alarm_id (str): Alarm ID.
        is_active (bool): New active status.

    Returns:
        dict: Updated alarm.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_alarms').update({
        'is_active': is_active,
        'updated_at': datetime.utcnow().isoformat()
    }).eq('id', alarm_id).execute()
    return res.data[0] if res.data else None


def delete_routine_alarm(alarm_id):
    """Delete a routine alarm.

    Args:
        alarm_id (str): Alarm ID.

    Returns:
        dict: Deleted alarm.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_alarms').delete().eq('id', alarm_id).execute()
    return res.data[0] if res.data else None
