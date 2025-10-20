"""Points controller for handling points management endpoints."""
from flask import jsonify
from services.points_service import (
    get_points,
    calculate_goal_points_target,
    add_earned_points,
    subtract_earned_points,
    recalculate_all_points
)


def get_user_points(user_id):
    """Get points summary for a user.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        tuple: JSON response with points data and status code.
    """
    try:
        points_data = get_points(user_id)
        
        if points_data is None:
            return jsonify({'error': 'User profile not found'}), 404
        
        return jsonify(points_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def calculate_target_points(user_id):
    """Calculate and update goal_points_target for a user.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        tuple: JSON response with calculated points breakdown and status code.
    """
    try:
        result = calculate_goal_points_target(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def add_points(user_id, data):
    """Add earned points to a user's profile.
    
    Args:
        user_id (str): The user's ID.
        data (dict): Request data containing points and task_type.
    
    Returns:
        tuple: JSON response with updated points and status code.
    """
    try:
        points = data.get('points')
        task_type = data.get('task_type', 'mind')
        
        if points is None:
            return jsonify({'error': 'Points value is required'}), 400
        
        if not isinstance(points, (int, float)) or points <= 0:
            return jsonify({'error': 'Points must be a positive number'}), 400
        
        if task_type not in ['mind', 'body', 'goal']:
            return jsonify({'error': 'Invalid task_type. Must be mind, body, or goal'}), 400
        
        result = add_earned_points(user_id, float(points), task_type)
        
        if result is None:
            return jsonify({'error': 'User profile not found'}), 404
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def subtract_points(user_id, data):
    """Subtract earned points from a user's profile.
    
    Args:
        user_id (str): The user's ID.
        data (dict): Request data containing points and task_type.
    
    Returns:
        tuple: JSON response with updated points and status code.
    """
    try:
        points = data.get('points')
        task_type = data.get('task_type', 'mind')
        
        if points is None:
            return jsonify({'error': 'Points value is required'}), 400
        
        if not isinstance(points, (int, float)) or points <= 0:
            return jsonify({'error': 'Points must be a positive number'}), 400
        
        if task_type not in ['mind', 'body', 'goal']:
            return jsonify({'error': 'Invalid task_type. Must be mind, body, or goal'}), 400
        
        result = subtract_earned_points(user_id, float(points), task_type)
        
        if result is None:
            return jsonify({'error': 'User profile not found'}), 404
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def recalculate_points(user_id):
    """Recalculate all points for a user.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        tuple: JSON response with complete points summary and status code.
    """
    try:
        result = recalculate_all_points(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
