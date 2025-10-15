"""Notification controller for handling FCM token registration and push notifications."""
from flask import jsonify
from services.notification_service import (
    upsert_device_token,
    get_user_active_tokens,
    deactivate_device_token,
    delete_device_token,
    send_notification_to_user,
    send_notification_to_multiple_users,
    get_all_device_tokens,
    send_alarm_to_user
)


def register_device_token(user_id, token, platform="android", device_info=None):
    """Register or update a device token for push notifications.
    
    Args:
        user_id (str): User ID.
        token (str): FCM device token.
        platform (str, optional): Platform type.
        device_info (dict, optional): Device information.
    
    Returns:
        tuple: JSON response and status code.
    """
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    try:
        result = upsert_device_token(user_id, token, platform, device_info)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Device token registered successfully',
                'data': result
            }), 201
        else:
            return jsonify({
                'error': 'Failed to register device token'
            }), 500
    
    except Exception as e:
        return jsonify({
            'error': f'Error registering device token: {str(e)}'
        }), 500


def get_user_tokens(user_id):
    """Get all active tokens for a user.
    
    Args:
        user_id (str): User ID.
    
    Returns:
        tuple: JSON response and status code.
    """
    try:
        tokens = get_user_active_tokens(user_id)
        return jsonify({
            'status': 'success',
            'count': len(tokens),
            'data': tokens
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving tokens: {str(e)}'
        }), 500


def remove_device_token(token, hard_delete=False):
    """Deactivate or delete a device token.
    
    Args:
        token (str): FCM device token.
        hard_delete (bool): If True, delete permanently; otherwise deactivate.
    
    Returns:
        tuple: JSON response and status code.
    """
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    try:
        if hard_delete:
            result = delete_device_token(token)
            message = 'Device token deleted successfully'
        else:
            result = deactivate_device_token(token)
            message = 'Device token deactivated successfully'
        
        if result:
            return jsonify({
                'status': 'success',
                'message': message,
                'data': result
            }), 200
        else:
            return jsonify({
                'error': 'Token not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'error': f'Error removing device token: {str(e)}'
        }), 500


def send_push_notification(user_id, title, body, data=None):
    """Send a push notification to a user's devices.
    
    Args:
        user_id (str): User ID.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    
    Returns:
        tuple: JSON response and status code.
    """
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    if not title or not body:
        return jsonify({'error': 'Title and body are required'}), 400
    
    try:
        result = send_notification_to_user(user_id, title, body, data)
        
        if result['status'] == 'no_tokens':
            return jsonify({
                'status': 'warning',
                'message': result['message']
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Notification sent',
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error sending notification: {str(e)}'
        }), 500


def send_bulk_notification(user_ids, title, body, data=None):
    """Send a push notification to multiple users.
    
    Args:
        user_ids (list): List of user IDs.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    
    Returns:
        tuple: JSON response and status code.
    """
    if not user_ids or not isinstance(user_ids, list):
        return jsonify({'error': 'User IDs list is required'}), 400
    
    if not title or not body:
        return jsonify({'error': 'Title and body are required'}), 400
    
    try:
        result = send_notification_to_multiple_users(user_ids, title, body, data)
        
        return jsonify({
            'status': 'success',
            'message': 'Bulk notification sent',
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error sending bulk notification: {str(e)}'
        }), 500


def send_alarm(user_id, mensaje, title=None, body=None, additional_data=None):
    """Send an alarm data-only message to a user's devices.
    
    Args:
        user_id (str): User ID.
        mensaje (str): Alarm message.
        title (str, optional): Title for notification display in app.
        body (str, optional): Body for notification display in app.
        additional_data (dict, optional): Additional data payload.
    
    Returns:
        tuple: JSON response and status code.
    """
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    if not mensaje:
        return jsonify({'error': 'Mensaje is required'}), 400
    
    try:
        result = send_alarm_to_user(user_id, mensaje, title, body, additional_data)
        
        if result['status'] == 'no_tokens':
            return jsonify({
                'status': 'warning',
                'message': result['message']
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Alarm sent',
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error sending alarm: {str(e)}'
        }), 500


def list_device_tokens(user_id=None, platform=None, is_active=None):
    """List device tokens with optional filters.
    
    Args:
        user_id (str, optional): Filter by user ID.
        platform (str, optional): Filter by platform.
        is_active (bool, optional): Filter by active status.
    
    Returns:
        tuple: JSON response and status code.
    """
    try:
        tokens = get_all_device_tokens(user_id, platform, is_active)
        
        return jsonify({
            'status': 'success',
            'count': len(tokens),
            'data': tokens
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error listing device tokens: {str(e)}'
        }), 500
