from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.services.supabase_client import get_supabase

router = APIRouter()


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


@router.get("/login")
async def get_login_url(redirect_to: str = "http://localhost:3000/auth/callback"):
    """Generate the Google OAuth URL via Supabase Auth."""
    sb = get_supabase()
    response = sb.auth.sign_in_with_oauth(
        {
            "provider": "google",
            "options": {"redirect_to": redirect_to},
        }
    )
    return {"url": response.url}


@router.post("/callback")
async def auth_callback(access_token: str, refresh_token: str):
    """Exchange tokens from Supabase OAuth callback."""
    sb = get_supabase()
    try:
        response = sb.auth.set_session(access_token, refresh_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user": {
            "id": response.user.id,
            "email": response.user.email,
            "name": response.user.user_metadata.get("full_name", ""),
            "avatar_url": response.user.user_metadata.get("avatar_url", ""),
        },
    }


@router.post("/refresh")
async def refresh_session(body: RefreshRequest):
    """Refresh an expired session using the refresh token."""
    sb = get_supabase()
    try:
        response = sb.auth.refresh_session(body.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
    }


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return user


@router.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    """Sign out the current user."""
    sb = get_supabase()
    try:
        sb.auth.sign_out()
    except Exception:
        pass
    return {"message": "logged out"}
