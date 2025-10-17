# Profile Goal Points System

## Overview

The profile goal points system tracks user progress on goals by accumulating points from completed tasks. This document explains how the system works and how to use the new endpoint.

## Database Schema

### New Columns in `profiles` table

- **`goal_points_target`** (NUMERIC): Total points available from all active goals and tasks
- **`goal_points_earned`** (NUMERIC): Points earned from completed tasks

Both columns have:
- Default value: 0
- Constraint: Must be non-negative (>= 0)

### Migration

Run the migration file to add these columns to existing databases:
```sql
-- File: db_schemas/profiles_migration_add_goal_points.sql
```

## How Points are Calculated

When a task occurrence is completed:

1. The system looks up the task occurrence by ID
2. Retrieves the task's `weight` value (default: 1)
3. Checks the task_logs for the completion entry
4. Uses `metadata.value` if present, otherwise uses the task `weight`
5. Adds the points to the user's `goal_points_earned`

## API Endpoint

### POST `/api/profile/add-goal-points`

Add points to the authenticated user's profile from a completed goal task.

#### Request

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Body:**
```json
{
  "task_occurrence_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Response

**Success (200):**
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "goal_points_target": 100,
  "goal_points_earned": 55.5,
  "points_added": 10,
  "previous_earned": 45.5,
  "timezone": "America/Mexico_City",
  "birth_date": "1990-01-15",
  "gender": "male",
  "weight_kg": 75.5,
  "height_cm": 175,
  "preferred_language": "es",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

- **400 Bad Request**: Task not completed or invalid request
  ```json
  {
    "error": "Task is not marked as completed"
  }
  ```

- **404 Not Found**: Task occurrence or profile not found
  ```json
  {
    "error": "Failed to add points. Task occurrence not found or profile not found."
  }
  ```

## Integration Flow

### Typical Usage

1. User completes a task occurrence
2. Task completion is logged in `task_logs` with action='completed'
3. Frontend/Backend calls `/api/profile/add-goal-points` with the `task_occurrence_id`
4. System validates the task is completed
5. Points are calculated and added to the user's profile
6. Updated profile is returned with points details

### Example Integration

```python
# After marking a task as completed
task_occurrence_id = "123e4567-e89b-12d3-a456-426614174000"

# Log the completion
log_task_completion(task_occurrence_id, user_id, metadata={'value': 15})

# Add points to profile
response = requests.post(
    'https://api.example.com/api/profile/add-goal-points',
    headers={'Authorization': f'Bearer {jwt_token}'},
    json={'task_occurrence_id': task_occurrence_id}
)

if response.status_code == 200:
    profile = response.json()
    print(f"Points added: {profile['points_added']}")
    print(f"Total earned: {profile['goal_points_earned']}")
```

## Related Tables

- **`goal_tasks`**: Contains task definitions with `weight` field
- **`task_occurrences`**: Specific instances of tasks to be completed
- **`task_logs`**: Logs of task actions (completed, skipped, etc.)
- **`goals`**: Parent goals that contain tasks

## Notes

- Points are only added for tasks with action='completed' in task_logs
- The system uses the most recent log entry for the task occurrence
- If `metadata.value` exists in the log, it takes precedence over task weight
- The endpoint is idempotent - calling it multiple times for the same completed task will add points each time (consider adding duplicate prevention if needed)
