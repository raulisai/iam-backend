"""Goal Task Recommendation Controller - Handle AI-powered task recommendations for goals."""
from flask import jsonify, request
from services.goal_task_recommendation_service import generate_goal_task_recommendations


def get_goal_task_recommendations(goal_id):
    """Get AI-powered task recommendations for a specific goal.
    
    Args:
        goal_id (str): Goal ID from URL parameter.
    
    Returns:
        tuple: JSON response with recommendations and status code.
    """
    user_id = request.user.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID not found'}), 401
    
    # Get query parameters
    use_ai = request.args.get('use_ai', 'true').lower() == 'true'
    count = int(request.args.get('count', 5))
    count = max(1, min(count, 10))  # Limit between 1 and 10
    
    # Get additional context from request body if provided
    additional_context = None
    if request.is_json:
        data = request.get_json()
        additional_context = data.get('context')
    
    try:
        result = generate_goal_task_recommendations(
            goal_id=goal_id,
            user_id=user_id,
            count=count,
            use_ai=use_ai,
            additional_context=additional_context
        )
        
        if not result.get('success', True):
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid parameters: {str(e)}'
        }), 400
    except (RuntimeError, KeyError, TypeError) as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate recommendations: {str(e)}'
        }), 500
