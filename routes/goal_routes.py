"""Goal routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.goal_controller import (
    get_my_goals,
    get_goal,
    create_new_goal,
    update_goal_data,
    delete_goal_by_id
)

goal_routes = Blueprint('goals', __name__, url_prefix='/api/goals')


@goal_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_goals():
    """Get all goals for authenticated user.
    ---
    tags:
      - Goals
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: is_active
        type: boolean
        required: false
        description: Filter by active status
        example: true
    responses:
      200:
        description: List of user goals
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
                example: "Meditar 30 días seguidos"
              description:
                type: string
                example: "Crear el hábito de meditación diaria"
              metric_key:
                type: string
                example: "meditation_days"
                description: Key identifier for the metric
              target_value:
                type: number
                example: 30
                description: Target value to achieve
              is_active:
                type: boolean
                example: true
              start_date:
                type: string
                format: date
                example: "2025-01-01"
              end_date:
                type: string
                format: date
                example: "2025-01-31"
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
    return get_my_goals()


@goal_routes.route('/<goal_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_goal_by_id(goal_id):
    """Get specific goal by ID.
    ---
    tags:
      - Goals
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: goal_id
        in: path
        required: true
        type: string
        format: uuid
        description: Goal ID
    responses:
      200:
        description: Goal data
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
            description:
              type: string
            metric_key:
              type: string
            target_value:
              type: number
            is_active:
              type: boolean
            start_date:
              type: string
              format: date
            end_date:
              type: string
              format: date
              nullable: true
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Goal belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Goal not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_goal(goal_id)


@goal_routes.route('/', methods=['POST'])
@token_required
def create_goal():
    """Create new goal.
    ---
    tags:
      - Goals
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Goal data
        required: true
        schema:
          type: object
          required:
            - title
            - target_value
            - start_date
          properties:
            title:
              type: string
              example: "Meditar 30 días seguidos"
              description: Goal title
            description:
              type: string
              example: "Crear hábito de meditación diaria"
              description: Goal description
            metric_key:
              type: string
              example: "meditation_days"
              description: Key identifier for the metric
            target_value:
              type: number
              example: 30
              description: Target value to achieve
            is_active:
              type: boolean
              example: true
              default: true
              description: Whether goal is currently active
            start_date:
              type: string
              format: date
              example: "2025-01-01"
              description: Goal start date
            end_date:
              type: string
              format: date
              example: "2025-01-31"
              description: Optional target completion date
    responses:
      201:
        description: Goal created successfully
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
            description:
              type: string
            metric_key:
              type: string
            target_value:
              type: number
            is_active:
              type: boolean
            start_date:
              type: string
              format: date
            end_date:
              type: string
              format: date
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
    return create_new_goal(data)


@goal_routes.route('/<goal_id>', methods=['PUT'])
@token_required
def update_goal(goal_id):
    """Update goal.
    ---
    tags:
      - Goals
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: goal_id
        in: path
        required: true
        type: string
        format: uuid
        description: Goal ID
      - in: body
        name: body
        description: Updated goal data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Meditar 60 días seguidos"
            description:
              type: string
            metric_key:
              type: string
              example: "meditation_days"
            target_value:
              type: number
              example: 60
            is_active:
              type: boolean
              example: true
            end_date:
              type: string
              format: date
    responses:
      200:
        description: Goal updated successfully
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
            description:
              type: string
            metric_key:
              type: string
            target_value:
              type: number
            is_active:
              type: boolean
            start_date:
              type: string
              format: date
            end_date:
              type: string
              format: date
              nullable: true
            created_at:
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
        description: Forbidden - Goal belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Goal not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_goal_data(goal_id, data)


@goal_routes.route('/<goal_id>', methods=['DELETE'])
@token_required
def delete_goal(goal_id):
    """Delete goal.
    ---
    tags:
      - Goals
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: goal_id
        in: path
        required: true
        type: string
        format: uuid
        description: Goal ID to delete
    responses:
      200:
        description: Goal deleted successfully
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
        description: Forbidden - Goal belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Goal not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_goal_by_id(goal_id)
