"""Debug - verificar scheduled_at de mind y body tasks."""
from services.mind_task_service import get_user_mind_tasks
from services.body_task_service import get_user_body_tasks

USER_ID = "6a012777-fdaf-4ee1-b41b-b59f48374f59"

print("Mind tasks pending:")
mind_tasks = get_user_mind_tasks(USER_ID)
mind_pending = [t for t in mind_tasks if t['status'] in ['pending', 'in_progress']]
for task in mind_pending[:3]:  # Show first 3
    print(f"  - {task.get('id')}: scheduled_at = {task.get('scheduled_at')}")

print("\nBody tasks pending:")
body_tasks = get_user_body_tasks(USER_ID)
body_pending = [t for t in body_tasks if t['status'] in ['pending', 'in_progress']]
for task in body_pending[:3]:  # Show first 3
    print(f"  - {task.get('id')}: scheduled_at = {task.get('scheduled_at')}")
