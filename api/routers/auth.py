import logging
import httpx
from fastapi import APIRouter, Depends

from scraper.auth_manager import get_jwt_token
from api.schemas import AuthTokenResponse, ErrorResponse
from api.dependencies import get_http_client

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=AuthTokenResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Generate JWT Token"
)
async def get_token(client: httpx.Client = Depends(get_http_client)) -> dict:
    try:
        token = get_jwt_token(client)
        
        if token is None:
            return {
                "status": "error",
                "code": 500,
                "message": "Failed to generate token"
            }
        
        return {
            "status": "success",
            "code": 200,
            "message": "Token generated. Use in Authorization header",
            "data": {"token": token}
        }
    except Exception as e:
        logger.error(f"Token generation error: {e}")
        return {
            "status": "error",
            "code": 500,
            "message": f"Failed to generate token: {str(e)}"
        }
    finally:
        client.close()
