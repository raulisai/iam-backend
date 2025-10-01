"""Task template routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.task_template_controller import (
    get_all_templates,
    get_template_by_id,
    get_template_by_key,
    get_templates_by_cat,
    create_template,
    update_template,
    delete_template
)

task_template_routes = Blueprint('task_templates', __name__, url_prefix='/api/task-templates')


@task_template_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_templates():
    """Get all task templates.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: List of all task templates
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              key:
                type: string
                example: "meditation_10"
              name:
                type: string
                example: "Meditación 10 minutos"
              category:
                type: string
                example: "mind"
                enum: ["mind", "body"]
              estimated_minutes:
                type: integer
                example: 10
              difficulty:
                type: integer
                example: 3
                minimum: 1
                maximum: 5
              reward_xp:
                type: integer
                example: 50
              default_params:
                type: object
                example: {"type": "guided", "music": true}
              created_by:
                type: string
                example: "system"
              descr:
                type: string
                example: "Sesión de meditación guiada de 10 minutos"
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
    return get_all_templates()


@task_template_routes.route('/<template_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_template(template_id):
    """Get task template by ID.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: template_id
        in: path
        required: true
        type: string
        format: uuid
        description: Template ID
    responses:
      200:
        description: Template data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            key:
              type: string
              example: "meditation_10"
            name:
              type: string
              example: "Meditación 10 minutos"
            category:
              type: string
              enum: ["mind", "body"]
            estimated_minutes:
              type: integer
              example: 10
            difficulty:
              type: integer
              example: 3
              minimum: 1
              maximum: 5
            reward_xp:
              type: integer
              example: 50
            default_params:
              type: object
              example: {"type": "guided", "music": true}
            created_by:
              type: string
              example: "system"
            descr:
              type: string
              example: "Sesión de meditación guiada"
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Template not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_template_by_id(template_id)


@task_template_routes.route('/key/<key>', methods=['GET', 'OPTIONS'])
@token_required
def get_by_key(key):
    """Get task template by unique key.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: key
        in: path
        required: true
        type: string
        description: Template unique key
        example: "meditation_10"
    responses:
      200:
        description: Template data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            key:
              type: string
              example: "meditation_10"
            name:
              type: string
              example: "Meditación 10 minutos"
            category:
              type: string
              enum: ["mind", "body"]
            estimated_minutes:
              type: integer
              example: 10
            difficulty:
              type: integer
              example: 3
            reward_xp:
              type: integer
              example: 50
            default_params:
              type: object
              example: {"type": "guided"}
            created_by:
              type: string
              example: "system"
            descr:
              type: string
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Template not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_template_by_key(key)


@task_template_routes.route('/category/<category>', methods=['GET', 'OPTIONS'])
@token_required
def get_by_category(category):
    """Get task templates filtered by category.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: category
        in: path
        required: true
        type: string
        enum: ["mind", "body"]
        description: Template category
        example: "mind"
    responses:
      200:
        description: List of templates in category
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              key:
                type: string
              name:
                type: string
              category:
                type: string
                enum: ["mind", "body"]
              estimated_minutes:
                type: integer
              difficulty:
                type: integer
              reward_xp:
                type: integer
              default_params:
                type: object
              created_by:
                type: string
              descr:
                type: string
              created_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      400:
        description: Invalid category
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_templates_by_cat(category)


@task_template_routes.route('/', methods=['POST'])
@token_required
def create():
    """Create task template.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Task template data
        required: true
        schema:
          type: object
          required:
            - key
            - name
            - category
            - descr
          properties:
            key:
              type: string
              example: "meditation_15"
              description: Unique key identifier for the template
            name:
              type: string
              example: "Meditación 15 minutos"
              description: Display name of the template
            category:
              type: string
              example: "mind"
              enum: ["mind", "body"]
              description: Template category (mind or body)
            estimated_minutes:
              type: integer
              example: 15
              description: Estimated duration in minutes
            difficulty:
              type: integer
              example: 3
              minimum: 1
              maximum: 5
              default: 3
              description: Difficulty level from 1 to 5
            reward_xp:
              type: integer
              example: 75
              default: 0
              description: XP points awarded upon completion
            descr:
              type: string
              example: "Sesión de meditación guiada de 15 minutos"
              description: Description of the template
            default_params:
              type: object
              example: {"type": "guided", "music": true, "voice": "female"}
              description: Default JSON parameters for tasks created from this template
            created_by:
              type: string
              example: "system"
              default: "system"
              description: Creator identifier
    responses:
      201:
        description: Template created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            key:
              type: string
            name:
              type: string
            category:
              type: string
            estimated_minutes:
              type: integer
            difficulty:
              type: integer
            reward_xp:
              type: integer
            descr:
              type: string
            default_params:
              type: object
            created_by:
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
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_template(data)


@task_template_routes.route('/<template_id>', methods=['PUT'])
@token_required
def update(template_id):
    """Update task template.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: template_id
        in: path
        required: true
        type: string
        format: uuid
        description: Template ID
      - in: body
        name: body
        description: Updated template data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Meditación 15 minutos"
            category:
              type: string
              enum: ["mind", "body"]
            estimated_minutes:
              type: integer
              example: 15
            difficulty:
              type: integer
              minimum: 1
              maximum: 5
              example: 4
            reward_xp:
              type: integer
              example: 75
            descr:
              type: string
              example: "Sesión actualizada"
            default_params:
              type: object
              example: {"type": "advanced", "music": false}
    responses:
      200:
        description: Template updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            key:
              type: string
            name:
              type: string
            category:
              type: string
            estimated_minutes:
              type: integer
            difficulty:
              type: integer
            reward_xp:
              type: integer
            descr:
              type: string
            default_params:
              type: object
            created_by:
              type: string
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
      404:
        description: Template not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_template(template_id, data)


@task_template_routes.route('/<template_id>', methods=['DELETE'])
@token_required
def delete(template_id):
    """Delete task template.
    ---
    tags:
      - Task Templates
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: template_id
        in: path
        required: true
        type: string
        format: uuid
        description: Template ID to delete
    responses:
      200:
        description: Template deleted successfully
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
        description: Template not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      400:
        description: Cannot delete template - tasks exist that use it
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_template(template_id)
