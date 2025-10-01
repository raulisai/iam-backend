"""Authentication service for password verification and security utilities."""
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_jwt_token(user_id, email, name):
    """Generate a JWT token for the authenticated user.
    
    Args:
        user_id (int): The user's ID.
        email (str): The user's email.
        name (str): The user's name.
    
    Returns:
        str: The JWT token.
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def verify_jwt_token(token):
    """Verify and decode a JWT token.
    
    Args:
        token (str): The JWT token to verify.
    
    Returns:
        dict: The decoded token payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def verify_password(hashed_password, password):
    """Verify the given password against the hashed password.
    
    Args:
        hashed_password (str): The hashed password.
        password (str): The password to verify.
    
    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def hash_password(password):
    """Hash a password for storing.
    
    Args:
        password (str): The password to hash.
    
    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()
