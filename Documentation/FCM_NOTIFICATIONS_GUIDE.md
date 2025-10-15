# FCM Push Notifications Implementation Guide

## Overview

This backend now supports Firebase Cloud Messaging (FCM) for sending push notifications to Android, iOS, and Web applications. The system includes token management, notification delivery, and automatic cleanup of invalid tokens.

## Architecture

```
┌─────────────────┐
│  Mobile App     │
│  (Android/iOS)  │
└────────┬────────┘
         │ FCM Token
         ↓
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  API Endpoint   │─────→│  Controller      │─────→│  Service Layer  │
│  /register-token│      │  notification_   │      │  notification_  │
└─────────────────┘      │  controller.py   │      │  service.py     │
                         └──────────────────┘      └────────┬────────┘
                                                             │
                         ┌──────────────────┐              │
                         │  Firebase Client │←─────────────┘
                         │  firebase_client │
                         │     .py          │
                         └────────┬─────────┘
                                  │
                                  ↓
                         ┌──────────────────┐
                         │  Firebase Cloud  │
                         │   Messaging      │
                         └──────────────────┘
                                  │
                                  ↓
                         ┌──────────────────┐
                         │  Device          │
                         │  (Push Notif)    │
                         └──────────────────┘
```

## Database Schema

The system uses the `device_tokens` table:

```sql
CREATE TABLE IF NOT EXISTS public.device_tokens (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES public.users_iam(id) ON DELETE CASCADE,
  token       TEXT NOT NULL UNIQUE,
  platform    TEXT NOT NULL DEFAULT 'android',
  device_info JSONB DEFAULT '{}'::jsonb,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Indexes:**
- `idx_device_tokens_user_id` - Fast user token lookups
- `idx_device_tokens_token` - Token uniqueness and search
- `idx_device_tokens_created_at` - Chronological queries

## Setup Instructions

### 1. Install Dependencies

```bash
pip install firebase-admin==6.5.0
```

Or update from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Firebase Configuration

#### Get Firebase Service Account Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Project Settings** → **Service Accounts**
4. Click **Generate New Private Key**
5. Download the JSON file

#### Configure Environment Variables

Add to your `.env` file:

```bash
# Option 1: File path (local development)
FIREBASE_SERVICE_ACCOUNT=/path/to/firebase-service-account.json

# Option 2: JSON string (production/Render)
FIREBASE_SERVICE_ACCOUNT='{"type":"service_account","project_id":"your-project-id",...}'
```

### 3. Apply Database Schema

Run the SQL schema in your Supabase SQL Editor:

```bash
psql -h your-host -U postgres -d your-db -f db_schemas/token_notification_FCM.sql
```

Or execute directly in Supabase dashboard.

### 4. Restart Your Application

```bash
python app.py
```

## API Endpoints

### 1. Register Device Token

Register or update a device's FCM token.

**Endpoint:** `POST /api/notification/register-token`

**Authentication:** Required (JWT Bearer token)

**Request Body:**
```json
{
  "token": "dQw4w9WgXcQ:APA91bHun4MXIMpMX...",
  "platform": "android",
  "device_info": {
    "model": "Pixel 6",
    "os_version": "Android 13",
    "app_version": "1.0.0"
  }
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Device token registered successfully",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "789e0123-e45b-67c8-d901-234567890abc",
    "token": "dQw4w9WgXcQ:APA91bHun4MXIMpMX...",
    "platform": "android",
    "device_info": {
      "model": "Pixel 6",
      "os_version": "Android 13",
      "app_version": "1.0.0"
    },
    "is_active": true,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/notification/register-token \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "dQw4w9WgXcQ:APA91bHun4MXIMpMX...",
    "platform": "android",
    "device_info": {
      "model": "Pixel 6",
      "os_version": "Android 13"
    }
  }'
```

---

### 2. Get User Tokens

Retrieve all active tokens for the authenticated user.

**Endpoint:** `GET /api/notification/tokens`

**Authentication:** Required (JWT Bearer token)

**Response (200):**
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "token": "dQw4w9WgXcQ:APA91bHun4MXIMpMX...",
      "platform": "android",
      "device_info": {"model": "Pixel 6"},
      "is_active": true,
      "created_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": "456e7890-b12c-34d5-e678-901234567890",
      "token": "eRx5x0XhYdR:BQB02cIvo5NYJNqNY...",
      "platform": "ios",
      "device_info": {"model": "iPhone 13"},
      "is_active": true,
      "created_at": "2025-01-14T15:20:00Z"
    }
  ]
}
```

---

### 3. Remove Device Token

Deactivate or permanently delete a device token.

**Endpoint:** `POST /api/notification/remove-token`

**Authentication:** Required (JWT Bearer token)

**Request Body:**
```json
{
  "token": "dQw4w9WgXcQ:APA91bHun4MXIMpMX...",
  "hard_delete": false
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Device token deactivated successfully",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "is_active": false
  }
}
```

---

### 4. Send Push Notification

Send a notification to all active devices of a specific user.

**Endpoint:** `POST /api/notification/send`

**Authentication:** Required (JWT Bearer token)

**Request Body:**
```json
{
  "user_id": "789e0123-e45b-67c8-d901-234567890abc",
  "title": "Task Reminder",
  "body": "Don't forget to complete your daily tasks!",
  "data": {
    "task_id": "456",
    "type": "reminder",
    "action": "open_task"
  }
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Notification sent",
  "data": {
    "status": "completed",
    "success_count": 2,
    "failure_count": 0,
    "results": [
      {
        "token": "dQw4w9WgXcQ:APA91bHun4MXIMpMX...",
        "status": "sent",
        "message_id": "projects/myproject/messages/0:1234567890"
      },
      {
        "token": "eRx5x0XhYdR:BQB02cIvo5NYJNqNY...",
        "status": "sent",
        "message_id": "projects/myproject/messages/0:9876543210"
      }
    ]
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/notification/send \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "789e0123-e45b-67c8-d901-234567890abc",
    "title": "Task Reminder",
    "body": "Complete your tasks!",
    "data": {
      "task_id": "456",
      "type": "reminder"
    }
  }'
```

---

### 5. Send Bulk Notification

Send a notification to multiple users at once.

**Endpoint:** `POST /api/notification/send-bulk`

**Authentication:** Required (JWT Bearer token)

**Request Body:**
```json
{
  "user_ids": [
    "789e0123-e45b-67c8-d901-234567890abc",
    "012e3456-f78g-90h1-i234-567890123456"
  ],
  "title": "System Announcement",
  "body": "New features are now available!",
  "data": {
    "type": "announcement",
    "version": "2.0"
  }
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Bulk notification sent",
  "data": {
    "status": "completed",
    "total_users": 2,
    "total_success": 3,
    "total_failure": 1,
    "user_results": [...]
  }
}
```

---

### 6. List All Device Tokens (Admin)

List all device tokens with optional filters.

**Endpoint:** `GET /api/notification/tokens/all`

**Authentication:** Required (JWT Bearer token)

**Query Parameters:**
- `user_id` (optional) - Filter by user ID
- `platform` (optional) - Filter by platform (android/ios/web)
- `is_active` (optional) - Filter by active status (true/false)

**Example:**
```
GET /api/notification/tokens/all?platform=android&is_active=true
```

**Response (200):**
```json
{
  "status": "success",
  "count": 15,
  "data": [...]
}
```

## Client Integration Examples

### Android (Kotlin)

```kotlin
// Get FCM token
FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val token = task.result
        registerToken(token)
    }
}

// Register token with backend
fun registerToken(fcmToken: String) {
    val client = OkHttpClient()
    val json = JSONObject().apply {
        put("token", fcmToken)
        put("platform", "android")
        put("device_info", JSONObject().apply {
            put("model", Build.MODEL)
            put("os_version", "Android ${Build.VERSION.RELEASE}")
            put("app_version", BuildConfig.VERSION_NAME)
        })
    }
    
    val request = Request.Builder()
        .url("https://your-api.com/api/notification/register-token")
        .addHeader("Authorization", "Bearer $jwtToken")
        .post(json.toString().toRequestBody("application/json".toMediaType()))
        .build()
    
    client.newCall(request).enqueue(object : Callback {
        override fun onResponse(call: Call, response: Response) {
            // Token registered successfully
        }
        override fun onFailure(call: Call, e: IOException) {
            // Handle error
        }
    })
}
```

### iOS (Swift)

```swift
import Firebase

// Get FCM token
Messaging.messaging().token { token, error in
    if let error = error {
        print("Error fetching FCM token: \(error)")
    } else if let token = token {
        registerToken(token: token)
    }
}

// Register token with backend
func registerToken(token: String) {
    let url = URL(string: "https://your-api.com/api/notification/register-token")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("Bearer \(jwtToken)", forHTTPHeaderField: "Authorization")
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body: [String: Any] = [
        "token": token,
        "platform": "ios",
        "device_info": [
            "model": UIDevice.current.model,
            "os_version": "iOS \(UIDevice.current.systemVersion)",
            "app_version": Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
        ]
    ]
    
    request.httpBody = try? JSONSerialization.data(withJSONObject: body)
    
    URLSession.shared.dataTask(with: request) { data, response, error in
        // Handle response
    }.resume()
}
```

### React Native / JavaScript

```javascript
import messaging from '@react-native-firebase/messaging';

// Request permission and get token
async function registerForPushNotifications() {
  const authStatus = await messaging().requestPermission();
  const enabled =
    authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
    authStatus === messaging.AuthorizationStatus.PROVISIONAL;

  if (enabled) {
    const fcmToken = await messaging().getToken();
    await registerToken(fcmToken);
  }
}

// Register token with backend
async function registerToken(fcmToken) {
  const response = await fetch('https://your-api.com/api/notification/register-token', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${jwtToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      token: fcmToken,
      platform: Platform.OS, // 'android' or 'ios'
      device_info: {
        model: DeviceInfo.getModel(),
        os_version: DeviceInfo.getSystemVersion(),
        app_version: DeviceInfo.getVersion(),
      },
    }),
  });
  
  const data = await response.json();
  console.log('Token registered:', data);
}
```

## Backend Usage Examples

### Send notification when a task is completed

```python
from services.notification_service import send_notification_to_user

def complete_task(task_id, user_id):
    # ... task completion logic ...
    
    # Send notification
    send_notification_to_user(
        user_id=user_id,
        title="Task Completed! 🎉",
        body="Great job! You've earned 50 XP.",
        data={
            "task_id": task_id,
            "type": "task_completed",
            "xp_earned": 50
        }
    )
```

### Send reminder notifications

```python
from services.notification_service import send_notification_to_multiple_users

def send_daily_reminders():
    # Get users who need reminders
    users_to_remind = get_users_with_pending_tasks()
    user_ids = [user['id'] for user in users_to_remind]
    
    # Send bulk notification
    send_notification_to_multiple_users(
        user_ids=user_ids,
        title="Daily Reminder",
        body="You have pending tasks to complete!",
        data={
            "type": "daily_reminder"
        }
    )
```

## Error Handling

The system automatically handles invalid tokens:

1. **Invalid/Unregistered Tokens**: Automatically deactivated
2. **Expired Tokens**: Marked as inactive
3. **Network Errors**: Logged and reported in response

## Security Considerations

1. **JWT Authentication**: All endpoints require valid JWT tokens
2. **User Isolation**: Users can only register/view their own tokens
3. **Token Validation**: FCM validates tokens before sending
4. **Environment Variables**: Sensitive Firebase credentials in `.env`
5. **HTTPS Only**: Use HTTPS in production

## Monitoring & Debugging

### Check Firebase Admin Initialization

```python
from lib.firebase_client import _firebase_app

if _firebase_app:
    print("✅ Firebase initialized")
else:
    print("❌ Firebase not initialized - check FIREBASE_SERVICE_ACCOUNT")
```

### View Logs

```bash
# Check application logs for Firebase errors
tail -f logs/app.log | grep -i firebase
```

### Test Token Registration

```bash
curl -X POST http://localhost:5000/api/notification/register-token \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token":"test-token-123","platform":"android"}'
```

## Troubleshooting

### Firebase Not Initialized

**Problem:** `Firebase Admin SDK not initialized`

**Solution:**
1. Check `FIREBASE_SERVICE_ACCOUNT` in `.env`
2. Verify JSON format is valid
3. Ensure service account has FCM permissions

### Token Registration Fails

**Problem:** Token not saving to database

**Solution:**
1. Verify `device_tokens` table exists
2. Check Supabase connection
3. Ensure user_id is valid UUID

### Notifications Not Received

**Problem:** Messages sent but not received

**Solution:**
1. Verify FCM token is valid and current
2. Check device has internet connection
3. Ensure app has notification permissions
4. Check Firebase Console for delivery status

## Production Deployment

### Render.com

Add environment variable in Render dashboard:

```
FIREBASE_SERVICE_ACCOUNT={"type":"service_account","project_id":"your-project",...}
```

### Heroku

```bash
heroku config:set FIREBASE_SERVICE_ACCOUNT='{"type":"service_account",...}'
```

### Docker

```dockerfile
ENV FIREBASE_SERVICE_ACCOUNT=/app/firebase-service-account.json
COPY firebase-service-account.json /app/
```

## Performance Tips

1. **Batch Notifications**: Use bulk endpoint for multiple users
2. **Async Processing**: Consider Celery for large notification batches
3. **Token Cleanup**: Periodically remove old inactive tokens
4. **Rate Limiting**: FCM has rate limits; implement queuing for high volume

## Additional Resources

- [Firebase Cloud Messaging Documentation](https://firebase.google.com/docs/cloud-messaging)
- [Firebase Admin Python SDK](https://firebase.google.com/docs/admin/setup)
- [FCM HTTP v1 API](https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages)

## Support

For issues or questions:
1. Check Firebase Console logs
2. Review application logs
3. Verify environment configuration
4. Test with cURL examples above
