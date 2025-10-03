# JWT Authentication Implementation

## Overview
This backend now uses JWT (JSON Web Tokens) for authentication. All task endpoints are protected and require a valid JWT token.

## How It Works

### 1. Login and Get JWT Token
**Endpoint:** `POST /api/auth/login` or `POST /login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "user": "John Doe",
    "email": "user@example.com"
  }
}
```

The token expires after 24 hours.

### 2. Use JWT Token in Protected Requests
All task endpoints now require authentication. Include the JWT token in the `Authorization` header:

**Header:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Protected Endpoints

All task endpoints now require JWT authentication:

- `GET /api/task/get` - Get all tasks
- `GET /api/task/get/<task_id>` - Get specific task
- `POST /api/task/create` - Create new task
- `PUT /api/task/update/<task_id>` - Update task
- `DELETE /api/task/delete/<task_id>` - Delete task

### Example Request with JWT Token

**JavaScript/Fetch:**
```javascript
const token = 'your-jwt-token-here';

fetch('http://localhost:5000/api/task/get', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

**Python/Requests:**
```python
import requests

token = 'your-jwt-token-here'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get('http://localhost:5000/api/task/get', headers=headers)
print(response.json())
```

**cURL:**
```bash
curl -X GET http://localhost:5000/api/task/get \
  -H "Authorization: Bearer your-jwt-token-here" \
  -H "Content-Type: application/json"
```

## Error Responses

### Missing Token (401)
```json
{
  "error": "Authentication token is missing"
}
```

### Invalid Token Format (401)
```json
{
  "error": "Invalid token format. Use: Bearer <token>"
}
```

### Expired or Invalid Token (401)
```json
{
  "error": "Invalid or expired token"
}
```

## JWT Token Contents

The JWT token contains the following information:
- `user_id`: User's ID
- `email`: User's email
- `name`: User's name
- `exp`: Expiration timestamp (24 hours from issuance)
- `iat`: Issued at timestamp

## Configuration

### Secret Key
The JWT secret key can be configured via environment variable:

```bash
# Windows PowerShell
$env:JWT_SECRET_KEY="your-secret-key-here"

# Windows CMD
set JWT_SECRET_KEY=your-secret-key-here

# Linux/Mac
export JWT_SECRET_KEY=your-secret-key-here
```

**Important:** In production, always use a strong, randomly generated secret key and set it via environment variable!

## Security Notes

1. **HTTPS Only in Production:** Always use HTTPS in production to protect tokens in transit
2. **Secure Storage:** Store JWT tokens securely on the client side (avoid localStorage for sensitive apps)
3. **Token Expiration:** Tokens expire after 24 hours. Implement token refresh if needed
4. **Secret Key:** Use a strong, random secret key in production (minimum 32 characters)

## Files Modified/Created

- `services/auth_service.py` - Added JWT generation and verification functions
- `controllers/auth_controller.py` - Updated login to return JWT token
- `middleware/auth_middleware.py` - Created JWT authentication decorator
- `routes/task_routes.py` - Added JWT protection to all task endpoints
- `app.py` - Added SECRET_KEY configuration
