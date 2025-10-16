"""Routine alarm controller for handling alarm operations."""
from flask import jsonify, request
from services.routine_alarm_service import (
    get_user_routine_alarms,
    get_routine_alarm_by_id,
    create_routine_alarm,
    update_routine_alarm,
    update_alarm_status,
    delete_routine_alarm
)


def get_my_routine_alarms():
    """Get authenticated user's routine alarms.

    Returns:
        tuple: JSON response with alarms and status code.
    """
    user_id = request.user.get('user_id')
    source_type = request.args.get('source_type')
    is_active = request.args.get('is_active')

    # Convert is_active string to boolean if provided
    if is_active is not None:
        is_active = is_active.lower() == 'true'

    alarms = get_user_routine_alarms(user_id, source_type, is_active)
    return jsonify(alarms), 200


def get_routine_alarm(alarm_id):
    """Get routine alarm by ID.

    Args:
        alarm_id (str): Alarm ID.

    Returns:
        tuple: JSON response with alarm and status code.
    """
    alarm = get_routine_alarm_by_id(alarm_id)

    if alarm is None:
        return jsonify({'error': 'Alarm not found'}), 404

    # Verify alarm belongs to authenticated user
    user_id = request.user.get('user_id')
    if alarm.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(alarm), 200


def create_new_routine_alarm(data):
    """Create a new routine alarm.

    Args:
        data (dict): Alarm data.

    Returns:
        tuple: JSON response with created alarm and status code.
    """
    user_id = request.user.get('user_id')

    # Required fields
    required_fields = ['name', 'alarm_time', 'notification_title', 'notification_body']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Validate source_type if provided
    valid_sources = ['mind', 'body', 'goal', 'custom', None]
    if 'source_type' in data and data['source_type'] not in valid_sources:
        error_msg = 'Invalid source_type. Must be: mind, body, goal, or custom'
        return jsonify({'error': error_msg}), 400

    # Validate priority if provided
    valid_priorities = ['min', 'low', 'default', 'high', 'max']
    if 'priority' in data and data['priority'] not in valid_priorities:
        error_msg = 'Invalid priority. Must be: min, low, default, high, or max'
        return jsonify({'error': error_msg}), 400

    # Add user_id to data
    data['user_id'] = user_id

    alarm = create_routine_alarm(data)

    if alarm is None:
        return jsonify({'error': 'Failed to create alarm'}), 500

    return jsonify(alarm), 201


def update_routine_alarm_data(alarm_id, data):
    """Update a routine alarm.

    Args:
        alarm_id (str): Alarm ID.
        data (dict): Updated data.

    Returns:
        tuple: JSON response with updated alarm and status code.
    """
    user_id = request.user.get('user_id')

    # Verify alarm belongs to user
    alarm = get_routine_alarm_by_id(alarm_id)
    if alarm is None:
        return jsonify({'error': 'Alarm not found'}), 404

    if alarm.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Validate source_type if provided
    valid_sources = ['mind', 'body', 'goal', 'custom', None]
    if 'source_type' in data and data['source_type'] not in valid_sources:
        error_msg = 'Invalid source_type. Must be: mind, body, goal, or custom'
        return jsonify({'error': error_msg}), 400

    # Validate priority if provided
    valid_priorities = ['min', 'low', 'default', 'high', 'max']
    if 'priority' in data and data['priority'] not in valid_priorities:
        error_msg = 'Invalid priority. Must be: min, low, default, high, or max'
        return jsonify({'error': error_msg}), 400

    # Remove immutable fields
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('created_at', None)

    updated_alarm = update_routine_alarm(alarm_id, data)

    if updated_alarm is None:
        return jsonify({'error': 'Update failed'}), 500

    return jsonify(updated_alarm), 200


def toggle_alarm_status(alarm_id):
    """Toggle the is_active status of an alarm.

    Args:
        alarm_id (str): Alarm ID.

    Returns:
        tuple: JSON response with updated alarm and status code.
    """
    user_id = request.user.get('user_id')

    # Verify alarm belongs to user
    alarm = get_routine_alarm_by_id(alarm_id)
    if alarm is None:
        return jsonify({'error': 'Alarm not found'}), 404

    if alarm.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Get is_active from request body
    data = request.get_json()
    if data is None or 'is_active' not in data:
        return jsonify({'error': 'is_active is required'}), 400

    is_active = data.get('is_active')
    if not isinstance(is_active, bool):
        return jsonify({'error': 'is_active must be a boolean'}), 400

    updated_alarm = update_alarm_status(alarm_id, is_active)

    if updated_alarm is None:
        return jsonify({'error': 'Failed to update status'}), 500

    return jsonify(updated_alarm), 200


def delete_routine_alarm_by_id(alarm_id):
    """Delete a routine alarm.

    Args:
        alarm_id (str): Alarm ID.

    Returns:
        tuple: JSON response with deleted alarm and status code.
    """
    user_id = request.user.get('user_id')

    # Verify alarm belongs to user
    alarm = get_routine_alarm_by_id(alarm_id)
    if alarm is None:
        return jsonify({'error': 'Alarm not found'}), 404

    if alarm.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    deleted_alarm = delete_routine_alarm(alarm_id)

    if deleted_alarm is None:
        return jsonify({'error': 'Failed to delete alarm'}), 500

    return jsonify(deleted_alarm), 200
