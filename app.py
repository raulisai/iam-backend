"""
This is a simple Flask application that returns a greeting message
when the root endpoint is accessed.
"""

from flask import Flask
from flasgger import Swagger
from routes.auth_routes import auth_routes
from routes.task_routes import task_routes

app = Flask(__name__)

swagger = Swagger(app)

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