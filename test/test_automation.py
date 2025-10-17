#!/usr/bin/env python3
"""
Test script for automation system.

Run this locally to test automation components before deploying.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automation.score_calculator import ScoreCalculator
from automation.notification_sender import NotificationSender
from automation.metrics_updater import MetricsUpdater
from automation.scheduler import AutomationScheduler


def test_score_calculator():
    """Test score calculator functionality."""
    print("\n" + "="*60)
    print("Testing Score Calculator")
    print("="*60)
    
    try:
        calculator = ScoreCalculator()
        results = calculator.calculate_daily_scores()
        
        print(f"✓ Score calculation completed for {len(results)} users")
        
        # Show sample results
        if results:
            print("\nSample results:")
            for i, result in enumerate(results[:3]):
                if result['status'] == 'success':
                    print(f"\nUser {i+1}:")
                    print(f"  - Incomplete body tasks: {result['incomplete_body']}")
                    print(f"  - Incomplete mind tasks: {result['incomplete_mind']}")
                    print(f"  - Total penalty: {result['total_penalty']}")
                    print(f"  - New body score: {result['new_body_score']}")
                    print(f"  - New mind score: {result['new_mind_score']}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_notification_sender():
    """Test notification sender functionality."""
    print("\n" + "="*60)
    print("Testing Notification Sender")
    print("="*60)
    
    try:
        sender = NotificationSender()
        results = sender.send_scheduled_notifications()
        
        print(f"✓ Notifications sent:")
        print(f"  - Alarms: {results['alarms_sent']}")
        print(f"  - Reminders: {results['reminders_sent']}")
        print(f"  - Errors: {len(results['errors'])}")
        
        if results['errors']:
            print("\nErrors encountered:")
            for error in results['errors'][:3]:
                print(f"  - {error}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_metrics_updater():
    """Test metrics updater functionality."""
    print("\n" + "="*60)
    print("Testing Metrics Updater")
    print("="*60)
    
    try:
        updater = MetricsUpdater()
        results = updater.update_all_metrics()
        
        print(f"✓ Metrics updated for {len(results)} users")
        
        # Show sample results
        if results:
            print("\nSample metrics:")
            for i, result in enumerate(results[:3]):
                if result['status'] == 'success':
                    metrics = result['metrics']
                    print(f"\nUser {i+1}:")
                    print(f"  - Completed body tasks: {metrics.get('completed_body_tasks', 0)}")
                    print(f"  - Completed mind tasks: {metrics.get('completed_mind_tasks', 0)}")
                    print(f"  - Body completion rate: {metrics.get('body_completion_rate', 0):.1f}%")
                    print(f"  - Mind completion rate: {metrics.get('mind_completion_rate', 0):.1f}%")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_scheduler():
    """Test scheduler functionality."""
    print("\n" + "="*60)
    print("Testing Scheduler")
    print("="*60)
    
    try:
        scheduler = AutomationScheduler()
        results = scheduler.run_hourly_tasks()
        
        print(f"✓ Scheduler executed {len(results['tasks_executed'])} tasks")
        
        for task in results['tasks_executed']:
            status_symbol = "✓" if task['status'] == 'success' else "✗"
            print(f"  {status_symbol} {task['task']}: {task['status']}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all automation tests."""
    print("\n" + "#"*60)
    print("# Automation System Test Suite")
    print(f"# Started at: {datetime.now()}")
    print("#"*60)
    
    tests = [
        ("Metrics Updater", test_metrics_updater),
        ("Notification Sender", test_notification_sender),
        ("Score Calculator", test_score_calculator),
        ("Scheduler", test_scheduler),
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return all(results.values())


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        test_map = {
            'scores': test_score_calculator,
            'notifications': test_notification_sender,
            'metrics': test_metrics_updater,
            'scheduler': test_scheduler,
            'all': run_all_tests
        }
        
        if test_name in test_map:
            success = test_map[test_name]()
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown test: {test_name}")
            print(f"Available tests: {', '.join(test_map.keys())}")
            sys.exit(1)
    else:
        # Run all tests by default
        success = run_all_tests()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
