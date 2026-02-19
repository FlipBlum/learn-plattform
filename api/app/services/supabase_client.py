from supabase import Client, create_client

from app.core.config import settings

_client: Client | None = None
_admin_client: Client | None = None


def get_supabase() -> Client:
    """Return a Supabase client using the anon key (respects RLS)."""
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client


def get_supabase_admin() -> Client:
    """Return a Supabase client using the service-role key (bypasses RLS)."""
    global _admin_client
    if _admin_client is None:
        _admin_client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _admin_client
