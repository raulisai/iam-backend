"""Routes module for the Flask application."""
import bcrypt
from datetime import datetime
from flask import Blueprint, request, jsonify
from lib.db import get_supabase

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)


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
    supabase = get_supabase()
    res = supabase.from_('users_iam').select('*').execute()

    print(res)
    return jsonify(res.data)

@routes.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@routes.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """Handle the login endpoint and return a valid token.
    
    Returns:
        str: A valid token for the user.
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    supabase = get_supabase()
    
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    res = supabase.from_('users_iam').select('id, email,name, hashed_password').eq('email', email).execute()

    user = res.data[0] if res.data else None
    if user is not None and verify_password(user['hashed_password'], password):
        return jsonify({'token':user['id'], 'user':{'id': user['id'], 'user': user['name'], 'email': user['email']}})
    return jsonify({'error': 'Invalid credentials'}), 401

def verify_password(hashed_password, password):
    """Verify the given password against the hashed password.
    
    Args:
        hashed_password (str): The hashed password.
        password (str): The password to verify.
    
    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


@routes.route('/api/task/create', methods=['POST', 'OPTIONS'])
def create_task():
    """Handle the task create endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    supabase = get_supabase()
    
   
    title = data.get('title')
    time = data.get('time')
    points = data.get('points')
    desc = data.get('desc')
    level = data.get('level')
    categoria = data.get('categoria')
    if not id or not title or not time or not points or not desc or not level or not categoria:
        return jsonify({'error': 'All fields are required'}), 400
    res = supabase.from_('Tasks').insert({
        'created_at': datetime.now().isoformat(), 
        'title': title, 
        'time': time, 
        'points': points, 
        'desc': desc, 
        'level': level, 
        'categoria': categoria
    }).execute()
    return jsonify(res.data)



@routes.route('/api/task/get', methods=['GET', 'OPTIONS'])
def get_tasks():
    """Handle the task get endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    supabase = get_supabase()
    res = supabase.from_('Tasks').select('*').execute()
    return jsonify(res.data)

@routes.route('/api/task/get/<id>', methods=['GET', 'OPTIONS'])
def get_task(id):
    """Handle the task get endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    supabase = get_supabase()
    res = supabase.from_('Tasks').select('*').eq('id', id).execute()
    return jsonify(res.data)

@routes.route('/api/task/update/<id>', methods=['PUT', 'OPTIONS'])
def update_task(id):
    """Handle the task update endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    supabase = get_supabase()
    res = supabase.from_('Tasks').update({
        'title': data.get('title'),
        'time': data.get('time'),
        'points': data.get('points'),
        'desc': data.get('desc'),
        'level': data.get('level'),
        'categoria': data.get('categoria')
    }).eq('id', id).execute()
    return jsonify(res.data)

@routes.route('/api/task/delete/<id>', methods=['DELETE', 'OPTIONS'])
def delete_task(id):
    """Handle the task delete endpoint and return a greeting message.
    
    Returns:
        str: A simple 'Hello World!' greeting.
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    supabase = get_supabase()
    res = supabase.from_('Tasks').delete().eq('id', id).execute()
    return jsonify(res.data)
