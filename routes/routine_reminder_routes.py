"""Routine reminder routes."""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.routine_reminder_controller import (
    get_my_routine_reminders,
    get_routine_reminder,
    create_new_routine_reminder,
    update_routine_reminder_data,
    toggle_reminder_status,
    delete_routine_reminder_by_id
)

routine_reminder_routes = Blueprint(
    'routine_reminders',
    __name__,
    url_prefix='/api/routine/reminders'
)


@routine_reminder_routes.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_reminders():
    """Get all routine reminders for authenticated user.
    ---
    tags:
      - Routine Reminders
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
        example: "mind"
      - in: query
        name: is_active
        type: boolean
        required: false
        description: Filter by active status
        example: true
    responses:
      200:
        description: List of routine reminders
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
                example: "Hydration Reminder"
              description:
                type: string
                example: "Drink water throughout the day"
              source_type:
                type: string
                enum: ["mind", "body", "goal", "custom"]
                example: "body"
              task_id:
                type: string
                nullable: true
              times_per_day:
                type: integer
                example: 8
              start_time:
                type: string
                format: time
                example: "08:00:00"
              end_time:
                type: string
                format: time
                example: "22:00:00"
              days_of_week:
                type: array
                items:
                  type: integer
                example: [1, 2, 3, 4, 5, 6, 0]
              notification_title:
                type: string
                example: "Time to Hydrate!"
              notification_body:
                type: string
                example: "Drink a glass of water"
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
    return get_my_routine_reminders()


@routine_reminder_routes.route('/<reminder_id>', methods=['GET', 'OPTIONS'])
@token_required
def get_reminder(reminder_id):
    """Get specific routine reminder by ID.
    ---
    tags:
      - Routine Reminders
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: reminder_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine reminder ID
    responses:
      200:
        description: Routine reminder data
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
            times_per_day:
              type: integer
            start_time:
              type: string
              format: time
            end_time:
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
            vibration_enabled:
              type: boolean
            priority:
              type: string
              enum: ["min", "low", "default", "high", "max"]
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
        description: Forbidden - Reminder belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine reminder not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_routine_reminder(reminder_id)


@routine_reminder_routes.route('/', methods=['POST'])
@token_required
def create_reminder():
    """Create new routine reminder.
    ---
    tags:
      - Routine Reminders
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: body
        name: body
        description: Routine reminder data
        required: true
        schema:
          type: object
          required:
            - name
            - times_per_day
            - notification_title
            - notification_body
          properties:
            name:
              type: string
              example: "Hydration Reminder"
              description: Name of the reminder
            description:
              type: string
              example: "Drink water throughout the day"
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
            times_per_day:
              type: integer
              minimum: 1
              maximum: 24
              example: 8
              description: Number of times to remind per day
            start_time:
              type: string
              format: time
              default: "08:00:00"
              example: "08:00:00"
              description: Start of reminder window
            end_time:
              type: string
              format: time
              default: "22:00:00"
              example: "22:00:00"
              description: End of reminder window
            days_of_week:
              type: array
              items:
                type: integer
              example: [1, 2, 3, 4, 5]
              description: Days active (0=Sun, 1=Mon, ..., 6=Sat)
            notification_title:
              type: string
              example: "Time to Hydrate!"
              description: Notification title
            notification_body:
              type: string
              example: "Drink a glass of water"
              description: Notification body text
            notification_icon:
              type: string
              example: "water_icon"
              description: Optional notification icon
            notification_color:
              type: string
              example: "#2196F3"
              description: Optional notification color
            sound_enabled:
              type: boolean
              default: true
              description: Enable notification sound
            vibration_enabled:
              type: boolean
              default: true
              description: Enable vibration
            priority:
              type: string
              enum: ["min", "low", "default", "high", "max"]
              default: "default"
              example: "default"
              description: Notification priority
            is_active:
              type: boolean
              default: true
              description: Reminder active status
    responses:
      201:
        description: Routine reminder created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            times_per_day:
              type: integer
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
    return create_new_routine_reminder(data)


@routine_reminder_routes.route('/<reminder_id>', methods=['PUT'])
@token_required
def update_reminder(reminder_id):
    """Update routine reminder.
    ---
    tags:
      - Routine Reminders
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: reminder_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine reminder ID
      - in: body
        name: body
        description: Updated reminder data (only include fields to update)
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Updated Reminder Name"
            description:
              type: string
              example: "Updated description"
            times_per_day:
              type: integer
              minimum: 1
              maximum: 24
              example: 10
            start_time:
              type: string
              format: time
              example: "07:00:00"
            end_time:
              type: string
              format: time
              example: "23:00:00"
            days_of_week:
              type: array
              items:
                type: integer
              example: [1, 2, 3, 4, 5, 6, 0]
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
            priority:
              type: string
              enum: ["min", "low", "default", "high", "max"]
            is_active:
              type: boolean
    responses:
      200:
        description: Routine reminder updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              format: uuid
            name:
              type: string
            times_per_day:
              type: integer
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
        description: Forbidden - Reminder belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine reminder not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    return update_routine_reminder_data(reminder_id, data)


@routine_reminder_routes.route('/<reminder_id>/status', methods=['PATCH'])
@token_required
def update_status(reminder_id):
    """Update only the is_active status of a reminder.
    ---
    tags:
      - Routine Reminders
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: reminder_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine reminder ID
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
        description: Reminder status updated successfully
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
        description: Forbidden - Reminder belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine reminder not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return toggle_reminder_status(reminder_id)


@routine_reminder_routes.route('/<reminder_id>', methods=['DELETE'])
@token_required
def delete_reminder(reminder_id):
    """Delete routine reminder.
    ---
    tags:
      - Routine Reminders
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - name: reminder_id
        in: path
        required: true
        type: string
        format: uuid
        description: Routine reminder ID to delete
    responses:
      200:
        description: Routine reminder deleted successfully
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
        description: Forbidden - Reminder belongs to another user
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Routine reminder not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    return delete_routine_reminder_by_id(reminder_id)
