"""Points routes for managing user points and goals."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.points_controller import (
    get_user_points,
    calculate_target_points,
    add_points,
    subtract_points,
    recalculate_points
)

# Create Blueprint for points routes
points_routes = Blueprint('points', __name__)


@points_routes.route('/api/points', methods=['GET'])
@token_required
def get_points(current_user):
    """
    Get points summary for the authenticated user.
    ---
    tags:
      - Points
    security:
      - Bearer: []
    responses:
      200:
        description: Points summary
        schema:
          type: object
          properties:
            goal_points_target:
              type: number
              description: Total points available from all active tasks
            goal_points_earned:
              type: number
              description: Points earned from completed tasks
            goal_points_remaining:
              type: number
              description: Points remaining to earn
            completion_percentage:
              type: number
              description: Percentage of points earned vs target
      404:
        description: User profile not found
      401:
        description: Unauthorized
    """
    user_id = current_user['user_id']
    return get_user_points(user_id)


@points_routes.route('/api/points/calculate-target', methods=['POST'])
@token_required
def calculate_target(current_user):
    """
    Calculate and update goal_points_target from all pending tasks.
    ---
    tags:
      - Points
    security:
      - Bearer: []
    responses:
      200:
        description: Calculated points breakdown
        schema:
          type: object
          properties:
            mind_points:
              type: number
              description: Points from pending mind tasks
            body_points:
              type: number
              description: Points from pending body tasks
            goal_points:
              type: number
              description: Points from pending goal tasks
            total_target_points:
              type: number
              description: Total points calculated
      401:
        description: Unauthorized
    """
    user_id = current_user['user_id']
    return calculate_target_points(user_id)


@points_routes.route('/api/points/add', methods=['POST'])
@token_required
def add_earned_points(current_user):
    """
    Add points to goal_points_earned and update snapshot scores.
    ---
    tags:
      - Points
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Points to add
        required: true
        schema:
          type: object
          required:
            - points
          properties:
            points:
              type: number
              description: Amount of points to add
              example: 50
            task_type:
              type: string
              enum: [mind, body, goal]
              description: Type of task the points come from
              example: mind
    responses:
      200:
        description: Points added successfully
        schema:
          type: object
          properties:
            previous_earned:
              type: number
            points_added:
              type: number
            new_earned:
              type: number
            task_type:
              type: string
      400:
        description: Invalid request
      401:
        description: Unauthorized
      404:
        description: User profile not found
    """
    user_id = current_user['user_id']
    data = request.get_json()
    
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    return add_points(user_id, data)


@points_routes.route('/api/points/subtract', methods=['POST'])
@token_required
def subtract_earned_points(current_user):
    """
    Subtract points from goal_points_earned and update snapshot scores.
    ---
    tags:
      - Points
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        description: Points to subtract
        required: true
        schema:
          type: object
          required:
            - points
          properties:
            points:
              type: number
              description: Amount of points to subtract
              example: 25
            task_type:
              type: string
              enum: [mind, body, goal]
              description: Type of task the points come from
              example: body
    responses:
      200:
        description: Points subtracted successfully
        schema:
          type: object
          properties:
            previous_earned:
              type: number
            points_subtracted:
              type: number
            new_earned:
              type: number
            task_type:
              type: string
      400:
        description: Invalid request
      401:
        description: Unauthorized
      404:
        description: User profile not found
    """
    user_id = current_user['user_id']
    data = request.get_json()
    
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    return subtract_points(user_id, data)


@points_routes.route('/api/points/recalculate', methods=['POST'])
@token_required
def recalculate_all(current_user):
    """
    Recalculate all points (target and earned) for the authenticated user.
    ---
    tags:
      - Points
    security:
      - Bearer: []
    responses:
      200:
        description: Complete points summary after recalculation
        schema:
          type: object
          properties:
            target_breakdown:
              type: object
              properties:
                mind_points:
                  type: number
                body_points:
                  type: number
                goal_points:
                  type: number
                total_target_points:
                  type: number
            points_summary:
              type: object
              properties:
                goal_points_target:
                  type: number
                goal_points_earned:
                  type: number
                goal_points_remaining:
                  type: number
                completion_percentage:
                  type: number
      401:
        description: Unauthorized
    """
    user_id = current_user['user_id']
    return recalculate_points(user_id)
