"""
Dependencies for FastAPI routes.
"""

import logging
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from utils.constants import BASE_URL

logger = logging.getLogger(__name__)

# Security scheme for Swagger UI
security = HTTPBearer(
    scheme_name="Bearer Token",
    description="Enter your JWT token (obtained from POST /auth/token endpoint)",
    auto_error=False
)

# HTTP Client configuration
HEADERS = {
    "Host": "app.ecourts.gov.in",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 7 Build/BP3A.250905.014)",
    "Accept-Encoding": "gzip",
    "Accept-Charset": "UTF-8",
    "Connection": "keep-alive",
}


def get_http_client() -> httpx.Client:
    """
    Create a new HTTP client for each request.
    This ensures each user context has its own isolated HTTP client.
    """
    return httpx.Client(headers=HEADERS, timeout=20, follow_redirects=True)


async def get_auth_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Dependency to extract and validate JWT token from Authorization header.
    
    This function works with FastAPI's HTTPBearer security scheme, which automatically:
    - Extracts the Bearer token from the Authorization header
    - Provides Swagger UI integration with the 🔓 Authorize button
    - Validates the token format
    
    Args:
        credentials: HTTP Bearer credentials from the Authorization header
    
    Returns:
        str: Plain JWT token (not encrypted)
    
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not credentials:
        logger.error("Authorization header missing or invalid")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required. Use the 🔓 Authorize button in Swagger UI or include 'Authorization: Bearer <token>' header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    if not token:
        logger.error("Token is empty")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token cannot be empty",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info("JWT token extracted successfully from Authorization header")
    return token
