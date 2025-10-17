"""Main scheduler for automation tasks."""
from datetime import datetime
from automation.score_calculator import ScoreCalculator
from automation.notification_sender import NotificationSender
from automation.metrics_updater import MetricsUpdater
import pytz


class AutomationScheduler:
    """Orchestrate all automation tasks based on time and schedule."""
    
    def __init__(self):
        self.score_calculator = ScoreCalculator()
        self.notification_sender = NotificationSender()
        self.metrics_updater = MetricsUpdater()
    
    def run_hourly_tasks(self):
        """Run tasks that should execute every hour."""
        print(f"\n{'='*60}")
        print(f"HOURLY AUTOMATION RUN - {datetime.now()}")
        print(f"{'='*60}\n")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tasks_executed': []
        }
        
        current_hour = datetime.now().hour
        
        # 1. Send scheduled notifications (every hour)
        print("\n[TASK] Sending scheduled notifications...")
        try:
            notification_results = self.notification_sender.send_scheduled_notifications()
            results['tasks_executed'].append({
                'task': 'send_notifications',
                'status': 'success',
                'results': notification_results
            })
        except Exception as e:
            print(f"Error sending notifications: {str(e)}")
            results['tasks_executed'].append({
                'task': 'send_notifications',
                'status': 'error',
                'error': str(e)
            })
        
        # 2. Update metrics (every hour)
        print("\n[TASK] Updating user metrics...")
        try:
            metrics_results = self.metrics_updater.update_all_metrics()
            results['tasks_executed'].append({
                'task': 'update_metrics',
                'status': 'success',
                'results': metrics_results
            })
        except Exception as e:
            print(f"Error updating metrics: {str(e)}")
            results['tasks_executed'].append({
                'task': 'update_metrics',
                'status': 'error',
                'error': str(e)
            })
        
        # 3. Calculate daily scores (at 11 PM)
        if current_hour == 23:
            print("\n[TASK] Calculating daily scores (end of day)...")
            try:
                score_results = self.score_calculator.calculate_daily_scores()
                results['tasks_executed'].append({
                    'task': 'calculate_scores',
                    'status': 'success',
                    'results': score_results
                })
            except Exception as e:
                print(f"Error calculating scores: {str(e)}")
                results['tasks_executed'].append({
                    'task': 'calculate_scores',
                    'status': 'error',
                    'error': str(e)
                })
            
            # Send daily summaries
            print("\n[TASK] Sending daily summaries...")
            try:
                summary_results = self.notification_sender.send_daily_summary()
                results['tasks_executed'].append({
                    'task': 'send_daily_summary',
                    'status': 'success',
                    'results': summary_results
                })
            except Exception as e:
                print(f"Error sending daily summaries: {str(e)}")
                results['tasks_executed'].append({
                    'task': 'send_daily_summary',
                    'status': 'error',
                    'error': str(e)
                })
        
        # 4. Weekly cleanup (Sunday at midnight)
        if datetime.now().weekday() == 6 and current_hour == 0:
            print("\n[TASK] Running weekly cleanup...")
            try:
                cleanup_results = self.metrics_updater.cleanup_old_snapshots(days_to_keep=90)
                results['tasks_executed'].append({
                    'task': 'cleanup_snapshots',
                    'status': 'success',
                    'results': cleanup_results
                })
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")
                results['tasks_executed'].append({
                    'task': 'cleanup_snapshots',
                    'status': 'error',
                    'error': str(e)
                })
            
            # Generate weekly reports
            print("\n[TASK] Generating weekly reports...")
            try:
                report_results = self.metrics_updater.generate_weekly_report()
                results['tasks_executed'].append({
                    'task': 'weekly_reports',
                    'status': 'success',
                    'results': report_results
                })
            except Exception as e:
                print(f"Error generating weekly reports: {str(e)}")
                results['tasks_executed'].append({
                    'task': 'weekly_reports',
                    'status': 'error',
                    'error': str(e)
                })
        
        print(f"\n{'='*60}")
        print(f"HOURLY AUTOMATION COMPLETED")
        print(f"Tasks executed: {len(results['tasks_executed'])}")
        print(f"{'='*60}\n")
        
        return results
    
    def run_specific_task(self, task_name):
        """Run a specific automation task manually."""
        print(f"\n[MANUAL RUN] Executing task: {task_name}")
        
        task_map = {
            'notifications': self.notification_sender.send_scheduled_notifications,
            'metrics': self.metrics_updater.update_all_metrics,
            'scores': self.score_calculator.calculate_daily_scores,
            'daily_summary': self.notification_sender.send_daily_summary,
            'cleanup': self.metrics_updater.cleanup_old_snapshots,
            'weekly_report': self.metrics_updater.generate_weekly_report
        }
        
        if task_name not in task_map:
            print(f"Unknown task: {task_name}")
            print(f"Available tasks: {', '.join(task_map.keys())}")
            return {'status': 'error', 'error': f'Unknown task: {task_name}'}
        
        try:
            result = task_map[task_name]()
            print(f"Task {task_name} completed successfully")
            return {'status': 'success', 'result': result}
        except Exception as e:
            print(f"Error executing task {task_name}: {str(e)}")
            return {'status': 'error', 'error': str(e)}
