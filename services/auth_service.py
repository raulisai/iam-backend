"""Authentication service for password verification and security utilities."""
import bcrypt


def verify_password(hashed_password, password):
    """Verify the given password against the hashed password.
    
    Args:
        hashed_password (str): The hashed password.
        password (str): The password to verify.
    
    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def hash_password(password):
    """Hash a password for storing.
    
    Args:
        password (str): The password to hash.
    
    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()
