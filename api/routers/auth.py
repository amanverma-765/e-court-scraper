"""
Authentication routes for the API.
"""

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
    responses={
        500: {"model": ErrorResponse, "description": "Failed to generate token"},
    },
    summary="Generate JWT Token",
    description="""Generate a JWT token for authenticating with e-courts API.
    
    This token should be used in the Authorization header for all subsequent API requests:
    `Authorization: Bearer <token>`
    
    The token is used to authenticate requests to e-courts backend services."""
)
async def get_token(client: httpx.Client = Depends(get_http_client)) -> dict:
    """
    Generate JWT token for API authentication.
    
    The generated token must be passed in the Authorization header for all other endpoints.
    
    Returns:
        dict: Contains the JWT token to be used in Authorization header
        
    Raises:
        HTTPException: If token generation fails
    """
    try:
        logger.info("Generating JWT token")
        token = get_jwt_token(client)
        
        if token is None:
            logger.error("Token generation failed: returned None")
            return {
                "status": "error",
                "code": 500,
                "message": "Failed to generate authentication token"
            }
        
        logger.info("JWT token generated successfully")
        return {
            "status": "success",
            "code": 200,
            "message": "Token generated successfully. Use this token in Authorization header as 'Bearer <token>' for all API requests",
            "data": {"token": token}
        }
    except Exception as e:
        logger.error(f"Token generation error: {e}", exc_info=True)
        return {
            "status": "error",
            "code": 500,
            "message": f"Failed to generate token: {str(e)}"
        }
    finally:
        # Close the client after use since it's per-request
        client.close()
