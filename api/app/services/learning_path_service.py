from datetime import datetime, timezone

from app.services.supabase_client import get_supabase_admin


def list_paths(user_id: str) -> list[dict]:
    sb = get_supabase_admin()
    result = (
        sb.table("learning_paths")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data or []


def create_path(user_id: str, name: str, status: str = "active") -> dict:
    sb = get_supabase_admin()
    result = (
        sb.table("learning_paths")
        .insert(
            {
                "user_id": user_id,
                "name": name,
                "status": status,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .execute()
    )
    return result.data[0]


def update_path(path_id: str, user_id: str, updates: dict) -> dict | None:
    sb = get_supabase_admin()
    filtered = {k: v for k, v in updates.items() if v is not None}
    if not filtered:
        return None
    result = (
        sb.table("learning_paths")
        .update(filtered)
        .eq("id", path_id)
        .eq("user_id", user_id)
        .execute()
    )
    return result.data[0] if result.data else None


def delete_path(path_id: str, user_id: str) -> bool:
    sb = get_supabase_admin()
    result = (
        sb.table("learning_paths")
        .delete()
        .eq("id", path_id)
        .eq("user_id", user_id)
        .execute()
    )
    return bool(result.data)
