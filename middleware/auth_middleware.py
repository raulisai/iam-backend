"""Middleware for JWT authentication and route protection."""
from functools import wraps
from flask import request, jsonify
from services.auth_service import verify_jwt_token


def token_required(f):
    """Decorator to protect routes with JWT authentication.
    
    This decorator verifies the JWT token in the Authorization header
    and adds the decoded user information to the request context.
    
    Usage:
        @token_required
        def protected_route():
            # Access user info via request.user
            user_id = request.user['user_id']
            return jsonify({'message': 'Protected data'})
    
    Args:
        f: The function to wrap.
    
    Returns:
        The wrapped function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        # Verify the token
        payload = verify_jwt_token(token)
        
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user information to request context
        request.user = payload
        
        return f(*args, **kwargs)
    
    return decorated
