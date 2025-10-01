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
    get:
      summary: Get a greeting message
      responses:
        200:
          description: A greeting message
          content:
            text/plain:
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
    get:
      summary: Get all users
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    email:
                      type: string
                    name:
                      type: string
                    hashed_password:
                      type: string
    """
    return get_all_users()


@auth_routes.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@auth_routes.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """
    Handle the login endpoint and return a valid token.
    ---
    post:
      summary: Login user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
              required:
                - email
                - password
      responses:
        200:
          description: Successful login
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                  user:
                    type: object
                    properties:
                      id:
                        type: integer
                      user:
                        type: string
                      email:
                        type: string
        400:
          description: Invalid request
        401:
          description: Invalid credentials
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    return authenticate_user(email, password)
