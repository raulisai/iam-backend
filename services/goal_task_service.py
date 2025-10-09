"""Goal Task service for goal task operations."""
from lib.db import get_supabase
from datetime import datetime, timedelta
from dateutil import rrule as rrule_module
import time
import logging

logger = logging.getLogger(__name__)


def get_goal_tasks(goal_id, user_id):
    """Get all tasks for a specific goal.
    
    Args:
        goal_id (str): Goal ID.
        user_id (str): User ID for authorization.
    
    Returns:
        list: List of goal tasks.
    """
    supabase = get_supabase()
    res = supabase.from_('goal_tasks')\
        .select('*')\
        .eq('goal_id', goal_id)\
        .eq('user_id', user_id)\
        .order('created_at', desc=False)\
        .execute()
    return res.data


def get_goal_task_by_id(task_id):
    """Get goal task by ID.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Task data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('goal_tasks').select('*').eq('id', task_id).execute()
    return res.data[0] if res.data else None


def create_goal_task(data):
    """Create a new goal task with retry logic.
    
    Args:
        data (dict): Task data.
    
    Returns:
        dict: Created task.
    
    Raises:
        Exception: If creation fails after retries.
    """
    supabase = get_supabase()
    max_retries = 3
    retry_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            res = supabase.from_('goal_tasks').insert(data).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            error_msg = str(e).lower()
            # Don't retry on schema errors or client errors
            if 'could not find' in error_msg or 'pgrst204' in error_msg:
                logger.error(f"Schema error creating goal task: {e}")
                raise
            
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed creating goal task: {e}. Retrying...")
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
            else:
                logger.error(f"Failed to create goal task after {max_retries} attempts: {e}")
                raise


def update_goal_task(task_id, data):
    """Update a goal task.
    
    Args:
        task_id (str): Task ID.
        data (dict): Updated data.
    
    Returns:
        dict: Updated task.
    """
    supabase = get_supabase()
    res = supabase.from_('goal_tasks').update(data).eq('id', task_id).execute()
    return res.data[0] if res.data else None


def delete_goal_task(task_id):
    """Delete a goal task.
    
    Args:
        task_id (str): Task ID.
    
    Returns:
        dict: Deleted task.
    """
    supabase = get_supabase()
    res = supabase.from_('goal_tasks').delete().eq('id', task_id).execute()
    return res.data[0] if res.data else None


def get_task_occurrences(task_id, start_date=None, end_date=None):
    """Get occurrences for a task, optionally filtered by date range.
    
    Args:
        task_id (str): Task ID.
        start_date (str, optional): Start date filter (ISO format).
        end_date (str, optional): End date filter (ISO format).
    
    Returns:
        list: List of task occurrences.
    """
    supabase = get_supabase()
    query = supabase.from_('task_occurrences')\
        .select('*')\
        .eq('task_id', task_id)
    
    if start_date:
        query = query.gte('scheduled_at', start_date)
    if end_date:
        query = query.lte('scheduled_at', end_date)
    
    res = query.order('scheduled_at', desc=False).execute()
    return res.data


def get_occurrence_by_id(occurrence_id):
    """Get occurrence by ID.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        dict: Occurrence data or None.
    """
    supabase = get_supabase()
    res = supabase.from_('task_occurrences').select('*').eq('id', occurrence_id).execute()
    return res.data[0] if res.data else None


def create_task_occurrence(data):
    """Create a new task occurrence.
    
    Args:
        data (dict): Occurrence data (task_id, scheduled_at, optional: value for metadata).
    
    Returns:
        dict: Created occurrence or None if already exists.
    """
    supabase = get_supabase()
    try:
        # Only keep fields that exist in the task_occurrences table
        # Note: 'value' and 'notes' are stored in logs, not in occurrences table
        allowed_fields = ['task_id', 'scheduled_at', 'completed_at', 'skipped_at']
        filtered_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        res = supabase.from_('task_occurrences').insert(filtered_data).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        # Handle unique constraint violation
        if 'duplicate key' in str(e).lower():
            logger.warning(f"Duplicate occurrence for task_id={data.get('task_id')}, scheduled_at={data.get('scheduled_at')}")
            return None
        logger.error(f"Error creating occurrence: {e}")
        raise


def generate_occurrences_for_task(task_id, task_data, start_date, end_date):
    """Generate occurrences for a task based on its schedule.
    
    Args:
        task_id (str): Task ID.
        task_data (dict): Task data containing schedule_rrule or due_at.
        start_date (datetime): Start date for generation.
        end_date (datetime): End date for generation.
    
    Returns:
        list: List of created occurrences.
    """
    supabase = get_supabase()
    created_occurrences = []
    
    # If task has a schedule_rrule, generate recurring occurrences
    if task_data.get('schedule_rrule'):
        try:
            # Parse the RRULE string
            rrule_str = task_data['schedule_rrule']
            if not rrule_str.startswith('RRULE:'):
                rrule_str = 'RRULE:' + rrule_str
            
            # Generate dates using rrule
            rule = rrule_module.rrulestr(rrule_str, dtstart=start_date)
            dates = list(rule.between(start_date, end_date, inc=True))
            
            for date in dates:
                occurrence_data = {
                    'task_id': task_id,
                    'scheduled_at': date.isoformat()
                }
                created = create_task_occurrence(occurrence_data)
                if created:
                    created_occurrences.append(created)
                    
        except (ValueError, AttributeError) as e:
            print(f"Error generating occurrences from rrule: {e}")
            
    # If task has a due_at, create a single occurrence
    elif task_data.get('due_at'):
        due_at = datetime.fromisoformat(task_data['due_at'].replace('Z', '+00:00'))
        if start_date <= due_at <= end_date:
            occurrence_data = {
                'task_id': task_id,
                'scheduled_at': due_at.isoformat()
            }
            created = create_task_occurrence(occurrence_data)
            if created:
                created_occurrences.append(created)
    
    return created_occurrences


def delete_task_occurrence(occurrence_id):
    """Delete a task occurrence.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        dict: Deleted occurrence.
    """
    supabase = get_supabase()
    res = supabase.from_('task_occurrences').delete().eq('id', occurrence_id).execute()
    return res.data[0] if res.data else None


def get_occurrence_logs(occurrence_id):
    """Get all logs for a specific occurrence.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        list: List of logs.
    """
    supabase = get_supabase()
    res = supabase.from_('task_logs')\
        .select('*')\
        .eq('task_table', 'task_occurrences')\
        .eq('task_id', occurrence_id)\
        .order('timestamp', desc=True)\
        .execute()
    return res.data


def log_occurrence_action(occurrence_id, user_id, action, metadata=None):
    """Log an action on an occurrence.
    
    Args:
        occurrence_id (str): Occurrence ID.
        user_id (str): User ID.
        action (str): Action type (e.g., 'completed', 'skipped', 'started').
        metadata (dict, optional): Additional metadata.
    
    Returns:
        dict: Created log entry.
    """
    supabase = get_supabase()
    log_data = {
        'task_table': 'task_occurrences',
        'task_id': occurrence_id,
        'user_id': user_id,
        'action': action,
        'timestamp': datetime.utcnow().isoformat(),
        'metadata': metadata or {}
    }
    res = supabase.from_('task_logs').insert(log_data).execute()
    return res.data[0] if res.data else None


def get_goal_progress(goal_id):
    """Get progress for a specific goal.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        dict: Progress data with percentage and details.
    """
    supabase = get_supabase()
    
    # Try to get from view first
    res = supabase.from_('goal_progress_view')\
        .select('*')\
        .eq('goal_id', goal_id)\
        .execute()
    
    if res.data and len(res.data) > 0:
        progress_data = res.data[0]
    else:
        progress_data = {'goal_id': goal_id, 'progress_percent': 0}
    
    # Get additional details: total tasks, completed occurrences, etc.
    try:
        # Get all tasks for this goal
        tasks = supabase.from_('goal_tasks')\
            .select('id, title, required, weight')\
            .eq('goal_id', goal_id)\
            .execute()
        
        total_tasks = len(tasks.data) if tasks.data else 0
        
        # Get all occurrences with their status
        completed_count = 0
        total_occurrences = 0
        
        if tasks.data:
            for task in tasks.data:
                # Get occurrences for this task
                occurrences = supabase.from_('task_occurrences')\
                    .select('id')\
                    .eq('task_id', task['id'])\
                    .execute()
                
                if occurrences.data:
                    for occ in occurrences.data:
                        total_occurrences += 1
                        # Check if this occurrence is completed
                        logs = supabase.from_('task_logs')\
                            .select('action')\
                            .eq('task_table', 'task_occurrences')\
                            .eq('task_id', occ['id'])\
                            .order('timestamp', desc=True)\
                            .limit(1)\
                            .execute()
                        
                        if logs.data and len(logs.data) > 0:
                            if logs.data[0]['action'] == 'completed':
                                completed_count += 1
        
        progress_data['total_tasks'] = total_tasks
        progress_data['total_occurrences'] = total_occurrences
        progress_data['completed_occurrences'] = completed_count
        
    except Exception as e:
        logger.error(f"Error getting progress details for goal {goal_id}: {e}")
    
    return progress_data


def get_occurrence_with_status(occurrence_id):
    """Get occurrence with its current status from logs.
    
    Args:
        occurrence_id (str): Occurrence ID.
    
    Returns:
        dict: Occurrence with status and last log.
    """
    # Get occurrence
    occurrence = get_occurrence_by_id(occurrence_id)
    if not occurrence:
        return None
    
    # Get latest log
    logs = get_occurrence_logs(occurrence_id)
    
    occurrence['status'] = 'pending'
    occurrence['last_action'] = None
    occurrence['last_value'] = None
    
    if logs and len(logs) > 0:
        latest_log = logs[0]
        occurrence['last_action'] = latest_log.get('action')
        occurrence['status'] = latest_log.get('action', 'pending')
        if latest_log.get('metadata'):
            occurrence['last_value'] = latest_log['metadata'].get('value')
    
    return occurrence


def get_occurrences_with_status(task_id, start_date=None, end_date=None):
    """Get occurrences with their status from logs.
    
    Args:
        task_id (str): Task ID.
        start_date (str, optional): Start date filter.
        end_date (str, optional): End date filter.
    
    Returns:
        list: List of occurrences with status.
    """
    occurrences = get_task_occurrences(task_id, start_date, end_date)
    
    for occurrence in occurrences:
        logs = get_occurrence_logs(occurrence['id'])
        
        occurrence['status'] = 'pending'
        occurrence['last_action'] = None
        occurrence['last_value'] = None
        
        if logs and len(logs) > 0:
            latest_log = logs[0]
            occurrence['last_action'] = latest_log.get('action')
            occurrence['status'] = latest_log.get('action', 'pending')
            if latest_log.get('metadata'):
                occurrence['last_value'] = latest_log['metadata'].get('value')
    
    return occurrences


def get_goal_progress_detailed(goal_id):
    """Get detailed progress information for debugging.
    
    Args:
        goal_id (str): Goal ID.
    
    Returns:
        dict: Detailed progress data including tasks, occurrences, and logs.
    """
    supabase = get_supabase()
    
    # Get goal info
    goal_res = supabase.from_('goals').select('*').eq('id', goal_id).execute()
    goal = goal_res.data[0] if goal_res.data else None
    
    if not goal:
        return {'error': 'Goal not found'}
    
    # Get all tasks
    tasks = supabase.from_('goal_tasks')\
        .select('*')\
        .eq('goal_id', goal_id)\
        .execute()
    
    tasks_detail = []
    total_occurrences = 0
    completed_occurrences = 0
    
    for task in (tasks.data or []):
        # Get occurrences for this task
        occurrences = supabase.from_('task_occurrences')\
            .select('*')\
            .eq('task_id', task['id'])\
            .execute()
        
        task_occurrences = []
        for occ in (occurrences.data or []):
            total_occurrences += 1
            
            # Get logs for this occurrence
            logs = supabase.from_('task_logs')\
                .select('*')\
                .eq('task_table', 'task_occurrences')\
                .eq('task_id', occ['id'])\
                .order('timestamp', desc=True)\
                .execute()
            
            status = 'pending'
            last_action = None
            last_value = None
            
            if logs.data and len(logs.data) > 0:
                latest = logs.data[0]
                last_action = latest.get('action')
                status = last_action
                if latest.get('metadata'):
                    last_value = latest['metadata'].get('value')
                
                if last_action == 'completed':
                    completed_occurrences += 1
            
            task_occurrences.append({
                'id': occ['id'],
                'scheduled_at': occ['scheduled_at'],
                'status': status,
                'last_action': last_action,
                'last_value': last_value,
                'logs_count': len(logs.data) if logs.data else 0
            })
        
        tasks_detail.append({
            'id': task['id'],
            'title': task['title'],
            'type': task.get('type'),
            'required': task.get('required', True),
            'weight': task.get('weight', 1),
            'occurrences_count': len(occurrences.data) if occurrences.data else 0,
            'occurrences': task_occurrences
        })
    
    # Get progress from view
    progress_view = supabase.from_('goal_progress_view')\
        .select('*')\
        .eq('goal_id', goal_id)\
        .execute()
    
    progress_percent = 0
    if progress_view.data and len(progress_view.data) > 0:
        progress_percent = progress_view.data[0].get('progress_percent', 0)
    
    # Calculate manual progress
    manual_progress = 0
    if total_occurrences > 0:
        if goal.get('target_value') and float(goal['target_value']) > 0:
            # Sum all values from completed occurrences
            total_value = 0
            for task in tasks_detail:
                for occ in task['occurrences']:
                    if occ['status'] == 'completed':
                        total_value += float(occ.get('last_value') or 1)
            manual_progress = min(100, (total_value / float(goal['target_value'])) * 100)
        else:
            # Percentage based on completed occurrences
            manual_progress = (completed_occurrences / total_occurrences) * 100
    
    return {
        'goal_id': goal_id,
        'goal_title': goal.get('title'),
        'target_value': goal.get('target_value'),
        'progress_from_view': progress_percent,
        'manual_calculation': manual_progress,
        'total_tasks': len(tasks.data) if tasks.data else 0,
        'total_occurrences': total_occurrences,
        'completed_occurrences': completed_occurrences,
        'tasks': tasks_detail
    }
