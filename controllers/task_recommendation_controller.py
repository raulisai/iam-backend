"""Task recommendation controller for handling recommendation requests."""
from flask import jsonify, request
from services.task_recommendation_service import (
    generate_task_recommendations,
    generate_mind_task_recommendations,
    generate_body_task_recommendations
)


def get_task_recommendations():
    """Get task recommendations for authenticated user.
    
    Returns:
        tuple: JSON response with recommendations and status code.
    """
    user_id = request.user.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID not found'}), 401
    
    # Check if AI should be used (query parameter)
    use_ai = request.args.get('use_ai', 'false').lower() == 'true'
    
    try:
        result = generate_task_recommendations(user_id, use_ai=use_ai)
        return jsonify(result), 200
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({'error': f'Failed to generate recommendations: {str(e)}'}), 500


def get_mind_task_recommendations():
    """Get mind task recommendations for authenticated user.
    
    Returns:
        tuple: JSON response with mind task recommendations and status code.
    """
    user_id = request.user.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID not found'}), 401
    
    # Check if AI should be used (query parameter)
    use_ai = request.args.get('use_ai', 'false').lower() == 'true'
    # Get count parameter (default 3)
    count = int(request.args.get('count', 3))
    count = max(1, min(count, 10))  # Limit between 1 and 10
    
    try:
        result = generate_mind_task_recommendations(user_id, use_ai=use_ai, count=count)
        return jsonify(result), 200
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({'error': f'Failed to generate mind task recommendations: {str(e)}'}), 500


def get_body_task_recommendations():
    """Get body task recommendations for authenticated user.
    
    Returns:
        tuple: JSON response with body task recommendations and status code.
    """
    user_id = request.user.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID not found'}), 401
    
    # Check if AI should be used (query parameter)
    use_ai = request.args.get('use_ai', 'false').lower() == 'true'
    # Get count parameter (default 3)
    count = int(request.args.get('count', 3))
    count = max(1, min(count, 10))  # Limit between 1 and 10
    
    try:
        result = generate_body_task_recommendations(user_id, use_ai=use_ai, count=count)
        return jsonify(result), 200
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({'error': f'Failed to generate body task recommendations: {str(e)}'}), 500
