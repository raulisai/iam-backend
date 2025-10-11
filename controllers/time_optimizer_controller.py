"""Time optimizer controller for handling time optimization requests.

This controller provides multiple endpoints for different time management scenarios:
1. Available time calculation
2. Full day schedule optimization
3. Current moment task recommendations
4. Remaining day optimization
"""

from flask import jsonify, request
from services.time_optimizer_service import (
    get_user_profile_info,
    optimize_daily_schedule,
    get_tasks_for_current_moment
)
from datetime import datetime


def get_available_time():
    """Get comprehensive available time information for user.
    
    Returns:
        JSON response with time availability breakdown
    """
    user_id = request.user.get('user_id')
    
    try:
        time_info = get_user_profile_info(user_id)
        
        if 'error' in time_info:
            return jsonify(time_info), 404
        
        return jsonify(time_info), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to calculate available time',
            'message': str(e)
        }), 500


def get_optimized_daily_schedule():
    """Generate optimized schedule for a specific day.
    
    Query Parameters:
        date: ISO date string (optional, defaults to today)
    
    Returns:
        JSON response with optimized daily schedule
    """
    user_id = request.user.get('user_id')
    target_date = request.args.get('date')
    
    try:
        schedule = optimize_daily_schedule(user_id, target_date)
        
        if 'error' in schedule:
            return jsonify(schedule), 404
        
        return jsonify(schedule), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to generate optimized schedule',
            'message': str(e)
        }), 500


def get_tasks_right_now():
    """Get tasks recommended for the current moment.
    
    Returns:
        JSON response with tasks that can be done right now
    """
    user_id = request.user.get('user_id')
    
    try:
        tasks = get_tasks_for_current_moment(user_id)
        
        if 'error' in tasks:
            return jsonify(tasks), 404
        
        return jsonify(tasks), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get current tasks',
            'message': str(e)
        }), 500


def get_remaining_day_schedule():
    """Get optimized schedule for the remaining part of today.
    
    This is similar to the daily schedule but starts from current time.
    
    Returns:
        JSON response with remaining day schedule
    """
    user_id = request.user.get('user_id')
    
    try:
        current_time = datetime.utcnow()
        today = current_time.date().isoformat()
        
        # Get full day schedule
        full_schedule = optimize_daily_schedule(user_id, today, current_time)
        
        if 'error' in full_schedule:
            return jsonify(full_schedule), 404
        
        # Filter to only future tasks
        morning_tasks = full_schedule['schedule']['morning']['tasks']
        evening_tasks = full_schedule['schedule']['evening']['tasks']
        
        remaining_tasks = []
        
        for task in morning_tasks + evening_tasks:
            task_start = datetime.fromisoformat(task['start_time'].replace('Z', '+00:00'))
            if task_start >= current_time:
                remaining_tasks.append(task)
        
        # Calculate remaining time
        current_hour = current_time.hour
        work_schedule = full_schedule['profile_summary']['work_schedule']
        work_end_h = int(work_schedule.split('-')[1].split(':')[0])
        
        if current_hour < work_end_h:
            # Still in work or before
            remaining_productive_hours = 22 - work_end_h  # Until 10 PM
        else:
            # In evening slot
            remaining_productive_hours = 22 - current_hour
        
        remaining_productive_minutes = max(0, (remaining_productive_hours * 60) - current_time.minute)
        
        # Calculate what can still be done
        total_remaining_task_minutes = sum(t['estimated_duration_minutes'] for t in remaining_tasks)
        
        return jsonify({
            'user_id': user_id,
            'current_time': current_time.isoformat(),
            'remaining_productive_hours': round(remaining_productive_minutes / 60, 2),
            'remaining_productive_minutes': remaining_productive_minutes,
            'remaining_tasks': remaining_tasks,
            'total_remaining_tasks': len(remaining_tasks),
            'total_remaining_task_minutes': total_remaining_task_minutes,
            'can_complete_all': total_remaining_task_minutes <= remaining_productive_minutes,
            'completion_percentage': round((len(full_schedule['summary']['total_tasks_scheduled']) - len(remaining_tasks)) / len(full_schedule['summary']['total_tasks_scheduled']) * 100, 1) if full_schedule['summary']['total_tasks_scheduled'] > 0 else 0,
            'full_day_summary': full_schedule['summary']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get remaining day schedule',
            'message': str(e)
        }), 500
