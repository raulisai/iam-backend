"""Authentication routes for user login and management."""
from flask import Blueprint, request, jsonify
from controllers.auth_controller import get_all_users, authenticate_user

# Create Blueprint for authentication routes
auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/', methods=['GET'])
def hello_world():
    """
    Handle the root endpoint and return a greeting message.
    ---
    tags:
      - Auth
    responses:
      200:
        description: A greeting message
        schema:
          type: string
          example: Hello World!
    """
    return 'Hello World!'


@auth_routes.route('/getusers', methods=['GET'])
def get_users():
    """
    Handle the user get endpoint and return all users.
    ---
    tags:
      - Auth
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    """
    return get_all_users()


@auth_routes.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@auth_routes.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """
    Handle the login endpoint and return a valid token.
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        description: Login credentials
        required: true
        schema:
          $ref: '#/definitions/LoginRequest'
    responses:
      200:
        description: Successful login
        schema:
          $ref: '#/definitions/LoginResponse'
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Invalid credentials
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    return authenticate_user(email, password)
