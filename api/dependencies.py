import logging
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

logger = logging.getLogger(__name__)

security = HTTPBearer(
    scheme_name="Bearer Token",
    description="Enter JWT token from /auth/token",
    auto_error=False
)

HEADERS = {
    "Host": "app.ecourts.gov.in",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 7 Build/BP3A.250905.014)",
    "Accept-Encoding": "gzip",
    "Accept-Charset": "UTF-8",
    "Connection": "keep-alive",
}


def get_http_client() -> httpx.Client:
    return httpx.Client(headers=HEADERS, timeout=20, follow_redirects=True)


async def get_auth_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization required. Use 'Authorization: Bearer <token>' in request header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token cannot be empty",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials
