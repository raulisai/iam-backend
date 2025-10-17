"""Profile controller for handling user profile operations."""
from flask import jsonify, request
from services.profile_service import (
    get_profile_by_user_id,
    create_profile,
    update_profile,
    delete_profile,
    add_goal_points
)


def get_user_profile():
    """Get the authenticated user's profile.
    
    Returns:
        tuple: JSON response with profile data and status code.
    """
    user_id = request.user.get('user_id')
    profile = get_profile_by_user_id(user_id)
    
    if profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify(profile), 200


def create_user_profile(data):
    """Create a new profile for the authenticated user.
    
    Args:
        data (dict): Profile data.
    
    Returns:
        tuple: JSON response with created profile and status code.
    """
    user_id = request.user.get('user_id')
    
    # Check if profile already exists
    existing_profile = get_profile_by_user_id(user_id)
    if existing_profile:
        return jsonify({
            'error': 'Profile already exists',
            'message': 'User already has a profile. Use PUT to update instead.',
            'profile': existing_profile
        }), 409
    
    # Add user_id to the profile data
    data['user_id'] = user_id
    
    try:
        profile = create_profile(data)
        
        if profile is None:
            return jsonify({'error': 'Failed to create profile'}), 500
        
        return jsonify(profile), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': f'Failed to create profile: {str(e)}'}), 500


def update_user_profile(data):
    """Update the authenticated user's profile.
    
    Args:
        data (dict): Updated profile data.
    
    Returns:
        tuple: JSON response with updated profile and status code.
    """
    user_id = request.user.get('user_id')
    
    # Remove user_id from update data if present (shouldn't be updated)
    data.pop('user_id', None)
    data.pop('id', None)
    
    profile = update_profile(user_id, data)
    
    if profile is None:
        return jsonify({'error': 'Profile not found or update failed'}), 404
    
    return jsonify(profile), 200


def delete_user_profile():
    """Delete the authenticated user's profile.
    
    Returns:
        tuple: JSON response with deleted profile and status code.
    """
    user_id = request.user.get('user_id')
    
    profile = delete_profile(user_id)
    
    if profile is None:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify(profile), 200


def add_goal_points_to_profile(data):
    """Add points to user profile from a completed goal task.
    
    Args:
        data (dict): Request data containing task_occurrence_id.
    
    Returns:
        tuple: JSON response with updated profile and points details.
    """
    user_id = request.user.get('user_id')
    task_occurrence_id = data.get('task_occurrence_id')
    
    if not task_occurrence_id:
        return jsonify({'error': 'task_occurrence_id is required'}), 400
    
    result = add_goal_points(user_id, task_occurrence_id)
    
    if result is None:
        return jsonify({'error': 'Failed to add points. Task occurrence not found or profile not found.'}), 404
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result), 200
