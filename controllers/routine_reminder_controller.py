"""Routine reminder controller for handling reminder operations."""
from flask import jsonify, request
from services.routine_reminder_service import (
    get_user_routine_reminders,
    get_routine_reminder_by_id,
    create_routine_reminder,
    update_routine_reminder,
    update_reminder_status,
    delete_routine_reminder
)


def get_my_routine_reminders():
    """Get authenticated user's routine reminders.

    Returns:
        tuple: JSON response with reminders and status code.
    """
    user_id = request.user.get('user_id')
    source_type = request.args.get('source_type')
    is_active = request.args.get('is_active')

    # Convert is_active string to boolean if provided
    if is_active is not None:
        is_active = is_active.lower() == 'true'

    reminders = get_user_routine_reminders(user_id, source_type, is_active)
    return jsonify(reminders), 200


def get_routine_reminder(reminder_id):
    """Get routine reminder by ID.

    Args:
        reminder_id (str): Reminder ID.

    Returns:
        tuple: JSON response with reminder and status code.
    """
    reminder = get_routine_reminder_by_id(reminder_id)

    if reminder is None:
        return jsonify({'error': 'Reminder not found'}), 404

    # Verify reminder belongs to authenticated user
    user_id = request.user.get('user_id')
    if reminder.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(reminder), 200


def create_new_routine_reminder(data):
    """Create a new routine reminder.

    Args:
        data (dict): Reminder data.

    Returns:
        tuple: JSON response with created reminder and status code.
    """
    user_id = request.user.get('user_id')

    # Required fields
    required_fields = ['name', 'times_per_day', 'notification_title', 'notification_body']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Validate times_per_day
    times_per_day = data.get('times_per_day')
    is_valid = isinstance(times_per_day, int)
    is_valid = is_valid and 1 <= times_per_day <= 24
    if not is_valid:
        return jsonify({'error': 'times_per_day must be between 1 and 24'}), 400

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

    reminder = create_routine_reminder(data)

    if reminder is None:
        return jsonify({'error': 'Failed to create reminder'}), 500

    return jsonify(reminder), 201


def update_routine_reminder_data(reminder_id, data):
    """Update a routine reminder.

    Args:
        reminder_id (str): Reminder ID.
        data (dict): Updated data.

    Returns:
        tuple: JSON response with updated reminder and status code.
    """
    user_id = request.user.get('user_id')

    # Verify reminder belongs to user
    reminder = get_routine_reminder_by_id(reminder_id)
    if reminder is None:
        return jsonify({'error': 'Reminder not found'}), 404

    if reminder.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Validate times_per_day if provided
    if 'times_per_day' in data:
        times_per_day = data.get('times_per_day')
        is_valid = isinstance(times_per_day, int)
        is_valid = is_valid and 1 <= times_per_day <= 24
        if not is_valid:
            return jsonify({'error': 'times_per_day must be between 1 and 24'}), 400

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

    updated_reminder = update_routine_reminder(reminder_id, data)

    if updated_reminder is None:
        return jsonify({'error': 'Update failed'}), 500

    return jsonify(updated_reminder), 200


def toggle_reminder_status(reminder_id):
    """Toggle the is_active status of a reminder.

    Args:
        reminder_id (str): Reminder ID.

    Returns:
        tuple: JSON response with updated reminder and status code.
    """
    user_id = request.user.get('user_id')

    # Verify reminder belongs to user
    reminder = get_routine_reminder_by_id(reminder_id)
    if reminder is None:
        return jsonify({'error': 'Reminder not found'}), 404

    if reminder.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Get is_active from request body
    data = request.get_json()
    if data is None or 'is_active' not in data:
        return jsonify({'error': 'is_active is required'}), 400

    is_active = data.get('is_active')
    if not isinstance(is_active, bool):
        return jsonify({'error': 'is_active must be a boolean'}), 400

    updated_reminder = update_reminder_status(reminder_id, is_active)

    if updated_reminder is None:
        return jsonify({'error': 'Failed to update status'}), 500

    return jsonify(updated_reminder), 200


def delete_routine_reminder_by_id(reminder_id):
    """Delete a routine reminder.

    Args:
        reminder_id (str): Reminder ID.

    Returns:
        tuple: JSON response with deleted reminder and status code.
    """
    user_id = request.user.get('user_id')

    # Verify reminder belongs to user
    reminder = get_routine_reminder_by_id(reminder_id)
    if reminder is None:
        return jsonify({'error': 'Reminder not found'}), 404

    if reminder.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    deleted_reminder = delete_routine_reminder(reminder_id)

    if deleted_reminder is None:
        return jsonify({'error': 'Failed to delete reminder'}), 500

    return jsonify(deleted_reminder), 200
