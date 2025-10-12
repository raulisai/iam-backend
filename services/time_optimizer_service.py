"""Time optimizer service for calculating available time and optimal task distribution.

This service implements a sophisticated algorithm to maximize user productivity by:
1. Calculating real available time after fixed activities (work, sleep, personal care)
2. Prioritizing tasks by type (goals > mind/body) and deadline urgency
3. Distributing tasks optimally across available time slots
4. Considering weekly study hour limits from user profile
"""

from lib.db import get_supabase
from datetime import datetime, timedelta, time as dt_time
from typing import Dict, List, Any, Tuple, Optional
import pytz


# ==================== CONSTANTES DEL ALGORITMO ====================

# Horas fijas diarias (trabajo + sueño + aseo/comida/transporte)
FIXED_HOURS_DEFAULT = 9
SLEEP_HOURS = 8
PERSONAL_CARE_HOURS = 2  # Aseo, comida, transporte, etc.

# Buffer entre tareas (tiempo de descanso/transición)
BUFFER_MINUTES = 15

# Pesos de prioridad por tipo de tarea
PRIORITY_WEIGHTS = {
    'goal': 3.0,      # Máxima prioridad - metas del usuario
    'mind': 1.5,      # Media prioridad - desarrollo mental
    'body': 1.5       # Media prioridad - actividad física
}

# Distribución ideal de tareas (porcentajes)
IDEAL_DISTRIBUTION = {
    'goal': 0.60,     # 60% del tiempo a metas
    'mind': 0.20,     # 20% a tareas mentales
    'body': 0.20      # 20% a actividad física
}

# Horarios predeterminados
DEFAULT_WORK_START = 9
DEFAULT_WORK_END = 17
DEFAULT_WAKE_UP = 6
DEFAULT_SLEEP_TIME = 22


# ==================== FUNCIONES DE UTILIDAD ====================

def parse_time_string(time_str: str) -> Tuple[int, int]:
    """Parse time string like '9:00' or '17:30' to (hour, minute).
    
    Args:
        time_str: Time string in format 'HH:MM'
        
    Returns:
        Tuple of (hour, minute)
    """
    try:
        parts = time_str.split(':')
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    except:
        return (9, 0)


def parse_time_range(time_range: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Parse time range string like '9:00-17:00' to ((start_h, start_m), (end_h, end_m)).
    
    Args:
        time_range: Time range string in format 'HH:MM-HH:MM'
        
    Returns:
        Tuple of ((start_hour, start_minute), (end_hour, end_minute))
    """
    try:
        start, end = time_range.split('-')
        return (parse_time_string(start), parse_time_string(end))
    except:
        return ((DEFAULT_WORK_START, 0), (DEFAULT_WORK_END, 0))


def time_to_decimal_hours(hour: int, minute: int = 0) -> float:
    """Convert time to decimal hours.
    
    Args:
        hour: Hour (0-23)
        minute: Minute (0-59)
        
    Returns:
        Decimal hours (e.g., 9:30 -> 9.5)
    """
    return hour + (minute / 60.0)


def calculate_duration_hours(start_time: Tuple[int, int], end_time: Tuple[int, int]) -> float:
    """Calculate duration in hours between two times.
    
    Args:
        start_time: (hour, minute)
        end_time: (hour, minute)
        
    Returns:
        Duration in decimal hours
    """
    start_decimal = time_to_decimal_hours(*start_time)
    end_decimal = time_to_decimal_hours(*end_time)
    return max(0, end_decimal - start_decimal)


def get_days_until_deadline(deadline_str: str, reference_date: datetime = None) -> Optional[int]:
    """Calculate days until deadline from reference date.
    
    Args:
        deadline_str: ISO format date string or datetime string
        reference_date: Reference date (defaults to now)
        
    Returns:
        Number of days until deadline, or None if no deadline
    """
    if not deadline_str:
        return None
    
    try:
        deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        ref = reference_date or datetime.utcnow()
        delta = deadline - ref
        return delta.days
    except:
        return None


# ==================== ANÁLISIS DE PERFIL Y DISPONIBILIDAD ====================

def get_user_profile_info(user_id: str) -> Dict[str, Any]:
    """Get comprehensive user profile information including time availability.
    
    Args:
        user_id: User ID
        
    Returns:
        Dictionary with profile information and calculated availability
    """
    supabase = get_supabase()
    
    # Get user profile
    profile_res = supabase.from_('profiles').select('*').eq('user_id', user_id).execute()
    
    if not profile_res.data:
        return {
            'error': 'Profile not found',
            'message': 'Please create a profile first',
            'has_profile': False
        }
    
    profile = profile_res.data[0]
    
    # Extract relevant fields
    hours_per_week = profile.get('hours_available_to_week', 40)
    hours_used = profile.get('hours_used_to_week', 0)
    work_schedule = profile.get('work_schedules', '9:00-17:00')
    
    # Parse work schedule
    (work_start_h, work_start_m), (work_end_h, work_end_m) = parse_time_range(work_schedule)
    work_hours = calculate_duration_hours((work_start_h, work_start_m), (work_end_h, work_end_m))
    
    # Calculate daily free hours
    total_day_hours = 24
    fixed_hours = SLEEP_HOURS + work_hours + PERSONAL_CARE_HOURS
    free_hours_per_day = max(0, total_day_hours - fixed_hours)
    
    # Weekly calculations
    remaining_hours_this_week = max(0, hours_per_week - hours_used)
    avg_study_hours_per_day = hours_per_week / 7.0
    
    return {
        'user_id': user_id,
        'has_profile': True,
        'profile': {
            'work_schedule': work_schedule,
            'work_start': f"{work_start_h:02d}:{work_start_m:02d}",
            'work_end': f"{work_end_h:02d}:{work_end_m:02d}",
            'hours_per_week': hours_per_week,
            'hours_used_this_week': hours_used,
            'remaining_hours_this_week': remaining_hours_this_week
        },
        'daily_breakdown': {
            'total_hours': 24,
            'sleep_hours': SLEEP_HOURS,
            'work_hours': work_hours,
            'personal_care_hours': PERSONAL_CARE_HOURS,
            'fixed_hours_total': fixed_hours,
            'free_hours_available': round(free_hours_per_day, 2),
            'avg_study_hours_per_day': round(avg_study_hours_per_day, 2)
        },
        'time_slots': {
            'morning': {
                'start': f"{DEFAULT_WAKE_UP:02d}:00",
                'end': f"{work_start_h:02d}:{work_start_m:02d}",
                'duration_hours': calculate_duration_hours((DEFAULT_WAKE_UP, 0), (work_start_h, work_start_m)) - 1  # -1 for getting ready
            },
            'evening': {
                'start': f"{work_end_h:02d}:{work_end_m:02d}",
                'end': f"{DEFAULT_SLEEP_TIME:02d}:00",
                'duration_hours': calculate_duration_hours((work_end_h, work_end_m), (DEFAULT_SLEEP_TIME, 0))
            }
        }
    }


# ==================== OBTENCIÓN DE TAREAS PENDIENTES ====================

def get_pending_tasks_all_types(user_id: str, target_date: str = None, include_unscheduled: bool = True) -> Dict[str, List[Dict]]:
    """Get all pending tasks organized by type (goals, mind, body) for a specific date.
    
    Args:
        user_id: User ID
        target_date: ISO date string (defaults to today)
        include_unscheduled: If True, includes tasks without specific schedule dates
        
    Returns:
        Dictionary with tasks organized by type, each with priority calculations
    """
    supabase = get_supabase()
    
    # Determine target date
    if target_date:
        try:
            date_obj = datetime.fromisoformat(target_date.replace('Z', '+00:00')).date()
        except:
            date_obj = datetime.utcnow().date()
    else:
        date_obj = datetime.utcnow().date()
    
    date_start = datetime.combine(date_obj, dt_time.min)
    date_end = datetime.combine(date_obj, dt_time.max)
    
    tasks_by_type = {
        'goals': [],
        'mind': [],
        'body': []
    }
    
    # ==================== GOAL TASKS ====================
    try:
        # Get goal task occurrences for the target date
        occurrences_res = supabase.from_('task_occurrences').select(
            'id, task_id, scheduled_at, goal_tasks!inner(id, title, description, type, weight, goal_id, goals(title, end_date))'
        ).gte('scheduled_at', date_start.isoformat()).lte('scheduled_at', date_end.isoformat()).execute()
        
        if occurrences_res.data:
            for occ in occurrences_res.data:
                task_info = occ.get('goal_tasks', {})
                goal_info = task_info.get('goals', {}) if task_info else {}
                
                if task_info:
                    # Calculate deadline urgency
                    goal_deadline = goal_info.get('end_date') if goal_info else None
                    days_until_deadline = get_days_until_deadline(goal_deadline, date_start)
                    
                    # Calculate urgency multiplier (closer deadline = higher urgency)
                    urgency_multiplier = 1.0
                    if days_until_deadline is not None:
                        if days_until_deadline <= 1:
                            urgency_multiplier = 3.0  # Vence hoy o mañana
                        elif days_until_deadline <= 3:
                            urgency_multiplier = 2.5  # Vence en 2-3 días
                        elif days_until_deadline <= 7:
                            urgency_multiplier = 2.0  # Vence esta semana
                        elif days_until_deadline <= 14:
                            urgency_multiplier = 1.5  # Vence en 2 semanas
                    
                    tasks_by_type['goals'].append({
                        'id': occ['id'],
                        'task_id': task_info.get('id'),
                        'title': task_info.get('title', 'Goal Task'),
                        'description': task_info.get('description', ''),
                        'type': 'goal',
                        'goal_title': goal_info.get('title', '') if goal_info else '',
                        'goal_deadline': goal_deadline,
                        'days_until_deadline': days_until_deadline,
                        'urgency_multiplier': urgency_multiplier,
                        'weight': task_info.get('weight', 1),
                        'estimated_duration_minutes': 60,  # Default 1 hour
                        'scheduled_at': occ.get('scheduled_at'),
                        'status': 'pending'
                    })
        
        # Also get goal tasks without occurrences if include_unscheduled is True
        if include_unscheduled:
            goal_tasks_res = supabase.from_('goal_tasks').select(
                'id, title, description, type, weight, goal_id, user_id, goals(title, end_date)'
            ).eq('user_id', user_id).execute()
            
            if goal_tasks_res.data:
                # Get IDs of tasks already scheduled
                scheduled_task_ids = {t['task_id'] for t in tasks_by_type['goals'] if t.get('task_id')}
                
                for task_info in goal_tasks_res.data:
                    # Skip if already scheduled
                    if task_info.get('id') in scheduled_task_ids:
                        continue
                    
                    goal_info = task_info.get('goals', {})
                    goal_deadline = goal_info.get('end_date') if goal_info else None
                    days_until_deadline = get_days_until_deadline(goal_deadline, date_start)
                    
                    # Calculate urgency multiplier
                    urgency_multiplier = 1.0
                    if days_until_deadline is not None:
                        if days_until_deadline <= 1:
                            urgency_multiplier = 3.0
                        elif days_until_deadline <= 3:
                            urgency_multiplier = 2.5
                        elif days_until_deadline <= 7:
                            urgency_multiplier = 2.0
                        elif days_until_deadline <= 14:
                            urgency_multiplier = 1.5
                    
                    tasks_by_type['goals'].append({
                        'id': task_info.get('id'),
                        'task_id': task_info.get('id'),
                        'title': task_info.get('title', 'Goal Task'),
                        'description': task_info.get('description', ''),
                        'type': 'goal',
                        'goal_title': goal_info.get('title', '') if goal_info else '',
                        'goal_deadline': goal_deadline,
                        'days_until_deadline': days_until_deadline,
                        'urgency_multiplier': urgency_multiplier,
                        'weight': task_info.get('weight', 1),
                        'estimated_duration_minutes': 60,
                        'scheduled_at': None,
                        'status': 'pending'
                    })
    except Exception as e:
        print(f"Error fetching goal tasks: {e}")
    
    # ==================== MIND TASKS ====================
    try:
        mind_res = supabase.from_('tasks_mind').select(
            'id, template_id, status, scheduled_at, task_templates(name, estimated_minutes)'
        ).eq('user_id', user_id).in_('status', ['pending', 'in_progress']).execute()
        
        if mind_res.data:
            for task in mind_res.data:
                # Check if scheduled for target date, overdue, or no specific schedule
                task_scheduled_at = task.get('scheduled_at')
                should_include = False
                
                if task_scheduled_at:
                    task_date = datetime.fromisoformat(task_scheduled_at.replace('Z', '+00:00')).date()
                    # Include if scheduled for today OR overdue (scheduled in the past)
                    if task_date <= date_obj:
                        should_include = True
                elif include_unscheduled:
                    # Include tasks without specific schedule
                    should_include = True
                
                if not should_include:
                    continue
                
                template = task.get('task_templates', {})
                estimated_minutes = template.get('estimated_minutes', 30)
                
                tasks_by_type['mind'].append({
                    'id': task['id'],
                    'task_id': task['id'],
                    'title': template.get('name', 'Mind Task'),
                    'description': '',
                    'type': 'mind',
                    'estimated_duration_minutes': estimated_minutes,
                    'scheduled_at': task_scheduled_at,
                    'status': task.get('status', 'pending'),
                    'urgency_multiplier': 1.0  # Default, no deadline
                })
    except Exception as e:
        print(f"Error fetching mind tasks: {e}")
    
    # ==================== BODY TASKS ====================
    try:
        body_res = supabase.from_('tasks_body').select(
            'id, template_id, status, scheduled_at, task_templates(name, estimated_minutes)'
        ).eq('user_id', user_id).in_('status', ['pending', 'in_progress']).execute()
        
        if body_res.data:
            for task in body_res.data:
                # Check if scheduled for target date, overdue, or no specific schedule
                task_scheduled_at = task.get('scheduled_at')
                should_include = False
                
                if task_scheduled_at:
                    task_date = datetime.fromisoformat(task_scheduled_at.replace('Z', '+00:00')).date()
                    # Include if scheduled for today OR overdue (scheduled in the past)
                    if task_date <= date_obj:
                        should_include = True
                elif include_unscheduled:
                    # Include tasks without specific schedule
                    should_include = True
                
                if not should_include:
                    continue
                
                template = task.get('task_templates', {})
                estimated_minutes = template.get('estimated_minutes', 30)
                
                tasks_by_type['body'].append({
                    'id': task['id'],
                    'task_id': task['id'],
                    'title': template.get('name', 'Body Task'),
                    'description': '',
                    'type': 'body',
                    'estimated_duration_minutes': estimated_minutes,
                    'scheduled_at': task_scheduled_at,
                    'status': task.get('status', 'pending'),
                    'urgency_multiplier': 1.0  # Default, no deadline
                })
    except Exception as e:
        print(f"Error fetching body tasks: {e}")
    
    return tasks_by_type


# ==================== ALGORITMO DE OPTIMIZACIÓN ====================

def calculate_task_priority_score(task: Dict, current_time: datetime = None) -> float:
    """Calculate comprehensive priority score for a task.
    
    The score considers:
    - Task type weight (goals > mind/body)
    - Deadline urgency
    - Task weight/priority
    - Time of day (some tasks better for morning/evening)
    
    Args:
        task: Task dictionary
        current_time: Current time for context (optional)
        
    Returns:
        Priority score (higher = more important)
    """
    score = 0.0
    
    # Base type priority
    type_weight = PRIORITY_WEIGHTS.get(task['type'], 1.0)
    task_weight = task.get('weight', 1)
    score += type_weight * task_weight * 10
    
    # Urgency multiplier from deadline
    urgency = task.get('urgency_multiplier', 1.0)
    score *= urgency
    
    # Bonus for shorter tasks (easier to fit in schedule)
    duration_minutes = task.get('estimated_duration_minutes', 60)
    if duration_minutes <= 30:
        score += 5
    elif duration_minutes <= 60:
        score += 2
    
    return round(score, 2)


def optimize_daily_schedule(user_id: str, target_date: str = None, current_time: datetime = None) -> Dict[str, Any]:
    """Generate optimized daily schedule for maximum productivity.
    
    This is the main algorithm that:
    1. Gets user profile and available time
    2. Retrieves all pending tasks
    3. Calculates priority scores considering deadlines
    4. Distributes tasks across morning and evening slots
    5. Maximizes time utilization while respecting limits
    
    Args:
        user_id: User ID
        target_date: ISO date string (defaults to today)
        current_time: Current datetime (for "remaining today" calculations)
        
    Returns:
        Comprehensive schedule with optimized task distribution
    """
    # Get user profile and time availability
    profile_info = get_user_profile_info(user_id)
    
    if 'error' in profile_info:
        return profile_info
    
    # Get all pending tasks for the date
    tasks_by_type = get_pending_tasks_all_types(user_id, target_date)
    
    # Determine target date
    if target_date:
        try:
            date_obj = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
        except:
            date_obj = datetime.utcnow()
    else:
        date_obj = datetime.utcnow()
    
    # Extract time slot information
    morning_slot = profile_info['time_slots']['morning']
    evening_slot = profile_info['time_slots']['evening']
    
    morning_hours = morning_slot['duration_hours']
    evening_hours = evening_slot['duration_hours']
    total_available_hours = morning_hours + evening_hours
    
    # Convert to minutes for easier calculation
    morning_minutes = morning_hours * 60
    evening_minutes = evening_hours * 60
    total_available_minutes = total_available_hours * 60
    
    # Combine all tasks and calculate priority scores
    all_tasks = []
    
    for task_type, tasks in tasks_by_type.items():
        for task in tasks:
            task['priority_score'] = calculate_task_priority_score(task, current_time)
            all_tasks.append(task)
    
    # Sort by priority score (highest first)
    all_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # ==================== DISTRIBUTE TASKS ====================
    
    scheduled_morning = []
    scheduled_evening = []
    remaining_morning_minutes = morning_minutes
    remaining_evening_minutes = evening_minutes
    total_scheduled_minutes = 0
    
    # Track task type distribution
    scheduled_by_type = {'goal': 0, 'mind': 0, 'body': 0}
    
    for task in all_tasks:
        duration = task['estimated_duration_minutes']
        task_type = task['type']
        
        # Check if we have any time left
        if remaining_morning_minutes < BUFFER_MINUTES and remaining_evening_minutes < BUFFER_MINUTES:
            break
        
        # Add buffer time
        duration_with_buffer = duration + BUFFER_MINUTES
        
        # Decide which slot to use
        # Goals and mind tasks prefer morning (better focus)
        # Body tasks prefer evening (after work stress)
        prefer_morning = task_type in ['goal', 'mind']
        
        scheduled = False
        
        if prefer_morning:
            # Try morning first
            if duration_with_buffer <= remaining_morning_minutes:
                # Calculate start time
                minutes_used = morning_minutes - remaining_morning_minutes
                start_h, start_m = parse_time_string(morning_slot['start'])
                start_time = datetime.combine(date_obj.date(), dt_time(start_h, start_m)) + timedelta(minutes=minutes_used)
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_morning.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': 'morning'
                })
                
                remaining_morning_minutes -= duration_with_buffer
                scheduled = True
            # Try evening as fallback
            elif duration_with_buffer <= remaining_evening_minutes:
                minutes_used = evening_minutes - remaining_evening_minutes
                start_h, start_m = parse_time_string(evening_slot['start'])
                start_time = datetime.combine(date_obj.date(), dt_time(start_h, start_m)) + timedelta(minutes=minutes_used)
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_evening.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': 'evening'
                })
                
                remaining_evening_minutes -= duration_with_buffer
                scheduled = True
        else:
            # Try evening first for body tasks
            if duration_with_buffer <= remaining_evening_minutes:
                minutes_used = evening_minutes - remaining_evening_minutes
                start_h, start_m = parse_time_string(evening_slot['start'])
                start_time = datetime.combine(date_obj.date(), dt_time(start_h, start_m)) + timedelta(minutes=minutes_used)
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_evening.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': 'evening'
                })
                
                remaining_evening_minutes -= duration_with_buffer
                scheduled = True
            # Try morning as fallback
            elif duration_with_buffer <= remaining_morning_minutes:
                minutes_used = morning_minutes - remaining_morning_minutes
                start_h, start_m = parse_time_string(morning_slot['start'])
                start_time = datetime.combine(date_obj.date(), dt_time(start_h, start_m)) + timedelta(minutes=minutes_used)
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_morning.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': 'morning'
                })
                
                remaining_morning_minutes -= duration_with_buffer
                scheduled = True
        
        if scheduled:
            total_scheduled_minutes += duration
            scheduled_by_type[task_type] += duration
    
    # ==================== CALCULATE METRICS ====================
    
    all_scheduled = scheduled_morning + scheduled_evening
    total_tasks_count = len(all_tasks)
    scheduled_tasks_count = len(all_scheduled)
    
    efficiency = (total_scheduled_minutes / total_available_minutes * 100) if total_available_minutes > 0 else 0
    
    # Calculate distribution metrics
    total_scheduled_hours = total_scheduled_minutes / 60
    distribution_actual = {}
    distribution_deviation = {}
    
    if total_scheduled_minutes > 0:
        for task_type in ['goal', 'mind', 'body']:
            actual_pct = scheduled_by_type[task_type] / total_scheduled_minutes
            ideal_pct = IDEAL_DISTRIBUTION[task_type]
            distribution_actual[task_type] = round(actual_pct * 100, 1)
            distribution_deviation[task_type] = round((actual_pct - ideal_pct) * 100, 1)
    else:
        for task_type in ['goal', 'mind', 'body']:
            distribution_actual[task_type] = 0
            distribution_deviation[task_type] = 0
    
    # Balance score (closer to ideal distribution = better)
    balance_score = 100 - sum(abs(distribution_deviation[t]) for t in distribution_deviation) / 3
    balance_score = max(0, min(100, balance_score))
    
    # Overall productivity score
    productivity_score = (efficiency * 0.6) + (balance_score * 0.4)
    
    return {
        'user_id': user_id,
        'date': target_date or date_obj.date().isoformat(),
        'generated_at': datetime.utcnow().isoformat(),
        'profile_summary': {
            'work_schedule': profile_info['profile']['work_schedule'],
            'daily_free_hours': profile_info['daily_breakdown']['free_hours_available'],
            'weekly_hours_remaining': profile_info['profile']['remaining_hours_this_week']
        },
        'schedule': {
            'morning': {
                'time_range': f"{morning_slot['start']} - {morning_slot['end']}",
                'available_hours': round(morning_hours, 2),
                'available_minutes': int(morning_minutes),
                'scheduled_minutes': int(morning_minutes - remaining_morning_minutes),
                'remaining_minutes': int(max(0, remaining_morning_minutes)),
                'tasks': scheduled_morning
            },
            'evening': {
                'time_range': f"{evening_slot['start']} - {evening_slot['end']}",
                'available_hours': round(evening_hours, 2),
                'available_minutes': int(evening_minutes),
                'scheduled_minutes': int(evening_minutes - remaining_evening_minutes),
                'remaining_minutes': int(max(0, remaining_evening_minutes)),
                'tasks': scheduled_evening
            }
        },
        'summary': {
            'total_tasks_available': total_tasks_count,
            'tasks_by_type_available': {
                'goals': len(tasks_by_type['goals']),
                'mind': len(tasks_by_type['mind']),
                'body': len(tasks_by_type['body'])
            },
            'total_tasks_scheduled': scheduled_tasks_count,
            'tasks_by_type_scheduled': {
                'goals': sum(1 for t in all_scheduled if t['type'] == 'goal'),
                'mind': sum(1 for t in all_scheduled if t['type'] == 'mind'),
                'body': sum(1 for t in all_scheduled if t['type'] == 'body')
            },
            'total_minutes_available': int(total_available_minutes),
            'total_minutes_scheduled': int(total_scheduled_minutes),
            'total_hours_scheduled': round(total_scheduled_hours, 2),
            'efficiency_percentage': round(efficiency, 2),
            'unscheduled_tasks': total_tasks_count - scheduled_tasks_count
        },
        'distribution_analysis': {
            'actual_distribution': distribution_actual,
            'ideal_distribution': {k: v * 100 for k, v in IDEAL_DISTRIBUTION.items()},
            'deviation_from_ideal': distribution_deviation,
            'balance_score': round(balance_score, 2)
        },
        'scores': {
            'efficiency_score': round(efficiency, 2),
            'balance_score': round(balance_score, 2),
            'productivity_score': round(productivity_score, 2)
        },
        'algorithm_info': {
            'version': '2.0',
            'priority_weights': PRIORITY_WEIGHTS,
            'buffer_between_tasks_minutes': BUFFER_MINUTES,
            'considers_deadlines': True,
            'considers_time_of_day': True
        }
    }


def get_day_name_abbreviation(weekday: int) -> str:
    """Convert weekday number to Spanish abbreviation.
    
    Args:
        weekday: Day of week (0=Monday, 6=Sunday)
        
    Returns:
        Spanish abbreviation (L,M,M,J,V,S,D)
    """
    day_map = {
        0: 'L',  # Lunes
        1: 'M',  # Martes
        2: 'M',  # Miércoles
        3: 'J',  # Jueves
        4: 'V',  # Viernes
        5: 'S',  # Sábado
        6: 'D'   # Domingo
    }
    return day_map.get(weekday, 'L')


def is_working_day(current_date: datetime, day_work: str) -> bool:
    """Check if current date is a working day.
    
    Args:
        current_date: Date to check
        day_work: Work days string (e.g., "L,M,M,J,V")
        
    Returns:
        True if it's a working day
    """
    if not day_work:
        # Default to Monday-Friday if not specified
        return current_date.weekday() < 5
    
    current_day_abbr = get_day_name_abbreviation(current_date.weekday())
    return current_day_abbr in day_work.split(',')


def get_tasks_for_current_moment(user_id: str) -> Dict[str, Any]:
    """Get tasks that should be done RIGHT NOW based on current time.
    
    This endpoint considers:
    - User's timezone
    - Work days from profile (day_work)
    - Time dead from profile
    - Current time of day
    - Remaining time calculation: (24 - work_hours - time_dead)
    - Task urgency and priority
    
    Args:
        user_id: User ID
        
    Returns:
        Tasks organized by type with correct time calculations
    """
    supabase = get_supabase()
    
    # Get user profile
    profile_res = supabase.from_('profiles').select('*').eq('user_id', user_id).execute()
    
    if not profile_res.data:
        return {
            'error': 'Profile not found',
            'message': 'Please create a profile first',
            'user_id': user_id
        }
    
    profile = profile_res.data[0]
    
    # Get timezone (default to America/Mexico_City)
    user_timezone = profile.get('timezone', 'America/Mexico_City')
    try:
        tz = pytz.timezone(user_timezone)
        # Get current time in user's timezone
        current_time_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
        current_time = current_time_utc.astimezone(tz)
    except (pytz.exceptions.UnknownTimeZoneError, ValueError, AttributeError):
        # Fallback if pytz not available or timezone invalid
        current_time = datetime.utcnow()
    
    # Get profile fields
    day_work = profile.get('day_work', 'L,M,M,J,V')  # Default Monday-Friday
    time_dead = profile.get('time_dead', 9)  # Default 9 hours
    work_schedules = profile.get('work_schedules', '9:00-17:00')
    hours_available_to_week = profile.get('hours_available_to_week', 40)
    hours_used_to_week = profile.get('hours_used_to_week', 0)
    
    # Check if today is a working day
    is_work_day = is_working_day(current_time, day_work)
    
    # Calculate work hours
    if is_work_day:
        (work_start_h, work_start_m), (work_end_h, work_end_m) = parse_time_range(work_schedules)
        work_hours = calculate_duration_hours((work_start_h, work_start_m), (work_end_h, work_end_m))
    else:
        # No work on non-working days
        work_hours = 0
    
    # Calculate available hours: (24 - work_hours - time_dead)
    available_hours_today = 24 - work_hours - time_dead
    available_minutes_today = available_hours_today * 60
    
    # Calculate remaining hours in the week
    remaining_hours_week = hours_available_to_week - hours_used_to_week
    remaining_minutes_week = remaining_hours_week * 60
    
    # Calculate remaining time TODAY from current time
    # The day goes from midnight to midnight (full 24 hours)
    # Calculate time until next midnight
    end_of_day = (current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_diff = end_of_day - current_time
    total_minutes_until_midnight = int(time_diff.total_seconds() / 60)
    
    # However, we need to subtract work hours and time_dead to get actual available time
    # If it's a working day, calculate when work ends
    if is_work_day and work_hours > 0:
        work_start_time = current_time.replace(hour=work_start_h, minute=work_start_m, second=0, microsecond=0)
        work_end_time = current_time.replace(hour=work_end_h, minute=work_end_m, second=0, microsecond=0)
        
        # If current time is before work starts, we have morning time
        if current_time < work_start_time:
            # Time from now until work starts
            morning_available = int((work_start_time - current_time).total_seconds() / 60)
            # Time after work ends until midnight
            evening_available = int((end_of_day - work_end_time).total_seconds() / 60)
            remaining_minutes_today = morning_available + evening_available
        # If during work hours, only evening is available
        elif current_time < work_end_time:
            remaining_minutes_today = int((end_of_day - work_end_time).total_seconds() / 60)
        # If after work, time until midnight minus time_dead
        else:
            remaining_minutes_today = total_minutes_until_midnight
    else:
        # Non-working day: all time until midnight is available
        remaining_minutes_today = total_minutes_until_midnight
    
    # Make sure it doesn't go negative
    remaining_minutes_today = max(0, remaining_minutes_today)
    
    # Get all pending tasks
    tasks_by_type = get_pending_tasks_all_types(user_id, current_time.date().isoformat(), include_unscheduled=True)
    
    # Combine and calculate priority scores
    all_goal_tasks = []
    all_mind_tasks = []
    all_body_tasks = []
    
    for task in tasks_by_type['goals']:
        task['priority_score'] = calculate_task_priority_score(task, current_time)
        all_goal_tasks.append(task)
    
    for task in tasks_by_type['mind']:
        task['priority_score'] = calculate_task_priority_score(task, current_time)
        all_mind_tasks.append(task)
    
    for task in tasks_by_type['body']:
        task['priority_score'] = calculate_task_priority_score(task, current_time)
        all_body_tasks.append(task)
    
    # Sort each type by priority
    all_goal_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
    all_mind_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
    all_body_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Determine time slot
    current_hour = current_time.hour
    if current_hour < 12:
        current_time_slot = 'morning'
    elif current_hour < 18:
        current_time_slot = 'afternoon'
    else:
        current_time_slot = 'evening'
    
    # AGGRESSIVE SCHEDULING: Fill as much time as possible with balanced distribution
    scheduled_goal_tasks = []
    scheduled_mind_tasks = []
    scheduled_body_tasks = []
    
    schedule_start_time = current_time
    available_time_buffer = remaining_minutes_today
    
    # Calculate target time allocations (ideal distribution)
    # Goal: 60%, Mind: 20%, Body: 20%
    target_goal_time = remaining_minutes_today * 0.60
    target_mind_time = remaining_minutes_today * 0.20
    target_body_time = remaining_minutes_today * 0.20
    
    time_used_goals = 0
    time_used_mind = 0
    time_used_body = 0
    
    # Create a combined priority queue with all tasks
    # But maintain minimum quotas for each type
    min_mind_tasks = max(1, len(all_mind_tasks) // 3) if all_mind_tasks else 0
    min_body_tasks = max(1, len(all_body_tasks) // 3) if all_body_tasks else 0
    
    goal_idx = 0
    mind_idx = 0
    body_idx = 0
    
    # Schedule tasks in rounds to ensure balance
    # Each round tries to add one task of each type if there's time
    max_rounds = max(len(all_goal_tasks), len(all_mind_tasks), len(all_body_tasks)) + 10
    
    for round_num in range(max_rounds):
        if available_time_buffer < 15:  # Stop if less than 15 min left
            break
        
        tasks_scheduled_this_round = False
        
        # Try to schedule a GOAL task (priority, but respect limits)
        if goal_idx < len(all_goal_tasks) and time_used_goals < target_goal_time:
            task = all_goal_tasks[goal_idx]
            duration = task.get('estimated_duration_minutes', 60)
            duration_with_buffer = duration + 10
            
            if duration_with_buffer <= available_time_buffer:
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_goal_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time + timedelta(minutes=10)
                available_time_buffer -= duration_with_buffer
                time_used_goals += duration
                goal_idx += 1
                tasks_scheduled_this_round = True
            elif duration <= available_time_buffer:
                # Try without buffer
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_goal_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time
                available_time_buffer -= duration
                time_used_goals += duration
                goal_idx += 1
                tasks_scheduled_this_round = True
            else:
                goal_idx += 1  # Skip task if too long
        
        # Try to schedule a MIND task (ensure minimum representation)
        if mind_idx < len(all_mind_tasks) and (time_used_mind < target_mind_time or len(scheduled_mind_tasks) < min_mind_tasks):
            task = all_mind_tasks[mind_idx]
            duration = task.get('estimated_duration_minutes', 30)
            duration_with_buffer = duration + 10
            
            if duration_with_buffer <= available_time_buffer:
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_mind_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time + timedelta(minutes=10)
                available_time_buffer -= duration_with_buffer
                time_used_mind += duration
                mind_idx += 1
                tasks_scheduled_this_round = True
            elif duration <= available_time_buffer:
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_mind_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time
                available_time_buffer -= duration
                time_used_mind += duration
                mind_idx += 1
                tasks_scheduled_this_round = True
            else:
                mind_idx += 1  # Skip task if too long
        
        # Try to schedule a BODY task (ensure minimum representation)
        if body_idx < len(all_body_tasks) and (time_used_body < target_body_time or len(scheduled_body_tasks) < min_body_tasks):
            task = all_body_tasks[body_idx]
            duration = task.get('estimated_duration_minutes', 30)
            duration_with_buffer = duration + 10
            
            if duration_with_buffer <= available_time_buffer:
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_body_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time + timedelta(minutes=10)
                available_time_buffer -= duration_with_buffer
                time_used_body += duration
                body_idx += 1
                tasks_scheduled_this_round = True
            elif duration <= available_time_buffer:
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_body_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time
                available_time_buffer -= duration
                time_used_body += duration
                body_idx += 1
                tasks_scheduled_this_round = True
            else:
                body_idx += 1  # Skip task if too long
        
        # If no tasks were scheduled this round and we've exhausted all lists, break
        if not tasks_scheduled_this_round:
            if goal_idx >= len(all_goal_tasks) and mind_idx >= len(all_mind_tasks) and body_idx >= len(all_body_tasks):
                break
    
    # After balanced scheduling, if there's still significant time left,
    # fill with any remaining tasks (prioritize goals)
    if available_time_buffer > 60:  # More than 1 hour left
        # Add remaining goal tasks
        while goal_idx < len(all_goal_tasks) and available_time_buffer >= 15:
            task = all_goal_tasks[goal_idx]
            duration = task.get('estimated_duration_minutes', 60)
            
            if duration + 10 <= available_time_buffer:
                start_time = schedule_start_time
                end_time = start_time + timedelta(minutes=duration)
                
                scheduled_goal_tasks.append({
                    **task,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'time_slot': current_time_slot
                })
                
                schedule_start_time = end_time + timedelta(minutes=10)
                available_time_buffer -= (duration + 10)
            
            goal_idx += 1
    
    # Calculate total time for scheduled tasks
    total_task_minutes = sum(t.get('estimated_duration_minutes', 60) for t in scheduled_goal_tasks)
    total_task_minutes += sum(t.get('estimated_duration_minutes', 30) for t in scheduled_mind_tasks)
    total_task_minutes += sum(t.get('estimated_duration_minutes', 30) for t in scheduled_body_tasks)
    
    # Calculate how much time is remaining after scheduling
    remaining_after_scheduling = remaining_minutes_today - total_task_minutes
    utilization_percentage = (total_task_minutes / remaining_minutes_today * 100) if remaining_minutes_today > 0 else 0
    
    # Build response in requested format
    return {
        'body_tasks': scheduled_body_tasks,
        'goal_tasks': scheduled_goal_tasks,
        'mind_tasks': scheduled_mind_tasks,
        'current_time': current_time.isoformat(),
        'message': f"You have {remaining_minutes_today} minutes remaining today. {total_task_minutes} minutes scheduled ({utilization_percentage:.0f}% utilization).",
        'remaining_hours_in_slot_week': round(remaining_hours_week, 2),
        'remaining_minutes_today': remaining_minutes_today,
        'remaining_hours_today': round(remaining_minutes_today / 60, 2),
        'total_body_tasks': len(scheduled_body_tasks),
        'total_goal_tasks': len(scheduled_goal_tasks),
        'total_mind_tasks': len(scheduled_mind_tasks),
        'total_time_used_for_tasks': int(total_task_minutes),
        'remaining_minutes_in_slot_week': int(remaining_minutes_week),
        'remaining_after_scheduling': max(0, remaining_after_scheduling),
        'utilization_percentage': round(utilization_percentage, 1),
        'total_available_tasks': len(all_goal_tasks) + len(all_mind_tasks) + len(all_body_tasks),
        'total_scheduled_tasks': len(scheduled_goal_tasks) + len(scheduled_mind_tasks) + len(scheduled_body_tasks),
        'user_id': user_id,
        'is_working_day': is_work_day,
        'available_hours_today': round(available_hours_today, 2),
        'work_hours_today': round(work_hours, 2),
        'time_dead': time_dead
    }
