"""Chat IA routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.chat_ia_controller import (
    get_my_chat_sessions,
    get_chat_session,
    create_new_chat_session,
    update_chat_session_data,
    delete_chat_session_by_id,
    get_messages,
    create_new_message,
    delete_message_by_id
)

chat_ia_routes = Blueprint('chat_ia', __name__, url_prefix='/api/chat')


# Session endpoints
@chat_ia_routes.route('/sessions', methods=['GET', 'OPTIONS'])
@token_required
def get_sessions():
    """Get all chat IA sessions for authenticated user.
    ---
    tags:
      - Chat IA
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: List of chat sessions
        schema:
          type: array
          items:
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
                example: "Conversación sobre meditación"
                nullable: true
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
    return get_my_chat_sessions()


@chat_ia_routes.route('/sessions/<session_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_session(session_id):
    """Get specific chat session by ID.
    ---
    tags:
      - Chat IA
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
    responses:
      200:
        description: Chat session data
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
              example: "Conversación sobre meditación"
              nullable: true
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
    return get_chat_session(session_id)


@chat_ia_routes.route('/sessions', methods=['POST'])
@token_required
def create_session():
    """Create new chat IA session.
    ---
    tags:
      - Chat IA
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Chat session data (optional)
        required: false
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Conversación sobre meditación"
              description: Optional session title
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
              nullable: true
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
    data = request.get_json() or {}
    return create_new_chat_session(data)


@chat_ia_routes.route('/sessions/<session_id>', methods=['PUT'])
@token_required
def update_session(session_id):
    """Update chat session.
    ---
    tags:
      - Chat IA
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
        description: Updated session data
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Conversación actualizada"
    responses:
      200:
        description: Chat session updated successfully
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
              nullable: true
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      400:
        description: Invalid request
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
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_chat_session_data(session_id, data)


@chat_ia_routes.route('/sessions/<session_id>', methods=['DELETE'])
@token_required
def delete_session(session_id):
    """Delete chat session and all its messages.
    ---
    tags:
      - Chat IA
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
        description: Chat session ID to delete
    responses:
      200:
        description: Chat session deleted successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
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
    return delete_chat_session_by_id(session_id)


# Message endpoints
@chat_ia_routes.route('/sessions/<session_id>/messages', methods=['GET', 'OPTIONS'])
@token_required
def get_session_messages(session_id):
    """Get all messages in a chat session.
    ---
    tags:
      - Chat IA
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
    responses:
      200:
        description: List of messages in the session
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              session_id:
                type: string
                format: uuid
              role:
                type: string
                enum: ["user", "assistant"]
                example: "user"
                description: Who sent the message
              content:
                type: string
                example: "¿Cómo puedo mejorar mi meditación?"
                description: Message content
              created_at:
                type: string
                format: date-time
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
    return get_messages(session_id)


@chat_ia_routes.route('/sessions/<session_id>/messages', methods=['POST'])
@token_required
def create_message(session_id):
    """Create new message in a chat session.
    ---
    tags:
      - Chat IA
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
            - role
            - content
          properties:
            role:
              type: string
              enum: ["user", "assistant"]
              example: "user"
              description: Who is sending the message
            content:
              type: string
              example: "¿Cómo puedo mejorar mi meditación?"
              description: Message content
    responses:
      201:
        description: Message created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            session_id:
              type: string
              format: uuid
            role:
              type: string
              enum: ["user", "assistant"]
            content:
              type: string
            created_at:
              type: string
              format: date-time
      400:
        description: Invalid request or missing required fields
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
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_message(session_id, data)


@chat_ia_routes.route('/messages/<message_id>', methods=['DELETE'])
@token_required
def delete_message(message_id):
    """Delete chat message.
    ---
    tags:
      - Chat IA
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: message_id
        in: path
        required: true
        type: string
        format: uuid
        description: Message ID to delete
    responses:
      200:
        description: Message deleted successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Message session belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Message not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_message_by_id(message_id)
