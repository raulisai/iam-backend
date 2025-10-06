"""Task recommendation routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.task_recommendation_controller import (
    get_task_recommendations,
    get_mind_task_recommendations,
    get_body_task_recommendations
)

task_recommendation_routes = Blueprint('task_recommendations', __name__, url_prefix='/api/tasks/recommendations')


@task_recommendation_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_recommendations():
    """Get personalized task recommendations for authenticated user.
    ---
    tags:
      - Task Recommendations
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: use_ai
        type: boolean
        required: false
        default: false
        description: Use AI agent for intelligent recommendations (only when user has sufficient task history)
        example: true
    responses:
      200:
        description: Task recommendations generated successfully
        schema:
          type: object
          properties:
            recommendations:
              type: array
              description: List of 3 recommended task templates
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                    description: Template ID
                  key:
                    type: string
                    example: "meditation_morning"
                    description: Template unique key
                  name:
                    type: string
                    example: "Meditación Matutina"
                    description: Template name
                  category:
                    type: string
                    enum: ["mind", "body"]
                    example: "mind"
                    description: Task category
                  desc:
                    type: string
                    example: "Sesión de meditación para comenzar el día"
                    description: Template description
                  default_xp:
                    type: integer
                    example: 10
                    description: Default XP awarded for completion
                  default_params:
                    type: object
                    example: {"duration": 15}
                    description: Default parameters for the task
                  suggested_schedule:
                    type: string
                    format: date-time
                    example: "2025-10-06T14:00:00Z"
                    description: Suggested time to schedule this task
                  reason:
                    type: string
                    example: "Recomendado para balancear tus tareas de mente"
                    description: Reason for this recommendation
            method:
              type: string
              enum: ["pattern_based", "ai_powered"]
              example: "pattern_based"
              description: Method used to generate recommendations
            generated_at:
              type: string
              format: date-time
              example: "2025-10-06T10:30:00Z"
              description: When recommendations were generated
            task_history_count:
              type: integer
              example: 12
              description: Number of recent tasks analyzed
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error generating recommendations
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_task_recommendations()


@task_recommendation_routes.route('/mind', methods=['GET', 'OPTIONS'])
@token_required
def get_mind_recommendations():
    """Get personalized mind task recommendations for authenticated user.
    ---
    tags:
      - Task Recommendations
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: use_ai
        type: boolean
        required: false
        default: false
        description: Use AI agent for intelligent recommendations
        example: true
      - in: query
        name: count
        type: integer
        required: false
        default: 3
        minimum: 1
        maximum: 10
        description: Number of recommendations to generate
        example: 3
    responses:
      200:
        description: Mind task recommendations generated successfully
        schema:
          type: object
          properties:
            recommendations:
              type: array
              description: List of recommended mind task templates
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  key:
                    type: string
                    example: "meditation_morning"
                  name:
                    type: string
                    example: "Meditación Matutina"
                  category:
                    type: string
                    enum: ["mind"]
                    example: "mind"
                  desc:
                    type: string
                    example: "Sesión de meditación para comenzar el día"
                  default_xp:
                    type: integer
                    example: 10
                  default_params:
                    type: object
                    example: {"duration": 15}
                  suggested_schedule:
                    type: string
                    format: date-time
                  reason:
                    type: string
            method:
              type: string
              enum: ["pattern_based", "ai_powered"]
            generated_at:
              type: string
              format: date-time
            task_history_count:
              type: integer
            category:
              type: string
              enum: ["mind"]
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error generating recommendations
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_mind_task_recommendations()


@task_recommendation_routes.route('/body', methods=['GET', 'OPTIONS'])
@token_required
def get_body_recommendations():
    """Get personalized body task recommendations for authenticated user.
    ---
    tags:
      - Task Recommendations
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: use_ai
        type: boolean
        required: false
        default: false
        description: Use AI agent for intelligent recommendations
        example: true
      - in: query
        name: count
        type: integer
        required: false
        default: 3
        minimum: 1
        maximum: 10
        description: Number of recommendations to generate
        example: 3
    responses:
      200:
        description: Body task recommendations generated successfully
        schema:
          type: object
          properties:
            recommendations:
              type: array
              description: List of recommended body task templates
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  key:
                    type: string
                    example: "cardio_30min"
                  name:
                    type: string
                    example: "Cardio 30 minutos"
                  category:
                    type: string
                    enum: ["body"]
                    example: "body"
                  desc:
                    type: string
                    example: "Ejercicio cardiovascular moderado"
                  default_xp:
                    type: integer
                    example: 15
                  default_params:
                    type: object
                    example: {"duration": 30, "intensity": "moderate"}
                  suggested_schedule:
                    type: string
                    format: date-time
                  reason:
                    type: string
            method:
              type: string
              enum: ["pattern_based", "ai_powered"]
            generated_at:
              type: string
              format: date-time
            task_history_count:
              type: integer
            category:
              type: string
              enum: ["body"]
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Error generating recommendations
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_body_task_recommendations()
