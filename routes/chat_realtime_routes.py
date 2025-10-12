"""Chat Realtime routes - Streaming chat similar to ChatGPT."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.chat_realtime_controller import (
    chat_stream,
    create_chat_stream_session
)

chat_realtime_routes = Blueprint('chat_realtime', __name__, url_prefix='/api/chat/realtime')


@chat_realtime_routes.route('/sessions', methods=['POST', 'OPTIONS'])
@token_required
def create_session():
    """Create new streaming chat session.
    ---
    tags:
      - Chat Realtime
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Session data
        required: false
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Conversación en tiempo real"
              description: Optional session title
            initial_message:
              type: string
              example: "Hola, ¿cómo estás?"
              description: Optional initial message
    responses:
      201:
        description: Chat session created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            title:
              type: string
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json() or {}
    return create_chat_stream_session(data)


@chat_realtime_routes.route('/sessions/<session_id>/stream', methods=['POST', 'OPTIONS'])
@token_required
def stream_message(session_id):
    """Send message and receive streaming response (like ChatGPT).
    ---
    tags:
      - Chat Realtime
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: session_id
        in: path
        required: true
        type: string
        format: uuid
        description: Chat session ID
      - in: body
        name: body
        description: Message data
        required: true
        schema:
          type: object
          required:
            - content
          properties:
            content:
              type: string
              example: "¿Cómo puedo mejorar mi productividad?"
              description: User message content
    produces:
      - text/event-stream
    responses:
      200:
        description: |
          Server-Sent Events stream. Events format:
          
          - **start**: `{"type": "start", "session_id": "uuid"}`
          - **content**: `{"type": "content", "content": "chunk of text"}`
          - **done**: `{"type": "done", "message_id": "uuid", "full_content": "complete response"}`
          - **error**: `{"type": "error", "error": "error message"}`
          
          Example stream:
          ```
          data: {"type": "start", "session_id": "abc-123"}
          
          data: {"type": "content", "content": "Hola"}
          
          data: {"type": "content", "content": ", ¿cómo"}
          
          data: {"type": "content", "content": " estás?"}
          
          data: {"type": "done", "message_id": "msg-456", "full_content": "Hola, ¿cómo estás?"}
          ```
        schema:
          type: string
      400:
        description: Invalid request or missing content
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Session belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Chat session not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return chat_stream(session_id)
