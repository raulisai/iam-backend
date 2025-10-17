#!/usr/bin/env python3
"""
Automation runner script for scheduled tasks.

This script is executed by GitHub Actions on an hourly schedule.
It orchestrates all automation tasks including:
- Sending scheduled notifications
- Updating user metrics
- Calculating daily scores
- Cleaning up old data
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automation.scheduler import AutomationScheduler


def main():
    """Main entry point for automation script."""
    print(f"\n{'#'*70}")
    print(f"# IAM Backend Automation Script")
    print(f"# Started at: {datetime.now()}")
    print(f"{'#'*70}\n")
    
    try:
        # Initialize scheduler
        scheduler = AutomationScheduler()
        
        # Check if specific task was requested
        if len(sys.argv) > 1:
            task_name = sys.argv[1]
            print(f"Running specific task: {task_name}\n")
            result = scheduler.run_specific_task(task_name)
        else:
            # Run all hourly tasks
            print("Running all hourly tasks\n")
            result = scheduler.run_hourly_tasks()
        
        # Print summary
        print("\n" + "="*70)
        print("EXECUTION SUMMARY")
        print("="*70)
        
        if isinstance(result, dict):
            if 'tasks_executed' in result:
                for task in result['tasks_executed']:
                    status_symbol = "✓" if task['status'] == 'success' else "✗"
                    print(f"{status_symbol} {task['task']}: {task['status']}")
            else:
                print(f"Status: {result.get('status', 'unknown')}")
        
        print("="*70 + "\n")
        
        # Exit with appropriate code
        if isinstance(result, dict) and result.get('status') == 'error':
            sys.exit(1)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n{'!'*70}")
        print(f"CRITICAL ERROR: {str(e)}")
        print(f"{'!'*70}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
