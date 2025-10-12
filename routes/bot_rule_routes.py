"""Bot rule routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.bot_rule_controller import (
    get_bot_rules,
    get_rule,
    create_rule,
    update_rule,
    delete_rule
)

bot_rule_routes = Blueprint('bot_rules', __name__, url_prefix='/api/bot-rules')


@bot_rule_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_rules():
    """Get all bot automation rules.
    ---
    tags:
      - Bot Rules
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: active_only
        type: boolean
        required: false
        description: Filter to only active rules
        example: true
    responses:
      200:
        description: List of bot rules
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              name:
                type: string
                example: "Auto-schedule morning meditation"
              condition:
                type: object
                example: {"time": "08:00", "days": ["mon", "tue", "wed"]}
                description: JSON conditions for when the rule triggers
              action:
                type: object
                example: {"type": "create_task", "template_id": "xyz"}
                description: JSON action to perform when triggered
              priority:
                type: integer
                example: 10
                description: Rule priority (higher = more important)
              active:
                type: boolean
                example: true
              last_evaluated:
                type: string
                format: date-time
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
    return get_bot_rules()


@bot_rule_routes.route('/<rule_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_rule_by_id(rule_id):
    """Get specific bot rule by ID.
    ---
    tags:
      - Bot Rules
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: rule_id
        in: path
        required: true
        type: string
        format: uuid
        description: Bot rule ID
    responses:
      200:
        description: Bot rule data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
              example: "Auto-schedule morning meditation"
            condition:
              type: object
              example: {"time": "08:00", "days": ["mon", "tue", "wed"]}
            action:
              type: object
              example: {"type": "create_task", "template_id": "xyz"}
            priority:
              type: integer
              example: 10
            active:
              type: boolean
            last_evaluated:
              type: string
              format: date-time
              nullable: true
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Bot rule not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_rule(rule_id)


@bot_rule_routes.route('/', methods=['POST'])
@token_required
def create_bot_rule():
    """Create new bot automation rule.
    ---
    tags:
      - Bot Rules
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Bot rule data
        required: true
        schema:
          type: object
          required:
            - name
            - condition
            - action
          properties:
            name:
              type: string
              example: "Auto-schedule morning meditation"
              description: Human-readable rule name
            condition:
              type: object
              example: {"time": "08:00", "days": ["mon", "tue", "wed", "thu", "fri"]}
              description: JSON conditions for when the rule triggers
            action:
              type: object
              example: {"type": "create_task", "template_id": "550e8400-e29b-41d4-a716-446655440000", "category": "mind"}
              description: JSON action to perform when triggered
            priority:
              type: integer
              example: 10
              default: 5
              description: Rule priority (higher = more important)
            active:
              type: boolean
              example: true
              default: true
              description: Whether the rule is currently active
    responses:
      201:
        description: Bot rule created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            condition:
              type: object
            action:
              type: object
            priority:
              type: integer
            active:
              type: boolean
            last_evaluated:
              type: string
              format: date-time
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
    return create_rule(data)


@bot_rule_routes.route('/<rule_id>', methods=['PUT'])
@token_required
def update_bot_rule(rule_id):
    """Update bot automation rule.
    ---
    tags:
      - Bot Rules
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: rule_id
        in: path
        required: true
        type: string
        format: uuid
        description: Bot rule ID
      - in: body
        name: body
        description: Updated rule data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Auto-schedule evening meditation"
            condition:
              type: object
              example: {"time": "20:00", "days": ["all"]}
            action:
              type: object
              example: {"type": "create_task", "template_id": "xyz"}
            priority:
              type: integer
              example: 15
            active:
              type: boolean
              example: false
    responses:
      200:
        description: Bot rule updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            condition:
              type: object
            action:
              type: object
            priority:
              type: integer
            active:
              type: boolean
            last_evaluated:
              type: string
              format: date-time
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
      404:
        description: Bot rule not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_rule(rule_id, data)


@bot_rule_routes.route('/<rule_id>', methods=['DELETE'])
@token_required
def delete_bot_rule(rule_id):
    """Delete bot automation rule.
    ---
    tags:
      - Bot Rules
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: rule_id
        in: path
        required: true
        type: string
        format: uuid
        description: Bot rule ID to delete
    responses:
      200:
        description: Bot rule deleted successfully
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
      404:
        description: Bot rule not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_rule(rule_id)
