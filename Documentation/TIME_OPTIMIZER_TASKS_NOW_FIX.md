# Time Optimizer Tasks-Now Endpoint Fix

## Problem
The `/api/time-optimizer/tasks-now` endpoint was returning empty arrays for body, mind, and goal tasks:
- `total_available_tasks: 0`
- No task arrays in response
- Tasks were being filtered out because they didn't have a `scheduled_at` date matching today

## Solution Implemented

### 1. Added `include_unscheduled` Parameter
Modified `get_pending_tasks_all_types()` function to accept an `include_unscheduled` parameter (default: `True`):

```python
def get_pending_tasks_all_types(user_id: str, target_date: str = None, include_unscheduled: bool = True) -> Dict[str, List[Dict]]:
```

### 2. Updated Task Filtering Logic

#### Mind Tasks
- Now includes tasks without `scheduled_at` if `include_unscheduled=True`
- Tasks scheduled for target date are always included
- Pending and in-progress tasks are retrieved

#### Body Tasks
- Same logic as mind tasks
- Includes unscheduled pending/in-progress tasks
- Filters by target date if scheduled

#### Goal Tasks
- Retrieves task occurrences for the target date (scheduled tasks)
- **NEW**: Also retrieves goal tasks without occurrences (unscheduled tasks)
- Prevents duplicates by tracking scheduled task IDs
- Calculates urgency based on goal deadline

### 3. Enhanced Response Format

Added separate arrays for each task type in the response:

```json
{
  "user_id": "...",
  "current_time": "...",
  "time_slot": "morning",
  "remaining_minutes_in_slot": 47574,
  "remaining_hours_in_slot": 792.9,
  "recommended_tasks": [...],
  "total_available_tasks": 15,
  "quick_wins": [...],
  "goal_tasks": [...],      // NEW: Array of goal tasks
  "mind_tasks": [...],      // NEW: Array of mind tasks
  "body_tasks": [...],      // NEW: Array of body tasks
  "message": "You have 47574 minutes remaining in your morning slot"
}
```

## Code Changes

### File: `services/time_optimizer_service.py`

#### Change 1: Function Signature
```python
# Before
def get_pending_tasks_all_types(user_id: str, target_date: str = None) -> Dict[str, List[Dict]]:

# After
def get_pending_tasks_all_types(user_id: str, target_date: str = None, include_unscheduled: bool = True) -> Dict[str, List[Dict]]:
```

#### Change 2: Mind Tasks Logic
```python
# Added check for unscheduled tasks
if task_scheduled_at:
    task_date = datetime.fromisoformat(task_scheduled_at.replace('Z', '+00:00')).date()
    if task_date == date_obj:
        should_include = True
elif include_unscheduled:
    # Include tasks without specific schedule
    should_include = True
```

#### Change 3: Body Tasks Logic
Same logic as mind tasks - includes unscheduled tasks when `include_unscheduled=True`

#### Change 4: Goal Tasks Logic
```python
# Added retrieval of unscheduled goal tasks
if include_unscheduled:
    goal_tasks_res = supabase.from_('goal_tasks').select(
        'id, title, description, type, weight, goal_id, goals(title, end_at)'
    ).eq('status', 'pending').execute()
    
    # Skip tasks already scheduled (avoid duplicates)
    scheduled_task_ids = {t['task_id'] for t in tasks_by_type['goals'] if t.get('task_id')}
    # ... process unscheduled tasks
```

#### Change 5: Response Structure in `get_tasks_for_current_moment()`
```python
# Organize all available tasks by type
tasks_by_type = {
    'goal_tasks': [t for t in available_now if t['type'] == 'goal'],
    'mind_tasks': [t for t in available_now if t['type'] == 'mind'],
    'body_tasks': [t for t in available_now if t['type'] == 'body']
}

return {
    # ... existing fields
    'goal_tasks': tasks_by_type['goal_tasks'],
    'mind_tasks': tasks_by_type['mind_tasks'],
    'body_tasks': tasks_by_type['body_tasks'],
    # ...
}
```

## Testing

### Test the Endpoint
```bash
curl -X GET "http://localhost:5000/api/time-optimizer/tasks-now" \
  -H "accept: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Expected Response
```json
{
  "body_tasks": [
    {
      "id": "...",
      "title": "Exercise Routine",
      "type": "body",
      "estimated_duration_minutes": 30,
      "priority_score": 15.0,
      "start_time": "2025-10-11T06:00:00",
      "end_time": "2025-10-11T06:30:00",
      "time_slot": "morning"
    }
  ],
  "mind_tasks": [
    {
      "id": "...",
      "title": "Learn Python",
      "type": "mind",
      "estimated_duration_minutes": 60,
      "priority_score": 17.0,
      "start_time": "2025-10-11T06:30:00",
      "end_time": "2025-10-11T07:30:00",
      "time_slot": "morning"
    }
  ],
  "goal_tasks": [
    {
      "id": "...",
      "title": "Complete Project Milestone",
      "type": "goal",
      "goal_title": "Career Growth 2025",
      "goal_deadline": "2025-12-31T23:59:59",
      "days_until_deadline": 81,
      "urgency_multiplier": 1.0,
      "estimated_duration_minutes": 60,
      "priority_score": 30.0,
      "start_time": "2025-10-11T07:30:00",
      "end_time": "2025-10-11T08:30:00",
      "time_slot": "morning"
    }
  ],
  "recommended_tasks": [...],
  "quick_wins": [...],
  "total_available_tasks": 15,
  "current_time": "2025-10-11T06:06:26.934059",
  "time_slot": "morning",
  "remaining_minutes_in_slot": 165,
  "remaining_hours_in_slot": 2.75,
  "message": "You have 165 minutes remaining in your morning slot"
}
```

## Benefits

1. **Complete Task Visibility**: Users now see all their pending tasks, not just scheduled ones
2. **Flexible Scheduling**: Unscheduled tasks can be included in optimization
3. **Better Planning**: Separate arrays make it easy to see what type of tasks are available
4. **Backward Compatible**: Existing functionality preserved with new parameter defaulting to `True`

## Related Files
- `services/time_optimizer_service.py` - Main service with algorithm
- `controllers/time_optimizer_controller.py` - Controller for endpoints
- `routes/time_optimizer_routes.py` - Route definitions

## API Reference
See: `Documentation/TIME_OPTIMIZER_CURL_EXAMPLES.md` for more examples
