"""Firebase Admin SDK client for FCM notifications."""
import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, messaging

load_dotenv()

# Initialize Firebase Admin SDK
_firebase_app = None


def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials."""
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    try:
        # Try to get credentials from environment variable (JSON string or file path)
        firebase_creds = os.getenv("FIREBASE_SERVICE_ACCOUNT")
        
        if not firebase_creds:
            print("Warning: FIREBASE_SERVICE_ACCOUNT not found in environment variables")
            return None
        
        # Check if it's a file path or JSON string
        if os.path.isfile(firebase_creds):
            cred = credentials.Certificate(firebase_creds)
        else:
            # Parse as JSON string
            cred_dict = json.loads(firebase_creds)
            cred = credentials.Certificate(cred_dict)
        
        _firebase_app = firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully")
        return _firebase_app
    
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {str(e)}")
        return None


class FirebaseInitializationError(RuntimeError):
    """Raised when the Firebase Admin SDK is not initialized."""
    pass


def send_message_to_token(token, title, body, data=None):
    """Send a push notification to a specific device token.
    
    Args:
        token (str): FCM device token.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    
    Returns:
        str: Message ID if successful.
    
    Raises:
        FirebaseInitializationError: If the Firebase Admin SDK is not initialized.
    """
    if _firebase_app is None:
        initialize_firebase()
    
    if _firebase_app is None:
        raise FirebaseInitializationError("Firebase Admin SDK not initialized")
    
    # Build the message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=token,
        android=messaging.AndroidConfig(
            priority='high',
            notification=messaging.AndroidNotification(
                sound='default',
                priority='high',
            )
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound='default',
                    badge=1,
                )
            )
        )
    )
    
    # Send the message
    try:
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending message to token {token}: {str(e)}")
        raise


def send_multicast_message(tokens, title, body, data=None):
    """Send a push notification to multiple device tokens.
    
    Args:
        tokens (list): List of FCM device tokens.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.
    
    Returns:
        dict: Response with success count and failed tokens.
    """
    if _firebase_app is None:
        initialize_firebase()
    
    if _firebase_app is None:
        raise Exception("Firebase Admin SDK not initialized")
    
    if not tokens:
        return {"success_count": 0, "failure_count": 0, "failed_tokens": []}
    
    # Build reusable pieces for each per-token message
    notification = messaging.Notification(
        title=title,
        body=body,
    )
    android_conf = messaging.AndroidConfig(
        priority='high',
        notification=messaging.AndroidNotification(
            sound='default',
            priority='high',
        )
    )
    apns_conf = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                sound='default',
                badge=1,
            )
        )
    )
    
    # Try available batching methods: send_all, then send_multicast, then per-token fallback
    try:
        # If send_all exists (older API), build individual Message objects and use it
        if hasattr(messaging, "send_all"):
            messages = [
                messaging.Message(
                    notification=notification,
                    data=data or {},
                    token=tok,
                    android=android_conf,
                    apns=apns_conf
                )
                for tok in tokens
            ]
            response = messaging.send_all(messages)
            failed_tokens = []
            if getattr(response, "failure_count", 0) > 0:
                for idx, resp in enumerate(getattr(response, "responses", [])):
                    if not getattr(resp, "success", False):
                        failed_tokens.append(tokens[idx])
            return {
                "success_count": getattr(response, "success_count", 0),
                "failure_count": getattr(response, "failure_count", 0),
                "failed_tokens": failed_tokens
            }

        # If send_multicast exists, use MulticastMessage
        elif hasattr(messaging, "send_multicast") and hasattr(messaging, "MulticastMessage"):
            multicast = messaging.MulticastMessage(
                notification=notification,
                data=data or {},
                tokens=tokens,
                android=android_conf,
                apns=apns_conf
            )
            response = messaging.send_multicast(multicast)
            failed_tokens = []
            if getattr(response, "failure_count", 0) > 0:
                for idx, resp in enumerate(getattr(response, "responses", [])):
                    if not getattr(resp, "success", False):
                        failed_tokens.append(tokens[idx])
            return {
                "success_count": getattr(response, "success_count", 0),
                "failure_count": getattr(response, "failure_count", 0),
                "failed_tokens": failed_tokens
            }

        # Fallback: send each message individually and aggregate results
        else:
            success_count = 0
            failure_count = 0
            failed_tokens = []
            for tok in tokens:
                msg = messaging.Message(
                    notification=notification,
                    data=data or {},
                    token=tok,
                    android=android_conf,
                    apns=apns_conf
                )
                try:
                    messaging.send(msg)
                    success_count += 1
                except Exception:
                    failure_count += 1
                    failed_tokens.append(tok)
            return {
                "success_count": success_count,
                "failure_count": failure_count,
                "failed_tokens": failed_tokens
            }

    except Exception as e:
        print(f"Error sending multicast message: {str(e)}")
        raise


# Initialize on module import
initialize_firebase()
