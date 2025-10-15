"""Notification service for FCM token and push notification operations."""
from lib.db import get_supabase
from lib.firebase_client import send_message_to_token, send_alarma_to_token
from datetime import datetime


def upsert_device_token(user_id, token, platform="android", device_info=None):
    """Register or update a device token for a user (upsert operation).
    
    Args:
        user_id (str): User ID.
        token (str): FCM device token.
        platform (str, optional): Platform type ('android', 'ios', 'web'). Defaults to 'android'.
        device_info (dict, optional): Additional device information.
    
    Returns:
        dict: Upserted device token record.
    """
    supabase = get_supabase()
    device_info = device_info or {}
    
    data = {
        "user_id": user_id,
        "token": token,
        "platform": platform,
        "device_info": device_info,
        "is_active": True,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Upsert: if token exists, update it; otherwise insert
    res = supabase.from_('device_tokens').upsert(data, on_conflict='token').execute()
    return res.data[0] if res.data else None


def get_user_active_tokens(user_id):
    """Get all active device tokens for a user.
    
    Args:
        user_id (str): User ID.
    
    Returns:
        list: List of active device token records.
    """
    supabase = get_supabase()
    res = supabase.from_('device_tokens').select('*').eq('user_id', user_id).eq('is_active', True).execute()
    return res.data


def deactivate_device_token(token):
    """Deactivate a device token.
    
    Args:
        token (str): FCM device token.
    
    Returns:
        dict: Updated device token record.
    """
    supabase = get_supabase()
    res = supabase.from_('device_tokens').update({
        'is_active': False,
        'updated_at': datetime.utcnow().isoformat()
    }).eq('token', token).execute()
    return res.data[0] if res.data else None


def delete_device_token(token):
    """Delete a device token.
    
    Args:
        token (str): FCM device token.
    
    Returns:
        dict: Deleted device token record.
    """
    supabase = get_supabase()
    res = supabase.from_('device_tokens').delete().eq('token', token).execute()
    return res.data[0] if res.data else None


def send_notification_to_user(user_id, title, body, data=None):
    """Send a push notification to all active devices of a user.
    
    Args:
        user_id (str): User ID.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    
    Returns:
        dict: Results with success/failure information for each token.
    """
    # Get all active tokens for the user
    tokens_data = get_user_active_tokens(user_id)
    
    if not tokens_data:
        return {
            "status": "no_tokens",
            "message": "No active tokens found for user",
            "results": []
        }
    
    results = []
    
    # Try to send to each token
    for token_record in tokens_data:
        token = token_record['token']
        try:
            msg_id = send_message_to_token(token, title, body, data)
            results.append({
                "token": token,
                "status": "sent",
                "message_id": msg_id
            })
        except Exception as e:
            error_msg = str(e)
            results.append({
                "token": token,
                "status": "error",
                "error": error_msg
            })
            
            # If token is invalid or unregistered, deactivate it
            if "not-found" in error_msg.lower() or "invalid" in error_msg.lower() or "unregistered" in error_msg.lower():
                try:
                    deactivate_device_token(token)
                    print(f"Deactivated invalid token: {token}")
                except Exception as deactivate_error:
                    print(f"Failed to deactivate token: {str(deactivate_error)}")
    
    success_count = sum(1 for r in results if r['status'] == 'sent')
    failure_count = sum(1 for r in results if r['status'] == 'error')
    
    return {
        "status": "completed",
        "success_count": success_count,
        "failure_count": failure_count,
        "results": results
    }


def send_notification_to_multiple_users(user_ids, title, body, data=None):
    """Send a push notification to multiple users.
    
    Args:
        user_ids (list): List of user IDs.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    
    Returns:
        dict: Aggregated results for all users.
    """
    all_results = []
    total_success = 0
    total_failure = 0
    
    for user_id in user_ids:
        result = send_notification_to_user(user_id, title, body, data)
        all_results.append({
            "user_id": user_id,
            "result": result
        })
        
        if result['status'] == 'completed':
            total_success += result['success_count']
            total_failure += result['failure_count']
    
    return {
        "status": "completed",
        "total_users": len(user_ids),
        "total_success": total_success,
        "total_failure": total_failure,
        "user_results": all_results
    }


def send_alarm_to_user(user_id, mensaje, title=None, body=None, additional_data=None):
    """Send an alarm data-only message to all active devices of a user.
    Uses data-only messages (no notification field) to ensure onMessageReceived 
    is always triggered, even when the app is in background or closed.
    
    Args:
        user_id (str): User ID.
        mensaje (str): Alarm message.
        title (str, optional): Title for notification display in app. Defaults to "Alarma".
        body (str, optional): Body for notification display in app. Defaults to mensaje.
        additional_data (dict, optional): Additional data payload.
    
    Returns:
        dict: Results with success/failure information for each token.
    """
    # Get all active tokens for the user
    tokens_data = get_user_active_tokens(user_id)
    
    if not tokens_data:
        return {
            "status": "no_tokens",
            "message": "No active tokens found for user",
            "results": []
        }
    
    results = []
    
    # Set default title and body if not provided
    notification_title = title or "Alarma"
    notification_body = body or mensaje
    
    # Prepare data-only payload - NO notification field
    # This ensures onMessageReceived is called even in background/closed state
    data_payload = {
        "tipo": "alarma",
        "mensaje": mensaje
    }
    
    # Merge with any additional data
    if additional_data:
        data_payload.update(additional_data)
    
    # Try to send to each token
    for token_record in tokens_data:
        token = token_record['token']
        try:
            # Use send_alarma_to_token to send a data-only message
            msg_id = send_alarma_to_token(
                token,
                data_payload
            )
            results.append({
                "token": token,
                "status": "sent",
                "message_id": msg_id
            })
        except Exception as e:
            error_msg = str(e)
            results.append({
                "token": token,
                "status": "error",
                "error": error_msg
            })
            
            # If token is invalid or unregistered, deactivate it
            if ("not found" in error_msg.lower() or 
                "not-found" in error_msg.lower() or 
                "invalid" in error_msg.lower() or 
                "unregistered" in error_msg.lower() or
                "entity was not found" in error_msg.lower()):
                try:
                    deactivate_device_token(token)
                    print(f"Deactivated invalid token: {token}")
                except Exception as deactivate_error:
                    print(f"Failed to deactivate token: {str(deactivate_error)}")
    
    success_count = sum(1 for r in results if r['status'] == 'sent')
    failure_count = sum(1 for r in results if r['status'] == 'error')
    
    return {
        "status": "completed",
        "success_count": success_count,
        "failure_count": failure_count,
        "results": results
    }


def get_all_device_tokens(user_id=None, platform=None, is_active=None):
    """Get device tokens with optional filters.
    
    Args:
        user_id (str, optional): Filter by user ID.
        platform (str, optional): Filter by platform.
        is_active (bool, optional): Filter by active status.
    
    Returns:
        list: List of device token records.
    """
    supabase = get_supabase()
    query = supabase.from_('device_tokens').select('*')
    
    if user_id is not None:
        query = query.eq('user_id', user_id)
    
    if platform is not None:
        query = query.eq('platform', platform)
    
    if is_active is not None:
        query = query.eq('is_active', is_active)
    
    res = query.order('created_at', desc=True).execute()
    return res.data
