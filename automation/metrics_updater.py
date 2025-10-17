"""Metrics updater for tracking user performance and statistics."""
from datetime import datetime, timedelta
from lib.db import get_supabase
import pytz


class MetricsUpdater:
    """Update user metrics and performance snapshots."""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    def update_all_metrics(self):
        """Update metrics for all users."""
        print(f"[{datetime.now()}] Starting metrics update...")
        
        users = self._get_active_users()
        print(f"Updating metrics for {len(users)} users")
        
        results = []
        for user in users:
            try:
                result = self._update_user_metrics(user)
                results.append(result)
            except Exception as e:
                print(f"Error updating metrics for user {user['id']}: {str(e)}")
                results.append({
                    'user_id': user['id'],
                    'status': 'error',
                    'error': str(e)
                })
        
        print(f"Completed metrics update for {len(results)} users")
        return results
    
    def _get_active_users(self):
        """Get all active users."""
        res = self.supabase.from_('users_iam').select('id, email').execute()
        return res.data or []
    
    def _update_user_metrics(self, user):
        """Update metrics for a specific user."""
        user_id = user['id']
        user_timezone = self._get_user_timezone(user_id)
        
        # Get today's date in user's timezone
        tz = pytz.timezone(user_timezone)
        now = datetime.now(tz)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Collect metrics
        metrics = {}
        
        # Task completion metrics
        metrics['completed_body_tasks'] = self._count_completed_tasks('tasks_body', user_id, today_start, today_end)
        metrics['completed_mind_tasks'] = self._count_completed_tasks('tasks_mind', user_id, today_start, today_end)
        metrics['pending_body_tasks'] = self._count_pending_tasks('tasks_body', user_id, today_start, today_end)
        metrics['pending_mind_tasks'] = self._count_pending_tasks('tasks_mind', user_id, today_start, today_end)
        
        # Calculate completion rates
        total_body = metrics['completed_body_tasks'] + metrics['pending_body_tasks']
        total_mind = metrics['completed_mind_tasks'] + metrics['pending_mind_tasks']
        
        metrics['body_completion_rate'] = (
            (metrics['completed_body_tasks'] / total_body * 100) if total_body > 0 else 0
        )
        metrics['mind_completion_rate'] = (
            (metrics['completed_mind_tasks'] / total_mind * 100) if total_mind > 0 else 0
        )
        
        # Active routines
        metrics['active_alarms'] = self._count_active_routines('routine_alarms', user_id)
        metrics['active_reminders'] = self._count_active_routines('routine_reminders', user_id)
        
        # Update timestamp
        metrics['last_updated'] = now.isoformat()
        
        # Save to performance snapshot
        self._update_snapshot(user_id, metrics)
        
        return {
            'user_id': user_id,
            'status': 'success',
            'metrics': metrics
        }
    
    def _get_user_timezone(self, user_id):
        """Get user's timezone from profile."""
        res = self.supabase.from_('profiles').select('timezone').eq('user_id', user_id).execute()
        if res.data and len(res.data) > 0:
            return res.data[0].get('timezone', 'America/Mexico_City')
        return 'America/Mexico_City'
    
    def _count_completed_tasks(self, table_name, user_id, start_time, end_time):
        """Count completed tasks for a user in a time range."""
        res = self.supabase.from_(table_name).select('id', count='exact').eq(
            'user_id', user_id
        ).eq(
            'status', 'completed'
        ).gte(
            'completed_at', start_time.isoformat()
        ).lte(
            'completed_at', end_time.isoformat()
        ).execute()
        
        return res.count or 0
    
    def _count_pending_tasks(self, table_name, user_id, start_time, end_time):
        """Count pending tasks for a user in a time range."""
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
    
    def _count_active_routines(self, table_name, user_id):
        """Count active routines for a user."""
        res = self.supabase.from_(table_name).select('id', count='exact').eq(
            'user_id', user_id
        ).eq(
            'is_active', True
        ).execute()
        
        return res.count or 0
    
    def _update_snapshot(self, user_id, metrics):
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
    
    def cleanup_old_snapshots(self, days_to_keep=90):
        """Clean up old performance snapshots."""
        print(f"[{datetime.now()}] Cleaning up snapshots older than {days_to_keep} days...")
        
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).date().isoformat()
        
        res = self.supabase.from_('performance_snapshots').delete().lt(
            'snapshot_date', cutoff_date
        ).execute()
        
        deleted_count = len(res.data) if res.data else 0
        print(f"Deleted {deleted_count} old snapshots")
        
        return {'deleted': deleted_count}
    
    def generate_weekly_report(self):
        """Generate weekly performance reports for all users."""
        print(f"[{datetime.now()}] Generating weekly reports...")
        
        users = self._get_active_users()
        reports = []
        
        for user in users:
            try:
                report = self._generate_user_weekly_report(user['id'])
                reports.append(report)
            except Exception as e:
                print(f"Error generating report for user {user['id']}: {str(e)}")
        
        print(f"Generated {len(reports)} weekly reports")
        return reports
    
    def _generate_user_weekly_report(self, user_id):
        """Generate weekly report for a specific user."""
        # Get last 7 days of snapshots
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        res = self.supabase.from_('performance_snapshots').select('*').eq(
            'user_id', user_id
        ).gte(
            'snapshot_date', start_date.isoformat()
        ).lte(
            'snapshot_date', end_date.isoformat()
        ).order('snapshot_date', desc=False).execute()
        
        snapshots = res.data or []
        
        if not snapshots:
            return {
                'user_id': user_id,
                'period': 'week',
                'data': None
            }
        
        # Aggregate metrics
        total_body_completed = sum(s.get('metrics', {}).get('completed_body_tasks', 0) for s in snapshots)
        total_mind_completed = sum(s.get('metrics', {}).get('completed_mind_tasks', 0) for s in snapshots)
        
        avg_body_score = sum(s.get('metrics', {}).get('score_body', 0) for s in snapshots) / len(snapshots)
        avg_mind_score = sum(s.get('metrics', {}).get('score_mind', 0) for s in snapshots) / len(snapshots)
        
        return {
            'user_id': user_id,
            'period': 'week',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'data': {
                'total_body_tasks_completed': total_body_completed,
                'total_mind_tasks_completed': total_mind_completed,
                'avg_body_score': round(avg_body_score, 2),
                'avg_mind_score': round(avg_mind_score, 2),
                'days_tracked': len(snapshots)
            }
        }
