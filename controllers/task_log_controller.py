"""Task log controller for handling task log operations."""
from flask import jsonify, request
from services.task_log_service import (
    get_user_task_logs,
    create_task_log
)


def get_my_task_logs():
    """Get authenticated user's task logs.
    
    Returns:
        tuple: JSON response with logs and status code.
    """
    user_id = request.user.get('user_id')
    task_table = request.args.get('task_table')  # Optional filter
    
    logs = get_user_task_logs(user_id, task_table)
    return jsonify(logs), 200


def create_log(data):
    """Create a new task log entry.
    
    Args:
        data (dict): Log data.
    
    Returns:
        tuple: JSON response with created log and status code.
    """
    user_id = request.user.get('user_id')
    
    required_fields = ['task_table', 'task_id', 'action']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'task_table, task_id, and action are required'}), 400
    
    data['user_id'] = user_id
    
    log = create_task_log(data)
    
    if log is None:
        return jsonify({'error': 'Failed to create log'}), 500
    
    return jsonify(log), 201
