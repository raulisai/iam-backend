"""Task routes for CRUD operations on tasks."""
from flask import Blueprint, request, jsonify
from controllers.task_controller import (
    get_all_tasks,
    get_task_by_id,
    create_new_task,
    update_task_by_id,
    delete_task_by_id
)
from middleware.auth_middleware import token_required

# Create Blueprint for task routes
task_routes = Blueprint('tasks', __name__, url_prefix='/api/task')


@task_routes.route('/create', methods=['POST', 'OPTIONS'])
@token_required
def create_task():
    """
    Handle the task create endpoint.
    ---
    tags:
      - Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Task fields
        required: true
        schema:
          $ref: '#/definitions/TaskInput'
    responses:
      200:
        description: Task created
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
      400:
        description: Invalid request or missing fields
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    return create_new_task(data)


@task_routes.route('/get', methods=['GET', 'OPTIONS'])
@token_required
def get_tasks():
    """
    Handle the task get endpoint.
    ---
    tags:
      - Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: List of tasks
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_all_tasks()


@task_routes.route('/get/<task_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_task(task_id):
    """
    Handle the task get by id endpoint.
    ---
    tags:
      - Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: integer
        description: Task ID
    responses:
      200:
        description: Task data
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_task_by_id(int(task_id))


@task_routes.route('/update/<task_id>', methods=['PUT', 'OPTIONS'])
@token_required
def update_task(task_id):
    """
    Handle the task update endpoint.
    ---
    tags:
      - Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: integer
        description: Task ID
      - in: body
        name: body
        description: Fields to update
        required: true
        schema:
          $ref: '#/definitions/TaskInput'
    responses:
      200:
        description: Updated task data
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_task_by_id(int(task_id), data)


@task_routes.route('/delete/<task_id>', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_task(task_id):
    """
    Handle the task delete endpoint.
    ---
    tags:
      - Tasks
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: task_id
        in: path
        required: true
        type: integer
        description: Task ID
    responses:
      200:
        description: Deleted task data
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return delete_task_by_id(int(task_id))
