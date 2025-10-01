"""Task routes for CRUD operations on tasks."""
from flask import Blueprint, request, jsonify
from controllers.task_controller import (
    get_all_tasks,
    get_task_by_id,
    create_new_task,
    update_task_by_id,
    delete_task_by_id
)

# Create Blueprint for task routes
task_routes = Blueprint('tasks', __name__, url_prefix='/api/task')


@task_routes.route('/create', methods=['POST', 'OPTIONS'])
def create_task():
    """
    Handle the task create endpoint.
    ---
    tags:
      - Tasks
    parameters:
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
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    return create_new_task(data)


@task_routes.route('/get', methods=['GET', 'OPTIONS'])
def get_tasks():
    """
    Handle the task get endpoint.
    ---
    tags:
      - Tasks
    responses:
      200:
        description: List of tasks
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_all_tasks()


@task_routes.route('/get/<task_id>', methods=['GET', 'OPTIONS'])
def get_task(task_id):
    """
    Handle the task get by id endpoint.
    ---
    tags:
      - Tasks
    parameters:
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
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_task_by_id(int(task_id))


@task_routes.route('/update/<task_id>', methods=['PUT', 'OPTIONS'])
def update_task(task_id):
    """
    Handle the task update endpoint.
    ---
    tags:
      - Tasks
    parameters:
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
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_task_by_id(int(task_id), data)


@task_routes.route('/delete/<task_id>', methods=['DELETE', 'OPTIONS'])
def delete_task(task_id):
    """
    Handle the task delete endpoint.
    ---
    tags:
      - Tasks
    parameters:
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
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return delete_task_by_id(int(task_id))
