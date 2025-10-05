"""Failure routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.failure_controller import (
    get_my_failures,
    create_failure_record,
    delete_failure_by_id
)

failure_routes = Blueprint('failures', __name__, url_prefix='/api/failures')


@failure_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_failures():
    """Get all failure records for authenticated user.
    ---
    tags:
      - Failures
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: severity
        type: string
        required: false
        description: Filter by failure severity
        enum: ["minor", "major", "critical"]
        example: "major"
    responses:
      200:
        description: List of failure records
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
              task_table:
                type: string
                enum: ["tasks_mind", "tasks_body"]
                example: "tasks_mind"
              task_id:
                type: string
                format: uuid
              reason:
                type: string
                example: "No tuve tiempo debido a trabajo"
              severity:
                type: string
                enum: ["minor", "major", "critical"]
                example: "minor"
              notes:
                type: string
                example: "Reprogramar para mañana"
                nullable: true
              title:
                type: string
                example: "Falta de gestión del tiempo"
                nullable: true
              rootCause:
                type: string
                example: "Sobrecarga de trabajo sin planificación adecuada"
                nullable: true
              prevention:
                type: string
                example: "Implementar técnica Pomodoro y planificación semanal"
                nullable: true
              created_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_my_failures()


@failure_routes.route('/', methods=['POST'])
@token_required
def create_failure():
    """Create new failure record.
    ---
    tags:
      - Failures
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Failure record data
        required: true
        schema:
          type: object
          required:
            - task_table
            - task_id
            - reason
          properties:
            task_table:
              type: string
              enum: ["tasks_mind", "tasks_body"]
              example: "tasks_mind"
              description: Which task table this failure belongs to
            task_id:
              type: string
              format: uuid
              example: "550e8400-e29b-41d4-a716-446655440000"
              description: ID of the failed task
            reason:
              type: string
              example: "No tuve tiempo debido a trabajo"
              description: Reason for the failure
            severity:
              type: string
              enum: ["minor", "major", "critical"]
              example: "minor"
              default: "minor"
              description: Severity level of the failure
            notes:
              type: string
              example: "Reprogramar para mañana"
              description: Optional additional notes
            title:
              type: string
              example: "Falta de gestión del tiempo"
              description: Title or summary of the failure
            rootCause:
              type: string
              example: "Sobrecarga de trabajo sin planificación adecuada"
              description: Root cause analysis of the failure
            prevention:
              type: string
              example: "Implementar técnica Pomodoro y planificación semanal"
              description: Prevention strategy for future occurrences
    responses:
      201:
        description: Failure record created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            task_table:
              type: string
              enum: ["tasks_mind", "tasks_body"]
            task_id:
              type: string
              format: uuid
            reason:
              type: string
            severity:
              type: string
              enum: ["minor", "major", "critical"]
            notes:
              type: string
              nullable: true
            title:
              type: string
              nullable: true
            rootCause:
              type: string
              nullable: true
            prevention:
              type: string
              nullable: true
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
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_failure_record(data)


@failure_routes.route('/<failure_id>', methods=['DELETE'])
@token_required
def delete_failure(failure_id):
    """Delete failure record.
    ---
    tags:
      - Failures
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: failure_id
        in: path
        required: true
        type: string
        format: uuid
        description: Failure record ID to delete
    responses:
      200:
        description: Failure record deleted successfully
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
        description: Forbidden - Failure record belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Failure record not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_failure_by_id(failure_id)
