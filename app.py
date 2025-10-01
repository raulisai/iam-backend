"""
This is a simple Flask application that returns a greeting message
when the root endpoint is accessed.
"""

from flask import Flask
from flasgger import Swagger
from routes.auth_routes import auth_routes
from routes.task_routes import task_routes

app = Flask(__name__)

# Swagger configuration and shared schema definitions (Swagger 2.0)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "IAM Backend API",
        "description": "API documentation for authentication and task management.",
        "version": "1.0.0"
    },
    "schemes": ["http"],
    "basePath": "/",
    "definitions": {
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Invalid credentials"}
            }
        },
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "email": {"type": "string", "example": "user@example.com"},
                "name": {"type": "string", "example": "John Doe"},
                "hashed_password": {"type": "string", "example": "$2b$12$..."}
            }
        },
        "LoginRequest": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "example": "user@example.com"},
                "password": {"type": "string", "example": "secret"}
            }
        },
        "LoginResponse": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "example": "uuid-token-or-userid"},
                "user": {"$ref": "#/definitions/User"}
            }
        },
        "Task": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 10},
                "created_at": {"type": "string", "format": "date-time"},
                "title": {"type": "string", "example": "Buy groceries"},
                "time": {"type": "string", "example": "30m"},
                "points": {"type": "integer", "example": 5},
                "desc": {"type": "string", "example": "Get milk, eggs, bread"},
                "level": {"type": "string", "example": "easy"},
                "categoria": {"type": "string", "example": "personal"}
            }
        },
        "TaskInput": {
            "type": "object",
            "required": ["title", "time", "points", "desc", "level", "categoria"],
            "properties": {
                "title": {"type": "string"},
                "time": {"type": "string"},
                "points": {"type": "integer"},
                "desc": {"type": "string"},
                "level": {"type": "string"},
                "categoria": {"type": "string"}
            }
        }
    }
}

swagger = Swagger(app, template=swagger_template)

# CORS: allow frontend at http://localhost:5173
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Vary'] = 'Origin'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# Register the blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(task_routes)

if __name__ == '__main__':
    app.run()