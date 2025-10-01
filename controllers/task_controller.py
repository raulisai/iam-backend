"""Task controller for handling task CRUD operations."""
from datetime import datetime
from flask import jsonify
from lib.db import get_supabase


def get_all_tasks():
    """Get all tasks from the database.
    
    Returns:
        tuple: JSON response with tasks data and status code.
    """
    supabase = get_supabase()
    res = supabase.from_('Tasks').select('*').execute()
    return jsonify(res.data), 200


def get_task_by_id(task_id):
    """Get a specific task by ID.
    
    Args:
        task_id (int): The task ID.
    
    Returns:
        tuple: JSON response with task data and status code.
    """
    supabase = get_supabase()
    res = supabase.from_('Tasks').select('*').eq('id', task_id).execute()
    return jsonify(res.data), 200


def create_new_task(data):
    """Create a new task.
    
    Args:
        data (dict): Task data containing title, time, points, desc, level, categoria.
    
    Returns:
        tuple: JSON response with created task data and status code.
    """
    title = data.get('title')
    time = data.get('time')
    points = data.get('points')
    desc = data.get('desc')
    level = data.get('level')
    categoria = data.get('categoria')
    
    if not all([title, time, points, desc, level, categoria]):
        return jsonify({'error': 'All fields are required'}), 400
    
    supabase = get_supabase()
    res = supabase.from_('Tasks').insert({
        'created_at': datetime.now().isoformat(),
        'title': title,
        'time': time,
        'points': points,
        'desc': desc,
        'level': level,
        'categoria': categoria
    }).execute()
    
    return jsonify(res.data), 200


def update_task_by_id(task_id, data):
    """Update an existing task.
    
    Args:
        task_id (int): The task ID.
        data (dict): Updated task data.
    
    Returns:
        tuple: JSON response with updated task data and status code.
    """
    supabase = get_supabase()
    res = supabase.from_('Tasks').update({
        'title': data.get('title'),
        'time': data.get('time'),
        'points': data.get('points'),
        'desc': data.get('desc'),
        'level': data.get('level'),
        'categoria': data.get('categoria')
    }).eq('id', task_id).execute()
    
    return jsonify(res.data), 200


def delete_task_by_id(task_id):
    """Delete a task by ID.
    
    Args:
        task_id (int): The task ID.
    
    Returns:
        tuple: JSON response with deleted task data and status code.
    """
    supabase = get_supabase()
    res = supabase.from_('Tasks').delete().eq('id', task_id).execute()
    return jsonify(res.data), 200
