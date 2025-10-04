# IAM Backend API - Advanced Features

## Overview
This document covers Achievements, Goals, Bot Rules, and Chat IA endpoints. These provide gamification, goal tracking, automation, and AI chat functionality. All endpoints require JWT authentication.

## Achievements

### GET /api/achievements
Retrieves user's achievements.

**Endpoint:** `GET /api/achievements`

**Success Response (200):**
```json
[
  {
    "id": "achievement-uuid",
    "user_id": "user-uuid",
    "key": "first_meditation",
    "title": "Primera Meditación",
    "description": "Completaste tu primera sesión de meditación",
    "unlocked_at": "2025-10-01T10:00:00Z",
    "metadata": {
      "xp_gained": 50
    }
  }
]
```

**Frontend Integration Notes:**
- Display achievements in user profile
- Show unlock animations
- Track progress towards new achievements

### POST /api/achievements
Grants a new achievement to the user.

**Request Body:**
```json
{
  "key": "string",  // Required: Unique achievement key
  "title": "string",  // Required: Display title
  "description": "string",  // Required: Description
  "metadata": {}  // Optional: Additional data
}
```

**Success Response (201):** Created achievement object

**Error Responses:**
- `409 Conflict`: Achievement already exists for user

### DELETE /api/achievements/<achievement_id>
Removes an achievement.

**Success Response (200):**
```json
{
  "message": "Achievement removed successfully"
}
```

## Goals

### GET /api/goals
Retrieves user's goals.

**Query Parameters:**
- `is_active`: true/false (optional)

**Success Response (200):**
```json
[
  {
    "id": "goal-uuid",
    "user_id": "user-uuid",
    "title": "Meditar 30 días seguidos",
    "description": "Completar una sesión de meditación cada día durante 30 días",
    "metric_key": "meditation_streak",
    "target_value": 30,
    "current_value": 5,
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "is_active": true,
    "created_at": "2025-10-01T00:00:00Z",
    "updated_at": "2025-10-01T00:00:00Z"
  }
]
```

### GET /api/goals/<goal_id>
Retrieves a specific goal.

### POST /api/goals
Creates a new goal.

**Request Body:**
```json
{
  "title": "string",  // Required
  "description": "string",  // Optional
  "metric_key": "string",  // Required: e.g., "meditation_streak"
  "target_value": "number",  // Required
  "start_date": "string",  // Required: YYYY-MM-DD
  "end_date": "string",  // Required: YYYY-MM-DD
  "is_active": true  // Optional, default true
}
```

### PUT /api/goals/<goal_id>
Updates a goal.

**Request Body:** Same as POST, all fields optional

### DELETE /api/goals/<goal_id>
Deletes a goal.

## Bot Rules

### GET /api/bot-rules
Retrieves bot rules.

**Query Parameters:**
- `active_only`: true/false (optional)

**Success Response (200):**
```json
[
  {
    "id": "rule-uuid",
    "user_id": "user-uuid",
    "name": "Auto-crear meditación matutina",
    "condition": {
      "time": "08:00",
      "days": ["monday", "wednesday", "friday"]
    },
    "action": {
      "type": "create_task",
      "template_key": "meditation_10",
      "category": "mind"
    },
    "priority": 10,
    "active": true,
    "created_at": "2025-10-01T00:00:00Z"
  }
]
```

### GET /api/bot-rules/<rule_id>
Retrieves a specific rule.

### POST /api/bot-rules
Creates a new bot rule.

**Request Body:**
```json
{
  "name": "string",  // Required
  "condition": {},  // Required: JSON condition object
  "action": {},  // Required: JSON action object
  "priority": "number",  // Optional: Default 0
  "active": true  // Optional: Default true
}
```

**Condition Examples:**
```json
{
  "time": "08:00",
  "days": ["monday", "wednesday", "friday"]
}
```

**Action Examples:**
```json
{
  "type": "create_task",
  "template_key": "meditation_10",
  "category": "mind"
}
```

### PUT /api/bot-rules/<rule_id>
Updates a bot rule.

### DELETE /api/bot-rules/<rule_id>
Deletes a bot rule.

## Chat IA

### Sessions

#### GET /api/chat/sessions
Retrieves chat sessions.

**Success Response (200):**
```json
[
  {
    "id": "session-uuid",
    "user_id": "user-uuid",
    "title": "Consulta sobre meditación",
    "model": "gpt-5",
    "system_prompt": "Eres un asistente experto en mindfulness",
    "created_at": "2025-10-01T00:00:00Z",
    "updated_at": "2025-10-01T00:00:00Z"
  }
]
```

#### GET /api/chat/sessions/<session_id>
Retrieves a specific session.

#### POST /api/chat/sessions
Creates a new chat session.

**Request Body:**
```json
{
  "title": "string",  // Required
  "model": "string",  // Optional: Default model
  "system_prompt": "string"  // Optional
}
```

#### PUT /api/chat/sessions/<session_id>
Updates a session.

**Request Body:**
```json
{
  "title": "string",  // Optional
  "model": "string",  // Optional
  "system_prompt": "string"  // Optional
}
```

#### DELETE /api/chat/sessions/<session_id>
Deletes a session.

### Messages

#### GET /api/chat/sessions/<session_id>/messages
Retrieves messages for a session.

**Success Response (200):**
```json
[
  {
    "id": "message-uuid",
    "session_id": "session-uuid",
    "role": "user",
    "content": "¿Cómo puedo mejorar mi práctica de meditación?",
    "content_json": null,
    "created_at": "2025-10-01T00:00:00Z"
  },
  {
    "id": "message-uuid-2",
    "session_id": "session-uuid",
    "role": "assistant",
    "content": "Para mejorar tu práctica de meditación...",
    "content_json": null,
    "created_at": "2025-10-01T00:00:01Z"
  }
]
```

#### POST /api/chat/sessions/<session_id>/messages
Sends a message to the chat session.

**Request Body:**
```json
{
  "role": "user",  // Required: "user" or "assistant"
  "content": "string",  // Required: Message content
  "content_json": {}  // Optional: JSON content
}
```

**Note:** This may trigger AI response generation on the backend.

#### DELETE /api/chat/messages/<message_id>
Deletes a specific message.

## Integration Patterns

### Achievement System
- Trigger POST when user completes milestones
- Display unlocked achievements with animations
- Use metadata for XP, badges, etc.

### Goal Tracking
- Update current_value via PUT as user progresses
- Show progress bars in UI
- Alert when goals are completed or expired

### Bot Rules
- Allow users to create automation rules
- Validate condition/action JSON on frontend
- Test rules before activation

### Chat Integration
- Maintain session state in frontend
- Stream messages for real-time feel
- Handle different message types (text, JSON)

### Error Handling
- `400`: Invalid JSON structure
- `401`: Unauthorized
- `404`: Resource not found
- `409`: Duplicate or conflict

### Data Types
- `condition`, `action`, `metadata`, `content_json`: JSON objects
- `role`: "user" or "assistant"
- `is_active`, `active`: boolean
- Dates: ISO 8601 strings