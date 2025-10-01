"""Bot rule service for bot rule operations."""
from lib.db import get_supabase


def get_all_bot_rules(active_only=False):
    """Get all bot rules, optionally filtered by active status.
    
    Args:
        active_only (bool): Filter to only active rules.
    
    Returns:
        list: List of bot rules.
    """
    supabase = get_supabase()
    query = supabase.from_('bot_rules').select('*')
    
    if active_only:
        query = query.eq('active', True)
    
    res = query.order('priority', desc=True).execute()
    return res.data


def get_bot_rule_by_id(rule_id):
    """Get bot rule by ID.
    
    Args:
        rule_id (str): Rule ID.
    
    Returns:
        dict: Rule data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('bot_rules').select('*').eq('id', rule_id).execute()
    return res.data[0] if res.data else None


def create_bot_rule(data):
    """Create a new bot rule.
    
    Args:
        data (dict): Rule data.
    
    Returns:
        dict: Created rule.
    """
    supabase = get_supabase()
    res = supabase.from_('bot_rules').insert(data).execute()
    return res.data[0] if res.data else None


def update_bot_rule(rule_id, data):
    """Update a bot rule.
    
    Args:
        rule_id (str): Rule ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated rule.
    """
    supabase = get_supabase()
    res = supabase.from_('bot_rules').update(data).eq('id', rule_id).execute()
    return res.data[0] if res.data else None


def delete_bot_rule(rule_id):
    """Delete a bot rule.
    
    Args:
        rule_id (str): Rule ID.
    
    Returns:
        dict: Deleted rule.
    """
    supabase = get_supabase()
    res = supabase.from_('bot_rules').delete().eq('id', rule_id).execute()
    return res.data[0] if res.data else None
