import base64
import re
from datetime import datetime, timezone

from db import get_supabase

LINK_PATTERN = re.compile(r'https?://[^\s<>"\']+')


def _get_gmail_service():
    """Build the Gmail API service using stored credentials."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    from config import GMAIL_CREDENTIALS_PATH

    creds = Credentials.from_authorized_user_file(
        GMAIL_CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    )
    return build("gmail", "v1", credentials=creds)


def _extract_links_from_body(payload: dict) -> list[str]:
    """Recursively extract links from email body parts."""
    links: list[str] = []
    if payload.get("body", {}).get("data"):
        text = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
        links.extend(LINK_PATTERN.findall(text))
    for part in payload.get("parts", []):
        links.extend(_extract_links_from_body(part))
    return links


def _parse_messages(service, max_results: int = 50) -> list[dict]:
    """Fetch recent messages and extract subject + links."""
    results = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results, q="newer_than:1d")
        .execute()
    )
    messages = results.get("messages", [])
    parsed: list[dict] = []

    for msg_ref in messages:
        msg = service.users().messages().get(userId="me", id=msg_ref["id"], format="full").execute()
        headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
        subject = headers.get("subject", "(kein Betreff)")
        sender = headers.get("from", "")
        links = list(set(_extract_links_from_body(msg["payload"])))

        parsed.append(
            {
                "subject": subject,
                "sender": sender,
                "links": links,
                "snippet": msg.get("snippet", ""),
            }
        )

    return parsed


def run():
    """Parse Gmail inbox for learning content and store in news_sources."""
    print("Running gmail_parser job...")
    try:
        service = _get_gmail_service()
    except Exception as e:
        print(f"Gmail auth failed: {e}")
        return

    parsed = _parse_messages(service)
    if not parsed:
        print("No new emails found")
        return

    sb = get_supabase()
    now = datetime.now(timezone.utc).isoformat()

    for item in parsed:
        sb.table("news_sources").insert(
            {
                "source_type": "gmail",
                "title": item["subject"],
                "content": item["snippet"],
                "links": item["links"],
                "raw_data": item,
                "fetched_at": now,
            }
        ).execute()

    print(f"Gmail parser: stored {len(parsed)} email entries")
