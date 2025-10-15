# 📱 Mobile App Integration Examples

## Android (Kotlin) - Complete Integration

### 1. Add Firebase to your project

**build.gradle (project level):**
```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

**build.gradle (app level):**
```gradle
plugins {
    id 'com.google.gms.google-services'
}

dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.7.0')
    implementation 'com.google.firebase:firebase-messaging-ktx'
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
}
```

### 2. Create FCM Service

**MyFirebaseMessagingService.kt:**
```kotlin
package com.yourapp.services

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.yourapp.MainActivity
import com.yourapp.R

class MyFirebaseMessagingService : FirebaseMessagingService() {

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Send token to your backend
        sendTokenToBackend(token)
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        // Handle notification
        remoteMessage.notification?.let {
            showNotification(it.title ?: "", it.body ?: "", remoteMessage.data)
        }
    }

    private fun sendTokenToBackend(token: String) {
        // This will be implemented in NotificationManager
        NotificationManager.registerToken(this, token)
    }

    private fun showNotification(title: String, body: String, data: Map<String, String>) {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channelId = "default_channel"
        
        // Create notification channel for Android O+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Default Notifications",
                NotificationManager.IMPORTANCE_HIGH
            )
            notificationManager.createNotificationChannel(channel)
        }
        
        // Create intent for notification tap
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            putExtra("notification_data", data.toString())
        }
        
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        
        // Build notification
        val notification = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .build()
        
        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }
}
```

### 3. Create Notification Manager

**NotificationManager.kt:**
```kotlin
package com.yourapp.managers

import android.content.Context
import android.os.Build
import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

object NotificationManager {
    
    private const val BASE_URL = "https://your-api.com"
    private val client = OkHttpClient()
    
    fun initialize(context: Context) {
        requestNotificationPermission(context)
        getAndRegisterToken(context)
    }
    
    private fun requestNotificationPermission(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            // Request notification permission on Android 13+
            // This should be done in your Activity/Fragment
        }
    }
    
    fun getAndRegisterToken(context: Context) {
        FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                val token = task.result
                registerToken(context, token)
            }
        }
    }
    
    fun registerToken(context: Context, token: String) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val jwtToken = getJwtToken(context) ?: return@launch
                
                val json = JSONObject().apply {
                    put("token", token)
                    put("platform", "android")
                    put("device_info", JSONObject().apply {
                        put("model", Build.MODEL)
                        put("manufacturer", Build.MANUFACTURER)
                        put("os_version", "Android ${Build.VERSION.RELEASE}")
                        put("app_version", getAppVersion(context))
                    })
                }
                
                val body = json.toString()
                    .toRequestBody("application/json".toMediaType())
                
                val request = Request.Builder()
                    .url("$BASE_URL/api/notification/register-token")
                    .addHeader("Authorization", "Bearer $jwtToken")
                    .post(body)
                    .build()
                
                client.newCall(request).execute().use { response ->
                    if (response.isSuccessful) {
                        println("✅ FCM token registered successfully")
                    } else {
                        println("❌ Failed to register FCM token: ${response.code}")
                    }
                }
            } catch (e: Exception) {
                println("❌ Error registering FCM token: ${e.message}")
            }
        }
    }
    
    fun removeToken(context: Context, token: String) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val jwtToken = getJwtToken(context) ?: return@launch
                
                val json = JSONObject().apply {
                    put("token", token)
                    put("hard_delete", false)
                }
                
                val body = json.toString()
                    .toRequestBody("application/json".toMediaType())
                
                val request = Request.Builder()
                    .url("$BASE_URL/api/notification/remove-token")
                    .addHeader("Authorization", "Bearer $jwtToken")
                    .post(body)
                    .build()
                
                client.newCall(request).execute().use { response ->
                    if (response.isSuccessful) {
                        println("✅ FCM token removed successfully")
                    }
                }
            } catch (e: Exception) {
                println("❌ Error removing FCM token: ${e.message}")
            }
        }
    }
    
    private fun getJwtToken(context: Context): String? {
        val prefs = context.getSharedPreferences("auth", Context.MODE_PRIVATE)
        return prefs.getString("jwt_token", null)
    }
    
    private fun getAppVersion(context: Context): String {
        return try {
            val packageInfo = context.packageManager.getPackageInfo(context.packageName, 0)
            packageInfo.versionName
        } catch (e: Exception) {
            "1.0.0"
        }
    }
}
```

### 4. Update AndroidManifest.xml

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
    
    <application>
        <!-- Your activities -->
        
        <!-- FCM Service -->
        <service
            android:name=".services.MyFirebaseMessagingService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT"/>
            </intent-filter>
        </service>
        
        <!-- Notification metadata -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_icon"
            android:resource="@drawable/ic_notification"/>
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_color"
            android:resource="@color/notification_color"/>
    </application>
</manifest>
```

### 5. Initialize in MainActivity

```kotlin
class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Initialize notifications
        NotificationManager.initialize(this)
        
        // Request permission on Android 13+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            requestPermissions(
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                1001
            )
        }
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 1001 && grantResults.isNotEmpty() && 
            grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            NotificationManager.getAndRegisterToken(this)
        }
    }
}
```

---

## iOS (Swift) - Complete Integration

### 1. Add Firebase to your project

**Package.swift or Podfile:**
```ruby
# Using CocoaPods
pod 'Firebase/Messaging'
```

Or use Swift Package Manager with Firebase iOS SDK.

### 2. Configure AppDelegate

**AppDelegate.swift:**
```swift
import UIKit
import Firebase
import FirebaseMessaging
import UserNotifications

@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Initialize Firebase
        FirebaseApp.configure()
        
        // Set FCM delegate
        Messaging.messaging().delegate = self
        
        // Request notification permission
        UNUserNotificationCenter.current().delegate = self
        let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
        UNUserNotificationCenter.current().requestAuthorization(options: authOptions) { granted, error in
            if granted {
                print("✅ Notification permission granted")
            }
        }
        
        application.registerForRemoteNotifications()
        
        return true
    }
    
    func application(_ application: UIApplication,
                     didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
        Messaging.messaging().apnsToken = deviceToken
    }
}

// MARK: - MessagingDelegate
extension AppDelegate: MessagingDelegate {
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        guard let token = fcmToken else { return }
        print("📱 FCM Token: \(token)")
        
        // Register token with backend
        NotificationService.shared.registerToken(token: token)
    }
}

// MARK: - UNUserNotificationCenterDelegate
extension AppDelegate: UNUserNotificationCenterDelegate {
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        // Show notification even when app is in foreground
        completionHandler([[.banner, .sound, .badge]])
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        let userInfo = response.notification.request.content.userInfo
        print("📩 Notification tapped with data: \(userInfo)")
        
        // Handle notification tap
        handleNotificationTap(userInfo: userInfo)
        
        completionHandler()
    }
    
    private func handleNotificationTap(userInfo: [AnyHashable: Any]) {
        // Navigate to specific screen based on notification data
        if let taskId = userInfo["task_id"] as? String {
            // Navigate to task detail
        }
    }
}
```

### 3. Create Notification Service

**NotificationService.swift:**
```swift
import Foundation
import Firebase

class NotificationService {
    static let shared = NotificationService()
    
    private let baseURL = "https://your-api.com"
    
    private init() {}
    
    func registerToken(token: String) {
        guard let jwtToken = KeychainHelper.getJwtToken() else {
            print("❌ No JWT token found")
            return
        }
        
        let deviceInfo: [String: Any] = [
            "model": UIDevice.current.model,
            "os_version": "iOS \(UIDevice.current.systemVersion)",
            "app_version": Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
        ]
        
        let parameters: [String: Any] = [
            "token": token,
            "platform": "ios",
            "device_info": deviceInfo
        ]
        
        guard let url = URL(string: "\(baseURL)/api/notification/register-token") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(jwtToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONSerialization.data(withJSONObject: parameters)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("❌ Error registering token: \(error.localizedDescription)")
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 201 {
                print("✅ FCM token registered successfully")
            } else {
                print("❌ Failed to register FCM token")
            }
        }.resume()
    }
    
    func removeToken(token: String) {
        guard let jwtToken = KeychainHelper.getJwtToken() else { return }
        
        let parameters: [String: Any] = [
            "token": token,
            "hard_delete": false
        ]
        
        guard let url = URL(string: "\(baseURL)/api/notification/remove-token") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(jwtToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONSerialization.data(withJSONObject: parameters)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                print("✅ FCM token removed successfully")
            }
        }.resume()
    }
}

// Helper for Keychain
class KeychainHelper {
    static func getJwtToken() -> String? {
        // Implement keychain retrieval
        return UserDefaults.standard.string(forKey: "jwt_token")
    }
}
```

### 4. Add to Info.plist

```xml
<key>UIBackgroundModes</key>
<array>
    <string>remote-notification</string>
</array>
<key>FirebaseAppDelegateProxyEnabled</key>
<false/>
```

---

## React Native - Complete Integration

### 1. Install packages

```bash
npm install @react-native-firebase/app @react-native-firebase/messaging
npm install @react-native-async-storage/async-storage axios
```

### 2. Create Notification Service

**services/NotificationService.js:**
```javascript
import messaging from '@react-native-firebase/messaging';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { Platform } from 'react-native';
import DeviceInfo from 'react-native-device-info';

const BASE_URL = 'https://your-api.com';

class NotificationService {
  async initialize() {
    await this.requestPermission();
    await this.registerToken();
    this.setupListeners();
  }

  async requestPermission() {
    const authStatus = await messaging().requestPermission();
    const enabled =
      authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
      authStatus === messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
      console.log('✅ Notification permission granted');
    } else {
      console.log('❌ Notification permission denied');
    }
  }

  async registerToken() {
    try {
      const fcmToken = await messaging().getToken();
      const jwtToken = await AsyncStorage.getItem('jwt_token');

      if (!jwtToken) {
        console.log('❌ No JWT token found');
        return;
      }

      const deviceInfo = {
        model: await DeviceInfo.getModel(),
        manufacturer: await DeviceInfo.getManufacturer(),
        os_version: `${Platform.OS} ${await DeviceInfo.getSystemVersion()}`,
        app_version: DeviceInfo.getVersion(),
      };

      const response = await axios.post(
        `${BASE_URL}/api/notification/register-token`,
        {
          token: fcmToken,
          platform: Platform.OS,
          device_info: deviceInfo,
        },
        {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.status === 201) {
        console.log('✅ FCM token registered successfully');
      }
    } catch (error) {
      console.log('❌ Error registering FCM token:', error.message);
    }
  }

  async removeToken() {
    try {
      const fcmToken = await messaging().getToken();
      const jwtToken = await AsyncStorage.getItem('jwt_token');

      const response = await axios.post(
        `${BASE_URL}/api/notification/remove-token`,
        {
          token: fcmToken,
          hard_delete: false,
        },
        {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.status === 200) {
        console.log('✅ FCM token removed successfully');
      }
    } catch (error) {
      console.log('❌ Error removing FCM token:', error.message);
    }
  }

  setupListeners() {
    // Handle background messages
    messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('📩 Background message:', remoteMessage);
    });

    // Handle foreground messages
    messaging().onMessage(async remoteMessage => {
      console.log('📩 Foreground message:', remoteMessage);
      // Show custom notification or alert
    });

    // Handle notification tap (app opened from quit state)
    messaging().onNotificationOpenedApp(remoteMessage => {
      console.log('📱 Notification opened app:', remoteMessage);
      this.handleNotificationTap(remoteMessage);
    });

    // Check if app was opened from a notification
    messaging()
      .getInitialNotification()
      .then(remoteMessage => {
        if (remoteMessage) {
          console.log('📱 App opened from notification:', remoteMessage);
          this.handleNotificationTap(remoteMessage);
        }
      });

    // Handle token refresh
    messaging().onTokenRefresh(async token => {
      console.log('🔄 FCM token refreshed');
      await this.registerToken();
    });
  }

  handleNotificationTap(remoteMessage) {
    const { data } = remoteMessage;
    
    if (data?.task_id) {
      // Navigate to task detail
      // navigation.navigate('TaskDetail', { taskId: data.task_id });
    }
  }
}

export default new NotificationService();
```

### 3. Initialize in App.js

**App.js:**
```javascript
import React, { useEffect } from 'react';
import NotificationService from './services/NotificationService';

function App() {
  useEffect(() => {
    // Initialize notifications
    NotificationService.initialize();
  }, []);

  return (
    // Your app components
  );
}

export default App;
```

---

## 🧪 Testing

### Test notification from backend:

```bash
curl -X POST http://localhost:5000/api/notification/send \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid-here",
    "title": "Test Notification 🎉",
    "body": "This is a test from the backend!",
    "data": {
      "test": true,
      "timestamp": "2025-01-15T10:30:00Z"
    }
  }'
```

### Test from Firebase Console:

1. Go to Firebase Console → Cloud Messaging
2. Click "Send your first message"
3. Enter notification details
4. Select your app
5. Send test message to your FCM token

---

¡Listo! Your mobile app is now fully integrated with the FCM notification system! 🚀
