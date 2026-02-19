from datetime import date, datetime, timezone

from app.services.supabase_client import get_supabase_admin


def list_news_pages(limit: int = 30, offset: int = 0) -> dict:
    sb = get_supabase_admin()
    result = (
        sb.table("news_pages")
        .select("*", count="exact")
        .order("date", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return {"pages": result.data, "total": result.count or 0}


def get_news_by_date(target_date: date) -> dict | None:
    sb = get_supabase_admin()
    result = (
        sb.table("news_pages").select("*").eq("date", target_date.isoformat()).single().execute()
    )
    return result.data


def get_latest_news() -> dict | None:
    sb = get_supabase_admin()
    today = datetime.now(timezone.utc).date().isoformat()
    result = sb.table("news_pages").select("*").eq("date", today).execute()
    if result.data:
        return result.data[0]

    result = (
        sb.table("news_pages").select("*").order("date", desc=True).limit(1).execute()
    )
    return result.data[0] if result.data else None
