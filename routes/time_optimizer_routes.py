"""Routes for time optimization and intelligent task scheduling.

These endpoints help users maximize their productivity by:
- Calculating real available time
- Generating optimized daily schedules
- Recommending tasks for current moment
- Managing remaining day efficiently
"""

from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from controllers.time_optimizer_controller import (
    get_available_time,
    get_optimized_daily_schedule,
    get_tasks_right_now,
    get_remaining_day_schedule
)

time_optimizer_routes = Blueprint('time_optimizer', __name__, url_prefix='/api/time-optimizer')


@time_optimizer_routes.route('/available-time', methods=['GET', 'OPTIONS'])
@token_required
def available_time():
    """Get comprehensive time availability information.
    ---
    tags:
      - Time Optimizer
    summary: Calculate available time for user
    description: |
      Calculates the user's available time by:
      - Reading profile hours per week
      - Considering work schedule
      - Removing fixed hours (sleep, work, personal care)
      - Breaking down by morning/evening slots
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: Time availability information
        schema:
          type: object
          properties:
            user_id:
              type: string
              format: uuid
            has_profile:
              type: boolean
            profile:
              type: object
              properties:
                work_schedule:
                  type: string
                  example: "9:00-17:00"
                work_start:
                  type: string
                  example: "09:00"
                work_end:
                  type: string
                  example: "17:00"
                hours_per_week:
                  type: number
                  example: 40
                hours_used_this_week:
                  type: number
                  example: 12.5
                remaining_hours_this_week:
                  type: number
                  example: 27.5
            daily_breakdown:
              type: object
              properties:
                total_hours:
                  type: integer
                  example: 24
                sleep_hours:
                  type: integer
                  example: 8
                work_hours:
                  type: number
                  example: 8
                personal_care_hours:
                  type: number
                  example: 2
                fixed_hours_total:
                  type: number
                  example: 18
                free_hours_available:
                  type: number
                  example: 6
                avg_study_hours_per_day:
                  type: number
                  example: 5.71
            time_slots:
              type: object
              properties:
                morning:
                  type: object
                  properties:
                    start:
                      type: string
                      example: "06:00"
                    end:
                      type: string
                      example: "09:00"
                    duration_hours:
                      type: number
                      example: 2
                evening:
                  type: object
                  properties:
                    start:
                      type: string
                      example: "17:00"
                    end:
                      type: string
                      example: "22:00"
                    duration_hours:
                      type: number
                      example: 5
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Internal server error
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_available_time()


@time_optimizer_routes.route('/optimize-day', methods=['GET', 'OPTIONS'])
@token_required
def optimize_day():
    """Generate optimized schedule for a specific day.
    ---
    tags:
      - Time Optimizer
    summary: Get optimized daily task schedule
    description: |
      Generates an intelligent schedule that:
      - Prioritizes goal tasks (especially those with approaching deadlines)
      - Balances mind and body tasks
      - Distributes tasks across morning and evening slots
      - Maximizes productivity within available time
      - Considers task duration and urgency
      
      The algorithm uses sophisticated scoring based on:
      - Task type (goals have 3x weight vs mind/body)
      - Deadline urgency (tasks due soon get higher priority)
      - Time of day (focus tasks in morning, physical in evening)
      - Task duration vs available time
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
      - in: query
        name: date
        type: string
        format: date
        description: Target date (ISO format YYYY-MM-DD). Defaults to today.
        required: false
        example: "2025-10-09"
    responses:
      200:
        description: Optimized daily schedule
        schema:
          type: object
          properties:
            user_id:
              type: string
              format: uuid
            date:
              type: string
              format: date
            generated_at:
              type: string
              format: date-time
            profile_summary:
              type: object
              properties:
                work_schedule:
                  type: string
                daily_free_hours:
                  type: number
                weekly_hours_remaining:
                  type: number
            schedule:
              type: object
              properties:
                morning:
                  type: object
                  properties:
                    time_range:
                      type: string
                      example: "06:00 - 09:00"
                    available_hours:
                      type: number
                    available_minutes:
                      type: integer
                    scheduled_minutes:
                      type: integer
                    remaining_minutes:
                      type: integer
                    tasks:
                      type: array
                      items:
                        type: object
                        properties:
                          id:
                            type: string
                          title:
                            type: string
                          type:
                            type: string
                            enum: ["goal", "mind", "body"]
                          estimated_duration_minutes:
                            type: integer
                          start_time:
                            type: string
                            format: date-time
                          end_time:
                            type: string
                            format: date-time
                          time_slot:
                            type: string
                          priority_score:
                            type: number
                          urgency_multiplier:
                            type: number
                          days_until_deadline:
                            type: integer
                            nullable: true
                evening:
                  type: object
                  properties:
                    time_range:
                      type: string
                    available_hours:
                      type: number
                    tasks:
                      type: array
                      items:
                        type: object
            summary:
              type: object
              properties:
                total_tasks_available:
                  type: integer
                tasks_by_type_available:
                  type: object
                total_tasks_scheduled:
                  type: integer
                tasks_by_type_scheduled:
                  type: object
                total_minutes_available:
                  type: integer
                total_minutes_scheduled:
                  type: integer
                total_hours_scheduled:
                  type: number
                efficiency_percentage:
                  type: number
                  description: Percentage of available time utilized
                unscheduled_tasks:
                  type: integer
            distribution_analysis:
              type: object
              properties:
                actual_distribution:
                  type: object
                  description: Actual percentage of time per task type
                ideal_distribution:
                  type: object
                  description: Ideal percentage (60% goals, 20% mind, 20% body)
                deviation_from_ideal:
                  type: object
                balance_score:
                  type: number
                  description: How close to ideal distribution (0-100)
            scores:
              type: object
              properties:
                efficiency_score:
                  type: number
                  description: Time utilization score (0-100)
                balance_score:
                  type: number
                  description: Task type balance score (0-100)
                productivity_score:
                  type: number
                  description: Overall productivity score (0-100)
            algorithm_info:
              type: object
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Failed to generate schedule
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_optimized_daily_schedule()


@time_optimizer_routes.route('/tasks-now', methods=['GET', 'OPTIONS'])
@token_required
def tasks_now():
    """Get tasks recommended for RIGHT NOW with aggressive scheduling.
    ---
    tags:
      - Time Optimizer
    summary: Get optimized tasks for remaining time today
    description: |
      Returns intelligently scheduled tasks for the rest of today based on:
      - User's timezone (e.g., America/Mexico_City)
      - Work days configuration (day_work field)
      - Time dead (sleep, personal care hours)
      - Current time until midnight
      - Available time calculation: (24 - work_hours - time_dead)
      
      **Aggressive Scheduling Algorithm:**
      - Priority 1: GOAL tasks (all that fit - most important)
      - Priority 2: MIND tasks (fill remaining time - development)
      - Priority 3: BODY tasks (use any final gaps - wellness)
      - Aims for 85-95% time utilization
      - 10-minute buffers between tasks
      - No artificial limits on task counts
      
      Perfect for "What should I do for the rest of today?" scenarios.
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: Scheduled tasks for remaining time today
        schema:
          type: object
          properties:
            body_tasks:
              type: array
              description: Scheduled body/wellness tasks
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  task_id:
                    type: string
                    format: uuid
                  title:
                    type: string
                    example: "Yoga Matutino"
                  description:
                    type: string
                  type:
                    type: string
                    enum: ["body"]
                  estimated_duration_minutes:
                    type: integer
                    example: 30
                  priority_score:
                    type: number
                    example: 20
                  urgency_multiplier:
                    type: number
                    example: 1
                  scheduled_at:
                    type: string
                    format: date-time
                    nullable: true
                  status:
                    type: string
                    example: "pending"
                  start_time:
                    type: string
                    format: date-time
                    example: "2025-10-12T20:30:00-06:00"
                  end_time:
                    type: string
                    format: date-time
                    example: "2025-10-12T21:00:00-06:00"
                  time_slot:
                    type: string
                    enum: ["morning", "afternoon", "evening"]
            goal_tasks:
              type: array
              description: Scheduled goal tasks (highest priority)
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  task_id:
                    type: string
                    format: uuid
                  title:
                    type: string
                    example: "Planificación del proyecto IAM"
                  description:
                    type: string
                  type:
                    type: string
                    enum: ["goal"]
                  goal_title:
                    type: string
                    example: "Finish web IAM"
                  goal_deadline:
                    type: string
                    format: date
                    example: "2025-10-29"
                  days_until_deadline:
                    type: integer
                    example: 17
                  urgency_multiplier:
                    type: number
                    example: 1
                  weight:
                    type: integer
                    example: 100000
                  estimated_duration_minutes:
                    type: integer
                    example: 60
                  priority_score:
                    type: number
                    example: 3000002
                  scheduled_at:
                    type: string
                    format: date-time
                    nullable: true
                  status:
                    type: string
                    example: "pending"
                  start_time:
                    type: string
                    format: date-time
                  end_time:
                    type: string
                    format: date-time
                  time_slot:
                    type: string
            mind_tasks:
              type: array
              description: Scheduled mind/development tasks
              items:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  task_id:
                    type: string
                    format: uuid
                  title:
                    type: string
                    example: "Networking Profesional"
                  description:
                    type: string
                  type:
                    type: string
                    enum: ["mind"]
                  estimated_duration_minutes:
                    type: integer
                    example: 30
                  priority_score:
                    type: number
                  urgency_multiplier:
                    type: number
                  scheduled_at:
                    type: string
                    format: date-time
                    nullable: true
                  status:
                    type: string
                  start_time:
                    type: string
                    format: date-time
                  end_time:
                    type: string
                    format: date-time
                  time_slot:
                    type: string
            current_time:
              type: string
              format: date-time
              description: Current time in user's timezone
              example: "2025-10-12T21:00:00-06:00"
            message:
              type: string
              example: "You have 180 minutes remaining today. 170 minutes scheduled (94% utilization)."
            remaining_hours_in_slot_week:
              type: number
              description: Remaining hours available this week
              example: 27.5
            remaining_minutes_today:
              type: integer
              description: Minutes from now until midnight
              example: 180
            remaining_hours_today:
              type: number
              description: Hours from now until midnight (decimal)
              example: 3.0
            total_body_tasks:
              type: integer
              description: Number of body tasks scheduled
              example: 2
            total_goal_tasks:
              type: integer
              description: Number of goal tasks scheduled
              example: 3
            total_mind_tasks:
              type: integer
              description: Number of mind tasks scheduled
              example: 1
            total_time_used_for_tasks:
              type: integer
              description: Total minutes of scheduled tasks
              example: 170
            remaining_minutes_in_slot_week:
              type: integer
              description: Minutes available this week
              example: 1650
            remaining_after_scheduling:
              type: integer
              description: Free time after all scheduled tasks
              example: 10
            utilization_percentage:
              type: number
              description: Percentage of available time being used (85-95% target)
              example: 94.4
            total_available_tasks:
              type: integer
              description: Total tasks available in database
              example: 17
            total_scheduled_tasks:
              type: integer
              description: Total tasks that fit in remaining time
              example: 6
            user_id:
              type: string
              format: uuid
            is_working_day:
              type: boolean
              description: Whether today is a working day (based on day_work field)
              example: false
            available_hours_today:
              type: number
              description: Total hours available today (24 - work_hours - time_dead)
              example: 15
            work_hours_today:
              type: number
              description: Work hours today (0 if not working day)
              example: 0
            time_dead:
              type: number
              description: Time dead from profile (sleep, etc.)
              example: 9
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Failed to get current tasks
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_tasks_right_now()


@time_optimizer_routes.route('/remaining-day', methods=['GET', 'OPTIONS'])
@token_required
def remaining_day():
    """Get optimized schedule for remaining part of today.
    ---
    tags:
      - Time Optimizer
    summary: Get schedule for rest of today
    description: |
      Returns the optimized schedule for the remaining part of today.
      Shows:
      - How much productive time is left
      - Which tasks are still pending
      - Whether all tasks can be completed today
      - Current completion progress
      
      Useful for checking in during the day to see what's left.
    parameters:
      - in: header
        name: Authorization
        description: JWT token (Bearer <token>)
        required: true
        type: string
    responses:
      200:
        description: Remaining day schedule
        schema:
          type: object
          properties:
            user_id:
              type: string
              format: uuid
            current_time:
              type: string
              format: date-time
            remaining_productive_hours:
              type: number
              description: Hours left until end of productive day
            remaining_productive_minutes:
              type: integer
            remaining_tasks:
              type: array
              description: Tasks that haven't been completed yet
              items:
                type: object
                properties:
                  id:
                    type: string
                  title:
                    type: string
                  type:
                    type: string
                  estimated_duration_minutes:
                    type: integer
                  start_time:
                    type: string
                    format: date-time
            total_remaining_tasks:
              type: integer
            total_remaining_task_minutes:
              type: integer
            can_complete_all:
              type: boolean
              description: Whether all remaining tasks can fit in remaining time
            completion_percentage:
              type: number
              description: Percentage of day's tasks already scheduled/completed
            full_day_summary:
              type: object
              description: Summary of the full day schedule
      401:
        description: Unauthorized
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Profile not found
        schema:
          $ref: '#/definitions/ErrorResponse'
      500:
        description: Failed to get remaining day schedule
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return get_remaining_day_schedule()
