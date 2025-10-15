# ✅ FCM Notifications - Setup Checklist

Use this checklist to ensure your notification system is properly configured and working.

## 🔧 Backend Setup

### 1. Dependencies
- [ ] Install firebase-admin: `pip install -r requirements.txt`
- [ ] Verify installation: `python -c "import firebase_admin; print('OK')"`

### 2. Firebase Configuration
- [ ] Download Firebase service account JSON from [Firebase Console](https://console.firebase.google.com/)
  - Go to Project Settings → Service Accounts
  - Click "Generate New Private Key"
  - Save the JSON file securely
- [ ] Add to `.env` file:
  ```bash
  FIREBASE_SERVICE_ACCOUNT=/path/to/firebase-service-account.json
  ```
- [ ] For production (Render/Heroku), set as environment variable:
  ```bash
  FIREBASE_SERVICE_ACCOUNT='{"type":"service_account",...}'
  ```

### 3. Database Schema
- [ ] Open Supabase SQL Editor
- [ ] Run the contents of `db_schemas/token_notification_FCM.sql`
- [ ] Verify table created:
  ```sql
  SELECT * FROM device_tokens LIMIT 1;
  ```
- [ ] Check indexes exist:
  ```sql
  SELECT indexname FROM pg_indexes WHERE tablename = 'device_tokens';
  ```

### 4. Application
- [ ] Routes registered in `app.py` (already done ✅)
- [ ] Restart application: `python app.py`
- [ ] Check logs for: `"Firebase Admin SDK initialized successfully"`
- [ ] No Firebase errors in console

### 5. Test Backend
- [ ] Get a JWT token (login to your app)
- [ ] Test token registration:
  ```bash
  curl -X POST http://localhost:5000/api/notification/register-token \
    -H "Authorization: Bearer YOUR_JWT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"token":"test-token-123","platform":"android"}'
  ```
- [ ] Should return 201 status with success message
- [ ] Check Supabase: token should appear in `device_tokens` table

---

## 📱 Mobile App Setup

### Android
- [ ] Add Firebase to your Android project
- [ ] Download `google-services.json` from Firebase Console
- [ ] Place in `app/` directory
- [ ] Add dependencies in `build.gradle`
- [ ] Create `MyFirebaseMessagingService` (see `MOBILE_APP_INTEGRATION_EXAMPLES.md`)
- [ ] Update `AndroidManifest.xml`
- [ ] Initialize `NotificationManager` in `MainActivity`
- [ ] Request POST_NOTIFICATIONS permission (Android 13+)
- [ ] Test: FCM token should be printed in logcat

### iOS
- [ ] Add Firebase to your iOS project
- [ ] Download `GoogleService-Info.plist` from Firebase Console
- [ ] Add to Xcode project
- [ ] Install Firebase pods: `pod install`
- [ ] Configure `AppDelegate.swift`
- [ ] Add `UIBackgroundModes` to `Info.plist`
- [ ] Request notification permission
- [ ] Test: FCM token should be printed in console

### React Native
- [ ] Install packages: `npm install @react-native-firebase/app @react-native-firebase/messaging`
- [ ] Link native modules: `cd ios && pod install`
- [ ] Add Firebase config files (both Android and iOS)
- [ ] Create `NotificationService.js`
- [ ] Initialize in `App.js`
- [ ] Test: Check console for token registration

---

## 🧪 Testing

### 1. Token Registration
- [ ] Open mobile app
- [ ] Login with valid credentials
- [ ] Check app logs: "✅ FCM token registered successfully"
- [ ] Verify in Supabase: token exists in `device_tokens` table
- [ ] User ID matches logged-in user
- [ ] Platform is correct (android/ios/web)

### 2. Send Test Notification (Backend)
- [ ] Use cURL or Postman:
  ```bash
  curl -X POST http://localhost:5000/api/notification/send \
    -H "Authorization: Bearer YOUR_JWT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "your-user-uuid",
      "title": "Test Notification",
      "body": "Hello from backend!",
      "data": {"test": true}
    }'
  ```
- [ ] Response status: 200
- [ ] Response contains success_count > 0
- [ ] Notification received on device

### 3. Send Test Notification (Firebase Console)
- [ ] Go to Firebase Console → Cloud Messaging
- [ ] Click "Send your first message"
- [ ] Enter title and body
- [ ] Select your app
- [ ] Paste FCM token
- [ ] Send test message
- [ ] Notification received on device

### 4. End-to-End Test
Create a scenario that triggers a notification:
- [ ] Complete a task in your app
- [ ] Backend sends notification via `send_notification_to_user()`
- [ ] Notification appears on device
- [ ] Tapping notification opens correct screen
- [ ] Notification data is passed correctly

---

## 🔍 Verification

### Backend Health Checks
```python
# Check Firebase initialization
from lib.firebase_client import _firebase_app
print("Firebase initialized:", _firebase_app is not None)

# Check database
from lib.db import get_supabase
supabase = get_supabase()
tokens = supabase.from_('device_tokens').select('count').execute()
print(f"Total tokens: {tokens.data[0]['count']}")
```

### Database Queries
```sql
-- Active tokens count
SELECT COUNT(*) FROM device_tokens WHERE is_active = true;

-- Tokens per user
SELECT user_id, COUNT(*) as token_count 
FROM device_tokens 
WHERE is_active = true 
GROUP BY user_id;

-- Recent registrations
SELECT * FROM device_tokens 
ORDER BY created_at DESC 
LIMIT 10;

-- Platform distribution
SELECT platform, COUNT(*) as count 
FROM device_tokens 
WHERE is_active = true 
GROUP BY platform;
```

---

## 🚨 Troubleshooting

### Firebase Not Initialized
**Symptom:** "Firebase Admin SDK not initialized" error

**Checks:**
- [ ] `FIREBASE_SERVICE_ACCOUNT` exists in `.env`
- [ ] Path is correct (if using file path)
- [ ] JSON is valid (if using JSON string)
- [ ] Service account has Firebase Admin SDK permissions
- [ ] Restart application after adding variable

**Fix:**
```bash
# Verify environment variable
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('FIREBASE_SERVICE_ACCOUNT'))"
```

### Token Not Saving
**Symptom:** 500 error when registering token

**Checks:**
- [ ] Database schema applied
- [ ] `device_tokens` table exists
- [ ] User ID is valid UUID
- [ ] Supabase connection working
- [ ] Check backend logs for error details

**Fix:**
```sql
-- Verify table exists
SELECT EXISTS (
  SELECT FROM information_schema.tables 
  WHERE table_schema = 'public' 
  AND table_name = 'device_tokens'
);
```

### Notifications Not Received
**Symptom:** Send returns 200 but no notification

**Checks:**
- [ ] FCM token is current (not expired)
- [ ] Device has internet connection
- [ ] App has notification permissions enabled
- [ ] App is registered in Firebase Console
- [ ] Check Firebase Console → Cloud Messaging → Reports
- [ ] Token marked as `is_active = true` in database

**Fix:**
1. Delete old token from device
2. Uninstall/reinstall app
3. Get new FCM token
4. Re-register token

### 401 Unauthorized
**Symptom:** All endpoints return 401

**Checks:**
- [ ] JWT token is valid and not expired
- [ ] Authorization header format: `Bearer YOUR_TOKEN`
- [ ] Token included in request headers
- [ ] User exists in database

**Fix:**
```bash
# Test JWT token
curl -X GET http://localhost:5000/api/notification/tokens \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📊 Monitoring

### Application Logs
```bash
# View Firebase initialization
tail -f logs/app.log | grep -i firebase

# View notification sends
tail -f logs/app.log | grep -i notification
```

### Firebase Console
- [ ] Check Cloud Messaging → Reports
- [ ] View delivery statistics
- [ ] Check for invalid tokens
- [ ] Monitor send quota

### Database Analytics
```sql
-- Daily registrations
SELECT DATE(created_at) as date, COUNT(*) as registrations
FROM device_tokens
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Token activity
SELECT 
  COUNT(*) FILTER (WHERE is_active = true) as active_tokens,
  COUNT(*) FILTER (WHERE is_active = false) as inactive_tokens,
  COUNT(*) as total_tokens
FROM device_tokens;
```

---

## ✅ Success Criteria

Your notification system is working correctly when:

1. ✅ Application starts without Firebase errors
2. ✅ Token registration returns 201 status
3. ✅ Tokens appear in Supabase `device_tokens` table
4. ✅ Send endpoint returns 200 with success_count > 0
5. ✅ Notification appears on mobile device
6. ✅ Tapping notification opens app with correct data
7. ✅ Multiple devices per user work correctly
8. ✅ Invalid tokens are automatically deactivated
9. ✅ Bulk notifications work for multiple users
10. ✅ No errors in application logs

---

## 📚 Additional Resources

- **Implementation Summary**: `NOTIFICATION_IMPLEMENTATION_SUMMARY.md`
- **Complete Guide**: `Documentation/FCM_NOTIFICATIONS_GUIDE.md`
- **Quick Reference**: `Documentation/FCM_QUICK_REFERENCE.md`
- **Mobile Integration**: `Documentation/MOBILE_APP_INTEGRATION_EXAMPLES.md`
- **Database Schema**: `db_schemas/token_notification_FCM.sql`

---

## 🎉 Ready to Deploy?

Before deploying to production:

- [ ] All tests passing
- [ ] Firebase credentials configured in production environment
- [ ] Database schema applied to production database
- [ ] CORS configured for production frontend URL
- [ ] Rate limiting configured (if needed)
- [ ] Monitoring and alerting set up
- [ ] Documentation updated with production URLs
- [ ] Mobile apps use production API URL

---

**Need Help?** Check the troubleshooting section above or review the complete guide in `Documentation/FCM_NOTIFICATIONS_GUIDE.md`.
