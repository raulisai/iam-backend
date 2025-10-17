#!/usr/bin/env python3
"""
Management script for automation system.

Provides utilities to manage and monitor the automation system.
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db import get_supabase


def show_recent_snapshots(days=7, limit=10):
    """Show recent performance snapshots."""
    print(f"\nRecent Performance Snapshots (last {days} days):")
    print("="*80)
    
    supabase = get_supabase()
    cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
    
    res = supabase.from_('performance_snapshots').select(
        'user_id, snapshot_date, metrics'
    ).gte(
        'snapshot_date', cutoff_date
    ).order('snapshot_date', desc=True).limit(limit).execute()
    
    if not res.data:
        print("No snapshots found.")
        return
    
    for snapshot in res.data:
        metrics = snapshot.get('metrics', {})
        print(f"\nUser: {snapshot['user_id'][:8]}... | Date: {snapshot['snapshot_date']}")
        print(f"  Body Score: {metrics.get('score_body', 'N/A')}")
        print(f"  Mind Score: {metrics.get('score_mind', 'N/A')}")
        print(f"  Completed Tasks: Body={metrics.get('completed_body_tasks', 0)}, Mind={metrics.get('completed_mind_tasks', 0)}")
        print(f"  Pending Tasks: Body={metrics.get('pending_body_tasks', 0)}, Mind={metrics.get('pending_mind_tasks', 0)}")


def show_active_routines():
    """Show active routine alarms and reminders."""
    print("\nActive Routine Alarms and Reminders:")
    print("="*80)
    
    supabase = get_supabase()
    
    # Get active alarms
    alarms_res = supabase.from_('routine_alarms').select(
        'id, user_id, name, alarm_time, days_of_week, is_active', count='exact'
    ).eq('is_active', True).execute()
    
    # Get active reminders
    reminders_res = supabase.from_('routine_reminders').select(
        'id, user_id, name, times_per_day, days_of_week, is_active', count='exact'
    ).eq('is_active', True).execute()
    
    print(f"\nActive Alarms: {alarms_res.count or 0}")
    if alarms_res.data:
        for alarm in alarms_res.data[:5]:
            print(f"  - {alarm['name']} @ {alarm['alarm_time']} (User: {alarm['user_id'][:8]}...)")
    
    print(f"\nActive Reminders: {reminders_res.count or 0}")
    if reminders_res.data:
        for reminder in reminders_res.data[:5]:
            print(f"  - {reminder['name']} ({reminder['times_per_day']}x/day) (User: {reminder['user_id'][:8]}...)")


def show_device_tokens():
    """Show registered device tokens."""
    print("\nRegistered Device Tokens:")
    print("="*80)
    
    supabase = get_supabase()
    
    res = supabase.from_('device_tokens').select(
        'user_id, platform, is_active, created_at', count='exact'
    ).execute()
    
    total = res.count or 0
    active = len([t for t in (res.data or []) if t['is_active']])
    
    print(f"\nTotal Tokens: {total}")
    print(f"Active Tokens: {active}")
    print(f"Inactive Tokens: {total - active}")
    
    if res.data:
        print("\nBreakdown by platform:")
        platforms = {}
        for token in res.data:
            platform = token['platform']
            platforms[platform] = platforms.get(platform, 0) + 1
        
        for platform, count in platforms.items():
            print(f"  - {platform}: {count}")


def show_user_stats(user_id):
    """Show detailed stats for a specific user."""
    print(f"\nUser Statistics: {user_id}")
    print("="*80)
    
    supabase = get_supabase()
    
    # Get user info
    user_res = supabase.from_('users_iam').select('email').eq('id', user_id).execute()
    if not user_res.data:
        print("User not found.")
        return
    
    print(f"Email: {user_res.data[0]['email']}")
    
    # Get profile
    profile_res = supabase.from_('profiles').select('timezone').eq('user_id', user_id).execute()
    if profile_res.data:
        print(f"Timezone: {profile_res.data[0]['timezone']}")
    
    # Get recent snapshots
    snapshots_res = supabase.from_('performance_snapshots').select(
        'snapshot_date, metrics'
    ).eq('user_id', user_id).order('snapshot_date', desc=True).limit(7).execute()
    
    if snapshots_res.data:
        print(f"\nRecent Performance (last {len(snapshots_res.data)} days):")
        for snapshot in snapshots_res.data:
            metrics = snapshot.get('metrics', {})
            print(f"\n  {snapshot['snapshot_date']}:")
            print(f"    Body Score: {metrics.get('score_body', 'N/A')}")
            print(f"    Mind Score: {metrics.get('score_mind', 'N/A')}")
            print(f"    Tasks Completed: {metrics.get('completed_body_tasks', 0)} body, {metrics.get('completed_mind_tasks', 0)} mind")
    
    # Get active routines
    alarms_res = supabase.from_('routine_alarms').select('name', count='exact').eq(
        'user_id', user_id
    ).eq('is_active', True).execute()
    
    reminders_res = supabase.from_('routine_reminders').select('name', count='exact').eq(
        'user_id', user_id
    ).eq('is_active', True).execute()
    
    print(f"\nActive Routines:")
    print(f"  Alarms: {alarms_res.count or 0}")
    print(f"  Reminders: {reminders_res.count or 0}")


def cleanup_old_data(days=90, dry_run=True):
    """Clean up old performance snapshots."""
    print(f"\nCleaning up snapshots older than {days} days...")
    print("="*80)
    
    supabase = get_supabase()
    cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
    
    # Count old snapshots
    count_res = supabase.from_('performance_snapshots').select(
        'id', count='exact'
    ).lt('snapshot_date', cutoff_date).execute()
    
    count = count_res.count or 0
    
    if count == 0:
        print("No old snapshots to clean up.")
        return
    
    print(f"Found {count} snapshots older than {cutoff_date}")
    
    if dry_run:
        print("\n[DRY RUN] No data will be deleted. Run with --execute to actually delete.")
    else:
        confirm = input(f"\nAre you sure you want to delete {count} snapshots? (yes/no): ")
        if confirm.lower() == 'yes':
            res = supabase.from_('performance_snapshots').delete().lt(
                'snapshot_date', cutoff_date
            ).execute()
            print(f"✓ Deleted {len(res.data) if res.data else 0} snapshots")
        else:
            print("Cancelled.")


def show_help():
    """Show help message."""
    print("""
Automation Management Script

Usage:
  python scripts/manage_automation.py <command> [options]

Commands:
  snapshots [days]     Show recent performance snapshots (default: 7 days)
  routines             Show active routine alarms and reminders
  tokens               Show registered device tokens
  user <user_id>       Show detailed stats for a specific user
  cleanup [days]       Clean up old snapshots (default: 90 days, dry run)
  cleanup --execute    Actually delete old snapshots
  help                 Show this help message

Examples:
  python scripts/manage_automation.py snapshots
  python scripts/manage_automation.py snapshots 14
  python scripts/manage_automation.py user abc123-def456-...
  python scripts/manage_automation.py cleanup
  python scripts/manage_automation.py cleanup --execute
""")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == 'snapshots':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            show_recent_snapshots(days)
        
        elif command == 'routines':
            show_active_routines()
        
        elif command == 'tokens':
            show_device_tokens()
        
        elif command == 'user':
            if len(sys.argv) < 3:
                print("Error: user_id required")
                print("Usage: python scripts/manage_automation.py user <user_id>")
                sys.exit(1)
            show_user_stats(sys.argv[2])
        
        elif command == 'cleanup':
            days = 90
            execute = '--execute' in sys.argv
            cleanup_old_data(days, dry_run=not execute)
        
        elif command == 'help':
            show_help()
        
        else:
            print(f"Unknown command: {command}")
            show_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
