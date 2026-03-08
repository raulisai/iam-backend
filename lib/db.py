import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are in .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def get_supabase() -> Client:
    """Returns a real Supabase client instance using environment variables."""
    # Load inside if not already loaded, but it's usually better at top level.
    # We fetch them here to ensure they are available after potentially being set in .env
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
        
    # Clean up quotes if they were added manually in .env
    url = url.strip("'\" ")
    key = key.strip("'\" ")
    
    return create_client(url, key)


# Compatibility layer if needed (mimicking the original DBResult logic)
# Note: The real supabase client returns objects that have a .data attribute
# so no wrapper is strictly needed if we just return create_client().
# But if the code expects a .error attribute or something similar, we keep it simple.
