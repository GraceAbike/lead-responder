import base64
import hashlib
import hmac
import os
from fastapi import Request, Response

DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "changeme")
SECRET_KEY = os.getenv("SECRET_KEY", "replace_with_a_strong_secret")


def _session_token() -> str:
    digest = hmac.new(SECRET_KEY.encode(), DASHBOARD_PASSWORD.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode()


def is_authenticated(request: Request) -> bool:
    token = request.cookies.get("session")
    if not token:
        return False
    return hmac.compare_digest(token, _session_token())


def login_response(response: Response) -> Response:
    response.set_cookie("session", _session_token(), httponly=True, samesite="lax")
    return response


def logout_response(response: Response) -> Response:
    response.delete_cookie("session")
    return response


def verify_password(password: str) -> bool:
    return password == DASHBOARD_PASSWORD
