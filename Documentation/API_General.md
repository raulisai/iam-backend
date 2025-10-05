# IAM Backend API - General Information

## Overview
This document provides general information about the IAM Backend API, including HTTP status codes, typical workflows, database structure, important notes, testing instructions, and environment variables.

## HTTP Status Codes

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data or parameters
- `401 Unauthorized` - Missing, invalid, or expired JWT token
- `403 Forbidden` - User doesn't have permission for the resource
- `404 Not Found` - Requested resource doesn't exist
- `409 Conflict` - Resource conflict (e.g., duplicate key, already exists)
- `500 Internal Server Error` - Unexpected server error

## Typical Workflow

### 1. Authentication
```bash
# Login to get JWT token
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Profile Setup
```bash
# Create or update user profile
curl -X POST http://localhost:5000/api/profile \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"timezone": "America/Mexico_City", "preferred_language": "es"}'
```

### 3. Task Management
```bash
# Get available task templates
curl -X GET http://localhost:5000/api/task-templates/category/mind \
  -H "Authorization: Bearer <token>"

# Create a task
curl -X POST http://localhost:5000/api/tasks/mind \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "<template-uuid>",
    "created_by": "user",
    "scheduled_at": "2025-10-01T10:00:00Z"
  }'

# Complete the task
curl -X POST http://localhost:5000/api/tasks/mind/<task-id>/complete \
  -H "Authorization: Bearer <token>"
```

### 4. Achievement Tracking
```bash
# Check user achievements
curl -X GET http://localhost:5000/api/achievements \
  -H "Authorization: Bearer <token>"
```

## Database Structure

### Core Tables

#### users_iam
- User authentication data
- Primary key: user ID (may not be UUID)

#### profiles
- User profile information
- Foreign key: user_id
- Fields: timezone, birth_date, gender, weight_kg, height_cm, preferred_language

#### task_templates
- Predefined task templates
- Fields: key (unique), name, category (mind/body), estimated_minutes, difficulty, reward_xp, descr, default_params (JSONB)

#### tasks_mind
- Mind-related tasks
- Foreign keys: template_id, user_id
- Fields: status, scheduled_at, completed_at, params (JSONB)

#### tasks_body
- Body-related tasks
- Same structure as tasks_mind

#### task_logs
- Task completion logs
- Foreign keys: task_table, task_id, user_id
- Fields: action, metadata (JSONB)

#### achievements
- User achievements/unlocks
- Foreign keys: user_id
- Fields: key, title, description, unlocked_at, metadata (JSONB)

#### failures
- Task failure records
- Foreign keys: task_table, task_id, user_id
- Fields: reason, severity, notes, title, rootCause, prevention, created_at

#### goals
- User goals/targets
- Foreign keys: user_id
- Fields: title, description, metric_key, target_value, current_value, start_date, end_date, is_active

#### bot_rules
- Automated bot rules
- Foreign keys: user_id
- Fields: name, condition (JSONB), action (JSONB), priority, active

#### chat_ia_sessions
- Chat AI conversation sessions
- Foreign keys: user_id
- Fields: title, model, system_prompt

#### chat_ia_messages
- Individual chat messages
- Foreign keys: session_id
- Fields: role (user/assistant), content, content_json (JSONB)

## Important Notes

### Security
- **JWT Authentication**: All endpoints except `/login` and `/getusers` require a valid JWT token in the `Authorization: Bearer <token>` header
- **Authorization**: Users can only access their own resources
- **Token Expiration**: Implement token refresh logic in frontend if tokens expire

### Data Validation
- Required fields are validated on the backend
- JSONB fields (`params`, `condition`, `action`, `metadata`, `content_json`) allow flexible data structures
- Input sanitization is handled by controllers

### Data Formats
- **Timestamps**: All dates/times in ISO 8601 format (UTC)
- **IDs**: Most IDs are UUIDs, except `users_iam` which may use different format
- **Languages**: Use ISO 639-1 codes (e.g., "es", "en")
- **Timezones**: Use IANA timezone identifiers (e.g., "America/Mexico_City")

### JSONB Fields Usage
- `params`: Task-specific parameters (e.g., duration, music settings)
- `condition`: Bot rule trigger conditions (e.g., time, days)
- `action`: Bot rule actions (e.g., create_task with template_key)
- `metadata`: Additional context (e.g., XP gained, notes)
- `content_json`: Structured message content in chat

### Performance Considerations
- Cache task templates on frontend
- Use pagination for large result sets (not currently implemented)
- Batch operations where possible

### Error Handling
- Always check HTTP status codes
- Parse error responses for user-friendly messages
- Implement retry logic for network failures
- Handle 401 errors by redirecting to login

## Testing with Swagger

The API includes interactive Swagger documentation at:
```
http://localhost:5000/apidocs/
```

Features:
- Try out API endpoints directly in browser
- View request/response schemas
- Test authentication
- Generate API client code

## Environment Variables

Required environment variables for the backend:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here

# Database Configuration (Supabase)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Optional: Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True
```

### Security Notes
- Never commit `JWT_SECRET_KEY` to version control
- Use strong, random keys for JWT signing
- Rotate keys periodically
- Store secrets securely (environment variables, secret managers)

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run the app: `python app.py`
5. Access API at `http://localhost:5000`
6. View Swagger docs at `http://localhost:5000/apidocs/`

## API Versioning

Current API version: v1
- Base path: `/api/`
- No versioning in URL (v1 assumed)
- Breaking changes will be communicated in advance

## Support

For API issues or questions:
- Check Swagger documentation first
- Review this documentation
- Test endpoints with curl/Postman
- Check server logs for errors