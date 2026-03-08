from lib.db import get_supabase
from services.auth_service import hash_password, verify_password
import uuid

def test_flow():
    print("Testing DB Connection and Logic...")
    
    db = get_supabase()
    
    # 1. Create a test user
    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    hashed = hash_password(password)
    
    print(f"Creating user {email}...")
    user_data = {
        "email": email,
        "name": "Test User",
        "hashed_password": hashed
    }
    
    user_res = db.from_('users_iam').insert(user_data).execute()
    if not user_res.data:
        print("FAILED: Could not create user")
        return
        
    user = user_res.data[0]
    print(f"User created with ID: {user['id']}")
    
    # 2. Verify password
    print("Verifying password...")
    if verify_password(user['hashed_password'], password):
        print("Password verification passed")
    else:
        print("FAILED: Password verification failed")

    # 3. Create Template
    print("Creating task template...")
    template_data = {
        "key": f"temp_{uuid.uuid4()}",
        "category": "mind",
        "name": "Test Meditation",
        "desc": "Just a test"
    }
    tpl_res = db.from_('task_templates').insert(template_data).execute()
    template = tpl_res.data[0]
    print(f"Template created: {template['id']}")

    # 4. Create Mind Task
    print("Creating mind task...")
    task_data = {
        "user_id": user['id'],
        "template_id": template['id'],
        "status": "pending"
    }
    task_res = db.from_('tasks_mind').insert(task_data).execute()
    task = task_res.data[0]
    print(f"Task created: {task['id']}")

    # 5. Fetch task with join logic (simulating service)
    print("Fetching task with join...")
    
    fetched_res = db.from_('tasks_mind').select('*').eq('id', task['id']).execute()
    fetched_task = fetched_res.data[0]
    
    if fetched_task.get('template_id'):
        tpl_res_2 = db.from_('task_templates').select('*').eq('id', fetched_task['template_id']).execute()
        if tpl_res_2.data:
            fetched_task['task_templates'] = tpl_res_2.data[0]
    
    if 'task_templates' in fetched_task and fetched_task['task_templates']['name'] == "Test Meditation":
        print("SUCCESS: Task fetched and template joined correctly!")
    else:
        print("FAILED: Join logic incorrect")
        print(fetched_task)

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"TEST FAILED with error: {e}")
