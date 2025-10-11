# IAM Backend API - Authentication and User Profile

## Overview
This document details the Authentication and User Profile endpoints of the IAM Backend API. These endpoints handle user login, token management, and user profile CRUD operations. All endpoints except login require JWT authentication.

## Authentication

### POST /login
Authenticates a user and returns a JWT token for subsequent API calls.

**Endpoint:** `POST /login`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "string",  // Required: User's email address
  "password": "string"  // Required: User's password
}
```

**Success Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  // JWT token for authentication
  "user": {
    "id": "uuid-or-user-id",
    "email": "user@example.com",
    "created_at": "2025-10-01T00:00:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid email or password format
- `401 Unauthorized`: Invalid credentials
- `500 Internal Server Error`: Server error

**Frontend Integration Notes:**
- Store the token securely (localStorage, secure cookies, or state management)
- Include token in `Authorization: Bearer <token>` header for all subsequent requests
- Handle token expiration (implement refresh logic if needed)
- Validate token on app startup

### GET /getusers
**Note:** This endpoint is for testing purposes only. Returns all users in the system.

**Endpoint:** `GET /getusers`

**Headers:** None required

**Response (200):**
```json
[
  {
    "id": "user-id",
    "email": "user@example.com",
    "created_at": "2025-10-01T00:00:00Z"
  }
]
```

**Frontend Integration Notes:**
- This endpoint should not be used in production frontend code
- Use only for development/testing user management

## User Profile

### GET /api/profile
Retrieves the authenticated user's profile information.

**Endpoint:** `GET /api/profile`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Success Response (200):**
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "timezone": "America/Mexico_City",
  "birth_date": "1990-01-15",
  "gender": "male",  // "male", "female", "other", or null
  "weight_kg": 75.5,
  "height_cm": 175,
  "preferred_language": "es",  // "es", "en", etc.
  "hours_available_to_week": 40,
  "work_schedules": "9:00-17:00",
  "current_status": "active",
  "hours_used_to_week": 0,
  "time_dead": 0,  // Time dead or unproductive time
  "day_work": "L,M,M,J,V",  // Work days (D,L,M,M,J,V,S format)
  "created_at": "2025-10-01T00:00:00Z",
  "updated_at": "2025-10-01T00:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Profile not found (user hasn't created one yet)

**Frontend Integration Notes:**
- Call this on app load to get user preferences
- Use timezone for date/time display
- Handle 404 gracefully (prompt user to create profile)

### POST /api/profile
Creates a new profile for the authenticated user.

**Endpoint:** `POST /api/profile`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "timezone": "string",  // Required: IANA timezone identifier (e.g., "America/Mexico_City")
  "birth_date": "string",  // Optional: ISO 8601 date (YYYY-MM-DD)
  "gender": "string",  // Optional: "male", "female", "other"
  "weight_kg": "number",  // Optional: Weight in kilograms
  "height_cm": "number",  // Optional: Height in centimeters
  "preferred_language": "string",  // Optional: Language code (e.g., "es", "en")
  "hours_available_to_week": "number",  // Optional: Available hours per week
  "work_schedules": "string",  // Optional: Work schedule (e.g., "9:00-17:00")
  "current_status": "string",  // Optional: Current status (e.g., "active", "busy")
  "hours_used_to_week": "number",  // Optional: Hours used in the week
  "time_dead": "number",  // Optional: Time dead or unproductive time
  "day_work": "string"  // Optional: Work days (D,L,M,M,J,V,S format)
}
```

**Success Response (201):**
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "timezone": "America/Mexico_City",
  "birth_date": "1990-01-15",
  "gender": "male",
  "weight_kg": 75.5,
  "height_cm": 175,
  "preferred_language": "es",
  "hours_available_to_week": 40,
  "work_schedules": "9:00-17:00",
  "current_status": "active",
  "hours_used_to_week": 0,
  "time_dead": 0,
  "day_work": "L,M,M,J,V",
  "created_at": "2025-10-02T00:00:00Z",
  "updated_at": "2025-10-02T00:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data format or missing required fields
- `401 Unauthorized`: Invalid token
- `409 Conflict`: Profile already exists for this user

**Frontend Integration Notes:**
- Required fields: only timezone
- Validate input on frontend before sending
- Redirect to profile setup flow if creation succeeds

### PUT /api/profile
Updates the authenticated user's profile information.

**Endpoint:** `PUT /api/profile`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "timezone": "string",  // Optional: IANA timezone identifier
  "birth_date": "string",  // Optional: ISO 8601 date
  "gender": "string",  // Optional: "male", "female", "other"
  "weight_kg": "number",  // Optional: Weight in kilograms
  "height_cm": "number",  // Optional: Height in centimeters
  "preferred_language": "string",  // Optional: Language code
  "hours_available_to_week": "number",  // Optional: Available hours per week
  "work_schedules": "string",  // Optional: Work schedule
  "current_status": "string",  // Optional: Current status
  "hours_used_to_week": "number",  // Optional: Hours used in the week
  "time_dead": "number",  // Optional: Time dead or unproductive time
  "day_work": "string"  // Optional: Work days (D,L,M,M,J,V,S format)
}
```

**Success Response (200):**
```json
{
  "id": "profile-uuid",
  "user_id": "user-uuid",
  "timezone": "America/New_York",
  "birth_date": "1990-01-15",
  "gender": "male",
  "weight_kg": 75.5,
  "height_cm": 175,
  "preferred_language": "en",
  "hours_available_to_week": 45,
  "work_schedules": "10:00-18:00",
  "current_status": "busy",
  "hours_used_to_week": 30.5,
  "time_dead": 5.0,
  "day_work": "L,M,M,J,V,S",
  "created_at": "2025-10-01T00:00:00Z",
  "updated_at": "2025-10-02T00:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data format
- `401 Unauthorized`: Invalid token
- `404 Not Found`: Profile not found

**Frontend Integration Notes:**
- Partial updates allowed - only send changed fields
- Update local state after successful update
- Show success/error messages to user

### DELETE /api/profile
Deletes the authenticated user's profile.

**Endpoint:** `DELETE /api/profile`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Success Response (200):**
```json
{
  "message": "Profile deleted successfully"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid token
- `404 Not Found`: Profile not found

**Frontend Integration Notes:**
- Use with caution - confirm deletion with user
- Clear local profile data after deletion
- May require re-authentication or profile recreation

## Common Error Handling
All endpoints may return these errors:
- `401 Unauthorized`: Token missing, invalid, or expired
- `500 Internal Server Error`: Unexpected server error

**Frontend Error Handling Strategy:**
- Check for 401 errors and redirect to login
- Display user-friendly error messages
- Implement retry logic for network errors
- Log errors for debugging

## Data Types and Validation
- **timezone**: Valid IANA timezone identifier
- **birth_date**: ISO 8601 date format (YYYY-MM-DD)
- **gender**: Enum: "male", "female", "other", or null
- **weight_kg**: Number, positive
- **height_cm**: Number, positive
- **preferred_language**: ISO 639-1 language code
- **hours_available_to_week**: Number, positive, hours available per week
- **work_schedules**: String, work schedule format (e.g., "9:00-17:00")
- **current_status**: String, user's current status
- **hours_used_to_week**: Number, hours used in the current week
- **time_dead**: Number, time dead or unproductive time tracked
- **day_work**: String, work days in format D,L,M,M,J,V,S (D=Domingo, L=Lunes, M=Martes, M=Miércoles, J=Jueves, V=Viernes, S=Sábado)

## Integration Flow Example
1. User logs in → Store token
2. Check if profile exists → GET /api/profile
3. If 404, prompt user to create profile → POST /api/profile
4. Update profile as needed → PUT /api/profile
5. Use profile data throughout the app