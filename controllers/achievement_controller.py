"""Achievement controller for handling achievement operations."""
from flask import jsonify, request
from services.achievement_service import (
    get_user_achievements,
    get_achievement_by_id,
    create_achievement,
    delete_achievement
)


def get_my_achievements():
    """Get authenticated user's achievements.
    
    Returns:
        tuple: JSON response with achievements and status code.
    """
    user_id = request.user.get('user_id')
    achievements = get_user_achievements(user_id)
    return jsonify(achievements), 200


def award_achievement(data):
    """Award a new achievement to the authenticated user.
    
    Args:
        data (dict): Achievement data.
    
    Returns:
        tuple: JSON response with created achievement and status code.
    """
    user_id = request.user.get('user_id')
    
    if 'key' not in data:
        return jsonify({'error': 'key is required'}), 400
    
    data['user_id'] = user_id
    
    achievement = create_achievement(data)
    
    if achievement is None:
        return jsonify({'error': 'Failed to create achievement or already exists'}), 500
    
    return jsonify(achievement), 201


def delete_achievement_by_id(achievement_id):
    """Delete an achievement.
    
    Args:
        achievement_id (str): Achievement ID.
    
    Returns:
        tuple: JSON response with deleted achievement and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify achievement belongs to user
    achievement = get_achievement_by_id(achievement_id)
    if achievement is None:
        return jsonify({'error': 'Achievement not found'}), 404
    
    if achievement.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted = delete_achievement(achievement_id)
    
    if deleted is None:
        return jsonify({'error': 'Failed to delete achievement'}), 500
    
    return jsonify(deleted), 200
