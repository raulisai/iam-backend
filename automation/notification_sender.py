"""Notification sender for routine reminders and alarms."""
from datetime import datetime, timedelta
from lib.db import get_supabase
from services.notification_service import send_alarm_to_user, send_notification_to_user
import pytz


class NotificationSender:
    """Send scheduled notifications based on routine alarms and reminders."""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    def send_scheduled_notifications(self):
        """Send all scheduled notifications for current time."""
        print(f"[{datetime.now()}] Checking scheduled notifications...")
        
        results = {
            'alarms_sent': 0,
            'reminders_sent': 0,
            'errors': []
        }
        
        # Process routine alarms
        alarm_results = self._process_routine_alarms()
        results['alarms_sent'] = alarm_results['sent']
        results['errors'].extend(alarm_results['errors'])
        
        # Process routine reminders
        reminder_results = self._process_routine_reminders()
        results['reminders_sent'] = reminder_results['sent']
        results['errors'].extend(reminder_results['errors'])
        
        print(f"Sent {results['alarms_sent']} alarms and {results['reminders_sent']} reminders")
        return results
    
    def _process_routine_alarms(self):
        """Process and send routine alarms that should trigger now."""
        results = {'sent': 0, 'errors': []}
        
        # Get all active alarms
        res = self.supabase.from_('routine_alarms').select('*').eq('is_active', True).execute()
        alarms = res.data or []
        
        for alarm in alarms:
            try:
                if self._should_trigger_alarm(alarm):
                    self._send_alarm_notification(alarm)
                    results['sent'] += 1
            except Exception as e:
                results['errors'].append({
                    'alarm_id': alarm['id'],
                    'error': str(e)
                })
        
        return results
    
    def _should_trigger_alarm(self, alarm):
        """Check if alarm should trigger at current time."""
        user_id = alarm['user_id']
        user_timezone = self._get_user_timezone(user_id)
        
        # Get current time in user's timezone
        tz = pytz.timezone(user_timezone)
        now = datetime.now(tz)
        
        # Check if today is in alarm's days_of_week
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        days_of_week = alarm.get('days_of_week', [])
        
        # Convert to match alarm format (might use 0=Sunday or 1=Monday)
        # Assuming 1=Monday, 7=Sunday format
        alarm_day = current_day + 1
        if alarm_day not in days_of_week:
            return False
        
        # Check if current time matches alarm time (within current hour)
        alarm_time = alarm.get('alarm_time', '')
        if not alarm_time:
            return False
        
        # Parse alarm time (format: "HH:MM:SS")
        alarm_hour = int(alarm_time.split(':')[0])
        current_hour = now.hour
        
        # Trigger if we're in the same hour
        return alarm_hour == current_hour
    
    def _send_alarm_notification(self, alarm):
        """Send notification for a routine alarm."""
        user_id = alarm['user_id']
        title = alarm.get('notification_title', 'Alarma')
        body = alarm.get('notification_body', 'Es hora de tu actividad')
        
        # Additional data for the notification
        data = {
            'type': 'routine_alarm',
            'alarm_id': alarm['id'],
            'source_type': alarm.get('source_type', 'custom'),
            'task_id': alarm.get('task_id', '')
        }
        
        # Send alarm notification
        send_alarm_to_user(
            user_id=user_id,
            mensaje=body,
            title=title,
            body=body,
            additional_data=data
        )
        
        print(f"Sent alarm notification to user {user_id}: {title}")
    
    def _process_routine_reminders(self):
        """Process and send routine reminders that should trigger now."""
        results = {'sent': 0, 'errors': []}
        
        # Get all active reminders
        res = self.supabase.from_('routine_reminders').select('*').eq('is_active', True).execute()
        reminders = res.data or []
        
        for reminder in reminders:
            try:
                if self._should_trigger_reminder(reminder):
                    self._send_reminder_notification(reminder)
                    results['sent'] += 1
            except Exception as e:
                results['errors'].append({
                    'reminder_id': reminder['id'],
                    'error': str(e)
                })
        
        return results
    
    def _should_trigger_reminder(self, reminder):
        """Check if reminder should trigger at current time."""
        user_id = reminder['user_id']
        user_timezone = self._get_user_timezone(user_id)
        
        # Get current time in user's timezone
        tz = pytz.timezone(user_timezone)
        now = datetime.now(tz)
        
        # Check if today is in reminder's days_of_week
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        days_of_week = reminder.get('days_of_week', [])
        
        # Convert to match reminder format
        reminder_day = current_day + 1
        if reminder_day not in days_of_week:
            return False
        
        # Check if current time is within reminder window
        start_time = reminder.get('start_time', '08:00:00')
        end_time = reminder.get('end_time', '22:00:00')
        times_per_day = reminder.get('times_per_day', 1)
        
        # Parse times
        start_hour = int(start_time.split(':')[0])
        end_hour = int(end_time.split(':')[0])
        current_hour = now.hour
        
        # Check if we're in the active window
        if not (start_hour <= current_hour <= end_hour):
            return False
        
        # Calculate interval between reminders
        active_hours = end_hour - start_hour
        if active_hours <= 0 or times_per_day <= 0:
            return False
        
        interval_hours = active_hours / times_per_day
        
        # Check if current hour matches a reminder slot
        hours_since_start = current_hour - start_hour
        slot_number = int(hours_since_start / interval_hours)
        expected_hour = start_hour + int(slot_number * interval_hours)
        
        return current_hour == expected_hour
    
    def _send_reminder_notification(self, reminder):
        """Send notification for a routine reminder."""
        user_id = reminder['user_id']
        title = reminder.get('notification_title', 'Recordatorio')
        body = reminder.get('notification_body', 'No olvides tu actividad')
        
        # Additional data for the notification
        data = {
            'type': 'routine_reminder',
            'reminder_id': reminder['id'],
            'source_type': reminder.get('source_type', 'custom'),
            'task_id': reminder.get('task_id', '')
        }
        
        # Send reminder notification
        send_notification_to_user(
            user_id=user_id,
            title=title,
            body=body,
            data=data
        )
        
        print(f"Sent reminder notification to user {user_id}: {title}")
    
    def _get_user_timezone(self, user_id):
        """Get user's timezone from profile."""
        res = self.supabase.from_('profiles').select('timezone').eq('user_id', user_id).execute()
        if res.data and len(res.data) > 0:
            return res.data[0].get('timezone', 'America/Mexico_City')
        return 'America/Mexico_City'
    
    def send_daily_summary(self):
        """Send daily summary notifications to users."""
        print(f"[{datetime.now()}] Sending daily summaries...")
        
        users = self._get_active_users()
        sent_count = 0
        
        for user in users:
            try:
                user_id = user['id']
                summary = self._generate_user_summary(user_id)
                
                if summary:
                    send_notification_to_user(
                        user_id=user_id,
                        title="Resumen del Día",
                        body=summary,
                        data={'type': 'daily_summary'}
                    )
                    sent_count += 1
            except Exception as e:
                print(f"Error sending summary to user {user['id']}: {str(e)}")
        
        print(f"Sent daily summaries to {sent_count} users")
        return {'sent': sent_count}
    
    def _get_active_users(self):
        """Get all active users."""
        res = self.supabase.from_('users_iam').select('id, email').execute()
        return res.data or []
    
    def _generate_user_summary(self, user_id):
        """Generate daily summary for user."""
        # Get today's snapshot
        today = datetime.now().date().isoformat()
        res = self.supabase.from_('performance_snapshots').select('*').eq(
            'user_id', user_id
        ).eq(
            'snapshot_date', today
        ).execute()
        
        if not res.data:
            return None
        
        metrics = res.data[0].get('metrics', {})
        
        completed_body = metrics.get('completed_body_tasks', 0)
        completed_mind = metrics.get('completed_mind_tasks', 0)
        score_body = metrics.get('score_body', 0)
        score_mind = metrics.get('score_mind', 0)
        
        summary = f"Completaste {completed_body} tareas físicas y {completed_mind} tareas mentales. "
        summary += f"Score Body: {score_body}, Score Mind: {score_mind}."
        
        return summary
