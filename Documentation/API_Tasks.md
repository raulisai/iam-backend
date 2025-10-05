# IAM Backend API - Tasks and Templates

## Overview
This document details the Task Templates, Mind Tasks, Body Tasks, Task Logs, and Failures endpoints. These endpoints manage task creation, completion, logging, and failure tracking. All endpoints require JWT authentication.

## Task Templates

### GET /api/task-templates
Retrieves all task templates.

**Endpoint:** `GET /api/task-templates`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Query Parameters:**
- None

**Success Response (200):**
```json
[
  {
    "id": "template-uuid",
    "key": "meditation_10",
    "name": "Meditación 10 minutos",
    "category": "mind",
    "estimated_minutes": 10,
    "difficulty": 2,
    "reward_xp": 50,
    "descr": "Sesión de meditación guiada de 10 minutos",
    "default_params": {
      "type": "guided",
      "music": true
    },
    "created_at": "2025-10-01T00:00:00Z"
  }
]
```

**Frontend Integration Notes:**
- Cache templates locally for performance
- Use for populating task creation forms
- Filter by category in UI

### GET /api/task-templates/<template_id>
Retrieves a specific task template by ID.

**Endpoint:** `GET /api/task-templates/{template_id}`

**Path Parameters:**
- `template_id`: UUID of the template

**Success Response (200):** Single template object as above

**Error Responses:**
- `404 Not Found`: Template not found

### GET /api/task-templates/key/<key>
Retrieves a template by its unique key.

**Endpoint:** `GET /api/task-templates/key/{key}`

**Path Parameters:**
- `key`: String key (e.g., "meditation_10")

**Success Response (200):** Single template object

### GET /api/task-templates/category/<category>
Retrieves templates by category.

**Endpoint:** `GET /api/task-templates/category/{category}`

**Path Parameters:**
- `category`: "mind" or "body"

**Success Response (200):** Array of template objects

### POST /api/task-templates
Creates a new task template.

**Endpoint:** `POST /api/task-templates`

**Request Body:**
```json
{
  "key": "string",  // Required: Unique identifier
  "name": "string",  // Required: Display name
  "category": "string",  // Required: "mind" or "body"
  "estimated_minutes": "number",  // Required: Estimated duration
  "difficulty": "number",  // Required: 1-5 scale
  "reward_xp": "number",  // Required: XP reward
  "descr": "string",  // Optional: Description
  "default_params": {}  // Optional: JSON object with default parameters
}
```

**Success Response (201):** Created template object

### PUT /api/task-templates/<template_id>
Updates a task template.

**Endpoint:** `PUT /api/task-templates/{template_id}`

**Request Body:** Same as POST, all fields optional for partial update

**Success Response (200):** Updated template object

### DELETE /api/task-templates/<template_id>
Deletes a task template.

**Endpoint:** `DELETE /api/task-templates/{template_id}`

**Success Response (200):**
```json
{
  "message": "Template deleted successfully"
}
```

## Mind Tasks

### GET /api/tasks/mind
Retrieves mind tasks for the authenticated user.

**Endpoint:** `GET /api/tasks/mind`

**Query Parameters:**
- `status`: "pending", "completed", "cancelled" (optional)

**Success Response (200):**
```json
[
  {
    "id": "task-uuid",
    "template_id": "template-uuid",
    "user_id": "user-uuid",
    "created_by": "user",
    "status": "pending",
    "scheduled_at": "2025-10-01T10:00:00Z",
    "completed_at": null,
    "params": {
      "duration": 10
    },
    "created_at": "2025-10-01T00:00:00Z",
    "updated_at": "2025-10-01T00:00:00Z"
  }
]
```

### GET /api/tasks/mind/<task_id>
Retrieves a specific mind task.

**Endpoint:** `GET /api/tasks/mind/{task_id}`

### POST /api/tasks/mind
Creates a new mind task.

**Request Body:**
```json
{
  "template_id": "uuid",  // Required
  "created_by": "user",  // Usually "user"
  "scheduled_at": "2025-10-01T10:00:00Z",  // Optional
  "params": {}  // Optional: Task-specific parameters
}
```

### PUT /api/tasks/mind/<task_id>
Updates a mind task.

**Request Body:**
```json
{
  "status": "string",  // Optional
  "scheduled_at": "string",  // Optional
  "params": {}  // Optional
}
```

### POST /api/tasks/mind/<task_id>/complete
Marks a task as completed.

**Success Response (200):** Updated task object with `completed_at` set

### DELETE /api/tasks/mind/<task_id>
Deletes a mind task.

## Body Tasks
Same endpoints as Mind Tasks but with `/api/tasks/body` base path.

**Note:** All operations identical to mind tasks, just different table.

## Task Logs

### GET /api/task-logs
Retrieves task logs.

**Query Parameters:**
- `task_table`: "tasks_mind" or "tasks_body" (optional)

**Success Response (200):**
```json
[
  {
    "id": "log-uuid",
    "task_table": "tasks_mind",
    "task_id": "task-uuid",
    "user_id": "user-uuid",
    "action": "completed",
    "metadata": {
      "duration": 600,
      "notes": "Great session"
    },
    "created_at": "2025-10-01T00:00:00Z"
  }
]
```

### POST /api/task-logs
Creates a new task log entry.

**Request Body:**
```json
{
  "task_table": "string",  // Required: "tasks_mind" or "tasks_body"
  "task_id": "uuid",  // Required
  "action": "string",  // Required: e.g., "completed", "started"
  "metadata": {}  // Optional: JSON object
}
```

## Failures

### GET /api/failures
Retrieves user failures.

**Query Parameters:**
- `severity`: "minor", "major", "critical" (optional)

**Success Response (200):**
```json
[
  {
    "id": "failure-uuid",
    "task_table": "tasks_mind",
    "task_id": "task-uuid",
    "user_id": "user-uuid",
    "reason": "Olvidé hacer la tarea",
    "severity": "minor",
    "notes": "Reprogramar para mañana",
    "title": "Falta de gestión del tiempo",
    "rootCause": "Sobrecarga de trabajo sin planificación adecuada",
    "prevention": "Implementar técnica Pomodoro y planificación semanal",
    "created_at": "2025-10-01T00:00:00Z"
  }
]
```

### POST /api/failures
Creates a failure record.

**Request Body:**
```json
{
  "task_table": "string",  // Required: "tasks_mind" or "tasks_body"
  "task_id": "uuid",  // Required
  "reason": "string",  // Required
  "severity": "string",  // Optional: "minor", "major", "critical" (default: "minor")
  "notes": "string",  // Optional: Additional notes
  "title": "string",  // Optional: Title or summary
  "rootCause": "string",  // Optional: Root cause analysis
  "prevention": "string"  // Optional: Prevention strategy
}
```

### DELETE /api/failures/<failure_id>
Deletes a failure record.

## Common Patterns

### Task Creation Flow
1. GET templates by category
2. User selects template
3. POST to create task with template_id
4. Schedule with scheduled_at

### Task Completion Flow
1. User completes task in app
2. POST to /complete endpoint
3. Optionally POST to task-logs for detailed logging

### Error Handling
- `400`: Invalid data
- `401`: Unauthorized
- `404`: Resource not found
- `409`: Conflict (e.g., duplicate key)

### Data Types
- `template_id`, `task_id`: UUID strings
- `status`: "pending", "completed", "cancelled"
- `params`, `metadata`: JSON objects
- `scheduled_at`, `completed_at`: ISO 8601 datetime strings