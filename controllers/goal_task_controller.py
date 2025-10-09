"""Goal Task controller for handling goal task operations."""
from flask import jsonify, request
from datetime import datetime, timedelta
from services.goal_task_service import (
    get_goal_tasks,
    get_goal_task_by_id,
    create_goal_task,
    update_goal_task,
    delete_goal_task,
    get_task_occurrences,
    get_occurrence_by_id,
    create_task_occurrence,
    generate_occurrences_for_task,
    delete_task_occurrence,
    get_occurrence_logs,
    log_occurrence_action,
    get_goal_progress,
    get_occurrence_with_status,
    get_occurrences_with_status,
    get_goal_progress_detailed
)
from services.goal_service import get_goal_by_id


def get_tasks_for_goal(goal_id):
    """Get all tasks for a goal.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        tuple: JSON response with tasks and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify goal exists and belongs to user
    goal = get_goal_by_id(goal_id)
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404
    
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    tasks = get_goal_tasks(goal_id, user_id)
    return jsonify(tasks), 200


def get_task(task_id):
    """Get task by ID.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with task and status code.
    """
    user_id = request.user.get('user_id')
    task = get_goal_task_by_id(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(task), 200


def create_new_goal_task(goal_id, data):
    """Create a new goal task.
    
    Args:
        goal_id (str): Goal ID.
        data (dict): Task data.
    
    Returns:
        tuple: JSON response with created task and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify goal exists and belongs to user
    goal = get_goal_by_id(goal_id)
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404
    
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Validate required fields
    if 'title' not in data:
        return jsonify({'error': 'title is required'}), 400
    
    # Set defaults
    data['goal_id'] = goal_id
    data['user_id'] = user_id
    if 'required' not in data:
        data['required'] = True
    if 'weight' not in data:
        data['weight'] = 1
    
    # Only keep fields that exist in goal_tasks schema
    # Valid fields: id, goal_id, user_id, title, description, type, required, weight, due_at, schedule_rrule, created_at
    allowed_fields = ['goal_id', 'user_id', 'title', 'description', 'type', 'required', 'weight', 'due_at', 'schedule_rrule']
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    
    try:
        task = create_goal_task(filtered_data)
        
        if not task:
            return jsonify({'error': 'Failed to create task'}), 500
        
        return jsonify(task), 201
    except Exception as e:
        error_msg = str(e)
        if 'could not find' in error_msg.lower() or 'pgrst204' in error_msg.lower():
            return jsonify({'error': 'Database schema error. Please contact support.', 'details': error_msg}), 500
        elif 'winerror 10035' in error_msg.lower() or 'readerror' in error_msg.lower():
            return jsonify({'error': 'Network connection issue. Please try again.'}), 503
        else:
            return jsonify({'error': 'Failed to create task', 'details': error_msg}), 500


def update_task_data(task_id, data):
    """Update a goal task.
    
    Args:
        task_id (str): Task ID.
        data (dict): Updated data.
    
    Returns:
        tuple: JSON response with updated task and status code.
    """
    user_id = request.user.get('user_id')
    
    task = get_goal_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Remove fields that shouldn't be updated
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('goal_id', None)
    data.pop('created_at', None)
    
    updated_task = update_goal_task(task_id, data)
    
    if not updated_task:
        return jsonify({'error': 'Update failed'}), 500
    
    return jsonify(updated_task), 200


def delete_task_by_id(task_id):
    """Delete a goal task.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with deleted task and status code.
    """
    user_id = request.user.get('user_id')
    
    task = get_goal_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted_task = delete_goal_task(task_id)
    
    if not deleted_task:
        return jsonify({'error': 'Failed to delete task'}), 500
    
    return jsonify(deleted_task), 200


def get_occurrences_for_task(task_id):
    """Get occurrences for a task.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with occurrences and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify task exists and belongs to user
    task = get_goal_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get date filters from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    include_status = request.args.get('include_status', 'true').lower() == 'true'
    
    if include_status:
        occurrences = get_occurrences_with_status(task_id, start_date, end_date)
    else:
        occurrences = get_task_occurrences(task_id, start_date, end_date)
    
    return jsonify(occurrences), 200


def create_new_occurrence(task_id, data):
    """Create a new task occurrence.
    
    Args:
        task_id (str): Task ID.
        data (dict): Occurrence data.
    
    Returns:
        tuple: JSON response with created occurrence and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify task exists and belongs to user
    task = get_goal_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Validate required fields
    if 'scheduled_at' not in data:
        return jsonify({'error': 'scheduled_at is required'}), 400
    
    data['task_id'] = task_id
    
    occurrence = create_task_occurrence(data)
    
    if not occurrence:
        return jsonify({'error': 'Failed to create occurrence or already exists'}), 409
    
    # Automatically log as completed when created (since creating = completing the task)
    metadata = {}
    if 'value' in data:
        metadata['value'] = data['value']
    
    log_occurrence_action(occurrence['id'], user_id, 'completed', metadata)
    
    # Return occurrence with completed status
    occurrence_with_status = get_occurrence_with_status(occurrence['id'])
    
    return jsonify(occurrence_with_status or occurrence), 201


def generate_occurrences(task_id):
    """Generate occurrences for a task based on its schedule.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        tuple: JSON response with generated occurrences and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify task exists and belongs to user
    task = get_goal_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get date range from query params or use defaults
    data = request.get_json() or {}
    start_date_str = data.get('start_date') or request.args.get('start_date')
    end_date_str = data.get('end_date') or request.args.get('end_date')
    
    # Default to current month if not specified
    if not start_date_str:
        start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
    
    if not end_date_str:
        # End of current month
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month.replace(day=1) - timedelta(days=1)
        end_date = end_date.replace(hour=23, minute=59, second=59)
    else:
        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
    
    occurrences = generate_occurrences_for_task(task_id, task, start_date, end_date)
    
    return jsonify({
        'generated': len(occurrences),
        'occurrences': occurrences
    }), 201


def get_occurrence(occurrence_id):
    """Get occurrence by ID with status.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        tuple: JSON response with occurrence and status code.
    """
    user_id = request.user.get('user_id')
    
    occurrence = get_occurrence_with_status(occurrence_id)
    if not occurrence:
        return jsonify({'error': 'Occurrence not found'}), 404
    
    # Verify ownership through task
    task = get_goal_task_by_id(occurrence.get('task_id'))
    if not task or task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(occurrence), 200


def delete_occurrence(occurrence_id):
    """Delete an occurrence.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        tuple: JSON response with deleted occurrence and status code.
    """
    user_id = request.user.get('user_id')
    
    occurrence = get_occurrence_by_id(occurrence_id)
    if not occurrence:
        return jsonify({'error': 'Occurrence not found'}), 404
    
    # Verify ownership through task
    task = get_goal_task_by_id(occurrence.get('task_id'))
    if not task or task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted = delete_task_occurrence(occurrence_id)
    
    if not deleted:
        return jsonify({'error': 'Failed to delete occurrence'}), 500
    
    return jsonify(deleted), 200


def log_action_on_occurrence(occurrence_id, data):
    """Log an action on an occurrence (complete, skip, etc).
    
    Args:
        occurrence_id (str): Occurrence ID.
        data (dict): Log data with action and optional metadata.
    
    Returns:
        tuple: JSON response with log entry and status code.
    """
    user_id = request.user.get('user_id')
    
    occurrence = get_occurrence_by_id(occurrence_id)
    if not occurrence:
        return jsonify({'error': 'Occurrence not found'}), 404
    
    # Verify ownership through task
    task = get_goal_task_by_id(occurrence.get('task_id'))
    if not task or task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Validate required fields
    if 'action' not in data:
        return jsonify({'error': 'action is required'}), 400
    
    action = data['action']
    metadata = data.get('metadata', {})
    
    log = log_occurrence_action(occurrence_id, user_id, action, metadata)
    
    if not log:
        return jsonify({'error': 'Failed to create log'}), 500
    
    return jsonify(log), 201


def get_logs_for_occurrence(occurrence_id):
    """Get all logs for an occurrence.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        tuple: JSON response with logs and status code.
    """
    user_id = request.user.get('user_id')
    
    occurrence = get_occurrence_by_id(occurrence_id)
    if not occurrence:
        return jsonify({'error': 'Occurrence not found'}), 404
    
    # Verify ownership through task
    task = get_goal_task_by_id(occurrence.get('task_id'))
    if not task or task.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    logs = get_occurrence_logs(occurrence_id)
    
    return jsonify(logs), 200


def get_progress_for_goal(goal_id):
    """Get progress for a goal.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        tuple: JSON response with progress data and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify goal exists and belongs to user
    goal = get_goal_by_id(goal_id)
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404
    
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    progress = get_goal_progress(goal_id)
    
    return jsonify(progress), 200


def get_progress_detailed_for_goal(goal_id):
    """Get detailed progress for a goal (for debugging).
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        tuple: JSON response with detailed progress data and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify goal exists and belongs to user
    goal = get_goal_by_id(goal_id)
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404
    
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    progress = get_goal_progress_detailed(goal_id)
    
    return jsonify(progress), 200
