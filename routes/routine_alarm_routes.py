"""Routine alarm routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.routine_alarm_controller import (
    get_my_routine_alarms,
    get_routine_alarm,
    create_new_routine_alarm,
    update_routine_alarm_data,
    toggle_alarm_status,
    delete_routine_alarm_by_id
)

routine_alarm_routes = Blueprint('routine_alarms', __name__, url_prefix='/api/routine/alarms')


@routine_alarm_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_alarms():
    """Get all routine alarms for authenticated user.
    ---
    tags:
      - Routine Alarms
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: source_type
        type: string
        required: false
        description: Filter by source type
        enum: ["mind", "body", "goal", "custom"]
        example: "body"
      - in: query
        name: is_active
        type: boolean
        required: false
        description: Filter by active status
        example: true
    responses:
      200:
        description: List of routine alarms
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                format: uuid
              user_id:
                type: string
                format: uuid
              name:
                type: string
                example: "Morning Exercise Reminder"
              description:
                type: string
                example: "Daily morning workout alarm"
              source_type:
                type: string
                enum: ["mind", "body", "goal", "custom"]
                example: "body"
              task_id:
                type: string
                nullable: true
              alarm_time:
                type: string
                format: time
                example: "07:00:00"
              days_of_week:
                type: array
                items:
                  type: integer
                example: [1, 2, 3, 4, 5]
              notification_title:
                type: string
                example: "Time to Exercise!"
              notification_body:
                type: string
                example: "Start your day with a workout"
              is_active:
                type: boolean
                example: true
              created_at:
                type: string
                format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_my_routine_alarms()


@routine_alarm_routes.route('/<alarm_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_alarm(alarm_id):
    """Get specific routine alarm by ID.
    ---
    tags:
      - Routine Alarms
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: alarm_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine alarm ID
    responses:
      200:
        description: Routine alarm data
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            user_id:
              type: string
              format: uuid
            name:
              type: string
            description:
              type: string
            source_type:
              type: string
              enum: ["mind", "body", "goal", "custom"]
            task_id:
              type: string
              nullable: true
            alarm_time:
              type: string
              format: time
            days_of_week:
              type: array
              items:
                type: integer
            notification_title:
              type: string
            notification_body:
              type: string
            notification_icon:
              type: string
              nullable: true
            notification_color:
              type: string
              nullable: true
            sound_enabled:
              type: boolean
            sound_uri:
              type: string
              nullable: true
            vibration_enabled:
              type: boolean
            vibration_pattern:
              type: array
              items:
                type: integer
              nullable: true
            snooze_enabled:
              type: boolean
            snooze_duration_min:
              type: integer
            max_snoozes:
              type: integer
            priority:
              type: string
              enum: ["min", "low", "default", "high", "max"]
            can_dismiss:
              type: boolean
            auto_dismiss_minutes:
              type: integer
              nullable: true
            is_active:
              type: boolean
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Alarm belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine alarm not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_routine_alarm(alarm_id)


@routine_alarm_routes.route('/', methods=['POST'])
@token_required
def create_alarm():
    """Create new routine alarm.
    ---
    tags:
      - Routine Alarms
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Routine alarm data
        required: true
        schema:
          type: object
          required:
            - name
            - alarm_time
            - notification_title
            - notification_body
          properties:
            name:
              type: string
              example: "Morning Exercise Reminder"
              description: Name of the alarm
            description:
              type: string
              example: "Daily morning workout alarm"
              description: Optional description
            source_type:
              type: string
              enum: ["mind", "body", "goal", "custom"]
              example: "body"
              description: Type of source
            task_id:
              type: string
              example: "task-template-id"
              description: Associated task template ID
            alarm_time:
              type: string
              format: time
              example: "07:00:00"
              description: Time when alarm triggers
            days_of_week:
              type: array
              items:
                type: integer
              example: [1, 2, 3, 4, 5]
              description: Days active (0=Sun, 1=Mon, ..., 6=Sat)
            notification_title:
              type: string
              example: "Time to Exercise!"
              description: Notification title
            notification_body:
              type: string
              example: "Start your day with a workout"
              description: Notification body text
            notification_icon:
              type: string
              example: "fitness_icon"
              description: Optional notification icon
            notification_color:
              type: string
              example: "#FF5722"
              description: Optional notification color
            sound_enabled:
              type: boolean
              default: true
              description: Enable alarm sound
            sound_uri:
              type: string
              example: "alarm_sound.mp3"
              description: Custom sound URI
            vibration_enabled:
              type: boolean
              default: true
              description: Enable vibration
            vibration_pattern:
              type: array
              items:
                type: integer
              example: [300, 200, 300]
              description: Vibration pattern in milliseconds
            snooze_enabled:
              type: boolean
              default: true
              description: Enable snooze functionality
            snooze_duration_min:
              type: integer
              default: 10
              example: 10
              description: Snooze duration in minutes
            max_snoozes:
              type: integer
              default: 3
              example: 3
              description: Maximum number of snoozes
            priority:
              type: string
              enum: ["min", "low", "default", "high", "max"]
              default: "max"
              example: "max"
              description: Notification priority
            can_dismiss:
              type: boolean
              default: true
              description: Can be dismissed
            auto_dismiss_minutes:
              type: integer
              example: 5
              description: Auto dismiss after N minutes
            is_active:
              type: boolean
              default: true
              description: Alarm active status
    responses:
      201:
        description: Routine alarm created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            alarm_time:
              type: string
              format: time
            is_active:
              type: boolean
            created_at:
              type: string
              format: date-time
      400:
        description: Invalid request or missing required fields
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return create_new_routine_alarm(data)


@routine_alarm_routes.route('/<alarm_id>', methods=['PUT'])
@token_required
def update_alarm(alarm_id):
    """Update routine alarm.
    ---
    tags:
      - Routine Alarms
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: alarm_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine alarm ID
      - in: body
        name: body
        description: Updated alarm data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Updated Alarm Name"
            description:
              type: string
              example: "Updated description"
            alarm_time:
              type: string
              format: time
              example: "08:00:00"
            days_of_week:
              type: array
              items:
                type: integer
              example: [1, 2, 3, 4, 5, 6]
            notification_title:
              type: string
              example: "Updated Title"
            notification_body:
              type: string
              example: "Updated body text"
            sound_enabled:
              type: boolean
            vibration_enabled:
              type: boolean
            snooze_enabled:
              type: boolean
            snooze_duration_min:
              type: integer
            max_snoozes:
              type: integer
            priority:
              type: string
              enum: ["min", "low", "default", "high", "max"]
            is_active:
              type: boolean
    responses:
      200:
        description: Routine alarm updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            alarm_time:
              type: string
              format: time
            is_active:
              type: boolean
            updated_at:
              type: string
              format: date-time
      400:
        description: Invalid request
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Alarm belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine alarm not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_routine_alarm_data(alarm_id, data)


@routine_alarm_routes.route('/<alarm_id>/status', methods=['PATCH'])
@token_required
def update_status(alarm_id):
    """Update only the is_active status of an alarm.
    ---
    tags:
      - Routine Alarms
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: alarm_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine alarm ID
      - in: body
        name: body
        description: Status update
        required: true
        schema:
          type: object
          required:
            - is_active
          properties:
            is_active:
              type: boolean
              example: false
              description: New active status
    responses:
      200:
        description: Alarm status updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            is_active:
              type: boolean
            updated_at:
              type: string
              format: date-time
      400:
        description: Invalid request or missing is_active field
        schema:
          $ref: '#/definitions/ErrorResponse'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Alarm belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine alarm not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return toggle_alarm_status(alarm_id)


@routine_alarm_routes.route('/<alarm_id>', methods=['DELETE'])
@token_required
def delete_alarm(alarm_id):
    """Delete routine alarm.
    ---
    tags:
      - Routine Alarms
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: alarm_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine alarm ID to delete
    responses:
      200:
        description: Routine alarm deleted successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      403:
        description: Forbidden - Alarm belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine alarm not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_routine_alarm_by_id(alarm_id)
