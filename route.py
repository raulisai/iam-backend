"""Routes module for the Flask application."""

from flask import Blueprint, request, jsonify

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)


@routes.before_request
def parse_json():
    """Handle JSON parsing before each request."""
    if request.method == 'GET':
        return
    data = request.get_json()
    if not data:
        message = {'message': 'No JSON data provided'}
        return jsonify(message), 400


@routes.route('/', methods=['GET'])
def hello_world():
    """Handle the root endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    return 'Hello World!'


@routes.route('/getusers', methods=['GET'])
def get_users():
    """Handle the user get endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    return 'Hello World!'
