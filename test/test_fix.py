"""
Script to test the time optimizer tasks-now endpoint fix
"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# User ID
user_id = "08e4e86f-4180-4255-aeaf-76ccdc33bc1b"

# Simulate the updated logic
target_date = datetime.now().date()
print(f"🔍 Testing with target_date: {target_date}")
print("=" * 60)

# Test mind tasks
print("\n📋 Mind Tasks:")
mind_res = supabase.from_('tasks_mind').select(
    'id, template_id, status, scheduled_at, task_templates(name, estimated_minutes)'
).eq('user_id', user_id).in_('status', ['pending', 'in_progress']).execute()

if mind_res.data:
    print(f"Found {len(mind_res.data)} pending/in_progress mind tasks")
    for task in mind_res.data:
        task_scheduled_at = task.get('scheduled_at')
        if task_scheduled_at:
            task_date = datetime.fromisoformat(task_scheduled_at.replace('Z', '+00:00')).date()
            should_include = task_date <= target_date
            status = "✅ INCLUDE" if should_include else "❌ EXCLUDE"
            print(f"  {status} - {task['id'][:8]}... scheduled: {task_date} (today: {target_date})")
        else:
            print(f"  ✅ INCLUDE - {task['id'][:8]}... (no schedule)")
else:
    print("No mind tasks found")

# Test body tasks
print("\n💪 Body Tasks:")
body_res = supabase.from_('tasks_body').select(
    'id, template_id, status, scheduled_at, task_templates(name, estimated_minutes)'
).eq('user_id', user_id).in_('status', ['pending', 'in_progress']).execute()

if body_res.data:
    print(f"Found {len(body_res.data)} pending/in_progress body tasks")
    for task in body_res.data:
        task_scheduled_at = task.get('scheduled_at')
        if task_scheduled_at:
            task_date = datetime.fromisoformat(task_scheduled_at.replace('Z', '+00:00')).date()
            should_include = task_date <= target_date
            status = "✅ INCLUDE" if should_include else "❌ EXCLUDE"
            print(f"  {status} - {task['id'][:8]}... scheduled: {task_date} (today: {target_date})")
        else:
            print(f"  ✅ INCLUDE - {task['id'][:8]}... (no schedule)")
else:
    print("No body tasks found")

print("\n" + "=" * 60)
print("✅ Test complete! Tasks with scheduled_at <= today should be included.")
