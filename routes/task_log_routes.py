"""Task log routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.task_log_controller import (
    get_my_task_logs,
    create_log
)

task_log_routes = Blueprint('task_logs', __name__, url_prefix='/api/task-logs')


@task_log_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_logs():
    """Get all task logs for authenticated user.
    ---
    tags:
      - Task Logs
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: task_table
        type: string
        required: false
        description: Filter by task table
        enum: ["tasks_mind", "tasks_body"]
        example: "tasks_mind"
    responses:
      200:
        description: List of task logs
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
              action:
                type: string
                example: "completed"
                description: Action performed on the task
              notes:
                type: string
                example: "Great session"
                nullable: true
              logged_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_my_task_logs()


@task_log_routes.route('/', methods=['POST'])
@token_required
def create_task_log():
    """Create new task log entry.
    ---
    tags:
      - Task Logs
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Task log data
        required: true
        schema:
          type: object
          required:
            - task_table
            - task_id
            - action
          properties:
            task_table:
              type: string
              enum: ["tasks_mind", "tasks_body"]
              example: "tasks_mind"
              description: Which task table this log belongs to
            task_id:
              type: string
              format: uuid
              example: "550e8400-e29b-41d4-a716-446655440000"
              description: ID of the task
            action:
              type: string
              example: "completed"
              description: Action performed (e.g., completed, started, failed)
            notes:
              type: string
              example: "Excellent meditation session"
              description: Optional notes about the log entry
    responses:
      201:
        description: Task log created successfully
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
            action:
              type: string
            notes:
              type: string
              nullable: true
            logged_at:
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
    return create_log(data)
