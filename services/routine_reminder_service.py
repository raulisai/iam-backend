"""Routine reminder service for reminder operations."""
from datetime import datetime

from lib.db import get_supabase


def get_user_routine_reminders(user_id, source_type=None, is_active=None):
    """Get routine reminders for a user, optionally filtered by source_type and is_active.

    Args:
        user_id (str): User ID.
        source_type (str, optional): Filter by source_type (mind, body, goal, custom).
        is_active (bool, optional): Filter by active status.

    Returns:
        list: List of routine reminders.
    """
    supabase = get_supabase()
    query = supabase.from_('routine_reminders').select('*').eq('user_id', user_id)

    if source_type:
        query = query.eq('source_type', source_type)

    if is_active is not None:
        query = query.eq('is_active', is_active)

    res = query.order('created_at', desc=True).execute()
    return res.data


def get_routine_reminder_by_id(reminder_id):
    """Get routine reminder by ID.

    Args:
        reminder_id (str): Reminder ID.

    Returns:
        dict: Reminder data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_reminders').select('*').eq('id', reminder_id).execute()
    return res.data[0] if res.data else None


def create_routine_reminder(data):
    """Create a new routine reminder.

    Args:
        data (dict): Reminder data.

    Returns:
        dict: Created reminder.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_reminders').insert(data).execute()
    return res.data[0] if res.data else None


def update_routine_reminder(reminder_id, data):
    """Update a routine reminder.

    Args:
        reminder_id (str): Reminder ID.
        data (dict): Updated data.

    Returns:
        dict: Updated reminder.
    """
    supabase = get_supabase()
    data['updated_at'] = datetime.utcnow().isoformat()
    res = supabase.from_('routine_reminders').update(data).eq('id', reminder_id).execute()
    return res.data[0] if res.data else None


def update_reminder_status(reminder_id, is_active):
    """Update only the is_active status of a reminder.

    Args:
        reminder_id (str): Reminder ID.
        is_active (bool): New active status.

    Returns:
        dict: Updated reminder.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_reminders').update({
        'is_active': is_active,
        'updated_at': datetime.utcnow().isoformat()
    }).eq('id', reminder_id).execute()
    return res.data[0] if res.data else None


def delete_routine_reminder(reminder_id):
    """Delete a routine reminder.

    Args:
        reminder_id (str): Reminder ID.

    Returns:
        dict: Deleted reminder.
    """
    supabase = get_supabase()
    res = supabase.from_('routine_reminders').delete().eq('id', reminder_id).execute()
    return res.data[0] if res.data else None
