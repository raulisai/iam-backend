"""Body task routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.body_task_controller import (
    get_my_body_tasks,
    get_body_task,
    create_new_body_task,
    update_body_task_data,
    complete_task,
    delete_body_task_by_id
)

body_task_routes = Blueprint('body_tasks', __name__, url_prefix='/api/tasks/body')


@body_task_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_tasks():
    """Get all body tasks for authenticated user.
    ---
    tags:
      - Body Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: status
        type: string
        required: false
        description: Filter by task status
        enum: ["pending", "completed", "failed", "in_progress"]
        example: "pending"
    responses:
      200:
        description: List of body tasks
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
              template_id:
                type: string
                format: uuid
              created_by:
                type: string
                enum: ["user", "bot"]
                example: "user"
              status:
                type: string
                enum: ["pending", "completed", "failed", "in_progress"]
                example: "pending"
              scheduled_at:
                type: string
                format: date-time
                example: "2025-10-01T10:00:00Z"
              completed_at:
                type: string
                format: date-time
                nullable: true
              xp_awarded:
                type: integer
                example: 15
              params:
                type: object
                example: {"reps": 10, "sets": 3, "weight": 20}
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
    return get_my_body_tasks()


@body_task_routes.route('/<task_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_task(task_id):
    """Get specific body task by ID.
    ---
    tags:
      - Body Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: string
        format: uuid
        description: Body task ID
    responses:
      200:
        description: Body task data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            template_id:
              type: string
              format: uuid
            created_by:
              type: string
              enum: ["user", "bot"]
              example: "user"
            status:
              type: string
              enum: ["pending", "completed", "failed", "in_progress"]
              example: "pending"
            scheduled_at:
              type: string
              format: date-time
              example: "2025-10-01T10:00:00Z"
            completed_at:
              type: string
              format: date-time
              nullable: true
            xp_awarded:
              type: integer
              example: 15
            params:
              type: object
              example: {"reps": 10, "sets": 3, "weight": 20}
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Task belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Body task not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_body_task(task_id)


@body_task_routes.route('/', methods=['POST'])
@token_required
def create_task():
    """Create new body task.
    ---
    tags:
      - Body Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Body task data
        required: true
        schema:
          type: object
          required:
            - template_id
            - scheduled_at
          properties:
            template_id:
              type: string
              format: uuid
              example: "550e8400-e29b-41d4-a716-446655440000"
              description: ID of the task template
            created_by:
              type: string
              enum: ["user", "bot"]
              default: "user"
              example: "user"
              description: Who created this task
            status:
              type: string
              enum: ["pending", "completed", "failed", "in_progress"]
              default: "pending"
              example: "pending"
              description: Initial task status
            scheduled_at:
              type: string
              format: date-time
              example: "2025-10-01T10:00:00Z"
              description: When the task is scheduled
            params:
              type: object
              example: {"reps": 10, "sets": 3, "weight": 20}
              description: Custom parameters for this task
    responses:
      201:
        description: Body task created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            template_id:
              type: string
              format: uuid
            created_by:
              type: string
              enum: ["user", "bot"]
            status:
              type: string
              enum: ["pending", "completed", "failed", "in_progress"]
            scheduled_at:
              type: string
              format: date-time
            completed_at:
              type: string
              format: date-time
              nullable: true
            xp_awarded:
              type: integer
            params:
              type: object
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
    return create_new_body_task(data)


@body_task_routes.route('/<task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    """Update body task.
    ---
    tags:
      - Body Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: string
        format: uuid
        description: Body task ID
      - in: body
        name: body
        description: Updated task data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              enum: ["pending", "completed", "failed", "in_progress"]
              example: "in_progress"
            scheduled_at:
              type: string
              format: date-time
              example: "2025-10-01T14:00:00Z"
            params:
              type: object
              example: {"reps": 12, "sets": 4, "weight": 25}
    responses:
      200:
        description: Body task updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            template_id:
              type: string
              format: uuid
            created_by:
              type: string
              enum: ["user", "bot"]
            status:
              type: string
              enum: ["pending", "completed", "failed", "in_progress"]
            scheduled_at:
              type: string
              format: date-time
            completed_at:
              type: string
              format: date-time
              nullable: true
            xp_awarded:
              type: integer
            params:
              type: object
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
        description: Forbidden - Task belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Body task not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_body_task_data(task_id, data)


@body_task_routes.route('/<task_id>/complete', methods=['POST'])
@token_required
def complete(task_id):
    """Mark body task as completed and award XP.
    ---
    tags:
      - Body Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: string
        format: uuid
        description: Body task ID to complete
    responses:
      200:
        description: Task completed successfully and XP awarded
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            template_id:
              type: string
              format: uuid
            status:
              type: string
              enum: ["completed"]
              example: "completed"
            completed_at:
              type: string
              format: date-time
            xp_awarded:
              type: integer
              example: 15
              description: XP points awarded for completion
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Task belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Body task not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      400:
        description: Task already completed
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return complete_task(task_id)


@body_task_routes.route('/<task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    """Delete body task.
    ---
    tags:
      - Body Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: string
        format: uuid
        description: Body task ID to delete
    responses:
      200:
        description: Body task deleted successfully
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
        description: Forbidden - Task belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Body task not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_body_task_by_id(task_id)
