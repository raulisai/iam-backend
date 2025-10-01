"""Achievement routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.achievement_controller import (
    get_my_achievements,
    award_achievement,
    delete_achievement_by_id
)

achievement_routes = Blueprint('achievements', __name__, url_prefix='/api/achievements')


@achievement_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_achievements():
    """Get all achievements for authenticated user.
    ---
    tags:
      - Achievements
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: List of user achievements
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
              achievement_key:
                type: string
                example: "first_meditation"
              title:
                type: string
                example: "Primera Meditación"
              descr:
                type: string
                example: "Completaste tu primera sesión de meditación"
              icon_url:
                type: string
                example: "https://example.com/icon.png"
                nullable: true
              awarded_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_my_achievements()


@achievement_routes.route('/', methods=['POST'])
@token_required
def create_achievement():
    """Award new achievement to user.
    ---
    tags:
      - Achievements
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Achievement data
        required: true
        schema:
          type: object
          required:
            - achievement_key
            - title
            - descr
          properties:
            achievement_key:
              type: string
              example: "first_meditation"
              description: Unique identifier for this achievement type
            title:
              type: string
              example: "Primera Meditación"
              description: Achievement title
            descr:
              type: string
              example: "Completaste tu primera sesión de meditación"
              description: Achievement description
            icon_url:
              type: string
              example: "https://example.com/icon.png"
              description: Optional icon URL
    responses:
      201:
        description: Achievement awarded successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            achievement_key:
              type: string
            title:
              type: string
            descr:
              type: string
            icon_url:
              type: string
              nullable: true
            awarded_at:
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
    return award_achievement(data)


@achievement_routes.route('/<achievement_id>', methods=['DELETE'])
@token_required
def delete_achievement(achievement_id):
    """Delete achievement.
    ---
    tags:
      - Achievements
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: achievement_id
        in: path
        required: true
        type: string
        format: uuid
        description: Achievement ID to delete
    responses:
      200:
        description: Achievement deleted successfully
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
        description: Forbidden - Achievement belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Achievement not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_achievement_by_id(achievement_id)
