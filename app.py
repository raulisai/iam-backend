"""
This is a simple Flask application that returns a greeting message
when the root endpoint is accessed.
"""

from flask import Flask, request, jsonify
from flasgger import Swagger
from routes.auth_routes import auth_routes
from routes.task_routes import task_routes
from routes.profile_routes import profile_routes
from routes.task_template_routes import task_template_routes
from routes.mind_task_routes import mind_task_routes
from routes.body_task_routes import body_task_routes
from routes.achievement_routes import achievement_routes
from routes.goal_routes import goal_routes
from routes.goal_task_routes import goal_task_routes
from routes.goal_task_recommendation_routes import goal_task_recommendation_routes
from routes.task_log_routes import task_log_routes
from routes.failure_routes import failure_routes
from routes.bot_rule_routes import bot_rule_routes
from routes.chat_ia_routes import chat_ia_routes
from routes.chat_realtime_routes import chat_realtime_routes
from routes.stats_routes import stats_routes
from routes.task_recommendation_routes import task_recommendation_routes
from routes.time_optimizer_routes import time_optimizer_routes
from routes.notification_routes import notification_routes
import os

app = Flask(__name__)

# JWT Secret Key - In production, use environment variable
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

# Swagger configuration and shared schema definitions (Swagger 2.0)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "IAM Backend API",
        "description": "API documentation for authentication and task management.",
        "version": "1.0.0"
    },
    "schemes": ["http", "https"],
    "basePath": "/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
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

# Handle preflight OPTIONS requests BEFORE blueprints
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        # Allow multiple origins (localhost for dev, production URL from env)
        allowed_origins = [
            'http://localhost:5173',
            'http://localhost:3000',
            'https://s8s23kr8-5173.usw3.devtunnels.ms',
            os.environ.get('FRONTEND_URL', '')
        ]
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Cache-Control, X-Accel-Buffering, Connection'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response, 200

# CORS configuration - Apply to all responses
@app.after_request
def after_request(response):
    # Allow multiple origins (localhost for dev, production URL from env)
    allowed_origins = [
        'http://localhost:5173',
        'http://localhost:3000',
        'https://s8s23kr8-5173.usw3.devtunnels.ms',
        os.environ.get('FRONTEND_URL', '')
    ]
    origin = request.headers.get('Origin')
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Cache-Control, X-Accel-Buffering, Connection'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# Register the blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(task_routes)
app.register_blueprint(profile_routes)
app.register_blueprint(task_template_routes)
app.register_blueprint(mind_task_routes)
app.register_blueprint(body_task_routes)
app.register_blueprint(achievement_routes)
app.register_blueprint(goal_routes)
app.register_blueprint(goal_task_routes)
app.register_blueprint(goal_task_recommendation_routes)
app.register_blueprint(task_log_routes)
app.register_blueprint(failure_routes)
app.register_blueprint(bot_rule_routes)
app.register_blueprint(chat_ia_routes)
app.register_blueprint(chat_realtime_routes)
app.register_blueprint(stats_routes)
app.register_blueprint(task_recommendation_routes)
app.register_blueprint(time_optimizer_routes)

if __name__ == '__main__':
    # Get port from environment variable (Render assigns this)
    port = int(os.environ.get('PORT', 5000))
    # Set debug to False in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)