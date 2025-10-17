"""Score calculator for daily user performance metrics."""
from datetime import datetime, timedelta
from lib.db import get_supabase
import pytz


class ScoreCalculator:
    """Calculate and update user scores based on task completion."""
    
    # Score penalties for incomplete tasks
    PENALTY_BODY_TASK = 5
    PENALTY_MIND_TASK = 5
    PENALTY_ROUTINE_ALARM = 3
    MIN_SCORE = 0
    MAX_SCORE = 100
    
    def __init__(self):
        self.supabase = get_supabase()
    
    def calculate_daily_scores(self):
        """Calculate scores for all users at end of day."""
        print(f"[{datetime.now()}] Starting daily score calculation...")
        
        # Get all active users
        users = self._get_active_users()
        print(f"Found {len(users)} active users")
        
        results = []
        for user in users:
            try:
                result = self._calculate_user_score(user)
                results.append(result)
            except Exception as e:
                print(f"Error calculating score for user {user['id']}: {str(e)}")
                results.append({
                    'user_id': user['id'],
                    'status': 'error',
                    'error': str(e)
                })
        
        print(f"Completed score calculation for {len(results)} users")
        return results
    
    def _get_active_users(self):
        """Get all active users from database."""
        res = self.supabase.from_('users_iam').select('id, email').execute()
        return res.data or []
    
    def _calculate_user_score(self, user):
        """Calculate score for a specific user."""
        user_id = user['id']
        user_timezone = self._get_user_timezone(user_id)
        
        # Get today's date in user's timezone
        tz = pytz.timezone(user_timezone)
        now = datetime.now(tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Count incomplete tasks
        incomplete_body = self._count_incomplete_tasks('tasks_body', user_id, today_start, today_end)
        incomplete_mind = self._count_incomplete_tasks('tasks_mind', user_id, today_start, today_end)
        missed_alarms = self._count_missed_alarms(user_id, today_start, today_end)
        
        # Calculate penalties
        total_penalty = (
            (incomplete_body * self.PENALTY_BODY_TASK) +
            (incomplete_mind * self.PENALTY_MIND_TASK) +
            (missed_alarms * self.PENALTY_ROUTINE_ALARM)
        )
        
        # Get current scores from latest snapshot
        current_snapshot = self._get_latest_snapshot(user_id)
        current_body_score = current_snapshot.get('metrics', {}).get('score_body', 100) if current_snapshot else 100
        current_mind_score = current_snapshot.get('metrics', {}).get('score_mind', 100) if current_snapshot else 100
        
        # Calculate new scores
        new_body_score = max(self.MIN_SCORE, current_body_score - (incomplete_body * self.PENALTY_BODY_TASK))
        new_mind_score = max(self.MIN_SCORE, current_mind_score - (incomplete_mind * self.PENALTY_MIND_TASK))
        
        # Update snapshot
        self._update_user_snapshot(user_id, {
            'score_body': new_body_score,
            'score_mind': new_mind_score,
            'incomplete_body_tasks': incomplete_body,
            'incomplete_mind_tasks': incomplete_mind,
            'missed_alarms': missed_alarms,
            'total_penalty': total_penalty
        })
        
        return {
            'user_id': user_id,
            'status': 'success',
            'incomplete_body': incomplete_body,
            'incomplete_mind': incomplete_mind,
            'missed_alarms': missed_alarms,
            'total_penalty': total_penalty,
            'new_body_score': new_body_score,
            'new_mind_score': new_mind_score
        }
    
    def _get_user_timezone(self, user_id):
        """Get user's timezone from profile."""
        res = self.supabase.from_('profiles').select('timezone').eq('user_id', user_id).execute()
        if res.data and len(res.data) > 0:
            return res.data[0].get('timezone', 'America/Mexico_City')
        return 'America/Mexico_City'
    
    def _count_incomplete_tasks(self, table_name, user_id, start_time, end_time):
        """Count incomplete tasks for a user in a time range."""
        res = self.supabase.from_(table_name).select('id', count='exact').eq(
            'user_id', user_id
        ).eq(
            'status', 'pending'
        ).gte(
            'scheduled_at', start_time.isoformat()
        ).lte(
            'scheduled_at', end_time.isoformat()
        ).execute()
        
        return res.count or 0
    
    def _count_missed_alarms(self, user_id, start_time, end_time):
        """Count missed routine alarms for a user."""
        # Get active alarms for user
        res = self.supabase.from_('routine_alarms').select('*').eq(
            'user_id', user_id
        ).eq(
            'is_active', True
        ).execute()
        
        alarms = res.data or []
        
        # Check which alarms should have triggered today
        missed_count = 0
        current_day = start_time.weekday()  # 0=Monday, 6=Sunday
        
        for alarm in alarms:
            days_of_week = alarm.get('days_of_week', [])
            # Convert to Python weekday (0=Monday)
            # If alarm uses 0=Sunday, convert it
            if current_day in days_of_week or (current_day + 1) % 7 in days_of_week:
                # This alarm should have triggered today
                # In a real scenario, you'd check if it was actually completed
                # For now, we assume it was missed if no completion record exists
                missed_count += 1
        
        return missed_count
    
    def _get_latest_snapshot(self, user_id):
        """Get the most recent performance snapshot for a user."""
        res = self.supabase.from_('performance_snapshots').select('*').eq(
            'user_id', user_id
        ).order('snapshot_date', desc=True).limit(1).execute()
        
        return res.data[0] if res.data else None
    
    def _update_user_snapshot(self, user_id, metrics):
        """Update or create performance snapshot for user."""
        today = datetime.now().date().isoformat()
        
        # Try to get today's snapshot
        res = self.supabase.from_('performance_snapshots').select('*').eq(
            'user_id', user_id
        ).eq(
            'snapshot_date', today
        ).execute()
        
        if res.data:
            # Update existing snapshot
            snapshot_id = res.data[0]['id']
            current_metrics = res.data[0].get('metrics', {})
            current_metrics.update(metrics)
            
            self.supabase.from_('performance_snapshots').update({
                'metrics': current_metrics
            }).eq('id', snapshot_id).execute()
        else:
            # Create new snapshot
            self.supabase.from_('performance_snapshots').insert({
                'user_id': user_id,
                'snapshot_date': today,
                'metrics': metrics
            }).execute()
