"""Lightweight shared API-key guard for integration routers.

Set NOSHOW_API_KEY in the environment; clients send it in the X-API-Key
header. If unset, the guard is disabled (local dev only). These endpoints
handle patient-shaped data and should never be exposed anonymously in prod.
"""
import os

from fastapi import Header, HTTPException, status

_API_KEY = os.getenv("NOSHOW_API_KEY", "").strip()


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not _API_KEY:
        return  # dev mode: no key configured
    if not x_api_key or x_api_key != _API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key.",
        )