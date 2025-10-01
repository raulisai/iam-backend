"""Goal controller for handling goal operations."""
from flask import jsonify, request
from services.goal_service import (
    get_user_goals,
    get_goal_by_id,
    create_goal,
    update_goal,
    delete_goal
)


def get_my_goals():
    """Get authenticated user's goals.
    
    Returns:
        tuple: JSON response with goals and status code.
    """
    user_id = request.user.get('user_id')
    is_active = request.args.get('is_active')
    
    # Convert string to boolean if present
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    
    goals = get_user_goals(user_id, is_active)
    return jsonify(goals), 200


def get_goal(goal_id):
    """Get goal by ID.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        tuple: JSON response with goal and status code.
    """
    goal = get_goal_by_id(goal_id)
    
    if goal is None:
        return jsonify({'error': 'Goal not found'}), 404
    
    user_id = request.user.get('user_id')
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(goal), 200


def create_new_goal(data):
    """Create a new goal.
    
    Args:
        data (dict): Goal data.
    
    Returns:
        tuple: JSON response with created goal and status code.
    """
    user_id = request.user.get('user_id')
    
    if 'title' not in data:
        return jsonify({'error': 'title is required'}), 400
    
    data['user_id'] = user_id
    
    goal = create_goal(data)
    
    if goal is None:
        return jsonify({'error': 'Failed to create goal'}), 500
    
    return jsonify(goal), 201


def update_goal_data(goal_id, data):
    """Update a goal.
    
    Args:
        goal_id (str): Goal ID.
        data (dict): Updated data.
    
    Returns:
        tuple: JSON response with updated goal and status code.
    """
    user_id = request.user.get('user_id')
    
    goal = get_goal_by_id(goal_id)
    if goal is None:
        return jsonify({'error': 'Goal not found'}), 404
    
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('created_at', None)
    
    updated_goal = update_goal(goal_id, data)
    
    if updated_goal is None:
        return jsonify({'error': 'Update failed'}), 500
    
    return jsonify(updated_goal), 200


def delete_goal_by_id(goal_id):
    """Delete a goal.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        tuple: JSON response with deleted goal and status code.
    """
    user_id = request.user.get('user_id')
    
    goal = get_goal_by_id(goal_id)
    if goal is None:
        return jsonify({'error': 'Goal not found'}), 404
    
    if goal.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted_goal = delete_goal(goal_id)
    
    if deleted_goal is None:
        return jsonify({'error': 'Failed to delete goal'}), 500
    
    return jsonify(deleted_goal), 200
