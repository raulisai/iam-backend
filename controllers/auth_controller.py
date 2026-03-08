"""Authentication controller for handling user authentication logic."""
from flask import jsonify
from lib.db import get_supabase
from services.auth_service import verify_password, generate_jwt_token, hash_password


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
        # Generate JWT token
        token = generate_jwt_token(user['id'], user['email'], user['name'])
        
        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'user': user['name'],
                'email': user['email']
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401


def register_user(email, password, name=None):
    """Register a new user with email and password.
    
    Args:
        email (str): User's email.
        password (str): User's password.
        name (str, optional): User's name.
    
    Returns:
        tuple: JSON response with user data or error, and status code.
    """
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    supabase = get_supabase()
    
    # Check if user already exists
    existing_user = supabase.from_('users_iam').select('id').eq('email', email).execute()
    if existing_user.data:
        return jsonify({'error': 'User with this email already exists'}), 409
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Insert new user
    user_data = {
        'email': email,
        'hashed_password': hashed_password,
        'name': name or email.split('@')[0]  # Default name if not provided
    }
    
    try:
        res = supabase.from_('users_iam').insert(user_data).execute()
        if res.data:
            new_user = res.data[0]
            # Generate token for the new user immediately to log them in
            token = generate_jwt_token(new_user['id'], new_user['email'], new_user['name'])
            
            return jsonify({
                'message': 'User registered successfully',
                'token': token,
                'user': {
                    'id': new_user['id'],
                    'user': new_user['name'],
                    'email': new_user['email']
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
