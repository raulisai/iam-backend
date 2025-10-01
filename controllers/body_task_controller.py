"""Body task controller for handling body task operations."""
from flask import jsonify, request
from services.body_task_service import (
    get_user_body_tasks,
    get_body_task_by_id,
    create_body_task,
    update_body_task,
    complete_body_task,
    delete_body_task
)


def get_my_body_tasks():
    """Get authenticated user's body tasks.
    
    Returns:
        tuple: JSON response with tasks and status code.
    """
    user_id = request.user.get('user_id')
    status = request.args.get('status')  # Optional query parameter
    
    tasks = get_user_body_tasks(user_id, status)
    return jsonify(tasks), 200


def get_body_task(task_id):
    """Get body task by ID.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with task and status code.
    """
    task = get_body_task_by_id(task_id)
    
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    # Verify task belongs to authenticated user
    user_id = request.user.get('user_id')
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(task), 200


def create_new_body_task(data):
    """Create a new body task.
    
    Args:
        data (dict): Task data.
    
    Returns:
        tuple: JSON response with created task and status code.
    """
    user_id = request.user.get('user_id')
    
    # Required fields
    if 'template_id' not in data or 'created_by' not in data:
        return jsonify({'error': 'template_id and created_by are required'}), 400
    
    # Add user_id to data
    data['user_id'] = user_id
    
    task = create_body_task(data)
    
    if task is None:
        return jsonify({'error': 'Failed to create task'}), 500
    
    return jsonify(task), 201


def update_body_task_data(task_id, data):
    """Update a body task.
    
    Args:
        task_id (str): Task ID.
        data (dict): Updated data.
    
    Returns:
        tuple: JSON response with updated task and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify task belongs to user
    task = get_body_task_by_id(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Remove immutable fields
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('created_at', None)
    
    updated_task = update_body_task(task_id, data)
    
    if updated_task is None:
        return jsonify({'error': 'Update failed'}), 500
    
    return jsonify(updated_task), 200


def complete_task(task_id):
    """Mark a body task as completed.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with updated task and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify task belongs to user
    task = get_body_task_by_id(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get XP from template or use default
    xp_awarded = task.get('task_templates', {}).get('reward_xp', 0) if task.get('task_templates') else 0
    
    updated_task = complete_body_task(task_id, xp_awarded)
    
    if updated_task is None:
        return jsonify({'error': 'Failed to complete task'}), 500
    
    return jsonify(updated_task), 200


def delete_body_task_by_id(task_id):
    """Delete a body task.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with deleted task and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify task belongs to user
    task = get_body_task_by_id(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted_task = delete_body_task(task_id)
    
    if deleted_task is None:
        return jsonify({'error': 'Failed to delete task'}), 500
    
    return jsonify(deleted_task), 200
