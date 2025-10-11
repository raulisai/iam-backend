"""Test final - verificar que traiga todas las tareas categorizadas."""
import sys
from services.time_optimizer_service import get_tasks_for_current_moment
from services.mind_task_service import get_user_mind_tasks
from services.body_task_service import get_user_body_tasks
from lib.db import get_supabase

# Test user ID
USER_ID = "6a012777-fdaf-4ee1-b41b-b59f48374f59"

print("=" * 80)
print("Testing Time Optimizer - FINAL VERSION")
print("=" * 80)

# Check existing tasks in database
print("\n1. Verificando tareas existentes en BD...")
try:
    supabase = get_supabase()
    
    # Count goal tasks
    goals_res = supabase.from_('goal_tasks').select('id', count='exact').eq('user_id', USER_ID).execute()
    print(f"   Goal tasks en BD: {goals_res.count if hasattr(goals_res, 'count') else len(goals_res.data or [])}")
    
    # Count mind tasks
    mind_tasks = get_user_mind_tasks(USER_ID)
    mind_pending = [t for t in mind_tasks if t['status'] in ['pending', 'in_progress']]
    print(f"   Mind tasks en BD: {len(mind_tasks)} total, {len(mind_pending)} pending/in_progress")
    
    # Count body tasks
    body_tasks = get_user_body_tasks(USER_ID)
    body_pending = [t for t in body_tasks if t['status'] in ['pending', 'in_progress']]
    print(f"   Body tasks en BD: {len(body_tasks)} total, {len(body_pending)} pending/in_progress")
    
except Exception as e:
    print(f"   Error verificando BD: {e}")

# Test the endpoint
print("\n2. Testing get_tasks_for_current_moment()...")
try:
    result = get_tasks_for_current_moment(USER_ID)
    
    if 'error' in result:
        print(f"   ✗ Error: {result.get('message', 'Unknown error')}")
        sys.exit(1)
    
    print(f"\n   Time slot: {result.get('time_slot', 'N/A')}")
    print(f"   Remaining minutes: {result.get('remaining_minutes_in_slot', 0)}")
    print(f"   Total available tasks: {result.get('total_available_tasks', 0)}")
    
    # Check arrays
    goal_tasks = result.get('goal_tasks', [])
    mind_tasks = result.get('mind_tasks', [])
    body_tasks = result.get('body_tasks', [])
    quick_wins = result.get('quick_wins', [])
    
    print(f"\n   ✓ Goal tasks: {len(goal_tasks)}")
    print(f"   ✓ Mind tasks: {len(mind_tasks)}")
    print(f"   ✓ Body tasks: {len(body_tasks)}")
    print(f"   ✓ Quick wins: {len(quick_wins)}")
    
    # Verify sum
    total_categorized = len(goal_tasks) + len(mind_tasks) + len(body_tasks)
    total_available = result.get('total_available_tasks', 0)
    
    print(f"\n   Verification:")
    print(f"   - Total available: {total_available}")
    print(f"   - Total categorized (goal+mind+body): {total_categorized}")
    
    if total_categorized == total_available:
        print(f"   ✓ CORRECTO: Todas las tareas están categorizadas")
    else:
        print(f"   ✗ WARNING: Números no coinciden")
    
    # Check that recommended_tasks is NOT in response
    if 'recommended_tasks' in result:
        print(f"   ✗ ERROR: recommended_tasks NO debería estar en la respuesta")
    else:
        print(f"   ✓ CORRECTO: recommended_tasks fue removido")
    
    # Show samples
    if goal_tasks:
        print(f"\n   Sample goal task: {goal_tasks[0].get('title', 'N/A')}")
    if mind_tasks:
        print(f"   Sample mind task: {mind_tasks[0].get('title', 'N/A')}")
    if body_tasks:
        print(f"   Sample body task: {body_tasks[0].get('title', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("✓ Test completed successfully!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
