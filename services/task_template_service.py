"""Task template service for task template operations."""
from lib.db import get_supabase


def get_all_task_templates():
    """Get all task templates.
    
    Returns:
        list: List of task templates.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').select('*').execute()
    return res.data


def get_task_template_by_id(template_id):
    """Get task template by ID.
    
    Args:
        template_id (str): Template ID.
    
    Returns:
        dict: Template data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').select('*').eq('id', template_id).execute()
    return res.data[0] if res.data else None


def get_task_template_by_key(key):
    """Get task template by key.
    
    Args:
        key (str): Template key.
    
    Returns:
        dict: Template data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').select('*').eq('key', key).execute()
    return res.data[0] if res.data else None


def get_templates_by_category(category):
    """Get templates by category.
    
    Args:
        category (str): Category ('mind' or 'body').
    
    Returns:
        list: List of templates.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').select('*').eq('category', category).execute()
    return res.data


def create_task_template(data):
    """Create a new task template.
    
    Args:
        data (dict): Template data.
    
    Returns:
        dict: Created template.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').insert(data).execute()
    return res.data[0] if res.data else None


def update_task_template(template_id, data):
    """Update a task template.
    
    Args:
        template_id (str): Template ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated template.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').update(data).eq('id', template_id).execute()
    return res.data[0] if res.data else None


def delete_task_template(template_id):
    """Delete a task template.
    
    Args:
        template_id (str): Template ID.
    
    Returns:
        dict: Deleted template.
    """
    supabase = get_supabase()
    res = supabase.from_('task_templates').delete().eq('id', template_id).execute()
    return res.data[0] if res.data else None
