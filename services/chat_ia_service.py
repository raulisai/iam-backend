"""Chat IA service for chat session and message operations."""
from lib.db import get_supabase


def get_user_chat_sessions(user_id):
    """Get all chat sessions for a user.
    
    Args:
        user_id (str): User ID.
    
    Returns:
        list: List of chat sessions.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_sessions').select('*').eq('user_id', user_id).order('last_message_at', desc=True).execute()
    return res.data


def get_chat_session_by_id(session_id):
    """Get chat session by ID.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        dict: Session data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_sessions').select('*').eq('id', session_id).execute()
    return res.data[0] if res.data else None


def create_chat_session(data):
    """Create a new chat session.
    
    Args:
        data (dict): Session data.
    
    Returns:
        dict: Created session.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_sessions').insert(data).execute()
    return res.data[0] if res.data else None


def update_chat_session(session_id, data):
    """Update a chat session.
    
    Args:
        session_id (str): Session ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated session.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_sessions').update(data).eq('id', session_id).execute()
    return res.data[0] if res.data else None


def delete_chat_session(session_id):
    """Delete a chat session.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        dict: Deleted session.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_sessions').delete().eq('id', session_id).execute()
    return res.data[0] if res.data else None


def get_session_messages(session_id):
    """Get all messages in a chat session.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        list: List of messages.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_messages').select('*').eq('session_id', session_id).order('created_at', desc=False).execute()
    return res.data


def create_message(data):
    """Create a new chat message.
    
    Args:
        data (dict): Message data.
    
    Returns:
        dict: Created message.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_messages').insert(data).execute()
    return res.data[0] if res.data else None


def delete_message(message_id):
    """Delete a chat message.
    
    Args:
        message_id (str): Message ID.
    
    Returns:
        dict: Deleted message.
    """
    supabase = get_supabase()
    res = supabase.from_('chat_ia_messages').delete().eq('id', message_id).execute()
    return res.data[0] if res.data else None
