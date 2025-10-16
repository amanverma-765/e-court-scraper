"""
Dependencies for FastAPI routes.
"""

import logging
import httpx
from fastapi import Depends, HTTPException, status

from scraper.auth_manager import get_jwt_token
from utils.constants import BASE_URL

logger = logging.getLogger(__name__)

# HTTP Client configuration
HEADERS = {
    "Host": "app.ecourts.gov.in",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 7 Build/BP3A.250905.014)",
    "Accept-Encoding": "gzip",
    "Accept-Charset": "UTF-8",
    "Connection": "keep-alive",
}

# Global HTTP client
_http_client: httpx.Client | None = None


def get_http_client() -> httpx.Client:
    """Get or create HTTP client."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.Client(headers=HEADERS, timeout=20, follow_redirects=True)
    return _http_client


def close_http_client() -> None:
    """Close the HTTP client."""
    global _http_client
    if _http_client is not None:
        _http_client.close()
        _http_client = None


async def get_auth_token(client: httpx.Client = Depends(get_http_client)) -> str:
    """
    Dependency to get JWT token.
    
    Raises:
        HTTPException: If token retrieval fails
    """
    try:
        token = get_jwt_token(client)
        if token is None:
            logger.error("Failed to fetch JWT token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to authenticate with e-courts API"
            )
        return token
    except Exception as e:
        logger.error(f"Token retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate with e-courts API"
        )
