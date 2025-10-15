"""Notification routes for FCM token management and push notifications."""
from flask import Blueprint, request
from controllers.notification_controller import (
    register_device_token,
    get_user_tokens,
    remove_device_token,
    send_push_notification,
    send_bulk_notification,
    list_device_tokens
)
from middleware.auth_middleware import token_required

# Create Blueprint for notification routes
notification_routes = Blueprint('notification', __name__)


@notification_routes.route('/api/notification/register-token', methods=['POST'])
@token_required
def register_token(current_user):
    """
    Register or update a device token for push notifications.
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Device token registration data
        required: true
        schema:
          type: object
          required:
            - token
          properties:
            token:
              type: string
              description: FCM device token
              example: "dQw4w9WgXcQ:APA91bHun4M..."
            platform:
              type: string
              description: Device platform
              enum: [android, ios, web]
              default: android
              example: "android"
            device_info:
              type: object
              description: Additional device information
              properties:
                model:
                  type: string
                  example: "Pixel 6"
                os_version:
                  type: string
                  example: "Android 13"
                app_version:
                  type: string
                  example: "1.0.0"
    responses:
      201:
        description: Token registered successfully
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Device token registered successfully"
            data:
              type: object
      400:
        description: Invalid request
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    payload = request.get_json() or {}
    token = payload.get('token')
    platform = payload.get('platform', 'android')
    device_info = payload.get('device_info')
    
    # Get user_id from JWT token (current_user is set by @token_required)
    user_id = current_user.get('user_id')
    
    return register_device_token(user_id, token, platform, device_info)


@notification_routes.route('/api/notification/tokens', methods=['GET'])
@token_required
def get_tokens(current_user):
    """
    Get all active device tokens for the authenticated user.
    ---
    tags:
      - Notifications
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: List of active tokens
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            count:
              type: integer
              example: 2
            data:
              type: array
              items:
                type: object
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    user_id = current_user.get('user_id')
    return get_user_tokens(user_id)


@notification_routes.route('/api/notification/remove-token', methods=['POST'])
@token_required
def remove_token(current_user):
    """
    Deactivate or delete a device token.
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Token removal data
        required: true
        schema:
          type: object
          required:
            - token
          properties:
            token:
              type: string
              description: FCM device token to remove
              example: "dQw4w9WgXcQ:APA91bHun4M..."
            hard_delete:
              type: boolean
              description: If true, permanently delete; otherwise deactivate
              default: false
              example: false
    responses:
      200:
        description: Token removed successfully
      400:
        description: Invalid request
      401:
        description: Unauthorized
      404:
        description: Token not found
      500:
        description: Server error
    """
    payload = request.get_json() or {}
    token = payload.get('token')
    hard_delete = payload.get('hard_delete', False)
    
    return remove_device_token(token, hard_delete)


@notification_routes.route('/api/notification/send', methods=['POST'])
@token_required
def send_notification(current_user):
    """
    Send a push notification to a specific user.
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Notification data
        required: true
        schema:
          type: object
          required:
            - user_id
            - title
            - body
          properties:
            user_id:
              type: string
              description: Target user ID
              example: "123e4567-e89b-12d3-a456-426614174000"
            title:
              type: string
              description: Notification title
              example: "Task Reminder"
            body:
              type: string
              description: Notification body
              example: "Don't forget to complete your daily tasks!"
            data:
              type: object
              description: Additional data payload
              example:
                task_id: "456"
                type: "reminder"
    responses:
      200:
        description: Notification sent successfully
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Notification sent"
            data:
              type: object
      400:
        description: Invalid request
      401:
        description: Unauthorized
      404:
        description: No active tokens found
      500:
        description: Server error
    """
    payload = request.get_json() or {}
    user_id = payload.get('user_id')
    title = payload.get('title')
    body = payload.get('body')
    data = payload.get('data')
    
    return send_push_notification(user_id, title, body, data)


@notification_routes.route('/api/notification/send-bulk', methods=['POST'])
@token_required
def send_bulk(current_user):
    """
    Send a push notification to multiple users.
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Bulk notification data
        required: true
        schema:
          type: object
          required:
            - user_ids
            - title
            - body
          properties:
            user_ids:
              type: array
              description: List of target user IDs
              items:
                type: string
              example: ["123e4567-e89b-12d3-a456-426614174000", "789e0123-e45b-67c8-d901-234567890abc"]
            title:
              type: string
              description: Notification title
              example: "System Announcement"
            body:
              type: string
              description: Notification body
              example: "New features are now available!"
            data:
              type: object
              description: Additional data payload
              example:
                type: "announcement"
    responses:
      200:
        description: Bulk notification sent
      400:
        description: Invalid request
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    payload = request.get_json() or {}
    user_ids = payload.get('user_ids')
    title = payload.get('title')
    body = payload.get('body')
    data = payload.get('data')
    
    return send_bulk_notification(user_ids, title, body, data)


@notification_routes.route('/api/notification/tokens/all', methods=['GET'])
@token_required
def list_all_tokens(current_user):
    """
    List all device tokens with optional filters (admin endpoint).
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: query
        name: user_id
        type: string
        description: Filter by user ID
      - in: query
        name: platform
        type: string
        enum: [android, ios, web]
        description: Filter by platform
      - in: query
        name: is_active
        type: boolean
        description: Filter by active status
    responses:
      200:
        description: List of device tokens
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    user_id = request.args.get('user_id')
    platform = request.args.get('platform')
    is_active = request.args.get('is_active')
    
    # Convert is_active to boolean if provided
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    
    return list_device_tokens(user_id, platform, is_active)
