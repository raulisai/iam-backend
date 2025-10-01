"""Authentication controller for handling user authentication logic."""
from flask import jsonify
from lib.db import get_supabase
from services.auth_service import verify_password


def get_all_users():
    """Get all users from the database.
    
    Returns:
        tuple: JSON response with users data and status code.
    """
    supabase = get_supabase()
    res = supabase.from_('users_iam').select('*').execute()
    print(res)
    return jsonify(res.data), 200


def authenticate_user(email, password):
    """Authenticate a user with email and password.
    
    Args:
        email (str): User's email.
        password (str): User's password.
    
    Returns:
        tuple: JSON response with token and user data, and status code.
    """
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    supabase = get_supabase()
    res = supabase.from_('users_iam').select(
        'id, email, name, hashed_password'
    ).eq('email', email).execute()

    user = res.data[0] if res.data else None
    
    if user is not None and verify_password(user['hashed_password'], password):
        return jsonify({
            'token': user['id'],
            'user': {
                'id': user['id'],
                'user': user['name'],
                'email': user['email']
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401
