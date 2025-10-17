"""Profile routes for user profile management."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.profile_controller import (
    get_user_profile,
    create_user_profile,
    update_user_profile,
    delete_user_profile,
    add_goal_points_to_profile
)

profile_routes = Blueprint('profile', __name__, url_prefix='/api/profile')


@profile_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_profile():
    """Get authenticated user's profile.
    ---
    tags:
      - Profile
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: User profile
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            timezone:
              type: string
              example: "America/Mexico_City"
            birth_date:
              type: string
              format: date
              example: "1990-01-15"
            gender:
              type: string
              example: "male"
            weight_kg:
              type: number
              example: 75.5
            height_cm:
              type: number
              example: 175
            preferred_language:
              type: string
              example: "es"
            hours_available_to_week:
              type: number
              example: 40
            work_schedules:
              type: string
              example: "9:00-17:00"
            current_status:
              type: string
              example: "active"
            hours_used_to_week:
              type: number
              example: 25.5
            time_dead:
              type: number
              example: 0
            day_work:
              type: string
              example: "L,M,M,J,V"
            goal_points_target:
              type: number
              example: 100
            goal_points_earned:
              type: number
              example: 45.5
            created_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_user_profile()


@profile_routes.route('/', methods=['POST'])
@token_required
def create_profile():
    """Create user profile.
    ---
    tags:
      - Profile
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Profile data
        required: true
        schema:
          type: object
          properties:
            timezone:
              type: string
              example: "America/Mexico_City"
              description: Timezone del usuario
            birth_date:
              type: string
              format: date
              example: "1990-01-15"
              description: Fecha de nacimiento
            gender:
              type: string
              example: "male"
              description: Género (male, female, other)
            weight_kg:
              type: number
              example: 75.5
              description: Peso en kilogramos
            height_cm:
              type: number
              example: 175
              description: Altura en centímetros
            preferred_language:
              type: string
              example: "es"
              default: "es"
              description: Idioma preferido (es, en, etc.)
            hours_available_to_week:
              type: number
              example: 40
              description: Horas disponibles por semana
            work_schedules:
              type: string
              example: "9:00-17:00"
              description: Horarios de trabajo
            current_status:
              type: string
              example: "active"
              description: Estado actual del usuario
            hours_used_to_week:
              type: number
              example: 0
              description: Horas usadas en la semana
            time_dead:
              type: number
              example: 0
              description: Tiempo muerto o no productivo
            day_work:
              type: string
              example: "L,M,M,J,V"
              description: Días de trabajo en la semana (D,L,M,M,J,V,S)
            goal_points_target:
              type: number
              example: 100
              description: Total de puntos disponibles de todos los goals y tareas activas
            goal_points_earned:
              type: number
              example: 0
              description: Puntos ganados de tareas completadas
    responses:
      201:
        description: Profile created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            timezone:
              type: string
            birth_date:
              type: string
              format: date
            gender:
              type: string
            weight_kg:
              type: number
            height_cm:
              type: number
            preferred_language:
              type: string
            hours_available_to_week:
              type: number
            work_schedules:
              type: string
            current_status:
              type: string
            hours_used_to_week:
              type: number
            time_dead:
              type: number
            day_work:
              type: string
            goal_points_target:
              type: number
            goal_points_earned:
              type: number
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
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_user_profile(data)


@profile_routes.route('/', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile.
    ---
    tags:
      - Profile
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Updated profile data (solo incluir campos a actualizar)
        required: true
        schema:
          type: object
          properties:
            timezone:
              type: string
              example: "America/Mexico_City"
            birth_date:
              type: string
              format: date
              example: "1990-01-15"
            gender:
              type: string
              example: "male"
            weight_kg:
              type: number
              example: 76.0
            height_cm:
              type: number
              example: 176
            preferred_language:
              type: string
              example: "en"
            hours_available_to_week:
              type: number
              example: 45
            work_schedules:
              type: string
              example: "10:00-18:00"
            current_status:
              type: string
              example: "busy"
            hours_used_to_week:
              type: number
              example: 30.5
            time_dead:
              type: number
              example: 5.0
            day_work:
              type: string
              example: "L,M,M,J,V,S"
            goal_points_target:
              type: number
              example: 150
              description: Total de puntos disponibles de todos los goals y tareas activas
            goal_points_earned:
              type: number
              example: 75.5
              description: Puntos ganados de tareas completadas
    responses:
      200:
        description: Profile updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            timezone:
              type: string
            birth_date:
              type: string
              format: date
            gender:
              type: string
            weight_kg:
              type: number
            height_cm:
              type: number
            preferred_language:
              type: string
            hours_available_to_week:
              type: number
            work_schedules:
              type: string
            current_status:
              type: string
            hours_used_to_week:
              type: number
            time_dead:
              type: number
            day_work:
              type: string
            goal_points_target:
              type: number
            goal_points_earned:
              type: number
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
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_user_profile(data)


@profile_routes.route('/', methods=['DELETE'])
@token_required
def delete_profile():
    """Delete user profile.
    ---
    tags:
      - Profile
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: Profile deleted successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_user_profile()


@profile_routes.route('/add-goal-points', methods=['POST'])
@token_required
def add_goal_points():
    """Add points to user profile from a completed goal task.
    ---
    tags:
      - Profile
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Task occurrence data
        required: true
        schema:
          type: object
          required:
            - task_occurrence_id
          properties:
            task_occurrence_id:
              type: string
              format: uuid
              description: ID de la ocurrencia de tarea completada
              example: "123e4567-e89b-12d3-a456-426614174000"
    responses:
      200:
        description: Points added successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            goal_points_target:
              type: number
              example: 100
            goal_points_earned:
              type: number
              example: 55.5
            points_added:
              type: number
              example: 10
              description: Puntos agregados en esta operación
            previous_earned:
              type: number
              example: 45.5
              description: Puntos ganados antes de esta operación
            timezone:
              type: string
            birth_date:
              type: string
              format: date
            gender:
              type: string
            weight_kg:
              type: number
            height_cm:
              type: number
            preferred_language:
              type: string
            hours_available_to_week:
              type: number
            work_schedules:
              type: string
            current_status:
              type: string
            hours_used_to_week:
              type: number
            time_dead:
              type: number
            day_work:
              type: string
            created_at:
              type: string
              format: date-time
      400:
        description: Invalid request or task not completed
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Task is not marked as completed"
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Task occurrence or profile not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Failed to add points. Task occurrence not found or profile not found."
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return add_goal_points_to_profile(data)
