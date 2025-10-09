"""Goal Task Recommendation Routes - Endpoints for AI-powered goal task recommendations."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.goal_task_recommendation_controller import get_goal_task_recommendations

goal_task_recommendation_routes = Blueprint(
    'goal_task_recommendations',
    __name__,
    url_prefix='/api/goals'
)


@goal_task_recommendation_routes.route('/<goal_id>/recommendations', methods=['GET', 'POST', 'OPTIONS'])
@token_required
def get_goal_recommendations(goal_id):
    """Get AI-powered task recommendations for a specific goal.
    ---
    tags:
      - Goal Task Recommendations
    parameters:
      - in: path
        name: goal_id
        description: Goal ID (UUID)
        required: true
        type: string
        format: uuid
        example: "550e8400-e29b-41d4-a716-446655440000"
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: use_ai
        type: boolean
        required: false
        default: true
        description: Use AI agent for intelligent recommendations (highly recommended)
        example: true
      - in: query
        name: count
        type: integer
        required: false
        default: 5
        minimum: 1
        maximum: 10
        description: Number of task recommendations to generate
        example: 5
      - in: body
        name: context
        description: Optional additional context to help AI generate better recommendations (POST only)
        schema:
          type: object
          properties:
            context:
              type: object
              description: Additional information to help generate recommendations
              properties:
                current_challenges:
                  type: string
                  example: "Falta de tiempo y recursos limitados"
                  description: Current challenges or obstacles
                available_time:
                  type: string
                  example: "2 horas por día"
                  description: Available time to work on goal
                resources:
                  type: array
                  items:
                    type: string
                  example: ["Computadora", "Internet", "Libros"]
                  description: Available resources
                preferences:
                  type: string
                  example: "Prefiero tareas prácticas y cortas"
                  description: User preferences for task types
    responses:
      200:
        description: Task recommendations generated successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            goal:
              type: object
              properties:
                id:
                  type: string
                  format: uuid
                  example: "550e8400-e29b-41d4-a716-446655440000"
                title:
                  type: string
                  example: "Aprender Python"
                description:
                  type: string
                  example: "Dominar programación en Python en 6 meses"
            recommendations:
              type: array
              description: List of recommended tasks to achieve the goal
              items:
                type: object
                properties:
                  title:
                    type: string
                    example: "Completar tutorial básico de Python"
                    description: Task title
                  description:
                    type: string
                    example: "Seguir un tutorial introductorio completo de Python que cubra variables, funciones y estructuras de control"
                    description: Detailed task description
                  priority:
                    type: string
                    enum: ["low", "medium", "high"]
                    example: "high"
                    description: Task priority level
                  estimated_duration:
                    type: string
                    example: "2 horas"
                    description: Estimated time to complete
                  template_id:
                    type: string
                    format: uuid
                    nullable: true
                    example: null
                    description: Related template ID if applicable
                  order:
                    type: integer
                    example: 1
                    description: Suggested order of execution
                  reason:
                    type: string
                    example: "Fundamental para construir una base sólida antes de proyectos avanzados"
                    description: Why this task is important for the goal
            method:
              type: string
              enum: ["ai_powered", "pattern_based"]
              example: "ai_powered"
              description: Method used to generate recommendations
            generated_at:
              type: string
              format: date-time
              example: "2025-10-08T10:30:00Z"
              description: When recommendations were generated
            existing_task_count:
              type: integer
              example: 3
              description: Number of existing tasks for this goal
            ai_metadata:
              type: object
              description: AI generation metadata (only when use_ai=true)
              properties:
                tokens_used:
                  type: integer
                  example: 1250
                model:
                  type: string
                  example: "gpt-4-turbo-preview"
      400:
        description: Bad request - Invalid parameters or goal not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Goal not found or unauthorized"
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Server error generating recommendations
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Failed to generate recommendations: AI service unavailable"
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_goal_task_recommendations(goal_id)
