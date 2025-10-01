"""Failure controller for handling failure tracking operations."""
from flask import jsonify, request
from services.failure_service import (
    get_user_failures,
    get_failure_by_id,
    create_failure,
    delete_failure
)


def get_my_failures():
    """Get authenticated user's failures.
    
    Returns:
        tuple: JSON response with failures and status code.
    """
    user_id = request.user.get('user_id')
    severity = request.args.get('severity')  # Optional filter
    
    failures = get_user_failures(user_id, severity)
    return jsonify(failures), 200


def create_failure_record(data):
    """Create a new failure record.
    
    Args:
        data (dict): Failure data.
    
    Returns:
        tuple: JSON response with created failure and status code.
    """
    user_id = request.user.get('user_id')
    data['user_id'] = user_id
    
    failure = create_failure(data)
    
    if failure is None:
        return jsonify({'error': 'Failed to create failure record'}), 500
    
    return jsonify(failure), 201


def delete_failure_by_id(failure_id):
    """Delete a failure record.
    
    Args:
        failure_id (str): Failure ID.
    
    Returns:
        tuple: JSON response with deleted failure and status code.
    """
    user_id = request.user.get('user_id')
    
    failure = get_failure_by_id(failure_id)
    if failure is None:
        return jsonify({'error': 'Failure not found'}), 404
    
    if failure.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    deleted = delete_failure(failure_id)
    
    if deleted is None:
        return jsonify({'error': 'Failed to delete failure'}), 500
    
    return jsonify(deleted), 200
