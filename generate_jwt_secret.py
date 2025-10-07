#!/usr/bin/env python3
"""
Generate a secure JWT secret key for production use.
Run this script and copy the output to your Render environment variables.
"""

import secrets

def generate_jwt_secret():
    """Generate a cryptographically secure random string for JWT secret."""
    # Generate 64 random bytes and convert to hex (128 characters)
    secret_key = secrets.token_hex(32)
    return secret_key

if __name__ == "__main__":
    print("=" * 80)
    print("🔐 JWT Secret Key Generator")
    print("=" * 80)
    print()
    print("Generated secure JWT secret key:")
    print()
    print(f"  {generate_jwt_secret()}")
    print()
    print("=" * 80)
    print("Copy this value to your Render environment variable: JWT_SECRET_KEY")
    print("=" * 80)
