"""Chat Realtime controller for handling streaming chat conversations."""
from flask import jsonify, request, Response, stream_with_context
import logging
import json
from services.chat_ia_service import (
    get_chat_session_by_id,
    create_chat_session,
    get_session_messages,
    create_message
)
from services.agent_service import get_agent_service

logger = logging.getLogger(__name__)


def stream_chat_response(session_id, user_message_content, _user_id):
    """Generate a streaming response for chat.
    
    Args:
        session_id (str): Session ID.
        user_message_content (str): User's message content.
        _user_id (str): User ID (reserved for future use).
    
    Yields:
        str: Server-Sent Events formatted data.
    """
    try:
        # Get conversation history
        all_messages = get_session_messages(session_id)
        recent_messages = all_messages[-10:] if len(all_messages) > 0 else []
        
        # Build conversation context
        conversation_history = []
        for msg in recent_messages:
            conversation_history.append({
                'role': msg.get('role', 'user'),
                'content': msg.get('content', '')
            })
        
        # Get agent service
        agent_service = get_agent_service()
        
        # Add conversation history to agent
        if conversation_history and session_id not in agent_service.agent.conversations:
            conversation = agent_service.agent.get_or_create_conversation(session_id)
            for msg in conversation_history:
                conversation.add_message(msg['role'], msg['content'])
        
        # Send initial event
        yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"
        
        # Use OpenAI streaming
        try:
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            
            # Build messages for OpenAI
            messages = []
            
            # Add system message
            system_prompt = agent_service.agent.system_prompt or "You are a helpful assistant."
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history
            for msg in conversation_history:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message_content})
            
            # Stream response from OpenAI
            full_response = ""
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=2000
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    
                    # Send content chunk
                    yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
            
            # Save full response to database
            assistant_data = {
                'session_id': session_id,
                'role': 'assistant',
                'content': full_response
            }
            assistant_message = create_message(assistant_data)
            
            # Send completion event with message ID
            yield f"data: {json.dumps({'type': 'done', 'message_id': assistant_message.get('id'), 'full_content': full_response})}\n\n"
            
        except (ValueError, KeyError, IOError) as e:
            logger.error("Error in OpenAI streaming: %s", str(e), exc_info=True)
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            
            # Save error message
            assistant_data = {
                'session_id': session_id,
                'role': 'assistant',
                'content': error_message
            }
            create_message(assistant_data)
            
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
            
    except (ValueError, KeyError, IOError) as e:
        logger.error("Error in stream_chat_response: %s", str(e), exc_info=True)
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"


def chat_stream(session_id):
    """Handle streaming chat endpoint.
    
    Args:
        session_id (str): Session ID.
    
    Returns:
        Response: Streaming response.
    """
    user_id = request.user.get('user_id')
    
    # Verify session belongs to user
    session = get_chat_session_by_id(session_id)
    if session is None:
        return jsonify({'error': 'Session not found'}), 404
    
    if session.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get message from request
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'content is required'}), 400
    
    content = data.get('content')
    
    # Save user message
    user_message_data = {
        'session_id': session_id,
        'role': 'user',
        'content': content
    }
    
    user_message = create_message(user_message_data)
    
    if user_message is None:
        return jsonify({'error': 'Failed to create message'}), 500
    
    # Return streaming response
    return Response(
        stream_with_context(stream_chat_response(session_id, content, user_id)),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )


def create_chat_stream_session(data):
    """Create a new chat session for streaming.
    
    Args:
        data (dict): Session data with optional initial message.
    
    Returns:
        tuple: JSON response with created session and status code.
    """
    user_id = request.user.get('user_id')
    
    # Create session
    session_data = {
        'user_id': user_id,
        'title': data.get('title', 'Nueva conversación')
    }
    
    session = create_chat_session(session_data)
    
    if session is None:
        return jsonify({'error': 'Failed to create session'}), 500
    
    # If there's an initial message, add it
    initial_message = data.get('initial_message')
    if initial_message:
        message_data = {
            'session_id': session['id'],
            'role': 'user',
            'content': initial_message
        }
        create_message(message_data)
    
    return jsonify(session), 201
