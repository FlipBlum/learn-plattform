from datetime import datetime, timedelta, timezone

from app.services.supabase_client import get_supabase_admin


def list_videos(
    source: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    sb = get_supabase_admin()
    query = sb.table("videos").select("*", count="exact")

    if source:
        query = query.eq("source", source)

    query = query.order("discovered_at", desc=True).range(offset, offset + limit - 1)
    result = query.execute()

    return {"videos": result.data, "total": result.count or 0}


def get_new_videos(days: int = 7) -> dict:
    sb = get_supabase_admin()
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    result = (
        sb.table("videos")
        .select("*", count="exact")
        .gte("discovered_at", since)
        .order("discovered_at", desc=True)
        .execute()
    )

    return {"videos": result.data, "total": result.count or 0}
