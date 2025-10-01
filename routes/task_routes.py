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
    post:
      summary: Create a new task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                time:
                  type: string
                points:
                  type: integer
                desc:
                  type: string
                level:
                  type: string
                categoria:
                  type: string
              required:
                - title
                - time
                - points
                - desc
                - level
                - categoria
      responses:
        200:
          description: Task created
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  created_at:
                    type: string
                  title:
                    type: string
                  time:
                    type: string
                  points:
                    type: integer
                  desc:
                    type: string
                  level:
                    type: string
                  categoria:
                    type: string
        400:
          description: Invalid request or missing fields
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
    get:
      summary: Get all tasks
      responses:
        200:
          description: List of tasks
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    created_at:
                      type: string
                    title:
                      type: string
                    time:
                      type: string
                    points:
                      type: integer
                    desc:
                      type: string
                    level:
                      type: string
                    categoria:
                      type: string
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_all_tasks()


@task_routes.route('/get/<id>', methods=['GET', 'OPTIONS'])
def get_task(id):
    """
    Handle the task get by id endpoint.
    ---
    get:
      summary: Get a task by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Task data
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    created_at:
                      type: string
                    title:
                      type: string
                    time:
                      type: string
                    points:
                      type: integer
                    desc:
                      type: string
                    level:
                      type: string
                    categoria:
                      type: string
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return get_task_by_id(id)


@task_routes.route('/update/<id>', methods=['PUT', 'OPTIONS'])
def update_task(id):
    """
    Handle the task update endpoint.
    ---
    put:
      summary: Update a task by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                time:
                  type: string
                points:
                  type: integer
                desc:
                  type: string
                level:
                  type: string
                categoria:
                  type: string
      responses:
        200:
          description: Updated task data
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    created_at:
                      type: string
                    title:
                      type: string
                    time:
                      type: string
                    points:
                      type: integer
                    desc:
                      type: string
                    level:
                      type: string
                    categoria:
                      type: string
        400:
          description: Invalid request
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    return update_task_by_id(id, data)


@task_routes.route('/delete/<id>', methods=['DELETE', 'OPTIONS'])
def delete_task(id):
    """
    Handle the task delete endpoint.
    ---
    delete:
      summary: Delete a task by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Deleted task data
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    created_at:
                      type: string
                    title:
                      type: string
                    time:
                      type: string
                    points:
                      type: integer
                    desc:
                      type: string
                    level:
                      type: string
                    categoria:
                      type: string
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    return delete_task_by_id(id)
