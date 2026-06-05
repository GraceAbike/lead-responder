import base64
import hashlib
import hmac
import os
from fastapi import Request, Response
from sqlalchemy.orm import Session
from . import models

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or os.getenv("DASHBOARD_PASSWORD", "changeme")
SECRET_KEY = os.getenv("SECRET_KEY", "replace_with_a_strong_secret")


def hash_password(password: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hmac.compare_digest(hash_password(password), password_hash)


def _admin_session_token() -> str:
    """Generate admin session token."""
    digest = hmac.new(SECRET_KEY.encode(), ADMIN_PASSWORD.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode()


def is_admin_authenticated(request: Request) -> bool:
    """Check if request is from an authenticated admin."""
    token = request.cookies.get("admin_session")
    if not token:
        return False
    return hmac.compare_digest(token, _admin_session_token())


def is_client_authenticated(request: Request) -> bool:
    """Check if request is from an authenticated client."""
    token = request.cookies.get("client_session")
    return bool(token)


def get_client_id_from_session(request: Request, db: Session) -> int:
    """Extract and validate client_id from session token."""
    token = request.cookies.get("client_session")
    if not token:
        return None
    
    try:
        client_id_str = base64.urlsafe_b64decode(token.encode()).decode()
        return int(client_id_str)
    except:
        return None


def admin_login_response(response: Response) -> Response:
    """Set admin session cookie."""
    response.set_cookie("admin_session", _admin_session_token(), httponly=True, samesite="lax", max_age=86400*7)
    response.delete_cookie("client_session")
    return response


def admin_logout_response(response: Response) -> Response:
    """Clear admin session cookie."""
    response.delete_cookie("admin_session")
    return response


def client_login_response(response: Response, client_id: int) -> Response:
    """Set client session cookie."""
    token = base64.urlsafe_b64encode(str(client_id).encode()).decode()
    response.set_cookie("client_session", token, httponly=True, samesite="lax", max_age=86400*7)
    response.delete_cookie("admin_session")
    return response


def client_logout_response(response: Response) -> Response:
    """Clear client session cookie."""
    response.delete_cookie("client_session")
    return response


def verify_admin_password(password: str) -> bool:
    """Verify admin password."""
    return password == ADMIN_PASSWORD

