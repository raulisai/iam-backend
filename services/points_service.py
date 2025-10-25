"""Points service for managing goal points and calculating scores."""
from datetime import date
from lib.db import get_supabase


def get_points(user_id):
    """Get points summary for a user.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        dict: Points data including target and earned points.
    """
    supabase = get_supabase()
    
    result = supabase.from_('profiles').select(
        'goal_points_target, goal_points_earned'
    ).eq('user_id', user_id).execute()
    
    if not result.data:
        return None
    
    profile = result.data[0]
    return {
        'goal_points_target': float(profile['goal_points_target']),
        'goal_points_earned': float(profile['goal_points_earned']),
        'goal_points_remaining': float(profile['goal_points_target']) - float(profile['goal_points_earned']),
        'completion_percentage': (
            (float(profile['goal_points_earned']) / float(profile['goal_points_target']) * 100)
            if float(profile['goal_points_target']) > 0 else 0
        )
    }


def calculate_goal_points_target(user_id):
    """Calculate total points from all pending tasks (mind, body, goal_tasks).
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        dict: Calculated points breakdown by category.
    """
    supabase = get_supabase()
    
    # Calculate points from pending mind tasks
    mind_result = supabase.rpc(
        'calculate_pending_points',
        {
            'p_user_id': user_id,
            'p_table_name': 'tasks_mind'
        }
    ).execute()
    
    mind_points = mind_result.data if mind_result.data else 0
    
    # Calculate points from pending body tasks
    body_result = supabase.rpc(
        'calculate_pending_points',
        {
            'p_user_id': user_id,
            'p_table_name': 'tasks_body'
        }
    ).execute()
    
    body_points = body_result.data if body_result.data else 0
    
    # Calculate points from active goal tasks
    # Sum the weight of all goal_tasks that belong to active goals
    goal_tasks_result = supabase.from_('goal_tasks').select(
        'weight, goals!inner(is_active)'
    ).eq('user_id', user_id).eq('goals.is_active', True).execute()
    
    goal_points = sum(float(task['weight']) for task in goal_tasks_result.data) if goal_tasks_result.data else 0
    
    total_points = mind_points + body_points + goal_points
    
    # Update profile with calculated target
    supabase.from_('profiles').update({
        'goal_points_target': total_points
    }).eq('user_id', user_id).execute()
    
    return {
        'mind_points': float(mind_points),
        'body_points': float(body_points),
        'goal_points': float(goal_points),
        'total_target_points': float(total_points)
    }


def add_earned_points(user_id, points, task_type='mind'):
    """Add points to goal_points_earned and update snapshot scores.
    
    Args:
        user_id (str): The user's ID.
        points (float): Points to add.
        task_type (str): Type of task ('mind', 'body', or 'goal').
    
    Returns:
        dict: Updated points and scores.
    """
    supabase = get_supabase()
    
    # Get current earned points
    profile_result = supabase.from_('profiles').select(
        'goal_points_earned'
    ).eq('user_id', user_id).execute()
    
    if not profile_result.data:
        return None
    
    current_earned = float(profile_result.data[0]['goal_points_earned'])
    new_earned = current_earned + points
    
    # Update profile earned points
    supabase.from_('profiles').update({
        'goal_points_earned': new_earned
    }).eq('user_id', user_id).execute()
    
    # Update snapshot scores based on task type
    _update_snapshot_score(user_id, points, task_type, 'add')
    
    return {
        'previous_earned': float(current_earned),
        'points_added': float(points),
        'new_earned': float(new_earned),
        'task_type': task_type
    }


def subtract_earned_points(user_id, points, task_type='mind'):
    """Subtract points from goal_points_earned and update snapshot scores.
    
    Args:
        user_id (str): The user's ID.
        points (float): Points to subtract.
        task_type (str): Type of task ('mind', 'body', or 'goal').
    
    Returns:
        dict: Updated points and scores.
    """
    supabase = get_supabase()
    
    # Get current earned points
    profile_result = supabase.from_('profiles').select(
        'goal_points_earned'
    ).eq('user_id', user_id).execute()
    
    if not profile_result.data:
        return None
    
    current_earned = float(profile_result.data[0]['goal_points_earned'])
    new_earned = max(0, current_earned - points)
    
    # Update profile earned points
    supabase.from_('profiles').update({
        'goal_points_earned': new_earned
    }).eq('user_id', user_id).execute()
    
    # Update snapshot scores based on task type
    _update_snapshot_score(user_id, points, task_type, 'subtract')
    
    return {
        'previous_earned': float(current_earned),
        'points_subtracted': float(points),
        'new_earned': float(new_earned),
        'task_type': task_type
    }


def _update_snapshot_score(user_id, points, task_type, operation='add'):
    """Update performance snapshot score based on task type.
    
    Args:
        user_id (str): The user's ID.
        points (float): Points to add/subtract.
        task_type (str): Type of task ('mind', 'body', or 'goal').
        operation (str): Operation type ('add' or 'subtract').
    """
    supabase = get_supabase()
    from datetime import datetime
    today = datetime.now().date().isoformat()
    
    # Get or create today's snapshot
    snapshot_result = supabase.from_('performance_snapshots').select(
        'id, score_mind, score_body, inputs'
    ).eq('user_id', user_id).gte('snapshot_at', f'{today}T00:00:00').lte('snapshot_at', f'{today}T23:59:59').execute()
    
    if snapshot_result.data:
        # Update existing snapshot
        snapshot = snapshot_result.data[0]
        
        # Get current scores
        current_mind_score = float(snapshot.get('score_mind', 0) or 0)
        current_body_score = float(snapshot.get('score_body', 0) or 0)
        inputs = snapshot.get('inputs') or {}
        goal_score = float(inputs.get('goal_score', 0))
        
        # Calculate score change based on task type
        if task_type == 'mind':
            score_change = points if operation == 'add' else -points
            new_mind_score = max(0, current_mind_score + score_change)
            
            supabase.from_('performance_snapshots').update({
                'score_mind': new_mind_score
            }).eq('id', snapshot['id']).execute()
            
        elif task_type == 'body':
            score_change = points if operation == 'add' else -points
            new_body_score = max(0, current_body_score + score_change)
            
            supabase.from_('performance_snapshots').update({
                'score_body': new_body_score
            }).eq('id', snapshot['id']).execute()
            
        elif task_type == 'goal':
            # Goal tasks contribute to inputs.goal_score
            multiplier = 0.5  # Goal tasks contribute less
            score_change = (points * multiplier) if operation == 'add' else -(points * multiplier)
            new_goal_score = max(0, goal_score + score_change)
            inputs['goal_score'] = new_goal_score
            
            supabase.from_('performance_snapshots').update({
                'inputs': inputs
            }).eq('id', snapshot['id']).execute()
    else:
        # Create new snapshot with initial scores
        from datetime import datetime
        new_snapshot = {
            'user_id': user_id,
            'snapshot_at': datetime.now().isoformat(),
            'score_mind': points if task_type == 'mind' else 0,
            'score_body': points if task_type == 'body' else 0,
            'inputs': {'goal_score': points * 0.5 if task_type == 'goal' else 0}
        }
        
        supabase.from_('performance_snapshots').insert(new_snapshot).execute()


def recalculate_all_points(user_id):
    """Recalculate both target and earned points for a user.
    
    Args:
        user_id (str): The user's ID.
    
    Returns:
        dict: Complete points summary after recalculation.
    """
    # Recalculate target points
    target_data = calculate_goal_points_target(user_id)
    
    # Get current earned points (no recalculation needed, it's cumulative)
    points_data = get_points(user_id)
    
    return {
        'target_breakdown': target_data,
        'points_summary': points_data
    }
