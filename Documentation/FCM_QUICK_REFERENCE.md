# FCM Notifications - Quick Reference

## Quick Setup Checklist

- [ ] Install `firebase-admin` package
- [ ] Add `FIREBASE_SERVICE_ACCOUNT` to `.env`
- [ ] Apply database schema (token_notification_FCM.sql)
- [ ] Register routes in `app.py`
- [ ] Restart application

## Essential Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/notification/register-token` | POST | ✅ | Register FCM token |
| `/api/notification/tokens` | GET | ✅ | Get user's tokens |
| `/api/notification/send` | POST | ✅ | Send to one user |
| `/api/notification/send-bulk` | POST | ✅ | Send to many users |

## Quick Test

### 1. Register Token
```bash
curl -X POST http://localhost:5000/api/notification/register-token \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  -d '{"token":"test-fcm-token","platform":"android"}'
```

### 2. Send Notification
```bash
curl -X POST http://localhost:5000/api/notification/send \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":"USER_UUID",
    "title":"Test",
    "body":"Hello!",
    "data":{"test":true}
  }'
```

## Environment Variables

```bash
# In .env file
FIREBASE_SERVICE_ACCOUNT=/path/to/firebase-service-account.json
```

Or for production (Render/Heroku):
```bash
FIREBASE_SERVICE_ACCOUNT='{"type":"service_account","project_id":"..."}'
```

## Common Issues

| Problem | Solution |
|---------|----------|
| "Firebase not initialized" | Check `FIREBASE_SERVICE_ACCOUNT` in `.env` |
| "Token required" | Include `token` field in request body |
| "Invalid token format" | Use `Bearer YOUR_TOKEN` in Authorization header |
| "No tokens found" | User hasn't registered any device tokens yet |

## Code Snippets

### Python: Send Notification
```python
from services.notification_service import send_notification_to_user

send_notification_to_user(
    user_id="uuid-here",
    title="Task Complete!",
    body="You earned 50 XP",
    data={"task_id": "123", "type": "completion"}
)
```

### Android: Register Token
```kotlin
FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
    val token = task.result
    // Send token to your backend /api/notification/register-token
}
```

### iOS: Register Token
```swift
Messaging.messaging().token { token, error in
    // Send token to your backend /api/notification/register-token
}
```

## Database Query

```sql
-- View all active tokens
SELECT user_id, token, platform, is_active, created_at 
FROM device_tokens 
WHERE is_active = true;

-- Count tokens per user
SELECT user_id, COUNT(*) as token_count 
FROM device_tokens 
WHERE is_active = true 
GROUP BY user_id;
```

## Architecture Flow

```
Mobile App → Register Token → Backend → Supabase
                                    ↓
Backend Trigger → Send Notification → Firebase → Mobile Device
```

## Testing Tips

1. **Use Firebase Console**: Test messages from Firebase Console first
2. **Check Logs**: Look for "Firebase initialized" message on startup
3. **Verify Token**: Ensure FCM token is current (they can expire)
4. **Test Platforms**: Android, iOS, and Web have different token formats

## Links

- Full Guide: [FCM_NOTIFICATIONS_GUIDE.md](./FCM_NOTIFICATIONS_GUIDE.md)
- Firebase Console: https://console.firebase.google.com/
- Database Schema: [../db_schemas/token_notification_FCM.sql](../db_schemas/token_notification_FCM.sql)
