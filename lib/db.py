"""Database module for the Flask application."""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import httpx

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Create Supabase client first
supabase: Client = create_client(url, key)

# Get the original session configuration
original_session = supabase.postgrest.session

# Create a new httpx client with HTTP/2 disabled but keep the original configuration
custom_http_client = httpx.Client(
    base_url=original_session.base_url,  # Keep the base URL
    headers=original_session.headers,    # Keep the headers (auth token, etc.)
    http2=False,  # Disable HTTP/2 to avoid WinError 10035 on Windows
    timeout=httpx.Timeout(30.0, connect=10.0),  # Set reasonable timeouts
    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
)

# Replace the session with our custom one
supabase.postgrest.session = custom_http_client


def get_supabase():
    """Return the Supabase client."""
    return supabase
