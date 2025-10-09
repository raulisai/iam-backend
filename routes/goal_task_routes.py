"""Goal Task routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.goal_task_controller import (
    get_tasks_for_goal,
    get_task,
    create_new_goal_task,
    update_task_data,
    delete_task_by_id,
    get_occurrences_for_task,
    create_new_occurrence,
    generate_occurrences,
    get_occurrence,
    delete_occurrence,
    log_action_on_occurrence,
    get_logs_for_occurrence,
    get_progress_for_goal,
    get_progress_detailed_for_goal
)

goal_task_routes = Blueprint('goal_tasks', __name__, url_prefix='/api/goals')


# ===== GOAL TASKS ENDPOINTS =====

@goal_task_routes.route('/<goal_id>/tasks', methods=['GET', 'OPTIONS'])
@token_required
def get_goal_tasks(goal_id):
    """Get all tasks for a specific goal.
    ---
    tags:
      - Goal Tasks
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
        description: List of goal tasks
        schema:
          type: array
          items:
            $ref: '#/definitions/GoalTask'
      401:
        description: Unauthorized
      403:
        description: Forbidden - Goal belongs to another user
      404:
        description: Goal not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_tasks_for_goal(goal_id)


@goal_task_routes.route('/<goal_id>/tasks', methods=['POST'])
@token_required
def create_goal_task(goal_id):
    """Create a new task for a goal.
    ---
    tags:
      - Goal Tasks
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
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: "Meditar 10 minutos"
            description:
              type: string
              example: "Sesión de meditación matutina"
            type:
              type: string
              example: "mind"
              description: Task type (mind, body, habit, one_off)
            required:
              type: boolean
              default: true
              description: Whether task counts for goal progress
            weight:
              type: number
              default: 1
              description: Task weight for progress calculation
            due_at:
              type: string
              format: date-time
              description: Due date for one-time tasks
            schedule_rrule:
              type: string
              example: "FREQ=DAILY;BYHOUR=8"
              description: Recurrence rule for recurring tasks (RFC 5545)
    responses:
      201:
        description: Task created successfully
        schema:
          $ref: '#/definitions/GoalTask'
      400:
        description: Invalid request
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Goal not found
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_goal_task(goal_id, data)


@goal_task_routes.route('/tasks/<task_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_task_by_id(task_id):
    """Get specific task by ID.
    ---
    tags:
      - Goal Tasks
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
        description: Task ID
    responses:
      200:
        description: Task data
        schema:
          $ref: '#/definitions/GoalTask'
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_task(task_id)


@goal_task_routes.route('/tasks/<task_id>', methods=['PUT'])
@token_required
def update_goal_task(task_id):
    """Update a goal task.
    ---
    tags:
      - Goal Tasks
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
        description: Task ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            type:
              type: string
            required:
              type: boolean
            weight:
              type: number
            due_at:
              type: string
              format: date-time
            schedule_rrule:
              type: string
    responses:
      200:
        description: Task updated successfully
        schema:
          $ref: '#/definitions/GoalTask'
      400:
        description: Invalid request
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    return update_task_data(task_id, data)


@goal_task_routes.route('/tasks/<task_id>', methods=['DELETE'])
@token_required
def delete_goal_task(task_id):
    """Delete a goal task.
    ---
    tags:
      - Goal Tasks
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
        description: Task ID
    responses:
      200:
        description: Task deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    return delete_task_by_id(task_id)


# ===== TASK OCCURRENCES ENDPOINTS =====

@goal_task_routes.route('/tasks/<task_id>/occurrences', methods=['GET', 'OPTIONS'])
@token_required
def get_task_occurrences(task_id):
    """Get occurrences for a task.
    ---
    tags:
      - Task Occurrences
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
        description: Task ID
      - in: query
        name: start_date
        type: string
        format: date-time
        description: Filter occurrences from this date
      - in: query
        name: end_date
        type: string
        format: date-time
        description: Filter occurrences until this date
      - in: query
        name: include_status
        type: boolean
        default: true
        description: Include status from logs
    responses:
      200:
        description: List of occurrences
        schema:
          type: array
          items:
            $ref: '#/definitions/TaskOccurrence'
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_occurrences_for_task(task_id)


@goal_task_routes.route('/tasks/<task_id>/occurrences', methods=['POST'])
@token_required
def create_occurrence(task_id):
    """Create a new occurrence for a task.
    ---
    tags:
      - Task Occurrences
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
        description: Task ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - scheduled_at
          properties:
            scheduled_at:
              type: string
              format: date-time
              example: "2025-10-08T08:00:00Z"
              description: When this occurrence is scheduled
    responses:
      201:
        description: Occurrence created successfully
        schema:
          $ref: '#/definitions/TaskOccurrence'
      400:
        description: Invalid request
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
      409:
        description: Occurrence already exists
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_occurrence(task_id, data)


@goal_task_routes.route('/tasks/<task_id>/occurrences/generate', methods=['POST'])
@token_required
def generate_task_occurrences(task_id):
    """Generate occurrences for a task based on its schedule.
    ---
    tags:
      - Task Occurrences
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
        description: Task ID
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            start_date:
              type: string
              format: date-time
              description: Start date for generation (defaults to start of current month)
            end_date:
              type: string
              format: date-time
              description: End date for generation (defaults to end of current month)
    responses:
      201:
        description: Occurrences generated successfully
        schema:
          type: object
          properties:
            generated:
              type: integer
              description: Number of occurrences generated
            occurrences:
              type: array
              items:
                $ref: '#/definitions/TaskOccurrence'
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Task not found
    """
    return generate_occurrences(task_id)


@goal_task_routes.route('/occurrences/<occurrence_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_occurrence_by_id(occurrence_id):
    """Get specific occurrence by ID.
    ---
    tags:
      - Task Occurrences
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: occurrence_id
        in: path
        required: true
        type: string
        format: uuid
        description: Occurrence ID
    responses:
      200:
        description: Occurrence data with status
        schema:
          $ref: '#/definitions/TaskOccurrenceWithStatus'
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Occurrence not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_occurrence(occurrence_id)


@goal_task_routes.route('/occurrences/<occurrence_id>', methods=['DELETE'])
@token_required
def delete_occurrence_by_id(occurrence_id):
    """Delete an occurrence.
    ---
    tags:
      - Task Occurrences
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: occurrence_id
        in: path
        required: true
        type: string
        format: uuid
        description: Occurrence ID
    responses:
      200:
        description: Occurrence deleted successfully
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Occurrence not found
    """
    return delete_occurrence(occurrence_id)


@goal_task_routes.route('/occurrences/<occurrence_id>/log', methods=['POST'])
@token_required
def log_occurrence_action(occurrence_id):
    """Log an action on an occurrence (complete, skip, start, etc).
    ---
    tags:
      - Task Occurrences
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: occurrence_id
        in: path
        required: true
        type: string
        format: uuid
        description: Occurrence ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - action
          properties:
            action:
              type: string
              example: "completed"
              description: Action type (completed, skipped, started, etc)
            metadata:
              type: object
              description: Additional metadata
              properties:
                value:
                  type: number
                  example: 10
                  description: Numeric value for progress (optional)
                notes:
                  type: string
                  description: Additional notes
    responses:
      201:
        description: Action logged successfully
        schema:
          $ref: '#/definitions/TaskLog'
      400:
        description: Invalid request
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Occurrence not found
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    return log_action_on_occurrence(occurrence_id, data)


@goal_task_routes.route('/occurrences/<occurrence_id>/logs', methods=['GET', 'OPTIONS'])
@token_required
def get_occurrence_logs(occurrence_id):
    """Get all logs for an occurrence.
    ---
    tags:
      - Task Occurrences
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: occurrence_id
        in: path
        required: true
        type: string
        format: uuid
        description: Occurrence ID
    responses:
      200:
        description: List of logs
        schema:
          type: array
          items:
            $ref: '#/definitions/TaskLog'
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Occurrence not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_logs_for_occurrence(occurrence_id)


# ===== PROGRESS ENDPOINT =====

@goal_task_routes.route('/<goal_id>/progress', methods=['GET', 'OPTIONS'])
@token_required
def get_goal_progress(goal_id):
    """Get progress for a goal based on task occurrences.
    ---
    tags:
      - Goal Tasks
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
        description: Goal progress data
        schema:
          type: object
          properties:
            goal_id:
              type: string
              format: uuid
            progress_percent:
              type: number
              example: 75.5
              description: Progress percentage (0-100)
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Goal not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_progress_for_goal(goal_id)


@goal_task_routes.route('/<goal_id>/progress/detailed', methods=['GET', 'OPTIONS'])
@token_required
def get_goal_progress_detailed_route(goal_id):
    """Get detailed progress for a goal (for debugging).
    ---
    tags:
      - Goal Tasks
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
        description: Detailed goal progress data
        schema:
          type: object
          properties:
            goal_id:
              type: string
              format: uuid
            progress_from_view:
              type: number
              description: Progress from database view
            manual_calculation:
              type: number
              description: Manually calculated progress
            total_tasks:
              type: integer
            total_occurrences:
              type: integer
            completed_occurrences:
              type: integer
            tasks:
              type: array
              items:
                type: object
      401:
        description: Unauthorized
      403:
        description: Forbidden
      404:
        description: Goal not found
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_progress_detailed_for_goal(goal_id)


# ===== SWAGGER DEFINITIONS =====
"""
definitions:
  GoalTask:
    type: object
    properties:
      id:
        type: string
        format: uuid
      goal_id:
        type: string
        format: uuid
      user_id:
        type: string
        format: uuid
      title:
        type: string
      description:
        type: string
      type:
        type: string
        description: Task type (mind, body, habit, one_off)
      required:
        type: boolean
        description: Whether task counts for goal progress
      weight:
        type: number
        description: Task weight for progress calculation
      due_at:
        type: string
        format: date-time
        description: Due date for one-time tasks
      schedule_rrule:
        type: string
        description: Recurrence rule for recurring tasks
      created_at:
        type: string
        format: date-time
  
  TaskOccurrence:
    type: object
    properties:
      id:
        type: string
        format: uuid
      task_id:
        type: string
        format: uuid
      scheduled_at:
        type: string
        format: date-time
      created_at:
        type: string
        format: date-time
  
  TaskOccurrenceWithStatus:
    allOf:
      - $ref: '#/definitions/TaskOccurrence'
      - type: object
        properties:
          status:
            type: string
            description: Current status (pending, completed, skipped, etc)
          last_action:
            type: string
            description: Last action performed
          last_value:
            type: number
            description: Last numeric value logged
  
  TaskLog:
    type: object
    properties:
      id:
        type: string
        format: uuid
      task_table:
        type: string
        example: "task_occurrences"
      task_id:
        type: string
        format: uuid
        description: Reference to occurrence ID
      user_id:
        type: string
        format: uuid
      action:
        type: string
        example: "completed"
      timestamp:
        type: string
        format: date-time
      metadata:
        type: object
        description: Additional data
"""
