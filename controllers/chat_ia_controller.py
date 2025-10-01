"""Chat IA controller for handling chat session and message operations."""
from flask import jsonify, request
from datetime import datetime
from services.chat_ia_service import (
    get_user_chat_sessions,
    get_chat_session_by_id,
    create_chat_session,
    update_chat_session,
    delete_chat_session,
    get_session_messages,
    create_message,
    delete_message
)


def get_my_chat_sessions():
    """Get authenticated user's chat sessions.
    
    Returns:
        tuple: JSON response with sessions and status code.
    """
    user_id = request.user.get('user_id')
    sessions = get_user_chat_sessions(user_id)
    return jsonify(sessions), 200


def get_chat_session(session_id):
    """Get chat session by ID.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        tuple: JSON response with session and status code.
    """
    session = get_chat_session_by_id(session_id)
    
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    
    user_id = request.user.get('user_id')
    if session.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(session), 200


def create_new_chat_session(data):
    """Create a new chat session.
    
    Args:
        data (dict): Session data.
    
    Returns:
        tuple: JSON response with created session and status code.
    """
    user_id = request.user.get('user_id')
    data['user_id'] = user_id
    
    session = create_chat_session(data)
    
    if session is None:
        return jsonify({'error': 'Failed to create session'}), 500
    
    return jsonify(session), 201


def update_chat_session_data(session_id, data):
    """Update a chat session.
    
    Args:
        session_id (str): Session ID.
        data (dict): Updated data.
    
    Returns:
        tuple: JSON response with updated session and status code.
    """
    user_id = request.user.get('user_id')
    
    session = get_chat_session_by_id(session_id)
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    
    if session.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('created_at', None)
    
    updated_session = update_chat_session(session_id, data)
    
    if updated_session is None:
        return jsonify({'error': 'Update failed'}), 500
    
    return jsonify(updated_session), 200


def delete_chat_session_by_id(session_id):
    """Delete a chat session.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        tuple: JSON response with deleted session and status code.
    """
    user_id = request.user.get('user_id')
    
    session = get_chat_session_by_id(session_id)
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    
    if session.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted_session = delete_chat_session(session_id)
    
    if deleted_session is None:
        return jsonify({'error': 'Failed to delete session'}), 500
    
    return jsonify(deleted_session), 200


def get_messages(session_id):
    """Get all messages in a chat session.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        tuple: JSON response with messages and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify session belongs to user
    session = get_chat_session_by_id(session_id)
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    
    if session.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    messages = get_session_messages(session_id)
    return jsonify(messages), 200


def create_new_message(session_id, data):
    """Create a new message in a chat session.
    
    Args:
        session_id (str): Session ID.
        data (dict): Message data.
    
    Returns:
        tuple: JSON response with created message and status code.
    """
    user_id = request.user.get('user_id')
    
    # Verify session belongs to user
    session = get_chat_session_by_id(session_id)
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    
    if session.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'role' not in data or 'content' not in data:
        return jsonify({'error': 'role and content are required'}), 400
    
    data['session_id'] = session_id
    
    message = create_message(data)
    
    if message is None:
        return jsonify({'error': 'Failed to create message'}), 500
    
    # Update session's last_message_at
    update_chat_session(session_id, {'last_message_at': datetime.utcnow().isoformat()})
    
    return jsonify(message), 201


def delete_message_by_id(message_id):
    """Delete a chat message.
    
    Args:
        message_id (str): Message ID.
    
    Returns:
        tuple: JSON response with deleted message and status code.
    """
    # Note: This is a simplified version. In production, you'd want to verify
    # the message belongs to a session owned by the user
    deleted_message = delete_message(message_id)
    
    if deleted_message is None:
        return jsonify({'error': 'Message not found'}), 404
    
    return jsonify(deleted_message), 200
